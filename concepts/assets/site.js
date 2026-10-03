(function () {
  var d = document.documentElement;
  var btn = document.querySelector('.theme');
  if (btn) btn.addEventListener('click', function () {
    var next = d.dataset.theme === 'dark' ? 'light' : 'dark';
    d.dataset.theme = next;
    try { localStorage.setItem('pe-theme', next); } catch (e) {}
  });
  var bar = document.querySelector('.progress i');
  function onScroll() {
    if (!bar) return;
    var h = d.scrollHeight - d.clientHeight;
    bar.style.width = (h > 0 ? Math.min(100, (d.scrollTop / h) * 100) : 0) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  var menu = document.querySelector('.menu');
  document.addEventListener('click', function (e) { if (menu && menu.open && !menu.contains(e.target)) menu.open = false; });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu) menu.open = false; });
})();
