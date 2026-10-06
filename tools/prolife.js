/* "I'm pro-life" joke button on the criticism page (theme B, wide screens only).
   It lives in the free space right of the side table of contents and jumps away before anyone can press it. */
(function () {
  var b = document.currentScript.previousElementSibling, toc = b.previousElementSibling, fx = .5, fy = .3, raf = 0;
  function zone() {
    if (getComputedStyle(b).display === 'none') return null;
    var r = toc.getBoundingClientRect(), w = b.offsetWidth, h = b.offsetHeight;
    if (!r.width || r.bottom < 0 || r.top > innerHeight) return null;
    var x0 = r.right + 32, x1 = innerWidth - 24 - w, y0 = Math.max(r.top, 90), y1 = Math.min(innerHeight - 24, y0 + Math.max(r.height, 360)) - h;
    return x1 - x0 < 60 || y1 - y0 < 60 ? null : { x0: x0, x1: x1, y0: y0, y1: y1 };
  }
  function place() {
    raf = 0;
    var z = zone();
    b.classList.toggle('off', !z);
    if (z) b.style.transform = 'translate(' + (z.x0 + fx * (z.x1 - z.x0)) + 'px,' + (z.y0 + fy * (z.y1 - z.y0)) + 'px)';
  }
  function later() { if (!raf) raf = requestAnimationFrame(place); }
  function flee(px, py) {   // new spot, far enough from the pointer
    var z = zone(); if (!z) return;
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
