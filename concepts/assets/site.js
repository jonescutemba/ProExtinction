(function () {
  var d = document.documentElement;
  var btn = document.querySelector('.theme');
  if (btn) btn.addEventListener('click', function () {
    var next = d.dataset.theme === 'dark' ? 'light' : 'dark';
    d.dataset.theme = next;
    try { localStorage.setItem('pe-theme', next); } catch (e) {}
  });
  // The OS setting "reduce motion" switches the logo effect off. For testing it can be overridden: add ?motion=on (or ?motion=off to undo).
  try {
    var mp = new URLSearchParams(location.search).get('motion');
    if (mp === 'on') localStorage.setItem('pe-motion', 'on');
    if (mp === 'off') localStorage.removeItem('pe-motion');
    if (localStorage.getItem('pe-motion') === 'on') d.dataset.motion = 'on';
  } catch (e) {}
  var logo = document.querySelector('.hero-logo');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches && d.dataset.motion !== 'on';
  var armed = true;
  function scare(e) {
    if (!logo || reduce || !armed) return;
    armed = false;
    logo.classList.add('scare'); d.classList.add('scaring');
    setTimeout(function () {
      logo.classList.remove('scare'); d.classList.remove('scaring');
      if (e && e.type === 'click') armed = true; // touch has no mouseleave
    }, 4000);
  }
  if (logo) {
    logo.addEventListener('mouseenter', scare);
    logo.addEventListener('click', scare);
    // re-arm only after the pointer has left, so resting on the logo does not loop the effect
    logo.addEventListener('mouseleave', function () { if (!logo.classList.contains('scare')) armed = true; });
    document.addEventListener('mousemove', function (e) {
      if (!armed && !logo.classList.contains('scare') && !logo.contains(e.target)) armed = true;
    }, { passive: true });
  }
  var bar = document.querySelector('.progress i');
  function onScroll() {
    if (!bar) return;
    var h = d.scrollHeight - d.clientHeight;
    bar.style.width = (h > 0 ? Math.min(100, (d.scrollTop / h) * 100) : 0) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  var links = [].slice.call(document.querySelectorAll('.toc a'));
  if (links.length && 'IntersectionObserver' in window) {
    var map = {};
    links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) {
          links.forEach(function (a) { a.removeAttribute('aria-current'); });
          var a = map[e.target.id]; if (a) a.setAttribute('aria-current', 'true');
        }
      });
    }, { rootMargin: '-15% 0px -75% 0px' });
    [].slice.call(document.querySelectorAll('.prose h2')).forEach(function (h) { io.observe(h); });
  }
  var rail = document.querySelector('.sitenav');
  var railList = rail && rail.querySelector('ul');
  // the scrolling element is the rail itself (A) or just its list inside a bordered card (C); fade only that one
  function railMore() {
    [rail, railList].forEach(function (el) {
      if (!el) return;
      var scrolls = el.scrollHeight - el.clientHeight > 6 && getComputedStyle(el).overflowY !== 'visible';
      var more = scrolls && el.scrollHeight - el.clientHeight - el.scrollTop > 6;
      if (more) el.setAttribute('data-more', ''); else el.removeAttribute('data-more');
    });
  }
  if (rail) {
    [rail, railList].forEach(function (el) { el.addEventListener('scroll', railMore, { passive: true }); });
    window.addEventListener('resize', railMore); railMore();
  }
  var cur = document.querySelector('.sitenav [aria-current=page]');
  if (cur && cur.scrollIntoView && getComputedStyle(cur.parentNode.parentNode).overflowX === 'auto') {
    cur.parentNode.parentNode.scrollLeft = cur.offsetLeft - 16;
  }
})();
