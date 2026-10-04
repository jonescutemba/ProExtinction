"""Store an AI translation: python tools/put_translation.py <lang> <slug> <english-slug> <textfile>
The text file has exactly one line per line of content/en/<english-slug>.json."""
import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
lang, slug, en, src = sys.argv[1:5]
EN = json.loads((ROOT / 'content' / 'en' / f'{en}.json').read_text(encoding='utf-8'))
L = [l.rstrip() for l in pathlib.Path(src).read_text(encoding='utf-8').strip('\n').split('\n')]
if len(L) != len(EN):
    sys.exit(f'{lang}/{slug}: {len(L)} lines, English has {len(EN)}')
bad = [i for i, l in enumerate(L) if not l.strip() or '—' in l or any(q in l for q in '“”„‘’«»')]
if bad: sys.exit(f'{lang}/{slug}: empty line, em dash or curly quote in lines {bad}')
(ROOT / 'content' / lang / f'{slug}.json').write_text(json.dumps(L, ensure_ascii=False, indent=1), encoding='utf-8')
print(lang, slug, len(L), 'lines ok')
