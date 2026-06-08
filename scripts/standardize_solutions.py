"""把题解代码块标准化成 LeetCode 可直接提交的形式。

为什么需要它:
- 原始 .py 把多种解法放在同一个 `class Solution` 里,方法名带后缀(twoSum_brute 等),
  还有文件级辅助函数(_merge)、自测脚本(_test)。这些直接复制到 LeetCode 会
  报 SyntaxError / NameError / 找不到方法名。
- 本模块从 `raw_source` 用 AST 重新抽取每个解法,产出独立、完整、可提交的
  `class Solution`(或设计题的 `class Xxx`):方法名统一为 LeetCode 规范名(无下划线那个),
  自动内联它依赖的辅助方法 / 函数 / 常量 / 并查集,并按需补上 import。

被 build.py 调用;也可单独对已生成的 data/problems/*.json 批量应用。
所有产物都经 ast 解析 + pyflakes「无未定义名」+ 关键题功能用例验证。
"""
from __future__ import annotations
import ast
import re

UNIONFIND_SRC = '''class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1'''


def _node_src(node, lines):
    start = node.lineno
    if getattr(node, "decorator_list", None):
        start = min(start, min(d.lineno for d in node.decorator_list))
    return "\n".join(lines[start - 1:node.end_lineno]).rstrip()


def _uses(name, code):
    return re.search(rf'(?<![.\w]){re.escape(name)}\b', code) is not None


def _self_methods(code):
    return set(re.findall(r'self\.(\w+)\s*\(', code))


def _collect_imports(tree, src):
    out = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.ImportFrom) and node.module in ("__future__", "_common.ds"):
                continue  # __future__ 不需要;ListNode/TreeNode/UnionFind 由 LeetCode 提供或内联
            seg = ast.get_source_segment(src, node)
            names = {a.asname or a.name.split('.')[0] for a in node.names}
            out.append((seg, names))
    return out


def _collect_top_defs(tree, lines):
    funcs, consts = {}, {}
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name != "_test":
            funcs[n.name] = _node_src(n, lines)
        elif isinstance(n, ast.ClassDef) and n.name != "Solution":
            funcs[n.name] = _node_src(n, lines)
        elif isinstance(n, (ast.Assign, ast.AnnAssign)):
            tgts = n.targets if isinstance(n, ast.Assign) else [n.target]
            for t in tgts:
                if isinstance(t, ast.Name):
                    consts[t.id] = _node_src(n, lines)
    return funcs, consts


def _needed_imports(code, imports):
    return [seg for seg, names in imports if any(_uses(n, code) for n in names)]


def _rename_entry(src, entry, M):
    if entry == M:
        return src
    src = re.sub(rf'\bdef\s+{re.escape(entry)}\b', f'def {M}', src)
    src = re.sub(rf'self\.{re.escape(entry)}\b', f'self.{M}', src)
    return src


def _real_solutions(data):
    """过滤掉 entry 以 _ 开头的伪解法(被解析器误当成解法的内部辅助方法)。"""
    out = []
    for s in data.get("solutions", []):
        m = re.match(r'\s*def\s+(\w+)', s["code"])
        if m and not m.group(1).startswith("_"):
            out.append((s, m.group(1)))
    return out


def _build_normal(data, raw):
    tree = ast.parse(raw)
    lines = raw.split("\n")
    imports = _collect_imports(tree, raw)
    sol_cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Solution")
    methods = {m.name: m for m in sol_cls.body if isinstance(m, ast.FunctionDef)}
    top_funcs, top_consts = _collect_top_defs(tree, lines)
    M = next(n for n in methods if "_" not in n)  # LeetCode 规范方法名(无下划线那个,唯一)
    results = []
    for s, entry in _real_solutions(data):
        want_methods, want_funcs, want_consts, want_uf = [], [], [], False
        seen, work = set(), [entry]
        while work:
            cur = work.pop()
            if cur in seen:
                continue
            seen.add(cur)
            body = _node_src(methods[cur], lines) if cur in methods else (
                top_funcs.get(cur) or top_consts.get(cur) or "")
            for sm in _self_methods(body):
                if sm in methods and sm != entry and sm not in seen:
                    want_methods.append(sm); work.append(sm)
            for fn in top_funcs:
                if fn != cur and _uses(fn, body) and fn not in seen:
                    want_funcs.append(fn); work.append(fn)
            for cn in top_consts:
                if _uses(cn, body) and cn not in seen:
                    want_consts.append(cn); work.append(cn)
            if _uses("UnionFind", body):
                want_uf = True
        entry_src = _rename_entry(_node_src(methods[entry], lines), entry, M)
        method_blocks = [entry_src] + [_node_src(methods[mm], lines) for mm in dict.fromkeys(want_methods)]
        head = ([UNIONFIND_SRC] if want_uf else [])
        head += [top_consts[c] for c in dict.fromkeys(want_consts)]
        head += [top_funcs[fn] for fn in dict.fromkeys(want_funcs)]
        cls_block = "class Solution:\n" + "\n\n".join(method_blocks)
        imps = _needed_imports("\n".join(method_blocks + head), imports)
        pieces = ([("\n".join(imps))] if imps else []) + head + [cls_block]
        block = "\n\n".join(pieces).strip() + "\n"
        ast.parse(block)  # 语法保险
        ns = dict(s); ns["code"] = block
        results.append(ns)
    return results


def _build_design(data, raw):
    tree = ast.parse(raw)
    lines = raw.split("\n")
    imports = _collect_imports(tree, raw)
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    blocks = [_node_src(c, lines) for c in classes]
    imps = _needed_imports("\n".join(blocks), imports)
    pieces = ([("\n".join(imps))] if imps else []) + blocks
    block = "\n\n".join(pieces).strip() + "\n"
    ast.parse(block)
    return [{"method": classes[-1].name, "title": "标准实现",
             "time": "", "space": "", "starred": True, "code": block}]


def standardize_problem(data: dict) -> dict:
    """就地把 data['solutions'] 替换为 LeetCode 可提交的标准块。需要 data['raw_source']。"""
    raw = data.get("raw_source", "")
    if not raw:
        return data
    data["solutions"] = _build_normal(data, raw) if data.get("solutions") else _build_design(data, raw)
    return data
