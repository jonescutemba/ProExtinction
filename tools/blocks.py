"""Turn raw lines into typed blocks and abridge long pages for concept previews."""
import re

def is_heading(l):
    return (len(l) <= 70 and not re.search(r'[.,;!]$', l) and ',' not in l and '/' not in l
            and not l[:1].isdigit() and not l.startswith(('*', '–', '-', '•', 'http', 'Protest')))

def is_list_line(l):
    return l.startswith(('*', '–', '- ', '•', '-')) and len(l) > 2

def blocks_of(lines):
    out = []
    skip = {'Discord', 'Whatsapp', 'WhatsApp'}
    clean = [l.strip() for l in lines if l.strip() and l.strip() not in skip and not l.startswith('Proextinction Website -')]
    for n, l in enumerate(clean):
        nxt = clean[n + 1] if n + 1 < len(clean) else ''
        # a line that introduces a list ("... if they:") is a lead-in sentence, not a chapter
        if is_heading(l) and is_list_line(nxt) and (l.endswith(':') or len(l) > 40 or ',' in l or l[:1].islower()) :
            out.append(('p', l)); continue
        if is_list_line(l):
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
    """Pairs of (question, [answer paragraphs]); returns (intro_lines, pairs).

    Questions are lines starting with "N." (the source numbers them inconsistently, so the
    number is stripped and re-counted by CSS). Before question 10, short unnumbered lines
    ending in "?" also count (the English source forgets numbers on some early questions).
    """
    intro, pairs, cur, seen_late = [], [], None, False
    for l in lines:
        l = l.strip()
        if not l: continue
        m = re.match(r'^(\d+)\.\s*(.+)$', l)
        if m:
            if int(m.group(1)) >= 10: seen_late = True
            cur = (m.group(2).strip(), []); pairs.append(cur)
        elif l.endswith('?') and len(l) <= 62 and l[:1].isupper() and not seen_late:
            cur = (l, []); pairs.append(cur)
        elif cur: cur[1].append(l)
        else: intro.append(l)
    return intro, pairs
