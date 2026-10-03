# Pro Extinction · Website-Redesign (Konzeptphase)

Drei Designkonzepte für die Seite, jeweils EN und DE, Hell und Dunkel.
**Die Konzeptwahl steht noch aus:** `DECISIONS.md`.

| Pfad | Inhalt |
|---|---|
| `concepts/index.html` | Einstieg: die drei Konzepte nebeneinander öffnen |
| `brand/` | je Konzept ein Brand Kit (Tokens, `BRAND.md`, Referenzseiten) |
| `content/` | gescrapter Originaltext als JSON (`en/`, `de/`); `_translation-pending/` = Entwürfe, nicht eingebaut |
| `tools/` | Generator: `build.py` (Seiten), `kit.py` (Kits), `blocks.py`, `parse.py`, CSS-Quellen |
| `DECISIONS.md` | was entschieden und was offen ist |

Bauen: `python3 tools/build.py && python3 tools/kit.py`. Danach `concepts/index.html` im Browser öffnen.
Das ist ein Prototyp: Google-Fonts-Einbindung und Auszüge/Platzhalter sind noch nicht für den Livegang gedacht.
