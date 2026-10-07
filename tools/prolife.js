/* "I'm pro-life" joke button on the criticism page (theme B, wide screens only).
   It lives in the free space left of the text or right of the side table of contents,
   and jumps away (sometimes to the other side) before anyone can press it. */
(function () {
  var b = document.currentScript.previousElementSibling, toc = b.previousElementSibling, prose = toc.closest('.prose') || toc.parentNode,
      side = 'r', fx = .5, fy = .3, raf = 0;
  function zones() {   // {l, r}: free areas in viewport coordinates, or null where there is no room
    if (getComputedStyle(b).display === 'none') return {};
    var t = toc.getBoundingClientRect(), p = prose.getBoundingClientRect(), w = b.offsetWidth, h = b.offsetHeight;
    if (!t.width || t.bottom < 0 || t.top > innerHeight) return {};
    var y0 = Math.max(t.top, 90), y1 = Math.min(innerHeight - 96, y0 + Math.max(t.height, 360)) - h;   // keep clear of the scroll-to-top button
    if (y1 - y0 < 60) return {};
    var z = {}, rx0 = t.right + 32, rx1 = innerWidth - 24 - w, lx0 = 24, lx1 = p.left - 40 - w;
    if (rx1 - rx0 > 40) z.r = { x0: rx0, x1: rx1, y0: y0, y1: y1 };
    if (lx1 - lx0 > 40) z.l = { x0: lx0, x1: lx1, y0: y0, y1: y1 };
    return z;
  }
  function place() {
    raf = 0;
    var all = zones(), z = all[side] || all[side === 'r' ? 'l' : 'r'];
    b.classList.toggle('off', !z);
    if (z) b.style.transform = 'translate(' + (z.x0 + fx * (z.x1 - z.x0)) + 'px,' + (z.y0 + fy * (z.y1 - z.y0)) + 'px)';
  }
  function later() { if (!raf) raf = requestAnimationFrame(place); }
  function flee(px, py) {   // new spot, far enough from the pointer; every third jump or so switches sides
    var all = zones(), other = side === 'r' ? 'l' : 'r';
    if (all[other] && (!all[side] || Math.random() < .35)) side = other;
    var z = all[side]; if (!z) return;
    for (var i = 0; i < 12; i++) {
      var nx = Math.random(), ny = Math.random(),
          x = z.x0 + nx * (z.x1 - z.x0) + b.offsetWidth / 2, y = z.y0 + ny * (z.y1 - z.y0) + b.offsetHeight / 2;
      if (Math.hypot(x - px, y - py) > 140) break;
    }
    fx = nx; fy = ny; place();
  }
  document.addEventListener('pointermove', function (e) {
    if (b.classList.contains('off')) return;
    var r = b.getBoundingClientRect();
    if (e.clientX > r.left - 70 && e.clientX < r.right + 70 && e.clientY > r.top - 60 && e.clientY < r.bottom + 60) flee(e.clientX, e.clientY);
  }, { passive: true });
  b.addEventListener('pointerdown', function (e) { e.preventDefault(); flee(e.clientX, e.clientY); });
  b.addEventListener('focus', function () { var r = b.getBoundingClientRect(); flee(r.left, r.top); b.blur(); });
  b.addEventListener('click', function (e) { e.preventDefault(); var r = b.getBoundingClientRect(); flee(r.left, r.top); });
  addEventListener('scroll', later, { passive: true, capture: true });
  addEventListener('resize', later);
  addEventListener('hashchange', function () { setTimeout(later, 50); });
  new MutationObserver(later).observe(document.documentElement, { attributes: true, attributeFilter: ['data-concept'] });
  later();
})();
