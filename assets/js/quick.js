// 「一句话速记」页:#/quick  ·  #/quick/<id> 定位到某题
// 两种模式:列表速览(可遮住答案自测)/ 闪卡(一张一张背,空格翻面)。
import { getOneliner } from "./data.js";

const MASTER_KEY = "lc100.oneliner.v1";   // { [id]: 掌握时间戳 }
const PREF_KEY = "lc100.quick.prefs";      // { mode, hide }

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}
// 转义后把 O(...) 复杂度标成行内代码,方便扫读
function fmt(s) {
  return esc(s).replace(/O\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)/g, m => `<code>${m}</code>`);
}
function diffClass(d) {
  d = (d || "").toLowerCase();
  return d.startsWith("e") ? "easy" : d.startsWith("h") ? "hard" : "medium";
}

// ---- 本地状态 ----
function loadJSON(key, fallback) {
  try { return JSON.parse(localStorage.getItem(key)) || fallback; } catch { return fallback; }
}
const mastered = {
  all() { return loadJSON(MASTER_KEY, {}); },
  has(id) { return !!this.all()[id]; },
  toggle(id) {
    const s = this.all();
    if (s[id]) delete s[id]; else s[id] = Date.now();
    localStorage.setItem(MASTER_KEY, JSON.stringify(s));
    return !!s[id];
  },
};
const prefs = Object.assign({ mode: "list", hide: false }, loadJSON(PREF_KEY, {}));
function savePrefs() { localStorage.setItem(PREF_KEY, JSON.stringify(prefs)); }

const SVG_EXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>';
const SVG_COPY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';

// ---- 片段 ----
function codeHtml(it) {
  const lines = it.code.split("\n").length;
  return `
    <details class="ql-code">
      <summary>Python 代码 <span class="ql-mute">· ${lines} 行</span></summary>
      <div class="code-block">
        <div class="code-toolbar"><span>python</span>
          <button class="copy-btn" type="button">${SVG_COPY} <span>复制</span></button>
        </div>
        <pre class="code"><code class="language-python">${esc(it.code)}</code></pre>
      </div>
    </details>`;
}

function answerHtml(it) {
  return `
    <div class="ql-grid">
      <div>
        <div class="ql-label">面试口述 · ${esc(it.method)}</div>
        <ol class="ql-steps">${it.steps.map(s => `<li>${fmt(s)}</li>`).join("")}</ol>
      </div>
      <div>
        <div class="ql-label">3 个核心要点</div>
        <ul class="ql-points">${it.points.map(p => `<li><strong>${esc(p.k)}</strong>${fmt(p.v)}</li>`).join("")}</ul>
      </div>
    </div>
    ${it.followup ? `<div class="ql-follow"><span class="ql-label">追问应对</span>${fmt(it.followup)}</div>` : ""}`;
}

function linksHtml(it) {
  return `
    ${it.in_site ? `<a class="ql-link" href="#/p/${it.id}" title="站内详解:题面 / 多解法 / 可视化">详解 →</a>` : ""}
    <a class="lc-btn" href="${esc(it.leetcode_url)}" target="_blank" rel="noopener" title="在 LeetCode 上默写">${SVG_EXT}<span>练习</span></a>`;
}

function masterBtn(it) {
  const on = mastered.has(it.id);
  return `<button class="ql-master ${on ? "on" : ""}" type="button" data-id="${it.id}" aria-pressed="${on}" title="标记为已掌握">${on ? "✓ 已掌握" : "标记掌握"}</button>`;
}

function headHtml(it) {
  return `
    <span class="ql-num">#${it.id}</span>
    <h3 class="ql-title">${esc(it.title)}</h3>
    <span class="diff ${diffClass(it.difficulty)}">${esc(it.difficulty)}</span>
    ${it.in_site ? "" : `<span class="ql-tag" title="不在本站 Hot 100 题单内的高频补充题">补充</span>`}`;
}

function cardHtml(it) {
  return `
    <article class="ql-card ${mastered.has(it.id) ? "is-mastered" : ""}" id="q-${it.id}" data-id="${it.id}">
      <header class="ql-head">
        ${headHtml(it)}
        <div class="ql-actions">${masterBtn(it)}${linksHtml(it)}</div>
      </header>
      <div class="ql-answer" tabindex="0" aria-label="答案,遮住时点击显示">
        <p class="ql-one">${fmt(it.oneliner)}</p>
        ${answerHtml(it)}
      </div>
      ${codeHtml(it)}
    </article>`;
}

// ---- 页面 ----
const state = { q: "", cat: "all", st: "all", order: null, idx: 0, flipped: false, data: null };

export async function renderQuick(focusId) {
  const app = document.getElementById("app");
  app.innerHTML = `<div class="loader"></div>`;
  let data;
  try {
    data = await getOneliner();
  } catch {
    app.innerHTML = `<div class="container empty">一句话速记数据加载失败,请刷新重试。</div>`;
    return;
  }
  state.data = data;
  state.order = null;
  if (focusId) { state.cat = "all"; state.st = "all"; state.q = ""; prefs.mode = "list"; }

  const cats = data.categories;
  app.innerHTML = `
    <div class="container quick">
      <div class="ql-hero">
        <h1>⚡ 一句话速记</h1>
        <p class="section-sub">${data.items.length} 道高频题的 Python 面试口述版:先背一句话,再展开口述步骤、3 个核心要点和代码。
          遮住答案自测,或切到闪卡一张张过。</p>
        <div class="ql-meter"><span id="ql-meter-text"></span><div class="progress-bar"><div class="progress-fill" id="ql-meter-fill"></div></div></div>
      </div>

      <div class="ql-bar">
        <div class="toolbar ql-toolbar">
          <div class="search">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input id="search" type="search" placeholder="搜索:题号 / 标题 / 关键词(如 单调栈、dummy)" value="${esc(state.q)}" />
          </div>
          <span class="seg-toggle" id="ql-mode" role="tablist" aria-label="浏览模式">
            <button class="seg-btn" data-mode="list" role="tab">列表速览</button>
            <button class="seg-btn" data-mode="cards" role="tab">闪卡背诵</button>
          </span>
          <label class="ql-switch" id="ql-hide-wrap" title="遮住一句话和要点,点击卡片再看,先自己回忆"><input type="checkbox" id="ql-hide"> 遮住答案</label>
          <div class="filter-pills" id="ql-st">
            <button class="pill" data-st="all">全部</button>
            <button class="pill" data-st="todo">未掌握</button>
            <button class="pill" data-st="done">已掌握</button>
          </div>
        </div>
        <div class="ql-cats" id="ql-cats">
          <button class="pill" data-cat="all">全部 <span class="ql-count">${data.items.length}</span></button>
          ${cats.map(c => `<button class="pill" data-cat="${esc(c.name)}">${esc(c.name)} <span class="ql-count">${c.ids.length}</span></button>`).join("")}
        </div>
      </div>

      <div id="ql-view"></div>

      <section class="ql-summary">
        <h2 class="section-title">技巧总览</h2>
        <p class="section-sub">每类题的核心方法,一行一个。</p>
        <div class="md"><table><thead><tr><th>分类</th><th>核心方法</th></tr></thead><tbody>
          ${data.summary.map(([a, b]) => `<tr><td><a href="#" data-cat-jump="${esc(a)}">${esc(a)}</a></td><td>${esc(b)}</td></tr>`).join("")}
        </tbody></table></div>
      </section>
    </div>`;

  bindControls();
  update();

  if (focusId) {
    const card = document.getElementById(`q-${focusId}`);
    if (card) {
      card.scrollIntoView({ block: "start" });
      card.classList.add("flash");
      setTimeout(() => card.classList.remove("flash"), 1600);
    }
  }
}

function filtered() {
  const { items } = state.data;
  const q = state.q.trim().toLowerCase();
  return items.filter(it => {
    if (state.cat !== "all" && it.category !== state.cat) return false;
    const m = mastered.has(it.id);
    if (state.st === "done" && !m) return false;
    if (state.st === "todo" && m) return false;
    if (!q) return true;
    if (String(it.id) === q) return true;
    const blob = [it.title, it.method, it.oneliner, it.category, ...it.steps,
      ...it.points.map(p => p.k + p.v), it.followup, it.code].join(" ").toLowerCase();
    return blob.includes(q);
  });
}

function update() {
  const all = state.data.items;
  const done = all.filter(it => mastered.has(it.id)).length;
  document.getElementById("ql-meter-text").textContent = `已掌握 ${done} / ${all.length}`;
  document.getElementById("ql-meter-fill").style.width = `${Math.round(done / all.length * 100)}%`;

  document.querySelectorAll("#ql-mode .seg-btn").forEach(b => {
    const on = b.dataset.mode === prefs.mode;
    b.classList.toggle("active", on);
    b.setAttribute("aria-selected", on);
  });
  document.querySelectorAll("#ql-st .pill").forEach(b => b.classList.toggle("active", b.dataset.st === state.st));
  document.querySelectorAll("#ql-cats .pill").forEach(b => b.classList.toggle("active", b.dataset.cat === state.cat));
  document.getElementById("ql-hide").checked = prefs.hide;
  document.getElementById("ql-hide-wrap").hidden = prefs.mode !== "list";

  if (prefs.mode === "cards") renderCards(); else renderList();
}

function renderList() {
  const view = document.getElementById("ql-view");
  const items = filtered();
  if (!items.length) {
    view.innerHTML = `<div class="empty">没有匹配的题目。</div>`;
    return;
  }
  // 按分类分组,保留原顺序
  const groups = new Map();
  for (const it of items) {
    if (!groups.has(it.category)) groups.set(it.category, []);
    groups.get(it.category).push(it);
  }
  view.innerHTML = `<div class="ql-list ${prefs.hide ? "quiz" : ""}">${
    [...groups].map(([cat, arr]) => `
      <section class="ql-group">
        <h2 class="ql-group-title">${esc(cat)} <span class="ql-mute">${arr.length} 题</span></h2>
        ${arr.map(cardHtml).join("")}
      </section>`).join("")
  }</div>`;
}

// ---- 闪卡 ----
function cardPool() {
  const pool = filtered();
  if (state.order) {
    const rank = new Map(state.order.map((id, i) => [id, i]));
    pool.sort((a, b) => (rank.get(a.id) ?? 1e9) - (rank.get(b.id) ?? 1e9));
  }
  return pool;
}

function renderCards() {
  const view = document.getElementById("ql-view");
  const pool = cardPool();
  if (!pool.length) {
    view.innerHTML = `<div class="empty">没有匹配的题目。${state.st === "todo" ? "当前筛选下都已掌握 🎉" : ""}</div>`;
    return;
  }
  state.idx = Math.min(Math.max(state.idx, 0), pool.length - 1);
  const it = pool[state.idx];
  view.innerHTML = `
    <div class="fc">
      <div class="fc-top">
        <span class="ql-mute">${state.idx + 1} / ${pool.length} · ${esc(it.category)}</span>
        <button class="pill" type="button" id="fc-shuffle" title="打乱当前筛选结果的顺序">🔀 ${state.order ? "恢复顺序" : "打乱"}</button>
      </div>
      <article class="ql-card fc-card ${mastered.has(it.id) ? "is-mastered" : ""} ${state.flipped ? "revealed" : ""}" data-id="${it.id}">
        <header class="ql-head">
          ${headHtml(it)}
          <div class="ql-actions">${masterBtn(it)}${linksHtml(it)}</div>
        </header>
        <p class="fc-prompt">用一句话说出思路,再口述步骤和 3 个要点。<span class="ql-mute">提示:${esc(it.method)}</span></p>
        ${state.flipped ? `
          <div class="ql-answer">
            <p class="ql-one">${fmt(it.oneliner)}</p>
            ${answerHtml(it)}
          </div>
          ${codeHtml(it)}`
        : `<button class="fc-reveal" type="button" id="fc-reveal">显示答案 <span class="kbd">Space</span></button>`}
      </article>
      <div class="fc-nav">
        <button class="pill" type="button" id="fc-prev" ${state.idx === 0 ? "disabled" : ""}>← 上一张</button>
        <span class="ql-mute fc-keys"><span class="kbd">←</span><span class="kbd">→</span> 翻页 · <span class="kbd">Space</span> 翻面 · <span class="kbd">M</span> 掌握</span>
        <button class="pill" type="button" id="fc-next" ${state.idx >= pool.length - 1 ? "disabled" : ""}>下一张 →</button>
      </div>
    </div>`;
  document.getElementById("fc-prev").onclick = () => fcGo(-1);
  document.getElementById("fc-next").onclick = () => fcGo(1);
  const rv = document.getElementById("fc-reveal");
  if (rv) rv.onclick = fcFlip;
  document.getElementById("fc-shuffle").onclick = () => {
    if (state.order) state.order = null;
    else {
      const ids = state.data.items.map(x => x.id);
      for (let i = ids.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [ids[i], ids[j]] = [ids[j], ids[i]];
      }
      state.order = ids;
    }
    state.idx = 0; state.flipped = false;
    renderCards();
  };
}

function fcGo(d) {
  const n = cardPool().length;
  const next = state.idx + d;
  if (next < 0 || next >= n) return;
  state.idx = next; state.flipped = false;
  renderCards();
}
function fcFlip() {
  state.flipped = !state.flipped;
  renderCards();
  if (state.flipped) highlightIn(document.querySelector(".fc-card"));
}

// ---- 交互 ----
function highlightIn(root) {
  if (!window.hljs || !root) return;
  root.querySelectorAll("pre.code code:not(.hljs)").forEach(b => window.hljs.highlightElement(b));
}

function resetPos() { state.idx = 0; state.flipped = false; }

function bindControls() {
  let t;
  document.getElementById("search").addEventListener("input", e => {
    state.q = e.target.value;
    clearTimeout(t);
    t = setTimeout(() => { resetPos(); update(); }, 120);
  });
  document.getElementById("ql-mode").addEventListener("click", e => {
    const m = e.target.closest("[data-mode]");
    if (!m) return;
    prefs.mode = m.dataset.mode; savePrefs(); resetPos(); update();
  });
  document.getElementById("ql-hide").addEventListener("change", e => {
    prefs.hide = e.target.checked; savePrefs(); update();
  });
  document.getElementById("ql-st").addEventListener("click", e => {
    const b = e.target.closest("[data-st]");
    if (!b) return;
    state.st = b.dataset.st; resetPos(); update();
  });
  document.getElementById("ql-cats").addEventListener("click", e => {
    const b = e.target.closest("[data-cat]");
    if (!b) return;
    state.cat = b.dataset.cat; resetPos(); update();
  });

  const root = document.querySelector(".quick");
  root.addEventListener("click", e => {
    const jump = e.target.closest("[data-cat-jump]");
    if (jump) {
      e.preventDefault();
      state.cat = jump.dataset.catJump; resetPos(); update();
      document.querySelector(".ql-bar").scrollIntoView({ behavior: "smooth" });
      return;
    }
    const mb = e.target.closest(".ql-master");
    if (mb) {
      const id = Number(mb.dataset.id);
      mastered.toggle(id);
      // 列表模式就地更新,避免重渲染丢失展开状态;「未掌握/已掌握」筛选下需要重排
      if (prefs.mode === "list" && state.st === "all") {
        const on = mastered.has(id);
        mb.outerHTML = masterBtn({ id });
        document.getElementById(`q-${id}`)?.classList.toggle("is-mastered", on);
        const all = state.data.items, done = all.filter(x => mastered.has(x.id)).length;
        document.getElementById("ql-meter-text").textContent = `已掌握 ${done} / ${all.length}`;
        document.getElementById("ql-meter-fill").style.width = `${Math.round(done / all.length * 100)}%`;
      } else {
        update();
      }
      return;
    }
    const copy = e.target.closest(".copy-btn");
    if (copy) {
      const code = copy.closest(".code-block").querySelector("pre.code").innerText;
      navigator.clipboard?.writeText(code);
      copy.querySelector("span").textContent = "已复制";
      setTimeout(() => copy.querySelector("span").textContent = "复制", 1200);
      return;
    }
    // 遮住答案模式:点击答案区显示
    const ans = e.target.closest(".quiz .ql-answer");
    if (ans) ans.closest(".ql-card").classList.add("revealed");
  });
  root.addEventListener("keydown", e => {
    if ((e.key === "Enter" || e.key === " ") && e.target.matches(".quiz .ql-answer")) {
      e.preventDefault();
      e.target.closest(".ql-card").classList.add("revealed");
    }
  });
  // 代码展开时再高亮,避免一次性高亮 58 段
  root.addEventListener("toggle", e => {
    if (e.target.matches?.("details.ql-code") && e.target.open) highlightIn(e.target);
  }, true);
}

// 闪卡快捷键(全局只注册一次,仅在本页闪卡模式下生效)
document.addEventListener("keydown", e => {
  if (!location.hash.startsWith("#/quick") || prefs.mode !== "cards" || !state.data) return;
  if (e.target.matches("input, textarea") || e.metaKey || e.ctrlKey || e.altKey) return;
  if (e.key === "ArrowLeft") { fcGo(-1); e.preventDefault(); }
  else if (e.key === "ArrowRight") { fcGo(1); e.preventDefault(); }
  else if (e.key === " " || e.key === "Enter") {
    if (e.target.matches("button, a, summary")) return;
    fcFlip(); e.preventDefault();
  } else if (e.key === "m" || e.key === "M") {
    const it = cardPool()[state.idx];
    if (it) { mastered.toggle(it.id); update(); }
  }
});

// 供题目详情页调用:返回某题的一句话速记(没有则 null)
export async function onelinerFor(id) {
  try {
    const d = await getOneliner();
    return d.items.find(x => x.id === id) || null;
  } catch {
    return null;
  }
}
