// Minimal markdown-ish renderer tuned for Python docstrings + tables.
// Not a full Markdown spec — just enough for the patterns we use.

const ESC_MAP = { "&": "&amp;", "<": "&lt;", ">": "&gt;" };
function esc(s) {
  return String(s).replace(/[&<>]/g, c => ESC_MAP[c]);
}

// Render an entire docstring (multi-line text). Supports:
//   * 🔹 sections as h3
//   * pipe tables (autodetected)
//   * - / * bullet lists
//   * `inline code`, **bold**
//   * blank lines as paragraph break
export function renderDoc(text) {
  if (!text) return "";
  // Strip leading 4 spaces / 8 spaces uniformly (docstrings are indented).
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  // Find common leading whitespace across non-empty lines.
  let minIndent = Infinity;
  for (const l of lines) {
    if (l.trim() === "") continue;
    const m = l.match(/^( +)/);
    minIndent = Math.min(minIndent, m ? m[1].length : 0);
  }
  if (minIndent === Infinity) minIndent = 0;
  const trimmed = lines.map(l => l.startsWith(" ".repeat(minIndent)) ? l.slice(minIndent) : l);

  const out = [];
  let i = 0;
  while (i < trimmed.length) {
    const line = trimmed[i];

    // Section header: lines starting with 🔹
    if (line.startsWith("🔹")) {
      const title = line.replace(/^🔹\s*/, "");
      out.push(`<h3 class="sec-h"><span class="head-icon">🔹</span>${escInline(title)}</h3>`);
      i++;
      continue;
    }

    // Blank line
    if (line.trim() === "") {
      i++;
      continue;
    }

    // Pipe table: line starts with |, next line is separator
    if (line.trim().startsWith("|")) {
      const tableLines = [];
      while (i < trimmed.length && trimmed[i].trim().startsWith("|")) {
        tableLines.push(trimmed[i].trim());
        i++;
      }
      out.push(renderTable(tableLines));
      continue;
    }

    // Bullet list: lines starting with - or *
    if (/^\s*[-*]\s+/.test(line)) {
      const items = [];
      while (i < trimmed.length && /^\s*[-*]\s+/.test(trimmed[i])) {
        items.push(trimmed[i].replace(/^\s*[-*]\s+/, ""));
        i++;
      }
      out.push(`<ul>${items.map(it => `<li>${escInline(it)}</li>`).join("")}</ul>`);
      continue;
    }

    // Numbered list:  1.  ... 2.  ...
    if (/^\s*\d+\.\s+/.test(line)) {
      const items = [];
      while (i < trimmed.length && /^\s*\d+\.\s+/.test(trimmed[i])) {
        items.push(trimmed[i].replace(/^\s*\d+\.\s+/, ""));
        i++;
      }
      out.push(`<ol>${items.map(it => `<li>${escInline(it)}</li>`).join("")}</ol>`);
      continue;
    }

    // Paragraph: collect contiguous non-empty / non-section lines
    const para = [];
    while (i < trimmed.length && trimmed[i].trim() !== ""
            && !trimmed[i].startsWith("🔹")
            && !trimmed[i].trim().startsWith("|")
            && !/^\s*[-*]\s+/.test(trimmed[i])
            && !/^\s*\d+\.\s+/.test(trimmed[i])) {
      para.push(trimmed[i]);
      i++;
    }
    if (para.length) {
      // join with <br> to preserve line breaks, escInline each
      out.push(`<p>${para.map(escInline).join("<br>")}</p>`);
    }
  }
  return out.join("\n");
}

function renderTable(lines) {
  // expects: ['|h1|h2|', '|---|---|', '|c1|c2|', ...]
  if (lines.length < 2) return `<pre>${esc(lines.join("\n"))}</pre>`;
  const splitRow = l => l.split("|").slice(1, -1).map(c => c.trim());
  const headers = splitRow(lines[0]);
  // Skip separator at line[1]
  const rows = lines.slice(2).map(splitRow);
  const ths = headers.map(h => `<th>${escInline(h)}</th>`).join("");
  const trs = rows.map(r => `<tr>${r.map(c => `<td>${escInline(c)}</td>`).join("")}</tr>`).join("");
  return `<table><thead><tr>${ths}</tr></thead><tbody>${trs}</tbody></table>`;
}

// Inline: `code`, **bold**, simple escape
function escInline(s) {
  let r = esc(s);
  r = r.replace(/`([^`]+)`/g, (_, c) => `<code>${c}</code>`);
  r = r.replace(/\*\*([^*]+)\*\*/g, (_, c) => `<strong>${c}</strong>`);
  return r;
}

// Convert raw markdown text (entire .md file) to HTML.
// Supports # / ## / ### headings, ``` fenced code, pipe tables, lists, paragraphs.
export function renderMarkdown(text) {
  if (!text) return "";
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const out = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];

    // ATX headings
    const m = line.match(/^(#{1,6})\s+(.*)$/);
    if (m) {
      const lvl = m[1].length;
      out.push(`<h${lvl}>${escInline(m[2])}</h${lvl}>`);
      i++;
      continue;
    }
    // Fenced code
    if (line.trim().startsWith("```")) {
      const lang = line.trim().slice(3).trim();
      const buf = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith("```")) {
        buf.push(lines[i]);
        i++;
      }
      i++;
      out.push(`<pre class="code"><code class="language-${lang || "plaintext"}">${esc(buf.join("\n"))}</code></pre>`);
      continue;
    }
    // Pipe tables
    if (line.trim().startsWith("|")) {
      const tbl = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) {
        tbl.push(lines[i].trim());
        i++;
      }
      out.push(renderTable(tbl));
      continue;
    }
    // Bullet lists
    if (/^\s*[-*]\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*[-*]\s+/, ""));
        i++;
      }
      out.push(`<ul>${items.map(it => `<li>${escInline(it)}</li>`).join("")}</ul>`);
      continue;
    }
    // Numbered list
    if (/^\s*\d+\.\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*\d+\.\s+/, ""));
        i++;
      }
      out.push(`<ol>${items.map(it => `<li>${escInline(it)}</li>`).join("")}</ol>`);
      continue;
    }
    // Paragraph
    if (line.trim() !== "") {
      const para = [];
      while (i < lines.length
              && lines[i].trim() !== ""
              && !lines[i].match(/^(#{1,6})\s+/)
              && !lines[i].trim().startsWith("```")
              && !lines[i].trim().startsWith("|")
              && !/^\s*[-*]\s+/.test(lines[i])
              && !/^\s*\d+\.\s+/.test(lines[i])) {
        para.push(lines[i]);
        i++;
      }
      out.push(`<p>${para.map(escInline).join("<br>")}</p>`);
      continue;
    }
    i++;
  }
  return out.join("\n");
}
