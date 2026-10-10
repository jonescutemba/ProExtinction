/* Small easter eggs, shared by the pages and the presentation:
   1. Cosmic extinction page: faint stars go out one by one while the reader scrolls; at the end the sky is dark.
   2. Logo clicked five times quickly: the page fades into nothing, the manifesto's last line appears, then everything returns.
   3. Footer: humans and farm animals born since the page was opened (estimate from yearly figures).
   4. A note in the browser console for the curious.
   "Reduce motion" (OS setting): no twinkle and no drifting, only fades. */
(function () {
  var d = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches && d.dataset.motion !== 'on';
  var visible = function (el) { return !!(el && el.getClientRects().length); };   // also true for position:fixed

  // ---- 1. stars
  function stars() {
    [].forEach.call(document.querySelectorAll('.stars'), function (box) {
      if (box.dataset.ready) return;
      box.dataset.ready = '1';
      var n = 70;
      for (var i = 0; i < n; i++) {
        var s = document.createElement('i');
        s.style.left = (Math.random() * 100).toFixed(2) + '%';
        s.style.top = (Math.random() * 100).toFixed(2) + '%';
        var r = Math.random(), size = r < .07 ? 5 : r < .2 ? 3.5 : r < .55 ? 2 : 1.4;   // a few big ones, most small
        s.style.width = s.style.height = size + 'px';
        if (size >= 3.5) s.className = 'big';
        s.style.animationDelay = (-Math.random() * 4).toFixed(2) + 's';
        s.style.animationDuration = (2.5 + Math.random() * 3).toFixed(2) + 's';
        box.appendChild(s);
      }
      // random order in which they go out
      box._order = [].slice.call(box.children).sort(function () { return Math.random() - .5; });
      box._out = 0;
    });
    sky();
  }
  function sky() {
    [].forEach.call(document.querySelectorAll('.stars'), function (box) {
      if (!visible(box) || !box._order) return;
      var room = d.scrollHeight - innerHeight;
      var f = room > 0 ? Math.min(1, (window.pageYOffset || d.scrollTop) / room) : 0;
      var want = Math.round(box._order.length * f);
      while (box._out < want) box._order[box._out++].classList.add('out');   // once out, a star stays out
    });
  }
  addEventListener('scroll', sky, { passive: true });
  addEventListener('hashchange', function () { setTimeout(stars, 50); });
  stars();

  // ---- 2. logo five times: back to nothing
  var clicks = [];
  document.addEventListener('click', function (e) {
    var logo = e.target.closest && e.target.closest('.brand .logo, .hero-logo');
    if (!logo) return;
    var now = Date.now(), t;
    try { t = JSON.parse(sessionStorage.getItem('pe-void') || '[]'); } catch (x) { t = clicks; }
    t = t.filter(function (x) { return now - x < 3000; }); t.push(now);
    try { sessionStorage.setItem('pe-void', JSON.stringify(t)); } catch (x) { clicks = t; }
    if (t.length >= 2) e.preventDefault();   // fast clicks stay on the page instead of reloading home
    if (t.length >= 5) {
      try { sessionStorage.removeItem('pe-void'); } catch (x) {} clicks = [];
      vanish();
    }
  }, true);

  var vanishing = false;
  function vanish() {
    if (vanishing || !document.body.animate) return;
    vanishing = true;
    var foot = [].filter.call(document.querySelectorAll('.foot[data-peace]'), visible)[0];
    var line = foot ? foot.dataset.peace : 'Long live peace!';
    var parts = [].filter.call(document.querySelectorAll('header.top, .sitenav, .progress, .stars, main h1, main h2, main h3, main p, main li, main figure, main img, main svg, main blockquote, main .btn, .hero-logo, .cta, .foot, .toc'), function (el) {
      if (!visible(el)) return false;
      var r = el.getBoundingClientRect();
      return r.bottom > 0 && r.top < innerHeight;
    });
    var gone = [];
    parts.forEach(function (el) {
      var delay = reduce ? 0 : Math.random() * 1200;
      var a = el.animate(reduce ? [{ opacity: 1 }, { opacity: 0 }] :
        [{ opacity: 1, filter: 'blur(0)', transform: 'none' }, { opacity: 0, filter: 'blur(6px)', transform: 'translateY(-12px)' }],
        { duration: reduce ? 600 : 900, delay: delay, easing: 'ease-in', fill: 'forwards' });
      gone.push(a);
    });
    var msg = document.createElement('div');
    msg.className = 'void-line';
    msg.setAttribute('role', 'status');
    msg.textContent = line;
    document.body.appendChild(msg);
    var show = msg.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 900, delay: reduce ? 600 : 2100, fill: 'forwards' });
    show.onfinish = function () {
      setTimeout(function () {
        msg.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 700, fill: 'forwards' }).onfinish = function () { msg.remove(); };
        gone.forEach(function (a) { a.reverse(); });
        setTimeout(function () { gone.forEach(function (a) { a.cancel(); }); vanishing = false; }, 1500);
      }, 2200);
    };
  }

  // ---- 3. births since the page was opened
  var t0 = Date.now(), fmt = {};
  function births() {
    var sec = (Date.now() - t0) / 1000;
    [].forEach.call(document.querySelectorAll('.born[data-rates]'), function (p) {
      if (!visible(p)) return;
      var lang = (p.closest('[lang]') || d).getAttribute('lang') || 'en';
      var nf = fmt[lang] || (fmt[lang] = (function () { try { return new Intl.NumberFormat(lang); } catch (x) { return new Intl.NumberFormat('en'); } })());
      var rates = p.dataset.rates.split(',');
      [].forEach.call(p.querySelectorAll('b[data-i]'), function (b) { b.textContent = nf.format(Math.floor(sec * +rates[b.dataset.i])); });
    });
  }
  births(); setInterval(births, 250);

  // ---- 4. console
  try {
    var dc = document.querySelector('.foot[data-discord]');
    console.log('%c∅ PRO EXTINCTION%c\nYou looked deeper than most. No more victims, no more suffering.\nJoin us: ' + (dc ? dc.dataset.discord : 'proextinction.com'),
      'font:700 22px/1.4 sans-serif;letter-spacing:.06em;color:#c4161c', 'font:14px/1.6 sans-serif');
  } catch (x) {}
})();
