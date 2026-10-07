/* Full FAQ: filter the questions while typing. Matches question and answer text, ignores case and accents,
   every word must appear. Numbers stay as they are (counter-set in the markup). */
(function () {
  var ask = document.currentScript.previousElementSibling, none = ask.previousElementSibling, faq = none.previousElementSibling,
      box = faq.previousElementSibling, input = box.querySelector('input'), count = box.querySelector('.faq-count'),
      items = [].slice.call(faq.querySelectorAll('details'));
  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }
  var text = items.map(function (d) { return norm(d.textContent); });
  function run() {
    var words = norm(input.value).split(/\s+/).filter(Boolean), n = 0;
    items.forEach(function (d, i) {
      var hit = words.every(function (w) { return text[i].indexOf(w) > -1; });
      d.hidden = !hit; if (hit) n++;
    });
    none.hidden = n > 0;
    count.textContent = words.length ? box.dataset.count.replace('{n}', n).replace('{t}', items.length) : '';
  }
  input.addEventListener('input', run);
  input.addEventListener('keydown', function (e) { if (e.key === 'Escape') { input.value = ''; run(); } });
})();
