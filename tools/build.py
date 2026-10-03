"""Build the three design concepts (EN + DE) into concepts/<concept>/<lang>/*.html."""
import json, re, html, pathlib, sys, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from blocks import blocks_of, abridge, faq_pairs

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'concepts'
esc = html.escape

# slug, kind ('doc'|'faq'), original path on the live site, labels
PAGES = {
 'en': [
  ('home','home'),('manifesto','doc'),('basic-faq','faq'),('full-faq','faq'),
  ('criticism-of-different-pro-life-ideologies','doc'),('principles-of-the-movement','doc'),
  ('suffering-in-detail','doc'),('cosmic-extinction','doc'),('history','doc'),('join-us','doc'),
  ('social-media-channels','doc'),('contact','doc'),('donate','doc')],
 'de': [
  ('home','home'),('manifest','doc'),('basis-faq','faq'),('vollstaendiges-faq','faq'),
  ('die-prinzipien-unserer-bewegung','doc'),
  ('leid-im-detail','doc'),('geschichte','doc'),('aktiv-werden','doc'),
  ('kontakt','doc'),('ressourcen','doc')],
}
NAV = {
 'en': {'home':'Home','manifesto':'Manifesto','basic-faq':'Basic FAQ','full-faq':'Full FAQ',
  'criticism-of-different-pro-life-ideologies':'Criticism of pro-life ideologies',
  'principles-of-the-movement':'Principles of the movement','suffering-in-detail':'Suffering in detail',
  'cosmic-extinction':'Cosmic Extinction','history':'History','join-us':'Join us',
  'social-media-channels':'Social Media Channels','contact':'Contact','donate':'Donate'},
 'de': {'home':'Home','manifest':'Manifest','basis-faq':'Basis-FAQ','vollstaendiges-faq':'Vollständiges FAQ',
  'die-prinzipien-unserer-bewegung':'Die Prinzipien unserer Bewegung','leid-im-detail':'Leid im Detail',
  'geschichte':'Geschichte','aktiv-werden':'Aktiv werden','kontakt':'Kontakt','ressourcen':'Ressourcen'},
}
PAIR = {  # en slug -> de slug
 'home':'home','manifesto':'manifest','basic-faq':'basis-faq','full-faq':'vollstaendiges-faq',
 'criticism-of-different-pro-life-ideologies':'kritik-an-pro-life-ideologien',
 'principles-of-the-movement':'die-prinzipien-unserer-bewegung','suffering-in-detail':'leid-im-detail',
 'cosmic-extinction':'kosmisches-leben','history':'geschichte','join-us':'aktiv-werden',
 'social-media-channels':'social-media','contact':'kontakt','donate':'spenden'}
PAIR_REV = {v: k for k, v in PAIR.items()}
KI = set()  # machine-translated pages: translation is a separate step (content/_translation-pending)
ORIGINAL = {'en': 'https://www.proextinction.com/{}', 'de': 'https://sites.google.com/view/proextinctionwebsitegerman/{}'}
ORIG_DE_SLUG = {'vollstaendiges-faq': 'vollständiges-faq'}
ORIG_EN_SLUG = {'home': 'home'}

T = {
 'en': dict(menu='Menu', skip='Skip to content', lang='Language', theme='Switch light/dark mode',
  tagline='Together, we end suffering.', sub='The organisation dedicated to ending forced existence and suffering',
  cta1='Join us', cta2='Read the manifesto', mission='Our Mission',
  mission_text='Preventing as much suffering as physically possible, without tradeoffs.',
  effort='Effort', questions='Questions?', questions_text='Contact info@proextinction.com to get more information on the project',
  action='Take action', toc='On this page', abridged='Preview: the long list of channels is left out in this concept. The full list is on the current site:',
  abridged_link='Open the full page', ki='Machine-translated from English (AI). The German original site does not have this page. Abridged preview.',
  ki_tag='AI', back='Concepts', back_title='Back to the concept overview', progress='Reading progress', home_link='Pro Extinction – home',
  efforts=['Growing the movement to make it possible to prevent billions of years of suffering.',
   'Universal, non-discriminatory help for as many victims as physically possible. For animals, as much extraterrestrial life as possible, and humans.',
   'Purely organised action/activism based. No lamenting at the expense of the victims.',
   'Fully rational, empathetic, atheistic, logical, and fair.'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
 'de': dict(menu='Menü', skip='Zum Inhalt springen', lang='Sprache', theme='Hell/Dunkel umschalten',
  tagline='Together, we end suffering.', sub='Die Organisation, die sich für das Ende erzwungener Existenz und erzwungenen Leids einsetzt.',
  cta1='Aktiv werden', cta2='Manifest lesen', mission='Unsere Mission',
  mission_text='Wir zielen darauf ab, ohne Kompromisse, so viel Leid wie möglich zu beenden.',
  effort='Einsatz', questions='Fragen?', questions_text='Kontaktiere info@proextinction.com, um mehr Informationen zu bekommen.',
  action='Mach mit', toc='Auf dieser Seite', abridged='Vorschau: die lange Kanalliste ist in diesem Konzept weggelassen. Die vollständige Liste steht auf der aktuellen Seite:',
  abridged_link='Vollständige Seite öffnen', ki='Automatisch aus dem Englischen übersetzt (KI). Die deutsche Originalseite hat diese Seite nicht. Gekürzte Vorschau.',
  ki_tag='KI', back='Konzepte', back_title='Zurück zur Konzeptübersicht', progress='Lesefortschritt', home_link='Pro Extinction – Startseite',
  efforts=['Wir vergrößern die Bewegung, um unzählige Jahre Leid zu verhindern.',
   'Universelle, nicht diskriminierende Hilfe für so viele Opfer wie physisch möglich. Für Tiere, so viel außerirdisches Leben wie möglich und Menschen.',
   'Wir sind strikt handlungsorientiert, anstatt auf Kosten der Opfer nur über das extreme Leid zu klagen.',
   'Wir sind völlig rational, empathisch, atheistisch, logisch und fair.'],
  foot='Pro Extinction · Global · +44 7557095418', page_title='Pro Extinction'),
}
DISCORD = 'https://discord.gg/nb2K8y846R'
WHATSAPP = 'https://chat.whatsapp.com/J9WIHBa7Lqy8MyhlQYLogs'
EMAIL = 'info@proextinction.com'

CONCEPTS = {
 'a-ember':  dict(name='Ember',  mode='dark',  fonts='family=Oswald:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500'),
 'b-poster': dict(name='Poster', mode='dark',  fonts='family=Anton&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500'),
 'c-ring':   dict(name='Ring',   mode='light', fonts='family=Bebas+Neue&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500'),
}

def linkify(s):
    s = esc(s)
    s = re.sub(r'(https?://[^\s<]+)', lambda m: f'<a href="{m.group(1)}" rel="noopener">{m.group(1)}</a>', s)
    return re.sub(r'\b([\w.+-]+@[\w-]+\.[\w.-]+)\b', r'<a href="mailto:\1">\1</a>', s)

def slug_id(s, used):
    base = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40] or 'section'
    i, k = base, 2
    while i in used: i = f'{base}-{k}'; k += 1
    used.add(i); return i

def render_blocks(blocks, used):
    out, toc = [], []
    for b in blocks:
        if b[0] == 'h':
            i = slug_id(b[1], used); toc.append((i, b[1].rstrip(':')))
            out.append(f'<h2 id="{i}">{esc(b[1].rstrip(":"))}</h2>')
        elif b[0] == 'ul':
            out.append('<ul>' + ''.join(f'<li>{linkify(i)}</li>' for i in b[1]) + '</ul>')
        else:
            out.append(f'<p>{linkify(b[1])}</p>')
    return '\n'.join(out), toc

def head_lede(lines):
    title, rest = lines[0], lines[1:]
    lede = None
    from blocks import is_heading
    if len(rest) > 1 and len(rest[0]) <= 90 and not rest[0].endswith('?') \
            and (rest[0].endswith('.') or is_heading(rest[0])) and is_heading(rest[1]) and not rest[1].endswith('?'):
        lede, rest = rest[0].rstrip(':'), rest[1:]
    return title, lede, rest

def doc_body(lang, slug, lines, full_url):
    t = T[lang]; used = set()
    title, lede, rest = head_lede(lines)
    kind = 'doc'; truncated = False
    if slug in ('social-media-channels',):
        bl = blocks_of(rest)[:2]; truncated = True
    else:
        bl = blocks_of(rest)
    body, toc = render_blocks(bl, used)
    return title, lede, body, toc, truncated

def faq_body(lang, slug, lines):
    t = T[lang]
    title, lede, rest = head_lede(lines)
    intro, pairs = faq_pairs(rest)
    shown = pairs
    intro_html = ''.join(f'<p>{linkify(l)}</p>' for l in intro)
    items = []
    for q, a in shown:
        items.append(f'<details><summary>{esc(q)}</summary><div class="a">' + ''.join(f'<p>{linkify(p)}</p>' for p in a) + '</div></details>')
    return title, lede, intro_html + '<div class="faq">' + '\n'.join(items) + '</div>', [], len(shown) < len(pairs)

def sitenav(lang, slug):
    t = T[lang]; cur = ' aria-current="page"'
    items = ''.join('<li><a href="%s.html"%s>%s</a></li>' % (s_, cur if s_ == slug else '', esc(NAV[lang][s_])) for s_, _ in PAGES[lang])
    return f'<nav class="sitenav" aria-label="Main"><ul>{items}</ul></nav>'

def header(c, lang, slug, ctx):
    t = T[lang]; other = 'de' if lang == 'en' else 'en'
    other_slug = (PAIR[slug] if lang == 'en' else PAIR_REV.get(slug, 'home'))
    if other == 'de' and other_slug not in NAV['de']: other_slug = 'home'
    return f'''<a class="skip" href="#main">{t["skip"]}</a>
<div class="progress" aria-hidden="true"><i></i></div>
<header class="top">
  <div class="lead">
    <a class="brand" href="home.html" aria-label="{t["home_link"]}"><span class="logo" role="img" aria-label="Pro Extinction logo"></span><span class="wordmark">PRO EXTINCTION</span></a>
    <a class="back" href="../../index.html" title="{t["back_title"]}"><span aria-hidden="true">←</span> {t["back"]}</a>
  </div>
  <div class="tools">
    <a class="lang" href="../{other}/{other_slug}.html" hreflang="{other}" lang="{other}" aria-label="{t["lang"]}: {other.upper()}">{other.upper()}</a>
    <button class="theme" type="button" aria-label="{t["theme"]}" title="{t["theme"]}"><span></span></button>
  </div>
</header>'''

def footer(lang):
    t = T[lang]
    return f'''<section class="cta" aria-label="{t["action"]}">
  <hr class="slash">
  <h2>{t["action"]}</h2>
  <p class="cta-sub">{t["tagline"]}</p>
  <p class="cta-links"><a class="btn primary" href="{DISCORD}" rel="noopener">Discord</a><a class="btn" href="{WHATSAPP}" rel="noopener">WhatsApp</a><a class="btn" href="mailto:{EMAIL}">{EMAIL}</a></p>
</section>
<footer class="foot"><p class="mono">{t["foot"]}</p></footer>'''

def page_html(c, lang, slug, kind):
    t = T[lang]; cdef = CONCEPTS[c]
    ki = lang == 'de' and slug in KI
    if kind == 'home':
        main = home_main(lang)
        title = NAV[lang]['home']
        body_class = 'home'
    else:
        lines = json.loads((ROOT / 'content' / lang / f'{slug}.json').read_text())
        if kind == 'faq': title, lede, body, toc, truncated = faq_body(lang, slug, lines)
        else: title, lede, body, toc, truncated = doc_body(lang, slug, lines, '')
        if lang == 'en': orig = ORIGINAL['en'].format(slug)
        else: orig = ORIGINAL['de'].format(urllib.parse.quote(ORIG_DE_SLUG.get(slug, slug)))
        notes = ''
        if ki: notes += f'<p class="note ki"><span class="tag">{t["ki_tag"]}</span> {t["ki"]}</p>'
        elif truncated: notes += f'<p class="note">{t["abridged"]} <a href="{orig}" rel="noopener">{t["abridged_link"]}</a></p>'
        toc_html = ''
        if len(toc) > 1:
            toc_html = f'<nav class="toc" aria-label="{t["toc"]}"><p class="mono">{t["toc"]}</p><ol>' + ''.join(f'<li><a href="#{i}">{esc(n)}</a></li>' for i, n in toc) + '</ol></nav>'
        lede_html = f'<p class="lede">{esc(lede)}</p>' if lede else ''
        main = f'<article class="doc"><header class="doc-head"><p class="mono kicker">{esc(NAV[lang][slug])}</p><h1>{esc(title)}</h1>{lede_html}<hr class="slash"></header>{toc_html}<div class="prose">{notes}{body}</div></article>'
        body_class = 'page'
    other = 'de' if lang == 'en' else 'en'
    return f'''<!doctype html>
<html lang="{lang}" data-concept="{c}" data-default="{cdef["mode"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} – Pro Extinction · {cdef["name"]}</title>
<meta name="robots" content="noindex">
<script>(function(){{var d=document.documentElement,m=null;try{{m=new URLSearchParams(location.search).get('theme')||localStorage.getItem('pe-theme')}}catch(e){{}}
if(m!=='light'&&m!=='dark'){{m=window.matchMedia&&matchMedia('(prefers-color-scheme: light)').matches?'light':(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':d.dataset.default)}}d.dataset.theme=m}})()</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{cdef["fonts"]}&display=swap">
<link rel="stylesheet" href="../style.css">
</head>
<body class="{body_class}">
{header(c, lang, slug, None)}
<div class="shell">
{sitenav(lang, slug)}
<main id="main">
{main}
</main>
</div>
{footer(lang)}
<script src="../../assets/site.js" defer></script>
</body>
</html>
'''

def home_main(lang):
    t = T[lang]
    efforts = ''.join(f'<li><span class="num mono">{i+1:02d}</span><p class="eff-label mono">{t["effort"]} {i+1}</p><p>{esc(x)}</p></li>' for i, x in enumerate(t['efforts']))
    return f'''<section class="hero">
  <span class="logo hero-logo" role="img" aria-label="Pro Extinction logo"></span>
  <h1 class="wordmark">PRO EXTINCTION</h1>
  <p class="hero-tag">{t["tagline"]}</p>
  <p class="hero-sub">{esc(t["sub"])}</p>
  <p class="hero-cta"><a class="btn primary" href="{ 'aktiv-werden' if lang=='de' else 'join-us'}.html">{t["cta1"]}</a><a class="btn" href="{ 'manifest' if lang=='de' else 'manifesto'}.html">{t["cta2"]}</a></p>
</section>
<section class="mission"><hr class="slash"><p class="mono kicker">{t["mission"]}</p><blockquote>{esc(t["mission_text"])}</blockquote></section>
<section class="efforts"><ol>{efforts}</ol></section>
<section class="questions"><h2>{t["questions"]}</h2><p>{linkify(t["questions_text"])}</p></section>'''

def logo_css():
    svg = (OUT / 'assets' / 'logo.svg').read_text().replace('currentColor', '#000')
    uri = 'data:image/svg+xml,' + urllib.parse.quote(svg, safe="/:=' ")
    return f'.logo{{--logo:url("{uri}");-webkit-mask:var(--logo) center/contain no-repeat;mask:var(--logo) center/contain no-repeat;background:currentColor;display:inline-block}}\n'

def build():
    css_base = (ROOT / 'tools/css/base.css').read_text()
    for c in CONCEPTS:
        css = css_base + '\n' + (ROOT / 'brand' / c / 'tokens.css').read_text() + '\n' + (ROOT / f'tools/css/{c[0]}.css').read_text() + '\n' + logo_css()
        (OUT / c).mkdir(parents=True, exist_ok=True)
        (OUT / c / 'style.css').write_text(css)
        for lang in ('en', 'de'):
            d = OUT / c / lang; d.mkdir(exist_ok=True)
            for slug, kind in PAGES[lang]:
                (d / f'{slug}.html').write_text(page_html(c, lang, slug, kind))
    n = sum(len(PAGES[l]) for l in PAGES) * len(CONCEPTS)
    print('built', n, 'pages')

if __name__ == '__main__': build()

INDEX = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pro Extinction – design concepts</title><meta name="robots" content="noindex">
<style>:root{color-scheme:dark light;--bg:#0d0809;--text:#dcd8d8;--muted:#9a9292;--line:#2c2224;--accent:#e8484d}
@media (prefers-color-scheme:light){:root{--bg:#f4f0ea;--text:#151011;--muted:#5e5656;--line:#cfc6ba;--accent:#a30f14}}
body{margin:0;background:var(--bg);color:var(--text);font:1.05rem/1.6 Georgia,serif;padding:clamp(1.2rem,5vw,3rem);max-width:56rem;margin-inline:auto}
h1{font:600 clamp(2rem,6vw,3.4rem)/1 "Arial Narrow",Impact,sans-serif;text-transform:uppercase;margin:0 0 .5rem}
p{color:var(--muted)}li{border-top:1px solid var(--line);padding:1.2rem 0;list-style:none}ul{padding:0;margin:2rem 0}
h2{font:600 1.5rem "Arial Narrow",Impact,sans-serif;text-transform:uppercase;margin:0 0 .3rem}a{color:var(--accent);margin-right:1.2rem}</style></head>
<body><h1>Pro Extinction – design concepts</h1>
<p>Three directions for the redesign. All have a light/dark switch (button top right), EN and DE. Preview build with abridged texts.</p>
<ul>
<li><h2>A · Ember</h2><p>Angular, editorial, asymmetric. Red/black/silver, serif body text.</p><a href="a-ember/en/home.html">English</a><a href="a-ember/de/home.html">Deutsch</a></li>
<li><h2>B · Poster</h2><p>Angular, centred, loud. Red/black/silver, sans-serif body text.</p><a href="b-poster/en/home.html">English</a><a href="b-poster/de/home.html">Deutsch</a></li>
<li><h2>C · Ring</h2><p>Round, sepia and ink, editorial. Serif body text.</p><a href="c-ring/en/home.html">English</a><a href="c-ring/de/home.html">Deutsch</a></li>
</ul></body></html>
'''
(OUT / 'index.html').write_text(INDEX)
