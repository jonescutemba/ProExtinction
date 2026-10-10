(() => {
  // Fits the diagram labels to their boxes (any language or script) and, for the tree, wires "Generate new example".
  const fig = document.currentScript.parentNode, svg = fig.querySelector('svg'), btn = fig.querySelector('.dg-new');
  const tree = svg.classList.contains('dg-tree'), MAX = tree ? 270 : 220, BASE = tree ? 20 : 19;
  const fit = (g, label) => {
    const t = g.querySelector('text'), r = g.querySelector('rect'), x = +t.getAttribute('x');
    if (label != null) t.textContent = label;
    t.style.fontSize = '';
    let w = t.getComputedTextLength();
    if (!w) return;   // hidden view: measured again when it shows
    if (w > MAX) { t.style.fontSize = (BASE * MAX / w) + 'px'; w = MAX; }
    w = Math.max(120, w + 36);
    r.setAttribute('width', w); r.setAttribute('x', x - w / 2);
    if (!tree) r.setAttribute('rx', r.getAttribute('height') / 2);
  };
  const shrink = (t, max, base, label) => {   // headings and verdict: one line, smaller font when too wide
    if (!t) return;
    if (label != null) t.textContent = label;
    t.style.fontSize = '';
    const w = t.getComputedTextLength();
    if (w > max) t.style.fontSize = (base * max / w) + 'px';
  };
  const fitAll = () => {
    svg.querySelectorAll('.node').forEach(g => fit(g));
    shrink(svg.querySelector('.dg-heading'), 600, 52);
    shrink(svg.querySelector('.verdict'), 600, 30);
    svg.querySelectorAll('.center').forEach(t => shrink(t, 270, 40));
  };
  fitAll();
  if (document.fonts) document.fonts.ready.then(fitAll);
  if (window.IntersectionObserver) new IntersectionObserver(es => es.some(e => e.isIntersecting) && fitAll()).observe(svg);
  if (!btn) return;
  const all = JSON.parse(btn.dataset.examples);
  let order = [], cur = 0;
  const next = () => {
    if (!order.length) order = all.map((_, i) => i).filter(i => i !== cur).sort(() => Math.random() - .5);
    return order.pop();
  };
  btn.addEventListener('click', () => {
    cur = next();
    const [root, left, right, end] = all[cur];
    const l = svg.querySelectorAll('.side.l .node'), r = svg.querySelectorAll('.side.r .node');
    left.forEach((s, i) => fit(l[i], s));
    right.forEach((s, i) => fit(r[i], s));
    fit(svg.querySelector('.root'), root);
    shrink(svg.querySelector('.verdict'), 600, 30, end);
    svg.setAttribute('aria-label', `${svg.dataset.heading}. ${root}: ${left.join(', ')}. ${right.join(', ')}. ${end}`);
    svg.querySelectorAll('.flow,.node rect').forEach(e => { e.style.animation = 'none'; e.getBBox(); e.style.animation = ''; });
    svg.classList.remove('dg-swap'); void svg.getBBox(); svg.classList.add('dg-swap');
  });
})();
