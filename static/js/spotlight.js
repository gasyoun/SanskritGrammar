/*
 * Spotlight (E1, MG 02-10-2026) — клиент-фолбэк для #:~:text= фрагментов.
 *
 * Сайт — docusaurus SPA: при переходе по внутренней ссылке клиент-роутер меняет
 * маршрут без полной загрузки документа, и браузер НЕ выполняет нативный
 * text-fragment (он работает только при полной загрузке — прямое открытие или
 * новая вкладка). Этот скрипт декодирует #:~:text=<фраза> на любой навигации,
 * находит фразу в тексте, оборачивает её в <mark class="sg-spotlight"> и
 * скроллит к ней. Нативная подсветка браузера остаётся для жёстких загрузок.
 */
(function () {
  'use strict';

  var MARK_CLASS = 'sg-spotlight';
  var STYLE_ID = 'sg-spotlight-style';

  function ensureStyle() {
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent =
      'mark.' + MARK_CLASS + '{background:#fff3ad;color:inherit;padding:0 .1em;border-radius:2px;}' +
      /* Нативная подсветка text-фрагмента при прямом открытии URL: Chrome красит
       * её сиреневым (::target-text) — перекрашиваем в наш янтарный, чтобы обе
       * механики (SPA-клик и прямая загрузка) выглядели одинаково (МГ, 02-10). */
      '::target-text{background-color:#fff3ad;color:inherit;}';
    document.head.appendChild(style);
  }

  function clearMarks() {
    document.querySelectorAll('mark.' + MARK_CLASS).forEach(function (mark) {
      var parent = mark.parentNode;
      while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
      parent.removeChild(mark);
      parent.normalize();
    });
  }

  /* Фраза ищется внутри одного текстового узла (наши spot-фразы — в пределах
   * строки); составные через ',': первая часть обязательна. */
  function phraseCandidates(fragment) {
    return fragment.split(',').map(function (s) {
      return s.replace(/&[a-z]+;|\d+%2C/g, '').trim();
    });
  }

  function findRange(phrases) {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
    var node;
    while ((node = walker.nextNode())) {
      var text = node.nodeValue;
      for (var i = 0; i < phrases.length; i++) {
        var idx = text.indexOf(phrases[i]);
        if (idx !== -1 && phrases[i].length > 3) {
          return { node: node, start: idx, end: idx + phrases[i].length };
        }
      }
    }
    return null;
  }

  function highlight(range) {
    var target = range.node.splitText(range.start);
    target.splitText(range.end - range.start);
    var mark = document.createElement('mark');
    mark.className = MARK_CLASS;
    mark.appendChild(target.cloneNode(false));
    target.parentNode.replaceChild(mark, target);
    mark.scrollIntoView({ block: 'center' });
  }

  var lastHref = null;

  function tick() {
    if (location.href === lastHref) return;
    lastHref = location.href;
    ensureStyle(); // безусловно: при прямой загрузке Chrome вырезает :~:text из
    // location после нативной обработки — правило ::target-text должно стоять
    var m = location.hash.match(/^#:~:text=(.+)/);
    if (!m) return;
    clearMarks();
    var phrases = phraseCandidates(m[1]);
    try {
      phrases = phrases.map(function (p) { return decodeURIComponent(p); });
    } catch (e) { /* уже декодировано */ }
    var tries = 0;
    (function attempt() {
      var range = findRange(phrases);
      if (range) {
        highlight(range);
      } else if (++tries < 25) {
        setTimeout(attempt, 400); // ждём hydration / ленивые блоки
      }
    })();
  }

  setInterval(tick, 350);
  if (document.readyState !== 'loading') tick();
  else document.addEventListener('DOMContentLoaded', tick);
})();
