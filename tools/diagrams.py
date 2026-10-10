"""Animated SVG diagrams that replace the manifesto pictures #5 and #6.

Colours and fonts come from the theme tokens (--accent, --line, --display ...), so both concepts and light/dark work.
Labels live in TEXT per language; a language without its own entry falls back to English.
"""
from html import escape as esc

TEXT = {
    'en': {
        5: dict(title='The cycle of suffering: birth leads to suffering, suffering beings reproduce, and reproduction leads to new births.',
                center=('Cycle of', 'suffering'), nodes=('Birth', 'Suffering', 'Reproduction')),
        6: dict(heading='Cruel Design', title='Cruel design, predation: if the lion kills the zebra, the zebra dies a violent, painful death. If the zebra escapes, '
                      'the lion starves and dies slowly. Both paths end in suffering.',
                root='Predation', left=('Lion kills zebra', 'Violent, painful death'),
                right=('Zebra escapes', 'Lion starves', 'Slow starvation death'), end='Both paths end in suffering.'),
    },
}

# More "two paths, both end in suffering" examples for diagram 6; a button cycles through them (English only for now).
# Shape: root, left (choice, end), right (choice, step, end), verdict. Node labels stay short so the boxes fit.
EXAMPLES = [
    ('Drought season', ('Herd stays put', 'Dies of thirst'), ('Herd migrates', 'Crocodiles wait', 'Torn apart in river'), 'Both paths end in suffering.'),
    ('Winter comes', ('Bird stays', 'Freezes to death'), ('Bird migrates', 'Storm over the sea', 'Drowns exhausted'), 'Both paths end in suffering.'),
    ('Parasitic wasp', ('Wasp finds a host', 'Host eaten from inside'), ('No host found', 'Larvae cannot grow', 'Offspring starve'), 'Both paths end in suffering.'),
    ('Sea turtle hatching', ('Run to the sea', 'Eaten by birds'), ('Reach the water', 'Sharks and nets', 'Most die young'), 'Both paths end in suffering.'),
    ('A child is born', ('Born into poverty', 'Hunger and disease'), ('Born into wealth', 'Grows old anyway', 'Illness and death'), 'Every birth ends in death.'),
    ('Egg industry', ('Chick is female', 'Spent, then killed'), ('Chick is male', 'Useless to industry', 'Shredded on day one'), 'Both paths end in suffering.'),
    ('Dairy industry', ('Calf is female', 'Milked, then killed'), ('Calf is male', 'Taken from mother', 'Killed for veal'), 'Both paths end in suffering.'),
    ('Population boom', ('Rabbits multiply', 'Mass starvation'), ('Foxes multiply', 'Rabbits are hunted', 'Then foxes starve'), 'Both paths end in suffering.'),
    ('Old age', ('Body keeps going', 'Pain and dementia'), ('Body gives up', 'Organs fail', 'Dies in a hospital'), 'Both paths end in suffering.'),
    ('War breaks out', ('Soldier fights', 'Killed or maimed'), ('Soldier refuses', 'Prison or exile', 'Family is punished'), 'Both paths end in suffering.'),
    ('The flood comes', ('Flee the flood', 'Lose home and land'), ('Stay and hold on', 'Water keeps rising', 'Drowns with the house'), 'Both paths end in suffering.'),
    ('Cheetah mother', ('Leaves to hunt', 'Cubs taken by hyenas'), ('Stays with cubs', 'No food comes', 'Cubs starve'), 'Both paths end in suffering.'),
    ('Spider web', ('Fly is caught', 'Eaten alive slowly'), ('Fly escapes', 'Web stays empty', 'Spider starves'), 'Both paths end in suffering.'),
    ('Fishing boat', ('Fish is caught', 'Suffocates on deck'), ('Fish escapes', 'Bigger fish waits', 'Eaten alive'), 'Both paths end in suffering.'),
    ('Chronic pain', ('Live with it', 'Years of agony'), ('Take painkillers', 'Addiction grows', 'Withdrawal or overdose'), 'Both paths end in suffering.'),
    ('Stray dog', ('Left on the street', 'Hunger and cars'), ('Taken to a shelter', 'Shelter is full', 'Caged for years'), 'Both paths end in suffering.'),
    ('Love someone', ('You die first', 'They grieve'), ('They die first', 'You stay behind', 'You grieve'), 'Every bond ends in grief.'),
    ('Wildfire', ('Deer runs', 'Burned in the smoke'), ('Deer hides', 'Fire reaches it', 'Burned alive'), 'Both paths end in suffering.'),
    ('Pack hierarchy', ('Wolf fights leader', 'Wounded or killed'), ('Wolf submits', 'Eats last', 'Starves in winter'), 'Both paths end in suffering.'),
    ('Infection spreads', ('Sick deer stays', 'Herd gets infected'), ('Deer is cast out', 'Alone and weak', 'Wolves find it'), 'Both paths end in suffering.'),
    # a few lighter ones
    ('Monday morning', ('Get up for work', 'Tired all day'), ('Keep sleeping', 'Boss calls', 'Fired, still tired'), 'Both paths end in suffering.'),
    ('Last slice of pizza', ('Eat it', 'Stomach ache'), ('Leave it', 'Roommate eats it', 'Eternal regret'), 'Both paths end in suffering.'),
    ('Phone at 1%', ('Look for a charger', 'Every outlet taken'), ('Keep scrolling', 'Screen goes black', 'Alone with thoughts'), 'Both paths end in suffering.'),
    ('Group project', ('Do all the work', 'Others get credit'), ('Do nothing', 'Nobody else does', 'Everyone fails'), 'There is no winning.'),
    ('Hot summer night', ('Open the window', 'Mosquitoes feast'), ('Keep it closed', 'Room is a sauna', 'No sleep at all'), 'Both paths end in suffering.'),
    ('Software update', ('Install now', 'Everything breaks'), ('Remind me later', 'It asks again', 'Restarts mid-work'), 'Both paths end in suffering.'),
    ('Gym membership', ('Go to the gym', 'Sore for a week'), ('Stay on the couch', 'Still paying fees', 'Guilt and back pain'), 'Both paths end in suffering.'),
]
for _r, _l, _rt, _v in EXAMPLES:
    assert all(len(x) <= 22 for x in (*_l, *_rt)) and len(_r) <= 28 and len(_v) <= 32 and '—' not in _r + _v, _r

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
    return (f'<svg class="dg dg-tree" viewBox="0 0 640 530" role="img" aria-label="{esc(t["title"])}" data-heading="{esc(t["heading"])}">'
            f'<defs><marker id="{arrow}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M1,1 L9,5 L1,9" class="tip"/></marker>'
            f'<marker id="{hot}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M1,1 L9,5 L1,9" class="tip hot-tip"/></marker></defs>'
            f'<text class="dg-heading" x="320" y="34">{esc(t["heading"])}</text><g transform="translate(0,80)">'
            f'<g class="side l">{branch(left, "l")}{box(L, rows[0], t["left"][0], "node")}{box(L, rows[2], t["left"][1], "node end")}</g>'
            f'<g class="side r">{branch(right, "r")}{box(R, rows[0], t["right"][0], "node")}{box(R, rows[1], t["right"][1], "node")}'
            f'{box(R, rows[2], t["right"][2], "node end")}</g>'
            f'{box(320, root_y, t["root"], "node root")}'
            f'<text class="verdict" x="320" y="425">{esc(t["end"])}</text></g></svg>')

NEW_EXAMPLE = 'Generate new example'
_JS = open(__file__.rsplit('/', 1)[0] + '/dgexamples.js', encoding='utf-8').read()

def diagram(n, lang='en'):
    t = TEXT.get(lang, TEXT['en']).get(n) or TEXT['en'][n]
    if n == 5: return cycle(t)
    import json
    first = (t['root'], t['left'], t['right'], t['end'])
    data = esc(json.dumps([first] + EXAMPLES, ensure_ascii=False))
    return (tree(t) + f'<button class="btn dg-new" type="button" data-examples="{data}">{esc(NEW_EXAMPLE)}</button>'
            f'<script>{_JS}</script>')

NUMBERS = {5, 6}
