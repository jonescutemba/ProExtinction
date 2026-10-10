# Pro Extinction – Marken-Rohfassung

Ergebnis des Markeninterviews (Schritt 2 des Brand-Kit-Ablaufs). Alle Festlegungen
stammen vom Auftraggeber. Wo etwas offen ist, steht es ausdrücklich dabei.

## 1. Kern
- **Markenname:** Pro Extinction. "AbolishSuffering" bleibt nur der Discord-Name.
- **Tagline:** "Together, we end suffering." (vom Flyer, Wahl des Auftraggebers)
- **Mission (Originaltext):** "Preventing as much suffering as physically possible, without tradeoffs."
- **Zielgruppe:** Neulinge überzeugen, nicht die bestehende Community mobilisieren.
- **Abgrenzung:** von Pro-Life-Ideologien. Die Seite hat dazu eine eigene Unterseite.
- **Warum:** Die bestehende Google-Sites-Seite besteht fast nur aus Text. Sie soll
  für Neulinge lesbarer und eindrücklicher werden, ohne Inhalte zu verfälschen.

## 2. Persönlichkeit
- **Ja:** ernst, rational, empathisch, entschlossen, ruhig-düster.
- **Nein:** reißerisch, schockierend, esoterisch, verspielt, hoffnungslos.
- **Warum:** Die Ideologie hat etwas Melancholisches und Morbides, das die
  bestehende Marke (Flyer) schon aufgreift. Für Neulinge darf die Düsternis
  Ernsthaftigkeit zeigen, aber nicht Hoffnungslosigkeit. Die Tagline ist ein
  Handlungsversprechen.

## 3. Struktur
- Eine Dachmarke. Keine Untermarken. Keine Einzelpersonen im Vordergrund.
- Sprachen der Konzepte: Englisch und Deutsch.
- Fehlende deutsche Seiten (Criticism of different pro-life ideologies, Cosmic
  Extinction, Social Media Channels, Donate) werden per KI aus dem Englischen
  übersetzt und **sichtbar gekennzeichnet**.
- Tippfehler der deutschen Originalseite werden korrigiert (z. B. "WIr", "Resourcen").
- Die Telefonnummer von der deutschen Startseite bleibt auf der deutschen Seite.
  Auf der englischen Seite steht sie nicht.

## 4. Vorbilder und Gegenbilder
- **Gegenbild:** animal-ethics.org.
- **Vorbilder:** keine genannt. Stil wird aus Flyer, Logo und Animationswünschen
  abgeleitet. **Offen:** konkrete "Wow"-Referenzen.
- **Später gewünscht:** animiertes Logo bei Hover, animierter Staub am Seitenende.

## 5. Farbe
- Rot nur als Akzent, höchstens etwa 5 % einer Fläche.
- **Dunkelmodus:** fast schwarz mit leichtem Rotstich, silbergrauer Text.
- **Hellmodus:** warmes Papierweiß, fast schwarzer Text, dunkleres Rot.
- Silber nur im Logo und in großen Überschriften.
- Hell/Dunkel per Button umschaltbar. Das gilt für alle Konzepte.
- **Konzept C** hat eine abweichende Farbwelt: Sepia und Tinte.
- **Hex-Werte:** offen, werden in `brandkit-build` festgelegt und dort begründet.

## 6. Typografie
- **Display:** schwere, enge Versalien-Grotesk (z. B. Oswald, Bebas Neue, Anton).
- **Fließtext:** Konzept A und C mit Serifenschrift, Konzept B serifenlos
  (nicht Inter oder Roboto).
- **Mono:** sparsam für Labels, Kapitelnummern, Quellen.
- **Wordmark:** als Schrift gesetzt, Metalloptik per CSS. Kein Bild aus dem Flyer.
- **Verboten:** Inter und Roboto als Hauptschrift.

## 7. Raster und Anmutung
- Großzügiger Leerraum, Text in schmaler Spalte (etwa 65–70 Zeichen).
- Keine Schatten, keine Glaseffekte. Verläufe und Glanz nur im Logo und der Wordmark.
- Körnung im Hintergrund, im Dunkelmodus dezent.
- Haarlinien in Rot oder Silber als Trenner.
- **Konzept A "Ember":** eckig, redaktionell asymmetrisch, Kapitelnummern am Rand.
- **Konzept B "Poster":** eckig, zentriert und plakativ.
- **Konzept C "Ring":** rund (abgerundete Buttons und Karten, Ring als Gestaltungselement). *Später verworfen.*

## 8. Bausteine
1. Langtext-Seite mit Kapiteln, mitlaufendes Inhaltsverzeichnis, Lesefortschritt.
2. FAQ als aufklappbare Fragen.
3. Zitatblock für zentrale Sätze.
4. Die vier "Efforts" als nummerierte Karten.
5. Call-to-Action-Band (Discord, WhatsApp, Join us) am Seitenende.
6. Sprach- und Theme-Umschalter oben rechts.
- **Signature:** der rote Schrägstrich aus dem Logo, als Trenner, Hover-Effekt
  und Fortschrittsanzeige.
- Keine weiteren Bausteine in der ersten Runde.

## 9. Sprache
- Deutsch mit "du". Ton sachlich und direkt.
- Der Originaltext bleibt wörtlich, abgesehen von den Tippfehlerkorrekturen.
- Neue Texte nur für Buttons, Zwischenüberschriften und den KI-Übersetzungshinweis.
- **Verbotsliste (nur für neu geschriebene Texte):** "revolutionär", "bahnbrechend",
  "Reise", "Community" im Marketing-Sinn, "Hoffnung" als Floskel, Ausrufezeichen, Emojis.

## 10. Formate
- Nur Website, responsiv (Handy, Tablet, Desktop). Keine Thumbnails, Slides, PDFs.

## 11. Bilder
- Hauptbildsprache: eigene Grafiken im Code (Linien, Ringe, Schrägstrich, Körnung).
- Diagramme nur, wo der Originaltext Zahlen enthält. Keine erfundenen Zahlen.
- Drastische Bilder der Originalseite liegen hinter einem Klick.
- **Erste Runde ohne Fotos.** Die 16 Bilder von "Suffering in detail" kommen später.
- KI-Bilder (Higgsfield) vorerst nicht.
- **Verboten:** Stockfotos, Sonnenuntergangs-Silhouetten, Totenkopf- und Blut-Klischees,
  Metal-Optik im Fließtext.

## Logo
- Ouroboros mit rotem Schrägstrich. Als SVG nachgezeichnet aus einem 500-px-Bild
  (`tools/assets/logo.svg`). **Offen:** Original-Vektordatei, falls auffindbar.

## Offene Punkte
1. Konkrete Gestaltungsvorbilder.
2. Hex-Werte der Farben.
3. Original-Vektorlogo.
4. Umgang mit den Bildern von "Suffering in detail".
