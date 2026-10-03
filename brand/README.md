# brand/

Drei Brand-Kit-Konzepte für Pro Extinction. **Welches gilt, ist offen** (siehe `../DECISIONS.md`).

| Ordner | Konzept |
|---|---|
| `a-ember/` | eckig, redaktionell, Leiste links, Rot/Schwarz/Silber, Serif |
| `b-poster/` | eckig, zentriert, Navbar oben, Rot/Schwarz/Silber, Sans |
| `c-ring/` | rund, Sepia und Tinte, Karte rechts, Serif |

Gemeinsam: `REFERENCE.md` (Rohfassung des Markeninterviews, mit Begründungen).
Jeder Konzeptordner hat `BRAND.md`, `CLAUDE.md`, `README.md`, `tokens.css`, `brand-helmet.html`,
`brand-props.json`, `wordmark.svg`, `mark.svg` und `beispiel/` mit allen Bausteinen (Desktop und mobil).

Neu erzeugen nach Änderungen an `tokens.css`: `python3 tools/build.py && python3 tools/kit.py`.
