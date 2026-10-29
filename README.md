# KI-Anfragen-Sortierer

Kleiner Python-Prototyp: Kundenanfragen eines Internetanbieters werden automatisch
**kategorisiert** (Störung, Rechnung, Vertrag, Umzug, Tarif, Sonstiges), nach **Priorität** eingestuft,
**zusammengefasst** und mit einem **Antwortvorschlag** versehen. Am Ende entsteht ein kurzer Bericht.

Dazu gehört ein Workshop-Konzept, das zeigt, wie Fachabteilungen dieselbe Aufgabe ohne Code mit
**Claude Cowork** lösen: [`workshop/Workshop_Claude_Cowork_im_Arbeitsalltag.md`](workshop/Workshop_Claude_Cowork_im_Arbeitsalltag.md)

## Zwei Modi

| Modus | Was passiert | Voraussetzung |
|---|---|---|
| `regel` | Einordnung über Schlüsselwörter – läuft offline | nur Python |
| `claude` | Claude (Anthropic API) ordnet ein und formuliert die Antwort | `ANTHROPIC_API_KEY` |

Kommt von der KI kein gültiges JSON zurück, fällt das Programm automatisch auf den Regel-Modus zurück.

## Starten

```bash
pip install -r requirements.txt
python sortierer.py daten/anfragen.csv --mode regel
# mit Claude:
export ANTHROPIC_API_KEY=...        # eigener Key
python sortierer.py daten/anfragen.csv --mode claude
```

Ergebnis: `ausgabe/ergebnis.csv` und `ausgabe/bericht.md`

## Mit Docker

```bash
docker build -t sortierer .
docker run --rm sortierer
```

## Tests

```bash
pytest -q
```

## Aufbau

```
sortierer.py            Programm (Regel- und Claude-Modus, Bericht)
daten/anfragen.csv      fiktive Beispielanfragen
tests/                  Unit-Tests
workshop/               Workshop-Konzept „Claude Cowork im Arbeitsalltag“
Dockerfile              Container-Version
```

Autor: Osama Khalifa · Die Beispieldaten sind frei erfunden.
