"""Parse scraped Google Sites text dumps into structured JSON (title + blocks)."""
import json, re, sys, pathlib
SRC = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2])
NAV_END = {'en': 'Donate', 'de': 'Kontakt'}
FIX = {'WIr': 'Wir', 'Resourcen': 'Ressourcen', 'becaufse': 'because'}

def parse(path, lang):
    L = [l for l in path.read_text().split('\n')]
    # content starts after the last nav-end item within the header, then "Proextinction Website"
    head = L[:80]
    last_nav = max(i for i, l in enumerate(head) if l == NAV_END[lang])
    start = last_nav + 1
    while L[start].startswith('Proextinction Website'): start += 1
    end = next(i for i, l in enumerate(L) if l.startswith('info@proextinction.com'))
    body = L[start:end]
    for k, v in FIX.items(): body = [re.sub(r'\b' + k + r'\b', v, l) for l in body]
    return body

if __name__ == '__main__':
    lang = sys.argv[3]
    OUT.mkdir(parents=True, exist_ok=True)
    for p in sorted(SRC.glob('*.txt')):
        body = parse(p, lang)
        (OUT / (p.stem + '.json')).write_text(json.dumps(body, ensure_ascii=False, indent=1))
        print(p.stem, len(body), 'lines')
