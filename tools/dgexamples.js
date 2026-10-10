(() => {
  // "Generate new example": puts another two-paths example into the tree diagram above the button.
  const btn = document.currentScript.previousElementSibling, svg = btn.previousElementSibling;
  const all = JSON.parse(btn.dataset.examples);
  let order = [], cur = 0;
  const next = () => {
    if (!order.length) order = all.map((_, i) => i).filter(i => i !== cur).sort(() => Math.random() - .5);
    return order.pop();
  };
  const fit = (g, label) => {
    const t = g.querySelector('text'), r = g.querySelector('rect'), x = +t.getAttribute('x');
    t.textContent = label; t.style.fontSize = '';
    let w = t.getComputedTextLength();
    if (w > 270) { t.style.fontSize = (20 * 270 / w) + 'px'; w = 270; }
    w = Math.max(120, w + 36);
    r.setAttribute('width', w); r.setAttribute('x', x - w / 2);
  };
  btn.addEventListener('click', () => {
    cur = next();
    const [root, left, right, end] = all[cur];
    const l = svg.querySelectorAll('.side.l .node'), r = svg.querySelectorAll('.side.r .node');
    [left[0], left[1]].forEach((s, i) => fit(l[i], s));
    right.forEach((s, i) => fit(r[i], s));
    fit(svg.querySelector('.root'), root);
    const v = svg.querySelector('.verdict');
    v.textContent = end; v.style.fontSize = '';
    if (v.getComputedTextLength() > 600) v.style.fontSize = (30 * 600 / v.getComputedTextLength()) + 'px';
    svg.setAttribute('aria-label', `${svg.dataset.heading}. ${root}: ${left.join(', ')}. ${right.join(', ')}. ${end}`);
    svg.querySelectorAll('.flow,.node rect').forEach(e => { e.style.animation = 'none'; e.getBBox(); e.style.animation = ''; });
    svg.classList.remove('dg-swap'); void svg.getBBox(); svg.classList.add('dg-swap');
  });
})();
