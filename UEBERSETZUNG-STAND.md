# Stand: 5 neue Sprachen (nl, uk, tl, pa, gu)

Auftrag: „bitte übersetze noch 5 weitere sprachen“. Gewählt nach Sprecherzahl: Niederländisch (nl), Ukrainisch (uk), Filipino (tl), Punjabi (pa), Gujarati (gu).
Stand vom 9. Oktober 2026. Branch: `claude/translations`. Die fertigen Seiten sind als Sicherung committet, aber noch nicht in den Build eingebaut. Die Website zeigt die 5 Sprachen also noch nicht.

## 1. Fertige Seiten

| Seite | nl | uk | tl | pa | gu |
|---|---|---|---|---|---|
| basic-faq, contact, donate, join-us | ✓ | ✓ | ✓ | ✓ | ✓ |
| history, social-media-channels, suffering-in-detail, cosmic-extinction | ✓ | ✓ | ✓ | ✓ | ✓ |
| manifesto, principles-of-the-movement | ✓ | ✓ | ✓ | ✓ | ✓ |
| full-faq | ✓ | ✓ | ✓ | ✓ | ✓ |
| criticism-of-different-pro-life-ideologies | ✓ | ✓ | ✓ | Zeilen 0–69 von 203 | offen |

Die fertigen Dateien liegen in `content/<sprache>/<seite>.json` (committet, aber nicht im Build).

## 2. Wo ich stehe

1. Punjabi, Criticism-Seite: Teil 1 (Zeilen 0–69, bis „Veganism“ einschließlich Zeile 69) ist übersetzt. Er liegt als Zwischenstand in `uebersetzung-wip/pa-criticism-of-different-pro-life-ideologies.json` (Zeilennummer als Schlüssel).
2. Als Nächstes: Punjabi Zeilen 70–139 (ab „So asking a person to be vegan…“ bis zur Überschrift „Feminism:“) und 140–202 (Feminismus bis Efilismus).
3. Danach: Gujarati, Criticism-Seite komplett (203 Zeilen, in drei Teilen 0–69, 70–139, 140–202).

## 3. Danach noch zu tun (Einbau in den Build)

1. `tools/build.py`: nl, uk, tl, pa, gu eintragen in `LANGS`, `FULL_AI`, `LANG_NAME`, `CODE`, `AI_MENU` (13 Menüpunkte je Sprache) und die UI-Texte in `T.update`.
2. Einträge in `VEIL` (Hinweis auf verschwommene Bilder), `GIVE` (Spendenkarten), `TOP` (Nach-oben-Knopf) und `FAQ_FIND` (FAQ-Suche).
3. `tools/css/base.css`: eigene `:lang`-Zeilenhöhe für pa und gu (Gurmukhi und Gujarati brauchen mehr Platz).
4. README.md und DECISIONS.md auf 29 Sprachen anpassen.
5. Build mit `tools/build_all.py`, dann prüfen: Zeilenzahl gleich Englisch, Gliederung und Inhaltsverzeichnis gleich wie Englisch, Screenshots mit ausgeblendeten Bildern.
6. Commit und Push nur nach `claude/translations`. Der Vercel-Branch bleibt unverändert.

## 4. Übersetzungsregeln, die gelten

1. Jede Sprache hat genau so viele Zeilen wie Englisch (1:1).
2. Kein Gedankenstrich (—), keine typografischen Anführungszeichen, einfache Wörter, aktive Sätze.
3. FAQ-Nummern bleiben wie im Englischen („1.“, „10.  “). Präfixe wie „a)“, „1)“, „* “ und „– “ bleiben.
4. URLs, Handles und Adressen bleiben unverändert.
5. Ich-Formen bleiben (nur auf „Cosmic Extinction“ umgeschrieben).
6. Fachbegriffe: nl „extinctionisme/uitsterving“, uk „екстинкціонізм/вимирання“, tl „extinctionism/extinction“, pa „ਵਿਲੁਪਤੀਵਾਦ/ਵਿਲੁਪਤੀ“, gu „વિલુપ્તિવાદ/વિલુપ્તિ“.

## 5. Werkzeuge (Kopie in `uebersetzung-wip/`, die Pfade darin zeigen auf das Scratchpad)

1. `tr/tw.py`: `save()` prüft Zeilenzahl, Gedankenstriche und Anführungszeichen; `part()` sammelt eine Seite in Teilen.
2. `tr/fromtxt.py <sprache> <seite> <startzeile> <datei.txt> [last]`: liest eine Textdatei (eine Zeile pro Absatz) und speichert sie als Teil.
