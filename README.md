# Pro Extinction · Website-Redesign (Konzeptphase)

Zwei Designkonzepte (A Ember, B Poster; C Ring wurde verworfen) für die Seite, in 24 Sprachen (EN, DE, PL, ES, IT sowie die komplett KI-übersetzten FR, PT, RU, ZH, HI, AR, BN, UR, ID, JA, TR, VI, KO, FA, MR, TE, TA, SW, TH; Arabisch, Urdu und Persisch von rechts nach links), Hell und Dunkel.
**Die Konzeptwahl steht noch aus:** `DECISIONS.md`.

| Pfad | Inhalt |
|---|---|
| **`presentation/`** | **Eine einzige Seite für Kundentermine (live-fähig):** beide Designs, 24 Sprachen, Hell/Dunkel, per Umschalter oben rechts. Schriften lokal in `fonts/` |
| `DEPLOY.md`, `vercel.json` | Livegang auf Vercel, Checkliste |
| `concepts/index.html` | Vorläufer: die Konzepte als getrennte Mehrseiten-Prototypen |
| `brand/` | je Konzept ein Brand Kit (Tokens, `BRAND.md`, Referenzseiten) |
| `content/` | Text als JSON pro Sprache (`en/ de/ pl/ es/ it/`): Originaltext der jeweiligen Sprachseite plus KI-Übersetzungen der fehlenden Seiten (welche das sind, steht in `SITE` in `tools/build.py`) |
| `raw/` | Rohtext der Google-Sites-Seiten PL/ES/IT (`tools/scrape.py`, dann `tools/parse_raw.py`) |
| `tools/` | Generator: `build.py` (Seiten), `kit.py` (Kits), `blocks.py`, `parse.py`, CSS-Quellen |
| `DECISIONS.md` | was entschieden und was offen ist |

Bauen: `python tools/build_all.py` (Windows, Mac, Linux; unter Mac/Linux ggf. `python3`). Danach `concepts/index.html` im Browser öffnen.
Das ist ein Prototyp: Google-Fonts-Einbindung und Auszüge/Platzhalter sind noch nicht für den Livegang gedacht.

## Präsentationsseite für Kunden
`presentation/index.html` ist **eine Seite** mit allen Ansichten (kein Server nötig; `fonts/` muss daneben liegen). Livegang: siehe `DEPLOY.md`.
Oben rechts: **A Ember · B Poster** (Design), **EN ▾** (Sprachauswahl; Seiten mit "(AI)" sind KI-Übersetzungen aus dem Englischen), **Hell/Dunkel**. Die Auswahl bleibt gespeichert.

Direktlinks für einzelne Varianten (an die Adresse hängen):
- Design: `?concept=a`, `?concept=b` oder `?concept=c` · Modus: `&theme=light` oder `&theme=dark`
- Seite: `#/en/manifesto`, `#/de/manifest`, `#/en/full-faq` …
- Beispiel: `index.html?concept=b&theme=dark#/en/manifesto`
- Logo-Effekt testen: `?scare=reset` (Zähler zurück), `?motion=on` (trotz „Bewegung reduzieren")
