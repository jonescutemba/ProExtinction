# Pro Extinction · Website-Redesign (Konzeptphase)

Zwei Designkonzepte (A Ember, B Poster; C Ring wurde verworfen) für die Seite, in 29 Sprachen (EN, DE, PL, ES, IT sowie die komplett KI-übersetzten FR, PT, RU, ZH, HI, AR, BN, UR, ID, JA, TR, VI, KO, FA, MR, TE, TA, SW, TH, NL, UK, TL, PA, GU; Arabisch, Urdu und Persisch von rechts nach links), Hell und Dunkel.
**Die Konzeptwahl steht noch aus:** `DECISIONS.md`.

| Pfad | Inhalt |
|---|---|
| **`presentation/`** | **Eine einzige Seite für Kundentermine (live-fähig):** Design B, 29 Sprachen, Hell/Dunkel (Design A versteckt: viermal schnell auf „Global“ in der Fußzeile klicken). Schriften lokal in `fonts/` |
| `DEPLOY.md`, `vercel.json` | Livegang auf Vercel, Checkliste |
| `concepts/index.html` | Vorläufer: die Konzepte als getrennte Mehrseiten-Prototypen |
| `brand/` | je Konzept ein Brand Kit (Tokens, `BRAND.md`, Referenzseiten) |
| `content/` | Text als JSON pro Sprache (`en/ de/ pl/ es/ it/`): Originaltext der jeweiligen Sprachseite plus KI-Übersetzungen der fehlenden Seiten (welche das sind, steht in `SITE` in `tools/build.py`) |
| `content/diagrams/` | Texte der zwei Manifest-Grafiken (Kreislauf des Leidens, Grausames Design mit allen Beispielen) pro Sprache, eine Zeile pro Text, Felder mit `|` getrennt; `en.txt` ist die Vorlage (`tools/diagrams.py`, `tools/dg.js`) |
| `raw/` | Rohtext der Google-Sites-Seiten PL/ES/IT (`tools/scrape.py`, dann `tools/parse_raw.py`) |
| `tools/` | Generator: `build.py` (Seiten), `kit.py` (Kits), `blocks.py`, `parse.py`, CSS-Quellen |
| `DECISIONS.md` | was entschieden und was offen ist |

Bauen: `python tools/build_all.py` (Windows, Mac, Linux; unter Mac/Linux ggf. `python3`). Danach `concepts/index.html` im Browser öffnen.
Das ist ein Prototyp: Google-Fonts-Einbindung und Auszüge/Platzhalter sind noch nicht für den Livegang gedacht.

## Präsentationsseite für Kunden
`presentation/index.html` ist **eine Seite** mit allen Ansichten (kein Server nötig; `fonts/` muss daneben liegen). Livegang: siehe `DEPLOY.md`.
Oben rechts: **A Ember · B Poster** (Design), **EN ▾** (Sprachauswahl; Seiten mit "(AI)" sind KI-Übersetzungen aus dem Englischen), **Hell/Dunkel**. Die Auswahl bleibt gespeichert.

Direktlinks für einzelne Varianten (an die Adresse hängen):
- Design: Standard ist B; `?concept=a` oder `?concept=b` erzwingt eins (wird gespeichert) · Modus: `&theme=light` oder `&theme=dark`
- Seite: `#/en/manifesto`, `#/de/manifest`, `#/en/full-faq` …
- Beispiel: `index.html?concept=b&theme=dark#/en/manifesto`
- Logo-Effekt testen: `?scare=reset` (Zähler zurück), `?motion=on` (trotz „Bewegung reduzieren")

Versteckte Effekte (`tools/smoke.js`, `tools/eggs.js`): Rauch am Ende langer Seiten; Sterne, die auf „Cosmic Extinction“ beim Lesen verlöschen; Logo fünfmal schnell anklicken (die Seite verblasst, der letzte Satz des Manifests erscheint); Geburtenzähler in der Fusszeile (Menschen, ~Nutztiere, ~Wildtiere, ~Insekten; grobe Schätzungen aus Jahreszahlen, `BORN` in `tools/build.py`); Gruss in der Browser-Konsole. Mit „Bewegung reduzieren“ nur sanfte Überblendungen.
