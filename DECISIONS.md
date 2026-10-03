# Entscheidungen · Pro Extinction Website-Redesign

Stand: laufend gepflegt. **Die Wahl des Konzepts ist bewusst offen und fällt später.**
Bis dahin werden alle drei Konzepte parallel gepflegt.

## Offen (später festlegen)
| Frage | Stand | Wann |
|---|---|---|
| **Welches Konzept gilt** (A Ember, B Poster, C Ring) oder eine Mischung | offen, nicht vorentschieden | nach dem Vergleich im Browser und der Rückmeldung von Beteiligten |
| Endgültige Hex-Werte | je Konzept vorläufig in `brand/<konzept>/tokens.css` | mit der Konzeptwahl |
| Original-Logo als Vektor | fehlt, `mark.svg` ist eine Nachzeichnung | sobald auffindbar |
| Schriften selbst hosten | noch Google Fonts (nur Prototyp) | vor Livegang, DSGVO |
| Bilder von „Suffering in detail" (16) | erste Runde ohne Fotos | nach der Konzeptwahl |
| Animationen (Staub am Seitenende, animiertes Logo) | Logo-Effekt vorhanden; Staub nicht gebaut | nach der Konzeptwahl |
| Deutsche Übersetzung der 4 fehlenden Seiten | Entwürfe in `content/_translation-pending/`, nicht eingebaut | eigener Schritt |
| Telefonnummer auf der deutschen Seite | bleibt (Wunsch), vor Livegang bestätigen | vor Livegang |
| Hosting und Domain der neuen Seite | nicht besprochen | nach der Konzeptwahl |

**Wie wir entscheiden:** Die Konzepte nebeneinander öffnen (`concepts/index.html`), dieselben
Seiten in Hell und Dunkel, EN und DE, auf Handy und Desktop ansehen. Danach ein Konzept
wählen, ggf. einzelne Bausteine aus einem anderen übernehmen, und das hier eintragen.
Erst dann gilt `brandkit-build` für das **gewählte** Kit als final und `brandkit-publish` baut die echte Seite.

## Entschieden (gilt für alle Konzepte)
1. **Marke:** Pro Extinction. „AbolishSuffering" bleibt nur der Discord-Name.
2. **Tagline:** „Together, we end suffering."
3. **Ziel:** Neulinge überzeugen, nicht die Community mobilisieren.
4. **Persönlichkeit:** ernst, rational, empathisch, entschlossen, ruhig-düster. Nicht reißerisch, esoterisch, verspielt, hoffnungslos.
5. **Modi:** Hell und Dunkel, umschaltbar per Button oben rechts.
6. **Sprachen der Konzepte:** EN und DE. Fehlende DE-Seiten per KI-Übersetzung, sichtbar gekennzeichnet. Tippfehler werden korrigiert.
7. **Inhalt:** Originaltext bleibt wörtlich. Neu geschrieben werden nur Buttons, Zwischenüberschriften, Hinweise (du-Ansprache, sachlich, Verbotsliste in `BRAND.md`).
8. **Farbe:** Akzent unter etwa 5 % der Fläche, Silber nur in Logo und Wordmark.
9. **Typografie:** schwere Versalien-Grotesk für Display, Mono sparsam, nie Inter oder Roboto als Hauptschrift. Wordmark als Schrift mit CSS-Metall, kein Flyer-Bild.
10. **Anmutung:** Leerraum, schmale Textspalte (68 ch), Körnung, Haarlinien, keine Schatten oder Glaseffekte.
11. **Signatur:** der rote Schrägstrich (Trenner, Fortschritt, Hover).
12. **Bausteine:** Navigation immer sichtbar (kein Hamburger-Menü), Kapitelübersicht, FAQ aufklappbar, Zitatblock, vier Efforts, Call-to-Action, Sprach- und Theme-Umschalter.
13. **Bilder:** Hauptbildsprache im Code (Linien, Ringe, Schrägstrich, Körnung). Keine Stockfotos. Drastische Bilder nur hinter einem Klick.
14. **Logo-Effekt:** nur das große Logo, beim 1. Hover und jedem 10., maximal 1,5×, 4 s, respektiert „Bewegung reduzieren".
15. **Scrollbars:** dünn, Akzentfarbe; innen dunkler als außen.
16. **Zielplattform:** nur Website, responsiv. Keine PDFs, Slides, Thumbnails.

## Konzeptspezifisch (der eigentliche Vergleich)
| | A · Ember | B · Poster | C · Ring |
|---|---|---|---|
| Form | eckig | eckig | rund |
| Aufbau | redaktionell, asymmetrisch | zentriert, plakativ | redaktionell |
| Navigation | Leiste links | Navbar oben | runde Karte rechts |
| Farbwelt | Rot/Schwarz/Silber | Rot/Schwarz/Silber | Sepia und Tinte (Bernstein) |
| Fließtext | Serif (Newsreader) | Sans (Barlow) | Serif (Source Serif 4) |
| Standardmodus | dunkel | dunkel | hell |

## Vorgehen bis zur Wahl
1. Konzepte pflegen, nur Fehler beheben und Gemeinsames verbessern. Nichts zwischen Konzepten mischen.
2. Gemeinsames liegt in `tools/css/base.css`, `tools/build.py`, `tools/blocks.py`, `content/`.
3. Konzeptspezifisches liegt in `brand/<konzept>/tokens.css` und `tools/css/<buchstabe>.css`.
4. Nach jeder Token-Änderung: `python3 tools/build.py && python3 tools/kit.py`.
5. Nach der Wahl: Entscheidung oben eintragen, Übersetzung, `brandkit-build` final, Responsivitäts- und Barrierefreiheitsprüfung, `brandkit-publish`.
