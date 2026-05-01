// localStorage-backed progress tracking.
const KEY = "lc100.progress.v1";

function load() {
  try {
    return JSON.parse(localStorage.getItem(KEY) || "{}");
  } catch {
    return {};
  }
}

function save(state) {
  localStorage.setItem(KEY, JSON.stringify(state));
}

export const progress = {
  isDone(id) { return !!load()[id]; },
  setDone(id, done) {
    const s = load();
    if (done) s[id] = Date.now();
    else delete s[id];
    save(s);
  },
  toggle(id) {
    const s = load();
    if (s[id]) delete s[id];
    else s[id] = Date.now();
    save(s);
    return !!s[id];
  },
  all() { return load(); },
  countDoneIn(ids) {
    const s = load();
    return ids.reduce((acc, id) => acc + (s[id] ? 1 : 0), 0);
  },
  reset() { localStorage.removeItem(KEY); },
};
