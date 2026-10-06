"""Animated SVG diagrams that replace the manifesto pictures #5 and #6.

Colours and fonts come from the theme tokens (--accent, --line, --display ...), so both concepts and light/dark work.
Labels live in TEXT per language; a language without its own entry falls back to English.
"""
from html import escape as esc

TEXT = {
    'en': {
        5: dict(title='The cycle of suffering: birth leads to suffering, suffering beings reproduce, and reproduction leads to new births.',
                center=('Cycle of', 'suffering'), nodes=('Birth', 'Suffering', 'Reproduction')),
        6: dict(title='Cruel design: if the lion kills the zebra, the zebra dies a violent, painful death. If the zebra escapes, '
                      'the lion starves and dies slowly. Both paths end in suffering.',
                root='Cruel design', left=('Lion kills zebra', 'Violent, painful death'),
                right=('Zebra escapes', 'Lion starves', 'Slow starvation death'), end='Both paths end in suffering.'),
    },
}

_uid = [0]

def _id(name):
    _uid[0] += 1
    return f'dg{_uid[0]}-{name}'

def _pill(x, y, label, cls, h=46, size=19):
    w = max(120, int(len(label) * size * .62) + 36)
    return (f'<g class="{cls}"><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w}" height="{h}" rx="{h / 2:.0f}"/>'
            f'<text x="{x}" y="{y}" font-size="{size}">{esc(label)}</text></g>')

def cycle(t):
    import math
    cx, cy, r = 300, 225, 160
    arrow = _id('arrow')
    pos = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in (-90, 30, 150)]
    arcs = []
    for a in (-90, 30, 150):   # clockwise arcs between the nodes, leaving room for the labels
        a0, a1 = math.radians(a + 26), math.radians(a + 120 - 26)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        arcs.append(f'<path class="arc" d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" marker-end="url(#{arrow})"/>')
    nodes = ''.join(_pill(x, y, n, f'node n{i}') for i, ((x, y), n) in enumerate(zip(pos, t['nodes'])))
    c1, c2 = t['center']
    return (f'<svg class="dg dg-cycle" viewBox="0 0 600 450" role="img" aria-label="{esc(t["title"])}">'
            f'<defs><marker id="{arrow}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M1,1 L9,5 L1,9" class="tip"/></marker></defs>'
            f'<circle class="ring" cx="{cx}" cy="{cy}" r="{r}"/>{"".join(arcs)}'
            f'<circle class="runner" r="7"><animateMotion dur="6s" repeatCount="indefinite" rotate="auto" '
            f'path="M{cx},{cy - r} A{r},{r} 0 1 1 {cx - .01},{cy - r}"/></circle>'
            f'<text class="center" x="{cx}" y="{cy - 8}">{esc(c1)}</text><text class="center hot" x="{cx}" y="{cy + 30}">{esc(c2)}</text>'
            f'{nodes}</svg>')

def tree(t):
    arrow = _id('arrow')
    L, R, root_y, rows = 165, 475, 42, (150, 250, 350)
    hot = _id('hot')
    def line(d, cls): return f'<path class="{cls}" d="{d}" pathLength="1" marker-end="url(#{hot if cls.startswith("flow") else arrow})"/>'
    left = [f'M320,{root_y + 23} V100 H{L} V{rows[0] - 26}', f'M{L},{rows[0] + 23} V{rows[2] - 26}']
    right = [f'M320,{root_y + 23} V100 H{R} V{rows[0] - 26}', f'M{R},{rows[0] + 23} V{rows[1] - 26}', f'M{R},{rows[1] + 23} V{rows[2] - 26}']
    def branch(paths, side): return ''.join(line(d, 'wire') + line(d, f'flow {side}') for d in paths)
    box = lambda x, y, s, c: _pill(x, y, s, c, h=50, size=20).replace('rx="25"', 'rx="4"')
    return (f'<svg class="dg dg-tree" viewBox="0 0 640 450" role="img" aria-label="{esc(t["title"])}">'
            f'<defs><marker id="{arrow}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M1,1 L9,5 L1,9" class="tip"/></marker>'
            f'<marker id="{hot}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M1,1 L9,5 L1,9" class="tip hot-tip"/></marker></defs>'
            f'<g class="side l">{branch(left, "l")}{box(L, rows[0], t["left"][0], "node")}{box(L, rows[2], t["left"][1], "node end")}</g>'
            f'<g class="side r">{branch(right, "r")}{box(R, rows[0], t["right"][0], "node")}{box(R, rows[1], t["right"][1], "node")}'
            f'{box(R, rows[2], t["right"][2], "node end")}</g>'
            f'{box(320, root_y, t["root"], "node root")}'
            f'<text class="verdict" x="320" y="425">{esc(t["end"])}</text></svg>')

def diagram(n, lang='en'):
    t = TEXT.get(lang, TEXT['en']).get(n) or TEXT['en'][n]
    return (cycle if n == 5 else tree)(t)

NUMBERS = {5, 6}
