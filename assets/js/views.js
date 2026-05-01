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

function diffClass(d) {
  d = (d || "").toLowerCase();
  if (d.startsWith("e")) return "easy";
  if (d.startsWith("h")) return "hard";
  return "medium";
}

const SVG_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';

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
        点击任意一题查看详解;每题包含<strong>题面 → 直觉 → 多种解法对比 → 复杂度 → 踩坑 → 同类变体</strong>。
        进度自动保存在浏览器 localStorage,清浏览器数据会重置。
        快捷键:<span class="kbd">/</span> 聚焦搜索,<span class="kbd">D</span> 切换暗色,<span class="kbd">Esc</span> 返回首页。
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
      </div>
      <div class="prob-list" id="prob-list"></div>
    </div>`;

  const state = { q: "", diff: "all", day: "all", st: "all" };

  function apply() {
    let v = list.slice();
    if (state.q) {
      const q = state.q.toLowerCase();
      v = v.filter(p =>
        String(p.id).includes(q) ||
        p.title.toLowerCase().includes(q) ||
        (p.tags || []).some(t => t.toLowerCase().includes(q)) ||
        (p.category || "").toLowerCase().includes(q)
      );
    }
    if (state.diff !== "all") v = v.filter(p => diffClass(p.difficulty) === state.diff);
    if (state.day !== "all")  v = v.filter(p => p.day === Number(state.day));
    if (state.st === "done")  v = v.filter(p => progress.isDone(p.id));
    if (state.st === "todo")  v = v.filter(p => !progress.isDone(p.id));
    renderProblemList(document.getElementById("prob-list"), v);
  }

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

function renderProblemList(container, items) {
  if (!items.length) {
    container.innerHTML = `<div class="empty">没有匹配的题目。</div>`;
    return;
  }
  container.innerHTML = "";
  for (const p of items) {
    const done = progress.isDone(p.id);
    const row = el(`
      <a class="prob-row ${done ? "done" : ""}" href="#/p/${p.id}">
        <div class="prob-check ${done ? "checked" : ""}" data-id="${p.id}">${SVG_CHECK}</div>
        <div class="prob-num">#${p.id}</div>
        <div class="prob-title">${escapeHtml(p.title)} ${p.n_sols >= 2 ? `<span class="star" title="${p.n_sols} 种解法">★ ${p.n_sols} 解法</span>` : ""}</div>
        <span class="diff ${diffClass(p.difficulty)}">${escapeHtml(p.difficulty)}</span>
        <div class="prob-cat">${escapeHtml(p.category || "")}</div>
        <div class="prob-day">Day ${p.day}</div>
      </a>`);
    row.querySelector(".prob-check").addEventListener("click", e => {
      e.preventDefault(); e.stopPropagation();
      const newDone = progress.toggle(p.id);
      row.classList.toggle("done", newDone);
      e.currentTarget.classList.toggle("checked", newDone);
    });
    container.appendChild(row);
  }
}

// ===================== Problem Detail =====================
export async function renderProblem(id) {
  id = Number(id);
  const app = document.getElementById("app");
  app.innerHTML = `<div class="loader"></div>`;
  let data;
  try {
    data = await getProblem(id);
  } catch {
    app.innerHTML = `<div class="container empty">题目 #${id} 不存在。</div>`;
    return;
  }
  const done = progress.isDone(id);
  const sols = data.solutions || [];
  const hasMulti = sols.length >= 2;

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
          <span class="sep">·</span>
          <a href="${data.leetcode_url}" target="_blank" rel="noopener">LeetCode 原题 ↗</a>
        </div>
        <h1>${escapeHtml(data.title)}</h1>
        <div style="display:flex;gap:12px;margin-top:14px;align-items:center;">
          <button id="toggle-done" class="prob-check ${done ? "checked" : ""}" style="position:relative;width:auto;height:34px;border-radius:6px;padding:0 12px;font-size:13px;font-weight:500;display:inline-flex;gap:6px;color:${done ? "white" : "var(--text-soft)"};background:${done ? "var(--accent)" : "var(--bg-elev)"}">${SVG_CHECK} <span>${done ? "已完成" : "标记完成"}</span></button>
        </div>
      </div>
      <div class="detail-layout">
        <article id="detail-main">
          <section class="detail-section" id="sec-doc">
            <h2>题面 & 直觉</h2>
            <div class="md">${renderDoc(data.doc)}</div>
          </section>
          ${data.viz ? `
          <section class="detail-section" id="sec-viz">
            <h2>可视化 <span class="badge">${escapeHtml(data.viz.label || data.viz.type)}</span></h2>
            <div class="viz-wrap">${renderViz(data.viz)}</div>
          </section>` : ""}
          ${hasMulti ? `
          <section class="detail-section" id="sec-solutions">
            <h2>多解法对比 <span class="badge">${sols.length} 种</span></h2>
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
              <div class="sol-meta">
                ${sols[0].time  ? `<span class="chip"><strong>时间</strong>${escapeHtml(sols[0].time)}</span>` : ""}
                ${sols[0].space ? `<span class="chip"><strong>空间</strong>${escapeHtml(sols[0].space)}</span>` : ""}
              </div>
              ${codeBlock(sols[0].code, "python")}` : `<p class="md">题目可能为类设计题(如 LRU/MinStack 等),完整源码见下方。</p>`}
          </section>`}
          <section class="detail-section" id="sec-source">
            <h2>完整源码 <span class="badge">${escapeHtml(data.filename)}</span></h2>
            ${codeBlock(data.raw_source, "python", true)}
          </section>
        </article>
        <aside class="toc">
          <div class="toc-title">本页目录</div>
          <ol>
            <li><a href="#sec-doc">题面 & 直觉</a></li>
            ${data.viz ? `<li><a href="#sec-viz">可视化</a></li>` : ""}
            ${hasMulti ? `<li><a href="#sec-solutions">多解法对比</a></li>` : `<li><a href="#sec-solution">解法</a></li>`}
            <li><a href="#sec-source">完整源码</a></li>
          </ol>
        </aside>
      </div>
    </div>`;

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
      <div style="margin:48px 0;text-align:center">
        <button class="pill" id="reset-btn">重置全部进度</button>
      </div>
    </div>`;

  document.getElementById("reset-btn").addEventListener("click", () => {
    if (confirm("确定要重置全部进度?此操作不可撤销。")) {
      progress.reset();
      renderProgress();
    }
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
