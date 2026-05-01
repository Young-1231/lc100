// SVG 可视化模块:链表 / 二叉树 / 数组 / 滑窗
// 所有函数返回 SVG 字符串。颜色用 CSS 变量,自动适配主题。

const COL = {
  node: "var(--bg-elev)",
  nodeBd: "var(--text-soft)",
  nodeText: "var(--text)",
  arrow: "var(--text-mute)",
  hi: "var(--accent)",
  hiBg: "var(--accent-soft)",
  null_: "var(--text-mute)",
  edge: "var(--text-soft)",
};

function svgWrap(width, height, body, label = "") {
  return `<svg viewBox="0 0 ${width} ${height}" width="100%" style="max-width:${width}px;display:block;background:var(--bg-soft);border:1px solid var(--border);border-radius:10px;padding:12px;box-sizing:border-box" role="img" aria-label="${label}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" fill="${COL.arrow}"/>
      </marker>
    </defs>
    ${body}
  </svg>`;
}

// ===================== Linked List =====================
// data: [1,2,3,4,5]   options: { highlight: [int idx], cycle?: boolean (last->first) }
export function renderList(data, opts = {}) {
  const { highlight = [], cycle = false, label = "linked list" } = opts;
  if (!data || !data.length) return "";
  const nw = 50, nh = 36, gap = 24, pad = 14;
  const total = data.length * (nw + gap) - gap;
  const W = total + pad * 2;
  const H = nh + 36;
  const y = pad;
  const parts = [];
  data.forEach((v, i) => {
    const x = pad + i * (nw + gap);
    const isHi = highlight.includes(i);
    parts.push(`<rect x="${x}" y="${y}" width="${nw}" height="${nh}" rx="6"
      fill="${isHi ? COL.hiBg : COL.node}" stroke="${isHi ? COL.hi : COL.nodeBd}" stroke-width="1.4"/>`);
    parts.push(`<text x="${x + nw / 2}" y="${y + nh / 2 + 5}" text-anchor="middle"
      font-family="JetBrains Mono, monospace" font-size="14" fill="${isHi ? COL.hi : COL.nodeText}" font-weight="500">${v}</text>`);
    if (i < data.length - 1) {
      const x1 = x + nw + 2;
      const x2 = x + nw + gap - 2;
      const ay = y + nh / 2;
      parts.push(`<line x1="${x1}" y1="${ay}" x2="${x2}" y2="${ay}" stroke="${COL.arrow}" stroke-width="1.4" marker-end="url(#arrow)"/>`);
    }
  });
  // null tail
  const tailX = pad + data.length * (nw + gap) - gap + 6;
  parts.push(`<text x="${tailX}" y="${y + nh / 2 + 5}" font-family="JetBrains Mono, monospace" font-size="13" fill="${COL.null_}">∅</text>`);
  if (cycle) {
    // 弧线从尾节点 right-bottom 拐回首节点 left-bottom
    const sx = pad + (data.length - 1) * (nw + gap) + nw / 2;
    const sy = y + nh;
    const ex = pad + nw / 2;
    const ey = y + nh;
    const cy = y + nh + 22;
    parts.push(`<path d="M${sx},${sy} Q${(sx + ex) / 2},${cy} ${ex},${ey}" fill="none" stroke="${COL.hi}" stroke-width="1.4" marker-end="url(#arrow)" stroke-dasharray="4 3"/>`);
  }
  return svgWrap(W, H + (cycle ? 20 : 0), parts.join(""), label);
}

// ===================== Binary Tree =====================
// data: LeetCode level-order array, e.g. [3,9,20,null,null,15,7]
export function renderTree(data, opts = {}) {
  const { label = "binary tree", highlight = [] } = opts;
  if (!data || !data.length || data[0] == null) return "";
  // Build node coords using full-binary slot indexing.
  // Root = index 1; its children at 2, 3; level d has 2^d slots.
  // We use the slot index to position x.
  const nodes = [];   // {idx, val, depth}
  const toSlot = (lcIdx) => slotById[lcIdx];
  const slotById = {};

  // BFS through given array, mapping LeetCode array index → slot index.
  const queue = [{ lc: 0, slot: 1, depth: 0 }];
  let maxDepth = 0;
  // We'll iterate the LC array and assign slots BFS-style.
  // The LC array compresses: nulls produce no children.
  // Walk: maintain a queue of slot positions for unfilled children.
  const slots = [{ slot: 1, depth: 0 }];
  let i = 0;
  while (i < data.length && slots.length) {
    const cur = slots.shift();
    const v = data[i++];
    if (v == null) continue;
    nodes.push({ slot: cur.slot, depth: cur.depth, val: v, lcIdx: i - 1 });
    maxDepth = Math.max(maxDepth, cur.depth);
    slots.push({ slot: cur.slot * 2,     depth: cur.depth + 1 });  // left
    slots.push({ slot: cur.slot * 2 + 1, depth: cur.depth + 1 });  // right
  }

  if (!nodes.length) return "";
  // Layout: each level has 2^d slots, slot k spans width / 2^d.
  const cellMin = 36;
  const W = Math.max(360, cellMin * (1 << maxDepth));
  const levelH = 56;
  const H = (maxDepth + 1) * levelH + 28;
  const nodeR = 16;
  const parts = [];

  // Draw edges first (so circles overlay)
  const byLcIdx = new Map();
  nodes.forEach(n => byLcIdx.set(n.lcIdx, n));
  // For each node, compute its parent slot:
  function pos(slot, depth) {
    const cells = 1 << depth;
    const cellW = W / cells;
    const x = (slot - (1 << depth)) * cellW + cellW / 2;
    const y = depth * levelH + 24;
    return { x, y };
  }
  nodes.forEach(n => {
    if (n.slot === 1) return;
    const parentSlot = n.slot >> 1;
    const parent = nodes.find(x => x.slot === parentSlot && x.depth === n.depth - 1);
    if (!parent) return;
    const a = pos(parent.slot, parent.depth);
    const b = pos(n.slot, n.depth);
    parts.push(`<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke="${COL.edge}" stroke-width="1.4"/>`);
  });
  nodes.forEach(n => {
    const { x, y } = pos(n.slot, n.depth);
    const isHi = highlight.includes(n.val);
    parts.push(`<circle cx="${x}" cy="${y}" r="${nodeR}" fill="${isHi ? COL.hiBg : COL.node}" stroke="${isHi ? COL.hi : COL.nodeBd}" stroke-width="1.4"/>`);
    parts.push(`<text x="${x}" y="${y + 4}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="13" fill="${isHi ? COL.hi : COL.nodeText}" font-weight="500">${n.val}</text>`);
  });
  return svgWrap(W, H, parts.join(""), label);
}

// ===================== Array =====================
// data: [1,2,3,4,5];  opts.highlight: [int idx]; opts.windowL/R: number
export function renderArray(data, opts = {}) {
  const { highlight = [], windowL = -1, windowR = -1, label = "array", indices = true } = opts;
  if (!data || !data.length) return "";
  const cw = 44, ch = 38, pad = 14;
  const W = pad * 2 + data.length * cw;
  const H = ch + (indices ? 20 : 0) + (windowL >= 0 ? 18 : 0) + 14;
  const y0 = pad;
  const parts = [];
  data.forEach((v, i) => {
    const x = pad + i * cw;
    const inWin = i >= windowL && i <= windowR && windowL >= 0;
    const isHi = highlight.includes(i);
    const fill = isHi ? COL.hi : (inWin ? COL.hiBg : COL.node);
    const stroke = isHi || inWin ? COL.hi : COL.nodeBd;
    const text = isHi ? "white" : (inWin ? COL.hi : COL.nodeText);
    parts.push(`<rect x="${x}" y="${y0}" width="${cw}" height="${ch}" fill="${fill}" stroke="${stroke}" stroke-width="1.2"/>`);
    parts.push(`<text x="${x + cw / 2}" y="${y0 + ch / 2 + 4}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="13" fill="${text}" font-weight="500">${v}</text>`);
    if (indices) {
      parts.push(`<text x="${x + cw / 2}" y="${y0 + ch + 14}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="${COL.null_}">${i}</text>`);
    }
  });
  if (windowL >= 0 && windowR >= windowL) {
    const x1 = pad + windowL * cw;
    const x2 = pad + (windowR + 1) * cw;
    const ay = y0 + ch + (indices ? 20 : 0) + 8;
    parts.push(`<path d="M${x1},${ay - 4} L${x1},${ay} L${x2},${ay} L${x2},${ay - 4}" fill="none" stroke="${COL.hi}" stroke-width="1.6"/>`);
    parts.push(`<text x="${(x1 + x2) / 2}" y="${ay + 12}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="11" fill="${COL.hi}">window [${windowL}, ${windowR}]</text>`);
  }
  return svgWrap(W, H, parts.join(""), label);
}

// ===================== Dispatcher =====================
// Given a problem.viz spec, return SVG.
export function renderViz(spec) {
  if (!spec) return "";
  switch (spec.type) {
    case "list":  return renderList(spec.data, spec);
    case "tree":  return renderTree(spec.data, spec);
    case "array": return renderArray(spec.data, spec);
    default: return "";
  }
}
