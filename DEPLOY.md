# Livegang auf Vercel

**Was live geht:** der Ordner `site/`: eine Datei pro Seite, dazu Sprachwahl, 404-Seite, Sitemap, `robots.txt`, Schriften und Bilder.
Es gibt keinen Build-Schritt. Die Konfiguration steht in `vercel.json` (Ausgabeordner, Sicherheits-Header,
Cache für Schriften). Die Seite ist statisch und als finale Version gebaut, aber noch **bewusst auf „noindex"**.

## Einrichten (einmalig, im Vercel-Dashboard)
1. vercel.com → **Add New… → Project** → GitHub-Repository `appsofuse/proextinction` importieren.
2. **Framework Preset: Other.** Build Command, Install Command und Output Directory leer lassen
   (kommt aus `vercel.json`, Ausgabeordner ist `site`).
3. **Deploy.** Die Adresse sieht aus wie `proextinction-….vercel.app`.
4. Branch: Die Arbeit liegt auf `claude/amazing-pascal-ej4vzp`. Vercel baut jeden Branch als **Preview**.
   Für die Produktions-Adresse entweder diesen Branch nach `main` mergen oder unter
   *Settings → Git → Production Branch* den Branch eintragen.

Alternativ per Kommandozeile im Repo-Ordner: `npm i -g vercel`, dann `vercel` (Preview) oder `vercel --prod`.

## Vor dem Teilen prüfen
| Punkt | Stand |
|---|---|
| Suchmaschinen | gesperrt. Freischalten: in `tools/build.py` `INDEXABLE = True` setzen, `python tools/build_all.py`, committen. Das ändert Meta-Tag, `X-Robots-Tag`-Header (`vercel.json`) und `robots.txt` zusammen. Vorher Impressum und Datenschutz ausfüllen |
| Domain | `SITE_URL` in `tools/build.py` (`https://proextinction.com`). In Vercel unter *Settings → Domains* eintragen, die www-Variante auf die Domain ohne www umleiten lassen |
| Zugriffsschutz | Die Adresse ist öffentlich erreichbar, nur nicht gelistet. Passwortschutz bietet Vercel in bezahlten Plänen (*Deployment Protection*); sonst Adresse nur direkt an Kunden geben |
| Vercel-Tarif | Der kostenlose Hobby-Tarif ist laut Vercel nur für nicht-kommerzielle Nutzung. Für Kundenarbeit den Pro-Tarif nehmen oder einen anderen statischen Host (Cloudflare Pages, Netlify, GitHub Pages: derselbe Ordner `presentation/`) |
| Schriften | lokal gehostet, kein Google-Abruf (Lizenz OFL, `site/fonts/licenses/`) |
| Impressum, Datenschutz | **Entwurf** in `content/legal/de.json` und `en.json`, im Footer jeder Seite verlinkt. Die Angaben in eckigen Klammern (Name, Anschrift, Verantwortliche Person, Stand) fehlen noch. Keine Rechtsberatung: vor Livegang prüfen lassen |
| Inhalte | Texte, Name, Logo und Spenden-IBAN stammen unverändert von der Original-Seite. Vorher sicherstellen, dass der Auftraggeber der Veröffentlichung zustimmt |
| Telefonnummer | steht auf der deutschen Startseite (Wunsch), vor Livegang bestätigen lassen |
| Fehlende DE-Seiten | 4 Seiten fehlen noch (Übersetzung ist ein eigener Schritt) |

## Aktualisieren
Nach Änderungen: `python tools/build_all.py`,
Ergebnis committen und pushen. Vercel veröffentlicht automatisch neu.

## Schriften neu beziehen
Quelle: npm-Pakete `@fontsource/*` (Oswald, Newsreader, Anton, Barlow, Bebas Neue, Source Serif 4, JetBrains Mono).
Verwendet werden nur `latin` und `latin-ext`, `woff2`. Die `@font-face`-Regeln stehen in `tools/fonts.css`.
