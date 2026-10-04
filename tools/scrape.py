"""Scrape Google Sites language versions of Pro Extinction into raw/<lang>/<slug>.txt (innerText).
Usage: python tools/scrape.py pl es it   (needs playwright)"""
import sys, pathlib, re, urllib.parse
import urllib.request, ssl
from playwright.sync_api import sync_playwright

# Chromium may not trust a TLS-intercepting proxy; fetch through Python (system CA config) instead.
CTX = ssl.create_default_context(cafile=__import__('os').environ.get('SSL_CERT_FILE'))
def fetch(route):
    r = route.request
    if r.resource_type in ('image', 'media', 'font'): return route.abort()
    try:
        req = urllib.request.Request(r.url, data=r.post_data_buffer, method=r.method,
                                     headers={k: v for k, v in r.headers.items() if k.lower() not in ('host', 'content-length')})
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            route.fulfill(status=resp.status, headers=dict(resp.headers), body=resp.read())
    except urllib.error.HTTPError as e:
        route.fulfill(status=e.code, body=e.read())
    except Exception:
        route.abort()

SITES = {
    'pl': 'https://sites.google.com/view/proextinction-website-polish/home',
    'es': 'https://sites.google.com/view/proextinction-website-spanish/p%C3%A1gina-inicial',
    'it': 'https://sites.google.com/view/proextinction-website-italian',
}
OUT = pathlib.Path(__file__).resolve().parent.parent / 'raw'

def slug(url, root):
    p = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    rest = p[len(root):].strip('/')
    return rest.replace('/', '__') or 'home'

def scrape(lang, start, page):
    page.goto(start, wait_until='load')
    root = '/'.join(urllib.parse.urlparse(page.url).path.split('/')[:3])  # /view/<site>
    hrefs = page.eval_on_selector_all('a[href]', 'as => as.map(a => a.href)')
    links, seen = [page.url], set()
    for h in hrefs:
        h = h.split('#')[0].split('?')[0]
        if urllib.parse.urlparse(h).path.startswith(root) and h not in links: links.append(h)
    d = OUT / lang; d.mkdir(parents=True, exist_ok=True)
    found = set()
    for u in links:
        s = slug(u, root)
        if s in seen: continue
        seen.add(s)
        page.goto(u, wait_until='load')
        txt = page.inner_text('body')
        (d / (s + '.txt')).write_text(txt, encoding='utf-8')
        for q in re.findall(r'sites\.google\.com%2Fview%2F([^%&"]+)', page.content()): found.add(q)
        print(lang, s, len(txt.splitlines()), 'lines')
    return found

if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = b.new_page(); pg.route('**/*', fetch)
        other = set()
        for lang in sys.argv[1:] or SITES:
            other |= scrape(lang, SITES[lang], pg)
        print('language sites linked:', sorted(other))
        b.close()
