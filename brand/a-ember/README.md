# Brand Kit · Pro Extinction · Ember

Eckig, redaktionell, asymmetrisch: Flyer-Ästhetik, aber lesbar. **Status: Konzept, noch nicht gewählt** (siehe `/DECISIONS.md`).

| Datei | Zweck |
|---|---|
| `BRAND.md` | die verbindliche Kurzfassung |
| `CLAUDE.md` | Arbeitsregeln, greifen automatisch in diesem Ordner |
| `tokens.css` | ausführbare Tokens, einzige Quelle der Wahrheit |
| `brand-helmet.html` | Schriften-Link, Tokens und Grundstile als fertiger Block (generiert) |
| `brand-props.json` | Akzent im Design-Editor umschaltbar (nur Markenfarben) |
| `wordmark.svg` | Schriftzug |
| `mark.svg` | Bildmarke, aus dem Original nachgezeichnet |
| `beispiel/` | lauffähige Referenz mit allen Bausteinen, Desktop und mobil |
| `../REFERENCE.md` | Rohfassung aus dem Interview, mit Begründungen |

**Das Kit lädt sich nicht von allein.** Arbeitest du außerhalb dieses Ordners, kopiere diesen Satz an
den Anfang der Sitzung:

```
Lies zuerst brand/a-ember/BRAND.md und halte dich exakt daran.
Referenz: brand/a-ember/beispiel/bausteine.html
```

`wordmark.svg` enthält `<text>` und braucht die Schrift Oswald auf dem anzeigenden Gerät.
Sobald die Wordmark den Browser verlässt (Druck, Illustrator, PDF), muss sie in Pfade umgewandelt werden.

Neu erzeugen: `python3 tools/kit.py` (Kit-Dateien) und `python3 tools/build.py` (Seiten).
