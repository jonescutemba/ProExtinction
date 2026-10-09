import json, os, re
ROOT = '/home/user/ProExtinction/content'
def save(lang, page, lines):
    en = json.load(open(f'{ROOT}/en/{page}.json'))
    assert len(lines) == len(en), (lang, page, len(lines), len(en))
    bad = [i for i, x in enumerate(lines) if '—' in x or '“' in x or '”' in x]
    assert not bad, (lang, page, 'em dash or curly quotes in lines', bad)
    os.makedirs(f'{ROOT}/{lang}', exist_ok=True)
    open(f'{ROOT}/{lang}/{page}.json', 'w').write(json.dumps(lines, ensure_ascii=False, indent=1) + '\n')
    print('saved', lang, page, len(lines))
def keep(page, changes):
    """English lines with only some indices replaced (for pages of names and links)."""
    en = json.load(open(f'{ROOT}/en/{page}.json'))
    out = list(en)
    for i, t in changes.items(): out[i] = t
    return out
PARTS = '/tmp/claude-0/-home-user-ProExtinction/16256cb7-0ffb-59f1-9ca3-47aeaae4b0ca/scratchpad/tr/parts'
def part(lang, page, start, lines, last=False):
    """Collect a page in pieces; save once the last piece arrives."""
    os.makedirs(PARTS, exist_ok=True)
    f = f'{PARTS}/{lang}-{page}.json'
    have = json.load(open(f)) if os.path.exists(f) else {}
    for k, x in enumerate(lines): have[str(start + k)] = x
    json.dump(have, open(f, 'w'), ensure_ascii=False)
    print('part', lang, page, start, start + len(lines) - 1, 'total', len(have))
    if last:
        en = json.load(open(f'{ROOT}/en/{page}.json'))
        missing = [i for i in range(len(en)) if str(i) not in have]
        assert not missing, ('missing lines', missing)
        save(lang, page, [have[str(i)] for i in range(len(en))])
