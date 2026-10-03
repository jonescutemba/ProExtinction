"""Generate the three brand kits (brand/<concept>/) from tokens.css + concept facts.

Run after editing a tokens.css:  python3 tools/kit.py && python3 tools/build.py
"""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
BRAND = ROOT / 'brand'

ROLES = {
 'bg': 'Grundfläche', 'surface': 'Karten, Panels, Navigationsleiste', 'text': 'Haupttext',
 'muted': 'Beschreibungen, Labels, Metadaten', 'line': 'Rahmen, Trenner, 1px',
 'accent': 'Akzent: Flächen, Linien, Buttons, große Zahlen (nicht für kleinen Text)',
 'link': 'Akzent für Text: Links, aktive Navigation, kleine Nummern',
 'on-accent': 'Text auf Akzentfläche', 'scare': 'nur Logo-Effekt (Jumpscare)',
 'accent-deep': 'dunklere Akzentvariante (Reserve)', 'grain': 'Deckkraft der Körnung',
}
ORDER = ['bg', 'surface', 'text', 'muted', 'line', 'accent', 'link', 'on-accent', 'scare']

CONCEPTS = {
 'a-ember': dict(
  name='Ember', fonts='family=Oswald:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500',
  display='Oswald', body='Newsreader', body_kind='Serif', default_mode='dunkel',
  one_liner='Eckig, redaktionell, asymmetrisch: Flyer-Ästhetik, aber lesbar.',
  shape='eckig (Radius 0 überall: Buttons, Karten, Scrollbar)', shape_short='eckig',
  accent_share='unter 5 % der Fläche',
  nav='Feste Leiste links, 17,5 rem breit, ab 900 px. Darunter waagerechter Streifen. Aktive Seite: roter 3-px-Balken links.',
  toc='Kapitelübersicht rechts, 14 rem, mitlaufend (sticky), ab 1280 px. Darunter über dem Text.',
  layout='Asymmetrisch: Text linksbündig, Spalte 68 ch. Kapitelnummern inline vor der H2 (01, 02 …).',
  efforts='Container-Breite: unter 34 rem 1 Spalte, ab 34 rem 2, ab 66 rem 4. Nummer 2,2 rem in Mono, Haarlinie oben.',
  h1='clamp(2,4 rem, 7 vw, 5 rem)', wordmark_hero='clamp(2,6 rem, 6,4 vw, 5,4 rem) ab 1280 px, sonst bis 8 rem',
  gutter='clamp(1,1 rem, 5 vw, 3,5 rem)', wide='78 rem', body_size='1,125 rem / Zeilenhöhe 1,65',
  bp='640 (Kopfzeile kompakt) · 900 (Seitenleiste) · 1280 (Hero zweispaltig, Kapitelübersicht rechts)',
  banned_extra=['Runde Karten oder Pillen-Buttons', 'Zentrierte Fließtextblöcke', 'Sans-Serif im Fließtext'],
  rail_note='Liste scrollt nur, wenn das Fenster niedriger ist als die Leiste; dann blendet sie unten weich aus.'),
 'b-poster': dict(
  name='Poster', fonts='family=Anton&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500',
  display='Anton', body='Barlow', body_kind='Sans-Serif (nicht Inter, nicht Roboto)', default_mode='dunkel',
  one_liner='Eckig, zentriert, plakativ: große Versalien, Konturziffern, ruhiger Text.',
  shape='eckig (Radius 0 überall)', shape_short='eckig',
  accent_share='unter 5 % der Fläche',
  nav='Navbar oben unter der Kopfzeile, zentriert, ab 900 px auf zwei Zeilen umbrechend, klebt oben (sticky). Darunter waagerechter Streifen. Aktive Seite: rot und unterstrichen.',
  toc='Kapitelchips mit Nummern zentriert über dem Text, immer inline.',
  layout='Zentriert: Titel, Trenner, Kapitelüberschriften mittig, Fließtext linksbündig in 68-ch-Spalte.',
  efforts='Container-Breite: unter 38 rem 1 Spalte, ab 38 rem 2×2. Nummer als Konturziffer 4–7 rem (Anton, 2 px Akzent-Kontur).',
  h1='clamp(2,6 rem, 9 vw, 6 rem)', wordmark_hero='clamp(2,2 rem, 11,5 vw, 9,5 rem)',
  gutter='clamp(1,1 rem, 5 vw, 3 rem)', wide='60 rem', body_size='1,125 rem / Zeilenhöhe 1,65',
  bp='640 (Kopfzeile kompakt) · 760 (Kopfzeile dreispaltig) · 900 (Navbar umbrechend)',
  banned_extra=['Runde Formen', 'Linksbündige Überschriften', 'Serifen im Fließtext'],
  rail_note='Keine Seitenleiste, daher kein Scrollproblem in der Navigation.'),
 'c-ring': dict(
  name='Ring', fonts='family=Bebas+Neue&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500',
  display='Bebas Neue', body='Source Serif 4', body_kind='Serif', default_mode='hell (Sepia-Papier)',
  one_liner='Rund, Sepia und Tinte, redaktionell: Archiv-Anmutung statt Metal.',
  shape='rund (Pillen für Buttons und Navigation, Karten 1,4 rem, Ringe als Zahlen-Marker)', shape_short='rund',
  accent_share='unter 5 % der Fläche (Bernstein/Sepia)',
  nav='Runde Karte rechts, 16,5 rem, ab 1000 px, klebt oben. Die Liste scrollt innerhalb der Karte, der Rand bleibt intakt. Darunter Pillen-Streifen. Aktive Seite: gefüllte Pille.',
  toc='Karte mit zwei Spalten über dem Text.',
  layout='Redaktionell, Inhalt linksbündig, maximal 58 rem. Kapitelnummern in Ringen (2,4 rem).',
  efforts='Container-Breite: unter 34 rem 1 Spalte, ab 34 rem 2 (bleibt 2: Karten mit Ring-Nummer links brauchen Breite).',
  h1='clamp(2,4 rem, 6,5 vw, 4,6 rem)', wordmark_hero='clamp(2,6 rem, 6 vw, 5,2 rem) ab 900 px, sonst bis 6,5 rem',
  gutter='clamp(1,1 rem, 5 vw, 3 rem)', wide='72 rem', body_size='1,15 rem / Zeilenhöhe 1,65',
  bp='640 (Kopfzeile kompakt) · 900 (Hero zweispaltig) · 1000 (Navigation als rechte Karte)',
  banned_extra=['Eckige Buttons', 'Metallic-Verläufe außerhalb der Wordmark', 'Rotes Blutrot als Akzent (nur im Logo-Effekt)'],
  rail_note='Nur die Liste in der Karte scrollt und blendet unten aus; der Kartenrand bleibt vollständig.'),
}

# ---------- helpers
def parse_tokens(c):
    s = (BRAND / c / 'tokens.css').read_text()
    root = re.search(r':root\{([^}]*)\}', s).group(1)
    th = {m: dict(re.findall(r'--([\w-]+):([^;}]+)', re.search(r':root\[data-theme=%s\]\{([^}]*)\}' % m, s).group(1))) for m in ('dark', 'light')}
    base = dict(re.findall(r'--([\w-]+):([^;}]+)', root))
    return base, th

def _norm(h):
    h = h.strip().lstrip('#'); return ''.join(ch * 2 for ch in h) if len(h) == 3 else h
def _lum(h):
    h = _norm(h); rgb = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(rgb[0]) + 0.7152 * f(rgb[1]) + 0.0722 * f(rgb[2])
def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True); return round((la + 0.05) / (lb + 0.05), 1)

def pretty_tokens(c):
    base, th = parse_tokens(c); d = CONCEPTS[c]
    out = [f'/* Pro Extinction · Konzept {d["name"]} · ausführbare Tokens (einzige Quelle der Wahrheit).',
           '   Werte sind VORLÄUFIG, bis ein Konzept gewählt ist (siehe /DECISIONS.md).',
           '   Rollen und Kontraste stehen in BRAND.md. Im Layout nur var(--…) benutzen, keine rohen Hex-Werte. */', ':root{']
    for k, v in base.items(): out.append(f'  --{k}:{v};')
    out.append('}')
    for m in ('dark', 'light'):
        out.append(f':root[data-theme={m}]{{')
        for k in ORDER + [k for k in th[m] if k not in ORDER]:
            if k in th[m]: out.append(f'  --{k}:{th[m][k]};' + (f'  /* {ROLES[k]} */' if k in ROLES else ''))
        out.append('}')
    (BRAND / c / 'tokens.css').write_text('\n'.join(out) + '\n')

def helmet(c):
    d = CONCEPTS[c]; tok = (BRAND / c / 'tokens.css').read_text()
    return f'''<!-- Brand Kit Pro Extinction · {d["name"]}. Generiert von tools/kit.py. Nicht von Hand ändern.
     Im Layout ausschließlich var(--…) benutzen. Der <style>-Block gehört in den <head>.
     Vor dem Livegang die Schriften selbst hosten (DSGVO), siehe BRAND.md, Abschnitt „Offen". -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{d["fonts"]}&display=swap">
<style>
{tok}
*,*::before,*::after{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:var(--body);line-height:1.65}}
h1,h2,h3{{margin:0;font-family:var(--display);font-weight:var(--display-weight,600);text-transform:uppercase;line-height:1.05}}
a{{color:var(--link)}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:3px}}
.lbl{{font-family:var(--mono);font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
.val{{font-family:var(--mono);font-variant-numeric:tabular-nums}}
</style>
'''

def brand_md(c):
    d = CONCEPTS[c]; base, th = parse_tokens(c)
    rows = []
    for k in ORDER:
        rows.append(f'| `--{k}` | `{th["dark"].get(k,"–")}` | `{th["light"].get(k,"–")}` | {ROLES[k]} |')
    cr = []
    for m, label in (('dark', 'Dunkel'), ('light', 'Hell')):
        t = th[m]
        cr.append(f'| {label} | {contrast(t["text"], t["bg"])} | {contrast(t["muted"], t["bg"])} | {contrast(t["link"], t["bg"])} | {contrast(t["accent"], t["bg"])} | {contrast(t["on-accent"], t["accent"])} |')
    banned = ['Inter oder Roboto als Hauptschrift', 'Stockfotos, Sonnenuntergangs-Silhouetten, Totenkopf- und Blut-Klischees',
              'Metal-Optik im Fließtext', 'Verläufe oder Glanz außer in Logo und Wordmark', 'Schatten und Glaseffekte',
              'Akzentfarbe als Sektionshintergrund oder Verlauf', 'Akzentfarbe für kleinen Text (dafür `--link`)',
              'Neue Farben, neue Schriften, rohe Hex-Werte im Layout'] + d['banned_extra']
    bl = '\n'.join(f'- {b}' for b in banned)
    return f'''# BRAND · Pro Extinction · Konzept {d["name"]}

Verbindliche Kurzfassung. Begründungen stehen in `../REFERENCE.md`. **Status: Konzept,
nicht final.** Welches der drei Konzepte gilt, ist noch offen (`/DECISIONS.md`). Alle Werte
unten sind vorläufig, aber innerhalb dieses Konzepts verbindlich.

## 1. Marke
**Pro Extinction.** Bewegung, die Leid beenden will, indem sie gegen erzwungene Existenz eintritt.
Zielgruppe: Neulinge überzeugen. Tagline: **„Together, we end suffering."**
Persönlichkeit: ernst · rational · empathisch · entschlossen · ruhig-düster.
Nicht: reißerisch, schockierend, esoterisch, verspielt, hoffnungslos.
Konzept {d["name"]}: {d["one_liner"]}

## 2. Tokens
Quelle: `tokens.css` (identisch eingebettet in `brand-helmet.html`). Hell und Dunkel sind
gleichwertig, Umschalter oben rechts. Standard: {d["default_mode"]}.

| Token | Dunkel | Hell | Rolle |
|---|---|---|---|
{chr(10).join(rows)}

Namen weichen von der Vorlage des Skills ab (`--surface` statt `--surf`, `--text` statt `--fg`,
`--muted` statt `--mut`, `--accent` statt `--acc`). Sie gelten ausschließlich in diesem Kit.

**Flächenverteilung:** Grundfläche 75–85 % · Karten/Panels 10–20 % · Akzent {d["accent_share"]}.
Akzent nie als Sektionshintergrund, nie als Verlauf.

**Kontrast (Verhältnis zur Grundfläche, Ziel für Text ≥ 4,5):**

| Modus | Text | Muted | Link | Akzent | Schrift auf Akzent |
|---|---|---|---|---|---|
{chr(10).join(cr)}

Der Akzent selbst liegt in manchen Modi unter 4,5. Deshalb: **kleiner Text nie in `--accent`,
immer in `--link`.** `--accent` nur für Flächen, Linien, Balken und große Zahlen (ab 2 rem).

## 3. Typografie
| Rolle | Schrift | Einsatz |
|---|---|---|
| Display | {d["display"]} (Fallback Arial Narrow, Impact) | Überschriften, Wordmark, Buttons, Navigation. Immer Versalien |
| Body | {d["body"]} · {d["body_kind"]} | Fließtext |
| Mono | JetBrains Mono | Labels, Kapitelnummern, Quellen. Sparsam, Versalien, 0,72–0,8 rem |

Größen: Fließtext {d["body_size"]} · Zeilenlänge 65–70 Zeichen (`68ch`) · H1 `{d["h1"]}` ·
H2 `clamp(1,4 rem, 3,2 vw, 2 rem)` · Hero-Wordmark `{d["wordmark_hero"]}`.
Nie Inter oder Roboto als Hauptschrift. Schriften vor dem Livegang selbst hosten.

## 4. Raster und Abstände
| Maß | Wert |
|---|---|
| Seitenrand | `{d["gutter"]}` |
| maximale Inhaltsbreite | {d["wide"]} |
| Form | {d["shape"]} |
| Rahmen | 1 px `--line`; Akzent-Rahmen nur für aktive Elemente |
| Schatten, Verläufe, Glas | keine (Ausnahme: Wordmark-Metall, Logo-Schein im Effekt) |
| Körnung | SVG-Rauschen über der Seite, `--grain` Deckkraft, nie animiert |
| Breakpoints | {d["bp"]} |

Getestet wird bei 320 · 390 · 600 · 768 · 1024 · 1280 · 1920 · 2560 px. Kein horizontales Scrollen.

## 5. Logo und Wordmark
| Datei | Wann |
|---|---|
| `wordmark.svg` | Schriftzug „PRO EXTINCTION" in {d["display"]}, Standardfall |
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
| Navigation | {d["nav"]} {d["rail_note"]} |
| Kapitelübersicht | {d["toc"]} Aktives Kapitel in `--link`, nummeriert 01, 02 … |
| Langtext | {d["layout"]} Absatzabstand 1,15 em |
| Vier Efforts | {d["efforts"]} |
| Mission-Zitat | Display, Versalien (C: Serif kursiv), bis 3,2 rem, höchstens 22–28 Zeichen Breite |
| FAQ | aufklappbar (`<details>`), fortlaufend nummeriert per CSS, Pfeil als Schrägstrich |
| Call-to-Action | Discord (primär), WhatsApp, E-Mail; am Seitenende jeder Seite |
| Schrägstrich | Signatur: Trenner, Fortschrittsbalken (oben, 4 px), Hover; immer `--accent` |
| Scrollbars | 8 px, `--accent` (Seite); in Leisten 6 px, `--accent-dim` (58 % Akzent), Hover `--accent` |
| Umschalter | Sprache (EN/DE) und Hell/Dunkel oben rechts; Zurück-Knopf zur Konzeptübersicht nur im Prototyp |

## 7. Formate
Nur Website, responsiv. Keine Thumbnails, Slides oder PDFs in dieser Runde.

## 8. Text
Deutsch mit „du", sachlich und direkt. Der Originaltext der Bewegung bleibt wörtlich
(nur Tippfehler korrigiert). Neu geschrieben werden nur Buttons, Zwischenüberschriften und
Hinweise. Fehlende deutsche Seiten: KI-Übersetzung, **sichtbar gekennzeichnet** („KI").
Gut: „Wir wollen so viel Leid wie möglich beenden, ohne Kompromisse."
Schlecht: „Gemeinsam für eine bessere Welt voller Hoffnung!"
Verboten in neu geschriebenen Texten: „revolutionär", „bahnbrechend", „Reise", „Community"
im Marketing-Sinn, „Hoffnung" als Floskel, Ausrufezeichen, Emojis.

## 9. Nicht benutzen
{bl}

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
'''

def claude_md(c):
    d = CONCEPTS[c]
    return f'''# Arbeitsregeln in diesem Ordner

Hier liegt das Brand-Kit-Konzept **{d["name"]}** der Marke **Pro Extinction**. Für jede Design-, Web- oder
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
'''

def readme(c):
    d = CONCEPTS[c]
    return f'''# Brand Kit · Pro Extinction · {d["name"]}

{d["one_liner"]} **Status: Konzept, noch nicht gewählt** (siehe `/DECISIONS.md`).

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
Lies zuerst brand/{c}/BRAND.md und halte dich exakt daran.
Referenz: brand/{c}/beispiel/bausteine.html
```

`wordmark.svg` enthält `<text>` und braucht die Schrift {d["display"]} auf dem anzeigenden Gerät.
Sobald die Wordmark den Browser verlässt (Druck, Illustrator, PDF), muss sie in Pfade umgewandelt werden.

Neu erzeugen: `python3 tools/kit.py` (Kit-Dateien) und `python3 tools/build.py` (Seiten).
'''

def wordmark_svg(c):
    d = CONCEPTS[c]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 80" role="img" aria-label="Pro Extinction">
  <!-- Schriftzug als <text>: braucht {d["display"]}. Vor Druck/Export in Pfade umwandeln. Farbe: currentColor (im Browser inline einbetten). -->
  <text x="0" y="62" fill="currentColor" font-family="'{d["display"]}','Arial Narrow',Impact,sans-serif" font-size="68" letter-spacing="3" font-weight="600">PRO EXTINCTION</text>
</svg>
'''

def props_json(c):
    base, th = parse_tokens(c)
    opts = sorted({th['dark']['accent'], th['light']['accent']})
    return json.dumps({
        'accent': {'label': 'Akzent', 'options': opts, 'default': th['dark']['accent']},
        '_note': 'Prüfwerkzeug, kein zweiter Markenakzent. Nur Markenfarben, keine Funktionsfarben.'
    }, indent=2, ensure_ascii=False) + '\n'

def examples(c):
    d = CONCEPTS[c]; base, th = parse_tokens(c)
    css = (ROOT / 'concepts' / c / 'style.css').read_text()
    js = (ROOT / 'concepts' / 'assets' / 'site.js').read_text()
    def sw(m):
        return ''.join(f'<li><span class="sw" style="background:{th[m][k]}"></span><b class="mono">--{k}</b><code>{th[m][k]}</code></li>' for k in ORDER)
    cur = ' aria-current="page"'
    nav = ''.join('<li><a href="#"%s>%s</a></li>' % (cur if i == 1 else '', t) for i, t in enumerate(['Home', 'Manifest', 'Basis-FAQ', 'Vollständiges FAQ', 'Geschichte', 'Aktiv werden', 'Kontakt']))
    eff = ''.join(f'<li><span class="num mono">{i+1:02d}</span><p class="eff-label mono">Einsatz {i+1}</p><p>Beispieltext für einen Einsatz. Länge und Umbruch wie im Original.</p></li>' for i in range(4))
    toc = ''.join(f'<li><a href="#b{i}">Beispielkapitel {i}</a></li>' for i in range(1, 6))
    faq = ''.join(f'<details><summary>Beispielfrage {i}?</summary><div class="a"><p>Beispielantwort. Echter Text kommt wörtlich aus dem Original.</p></div></details>' for i in range(1, 4))
    page = f'''<!doctype html>
<html lang="de" data-concept="{c}" data-default="{'light' if 'hell' in d['default_mode'] else 'dark'}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bausteine · Pro Extinction · {d["name"]}</title><meta name="robots" content="noindex">
<script>(function(){{var d=document.documentElement,m=null;try{{m=new URLSearchParams(location.search).get('theme')||localStorage.getItem('pe-theme')}}catch(e){{}}if(m!=='light'&&m!=='dark')m=d.dataset.default;d.dataset.theme=m}})()</script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{d["fonts"]}&display=swap">
<style>{css}
.ex-block{{padding:2rem var(--gutter);max-width:var(--wide);margin-inline:auto}}
.ex-block>h2{{font-size:1.4rem;margin-bottom:1rem}}
.ex-flag{{margin:0 0 1.2rem}}
.sw-list{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(11rem,1fr));gap:.6rem}}
.sw-list li{{display:grid;gap:.15rem;font-size:.8rem}}.sw{{display:block;height:2.2rem;border:1px solid var(--line)}}
.scroll-demo{{height:9rem;overflow:auto;border:1px solid var(--line);padding:1rem;max-width:30rem}}
.ex-row{{display:flex;flex-wrap:wrap;gap:.8rem;align-items:center}}
</style></head>
<body>
<div class="progress" aria-hidden="true"><i></i></div>
<header class="top"><div class="lead"><a class="brand" href="#"><span class="logo" role="img" aria-label="Pro Extinction"></span><span class="wordmark">PRO EXTINCTION</span></a></div>
<div class="tools"><a class="lang" href="#">EN</a><button class="theme" type="button" aria-label="Hell/Dunkel umschalten"><span></span></button></div></header>
<div class="shell"><nav class="sitenav" aria-label="Beispiel"><ul>{nav}</ul></nav>
<main id="main">
<section class="ex-block"><p class="mono ex-flag">BEISPIELDATEN · Referenz für Konzept {d["name"]} · alle Texte hier sind Platzhalter</p>
<h1>Bausteine</h1><hr class="slash"></section>
<section class="ex-block"><h2>Farben (Tokens)</h2><p class="mono ex-flag">Dunkel</p><ul class="sw-list">{sw("dark")}</ul><p class="mono ex-flag" style="margin-top:1.2rem">Hell</p><ul class="sw-list">{sw("light")}</ul></section>
<section class="ex-block"><h2>Typografie</h2><h1 style="font-size:{d['h1'].replace(',', '.').replace(' ', '')}">Überschrift H1</h1><h2 style="margin:1rem 0">Überschrift H2</h2><p class="lede">Lede-Zeile in Kursiv.</p><p style="max-width:68ch">Fließtext: {d["body"]}. Die Zeilenlänge bleibt bei etwa 68 Zeichen, damit lange Texte lesbar sind. <a href="#">Ein Link</a> steht in <code>--link</code>.</p><p class="mono">Mono-Label · 01 · Quelle</p></section>
<section class="ex-block"><h2>Buttons und Trenner</h2><div class="ex-row"><a class="btn primary" href="#">Aktiv werden</a><a class="btn" href="#">Manifest lesen</a></div><hr class="slash"></section>
<section class="hero" aria-label="Hero und Logo-Effekt"><span class="logo hero-logo" role="img" aria-label="Logo (Hover testen)"></span><h1 class="wordmark">PRO EXTINCTION</h1><p class="hero-tag">Together, we end suffering.</p><p class="hero-sub">Hover über das Logo: Effekt beim 1. und jedem 10. Mal. Zurücksetzen mit ?scare=reset.</p></section>
<section class="mission"><hr class="slash"><p class="mono kicker">Unsere Mission</p><blockquote>Beispielzitat in der Zitat-Schrift des Konzepts.</blockquote></section>
<section class="efforts"><ol>{eff}</ol></section>
<section class="ex-block"><h2>Kapitelübersicht und Langtext</h2><nav class="toc" aria-label="Auf dieser Seite"><p class="mono">Auf dieser Seite</p><ol>{toc}</ol></nav><div class="prose"><h2 id="b1">Beispielkapitel 1</h2><p>Absatz mit Beispieltext. Das mitlaufende aktive Kapitel wird per Script markiert.</p><ul><li>Listenpunkt mit Akzent-Marker</li><li>Zweiter Punkt</li></ul><h2 id="b2">Beispielkapitel 2</h2><p>Zweiter Absatz.</p></div></section>
<section class="ex-block"><h2>FAQ</h2><div class="faq">{faq}</div></section>
<section class="ex-block"><h2>Scrollbar (innen)</h2><div class="scroll-demo"><p>Scrolle in diesem Feld. Innere Scrollbars sind dünner und dunkler als die der Seite.</p>{"<p>Zeile Beispieltext.</p>"*12}</div></section>
<section class="cta"><hr class="slash"><h2>Mach mit</h2><p class="cta-sub">Together, we end suffering.</p><p class="cta-links"><a class="btn primary" href="#">Discord</a><a class="btn" href="#">WhatsApp</a><a class="btn" href="#">info@proextinction.com</a></p></section>
</main></div>
<footer class="foot"><p class="mono">Beispieldaten · Pro Extinction · {d["name"]}</p></footer>
<script>{js}</script></body></html>
'''
    (BRAND / c / 'beispiel' / 'bausteine.html').write_text(page)
    (BRAND / c / 'beispiel' / 'bausteine-mobil.html').write_text(f'''<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bausteine mobil · {d["name"]}</title>
<body style="margin:0;background:#444;display:grid;place-items:center;min-height:100vh"><iframe src="bausteine.html" title="Mobil 390 px" style="width:390px;height:844px;border:0;background:#fff"></iframe></body></html>
''')

def main():
    logo = (ROOT / 'concepts' / 'assets' / 'logo.svg').read_text()
    for c in CONCEPTS:
        d = BRAND / c; (d / 'beispiel').mkdir(parents=True, exist_ok=True)
        pretty_tokens(c)
        (d / 'brand-helmet.html').write_text(helmet(c))
        (d / 'BRAND.md').write_text(brand_md(c))
        (d / 'CLAUDE.md').write_text(claude_md(c))
        (d / 'README.md').write_text(readme(c))
        (d / 'wordmark.svg').write_text(wordmark_svg(c))
        (d / 'mark.svg').write_text(logo)
        (d / 'brand-props.json').write_text(props_json(c))
        examples(c)
    print('kits written:', ', '.join(CONCEPTS))

if __name__ == '__main__':
    main()
