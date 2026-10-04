# BRAND · Pro Extinction · Konzept Ring

Verbindliche Kurzfassung. Begründungen stehen in `../REFERENCE.md`. **Status: Konzept,
nicht final.** Welches der drei Konzepte gilt, ist noch offen (`/DECISIONS.md`). Alle Werte
unten sind vorläufig, aber innerhalb dieses Konzepts verbindlich.

## 1. Marke
**Pro Extinction.** Bewegung, die Leid beenden will, indem sie gegen erzwungene Existenz eintritt.
Zielgruppe: Neulinge überzeugen. Tagline: **„Together, we end suffering."**
Persönlichkeit: ernst · rational · empathisch · entschlossen · ruhig-düster.
Nicht: reißerisch, schockierend, esoterisch, verspielt, hoffnungslos.
Konzept Ring: Rund, Sepia und Tinte, redaktionell: Archiv-Anmutung statt Metal.

## 2. Tokens
Quelle: `tokens.css` (identisch eingebettet in `brand-helmet.html`). Hell und Dunkel sind
gleichwertig, Umschalter oben rechts. Standard: hell (Sepia-Papier).

| Token | Dunkel | Hell | Rolle |
|---|---|---|---|
| `--bg` | `#14100c` | `#f1e6d0` | Grundfläche |
| `--surface` | `#1d1711` | `#e8dac0` | Karten, Panels, Navigationsleiste |
| `--text` | `#e6dcc8` | `#2a1d12` | Haupttext |
| `--muted` | `#a39784` | `#6b5842` | Beschreibungen, Labels, Metadaten |
| `--line` | `#37291d` | `#cdb995` | Rahmen, Trenner, 1px |
| `--accent` | `#d29550` | `#8a4b1c` | Akzent: Flächen, Linien, Buttons, große Zahlen (nicht für kleinen Text) |
| `--link` | `#d9a263` | `#8a4b1c` | Akzent für Text: Links, aktive Navigation, kleine Nummern |
| `--on-accent` | `#1a1209` | `#fff7ea` | Text auf Akzentfläche |
| `--scare` | `#c63a1e` | `#8f1d12` | nur Logo-Effekt (Jumpscare) |

Namen weichen von der Vorlage des Skills ab (`--surface` statt `--surf`, `--text` statt `--fg`,
`--muted` statt `--mut`, `--accent` statt `--acc`). Sie gelten ausschließlich in diesem Kit.

**Flächenverteilung:** Grundfläche 75–85 % · Karten/Panels 10–20 % · Akzent unter 5 % der Fläche (Bernstein/Sepia).
Akzent nie als Sektionshintergrund, nie als Verlauf.

**Kontrast (Verhältnis zur Grundfläche, Ziel für Text ≥ 4,5):**

| Modus | Text | Muted | Link | Akzent | Schrift auf Akzent |
|---|---|---|---|---|---|
| Dunkel | 13.9 | 6.6 | 8.4 | 7.4 | 7.2 |
| Hell | 13.2 | 5.5 | 5.5 | 5.5 | 6.4 |

Der Akzent selbst liegt in manchen Modi unter 4,5. Deshalb: **kleiner Text nie in `--accent`,
immer in `--link`.** `--accent` nur für Flächen, Linien, Balken und große Zahlen (ab 2 rem).

## 3. Typografie
| Rolle | Schrift | Einsatz |
|---|---|---|
| Display | Bebas Neue (Fallback Arial Narrow, Impact) | Überschriften, Wordmark, Buttons, Navigation. Immer Versalien |
| Body | Source Serif 4 · Serif | Fließtext |
| Mono | JetBrains Mono | Labels, Kapitelnummern, Quellen. Sparsam, Versalien, 0,72–0,8 rem |

Größen: Fließtext 1,15 rem / Zeilenhöhe 1,65 · Zeilenlänge 65–70 Zeichen (`68ch`) · H1 `clamp(2,4 rem, 6,5 vw, 4,6 rem)` ·
H2 `clamp(1,4 rem, 3,2 vw, 2 rem)` · Hero-Wordmark `clamp(2,6 rem, 6 vw, 5,2 rem) ab 900 px, sonst bis 6,5 rem`.
Nie Inter oder Roboto als Hauptschrift. Schriften vor dem Livegang selbst hosten.

## 4. Raster und Abstände
| Maß | Wert |
|---|---|
| Seitenrand | `clamp(1,1 rem, 5 vw, 3 rem)` |
| maximale Inhaltsbreite | 72 rem |
| Form | rund (Pillen für Buttons und Navigation, Karten 1,4 rem, Ringe als Zahlen-Marker) |
| Rahmen | 1 px `--line`; Akzent-Rahmen nur für aktive Elemente |
| Schatten, Verläufe, Glas | keine (Ausnahme: Wordmark-Metall, Logo-Schein im Effekt) |
| Körnung | SVG-Rauschen über der Seite, `--grain` Deckkraft, nie animiert |
| Breakpoints | 640 (Kopfzeile kompakt) · 900 (Hero zweispaltig) · 1000 (Navigation als rechte Karte) |

Getestet wird bei 320 · 390 · 600 · 768 · 1024 · 1280 · 1920 · 2560 px. Kein horizontales Scrollen.

## 5. Logo und Wordmark
| Datei | Wann |
|---|---|
| `wordmark.svg` | Schriftzug „PRO EXTINCTION" in Bebas Neue, Standardfall |
| `mark.svg` | Bildmarke (Ouroboros mit Schrägstrich) für kleine Flächen und Hero |
| Metall-Look | nur Wordmark, per CSS (`--metal`), nie als Bild |

Mindestgröße: Wordmark 16 px Schrifthöhe · Marke 24 px. Schutzraum: Höhe des „P" rundherum.
Marke färbt sich in Textfarbe, bei Hover in `--accent`. Nicht verzerren, nicht drehen
(außer im Logo-Effekt), nicht mit Schatten versehen. Die Marke ist eine **Nachzeichnung** eines
500-px-Bildes; das Original-Vektor fehlt (siehe Offen).

**Logo-Effekt (nur Startseite, großes Logo):** beim 1. Hover und danach bei jedem 10.: Wachstum
auf höchstens 1,5×, Vibrieren, zwei Drehungen, 4 s, Farbe `--scare`, Seite dahinter auf 90 %
abgedunkelt. Kein Blitzen. Bei „Bewegung reduzieren" aus (Test: `?motion=on`, Zähler: `?scare=reset`).

## 6. Bausteine
| Baustein | Maße und Regeln |
|---|---|
| Navigation | Runde Karte rechts, 16,5 rem, ab 1000 px, klebt oben. Die Liste scrollt innerhalb der Karte, der Rand bleibt intakt. Darunter Pillen-Streifen. Aktive Seite: gefüllte Pille. Nur die Liste in der Karte scrollt und blendet unten aus; der Kartenrand bleibt vollständig. |
| Kapitelübersicht | Karte mit zwei Spalten über dem Text. Aktives Kapitel in `--link`, nummeriert 01, 02 … |
| Langtext | Redaktionell, Inhalt linksbündig, maximal 58 rem. Kapitelnummern in Ringen (2,4 rem). Absatzabstand 1,15 em |
| Vier Efforts | Container-Breite: unter 34 rem 1 Spalte, ab 34 rem 2 (bleibt 2: Karten mit Ring-Nummer links brauchen Breite). |
| Mission-Zitat | Display, Versalien (C: Serif kursiv), bis 3,2 rem, höchstens 22–28 Zeichen Breite |
| FAQ | aufklappbar (`<details>`), fortlaufend nummeriert per CSS, Pfeil als Schrägstrich |
| Call-to-Action | Discord (primär), WhatsApp, E-Mail; am Seitenende jeder Seite |
| Schrägstrich | Signatur: Trenner, Fortschrittsbalken (oben, 4 px), Hover; immer `--accent` |
| Scrollbars | 8 px, `--accent` (Seite); in Leisten 6 px, `--accent-dim` (58 % Akzent), Hover `--accent` |
| Umschalter | Sprachauswahl (EN, DE, PL, ES, IT sowie FR, PT, RU, ZH, HI als „(AI)“) und Hell/Dunkel oben rechts; Zurück-Knopf zur Konzeptübersicht nur im Prototyp |

## 7. Formate
Nur Website, responsiv. Keine Thumbnails, Slides oder PDFs in dieser Runde.

## 8. Text
Deutsch mit „du", sachlich und direkt. Der Originaltext der Bewegung bleibt wörtlich
(nur Tippfehler korrigiert). Neu geschrieben werden nur Buttons, Zwischenüberschriften und
Hinweise. Fehlende Seiten in DE, PL, ES und IT: KI-Übersetzung aus dem Englischen, **sichtbar gekennzeichnet** („(AI)" im Menütitel plus Hinweis auf der Seite). FR, PT, RU, ZH und HI sind komplett KI-übersetzt und in der Sprachauswahl als „(AI)“ markiert, plus Hinweis auf jeder Seite.
Gut: „Wir wollen so viel Leid wie möglich beenden, ohne Kompromisse."
Schlecht: „Gemeinsam für eine bessere Welt voller Hoffnung!"
Verboten in neu geschriebenen Texten: „revolutionär", „bahnbrechend", „Reise", „Community"
im Marketing-Sinn, „Hoffnung" als Floskel, Ausrufezeichen, Emojis.

## 9. Nicht benutzen
- Inter oder Roboto als Hauptschrift
- Stockfotos, Sonnenuntergangs-Silhouetten, Totenkopf- und Blut-Klischees
- Metal-Optik im Fließtext
- Verläufe oder Glanz außer in Logo und Wordmark
- Schatten und Glaseffekte
- Akzentfarbe als Sektionshintergrund oder Verlauf
- Akzentfarbe für kleinen Text (dafür `--link`)
- Neue Farben, neue Schriften, rohe Hex-Werte im Layout
- Eckige Buttons
- Metallic-Verläufe außerhalb der Wordmark
- Rotes Blutrot als Akzent (nur im Logo-Effekt)

## 10. Prüfliste vor dem Abgeben
1. Stehen im Layout nur `var(--…)`-Tokens, keine rohen Hex-Werte?
2. Funktioniert die Seite in Hell **und** Dunkel, mit sichtbarem Umschalter?
3. Liegt der Akzent unter 5 % der Fläche und nie als Hintergrund?
4. Steht kleiner Text in `--link`/`--text`/`--muted`, nie in `--accent`?
5. Sind Text-Kontraste ≥ 4,5 : 1 (Tabelle oben)?
6. Ist die Textspalte höchstens 70 Zeichen breit?
7. Gibt es kein horizontales Scrollen bei 320, 390, 768, 1280, 2560 px?
8. Steht der Originaltext wörtlich da, KI-Übersetzungen sind gekennzeichnet?
9. Sind Navigation, Kapitelübersicht und FAQ per Tastatur bedienbar, Fokus sichtbar?
10. Ist „Bewegung reduzieren" respektiert (kein Logo-Effekt, keine Animation)?

## Offen (nicht erfunden)
- **Konzeptwahl** A, B oder C: später, siehe `/DECISIONS.md`.
- **Hex-Werte** sind Vorschläge, nicht abgenommen.
- **Original-Logo als Vektor** fehlt; `mark.svg` ist eine Nachzeichnung.
- **Schriften:** in `presentation/` lokal gehostet. `brand-helmet.html` und die Prototyp-Seiten laden noch von Google; vor Livegang auch dort umstellen (DSGVO).
- **Bilder** („Suffering in detail", 16 Stück): erste Runde ohne Fotos; drastische Bilder nur hinter Klick.
- **Telefonnummer** nur auf der deutschen Seite, vor Livegang bestätigen lassen.
- **IBAN auf der Spendenseite:** unverändert aus dem Original; Seite gehört erst nach Freigabe live.
