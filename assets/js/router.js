// Tiny hash router.

const handlers = [];

export function on(re, fn) {
  handlers.push({ re, fn });
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
  // 404
  for (const { re, fn } of handlers) {
    if (re.toString() === "/^#\\/404$/") {
      fn();
      return;
    }
  }
}

export function start() {
  window.addEventListener("hashchange", dispatch);
  dispatch();
}
