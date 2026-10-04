"""Parse raw/<lang>/*.txt (innerText of the Google Sites pages) into content/<lang>/<slug>.json."""
import json, re, sys, pathlib, unicodedata
ROOT = pathlib.Path(__file__).resolve().parent.parent
SLUG = {'página-inicial': 'home'}
TAIL = ('Międzynarodowy WhatsApp', 'AbolishSuffering discord', 'https://chat.whatsapp.com')

def ascii_slug(s):
    s = SLUG.get(s, s)
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()

def parse(path):
    L = [l.strip() for l in path.read_text(encoding='utf-8').split('\n')]
    L = [l for l in L if l]
    i = L.index('Proextinction Website') + 1
    home = next(p for p in path.parent.glob('*.txt') if ascii_slug(p.stem) == 'home')
    H = [l.strip() for l in home.read_text(encoding='utf-8').split('\n') if l.strip()]
    j = H.index('Proextinction Website') + 1
    nav = []
    while j < len(H) and H[j] != H[j + 1:j + 2][0:1] and len(nav) < 20:
        if H[j] in nav: break
        nav.append(H[j]); j += 1
        if H[j - 1] in ('Kontakt', 'Mapa del sitio', 'Donazioni'): break
    if L[i:i + len(nav)] == nav: i += len(nav)
    end = next(k for k, l in enumerate(L) if l.startswith('info@proextinction.com') and k > i)
    body = L[i:end]
    while body and body[-1].startswith(TAIL): body.pop()
    return body, nav

if __name__ == '__main__':
    for lang in sys.argv[1:]:
        out = ROOT / 'content' / lang; out.mkdir(parents=True, exist_ok=True)
        for p in sorted((ROOT / 'raw' / lang).glob('*.txt')):
            body, nav = parse(p)
            s = ascii_slug(p.stem)
            (out / f'{s}.json').write_text(json.dumps(body, ensure_ascii=False, indent=1), encoding='utf-8')
            print(lang, s, len(body), '|', body[0][:60] if body else '-')
        print(lang, 'nav:', nav)
