# Livegang auf Vercel

**Was live geht:** der Ordner `presentation/` (`index.html`, `fonts/`, `favicon.svg`, `robots.txt`).
Es gibt keinen Build-Schritt. Die Konfiguration steht in `vercel.json` (Ausgabeordner, Sicherheits-Header,
Cache für Schriften). Die Seite ist ein statischer Entwurf zum Vorlegen, **bewusst auf „noindex"**.

## Einrichten (einmalig, im Vercel-Dashboard)
1. vercel.com → **Add New… → Project** → GitHub-Repository `appsofuse/proextinction` importieren.
2. **Framework Preset: Other.** Build Command, Install Command und Output Directory leer lassen
   (kommt aus `vercel.json`, Ausgabeordner ist `presentation`).
3. **Deploy.** Die Adresse sieht aus wie `proextinction-….vercel.app`.
4. Branch: Die Arbeit liegt auf `claude/amazing-pascal-ej4vzp`. Vercel baut jeden Branch als **Preview**.
   Für die Produktions-Adresse entweder diesen Branch nach `main` mergen oder unter
   *Settings → Git → Production Branch* den Branch eintragen.

Alternativ per Kommandozeile im Repo-Ordner: `npm i -g vercel`, dann `vercel` (Preview) oder `vercel --prod`.

## Vor dem Teilen prüfen
| Punkt | Stand |
|---|---|
| Suchmaschinen | gesperrt: Meta-Tag, `X-Robots-Tag`-Header, `robots.txt`. Zum Freischalten alle drei entfernen (`tools/present.py`, `vercel.json`, `presentation/robots.txt`) und neu bauen |
| Zugriffsschutz | Die Adresse ist öffentlich erreichbar, nur nicht gelistet. Passwortschutz bietet Vercel in bezahlten Plänen (*Deployment Protection*); sonst Adresse nur direkt an Kunden geben |
| Vercel-Tarif | Der kostenlose Hobby-Tarif ist laut Vercel nur für nicht-kommerzielle Nutzung. Für Kundenarbeit den Pro-Tarif nehmen oder einen anderen statischen Host (Cloudflare Pages, Netlify, GitHub Pages: derselbe Ordner `presentation/`) |
| Schriften | lokal gehostet, kein Google-Abruf (Lizenz OFL, `presentation/fonts/licenses/`) |
| Impressum, Datenschutz | **fehlen.** Für eine öffentliche deutsche Seite nötig. Für einen unverlinkten Entwurf unkritischer, vor einem echten Livegang einplanen. Keine Rechtsberatung |
| Inhalte | Texte, Name, Logo und Spenden-IBAN stammen unverändert von der Original-Seite. Vorher sicherstellen, dass der Auftraggeber der Veröffentlichung zustimmt |
| Telefonnummer | steht auf der deutschen Startseite (Wunsch), vor Livegang bestätigen lassen |
| Fehlende DE-Seiten | 4 Seiten fehlen noch (Übersetzung ist ein eigener Schritt) |

## Aktualisieren
Nach Änderungen: `python3 tools/build.py && python3 tools/present.py && python3 tools/kit.py`,
Ergebnis committen und pushen. Vercel veröffentlicht automatisch neu.

## Schriften neu beziehen
Quelle: npm-Pakete `@fontsource/*` (Oswald, Newsreader, Anton, Barlow, Bebas Neue, Source Serif 4, JetBrains Mono).
Verwendet werden nur `latin` und `latin-ext`, `woff2`. Die `@font-face`-Regeln stehen in `tools/fonts.css`.
