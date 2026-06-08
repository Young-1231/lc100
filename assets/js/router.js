// Tiny hash router.

const handlers = [];
let notFoundFn = null;

export function on(re, fn) {
  handlers.push({ re, fn });
}

export function setNotFound(fn) {
  notFoundFn = fn;
}

export function go(path) {
  if (!path.startsWith("#")) path = "#" + path;
  if (location.hash === path) {
    dispatch();
  } else {
    location.hash = path;
  }
}

function dispatch() {
  const path = location.hash || "#/";
  for (const { re, fn } of handlers) {
    const m = path.match(re);
    if (m) {
      fn(...m.slice(1));
      window.scrollTo(0, 0);
      return;
    }
  }
  // 没有路由命中 → 兜底 404
  if (notFoundFn) notFoundFn();
}

export function start() {
  window.addEventListener("hashchange", dispatch);
  dispatch();
}
