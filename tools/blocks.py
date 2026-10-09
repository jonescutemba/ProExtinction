"""Turn raw lines into typed blocks and abridge long pages for concept previews."""
import re

def is_heading(l):
    return (len(l) <= 70 and not re.search(r'[.,;!]$', l) and ',' not in l and '/' not in l
            and not l[:1].isdigit() and not l.startswith(('*', '–', '-', '•', 'http')) and not l.lower().startswith('protest'))

def is_list_line(l):
    return l.startswith(('*', '–', '- ', '•', '-')) and len(l) > 2

def blocks_of(lines, like=None, join=(), drop=(), pics=None, heads=()):
    """Typed blocks. like: the English lines a translation mirrors 1:1; the structure is then read from them.
    join: indices (into lines) of join buttons; each run of them becomes one ('join',) block (WhatsApp + Discord).
    pics: {line index: picture number}; a ('pic', n) block follows the block of that line.
    heads: indices (into lines) of chapter titles set by hand; shown as chapters, without a trailing colon."""
    out = []
    btn = {'Discord', 'Whatsapp', 'WhatsApp'}
    keep = lambda l: l.strip() and not l.startswith('Proextinction Website -')
    pairs = list(zip(lines, like)) if like else [(l, l) for l in lines]
    pairs = [(i, t.strip(), l.strip()) for i, (t, l) in enumerate(pairs) if keep(l) and i not in drop]
    clean = [l for _, _, l in pairs]
    pics = pics or {}
    for n, (i, text, l) in enumerate(pairs):
        nxt = clean[n + 1] if n + 1 < len(clean) else ''
        if n and pairs[n - 1][0] in pics: out.append(('pic', pics[pairs[n - 1][0]]))
        if i in heads:
            out.append(('h', text.rstrip(':：').rstrip())); continue
        if l in btn or i in join:
            if not (out and out[-1][0] == 'join'): out.append(('join',))
            continue
        # a line that introduces a list ("... if they:") is a lead-in sentence, not a chapter
        if is_heading(l) and is_list_line(nxt) and (l.endswith(':') or len(l) > 40 or ',' in l or l[:1].islower()) :
            out.append(('p', text)); continue
        if is_list_line(l):
            item = text.lstrip('*–-• ').strip()
            if out and out[-1][0] == 'ul': out[-1][1].append(item)
            else: out.append(('ul', [item]))
        elif is_heading(l): out.append(('h', text))
        else: out.append(('p', text))
    if pairs and pairs[-1][0] in pics: out.append(('pic', pics[pairs[-1][0]]))
    return out

def pic_anchors(blocks):
    """Where pictures sit, as (heading ordinal, blocks after that heading, picture number)."""
    h, off, out = -1, 0, []
    for b in blocks:
        if b[0] == 'h': h += 1; off = 0
        elif b[0] == 'pic': out.append((h, off, b[1]))
        else: off += 1
    return out

def place_pics(blocks, anchors, en_heads):
    """Put pictures into a page with the same chapters but its own paragraphs: same chapter, same paragraph position
    (or the chapter's end if the chapter is shorter). A page with extra chapters is aligned from its end."""
    shift = max(0, sum(b[0] == 'h' for b in blocks) - en_heads)
    out, h, off = [], -1, 0
    todo = [(a[0] + shift if a[0] >= 0 else a[0], a[1], a[2]) for a in anchors]
    def flush(final=False):
        for a in [a for a in todo if a[0] == h and (final or a[1] <= off)]:
            out.append(('pic', a[2])); todo.remove(a)
    for b in blocks:
        if b[0] == 'h': flush(True); h += 1; off = 0; out.append(b); flush(); continue
        out.append(b); off += 1; flush()
    flush(True)
    out += [('pic', a[2]) for a in todo]
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
