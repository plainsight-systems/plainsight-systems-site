/* Plainsight Systems — mobile navigation toggle.
 *
 * Progressive enhancement: without JS, the nav is always visible (CSS default).
 * With JS, the nav collapses on mobile behind a Menu/Close button.
 * The `js` class on <html> lets CSS target the JS-enabled state explicitly,
 * preventing flash-of-visible-menu before JS runs.
 */

(function () {
  'use strict';

  document.documentElement.classList.add('js');

  var toggle = document.querySelector('.ps-nav__toggle');
  var list = document.querySelector('.ps-nav__links');
  if (!toggle || !list) return;

  function setExpanded(expanded) {
    toggle.setAttribute('aria-expanded', String(expanded));
    toggle.textContent = expanded ? 'Close' : 'Menu';
  }

  toggle.addEventListener('click', function () {
    var expanded = toggle.getAttribute('aria-expanded') === 'true';
    setExpanded(!expanded);
  });

  // Close menu when a link is selected (improves mobile UX after navigation).
  Array.prototype.forEach.call(list.querySelectorAll('a'), function (link) {
    link.addEventListener('click', function () {
      if (toggle.getAttribute('aria-expanded') === 'true') {
        setExpanded(false);
      }
    });
  });

  // Close menu on Escape; return focus to the toggle.
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setExpanded(false);
      toggle.focus();
    }
  });
})();
