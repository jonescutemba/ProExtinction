/* Single-page presentation: concept switcher, light/dark, EN/DE, hash router, and the per-view behaviours. */
(function () {
  var d = document.documentElement;
  var CONCEPTS = { 'a-ember': { n: 'Ember', mode: 'dark' }, 'b-poster': { n: 'Poster', mode: 'dark' }, 'c-ring': { n: 'Ring', mode: 'light' } };
  var SHORT = { a: 'a-ember', b: 'b-poster', c: 'c-ring' };
  function qs(k) { try { return new URLSearchParams(location.search).get(k); } catch (e) { return null; } }
  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {}
    return null;
  }
  // ---- motion override (OS "reduce motion" switches effects off; ?motion=on forces them for testing)
  var mp = qs('motion');
  if (mp === 'on') store('pe-motion', 'on'); if (mp === 'off') store('pe-motion', null);
  if (store('pe-motion') === 'on') d.dataset.motion = 'on';
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches && d.dataset.motion !== 'on';

  // ---- concept + theme
  var styles = [].slice.call(document.querySelectorAll('style[data-concept]'));
  var btns = [].slice.call(document.querySelectorAll('.concepts button'));
  var userTheme = null;
  var tq = qs('theme'); if (tq === 'light' || tq === 'dark') userTheme = tq;
  else { var ts = store('pe-theme'); if (ts === 'light' || ts === 'dark') userTheme = ts; }
  function setTheme(m) { d.dataset.theme = m; }
  function applyConcept(c, save) {
    if (!CONCEPTS[c]) c = 'a-ember';
    d.dataset.concept = c; d.dataset.default = CONCEPTS[c].mode;
    styles.forEach(function (s) { s.media = s.dataset.concept === c ? 'all' : 'not all'; });
    btns.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.concept === c ? 'true' : 'false'); });
    setTheme(userTheme || CONCEPTS[c].mode);
    if (save) store('pe-concept', c);
    updateTitle(); setTimeout(railMore, 60); setTimeout(bindToc, 60);
  }
  var cq = qs('concept'); var concept = SHORT[cq] || (CONCEPTS[cq] && cq) || store('pe-concept') || 'a-ember';
  btns.forEach(function (b) { b.addEventListener('click', function () { applyConcept(b.dataset.concept, true); }); });
  var themeBtn = document.querySelector('.theme');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    userTheme = d.dataset.theme === 'dark' ? 'light' : 'dark'; setTheme(userTheme); store('pe-theme', userTheme);
  });

  // ---- router
  var views = {}; [].forEach.call(document.querySelectorAll('.view'), function (v) { views[v.dataset.view] = v; });
  var navs = [].slice.call(document.querySelectorAll('.sitenav'));
  var langLink = document.querySelector('.lang'), brand = document.querySelector('.brand');
  var langBlocks = [].slice.call(document.querySelectorAll('[data-lang]'));
  var PAIR = JSON.parse(document.getElementById('pair-map').textContent);
  var current = null, curKey = '';
  function parse() { var m = /^#\/(en|de)\/([\w-]+)/.exec(location.hash); return m ? { lang: m[1], slug: m[2] } : null; }
  function updateTitle() {
    var v = views[curKey]; document.title = (v ? v.dataset.title + ' – ' : '') + 'Pro Extinction · ' + (CONCEPTS[d.dataset.concept] || {}).n;
  }
  function show() {
    var r = parse();
    if (!r) { if (current) return; r = { lang: store('pe-lang') === 'de' ? 'de' : 'en', slug: 'home' }; }
    var key = r.lang + '/' + r.slug;
    if (!views[key]) { r = { lang: r.lang, slug: 'home' }; key = r.lang + '/home'; history.replaceState(null, '', '#/' + key); }
    var changed = key !== curKey;
    Object.keys(views).forEach(function (k) { views[k].hidden = k !== key; });
    current = r; curKey = key; d.lang = r.lang; store('pe-lang', r.lang);
    navs.forEach(function (n) {
      n.hidden = n.dataset.lang !== r.lang;
      [].forEach.call(n.querySelectorAll('a'), function (a) { if (a.dataset.slug === r.slug) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
    });
    langBlocks.forEach(function (b) { if (b.dataset.lang && !b.classList.contains('sitenav')) b.hidden = b.dataset.lang !== r.lang; });
    var other = r.lang === 'en' ? 'de' : 'en';
    var otherSlug = r.lang === 'en' ? (PAIR.en2de[r.slug] || 'home') : (PAIR.de2en[r.slug] || 'home');
    if (!views[other + '/' + otherSlug]) otherSlug = 'home';
    langLink.href = '#/' + other + '/' + otherSlug; langLink.textContent = other.toUpperCase(); langLink.lang = other; langLink.hreflang = other;
    langLink.setAttribute('aria-label', (r.lang === 'en' ? 'Language' : 'Sprache') + ': ' + other.toUpperCase());
    brand.href = '#/' + r.lang + '/home';
    var mb = document.querySelector('.menu-toggle');
    if (mb) { mb.setAttribute('aria-controls', 'nav-' + r.lang); mb.querySelector('.menu-t').textContent = r.lang === 'de' ? 'Menü' : 'Menu'; }
    updateTitle();
    if (changed) { d.style.scrollBehavior = 'auto'; window.scrollTo(0, 0); d.style.scrollBehavior = ''; }
    bindToc(); railMore(); bindLogos();
  }
  window.addEventListener('hashchange', show);


  // ---- expandable menu below 1000px
  var topBar = document.querySelector('.top'), menuBtn = document.querySelector('.menu-toggle');
  function setTopH() { if (topBar) d.style.setProperty('--top-h', Math.max(0, topBar.getBoundingClientRect().bottom) + 'px'); }
  function closeNav() { d.classList.remove('nav-open'); if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false'); }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      var open = !d.classList.contains('nav-open'); setTopH();
      d.classList.toggle('nav-open', open); menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && d.classList.contains('nav-open')) { closeNav(); menuBtn.focus(); } });
    document.addEventListener('click', function (e) {
      if (!d.classList.contains('nav-open')) return;
      if (e.target.closest('.sitenav a')) { closeNav(); return; }
      if (!e.target.closest('.sitenav') && !e.target.closest('.menu-toggle')) closeNav();
    });
    window.addEventListener('resize', function () { if (window.innerWidth >= 1000) closeNav(); else setTopH(); });
    window.addEventListener('scroll', function () { if (d.classList.contains('nav-open')) setTopH(); }, { passive: true });
  }
  // ---- progress bar
  var bar = document.querySelector('.progress i');
  function onScroll() { if (!bar) return; var h = d.scrollHeight - d.clientHeight; bar.style.width = (h > 0 ? Math.min(100, (d.scrollTop / h) * 100) : 0) + '%'; }
  window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll);

  // ---- chapter overview: highlight the chapter being read
  var io = null;
  function bindToc() {
    if (io) io.disconnect();
    var v = views[curKey]; if (!v || !('IntersectionObserver' in window)) return;
    var links = [].slice.call(v.querySelectorAll('.toc a')); if (!links.length) return;
    var map = {}; links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { links.forEach(function (a) { a.removeAttribute('aria-current'); }); var a = map[e.target.id]; if (a) a.setAttribute('aria-current', 'true'); } });
    }, { rootMargin: '-15% 0px -75% 0px' });
    [].forEach.call(v.querySelectorAll('.prose h2'), function (h) { io.observe(h); });
  }

  // ---- rail fade when the list is taller than the window
  function railMore() {
    var rail = navs.filter(function (n) { return !n.hidden; })[0]; if (!rail) return;
    var list = rail.querySelector('ul');
    navs.forEach(function (n) { n.removeAttribute('data-more'); var u = n.querySelector('ul'); if (u) u.removeAttribute('data-more'); });
    [rail, list].forEach(function (el) {
      if (!el) return;
      var scrolls = el.scrollHeight - el.clientHeight > 6 && getComputedStyle(el).overflowY !== 'visible';
      if (scrolls && el.scrollHeight - el.clientHeight - el.scrollTop > 6) el.setAttribute('data-more', '');
    });
  }
  navs.forEach(function (n) { [n, n.querySelector('ul')].forEach(function (el) { if (el) el.addEventListener('scroll', railMore, { passive: true }); }); });
  window.addEventListener('resize', railMore);

  // ---- logo effect: 1st hover and every 10th; max 1.5x, 4 s; ?scare=reset starts over
  var hovers = 0;
  try { if (qs('scare') === 'reset') store('pe-hovers', null); hovers = parseInt(store('pe-hovers'), 10) || 0; } catch (e) {}
  var armed = true, activeLogo = null;
  function scare(e) {
    var logo = e.currentTarget; if (reduce || !armed) return;
    armed = false; hovers++; store('pe-hovers', String(hovers));
    var isClick = e.type === 'click';
    if (hovers !== 1 && hovers % 10 !== 0) { if (isClick) armed = true; return; }
    activeLogo = logo; logo.classList.add('scare'); d.classList.add('scaring');
    setTimeout(function () { logo.classList.remove('scare'); d.classList.remove('scaring'); activeLogo = null; if (isClick) armed = true; }, 4000);
  }
  var logosBound = false;
  function bindLogos() {
    if (logosBound) return; logosBound = true;
    [].forEach.call(document.querySelectorAll('.hero-logo'), function (l) { l.addEventListener('mouseenter', scare); l.addEventListener('click', scare); });
    document.addEventListener('mousemove', function (e) {
      if (!armed && !activeLogo && !(e.target.closest && e.target.closest('.hero-logo'))) armed = true;
    }, { passive: true });
  }

  applyConcept(concept, false);
  show(); onScroll();
})();
