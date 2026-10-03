# Pro Extinction · Website-Redesign (Konzeptphase)

Drei Designkonzepte für die Seite, jeweils EN und DE, Hell und Dunkel.
**Die Konzeptwahl steht noch aus:** `DECISIONS.md`.

| Pfad | Inhalt |
|---|---|
| **`presentation/index.html`** | **Eine einzige Seite für Kundentermine:** alle drei Designs, EN/DE, Hell/Dunkel, per Umschalter oben rechts |
| `concepts/index.html` | Vorläufer: die drei Konzepte als getrennte Mehrseiten-Prototypen |
| `brand/` | je Konzept ein Brand Kit (Tokens, `BRAND.md`, Referenzseiten) |
| `content/` | gescrapter Originaltext als JSON (`en/`, `de/`); `_translation-pending/` = Entwürfe, nicht eingebaut |
| `tools/` | Generator: `build.py` (Seiten), `kit.py` (Kits), `blocks.py`, `parse.py`, CSS-Quellen |
| `DECISIONS.md` | was entschieden und was offen ist |

Bauen: `python3 tools/build.py && python3 tools/present.py && python3 tools/kit.py`. Danach `concepts/index.html` im Browser öffnen.
Das ist ein Prototyp: Google-Fonts-Einbindung und Auszüge/Platzhalter sind noch nicht für den Livegang gedacht.

## Präsentationsseite für Kunden
`presentation/index.html` ist eine **einzelne, in sich geschlossene Datei** (kein Server nötig, nur Internet für die Schriften).
Oben rechts: **A Ember · B Poster · C Ring** (Design), **EN/DE** (Sprache), **Hell/Dunkel**. Die Auswahl bleibt gespeichert.

Direktlinks für einzelne Varianten (an die Adresse hängen):
- Design: `?concept=a`, `?concept=b` oder `?concept=c` · Modus: `&theme=light` oder `&theme=dark`
- Seite: `#/en/manifesto`, `#/de/manifest`, `#/en/full-faq` …
- Beispiel: `index.html?concept=b&theme=dark#/en/manifesto`
- Logo-Effekt testen: `?scare=reset` (Zähler zurück), `?motion=on` (trotz „Bewegung reduzieren")
