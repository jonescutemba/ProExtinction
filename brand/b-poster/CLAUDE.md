# Arbeitsregeln in diesem Ordner

Hier liegt das Brand-Kit-Konzept **Poster** der Marke **Pro Extinction**. Für jede Design-, Web- oder
Grafikarbeit gilt:

1. **`BRAND.md` ist verbindlich** und schlägt allgemeine Design-Konventionen.
   `../REFERENCE.md` ist Nachschlagewerk. Bei Widerspruch gewinnt `BRAND.md`.
2. **Nur die definierten Tokens.** Keine neuen Farben, keine neuen Schriften, keine rohen
   Hex-Werte im Layout, immer `var(--…)` aus `tokens.css` / `brand-helmet.html`.
3. **Hell und Dunkel sind gleichwertig.** Jede Fläche muss in beiden Modi funktionieren.
4. **Akzent unter 5 % der Fläche,** nie als Hintergrund, nie als Verlauf. Kleiner Text nie in `--accent`.
5. **Wordmark nicht neu erfinden.** `wordmark.svg` und `mark.svg` benutzen. Verboten: Stockfotos,
   Totenkopf- und Blut-Klischees, Metal-Optik im Fließtext.
6. **Vor dem Neuerfinden nachsehen:** `beispiel/bausteine.html` zeigt alle Bausteine in korrekten Maßen.
7. **Text:** Deutsch mit „du", sachlich. Originaltext der Bewegung nie umschreiben. Verbotene Floskeln stehen in `BRAND.md`.
8. **Vor dem Abgeben** die Prüfliste in `BRAND.md` durchgehen.
9. **Dieses Konzept ist nicht gewählt.** Nicht zwischen den Konzepten mischen. Ändert sich ein Token,
   danach `python3 tools/kit.py && python3 tools/build.py` ausführen.

Änderungen am Kit selbst: erst fragen. Diese Dateien sind die einzige Quelle der Wahrheit für dieses Konzept.
