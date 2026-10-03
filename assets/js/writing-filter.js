// Filter bar for the write-ups list on the Research page
// (layouts/partials/writing/list.html). Progressive enhancement: the bar is
// hidden in the markup and revealed here; without JavaScript the full list
// shows. One chip (kind or topic) and the text box combine with AND.
(function () {
  "use strict";

  function setup(root) {
    var controls = root.querySelector(".ps-writing-controls");
    var input = root.querySelector(".ps-writing-search");
    var chips = Array.prototype.slice.call(root.querySelectorAll(".ps-writing-chip"));
    var items = Array.prototype.slice.call(root.querySelectorAll(".ps-writing__item"));
    var groups = Array.prototype.slice.call(root.querySelectorAll(".ps-writing__group"));
    var count = root.querySelector(".ps-writing-count");
    var empty = root.querySelector(".ps-writing-empty");
    var active = "";

    function matches(li, query) {
      if (active) {
        var sep = active.indexOf(":");
        var key = active.slice(0, sep);
        var value = active.slice(sep + 1);
        if (li.getAttribute("data-" + key) !== value) return false;
      }
      return !query || li.getAttribute("data-text").indexOf(query) !== -1;
    }

    function apply() {
      var query = input.value.trim().toLowerCase();
      var shown = 0;
      items.forEach(function (li) {
        var ok = matches(li, query);
        li.hidden = !ok;
        if (ok) shown += 1;
      });
      groups.forEach(function (group) {
        group.hidden = !group.querySelector(".ps-writing__item:not([hidden])");
      });
      empty.hidden = shown !== 0;
      count.textContent = shown === items.length
        ? items.length + (items.length === 1 ? " write-up" : " write-ups")
        : shown + " of " + items.length + " write-ups";
    }

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        active = chip.getAttribute("data-filter");
        chips.forEach(function (c) {
          c.setAttribute("aria-pressed", c === chip ? "true" : "false");
        });
        apply();
      });
    });
    input.addEventListener("input", apply);

    controls.hidden = false;
    apply();
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-writing-filter]"), setup);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
