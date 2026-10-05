(function () {
  var Q = window.QUIZ, KEY = "recall-quiz:" + Q.id;
  var DAY = 86400000, INTERVALS = [0, 1, 3, 7, 21]; // Leitner boxes 0..4, days until next review
  var $ = function (id) { return document.getElementById(id); };

  // ---- storage (falls back to memory if the browser blocks it) ----
  var memory = null, persistent = true;
  function load() {
    try { var s = localStorage.getItem(KEY); if (s) return JSON.parse(s); }
    catch (e) { persistent = false; }
    return memory || { items: {} };
  }
  function save() {
    memory = state;
    try { localStorage.setItem(KEY, JSON.stringify(state)); persistent = true; }
    catch (e) { persistent = false; }
    $("storeNote").textContent = persistent ? "" : "This browser is blocking storage, so progress will be lost when you close the tab. Use Download my progress.";
  }
  var state = load();
  if (!state.items) state.items = {};

  // ---- helpers ----
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function rec(id, result) {
    var it = state.items[id] || { box: 0, seen: 0, missed: 0, due: 0 };
    if (result === "miss") { it.box = 0; it.missed++; it.due = Date.now(); }
    else {
      if (result === "got") it.box = Math.min(it.box + 1, INTERVALS.length - 1);
      it.due = Date.now() + INTERVALS[it.box] * DAY;
    }
    it.seen++; it.last = Date.now();
    state.items[id] = it; save();
  }

  // ---- setup ----
  var units = [];
  Q.questions.forEach(function (q) { if (units.indexOf(q.unit) < 0) units.push(q.unit); });
  $("title").textContent = Q.book;
  $("sub").textContent = Q.questions.length + " questions · recall first, then check";
  var scope = $("scope");
  scope.appendChild(new Option("Whole book", "all"));
  units.forEach(function (u) {
    var t = Q.questions.filter(function (q) { return q.unit === u; })[0].unitTitle;
    scope.appendChild(new Option(u + (t ? " — " + t : ""), u));
  });

  function pool() {
    var s = scope.value, m = $("mode").value, now = Date.now();
    var list = Q.questions.filter(function (q) { return s === "all" || q.unit === s; });
    if (m === "due") list = list.filter(function (q) { var it = state.items[q.id]; return !it || it.due <= now; });
    if (m === "weak") list = list.filter(function (q) { var it = state.items[q.id]; return it && (it.box <= 1 && it.missed > 0); });
    list = shuffle(list);
    var n = parseInt($("count").value, 10);
    return n ? list.slice(0, n) : list;
  }

  // ---- session ----
  var queue = [], pos = 0, score = { got: 0, part: 0, miss: 0 };
  $("start").onclick = function () {
    queue = pool(); pos = 0; score = { got: 0, part: 0, miss: 0 };
    if (!queue.length) { show(el("p", null, "Nothing to practise with these settings. Try “Everything” or a different scope.")); return; }
    next();
  };
  function show() {
    var p = $("play"); p.classList.remove("hide"); p.textContent = "";
    for (var i = 0; i < arguments.length; i++) p.appendChild(arguments[i]);
    p.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  function next() {
    if (pos >= queue.length) return finish();
    var q = queue[pos];
    var frag = [];
    frag.push(el("div", "meta", (pos + 1) + " of " + queue.length + " · " + q.unit + " › " + q.section));
    frag.push(el("div", "q", q.q));
    if (q.kind === "mcq") {
      var box = el("div"), done = false;
      var fb = el("div");
      q.options.forEach(function (o, i) {
        var b = el("button", "opt", o);
        b.onclick = function () {
          if (done) return; done = true;
          var ok = i === q.answer;
          b.classList.add(ok ? "right" : "wrong");
          if (!ok) box.children[q.answer].classList.add("right");
          score[ok ? "got" : "miss"]++; rec(q.id, ok ? "got" : "miss");
          fb.appendChild(el("div", "reveal", (ok ? "Correct. " : "Not quite. ") + q.explain));
          var n = el("button", "primary", pos + 1 < queue.length ? "Next" : "Finish");
          n.onclick = function () { pos++; next(); };
          fb.appendChild(n);
        };
        box.appendChild(b);
      });
      frag.push(box); frag.push(fb);
    } else {
      var area = el("div");
      var r = el("button", "primary", "Show answer");
      r.onclick = function () {
        area.textContent = "";
        area.appendChild(el("div", "reveal", q.a));
        area.appendChild(el("p", "note", "How well did you recall it before looking?"));
        var rate = el("div", "rate");
        [["miss", "Missed"], ["part", "Partly"], ["got", "Got it"]].forEach(function (x) {
          var b = el("button", x[0], x[1]);
          b.onclick = function () { score[x[0]]++; rec(q.id, x[0]); pos++; next(); };
          rate.appendChild(b);
        });
        area.appendChild(rate);
      };
      area.appendChild(el("p", "note", "Try to recall it first, out loud or in your head."));
      area.appendChild(r);
      frag.push(area);
    }
    show.apply(null, frag);
    renderStats();
  }
  function finish() {
    var t = score.got + score.part + score.miss;
    var again = el("button", "primary", "Practise again");
    again.onclick = function () { $("start").click(); };
    show(el("div", "q", "Session done: " + score.got + " got it, " + score.part + " partly, " + score.miss + " missed (of " + t + ")."),
         el("p", "note", "Missed items come back in the next session; items you get right return after longer gaps."), again);
    renderStats();
  }

  // ---- stats / gaps ----
  function renderStats() {
    var s = $("stats"); s.textContent = "";
    s.appendChild(el("div", "meta", "Progress by chapter"));
    var tb = el("table"), hd = el("tr");
    ["Unit", "Seen", "Solid", "Missed", ""].forEach(function (h) { hd.appendChild(el("th", null, h)); });
    tb.appendChild(hd);
    var totalSolid = 0;
    units.forEach(function (u) {
      var qs = Q.questions.filter(function (q) { return q.unit === u; });
      var seen = 0, solid = 0, missed = 0;
      qs.forEach(function (q) { var it = state.items[q.id]; if (it) { seen++; if (it.box >= 3) solid++; missed += it.missed; } });
      totalSolid += solid;
      var tr = el("tr");
      tr.appendChild(el("td", null, u));
      tr.appendChild(el("td", null, seen + "/" + qs.length));
      tr.appendChild(el("td", null, String(solid)));
      tr.appendChild(el("td", null, String(missed)));
      var c = el("td"), bar = el("div", "bar"), i = el("i");
      i.style.width = (qs.length ? Math.round(100 * solid / qs.length) : 0) + "%";
      bar.appendChild(i); c.appendChild(bar); tr.appendChild(c);
      tb.appendChild(tr);
    });
    s.appendChild(tb);
    s.appendChild(el("p", "note", "Solid = answered right several times with growing gaps. " + totalSolid + " of " + Q.questions.length + " solid."));
  }

  // ---- backup / restore ----
  $("export").onclick = function () {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(state)], { type: "application/json" }));
    a.download = Q.id + "-progress.json"; a.click();
  };
  $("importBtn").onclick = function () { $("importFile").click(); };
  $("importFile").onchange = function (e) {
    var f = e.target.files[0]; if (!f) return;
    var r = new FileReader();
    r.onload = function () {
      try { var d = JSON.parse(r.result); if (!d.items) throw 0; state = d; save(); renderStats(); alert("Progress loaded."); }
      catch (x) { alert("That file doesn’t look like a progress backup."); }
    };
    r.readAsText(f);
  };
  $("reset").onclick = function () {
    if (confirm("Erase all progress in this browser?")) { state = { items: {} }; save(); renderStats(); }
  };

  save(); renderStats();
})();
