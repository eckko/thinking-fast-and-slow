(function () {
  var Q, KEY;
  var sessionCM = 0, locked = false, curConf = null, confOn = false;
  var DAY = 86400000, STEPS = [0, 1, 3, 7, 21]; // memory levels 0..4: days until the next review
  var $ = function (id) { return document.getElementById(id); };

  /* ---------- storage (falls back to memory if the browser blocks it) ---------- */
  var memory = null, persistent = true;
  function load() {
    try { var s = localStorage.getItem(KEY); if (s) return JSON.parse(s); } catch (e) { persistent = false; }
    return memory || { items: {}, days: [], history: [] };
  }
  var state = { items: {}, days: [], history: [] };
  function normalise() { if (!state.items) state.items = {}; if (!state.days) state.days = []; if (!state.history) state.history = []; }
  function save() {
    memory = state;
    try { localStorage.setItem(KEY, JSON.stringify(state)); persistent = true; } catch (e) { persistent = false; }
    $("storeNote").textContent = persistent ? "" : "This browser is blocking storage, so progress will be lost when you close the tab. Use Download to keep a copy.";
  }

  /* ---------- helpers ---------- */
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function dayKey(d) { var x = d || new Date(); return x.getFullYear() + "-" + (x.getMonth() + 1) + "-" + x.getDate(); }
  function numOf(u) { return u.replace(/^\D+/, ""); }
  var KIND = { tf: "True or false", multi: "Select all that apply", fill: "Fill in the blank", order: "Put in order", match: "Match the pairs", sort: "Sort into groups" };
  function kindLabel(q) {
    if (KIND[q.kind]) return KIND[q.kind];
    if (q.kind === "recall") return "Recall it from memory";
    if (/place in the argument|how this chapter|part overview/i.test(q.section)) return "Structure: why the book is built this way";
    return "Core idea";
  }
  function rec(q, result) {
    var it = state.items[q.id] || { box: 0, seen: 0, missed: 0, due: 0 };
    if (result === "miss") { it.box = 0; it.missed++; it.due = Date.now(); }
    else { if (result === "got") it.box = Math.min(it.box + 1, STEPS.length - 1); it.due = Date.now() + STEPS[it.box] * DAY; }
    if (confOn && curConf === 3 && result === "miss") { it.cm = (it.cm || 0) + 1; sessionCM++; }
    it.seen++; it.last = Date.now();
    state.items[q.id] = it;
    var k = dayKey(); if (state.days.indexOf(k) < 0) state.days.push(k);
    save();
  }
  function streak() {
    var n = 0, d = new Date();
    if (state.days.indexOf(dayKey(d)) < 0) d = new Date(Date.now() - DAY);
    while (state.days.indexOf(dayKey(d)) >= 0) { n++; d = new Date(d.getTime() - DAY); }
    return n;
  }
  function todayCount() {
    var t = new Date(); t.setHours(0, 0, 0, 0); var n = 0;
    Object.keys(state.items).forEach(function (k) { if (state.items[k].last >= t.getTime()) n++; });
    return n;
  }

  /* ---------- structure ---------- */
  var units = [], titles = {}, scope = $("scope");
  function boot(data) {
    if (!data || !data.questions || !data.questions.length) throw new Error("no questions");
    Q = data; KEY = "recall-quiz:" + (Q.id || "book");
    state = load(); normalise();
    units = []; titles = {};
    Q.questions.forEach(function (q) { if (units.indexOf(q.unit) < 0) { units.push(q.unit); titles[q.unit] = q.unitTitle || ""; } });
    $("title").textContent = Q.book;
    $("sub").textContent = Q.questions.length + " questions across " + units.length + (units.length === 1 ? " chapter" : " chapters") + ". Recall first, then check.";
    scope.textContent = "";
    scope.appendChild(new Option("Whole book", "all"));
    units.forEach(function (u) { scope.appendChild(new Option(u + (titles[u] ? ": " + titles[u] : ""), u)); });
    $("loadErr").classList.add("hide"); $("homeWrap").classList.remove("hide"); $("stats").classList.remove("hide");
    save(); renderHome();
  }
  function showLoadError() {
    $("homeWrap").classList.add("hide"); $("stats").classList.add("hide"); $("loadErr").classList.remove("hide");
  }
  function loadQuestions() {
    fetch("questions.json", { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error(String(r.status)); return r.json(); })
      .then(boot).catch(showLoadError);
  }
  $("qfile").addEventListener("change", function (e) {
    var f = e.target.files[0]; if (!f) return; var r = new FileReader();
    r.onload = function () { try { boot(JSON.parse(r.result)); } catch (x) { alert("That file is not a valid questions.json."); } };
    r.readAsText(f);
  });

  var mode = "due", limit = 0, lenType = "q";
  function seg(id, set) {
    $(id).addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      Array.prototype.forEach.call($(id).children, function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      set(b.getAttribute("data-v")); renderAvail();
    });
  }
  seg("modeSeg", function (v) { mode = v; });
  seg("lenSeg", function (v) {
    lenType = v; $("lenQ").classList.toggle("hide", v !== "q"); $("lenT").classList.toggle("hide", v !== "t");
  });
  document.querySelectorAll("[data-fill]").forEach(function (b) {
    b.addEventListener("click", function () {
      var box = $(b.getAttribute("data-to")); box.value = b.getAttribute("data-fill"); renderAvail();
    });
  });
  ["nQ", "nT"].forEach(function (id) { $(id).addEventListener("input", renderAvail); });
  seg("timerSeg", function (v) { limit = parseInt(v, 10); });
  seg("confSeg", function (v) { confOn = v === "1"; });
  scope.addEventListener("change", renderAvail);

  function filtered() {
    var s = scope.value, now = Date.now();
    var list = Q.questions.filter(function (q) { return s === "all" || q.unit === s; });
    if (mode === "due") list = list.filter(function (q) { var it = state.items[q.id]; return !it || it.due <= now; });
    if (mode === "weak") list = list.filter(function (q) { var it = state.items[q.id]; return it && it.missed > 0 && it.box <= 1; });
    return list;
  }
  function renderAvail() {
    var n = filtered().length;
    var tmins = Math.max(1, parseInt($("nT").value, 10) || 15);
    if (n && lenType === "t") { $("avail").textContent = n + (n === 1 ? " question is" : " questions are") + " ready. The session ends after " + tmins + (tmins === 1 ? " minute" : " minutes") + " or when you run out of questions."; return; }
    var nq = parseInt($("nQ").value, 10) || 0;
    if (n && nq) { $("avail").textContent = "Up to " + Math.min(nq, n) + " of " + n + " ready questions will be asked."; return; }
    $("avail").textContent = n ? n + (n === 1 ? " question is" : " questions are") + " ready with these settings." :
      (mode === "weak" ? "No gaps yet. Answer a few questions and any you miss will appear here." :
       mode === "due" ? "Nothing is due here right now. Try Everything to practise ahead." : "No questions in this chapter yet.");
  }

  /* ---------- home ---------- */
  function renderHome() {
    var total = Q.questions.length, solid = 0, learning = 0;
    Q.questions.forEach(function (q) { var it = state.items[q.id]; if (!it) return; if (it.box >= 3) solid++; else learning++; });
    var fresh = total - solid - learning, pct = total ? Math.round(100 * solid / total) : 0;
    $("ringFg").style.strokeDashoffset = String(263.9 * (1 - pct / 100));
    $("ringTx").textContent = pct + "%";
    var t = $("tally"); t.textContent = "";
    [["Solid", solid], ["Learning", learning], ["Not seen", fresh]].forEach(function (x) {
      var d = el("div"); d.appendChild(el("b", null, String(x[1]))); d.appendChild(el("span", null, x[0])); t.appendChild(d);
    });
    var due = Q.questions.filter(function (q) { var it = state.items[q.id]; return it && it.due <= Date.now(); }).length;
    $("today").textContent = "Today you answered " + todayCount() + ". " + (due ? due + " to revisit." : "Nothing waiting to revisit.");
    var s = streak(); $("streak").textContent = "";
    var b = el("b", null, s + (s === 1 ? " day" : " days")); $("streak").appendChild(b); $("streak").appendChild(document.createTextNode(" in a row"));
    renderAvail(); renderStats(); renderHistory();
  }

  /* ---------- session ---------- */
  var queue = [], pos = 0, score, missed, ctx = null;
  $("start").addEventListener("click", function () {
    var list = shuffle(filtered());
    if (lenType === "q") { var nq = parseInt($("nQ").value, 10) || 0; if (nq) list = list.slice(0, nq); }
    if (!list.length) { renderAvail(); return; }
    queue = list; pos = 0; score = { got: 0, part: 0, miss: 0 }; missed = []; sessionCM = 0;
    sessionTimed = lenType === "t"; stopTotal(); document.body.classList.add("playing");
    if (sessionTimed) startTotal(Math.max(1, parseInt($("nT").value, 10) || 15));
    $("homeWrap").classList.add("hide"); $("stats").classList.add("hide");
    next();
  });
  var totalId = null, sEnd = 0, sessionMins = 0, sessionOver = false, sessionTimed = false, clock = null, qAnswered = false;
  function stopTotal() { if (totalId) { clearInterval(totalId); totalId = null; } clock = null; $("clockPill").classList.add("hide"); }
  function startTotal(mins) { sessionMins = mins; sEnd = Date.now() + mins * 60000; sessionOver = false; $("clockPill").classList.remove("hide"); totalId = setInterval(tickTotal, 250); }
  function tickTotal() {
    var left = Math.max(0, sEnd - Date.now()), s = Math.ceil(left / 1000);
    var st = (s <= 60 ? " low" : "") + (s <= 15 ? " crit" : "");
    $("clockLab").textContent = "Time left"; $("clockNum").textContent = Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2);
    $("clockPill").className = "clockpill" + st + (totalId ? "" : " hide");
    if (clock) { clock.i.style.width = (100 * left / (sessionMins * 60000)) + "%"; clock.w.className = "clock" + st; }
    if (left <= 0) { stopTotal(); stopTimer(); if (qAnswered) sessionOver = true; else finish(); }
  }
  function clockEl() {
    var w = el("div", "clock"), row = el("div", "crow"), lab = el("span", null, "Question " + (pos + 1));
    var bar = el("div", "tbar"), i = el("i"); bar.appendChild(i);
    row.appendChild(lab); w.appendChild(row); w.appendChild(bar);
    clock = { w: w, i: i }; tickTotal();
    return w;
  }
  var tickId = null, onExpire = null, tEnd = 0;
  function stopTimer() { if (tickId) { clearInterval(tickId); tickId = null; } onExpire = null; }
  function timerEl() {
    var w = el("div", "timer"), bar = el("div", "tbar"), i = el("i"), num = el("div", "tnum");
    bar.appendChild(i); w.appendChild(bar); w.appendChild(num);
    tEnd = Date.now() + limit * 1000;
    function upd() {
      var left = Math.max(0, tEnd - Date.now()), s = Math.ceil(left / 1000);
      i.style.width = (100 * left / (limit * 1000)) + "%"; num.textContent = s + "s";
      w.className = "timer" + (s <= 5 ? " crit" : s <= 10 ? " low" : "");
      if (left <= 0) { var f = onExpire; stopTimer(); if (f) f(); }
    }
    tickId = setInterval(upd, 100); upd();
    return w;
  }
  function panel() { var p = $("play"); p.classList.remove("hide"); p.textContent = ""; window.scrollTo({ top: 0 }); return p; }
  function progressBar() {
    var d = el("div", "prog");
    queue.forEach(function (_, i) { d.appendChild(el("i", i < pos ? "done" : i === pos ? "now" : "")); });
    return d;
  }
  function where(q) {
    var w = el("div", "where"), c = el("div", "chapter");
    c.appendChild(el("span", "chip", "Chapter " + numOf(q.unit)));
    if (q.unitTitle) c.appendChild(el("span", "chtitle", q.unitTitle));
    w.appendChild(c);
    var t = el("div", "topic"); t.appendChild(document.createTextNode("Topic: ")); t.appendChild(el("mark", null, q.section)); w.appendChild(t);
    w.appendChild(el("span", "kind", kindLabel(q)));
    return w;
  }
  function next() {
    if (pos >= queue.length) return finish();
    stopTimer(); qAnswered = false;
    var q = queue[pos], p = panel();
    p.appendChild(sessionTimed ? clockEl() : progressBar()); if (limit) p.appendChild(timerEl()); p.appendChild(where(q)); var qw = el("div", "q-wrap"); qw.appendChild(el("span", "question", q.q)); p.appendChild(qw);
    if (!sessionTimed) { $("clockLab").textContent = "Questions left"; $("clockNum").textContent = (queue.length - pos) + "/" + queue.length; $("clockPill").className = "clockpill"; }
    var area = el("div");
    if (confOn) p.appendChild(confRow(area)); else { curConf = null; locked = false; }
    p.appendChild(area);
    var keys = el("p", "keys"); p.appendChild(keys);
    ctx = null;
    var TYPES = { mcq: mcq, recall: recall, multi: multi, fill: fill, order: order, match: match, sort: sort };
    if (q.kind === "tf") mcq(Object.assign({}, q, { options: ["True", "False"], answer: q.answer ? 0 : 1 }), area, keys);
    else (TYPES[q.kind] || mcq)(q, area, keys);
    var quit = el("button", "btn", "End session"); quit.style.marginTop = "18px"; quit.style.fontWeight = "500";
    quit.addEventListener("click", function () { if (pos > 0 || confirm("Leave this session?")) { ctx = null; goHome(); } });
    p.appendChild(quit);
  }
  function reread(q) {
    var r = el("p", "reread"); r.appendChild(document.createTextNode("To go deeper, reread ")); r.appendChild(el("b", null, "Chapter " + numOf(q.unit) + (q.unitTitle ? ", " + q.unitTitle : "")));
    r.appendChild(document.createTextNode(", topic ")); r.appendChild(el("b", null, q.section)); r.appendChild(document.createTextNode("."));
    return r;
  }
  function burst(node, n) {
    if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var r = node.getBoundingClientRect(), x = r.left + Math.min(r.width / 2, 60), y = r.top + r.height / 2;
    var cols = ["#ff5d73", "#12b5a6", "#7c5cff", "#ff9f1c", "#2743d6", "#ffd400"];
    for (var i = 0; i < (n || 16); i++) {
      var d = el("div", "fx"), a = Math.random() * 6.283, dist = 50 + Math.random() * 70;
      d.style.left = x + "px"; d.style.top = y + "px"; d.style.background = cols[i % cols.length];
      document.body.appendChild(d);
      var an = d.animate([{ transform: "translate(0,0) scale(1)", opacity: 1 }, { transform: "translate(" + Math.cos(a) * dist + "px," + (Math.sin(a) * dist + 20) + "px) scale(.2)", opacity: 0 }], { duration: 650 + Math.random() * 250, easing: "cubic-bezier(.2,.8,.3,1)" });
      an.onfinish = (function (n) { return function () { n.remove(); }; })(d);
    }
  }
  function advance() { if (sessionOver) { finish(); return; } pos++; next(); }
  /* ---------- shared feedback and confidence ---------- */
  var RES = { got: "Correct.", part: "Partly right.", miss: "Not this one." };
  function settle(q, area, keys, result, timedOut, extra) {
    qAnswered = true; stopTimer(); locked = false; area.classList.remove("locked");
    score[result]++; if (result === "miss") missed.push(q);
    rec(q, result);
    var f = el("div", "reveal-in");
    f.appendChild(el("p", "verdict " + (result === "got" ? "ok" : result === "part" ? "mid" : "no"), timedOut ? "Time's up." : RES[result]));
    if (extra) f.appendChild(extra);
    if (q.explain) f.appendChild(el("div", "why", q.explain));
    if (confOn && curConf === 3 && result === "miss") f.appendChild(el("p", "cm", "You were certain, so this is a confident miss. It is worth rereading."));
    f.appendChild(reread(q));
    var a = el("div", "act"), n = el("button", "btn main", pos + 1 < queue.length ? "Next question" : "See results"); n.type = "button";
    n.addEventListener("click", advance); a.appendChild(n); f.appendChild(a); area.appendChild(f); n.focus();
    keys.textContent = "Keys: Enter for next";
    ctx = function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); advance(); } };
    if (result === "got") burst(f, 18);
  }
  function confRow(area) {
    var w = el("div", "confrow"); w.appendChild(el("span", null, "How sure are you?"));
    [[1, "Guessing"], [2, "Fairly sure"], [3, "Certain"]].forEach(function (x) {
      var b = el("button", "mini", x[1]); b.type = "button";
      b.addEventListener("click", function () {
        curConf = x[0]; locked = false; area.classList.remove("locked"); b.blur();
        Array.prototype.forEach.call(w.querySelectorAll("button"), function (y) { y.classList.toggle("on", y === b); });
      });
      w.appendChild(b);
    });
    curConf = null; locked = true; area.classList.add("locked");
    return w;
  }
  function grade3(ok, n) { return ok === n ? "got" : ok >= Math.ceil(n / 2) ? "part" : "miss"; }
  function actBtn(label, cls, fn) { var b = el("button", "btn " + (cls || ""), label); b.type = "button"; b.addEventListener("click", fn); return b; }

  /* ---------- multiple choice (also true or false) ---------- */
  function mcq(q, area, keys) {
    var done = false, btns = [];
    q.options.forEach(function (o, i) {
      var b = el("button", "opt"); b.type = "button";
      b.appendChild(el("span", "k", String(i + 1))); b.appendChild(el("span", null, o));
      b.addEventListener("click", function () { pick(i, false); });
      area.appendChild(b); btns.push(b);
    });
    keys.textContent = "Keys: 1 to " + q.options.length + " to answer";
    function pick(i, timedOut) {
      if (done) return; done = true;
      var ok = i === q.answer;
      btns.forEach(function (b, j) { b.disabled = true; if (j === q.answer) b.classList.add("right"); else if (j === i) b.classList.add("wrong"); else b.classList.add("faded"); });
      settle(q, area, keys, ok ? "got" : "miss", timedOut);
    }
    ctx = function (e) { var n = parseInt(e.key, 10); if (n >= 1 && n <= q.options.length) pick(n - 1, false); };
    onExpire = function () { pick(-1, true); };
  }

  /* ---------- select all that apply ---------- */
  function multi(q, area, keys) {
    var sel = {}, right = {}, btns = [], done = false;
    q.answers.forEach(function (a) { right[a] = true; });
    q.options.forEach(function (o, i) {
      var b = el("button", "opt"); b.type = "button";
      b.appendChild(el("span", "k", String(i + 1))); b.appendChild(el("span", null, o));
      b.addEventListener("click", function () { if (done) return; sel[i] = !sel[i]; b.classList.toggle("picked", !!sel[i]); });
      area.appendChild(b); btns.push(b);
    });
    var act = el("div", "act"); var chk = actBtn("Check my answer", "main", function () { check(false); }); act.appendChild(chk); area.appendChild(act);
    keys.textContent = "Keys: 1 to " + q.options.length + " to tick, Enter to check";
    function check(timedOut) {
      if (done) return; done = true; act.remove();
      var hit = 0, wrong = 0, miss = 0;
      btns.forEach(function (b, i) {
        b.disabled = true; b.classList.remove("picked");
        if (right[i] && sel[i]) { b.classList.add("right"); hit++; }
        else if (right[i]) { b.classList.add("right", "unticked"); b.appendChild(el("em", "tag", "Correct, but you left it out")); miss++; }
        else if (sel[i]) { b.classList.add("wrong"); b.appendChild(el("em", "tag", "Not one of them")); wrong++; }
        else b.classList.add("faded");
      });
      settle(q, area, keys, (!wrong && !miss) ? "got" : (hit && !wrong ? "part" : "miss"), timedOut);
    }
    ctx = function (e) { var n = parseInt(e.key, 10); if (n >= 1 && n <= q.options.length) btns[n - 1].click(); else if (e.key === "Enter") check(false); };
    onExpire = function () { check(true); };
  }

  /* ---------- fill in the blank ---------- */
  function norm(s) { return String(s).toLowerCase().replace(/[^a-z0-9 ]+/g, " ").replace(/\b(the|a|an)\b/g, " ").replace(/\s+/g, " ").trim(); }
  function lev(a, b) {
    var m = [], i, k;
    for (i = 0; i <= a.length; i++) m[i] = [i];
    for (k = 1; k <= b.length; k++) m[0][k] = k;
    for (i = 1; i <= a.length; i++) for (k = 1; k <= b.length; k++) m[i][k] = Math.min(m[i - 1][k] + 1, m[i][k - 1] + 1, m[i - 1][k - 1] + (a[i - 1] === b[k - 1] ? 0 : 1));
    return m[a.length][b.length];
  }
  function fill(q, area, keys) {
    var done = false, inp = el("input", "fillbox"); inp.type = "text"; inp.autocomplete = "off"; inp.autocapitalize = "off"; inp.spellcheck = false; inp.placeholder = "Type the missing word or phrase";
    var act = el("div", "act"); act.appendChild(actBtn("Check", "main", function () { check(false); }));
    area.appendChild(inp); area.appendChild(act); setTimeout(function () { if (!locked) inp.focus(); }, 50);
    keys.textContent = "Keys: Enter to check";
    function ans(note) { var p = el("p", "answerline"); p.appendChild(document.createTextNode("Accepted answer: ")); p.appendChild(el("b", null, q.accept[0] + (note || ""))); return p; }
    function check(timedOut) {
      if (done) return; done = true; stopTimer(); act.remove(); inp.disabled = true;
      var v = norm(inp.value), hit = false, typo = false;
      q.accept.forEach(function (x) { var n = norm(x); if (v && v === n) hit = true; else if (v && n.length >= 6 && lev(v, n) <= 1) typo = true; });
      if (hit || typo) { inp.classList.add("ok"); settle(q, area, keys, "got", false, ans(typo && !hit ? " (small typo accepted)" : "")); return; }
      inp.classList.add("no");
      if (timedOut || !v) { settle(q, area, keys, "miss", timedOut, ans()); return; }
      var f = el("div", "reveal-in"); f.appendChild(ans());
      f.appendChild(el("p", "note", "Not an exact match. If your wording means the same thing, say so:"));
      var rate = el("div", "rate");
      [["miss", "Different"], ["part", "Close"], ["got", "Same idea"]].forEach(function (x) {
        var b = el("button", x[0], x[1]); b.type = "button";
        b.addEventListener("click", function () { f.remove(); settle(q, area, keys, x[0], false, ans()); }); rate.appendChild(b);
      });
      f.appendChild(rate); area.appendChild(f);
      ctx = null;
    }
    ctx = function (e) { if (e.key === "Enter") { e.preventDefault(); check(false); } };
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); e.stopPropagation(); check(false); } });
    onExpire = function () { check(true); };
  }

  /* ---------- put in order (tap to place) ---------- */
  function order(q, area, keys) {
    var items = shuffle(q.items.map(function (t, i) { return { t: t, i: i }; })), placed = [], done = false;
    var yours = el("div", "ordlist"), pool = el("div", "ordpool"), act = el("div", "act");
    var chk = actBtn("Check order", "main", function () { check(false); }); chk.disabled = true; act.appendChild(chk);
    area.appendChild(el("p", "note", "Tap the items from first to last. Tap a placed item to take it back."));
    area.appendChild(yours); area.appendChild(pool); area.appendChild(act);
    function draw() {
      yours.textContent = ""; pool.textContent = "";
      if (!placed.length) yours.appendChild(el("div", "ordhint", "Your order appears here"));
      placed.forEach(function (it, k) {
        var b = el("button", "ord placed"); b.type = "button"; b.appendChild(el("span", "k", String(k + 1))); b.appendChild(el("span", null, it.t));
        b.addEventListener("click", function () { if (!done) { placed.splice(k, 1); draw(); } }); yours.appendChild(b);
      });
      items.forEach(function (it) {
        if (placed.indexOf(it) >= 0) return;
        var b = el("button", "ord", it.t); b.type = "button";
        b.addEventListener("click", function () { if (!done) { placed.push(it); draw(); } }); pool.appendChild(b);
      });
      chk.disabled = placed.length !== items.length;
    }
    function check(timedOut) {
      if (done) return; done = true; act.remove();
      var complete = placed.length === items.length;
      items.forEach(function (it) { if (placed.indexOf(it) < 0) placed.push(it); });
      yours.textContent = ""; pool.textContent = ""; var ok = 0;
      placed.forEach(function (it, k) {
        var good = it.i === k; if (good) ok++;
        var b = el("div", "ord placed " + (good ? "right" : "wrong")); b.appendChild(el("span", "k", String(k + 1))); b.appendChild(el("span", null, it.t)); yours.appendChild(b);
      });
      var res = grade3(ok, items.length); if (timedOut && !complete) res = "miss";
      var ex = null;
      if (res !== "got") { ex = el("div", "corr"); ex.appendChild(el("p", "note", "Correct order:")); q.items.forEach(function (t, k) { ex.appendChild(el("div", "ordline", (k + 1) + ". " + t)); }); }
      settle(q, area, keys, res, timedOut, ex);
    }
    draw();
    keys.textContent = "Keys: Enter to check";
    ctx = function (e) { if (e.key === "Enter" && !chk.disabled) check(false); };
    onExpire = function () { check(true); };
  }

  /* ---------- match the pairs (tap left, then tap right) ---------- */
  var PAL = ["#ff5d73", "#12b5a6", "#7c5cff", "#ff9f1c", "#2743d6", "#1e8a63"];
  function tint(c) { return "color-mix(in srgb," + c + " 16%,#fff)"; }
  function match(q, area, keys) {
    var L = q.pairs.map(function (p) { return p[0]; }), R = shuffle(q.pairs.map(function (p, i) { return { t: p[1], i: i }; }));
    var link = {}, selL = null, done = false, wrap = el("div", "match"), lc = el("div", "mcol"), rc = el("div", "mcol");
    var act = el("div", "act"), chk = actBtn("Check matches", "main", function () { check(false); }); chk.disabled = true; act.appendChild(chk);
    area.appendChild(el("p", "note", "Tap an item on the left, then tap its match. Tap a linked item to undo."));
    wrap.appendChild(lc); wrap.appendChild(rc); area.appendChild(wrap); area.appendChild(act);
    function leftOf(r) { for (var i = 0; i < L.length; i++) if (link[i] === r) return i; return -1; }
    function draw() {
      lc.textContent = ""; rc.textContent = "";
      L.forEach(function (t, i) {
        var b = el("button", "mbtn" + (selL === i ? " sel" : ""), t); b.type = "button";
        if (link[i]) { b.style.borderColor = PAL[i]; b.style.background = tint(PAL[i]); }
        b.addEventListener("click", function () { if (done) return; if (link[i]) { delete link[i]; selL = i; } else selL = selL === i ? null : i; draw(); });
        lc.appendChild(b);
      });
      R.forEach(function (r) {
        var li = leftOf(r), b = el("button", "mbtn", r.t); b.type = "button";
        if (li >= 0) { b.style.borderColor = PAL[li]; b.style.background = tint(PAL[li]); }
        b.addEventListener("click", function () {
          if (done) return;
          if (li >= 0) { delete link[li]; selL = null; }
          else if (selL !== null) { link[selL] = r; selL = null; }
          draw();
        });
        rc.appendChild(b);
      });
      chk.disabled = Object.keys(link).length !== L.length;
    }
    function check(timedOut) {
      if (done) return; done = true; act.remove(); selL = null;
      var ok = 0; lc.textContent = ""; rc.textContent = "";
      var rows = el("div", "mres");
      L.forEach(function (t, i) {
        var r = link[i], good = r && r.i === i; if (good) ok++;
        var row = el("div", "mrow " + (good ? "right" : "wrong"));
        row.appendChild(el("b", null, t)); row.appendChild(el("span", null, r ? r.t : "(not matched)"));
        if (!good) row.appendChild(el("em", "tag", "Should be: " + q.pairs[i][1]));
        rows.appendChild(row);
      });
      wrap.replaceWith(rows);
      var res = grade3(ok, L.length); if (timedOut && Object.keys(link).length !== L.length) res = "miss";
      settle(q, area, keys, res, timedOut);
    }
    draw();
    keys.textContent = "Keys: Enter to check";
    ctx = function (e) { if (e.key === "Enter" && !chk.disabled) check(false); };
    onExpire = function () { check(true); };
  }

  /* ---------- sort into groups (tap item, then tap a group) ---------- */
  function sort(q, area, keys) {
    var items = shuffle(q.items.map(function (x, i) { return { t: x.t, g: x.g, at: null }; })), sel = null, done = false;
    var pool = el("div", "spool"), boxes = q.groups.map(function () { return el("div", "schips"); });
    var act = el("div", "act"), chk = actBtn("Check groups", "main", function () { check(false); }); chk.disabled = true; act.appendChild(chk);
    var grid = el("div", "sgrid");
    area.appendChild(el("p", "note", "Tap an item, then tap the group it belongs to. Tap a placed item to take it back."));
    area.appendChild(pool);
    q.groups.forEach(function (g, gi) {
      var box = el("div", "sbox"), head = el("button", "shead", g); head.type = "button";
      head.addEventListener("click", function () { if (!done && sel) { sel.at = gi; sel = null; draw(); } });
      box.appendChild(head); box.appendChild(boxes[gi]); grid.appendChild(box);
    });
    area.appendChild(grid); area.appendChild(act);
    function draw() {
      pool.textContent = ""; boxes.forEach(function (b) { b.textContent = ""; });
      items.forEach(function (it) {
        var b = el("button", "chip2" + (sel === it ? " sel" : ""), it.t); b.type = "button";
        b.addEventListener("click", function () { if (done) return; if (it.at !== null) { it.at = null; sel = null; } else sel = sel === it ? null : it; draw(); });
        (it.at === null ? pool : boxes[it.at]).appendChild(b);
      });
      if (!pool.children.length) pool.appendChild(el("div", "ordhint", "All placed. Check your groups."));
      chk.disabled = items.some(function (it) { return it.at === null; });
    }
    function check(timedOut) {
      if (done) return; done = true; act.remove();
      var complete = !items.some(function (it) { return it.at === null; }), ok = 0, notes = el("div", "corr");
      boxes.forEach(function (b) { b.textContent = ""; }); pool.textContent = "";
      items.forEach(function (it) {
        var good = it.at === it.g; if (good) ok++;
        var b = el("div", "chip2 " + (good ? "right" : "wrong"), it.t);
        (it.at === null ? pool : boxes[it.at]).appendChild(b);
        if (!good) notes.appendChild(el("p", "ordline", "\u201c" + it.t + "\u201d belongs under " + q.groups[it.g] + "."));
      });
      var res = grade3(ok, items.length); if (timedOut && !complete) res = "miss";
      settle(q, area, keys, res, timedOut, notes.children.length ? notes : null);
    }
    draw();
    keys.textContent = "Keys: Enter to check";
    ctx = function (e) { if (e.key === "Enter" && !chk.disabled) check(false); };
    onExpire = function () { check(true); };
  }

  function recall(q, area, keys) {
    area.appendChild(el("p", "cue", "Say or think your answer first. Then check how close you were."));
    var a = el("div", "act"), r = el("button", "btn main", "Show the answer"); r.type = "button"; a.appendChild(r); area.appendChild(a);
    keys.textContent = "Keys: Space to show the answer";
    function reveal(timedOut) {
      stopTimer(); area.textContent = "";
      var f = el("div", "reveal-in");
      f.appendChild(el("div", "why", q.a)); f.appendChild(reread(q));
      f.appendChild(el("p", "note", (timedOut === true ? "Time's up. " : "") + "How close was your answer?"));
      var rate = el("div", "rate");
      [["miss", "Missed it", "Back soon", "1"], ["part", "Partly", "In a day or so", "2"], ["got", "Got it", "Later", "3"]].forEach(function (x) {
        var b = el("button", x[0]); b.type = "button"; b.appendChild(document.createTextNode(x[1])); b.appendChild(el("small", null, x[2]));
        b.addEventListener("click", function () { if (x[0] === "got") burst(b); grade(x[0]); }); rate.appendChild(b);
      });
      f.appendChild(rate); area.appendChild(f);
      keys.textContent = "Keys: 1 missed, 2 partly, 3 got it";
      ctx = function (e) { if (e.key === "1") grade("miss"); if (e.key === "2") grade("part"); if (e.key === "3") grade("got"); };
    }
    function grade(r) { qAnswered = true; score[r]++; if (r === "miss") missed.push(q); rec(q, r); advance(); }
    r.addEventListener("click", function () { reveal(false); }); r.focus();
    ctx = function (e) { if (e.key === " " || e.key === "Enter") { e.preventDefault(); reveal(false); } };
    onExpire = function () { reveal(true); };
  }
  document.addEventListener("keydown", function (e) {
    if (!ctx || locked || e.metaKey || e.ctrlKey || e.altKey) return;
    if ((e.key === " " || e.key === "Enter") && e.target.tagName === "BUTTON") return; // let focused buttons act normally
    if (e.key === "Enter" || e.key === " ") e.preventDefault(); // stop the keypress from clicking a button that gets focus during this handler
    ctx(e);
  });

  function verdictFor(pct, total) {
    if (pct > 90 && total > 15) return "excellent";
    return pct >= 60 ? "pass" : "fail";
  }
  var VTEXT = { excellent: "Excellent", pass: "Pass", fail: "Fail" };
  function fmt(n) { return String(Math.round(n * 10) / 10); }
  function scopeName() { return scope.value === "all" ? "Whole book" : scope.value; }
  function finish() {
    stopTimer(); stopTotal(); ctx = null; var p = panel(), t = score.got + score.part + score.miss;
    if (t === 0) {
      var e0 = el("div", "result"); e0.appendChild(el("h2", null, "Time ran out before you answered anything."));
      e0.appendChild(el("p", "note", "This attempt was not recorded."));
      var h0 = el("button", "btn main", "Back to start"); h0.type = "button"; h0.addEventListener("click", goHome);
      var a0 = el("div", "act"); a0.style.justifyContent = "center"; a0.appendChild(h0); e0.appendChild(a0); p.appendChild(e0); return;
    }
    var marks = score.got + 0.5 * score.part, pct = t ? 100 * marks / t : 0, v = verdictFor(pct, t);
    state.history.unshift({ t: Date.now(), pct: pct, marks: marks, total: t, v: v, scope: scopeName(), limit: limit, mins: sessionTimed ? sessionMins : 0 });
    state.history = state.history.slice(0, 5); save();
    var box = el("div", "result v-" + v);
    var hero = el("div", "rhero pop-in");
    hero.appendChild(el("span", "rbadge", VTEXT[v]));
    var big = el("div", "rpct"); big.appendChild(document.createTextNode("0")); big.appendChild(el("small", null, "%")); hero.appendChild(big);
    hero.appendChild(el("div", "rmarks", "Marks: " + fmt(marks) + " out of " + t));
    if (sessionTimed) hero.appendChild(el("div", "rsub", t + (t === 1 ? " question" : " questions") + " answered in a " + sessionMins + " minute session"));
    var msg = v === "excellent" ? "Outstanding recall. This is what the book looks like when it sticks." :
              v === "pass" ? (pct > 90 && t <= 15 ? "Over 90%. Answer 16 or more questions in one session to earn Excellent." : "You passed. Keep going to make it stick.") :
              "Not yet. Reread the topics below, then try again.";
    hero.appendChild(el("p", "rmsg", msg));
    box.appendChild(hero);
    box.appendChild(el("p", "rrule", "Excellent: over 90% with more than 15 questions. Pass: 60% or more. Fail: under 60%. A partly-right answer earns half a mark."));
    var s3 = el("div", "score3");
    [["got", "Got it", score.got], ["part", "Partly", score.part], ["miss", "Missed", score.miss]].forEach(function (x) {
      var d = el("div", "s-" + x[0]); d.appendChild(el("b", null, String(x[2]))); d.appendChild(el("span", null, x[1])); s3.appendChild(d);
    });
    box.appendChild(s3);
    if (confOn && sessionCM) box.appendChild(el("p", "cm", sessionCM + (sessionCM === 1 ? " confident miss" : " confident misses") + ": you were certain and wrong. These are the best things to reread."));
    if (missed.length) {
      var h = el("p", "note", "Reread these before the next session. They will come back sooner."); h.style.textAlign = "left"; box.appendChild(h);
      var ul = el("ul", "revisit"); ul.style.textAlign = "left";
      missed.forEach(function (q) { var li = el("li", null, q.q); li.appendChild(el("span", null, "Chapter " + numOf(q.unit) + (q.unitTitle ? ", " + q.unitTitle : "") + ". Topic: " + q.section)); ul.appendChild(li); });
      box.appendChild(ul);
    }
    var a = el("div", "act"), again = el("button", "btn main", "Practise again"), home = el("button", "btn", "Back to start");
    a.style.justifyContent = "center";
    again.type = home.type = "button";
    again.addEventListener("click", function () { goHome(); $("start").click(); }); home.addEventListener("click", goHome);
    a.appendChild(again); a.appendChild(home); box.appendChild(a); p.appendChild(box);
    // count up the percentage
    var target = Math.round(pct * 10) / 10, reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) big.firstChild.nodeValue = fmt(target);
    else { var t0 = null; (function step(ts) { if (!t0) t0 = ts; var k = Math.min((ts - t0) / 900, 1); big.firstChild.nodeValue = fmt(target * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); })(performance.now()); }
    if (v !== "fail") setTimeout(function () { burst(hero, v === "excellent" ? 60 : 32); }, 250);
  }
  function renderHistory() {
    var h = $("hist"); h.textContent = "";
    if (!state.history.length) { h.classList.add("hide"); return; }
    h.classList.remove("hide");
    h.appendChild(el("h2", null, "Your recent results"));
    state.history.forEach(function (r) {
      var row = el("div", "hrow");
      row.appendChild(el("span", "vchip " + r.v, VTEXT[r.v]));
      var w = el("div", "when"), d = new Date(r.t);
      w.appendChild(el("b", null, r.scope + (r.mins ? ", " + r.mins + " min session" : "") + (r.limit ? ", " + r.limit + "s each" : "")));
      w.appendChild(document.createTextNode(d.toLocaleDateString(undefined, { day: "numeric", month: "short" }) + ", " + d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" })));
      row.appendChild(w);
      var hp = el("div", "hp", fmt(r.pct) + "%"); hp.appendChild(el("small", null, fmt(r.marks) + " of " + r.total + " marks")); row.appendChild(hp);
      h.appendChild(row);
    });
  }
  function goHome() { document.body.classList.remove("playing"); stopTotal(); stopTimer(); ctx = null; $("play").classList.add("hide"); $("homeWrap").classList.remove("hide"); $("stats").classList.remove("hide"); renderHome(); window.scrollTo({ top: 0 }); }

  /* ---------- gaps: chapter and topic ---------- */
  function renderStats() {
    var s = $("stats"); s.textContent = "";
    s.appendChild(el("h2", null, "Where you stand"));
    if (!Object.keys(state.items).length) s.appendChild(el("p", "empty", "Nothing yet. Start a session and your chapters and topics will fill in here, with the weak ones marked."));
    units.forEach(function (u) {
      var qs = Q.questions.filter(function (q) { return q.unit === u; });
      var solid = qs.filter(function (q) { var it = state.items[q.id]; return it && it.box >= 3; }).length;
      var d = el("details", "chap"), sm = el("summary");
      var nm = el("div", "nm"); nm.appendChild(el("b", null, u)); nm.appendChild(el("span", null, titles[u]));
      var bar = el("div", "bar"), i = el("i"); i.style.width = Math.round(100 * solid / qs.length) + "%"; bar.appendChild(i);
      sm.appendChild(nm); sm.appendChild(bar); sm.appendChild(el("div", "pct", Math.round(100 * solid / qs.length) + "%"));
      d.appendChild(sm);
      var tops = [], by = {};
      qs.forEach(function (q) { if (!by[q.section]) { by[q.section] = []; tops.push(q.section); } by[q.section].push(q); });
      var ul = el("ul", "tops");
      tops.forEach(function (tp) {
        var g = by[tp], sd = g.filter(function (q) { var it = state.items[q.id]; return it && it.box >= 3; }).length;
        var ms = g.reduce(function (n, q) { var it = state.items[q.id]; return n + (it ? it.missed : 0); }, 0);
        var li = el("li"), nm2 = el("span", ms ? "weak" : null, tp + (ms ? " (missed " + ms + "x)" : ""));
        var b2 = el("div", "bar"), i2 = el("i"); i2.style.width = Math.round(100 * sd / g.length) + "%"; b2.appendChild(i2);
        li.appendChild(nm2); li.appendChild(b2); li.appendChild(el("div", "pct", Math.round(100 * sd / g.length) + "%")); ul.appendChild(li);
      });
      d.appendChild(ul); s.appendChild(d);
    });
    s.appendChild(el("p", "note", "Solid means answered right several times with growing gaps. Open a chapter to see its topics. Topics in red are ones you have missed."));
  }

  /* ---------- backup ---------- */
  $("export").addEventListener("click", function () {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(state)], { type: "application/json" }));
    a.download = Q.id + "-progress.json"; a.click();
  });
  $("importBtn").addEventListener("click", function () { $("importFile").click(); });
  $("importFile").addEventListener("change", function (e) {
    var f = e.target.files[0]; if (!f) return; var r = new FileReader();
    r.onload = function () {
      try { var d = JSON.parse(r.result); if (!d.items) throw 0; if (!d.days) d.days = []; if (!d.history) d.history = []; state = d; save(); renderHome(); alert("Progress loaded."); }
      catch (x) { alert("That file is not a progress backup from this quiz."); }
    };
    r.readAsText(f);
  });
  $("reset").addEventListener("click", function () {
    if (confirm("Erase all progress saved in this browser?")) { state = { items: {}, days: [], history: [] }; save(); renderHome(); }
  });

  loadQuestions();
})();
