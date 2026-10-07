"""Build presentation/index.html: ONE self-contained page (the site) with both designs, all languages, light/dark."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build as B
ROOT = B.ROOT; esc = B.esc

FONTS = ('family=Oswald:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400'
         '&family=Anton&family=Barlow:wght@400;500;600&family=Bebas+Neue'
         '&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500')
def nav(lang):
    items = ''.join('<li><a href="#/%s/%s" data-slug="%s">%s</a></li>' % (lang, s, s, esc(B.NAV[lang][s])) for s, _ in B.PAGES[lang])
    return f'<nav class="sitenav" id="nav-{lang}" aria-label="Main" data-lang="{lang}" lang="{lang}" dir="{B.DIR(lang)}" hidden><ul>{items}</ul></nav>'

def build():
    views, navs, tails = [], [], []
    B.IMG_BASE = 'img/'
    for lang in B.LANGS:
        navs.append(nav(lang))
        for slug, kind in B.PAGES[lang]:
            B.ID_PREFIX = f'{lang}-{slug}-'
            title, main, _ = B.page_main(lang, slug, kind, href=lambda s, l=lang: f'#/{l}/{s}')
            views.append(f'<section class="view" data-view="{lang}/{slug}" lang="{lang}" dir="{B.DIR(lang)}" data-title="{esc(title)}" hidden>\n{main}\n</section>')
        B.ID_PREFIX = ''
        tails.append(f'<div data-lang="{lang}" lang="{lang}" dir="{B.DIR(lang)}" hidden>{B.footer(lang)}</div>')
    logo = B.logo_css()
    styles = f'<style id="logo">\n{logo}</style>\n' + ''.join(f'<style data-concept="{c}" media="{"all" if c == "a-ember" else "not all"}">\n{(ROOT / "concepts" / c / "style.css").read_text(encoding="utf-8").replace(logo, "")}\n</style>\n' for c in B.CONCEPTS)
    switch = ''.join(f'<button type="button" data-concept="{c}" aria-pressed="false" title="{B.CONCEPTS[c]["name"]}"><span class="k">{c[0].upper()}</span><span class="n">{B.CONCEPTS[c]["name"]}</span></button>' for c in B.CONCEPTS)
    pair = json.dumps({'en_of': B.EN_OF, 'of_en': B.OF_EN, 'ui': {l: {'code': B.CODE[l], 'dir': B.DIR(l), 'menu': B.T[l]['menu'], 'lang': B.T[l]['lang'], 'home': B.T[l]['home_link'], 'top': B.TOP[l]} for l in B.LANGS}}, ensure_ascii=False)
    js = (ROOT / 'tools' / 'present.js').read_text(encoding='utf-8')
    page = f'''<!doctype html>
<html lang="en" data-concept="a-ember" data-default="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pro Extinction</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style id="fonts">
{(ROOT / "tools" / "fonts.css").read_text(encoding="utf-8")}</style>
{styles}<script>(function(){{var d=document.documentElement,q=function(k){{try{{return new URLSearchParams(location.search).get(k)}}catch(e){{return null}}}},m={{a:'a-ember',b:'b-poster'}},c=m[q('concept')]||q('concept')||(function(){{try{{return localStorage.getItem('pe-concept')}}catch(e){{return null}}}})()||'a-ember';
if(!/^(a-ember|b-poster)$/.test(c))c='a-ember';d.dataset.concept=c;
[].forEach.call(document.querySelectorAll('style[data-concept]'),function(s){{s.media=s.dataset.concept===c?'all':'not all'}});
var t=q('theme');if(t!=='light'&&t!=='dark'){{try{{t=localStorage.getItem('pe-theme')}}catch(e){{t=null}}}}
d.dataset.theme=(t==='light'||t==='dark')?t:'dark'}})()</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><i></i></div>
{B.top_button("en")}
<header class="top">
  <div class="lead"><a class="brand" href="#/en/home" aria-label="Pro Extinction – home"><span class="logo" role="img" aria-label="Pro Extinction logo"></span><span class="wordmark">PRO EXTINCTION</span></a></div>
  <div class="tools">
    <div class="concepts" role="group" aria-label="Design">{switch}</div>
    {B.lang_select('en', lambda l: f'#/{l}/home')}
    <button class="theme" type="button" aria-label="Switch light/dark mode" title="Switch light/dark mode"><span></span></button>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-en"><span class="bars" aria-hidden="true"></span><span class="menu-t">Menu</span></button>
  </div>
</header>
<div class="shell">
{''.join(navs)}
<main id="main">
{chr(10).join(views)}
</main>
</div>
{''.join(tails)}
<script type="application/json" id="pair-map">{pair}</script>
<script>
{js}
</script>
</body>
</html>
'''
    out = ROOT / 'presentation' / 'index.html'
    out.write_text(page, encoding='utf-8')
    print('presentation/index.html', round(out.stat().st_size / 1024), 'KB,', len(views), 'views')

if __name__ == '__main__':
    build()
