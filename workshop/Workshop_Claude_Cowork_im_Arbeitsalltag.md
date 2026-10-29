# Workshop-Konzept: „Claude Cowork im Arbeitsalltag“

**Zielgruppe:** eine Fachabteilung ohne Programmierkenntnisse (z. B. Kundenservice oder Vertrieb)
**Dauer:** 60 Minuten · **Teilnehmende:** 6–12 · **Format:** vor Ort oder hybrid, alle mit eigenem Laptop
**Ziel:** Alle gehen mit **einer konkreten Aufgabe** raus, die sie ab morgen mit Claude Cowork schneller erledigen.

---

## Ablauf

| Zeit | Block | Inhalt | Methode |
|---|---|---|---|
| 0–5 | Einstieg | Kurze Runde: „Welche Aufgabe nervt Dich jede Woche?“ – Antworten auf Post-its sammeln | Blitzlicht |
| 5–15 | Was ist Cowork? | Unterschied Chat vs. Cowork: Cowork **arbeitet** – liest Dateien, erstellt Dokumente, nutzt Tools (z. B. Mail, Kalender, Drive) und zeigt den Fortschritt in einer Aufgabenliste | Live-Demo |
| 15–30 | Übung 1 | Aus einem Ordner mit 10 Beispiel-Kundenmails eine Übersicht erstellen lassen: Kategorie, Dringlichkeit, Antwortentwurf | Paararbeit |
| 30–45 | Übung 2 | Eigene Aufgabe vom Post-it mit Cowork lösen – ich gehe von Tisch zu Tisch | Einzelarbeit + Coaching |
| 45–55 | Gute Prompts & sicherer Umgang | Die 4-Teile-Formel (unten) · Was darf rein, was nicht (Datenschutz) · Ergebnisse immer prüfen | Kurzinput + Fragen |
| 55–60 | Abschluss | Jede:r nennt die eine Aufgabe für morgen · Spickzettel verteilen · Feedback (1–5) | Runde |

---

## Die 4-Teile-Formel für gute Aufträge

1. **Rolle:** „Du bist Assistenz im Kundenservice …“
2. **Aufgabe:** „Sortiere diese Mails nach Thema und Dringlichkeit.“
3. **Material:** „Die Mails liegen im Ordner *Anfragen_Oktober*.“
4. **Ergebnis:** „Erstelle eine Tabelle mit Spalten Thema, Priorität, Antwortentwurf.“

## Regeln für den sicheren Umgang

- Keine Passwörter, Bankdaten oder unnötigen personenbezogenen Daten eingeben – interne Datenschutzvorgaben gelten.
- KI-Ergebnisse sind **Entwürfe**: Fakten, Zahlen und Ton vor dem Versenden prüfen.
- Bei Aktionen mit Außenwirkung (Mail senden, Termin anlegen) lässt Cowork Dich bestätigen – bewusst lesen, dann freigeben.

## Spickzettel (1 Seite für die Teilnehmenden)

- „Fasse diese Datei in 5 Stichpunkten zusammen.“
- „Erstelle aus diesen Notizen ein Protokoll mit Aufgaben, Verantwortlichen und Terminen.“
- „Schreibe drei Varianten einer freundlichen Antwort auf diese Kundenmail – kurz, in Du-Form.“
- „Vergleiche diese zwei Tabellen und markiere Unterschiede.“

## Erfolgsmessung

- Feedback-Skala direkt nach dem Workshop (Ziel: Ø ≥ 4 von 5)
- Nach 2 Wochen kurze Umfrage: Wie viele nutzen Cowork mindestens 1× pro Woche? Welche Aufgabe spart am meisten Zeit?
- Beste Beispiele sammeln und als interne Anleitungen veröffentlichen

## Verbindung zum Python-Prototyp

Übung 1 zeigt das Prinzip ohne Code. Der Prototyp `sortierer.py` im selben Repository zeigt, wie dieselbe Aufgabe automatisiert in eine bestehende Systemlandschaft eingebunden werden kann (CSV rein → Kategorien, Prioritäten und Bericht raus).
