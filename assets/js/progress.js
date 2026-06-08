// localStorage-backed progress tracking.
// 三类数据共存:done(完成时间戳)/ rating(1-5 难度自评)/ note(笔记文本)
const KEY = "lc100.progress.v2";
const LEGACY_KEY = "lc100.progress.v1";    // 旧版仅 done 状态

// 内存缓存:避免每次读写都 JSON.parse 整个进度对象。
// 列表页一次渲染会对 100 题各查 done/rating,缓存后从 O(题数) 次 parse 降到 1 次。
let _cache = null;

function load() {
  if (_cache) return _cache;
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) return (_cache = JSON.parse(raw));
    // v1 -> v2 迁移
    const old = localStorage.getItem(LEGACY_KEY);
    if (old) {
      const parsed = JSON.parse(old);
      const upgraded = {};
      for (const [k, v] of Object.entries(parsed)) {
        upgraded[k] = { done: v, rating: 0, note: "" };
      }
      localStorage.setItem(KEY, JSON.stringify(upgraded));
      return (_cache = upgraded);
    }
    return (_cache = {});
  } catch {
    return (_cache = {});
  }
}

function save(state) {
  _cache = state;
  localStorage.setItem(KEY, JSON.stringify(state));
}

// 其他标签页修改进度时让本页缓存失效,保持跨标签一致。
window.addEventListener("storage", e => {
  if (e.key === KEY || e.key === LEGACY_KEY) _cache = null;
});

function entry(s, id) {
  if (!s[id]) s[id] = { done: 0, rating: 0, note: "" };
  return s[id];
}

export const progress = {
  // ---- 完成 ----
  isDone(id) { const s = load()[id]; return !!(s && s.done); },
  setDone(id, done) {
    const s = load();
    entry(s, id).done = done ? Date.now() : 0;
    save(s);
  },
  toggle(id) {
    const s = load();
    const e = entry(s, id);
    e.done = e.done ? 0 : Date.now();
    save(s);
    return !!e.done;
  },

  // ---- 评分(1-5;0 = 未评)----
  getRating(id) { const e = load()[id]; return e ? (e.rating || 0) : 0; },
  setRating(id, r) {
    const s = load();
    entry(s, id).rating = r;
    save(s);
  },

  // ---- 笔记 ----
  getNote(id) { const e = load()[id]; return e ? (e.note || "") : ""; },
  setNote(id, text) {
    const s = load();
    entry(s, id).note = text;
    save(s);
  },

  // ---- 聚合 ----
  all() { return load(); },
  countDoneIn(ids) {
    const s = load();
    return ids.reduce((acc, id) => acc + (s[id] && s[id].done ? 1 : 0), 0);
  },
  ratingDistribution() {
    const s = load();
    const dist = [0, 0, 0, 0, 0, 0];
    for (const e of Object.values(s)) {
      dist[(e && e.rating) || 0]++;
    }
    return dist;       // dist[0] = 未评,dist[1..5] = 各档
  },

  // ---- 导出 / 导入 ----
  export() {
    return JSON.stringify({
      version: 2,
      exportedAt: new Date().toISOString(),
      data: load(),
    }, null, 2);
  },
  import(text) {
    const obj = JSON.parse(text);
    if (!obj || !obj.data) throw new Error("Invalid format");
    save(obj.data);
  },

  reset() {
    _cache = null;
    localStorage.removeItem(KEY);
    localStorage.removeItem(LEGACY_KEY);
  },
};
