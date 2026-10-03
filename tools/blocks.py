"""Turn raw lines into typed blocks and abridge long pages for concept previews."""
import re

def is_heading(l):
    return len(l) <= 70 and not re.search(r'[.,;!]$', l) and not l.startswith(('*', '–', '-', '•', 'http'))

def blocks_of(lines):
    out = []
    for l in lines:
        l = l.strip()
        if not l: continue
        if l.startswith(('*', '–', '- ', '•', '-')) and len(l) > 2:
            item = l.lstrip('*–-• ').strip()
            if out and out[-1][0] == 'ul': out[-1][1].append(item)
            else: out.append(('ul', [item]))
        elif is_heading(l): out.append(('h', l))
        else: out.append(('p', l))
    return out

def wcount(b):
    return sum(len(i.split()) for i in b[1]) if b[0] == 'ul' else len(b[1].split())

def abridge(blocks, limit=230):
    total, kept = 0, []
    for b in blocks:
        kept.append(b); total += wcount(b)
        if total >= limit and b[0] != 'h': break
    while kept and kept[-1][0] == 'h': kept.pop()
    return kept, len(kept) < len(blocks)

def faq_pairs(lines):
    """Pairs of (question, [answer paragraphs]); returns (intro_lines, pairs)."""
    intro, pairs, cur = [], [], None
    for l in lines:
        l = l.strip()
        if not l: continue
        if l.endswith('?') and len(l) < 170:
            cur = (l, []); pairs.append(cur)
        elif cur: cur[1].append(l)
        else: intro.append(l)
    return intro, pairs
