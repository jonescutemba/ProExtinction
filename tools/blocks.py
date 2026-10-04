"""Turn raw lines into typed blocks and abridge long pages for concept previews."""
import re

def is_heading(l):
    return (len(l) <= 70 and not re.search(r'[.,;!]$', l) and ',' not in l and '/' not in l
            and not l[:1].isdigit() and not l.startswith(('*', '–', '-', '•', 'http', 'Protest')))

def is_list_line(l):
    return l.startswith(('*', '–', '- ', '•', '-')) and len(l) > 2

def blocks_of(lines, like=None):
    """Typed blocks. like: the English lines a translation mirrors 1:1; the structure is then read from them."""
    out = []
    skip = {'Discord', 'Whatsapp', 'WhatsApp'}
    keep = lambda l: l.strip() and l.strip() not in skip and not l.startswith('Proextinction Website -')
    pairs = list(zip(lines, like)) if like else [(l, l) for l in lines]
    pairs = [(t.strip(), l.strip()) for t, l in pairs if keep(l)]
    clean = [l for _, l in pairs]
    for n, (text, l) in enumerate(pairs):
        nxt = clean[n + 1] if n + 1 < len(clean) else ''
        # a line that introduces a list ("... if they:") is a lead-in sentence, not a chapter
        if is_heading(l) and is_list_line(nxt) and (l.endswith(':') or len(l) > 40 or ',' in l or l[:1].islower()) :
            out.append(('p', text)); continue
        if is_list_line(l):
            item = text.lstrip('*–-• ').strip()
            if out and out[-1][0] == 'ul': out[-1][1].append(item)
            else: out.append(('ul', [item]))
        elif is_heading(l): out.append(('h', text))
        else: out.append(('p', text))
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

def faq_pairs(lines, like=None):
    """Pairs of (question, [answer paragraphs]); returns (intro_lines, pairs). A numbered line whose number
    goes backwards (1., 2. inside answer 9) is a list inside the answer.

    Questions are lines starting with "N." (the source numbers them inconsistently, so the
    number is stripped and re-counted by CSS). Before question 10, short unnumbered lines
    ending in "?" also count (the English source forgets numbers on some early questions).
    like: the English lines a translation mirrors 1:1; questions are then found in them (Chinese and
    Hindi have no capitals and end questions with "？" or "।").
    """
    intro, pairs, cur, seen_late, last = [], [], None, False, 0
    for t, l in (zip(lines, like) if like else zip(lines, lines)):
        t, l = t.strip(), l.strip()
        if not l: continue
        m = re.match(r'^(\d+)\.\s*(.+)$', l)
        if m and cur and int(m.group(1)) < last:  # numbering restarts inside an answer: a sub-list, not a question
            cur[1].append(t)
        elif m:
            last = int(m.group(1))
            if last >= 10: seen_late = True
            cur = (re.sub(r'^\d+[.．、]\s*', '', t), []); pairs.append(cur)
        elif (l.endswith('?') or (l.isupper() and '?' in l)) and len(l) <= 62 and l.lstrip('¿¡')[:1].isupper() and not seen_late:
            cur = (t, []); pairs.append(cur)
        elif cur: cur[1].append(t)
        else: intro.append(t)
    return intro, pairs
