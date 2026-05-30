// All page views.
import { getProblems, getDays, getProblem, getPattern } from "./data.js";
import { renderDoc, renderMarkdown } from "./markdown.js";
import { progress } from "./progress.js";
import { renderViz } from "./viz.js";

const DAY_TITLES = {
  1: "哈希 / 双指针 / 滑动窗口 / 子串",
  2: "数组 / 矩阵",
  3: "链表",
  4: "二叉树",
  5: "图论 / 回溯 / 二分",
  6: "栈 / 堆 / 贪心",
  7: "DP / 多维DP / 技巧",
};
const DAY_KEY_WEAPONS = {
  1: "dict, Counter, 双指针, 单调队列, 前缀和+哈希",
  2: "原地修改, 环状增量, 转置+反转, 模拟",
  3: "哨兵节点, 快慢指针, 三指针翻转, 归并",
  4: "递归三件套, 中序, 层序, Morris",
  5: "并查集, Topo, DFS 涂色, 子集排列, 红蓝染色",
  6: "单调栈, heapq, Top-K, 区间贪心",
  7: "选/不选, 状态压缩, 滚动数组, Boyer-Moore",
};

function el(html) {
  const t = document.createElement("template");
  t.innerHTML = html.trim();
  return t.content.firstElementChild;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

// Inline markdown for explanation text: **bold** and `code` only.
function escInlineMd(s) {
  let r = escapeHtml(s);
  r = r.replace(/`([^`]+)`/g, (_, c) => `<code>${c}</code>`);
  r = r.replace(/\*\*([^*]+)\*\*/g, (_, c) => `<strong>${c}</strong>`);
  return r;
}

// Inline renderer tuned for problem statements: like escInlineMd but also
// prettifies math — x^y → superscript, <= / >= → ≤ / ≥.
function escStmt(s) {
  let r = escapeHtml(s);
  r = r.replace(/\^([0-9a-zA-Z]+)/g, (_, p) => `<sup>${p}</sup>`);
  r = r.replace(/&lt;=/g, "≤").replace(/&gt;=/g, "≥");
  r = r.replace(/`([^`]+)`/g, (_, c) => `<code>${c}</code>`);
  r = r.replace(/\*\*([^*]+)\*\*/g, (_, c) => `<strong>${c}</strong>`);
  return r;
}

// Render the description body: blank-line-separated blocks; a block whose lines
// all start with "- " becomes a <ul>, otherwise a <p> with <br> line breaks.
function renderStmtDesc(text) {
  if (!text) return "";
  const blocks = String(text).replace(/\r\n/g, "\n").split(/\n\s*\n/);
  return blocks.map(b => {
    const lines = b.split("\n").filter(l => l.trim() !== "");
    if (!lines.length) return "";
    if (lines.every(l => /^\s*[-*]\s+/.test(l))) {
      return `<ul>${lines.map(l => `<li>${escStmt(l.replace(/^\s*[-*]\s+/, ""))}</li>`).join("")}</ul>`;
    }
    return `<p>${lines.map(escStmt).join("<br>")}</p>`;
  }).join("");
}

// Render the full structured problem statement (description / examples / constraints).
function renderStatement(stmt) {
  if (!stmt) return "";
  const desc = stmt.description ? `<div class="stmt-desc md">${renderStmtDesc(stmt.description)}</div>` : "";
  const examples = Array.isArray(stmt.examples) && stmt.examples.length
    ? `<div class="stmt-examples">${stmt.examples.map((ex, i) => `
        <div class="example-card">
          <div class="ex-title">示例 ${i + 1}</div>
          ${ex.input  != null ? `<div class="ex-row"><span class="ex-label">输入</span><code class="ex-val">${escapeHtml(ex.input)}</code></div>` : ""}
          ${ex.output != null ? `<div class="ex-row"><span class="ex-label">输出</span><code class="ex-val">${escapeHtml(ex.output)}</code></div>` : ""}
          ${ex.explanation ? `<div class="ex-row ex-expl"><span class="ex-label">解释</span><span class="ex-val">${escStmt(ex.explanation).replace(/\n/g, "<br>")}</span></div>` : ""}
        </div>`).join("")}</div>`
    : "";
  const constraints = Array.isArray(stmt.constraints) && stmt.constraints.length
    ? `<div class="stmt-constraints">
         <div class="stmt-sub">提示</div>
         <ul>${stmt.constraints.map(c => `<li>${escStmt(c)}</li>`).join("")}</ul>
       </div>`
    : "";
  const followUp = stmt.follow_up
    ? `<div class="stmt-followup"><span class="stmt-sub">进阶</span> ${escStmt(stmt.follow_up)}</div>`
    : "";
  return `<div class="statement">${desc}${examples}${constraints}${followUp}</div>`;
}

function diffClass(d) {
  d = (d || "").toLowerCase();
  if (d.startsWith("e")) return "easy";
  if (d.startsWith("h")) return "hard";
  return "medium";
}

const SVG_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
const SVG_EXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>';

// LeetCode 直达练习按钮。url 为空时不渲染。
function lcButton(url, { large = false, label = "去 LeetCode 练习" } = {}) {
  if (!url) return "";
  return `<a class="lc-btn ${large ? "lc-btn-lg" : ""}" href="${url}" target="_blank" rel="noopener" title="在 LeetCode 上打开本题,边看边练">${SVG_EXT}<span>${escapeHtml(label)}</span></a>`;
}

// ===================== Home =====================
export async function renderHome() {
  const app = document.getElementById("app");
  const [list, days] = await Promise.all([getProblems(), getDays()]);
  const total = list.length;
  const done = list.reduce((acc, p) => acc + (progress.isDone(p.id) ? 1 : 0), 0);
  const totalSols = list.reduce((acc, p) => acc + (p.n_sols || 0), 0);

  const hero = `
    <section class="hero container">
      <h1>七天通关 LeetCode Hot 100<br/>带详解、多解法、可视化的 Python 题库</h1>
      <p class="lead">100 题全自测通过、${totalSols}+ 种解法对比、ASCII 可视化、本地进度追踪。
        分七天系统化训练,每题独立文件,适合面试速成与算法巩固。</p>
      <div class="hero-stats">
        <div class="stat"><span class="num accent">${total}</span><span class="label">收录题目</span></div>
        <div class="stat"><span class="num">${totalSols}</span><span class="label">代码解法</span></div>
        <div class="stat"><span class="num">${done}</span><span class="label">你已完成</span></div>
        <div class="stat"><span class="num">7</span><span class="label">天计划</span></div>
      </div>
    </section>`;

  const dayCards = Object.values(days).map(d => {
    const total = d.problem_ids.length;
    const cnt = progress.countDoneIn(d.problem_ids);
    const pct = total ? Math.round(cnt / total * 100) : 0;
    return `
      <a class="day-card" href="#/day/${d.day}">
        <span class="day-badge">DAY ${d.day}</span>
        <h3>${escapeHtml(d.title)}</h3>
        <div class="meta">
          <span>${total} 题</span>
          <span>${cnt}/${total} (${pct}%)</span>
        </div>
        <div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>
        <div style="margin-top:10px;font-size:12px;color:var(--text-mute)">关键武器: ${escapeHtml(DAY_KEY_WEAPONS[d.day] || "")}</div>
      </a>`;
  }).join("");

  app.innerHTML = `
    ${hero}
    <section class="container">
      <h2 class="section-title">7 天作战计划</h2>
      <p class="section-sub">每天 4–6 小时,前 90 min 看题读解,后续盖住代码独立写。</p>
      <div class="day-grid">${dayCards}</div>
    </section>
    <section class="container">
      <h2 class="section-title">使用说明</h2>
      <p class="section-sub" style="font-size:14px;line-height:1.8;">
        点击任意一题查看详解;每题包含<strong>题面 → 直觉 → 多种解法对比 → 复杂度 → 踩坑 → 同类变体</strong>,
        并提供 <strong style="color:var(--lc-text)">「去 LeetCode 练习」</strong> 橙色按钮,一键跳到原题盖码默写。
        第一次用 LeetCode?先看 <a href="#/guide">练习指南 →</a>。
        进度自动保存在浏览器 localStorage,清浏览器数据会重置。
        快捷键:<span class="kbd">/</span> 搜索,<span class="kbd">←</span><span class="kbd">→</span> 翻题,
        <span class="kbd">O</span> 打开 LeetCode,<span class="kbd">D</span> 切换暗色,<span class="kbd">Esc</span> 返回首页。
      </p>
    </section>
    <section class="container">
      <h2 class="section-title">模式速记表</h2>
      <p class="section-sub">把 100 题压成 7 张图,每天先读再做。</p>
      <div class="day-grid">
        ${[
          ["01_window_patterns", "滑动窗口 / 子串"],
          ["02_linked_list_patterns", "链表"],
          ["03_tree_patterns", "二叉树"],
          ["04_dp_patterns", "DP / 背包"],
          ["05_backtrack_patterns", "回溯"],
          ["06_binary_search_patterns", "二分查找"],
          ["07_monotonic_stack_heap", "单调栈 / 堆"],
        ].map(([slug, t]) => `
          <a class="day-card" href="#/pattern/${slug}">
            <span class="day-badge">速记</span>
            <h3>${escapeHtml(t)}</h3>
            <div class="meta"><span>模式总览</span></div>
          </a>`).join("")}
      </div>
    </section>`;
}

// ===================== Day View =====================
export async function renderDay(num) {
  num = Number(num);
  const app = document.getElementById("app");
  const [list, days] = await Promise.all([getProblems(), getDays()]);
  const day = days[num];
  if (!day) {
    app.innerHTML = `<div class="container empty">Day ${num} 不存在。</div>`;
    return;
  }
  const ids = new Set(day.problem_ids);
  const items = list.filter(p => ids.has(p.id));
  const cnt = progress.countDoneIn(day.problem_ids);
  const pct = day.problem_ids.length ? Math.round(cnt / day.problem_ids.length * 100) : 0;

  app.innerHTML = `
    <div class="container">
      <a class="detail-back" href="#/">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
        返回首页
      </a>
      <div class="detail-header">
        <span class="day-badge">DAY ${num}</span>
        <h1>${escapeHtml(day.title)}</h1>
        <div class="detail-meta">
          <span>${items.length} 题</span><span class="sep">·</span>
          <span>已完成 ${cnt}/${items.length}(${pct}%)</span><span class="sep">·</span>
          <span>关键武器: ${escapeHtml(DAY_KEY_WEAPONS[num] || "")}</span>
        </div>
      </div>
      <div class="prob-list" id="day-list"></div>
    </div>`;
  renderProblemList(document.getElementById("day-list"), items);
}

// ===================== All Problems =====================
export async function renderAll() {
  const app = document.getElementById("app");
  const list = await getProblems();
  app.innerHTML = `
    <div class="container">
      <h1 style="font-size:28px;margin:24px 0 8px;letter-spacing:-0.02em;font-weight:700">全部题目 (${list.length})</h1>
      <p class="section-sub">用关键字、难度、Day、状态筛选;点击题号跳到详情。</p>
      <div class="toolbar">
        <div class="search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input id="search" type="search" placeholder="搜索:题号 / 中文标题 / 标签 …" />
        </div>
        <div class="filter-pills" id="filter-diff">
          <button class="pill active" data-diff="all">全部难度</button>
          <button class="pill" data-diff="easy">Easy</button>
          <button class="pill" data-diff="medium">Medium</button>
          <button class="pill" data-diff="hard">Hard</button>
        </div>
        <div class="filter-pills" id="filter-day">
          <button class="pill active" data-day="all">全部</button>
          ${[1,2,3,4,5,6,7].map(d => `<button class="pill" data-day="${d}">D${d}</button>`).join("")}
        </div>
        <div class="filter-pills" id="filter-state">
          <button class="pill active" data-state="all">全部状态</button>
          <button class="pill" data-state="done">已完成</button>
          <button class="pill" data-state="todo">未做</button>
        </div>
        <button class="pill" id="random-btn" title="从当前筛选结果中随机抽一题">🎲 随机一题</button>
      </div>
      <div class="prob-list" id="prob-list"></div>
    </div>`;

  // 支持 URL ?q=xxx 预填搜索(便于分享/书签 + 测试)
  const urlQ = new URLSearchParams(location.search).get("q") || "";
  const state = { q: urlQ, diff: "all", day: "all", st: "all" };
  if (urlQ) document.getElementById("search").value = urlQ;
  let lastFiltered = list;

  function apply() {
    let v = list.slice();
    const snippetMap = new Map();
    if (state.q) {
      const q = state.q.toLowerCase();
      v = v.filter(p => {
        if (String(p.id).includes(q)) return true;
        const blob = p.search || (p.title + " " + (p.tags || []).join(" ")).toLowerCase();
        const idx = blob.indexOf(q);
        if (idx < 0) return false;
        // 抽取上下文片段(标题命中不显示,改为正文片段)
        const titleHit = p.title.toLowerCase().includes(q);
        if (!titleHit) {
          const start = Math.max(0, idx - 30);
          const end = Math.min(blob.length, idx + q.length + 60);
          const before = (start > 0 ? "…" : "") + escapeHtml(blob.slice(start, idx));
          const hit = `<mark>${escapeHtml(blob.slice(idx, idx + q.length))}</mark>`;
          const after = escapeHtml(blob.slice(idx + q.length, end)) + (end < blob.length ? "…" : "");
          snippetMap.set(p.id, before + hit + after);
        }
        return true;
      });
    }
    if (state.diff !== "all") v = v.filter(p => diffClass(p.difficulty) === state.diff);
    if (state.day !== "all")  v = v.filter(p => p.day === Number(state.day));
    if (state.st === "done")  v = v.filter(p => progress.isDone(p.id));
    if (state.st === "todo")  v = v.filter(p => !progress.isDone(p.id));
    lastFiltered = v;
    renderProblemList(document.getElementById("prob-list"), v, snippetMap);
  }

  document.getElementById("random-btn").addEventListener("click", () => {
    const pool = lastFiltered.length ? lastFiltered : list;
    const pick = pool[Math.floor(Math.random() * pool.length)];
    if (pick) location.hash = `#/p/${pick.id}`;
  });

  document.getElementById("search").oninput = e => { state.q = e.target.value; apply(); };
  document.getElementById("filter-diff").addEventListener("click", e => {
    if (!e.target.dataset.diff) return;
    state.diff = e.target.dataset.diff;
    e.currentTarget.querySelectorAll(".pill").forEach(p => p.classList.toggle("active", p === e.target));
    apply();
  });
  document.getElementById("filter-day").addEventListener("click", e => {
    if (!e.target.dataset.day) return;
    state.day = e.target.dataset.day;
    e.currentTarget.querySelectorAll(".pill").forEach(p => p.classList.toggle("active", p === e.target));
    apply();
  });
  document.getElementById("filter-state").addEventListener("click", e => {
    if (!e.target.dataset.state) return;
    state.st = e.target.dataset.state;
    e.currentTarget.querySelectorAll(".pill").forEach(p => p.classList.toggle("active", p === e.target));
    apply();
  });
  apply();
}

function renderProblemList(container, items, snippetMap) {
  if (!items.length) {
    container.innerHTML = `<div class="empty">没有匹配的题目。</div>`;
    return;
  }
  container.innerHTML = "";
  for (const p of items) {
    const done = progress.isDone(p.id);
    const rating = progress.getRating(p.id);
    const snippet = snippetMap && snippetMap.get(p.id);
    const ratingHtml = rating ? `<span class="row-rating" title="自评 ${rating} 星">${"★".repeat(rating)}</span>` : "";
    const row = el(`
      <a class="prob-row ${done ? "done" : ""} ${snippet ? "with-snippet" : ""}" href="#/p/${p.id}">
        <div class="prob-check ${done ? "checked" : ""}" data-id="${p.id}">${SVG_CHECK}</div>
        <div class="prob-num">#${p.id}</div>
        <div class="prob-title-wrap">
          <div class="prob-title">${escapeHtml(p.title)}
            ${p.n_sols >= 2 ? `<span class="star" title="${p.n_sols} 种解法">★ ${p.n_sols} 解法</span>` : ""}
            ${ratingHtml}
          </div>
          ${snippet ? `<div class="prob-snippet">${snippet}</div>` : ""}
        </div>
        <span class="diff ${diffClass(p.difficulty)}">${escapeHtml(p.difficulty)}</span>
        <div class="prob-cat">${escapeHtml(p.category || "")}</div>
        <div class="prob-day">Day ${p.day}</div>
        <div class="prob-practice">${
          p.leetcode_url
            ? `<button class="lc-btn" type="button" data-url="${p.leetcode_url}" title="在 LeetCode 上打开本题">${SVG_EXT}<span>练习</span></button>`
            : ""
        }</div>
      </a>`);
    row.querySelector(".prob-check").addEventListener("click", e => {
      e.preventDefault(); e.stopPropagation();
      const newDone = progress.toggle(p.id);
      row.classList.toggle("done", newDone);
      e.currentTarget.classList.toggle("checked", newDone);
    });
    // 行内的"练习"按钮在新标签打开 LeetCode,不触发整行跳转(避免 <a> 嵌套)
    const lc = row.querySelector(".prob-practice .lc-btn");
    if (lc) lc.addEventListener("click", e => {
      e.preventDefault(); e.stopPropagation();
      window.open(lc.dataset.url, "_blank", "noopener");
    });
    container.appendChild(row);
  }
}

// ===================== Problem Detail =====================
export async function renderProblem(id) {
  id = Number(id);
  const app = document.getElementById("app");
  app.innerHTML = `<div class="loader"></div>`;
  let data, list;
  try {
    [data, list] = await Promise.all([getProblem(id), getProblems()]);
  } catch {
    app.innerHTML = `<div class="container empty">题目 #${id} 不存在。</div>`;
    return;
  }
  const done = progress.isDone(id);
  const sols = data.solutions || [];
  const hasMulti = sols.length >= 2;

  // 上一题 / 下一题(按题单顺序)
  const idx = list.findIndex(p => p.id === id);
  const prev = idx > 0 ? list[idx - 1] : null;
  const next = idx >= 0 && idx < list.length - 1 ? list[idx + 1] : null;
  // 暴露给全局快捷键(J/K 翻题、O 打开 LeetCode)
  window.__lc = {
    prev: prev ? prev.id : null,
    next: next ? next.id : null,
    leetcode: data.leetcode_url || null,
  };

  app.innerHTML = `
    <div class="container">
      <a class="detail-back" href="#/day/${data.day}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
        Day ${data.day} · ${escapeHtml(data.day_title)}
      </a>
      <div class="detail-header">
        <div class="detail-meta">
          <span class="diff ${diffClass(data.difficulty)}">${escapeHtml(data.difficulty)}</span>
          <span class="sep">·</span>
          <span>#${data.id}</span>
          <span class="sep">·</span>
          <span>${escapeHtml(data.category || "")}</span>
        </div>
        <h1>${escapeHtml(data.title)}</h1>
        <div style="display:flex;gap:12px;margin-top:14px;align-items:center;flex-wrap:wrap;">
          ${lcButton(data.leetcode_url, { large: true })}
          <button id="toggle-done" class="prob-check ${done ? "checked" : ""}" style="position:relative;width:auto;height:36px;border-radius:999px;padding:0 16px;font-size:14px;font-weight:600;display:inline-flex;gap:6px;align-items:center;color:${done ? "white" : "var(--text-soft)"};background:${done ? "var(--accent)" : "var(--bg-elev)"};border:1px solid ${done ? "var(--accent)" : "var(--border)"}">${SVG_CHECK} <span>${done ? "已完成" : "标记完成"}</span></button>
        </div>
        <p style="margin:12px 0 0;font-size:12.5px;color:var(--text-mute)">
          💡 建议:先在本页读懂思路,再点「去 LeetCode 练习」盖住代码独立默写。第一次用 LeetCode?看 <a href="#/guide">练习指南 →</a>
        </p>
      </div>
      <div class="detail-layout">
        <article id="detail-main">
          ${data.statement ? `
          <section class="detail-section statement-section" id="sec-statement">
            <h2>📋 题目描述 <span class="badge">完整题面</span></h2>
            ${renderStatement(data.statement)}
          </section>` : ""}
          <section class="detail-section" id="sec-doc">
            <h2>💡 思路 & 直觉</h2>
            <div class="md">${renderDoc(data.doc)}</div>
          </section>
          ${data.viz ? `
          <section class="detail-section" id="sec-viz">
            <h2>可视化 <span class="badge">${escapeHtml(data.viz.label || data.viz.type)}</span></h2>
            <div class="viz-wrap">${renderViz(data.viz)}</div>
          </section>` : ""}
          ${data.explanation ? (() => {
            const longDefault = location.search.includes("expl=long");
            return `
          <section class="detail-section" id="sec-expl">
            <h2>💡 解题思路
              <span class="seg-toggle" id="expl-toggle" role="tablist">
                <button class="seg-btn ${longDefault ? "" : "active"}" data-mode="short">简洁</button>
                <button class="seg-btn ${longDefault ? "active" : ""}" data-mode="long">详细</button>
              </span>
            </h2>
            <div class="md expl-block ${longDefault ? "hidden" : ""}" id="expl-short">${
              data.explanation.short ? `<p class="lead-line">${escInlineMd(data.explanation.short)}</p>` : ""
            }</div>
            <div class="md expl-block ${longDefault ? "" : "hidden"}" id="expl-long">${
              Array.isArray(data.explanation.long)
                ? data.explanation.long.map(p => `<p>${escInlineMd(p)}</p>`).join("")
                : (data.explanation.long ? `<p>${escInlineMd(data.explanation.long)}</p>` : "")
            }</div>
          </section>`;})() : ""}
          ${data.explanation && data.explanation.complexity ? `
          <section class="detail-section" id="sec-complexity">
            <h2>🧮 复杂度推导</h2>
            <div class="complexity-grid">
              <div class="cx-card">
                <div class="cx-label">时间复杂度</div>
                <div class="md">${data.explanation.complexity.time ? `<p>${escInlineMd(data.explanation.complexity.time)}</p>` : ""}</div>
              </div>
              <div class="cx-card">
                <div class="cx-label">空间复杂度</div>
                <div class="md">${data.explanation.complexity.space ? `<p>${escInlineMd(data.explanation.complexity.space)}</p>` : ""}</div>
              </div>
            </div>
          </section>` : ""}
          ${hasMulti ? `
          <section class="detail-section" id="sec-solutions">
            <h2>多解法对比 <span class="badge">${sols.length} 种</span></h2>
            <p class="sol-tip">每种解法都是 LeetCode 可直接提交的完整 <code>class Solution</code>,点「复制」即可粘贴提交。</p>
            <div class="sol-tabs" id="sol-tabs">
              ${sols.map((s, i) => `
                <button class="sol-tab ${i === pickStarIdx(sols) ? "active" : ""}" data-i="${i}">
                  ${s.starred ? '<span class="star">★</span>' : ""}<span>${escapeHtml(s.title)}</span>
                </button>
              `).join("")}
            </div>
            <div id="sol-panels">
              ${sols.map((s, i) => `
                <div class="sol-content ${i === pickStarIdx(sols) ? "active" : ""}" data-i="${i}">
                  <div class="sol-meta">
                    ${s.time  ? `<span class="chip"><strong>时间</strong>${escapeHtml(s.time)}</span>` : ""}
                    ${s.space ? `<span class="chip"><strong>空间</strong>${escapeHtml(s.space)}</span>` : ""}
                    ${s.starred ? `<span class="chip" style="background:var(--accent-soft);color:var(--accent)"><strong>★</strong>面试首选</span>` : ""}
                  </div>
                  ${codeBlock(s.code, "python")}
                </div>
              `).join("")}
            </div>
          </section>` : `
          <section class="detail-section" id="sec-solution">
            <h2>解法</h2>
            ${sols[0] ? `
              <p class="sol-tip">这是 LeetCode 可直接提交的完整代码,点「复制」即可粘贴提交。</p>`: ""}
            ${sols[0] ? `
              <div class="sol-meta">
                ${sols[0].time  ? `<span class="chip"><strong>时间</strong>${escapeHtml(sols[0].time)}</span>` : ""}
                ${sols[0].space ? `<span class="chip"><strong>空间</strong>${escapeHtml(sols[0].space)}</span>` : ""}
              </div>
              ${codeBlock(sols[0].code, "python")}` : `<p class="md">本题暂无可提交代码。</p>`}
          </section>`}
          ${data.code_explain ? `
          <section class="detail-section" id="sec-walk">
            <h2>📖 代码讲解 <span class="badge">逐行</span></h2>
            <p class="sol-tip">下面是 ★ 首选解法的<strong>逐行中文注释版</strong>,帮你看懂每一行在做什么;提交时请用上面「解法」里的干净代码。</p>
            ${codeBlock(data.code_explain.annotated, "python")}
            ${(data.code_explain.gotchas && data.code_explain.gotchas.length) ? `
            <div class="gotchas">
              <div class="gotchas-title">⚠️ 注意点 / 易错点</div>
              <ul>${data.code_explain.gotchas.map(g => `<li>${escInlineMd(g)}</li>`).join("")}</ul>
            </div>` : ""}
          </section>` : ""}
          <section class="detail-section" id="sec-personal">
            <h2>📝 我的笔记 & 难度自评</h2>
            <div class="personal-grid">
              <div class="rating-card">
                <div class="cx-label">难度自评(对你而言)</div>
                <div class="rating-stars" id="rating-stars" data-current="${progress.getRating(id)}">
                  ${[1,2,3,4,5].map(n => `<button class="star-btn" data-val="${n}" aria-label="${n} 星">★</button>`).join("")}
                  <button class="star-clear" id="rating-clear" title="清除评分">×</button>
                </div>
                <div class="rating-hint">1=随手 / 2=轻松 / 3=中等 / 4=费劲 / 5=Hard 待复习</div>
              </div>
              <div class="note-card">
                <div class="cx-label">我的笔记 <span style="float:right;color:var(--text-mute);font-weight:400;font-size:11px" id="note-status"></span></div>
                <textarea id="note-area" placeholder="写下错题、思路卡点、复习计划… 自动保存到本机浏览器。">${escapeHtml(progress.getNote(id))}</textarea>
              </div>
            </div>
          </section>
        </article>
        <aside class="toc">
          <div class="toc-title">本页目录</div>
          <ol>
            ${data.statement ? `<li><a href="#sec-statement">📋 题目描述</a></li>` : ""}
            <li><a href="#sec-doc">💡 思路 & 直觉</a></li>
            ${data.viz ? `<li><a href="#sec-viz">可视化</a></li>` : ""}
            ${data.explanation ? `<li><a href="#sec-expl">💡 解题思路</a></li>` : ""}
            ${data.explanation && data.explanation.complexity ? `<li><a href="#sec-complexity">🧮 复杂度推导</a></li>` : ""}
            ${hasMulti ? `<li><a href="#sec-solutions">多解法对比</a></li>` : `<li><a href="#sec-solution">解法</a></li>`}
            ${data.code_explain ? `<li><a href="#sec-walk">📖 代码讲解</a></li>` : ""}
            <li><a href="#sec-personal">📝 笔记 & 自评</a></li>
          </ol>
        </aside>
      </div>
      <nav class="prob-nav">
        ${prev
          ? `<a class="prev" href="#/p/${prev.id}"><span class="nav-dir">← 上一题 · #${prev.id}</span><span class="nav-title">${escapeHtml(prev.title)}</span></a>`
          : `<span class="prev nav-empty"></span>`}
        ${next
          ? `<a class="next" href="#/p/${next.id}"><span class="nav-dir">下一题 · #${next.id} →</span><span class="nav-title">${escapeHtml(next.title)}</span></a>`
          : `<span class="next nav-empty"></span>`}
      </nav>
    </div>`;

  // 难度自评 & 笔记
  const stars = document.getElementById("rating-stars");
  if (stars) {
    function paint(cur) {
      stars.dataset.current = cur;
      [...stars.querySelectorAll(".star-btn")].forEach(b => {
        b.classList.toggle("filled", Number(b.dataset.val) <= cur);
      });
    }
    paint(progress.getRating(id));
    stars.addEventListener("click", e => {
      if (e.target.classList.contains("star-btn")) {
        const v = Number(e.target.dataset.val);
        progress.setRating(id, v);
        paint(v);
      }
      if (e.target.id === "rating-clear") {
        progress.setRating(id, 0);
        paint(0);
      }
    });
  }
  const note = document.getElementById("note-area");
  const noteStatus = document.getElementById("note-status");
  if (note) {
    let timer;
    note.addEventListener("input", () => {
      if (noteStatus) noteStatus.textContent = "正在保存…";
      clearTimeout(timer);
      timer = setTimeout(() => {
        progress.setNote(id, note.value);
        if (noteStatus) {
          noteStatus.textContent = "已保存 ✓";
          setTimeout(() => noteStatus.textContent = "", 1200);
        }
      }, 350);
    });
  }

  // 解题思路 简洁/详细 切换
  const explToggle = document.getElementById("expl-toggle");
  if (explToggle) {
    explToggle.addEventListener("click", e => {
      const mode = e.target.dataset.mode;
      if (!mode) return;
      explToggle.querySelectorAll(".seg-btn").forEach(b =>
        b.classList.toggle("active", b === e.target));
      document.getElementById("expl-short").classList.toggle("hidden", mode !== "short");
      document.getElementById("expl-long").classList.toggle("hidden", mode !== "long");
    });
  }

  // Solution tab switching
  const tabs = document.querySelectorAll(".sol-tab");
  const panels = document.querySelectorAll(".sol-content");
  tabs.forEach(t => t.addEventListener("click", () => {
    tabs.forEach(x => x.classList.remove("active"));
    panels.forEach(x => x.classList.remove("active"));
    t.classList.add("active");
    document.querySelector(`.sol-content[data-i="${t.dataset.i}"]`).classList.add("active");
    highlightAll();
  }));

  // Toggle done
  document.getElementById("toggle-done").addEventListener("click", () => {
    const newDone = progress.toggle(id);
    const btn = document.getElementById("toggle-done");
    btn.classList.toggle("checked", newDone);
    btn.style.background = newDone ? "var(--accent)" : "var(--bg-elev)";
    btn.style.color = newDone ? "white" : "var(--text-soft)";
    btn.querySelector("span").textContent = newDone ? "已完成" : "标记完成";
  });

  // Code copy
  document.querySelectorAll(".copy-btn").forEach(b => {
    b.addEventListener("click", () => {
      const code = b.closest(".code-block").querySelector("pre.code").innerText;
      navigator.clipboard.writeText(code);
      b.querySelector("span").textContent = "已复制";
      setTimeout(() => b.querySelector("span").textContent = "复制", 1200);
    });
  });

  highlightAll();
}

function pickStarIdx(sols) {
  const idx = sols.findIndex(s => s.starred);
  return idx >= 0 ? idx : Math.max(0, sols.length - 1);
}

function codeBlock(code, lang = "python", collapse = false) {
  const escaped = escapeHtml(code);
  return `
    <div class="code-block">
      <div class="code-toolbar">
        <span>${lang}</span>
        <button class="copy-btn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg> <span>复制</span></button>
      </div>
      <pre class="code"><code class="language-${lang}">${escaped}</code></pre>
    </div>`;
}

function highlightAll() {
  if (window.hljs) {
    document.querySelectorAll("pre.code code").forEach(b => {
      window.hljs.highlightElement(b);
    });
  }
}

// ===================== Progress Page =====================
export async function renderProgress() {
  const app = document.getElementById("app");
  const [list, days] = await Promise.all([getProblems(), getDays()]);
  const total = list.length;
  const doneCount = list.reduce((acc, p) => acc + (progress.isDone(p.id) ? 1 : 0), 0);
  const overall = total ? Math.round(doneCount / total * 100) : 0;

  // by difficulty
  const groups = { Easy: [], Medium: [], Hard: [] };
  list.forEach(p => {
    const k = p.difficulty.startsWith("E") ? "Easy" :
              p.difficulty.startsWith("H") ? "Hard" : "Medium";
    groups[k].push(p);
  });

  const dayCards = Object.values(days).map(d => {
    const cnt = progress.countDoneIn(d.problem_ids);
    const pct = d.problem_ids.length ? Math.round(cnt / d.problem_ids.length * 100) : 0;
    return `<div class="progress-card">
      <h4>Day ${d.day} · ${escapeHtml(d.title)}</h4>
      <div class="pct">${pct}%</div>
      <div class="frac">${cnt} / ${d.problem_ids.length}</div>
      <div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>
    </div>`;
  }).join("");

  const diffCards = Object.entries(groups).map(([k, ps]) => {
    const cnt = ps.reduce((a, p) => a + (progress.isDone(p.id) ? 1 : 0), 0);
    const pct = ps.length ? Math.round(cnt / ps.length * 100) : 0;
    return `<div class="progress-card">
      <h4>${k}</h4>
      <div class="pct">${pct}%</div>
      <div class="frac">${cnt} / ${ps.length}</div>
      <div class="progress-bar"><div class="progress-fill" style="width:${pct}%;background:var(--${diffClass(k)})"></div></div>
    </div>`;
  }).join("");

  app.innerHTML = `
    <div class="container">
      <div class="hero">
        <h1>我的进度</h1>
        <p class="lead">数据保存在本机浏览器(localStorage),清浏览器数据会重置。</p>
        <div class="hero-stats">
          <div class="stat"><span class="num accent">${overall}%</span><span class="label">总完成度</span></div>
          <div class="stat"><span class="num">${doneCount}</span><span class="label">已完成</span></div>
          <div class="stat"><span class="num">${total - doneCount}</span><span class="label">剩余</span></div>
        </div>
      </div>
      <h2 class="section-title">按 Day</h2>
      <div class="progress-grid">${dayCards}</div>
      <h2 class="section-title">按难度</h2>
      <div class="progress-grid">${diffCards}</div>
      <h2 class="section-title">我的难度自评分布</h2>
      <div class="rating-dist" id="rating-dist"></div>
      <div style="margin:48px 0;display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
        <button class="pill" id="export-btn">📦 导出进度 JSON</button>
        <button class="pill" id="import-btn">📥 导入进度 JSON</button>
        <input type="file" id="import-file" accept="application/json" style="display:none">
        <button class="pill" id="reset-btn" style="color:var(--hard);border-color:var(--hard)">⚠ 重置全部进度</button>
      </div>
    </div>`;

  // 评分分布柱状图
  const dist = progress.ratingDistribution();      // [unrated, ★, ★★, ★★★, ★★★★, ★★★★★]
  const distEl = document.getElementById("rating-dist");
  const maxN = Math.max(1, ...dist.slice(1));
  distEl.innerHTML = [1, 2, 3, 4, 5].map(r => {
    const n = dist[r];
    const pct = Math.round(n / maxN * 100);
    return `
      <div class="dist-row">
        <div class="dist-label">${"★".repeat(r)}<span class="dist-faint">${"★".repeat(5 - r)}</span></div>
        <div class="dist-bar"><div class="dist-fill" style="width:${pct}%"></div></div>
        <div class="dist-count">${n}</div>
      </div>`;
  }).join("");

  document.getElementById("reset-btn").addEventListener("click", () => {
    if (confirm("确定要重置全部进度(完成 / 评分 / 笔记)?此操作不可撤销。")) {
      progress.reset();
      renderProgress();
    }
  });
  document.getElementById("export-btn").addEventListener("click", () => {
    const blob = new Blob([progress.export()], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `lc100-progress-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  document.getElementById("import-btn").addEventListener("click", () => {
    document.getElementById("import-file").click();
  });
  document.getElementById("import-file").addEventListener("change", e => {
    const f = e.target.files[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = ev => {
      try {
        progress.import(ev.target.result);
        alert("✅ 导入成功!");
        renderProgress();
      } catch (err) {
        alert("❌ 导入失败:" + err.message);
      }
    };
    reader.readAsText(f);
  });
}

// ===================== Pattern (Markdown) =====================
export async function renderPattern(slug) {
  const app = document.getElementById("app");
  app.innerHTML = `<div class="loader"></div>`;
  try {
    const md = await getPattern(`${slug}.md`);
    app.innerHTML = `
      <div class="container">
        <a class="detail-back" href="#/">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
          返回首页
        </a>
        <article class="md" style="margin-top:32px">${renderMarkdown(md)}</article>
      </div>`;
    if (window.hljs) document.querySelectorAll("pre.code code").forEach(b => window.hljs.highlightElement(b));
  } catch {
    app.innerHTML = `<div class="container empty">未找到 pattern: ${slug}</div>`;
  }
}

// ===================== Guide (LeetCode 新手练习指南) =====================
export function renderGuide() {
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="container guide">
      <div class="hero">
        <h1>如何在 LeetCode 上练习 Hot 100</h1>
        <p class="lead">第一次用 LeetCode?跟着这份指南走一遍。本站负责讲透思路,LeetCode 负责真实判题——
          两者配合,效率最高。建议用 <strong>leetcode.cn(中国版,中文题面、国内访问快)</strong>。</p>
      </div>

      <section class="detail-section">
        <h2>① 注册 & 基础设置(5 分钟,一次性)</h2>
        <ol class="guide-list">
          <li>打开 <a href="https://leetcode.cn/" target="_blank" rel="noopener">leetcode.cn ↗</a>,用手机号 / 微信注册登录。</li>
          <li>进入任意一题,右上角语言选择器把默认语言设为 <span class="kbd">Python3</span>(本站题解都是 Python)。</li>
          <li>右上角头像 → 设置里可开启<strong>暗色主题</strong>、调字号,和本站对照看更舒服。</li>
        </ol>
      </section>

      <section class="detail-section">
        <h2>② 一道题的完整练习流程</h2>
        <p class="guide-p">这是本项目期望你养成的核心循环。每题都这样走一遍:</p>
        <div class="guide-steps">
          <div class="guide-step"><span class="gs-num">1</span><div><strong>在本站读懂</strong><p>看「题面 → 直觉 → 复杂度 → 多解法」,先把<em>为什么这么做</em>想明白,别急着背代码。</p></div></div>
          <div class="guide-step"><span class="gs-num">2</span><div><strong>点「去 LeetCode 练习」</strong><p>每道题详情页右上、列表每行右侧都有橙色按钮,新标签打开对应原题。</p></div></div>
          <div class="guide-step"><span class="gs-num">3</span><div><strong>盖住答案独立写</strong><p>在 LeetCode 代码框里凭理解默写。卡住了再回本站瞄一眼关键句,而不是整段抄。</p></div></div>
          <div class="guide-step"><span class="gs-num">4</span><div><strong>Run Code 先自测</strong><p>点「执行代码 / Run」用样例跑一遍,看输出对不对、有没有报错。这一步不计入提交。</p></div></div>
          <div class="guide-step"><span class="gs-num">5</span><div><strong>Submit 提交判题</strong><p>点「提交 / Submit」跑全部隐藏测试。通过(Accepted)后会显示击败百分比 (Runtime / Memory)。</p></div></div>
          <div class="guide-step"><span class="gs-num">6</span><div><strong>回本站标记 & 记笔记</strong><p>回到本题点「标记完成」,做 1–5 星难度自评,把卡点写进笔记区——这些都存在你本机浏览器里。</p></div></div>
        </div>
      </section>

      <section class="detail-section">
        <h2>③ 看懂 LeetCode 的判题结果</h2>
        <ul class="guide-list">
          <li><strong style="color:var(--easy)">Accepted</strong>:通过全部用例,搞定。看一眼 Runtime/Memory 击败比例即可,不必追求 100%。</li>
          <li><strong style="color:var(--hard)">Wrong Answer</strong>:逻辑错。它会给出<em>出错的那个输入</em>和你的输出 vs 期望输出,照着这个最小用例 debug。</li>
          <li><strong style="color:var(--hard)">Time Limit Exceeded (TLE)</strong>:思路对但太慢,说明复杂度不达标——回本站看「面试首选 ★」那版更优解法。</li>
          <li><strong style="color:var(--hard)">Runtime Error</strong>:崩了,通常是越界 / 空指针 / 除零。看报错行号。</li>
          <li>卡住超过 20–30 分钟很正常,直接回本站看详解,理解后<strong>第二天再裸写一遍</strong>,比硬磕更高效。</li>
        </ul>
      </section>

      <section class="detail-section">
        <h2>④ 高效练习的几个习惯</h2>
        <ul class="guide-list">
          <li>📅 <strong>按本站 7 天计划推进</strong>:每个 Day 是一个题型簇,集中练同一类手感更扎实。</li>
          <li>🔁 <strong>错题二刷</strong>:自评 4–5 星的题用「进度」页找出来,隔几天重做,直到能裸写。</li>
          <li>⏱️ <strong>限时</strong>:Easy 10 分钟、Medium 20–25 分钟还没思路就看解,不要干耗。</li>
          <li>🧠 <strong>先讲再写</strong>:能用一句话说清「这题用什么 + 为什么」,再动手写代码。</li>
          <li>💾 <strong>定期导出进度</strong>:进度页可导出 JSON,换设备 / 清缓存前备份。</li>
        </ul>
      </section>

      <section class="detail-section">
        <h2>⑤ 本站快捷键</h2>
        <div class="kbd-grid">
          <div><span class="kbd">/</span> 跳到全部题目并聚焦搜索</div>
          <div><span class="kbd">←</span> <span class="kbd">→</span> 详情页上一题 / 下一题</div>
          <div><span class="kbd">O</span> 在 LeetCode 打开当前题</div>
          <div><span class="kbd">D</span> 切换暗 / 亮主题</div>
          <div><span class="kbd">Esc</span> 返回首页</div>
        </div>
        <p class="guide-p" style="margin-top:24px">
          准备好了?<a href="#/list">→ 去全部题目</a> 或 <a href="#/day/1">从 Day 1 开始</a>。
        </p>
      </section>
    </div>`;
}

// ===================== About =====================
export function renderAbout() {
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="container">
      <div class="hero">
        <h1>关于 LC100</h1>
        <p class="lead">这是一个面向面试的 LeetCode Hot 100 全题解项目,Python 实现。所有题目自带单元测试通过,
          多解法题给出 2–4 种解法的复杂度对比。</p>
      </div>
      <section>
        <h2 class="section-title">项目特性</h2>
        <ul class="md" style="font-size:15px;line-height:2">
          <li>✅ 100 题全覆盖,严格按官方 Hot 100 + 灵神分类</li>
          <li>✅ 多解法对比:暴力 → 优化 → 最优,展示思路演进</li>
          <li>✅ 中文详解 + 复杂度速查 + 踩坑提醒</li>
          <li>✅ ASCII 可视化(链表/二叉树/滑动窗口)</li>
          <li>✅ 进度追踪(localStorage)</li>
          <li>✅ 7 张模式速记表,把 100 题压成 7 张图</li>
          <li>✅ 暗色模式 / 全文搜索 / 移动端响应式</li>
        </ul>
        <h2 class="section-title">本地运行</h2>
        <pre class="code"><code class="language-bash">git clone https://github.com/&lt;your&gt;/lc100.git
cd lc100
python3 -m http.server 8000   # 任意静态服务即可
open http://localhost:8000</code></pre>
        <h2 class="section-title">部署到 GitHub Pages</h2>
        <pre class="code"><code class="language-bash">git init && git add . && git commit -m "init"
gh repo create lc100 --public --source=. --push
# 然后在 Settings → Pages 选择 main 分支根目录,几分钟内访问:
# https://&lt;username&gt;.github.io/lc100/</code></pre>
      </section>
    </div>`;
}
