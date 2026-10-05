/* theme.js: light/dark/system mode and the theme picker.
   Loaded in <head> so the saved theme is applied before the page paints (no flash).
   The list of themes comes from themes-list.js, which tools/gen_themes.py generates. */
(function () {
  "use strict";
  var STORE = "recall-quiz:theme";            // one setting for every book on this site
  var root = document.documentElement;
  var themes = window.QUIZ_THEMES || [["classic", "Classic"]];
  var state = { t: "classic", m: "system" };  // t = theme id, m = light | dark | system

  try { var saved = JSON.parse(localStorage.getItem(STORE) || "{}"); if (saved.t) state.t = saved.t; if (saved.m) state.m = saved.m; } catch (e) {}
  if (!themes.some(function (t) { return t[0] === state.t; })) state.t = "classic";

  var darkQuery = window.matchMedia ? matchMedia("(prefers-color-scheme: dark)") : null;
  function isDark() { return state.m === "dark" || (state.m === "system" && darkQuery && darkQuery.matches); }

  function apply() {
    root.setAttribute("data-theme", state.t);
    root.setAttribute("data-mode", state.m);
    root.setAttribute("data-scheme", isDark() ? "dark" : "light");
    try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) {}
    each("#modeSegT button", function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-m") === state.m)); });
    each("#tiles .tile", function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-t") === state.t)); });
  }
  function each(sel, fn) { Array.prototype.forEach.call(document.querySelectorAll(sel), fn); }
  function make(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text) e.textContent = text; return e; }

  function buildPicker() {
    var tiles = document.getElementById("tiles"), panel = document.getElementById("themePanel"), btn = document.getElementById("themeBtn");
    if (!tiles || !btn) return;
    themes.forEach(function (t) {
      var b = make("button", "tile"); b.type = "button"; b.setAttribute("data-t", t[0]);
      b.appendChild(make("div", "tmas"));
      var sw = make("div", "tsw"); sw.appendChild(make("i")); sw.appendChild(make("i")); sw.appendChild(make("i")); b.appendChild(sw);
      b.appendChild(make("div", "tbtn", "Go")); b.appendChild(make("div", "tnm", t[1]));
      b.addEventListener("click", function () { state.t = t[0]; apply(); });
      tiles.appendChild(b);
    });
    each("#modeSegT button", function (b) { b.addEventListener("click", function () { state.m = b.getAttribute("data-m"); apply(); }); });
    btn.addEventListener("click", function () {
      var open = panel.classList.toggle("hide") === false;
      btn.setAttribute("aria-expanded", String(open));
    });
    if (darkQuery) { var f = function () { if (state.m === "system") apply(); }; darkQuery.addEventListener ? darkQuery.addEventListener("change", f) : darkQuery.addListener(f); }
    apply();
  }

  apply();                                    // before first paint
  document.addEventListener("DOMContentLoaded", buildPicker);
})();
