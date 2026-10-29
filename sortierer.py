"""KI-Anfragen-Sortierer
Ordnet Kundenanfragen (z. B. eines Internetanbieters) automatisch einer Kategorie
und Priorität zu, fasst sie kurz zusammen und schlägt eine Antwort vor.

Zwei Modi:
  regel   – einfache Schlüsselwort-Regeln, läuft offline ohne API-Key
  claude  – Claude (Anthropic API) übernimmt die Einordnung

Aufruf:
  python sortierer.py daten/anfragen.csv --mode regel
  python sortierer.py daten/anfragen.csv --mode claude   (ANTHROPIC_API_KEY nötig)
"""

import argparse
import csv
import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path

KATEGORIEN = ["Störung", "Rechnung", "Vertrag", "Umzug", "Tarif", "Sonstiges"]

# Schlüsselwörter je Kategorie für den Offline-Modus
REGELN = {
    "Störung": ["kein internet", "störung", "ausfall", "langsam", "wlan", "router", "verbindung"],
    "Rechnung": ["rechnung", "abbuchung", "lastschrift", "betrag", "zu viel", "gutschrift"],
    "Vertrag": ["kündigen", "kündigung", "vertrag", "laufzeit", "widerruf"],
    "Umzug": ["umzug", "ziehe um", "neue adresse", "umziehen"],
    "Tarif": ["tarif", "glasfaser", "upgrade", "schneller", "angebot", "gbit", "mbit"],
}
DRINGEND = ["sofort", "dringend", "homeoffice", "seit tagen", "kein internet", "notfall"]

ANTWORT_VORLAGEN = {
    "Störung": "Danke für Deine Meldung! Bitte starte Deinen Router einmal neu. Besteht die Störung weiter, prüfen wir Deinen Anschluss sofort.",
    "Rechnung": "Danke für Deine Nachricht! Wir prüfen Deine Rechnung und melden uns innerhalb von zwei Werktagen.",
    "Vertrag": "Danke für Deine Anfrage! Gern informieren wir Dich zu Laufzeit und Kündigungsfristen Deines Vertrags.",
    "Umzug": "Danke! Teile uns bitte Deine neue Adresse und Dein Umzugsdatum mit, dann prüfen wir die Verfügbarkeit.",
    "Tarif": "Danke für Dein Interesse! Wir prüfen gern, welche Tarife an Deiner Adresse verfügbar sind.",
    "Sonstiges": "Danke für Deine Nachricht! Wir leiten sie an das passende Team weiter.",
}


@dataclass
class Ergebnis:
    id: str
    kategorie: str
    prioritaet: str
    zusammenfassung: str
    antwortvorschlag: str


def kurzfassung(text: str, max_woerter: int = 12) -> str:
    woerter = text.split()
    return " ".join(woerter[:max_woerter]) + (" …" if len(woerter) > max_woerter else "")


def einordnen_regel(anfrage_id: str, text: str) -> Ergebnis:
    t = text.lower()
    punkte = {k: sum(w in t for w in woerter) for k, woerter in REGELN.items()}
    kategorie = max(punkte, key=punkte.get)
    if punkte[kategorie] == 0:
        kategorie = "Sonstiges"
    prioritaet = "hoch" if any(w in t for w in DRINGEND) else "normal"
    return Ergebnis(anfrage_id, kategorie, prioritaet, kurzfassung(text), ANTWORT_VORLAGEN[kategorie])


PROMPT = """Du bist Assistenz im Kundenservice eines Internetanbieters.
Ordne die Kundenanfrage ein und antworte NUR mit JSON in diesem Format:
{{"kategorie": eine von {kategorien}, "prioritaet": "hoch" oder "normal",
"zusammenfassung": max. 15 Wörter, "antwortvorschlag": 1–2 freundliche Sätze in Du-Form}}

Anfrage:
{text}"""


def einordnen_claude(client, modell: str, anfrage_id: str, text: str) -> Ergebnis:
    antwort = client.messages.create(
        model=modell,
        max_tokens=400,
        messages=[{"role": "user", "content": PROMPT.format(kategorien=KATEGORIEN, text=text)}],
    )
    roh = antwort.content[0].text.strip()
    roh = roh[roh.find("{"): roh.rfind("}") + 1]  # nur den JSON-Teil verwenden
    try:
        daten = json.loads(roh)
    except json.JSONDecodeError:
        return einordnen_regel(anfrage_id, text)  # Fallback, falls die KI kein gültiges JSON liefert
    kategorie = daten.get("kategorie") if daten.get("kategorie") in KATEGORIEN else "Sonstiges"
    return Ergebnis(anfrage_id, kategorie, daten.get("prioritaet", "normal"),
                    daten.get("zusammenfassung", kurzfassung(text)),
                    daten.get("antwortvorschlag", ANTWORT_VORLAGEN[kategorie]))


def lade_anfragen(pfad: Path) -> list[dict]:
    with open(pfad, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def speichere(ergebnisse: list[Ergebnis], ordner: Path) -> None:
    ordner.mkdir(exist_ok=True)
    with open(ordner / "ergebnis.csv", "w", encoding="utf-8", newline="") as f:
        schreiber = csv.DictWriter(f, fieldnames=list(asdict(ergebnisse[0]).keys()))
        schreiber.writeheader()
        schreiber.writerows(asdict(e) for e in ergebnisse)

    zeilen = ["# Auswertung Kundenanfragen", "", "| Kategorie | Anzahl | davon hoch |", "|---|---|---|"]
    for k in KATEGORIEN:
        gruppe = [e for e in ergebnisse if e.kategorie == k]
        if gruppe:
            zeilen.append(f"| {k} | {len(gruppe)} | {sum(e.prioritaet == 'hoch' for e in gruppe)} |")
    zeilen += ["", "## Dringende Anfragen", ""]
    zeilen += [f"- **#{e.id}** ({e.kategorie}): {e.zusammenfassung}" for e in ergebnisse if e.prioritaet == "hoch"]
    (ordner / "bericht.md").write_text("\n".join(zeilen) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Kundenanfragen mit KI einordnen")
    parser.add_argument("datei", type=Path, help="CSV mit den Spalten id,text")
    parser.add_argument("--mode", choices=["regel", "claude"], default="regel")
    parser.add_argument("--ausgabe", type=Path, default=Path("ausgabe"))
    args = parser.parse_args()

    anfragen = lade_anfragen(args.datei)
    if args.mode == "claude":
        import anthropic  # nur nötig, wenn der Claude-Modus genutzt wird
        client = anthropic.Anthropic()  # liest ANTHROPIC_API_KEY aus der Umgebung
        modell = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")
        ergebnisse = [einordnen_claude(client, modell, a["id"], a["text"]) for a in anfragen]
    else:
        ergebnisse = [einordnen_regel(a["id"], a["text"]) for a in anfragen]

    speichere(ergebnisse, args.ausgabe)
    for e in ergebnisse:
        print(f"#{e.id:>3} | {e.kategorie:<9} | {e.prioritaet:<6} | {e.zusammenfassung}")
    print(f"\nFertig: {len(ergebnisse)} Anfragen → {args.ausgabe}/ergebnis.csv und bericht.md")


if __name__ == "__main__":
    main()
