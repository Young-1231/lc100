// Entry point.
import { on, start, go } from "./router.js";
import {
  renderHome, renderDay, renderAll, renderProblem,
  renderProgress, renderPattern, renderAbout, renderGuide,
} from "./views.js";

// ===== Theme =====
const THEME_KEY = "lc100.theme";
function applyTheme(t) {
  document.documentElement.setAttribute("data-theme", t);
  document.getElementById("hl-light").disabled = (t === "dark");
  document.getElementById("hl-dark").disabled  = (t !== "dark");
  document.getElementById("icon-sun").style.display  = (t === "dark") ? "" : "none";
  document.getElementById("icon-moon").style.display = (t === "dark") ? "none" : "";
}
function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  const prefer = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  applyTheme(saved || prefer);
}
document.getElementById("theme-toggle").addEventListener("click", () => {
  const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
  localStorage.setItem(THEME_KEY, next);
  applyTheme(next);
});
initTheme();

// ===== Nav =====
const NAV = [
  { path: "#/",          label: "首页"     },
  { path: "#/list",      label: "全部题目" },
  { path: "#/day/1",     label: "7 天计划" },
  { path: "#/guide",     label: "练习指南" },
  { path: "#/progress",  label: "进度"     },
  { path: "#/about",     label: "关于"     },
];
const navEl = document.getElementById("nav");
navEl.innerHTML = NAV.map(n => `<a href="${n.path}">${n.label}</a>`).join("");

function updateActiveNav() {
  const cur = location.hash || "#/";
  navEl.querySelectorAll("a").forEach(a => {
    const matched =
      (a.getAttribute("href") === "#/" && cur === "#/") ||
      (a.getAttribute("href") !== "#/" && cur.startsWith(a.getAttribute("href").split("/").slice(0, 3).join("/")));
    a.classList.toggle("active", matched);
  });
}
window.addEventListener("hashchange", updateActiveNav);
setTimeout(updateActiveNav, 50);

// ===== Routes =====
on(/^#\/$/,                 renderHome);
on(/^#\/list$/,             renderAll);
on(/^#\/day\/(\d+)$/,       renderDay);
on(/^#\/p\/(\d+)$/,         renderProblem);
on(/^#\/progress$/,         renderProgress);
on(/^#\/pattern\/(.+)$/,    renderPattern);
on(/^#\/guide$/,            renderGuide);
on(/^#\/about$/,            renderAbout);
on(/^#\/404$/,              () => {
  document.getElementById("app").innerHTML = `
    <div class="container empty">
      <h2>404</h2>
      <p>页面不存在。<a href="#/">返回首页</a></p>
    </div>`;
});

// Default fallback
window.addEventListener("hashchange", () => {
  setTimeout(updateActiveNav, 0);
});

start();

// ===== Hotkeys =====
document.addEventListener("keydown", e => {
  // Ignore when typing in inputs
  if (e.target.matches("input, textarea")) {
    if (e.key === "Escape") e.target.blur();
    return;
  }
  if (e.key === "/") {
    const inp = document.getElementById("search");
    if (inp) { inp.focus(); e.preventDefault(); return; }
    go("/list");
    setTimeout(() => document.getElementById("search")?.focus(), 100);
    e.preventDefault();
  }
  if (e.key === "d" || e.key === "D") {
    document.getElementById("theme-toggle").click();
  }
  if (e.key === "Escape") {
    if (location.hash !== "#/") go("/");
  }
  // 题目详情页:← / → 翻题,O 打开 LeetCode 原题
  if (location.hash.startsWith("#/p/") && window.__lc) {
    if (e.key === "ArrowLeft" && window.__lc.prev) {
      go(`/p/${window.__lc.prev}`); e.preventDefault();
    }
    if (e.key === "ArrowRight" && window.__lc.next) {
      go(`/p/${window.__lc.next}`); e.preventDefault();
    }
    if ((e.key === "o" || e.key === "O") && window.__lc.leetcode) {
      window.open(window.__lc.leetcode, "_blank", "noopener");
    }
  }
});
