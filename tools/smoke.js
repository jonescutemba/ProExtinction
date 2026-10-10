/* End-of-page effect: when the reader scrolls to the very bottom of a long page, the page shakes briefly and dark smoke rises.
   Once per page (per view in the presentation). Only after real scrolling, so short pages and restored scroll positions stay calm.
   "Reduce motion" (OS setting): no shake, only a dark haze fading in and out. Clicks pass through. */
(function () {
  var d = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches && d.dataset.motion !== 'on';
  var key = null, travel = 0, last = 0, done = {};

  function pageKey() { return location.pathname + location.hash; }
  function check() {
    var k = pageKey(), y = window.pageYOffset || d.scrollTop;
    if (k !== key) { key = k; travel = 0; last = y; }
    if (y > last) travel += y - last;
    last = y;
    var room = d.scrollHeight - innerHeight;
    if (done[k] || room < 600 || travel < 400) return;
    if (y + innerHeight >= d.scrollHeight - 2) { done[k] = 1; fire(); }
  }
  addEventListener('scroll', check, { passive: true });
  addEventListener('hashchange', function () { key = null; });

  function dark() { return d.dataset.theme !== 'light'; }

  function fire() {
    if (reduce) return haze();
    shake();
    setTimeout(smoke, 180);
  }

  function shake() {
    if (!document.body.animate) return;
    var k = [], n = 9;
    for (var i = 0; i <= n; i++) {   // decaying rumble
      var a = i === n ? 0 : (1 - i / n) * 7;
      k.push({ transform: 'translate(' + (i % 2 ? -a : a).toFixed(1) + 'px,' + ((i % 3) - 1) * a * .4 + 'px) rotate(' + (i % 2 ? .18 : -.18) * (1 - i / n) + 'deg)' });
    }
    [].forEach.call(document.body.children, function (el) {
      if (el.tagName === 'SCRIPT' || el.hidden || el.classList.contains('pe-smoke')) return;
      el.animate(k, { duration: 650, easing: 'ease-out' });
    });
  }

  function layer(tag) {
    var el = document.createElement(tag);
    el.className = 'pe-smoke';
    el.setAttribute('aria-hidden', 'true');
    el.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:2147483000';
    document.body.appendChild(el);
    return el;
  }

  function haze() {
    var el = layer('div');
    el.style.background = 'linear-gradient(to top,' + (dark() ? 'rgba(70,62,60,.55)' : 'rgba(25,20,20,.35)') + ',transparent 70%)';
    el.style.opacity = 0;
    if (!el.animate) return el.remove();
    el.animate([{ opacity: 0 }, { opacity: 1 }, { opacity: 0 }], { duration: 3200, easing: 'ease-in-out' }).onfinish = function () { el.remove(); };
  }

  // Soft, lumpy puffs drawn once into small canvases, then reused as sprites.
  function sprites(rgb) {
    var out = [];
    for (var v = 0; v < 4; v++) {
      var c = document.createElement('canvas'), s = 128; c.width = c.height = s;
      var g = c.getContext('2d');
      for (var i = 0; i < 9; i++) {
        var x = s / 2 + (Math.random() - .5) * s * .35, y = s / 2 + (Math.random() - .5) * s * .35, r = s * (.18 + Math.random() * .2);
        var grad = g.createRadialGradient(x, y, 0, x, y, r);
        grad.addColorStop(0, 'rgba(' + rgb + ',.35)');
        grad.addColorStop(1, 'rgba(' + rgb + ',0)');
        g.fillStyle = grad; g.fillRect(0, 0, s, s);
      }
      out.push(c);
    }
    return out;
  }

  function smoke() {
    var cv = layer('canvas'), g = cv.getContext('2d');
    if (!g) return cv.remove();
    var dpr = Math.min(devicePixelRatio || 1, 1.5), W = innerWidth, H = innerHeight;
    cv.width = W * dpr; cv.height = H * dpr; g.scale(dpr, dpr);
    // dark smoke: charcoal on the dark theme (a little lighter than the page so it shows), near-black on the light theme
    var pics = sprites(dark() ? '78,70,68' : '28,24,24');
    var parts = [], total = Math.round(Math.min(220, Math.max(70, W / 9))), spawnFor = 1900, made = 0, t0 = performance.now(), prev = t0;
    function add() {
      var big = Math.random();
      parts.push({
        x: Math.random() * W, y: H + 40 + Math.random() * 60,
        vx: (Math.random() - .5) * 30, vy: -(70 + Math.random() * 110),
        s: 70 + big * 120, grow: 1.6 + Math.random() * 1.6, rot: Math.random() * 6.3, vr: (Math.random() - .5) * .6,
        life: 3600 + Math.random() * 2600, age: 0, seed: Math.random() * 100, pic: pics[(Math.random() * pics.length) | 0],
        peak: dark() ? .45 + Math.random() * .3 : .55 + Math.random() * .25
      });
    }
    function frame(now) {
      var dt = Math.min(50, now - prev); prev = now;
      var want = Math.min(total, Math.round(total * (now - t0) / spawnFor));
      while (made < want) { add(); made++; }
      g.clearRect(0, 0, W, H);
      for (var i = parts.length - 1; i >= 0; i--) {
        var p = parts[i]; p.age += dt;
        if (p.age >= p.life) { parts.splice(i, 1); continue; }
        var f = p.age / p.life, sec = dt / 1000;
        p.vx += Math.sin(now / 700 + p.seed) * 14 * sec;   // swirl
        p.vy *= 1 - .18 * sec;                            // rising slows down
        p.x += p.vx * sec; p.y += p.vy * sec; p.rot += p.vr * sec;
        var size = p.s * (1 + (p.grow - 1) * f);
        var a = (f < .15 ? f / .15 : 1 - (f - .15) / .85) * p.peak;
        g.globalAlpha = Math.max(0, a);
        g.save(); g.translate(p.x, p.y); g.rotate(p.rot);
        g.drawImage(p.pic, -size, -size, size * 2, size * 2);
        g.restore();
      }
      if (parts.length || made < total) requestAnimationFrame(frame);
      else cv.remove();
    }
    requestAnimationFrame(frame);
  }
})();
