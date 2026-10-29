import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sortierer import einordnen_regel


def test_stoerung_ist_dringend():
    e = einordnen_regel("1", "Seit gestern kein Internet, ich brauche es dringend")
    assert e.kategorie == "Störung"
    assert e.prioritaet == "hoch"


def test_rechnung():
    assert einordnen_regel("2", "Falscher Betrag auf der Rechnung").kategorie == "Rechnung"


def test_unbekannt_wird_sonstiges():
    assert einordnen_regel("3", "Vielen Dank für alles!").kategorie == "Sonstiges"
