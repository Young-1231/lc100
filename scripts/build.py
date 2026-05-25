#!/usr/bin/env python3
"""把 hot100/ 里的 .py 题解解析为静态站点用的 JSON 数据。

用法:
    python3 scripts/build.py
    python3 scripts/build.py --src /Users/max/Codefield/hot100 --dst .
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from standardize_solutions import standardize_problem

DAY_LABEL = {
    "day1_hash_two_pointer_window":         (1, "哈希 / 双指针 / 滑动窗口 / 子串"),
    "day2_array_matrix":                    (2, "数组 / 矩阵"),
    "day3_linked_list":                     (3, "链表"),
    "day4_binary_tree":                     (4, "二叉树"),
    "day5_graph_backtrack_binary_search":   (5, "图论 / 回溯 / 二分"),
    "day6_stack_heap_greedy":               (6, "栈 / 堆 / 贪心"),
    "day7_dp_multi_dp_tricks":              (7, "DP / 多维DP / 技巧"),
}

# 题号 -> LeetCode 官方 slug(已逐题对 leetcode.cn 校验,og:title 题号匹配)。
# 注意:不能用文件名缩写拼 slug,否则约半数题目链接 404。
SLUG_BY_ID: dict[int, str] = {
    1: "two-sum", 2: "add-two-numbers", 3: "longest-substring-without-repeating-characters",
    4: "median-of-two-sorted-arrays", 5: "longest-palindromic-substring", 11: "container-with-most-water",
    15: "3sum", 17: "letter-combinations-of-a-phone-number", 19: "remove-nth-node-from-end-of-list",
    20: "valid-parentheses", 21: "merge-two-sorted-lists", 22: "generate-parentheses", 23: "merge-k-sorted-lists",
    24: "swap-nodes-in-pairs", 25: "reverse-nodes-in-k-group", 31: "next-permutation", 32: "longest-valid-parentheses",
    33: "search-in-rotated-sorted-array", 34: "find-first-and-last-position-of-element-in-sorted-array",
    35: "search-insert-position", 39: "combination-sum", 41: "first-missing-positive", 42: "trapping-rain-water",
    45: "jump-game-ii", 46: "permutations", 48: "rotate-image", 49: "group-anagrams", 51: "n-queens",
    53: "maximum-subarray", 54: "spiral-matrix", 55: "jump-game", 56: "merge-intervals", 62: "unique-paths",
    64: "minimum-path-sum", 70: "climbing-stairs", 72: "edit-distance", 73: "set-matrix-zeroes",
    74: "search-a-2d-matrix", 75: "sort-colors", 76: "minimum-window-substring", 78: "subsets", 79: "word-search",
    84: "largest-rectangle-in-histogram", 94: "binary-tree-inorder-traversal", 98: "validate-binary-search-tree",
    101: "symmetric-tree", 102: "binary-tree-level-order-traversal", 104: "maximum-depth-of-binary-tree",
    105: "construct-binary-tree-from-preorder-and-inorder-traversal", 108: "convert-sorted-array-to-binary-search-tree",
    114: "flatten-binary-tree-to-linked-list", 118: "pascals-triangle", 121: "best-time-to-buy-and-sell-stock",
    124: "binary-tree-maximum-path-sum", 128: "longest-consecutive-sequence", 131: "palindrome-partitioning",
    136: "single-number", 138: "copy-list-with-random-pointer", 139: "word-break", 141: "linked-list-cycle",
    142: "linked-list-cycle-ii", 146: "lru-cache", 148: "sort-list", 152: "maximum-product-subarray",
    153: "find-minimum-in-rotated-sorted-array", 155: "min-stack", 160: "intersection-of-two-linked-lists",
    169: "majority-element", 189: "rotate-array", 198: "house-robber", 199: "binary-tree-right-side-view",
    200: "number-of-islands", 206: "reverse-linked-list", 207: "course-schedule", 208: "implement-trie-prefix-tree",
    215: "kth-largest-element-in-an-array", 226: "invert-binary-tree", 230: "kth-smallest-element-in-a-bst",
    234: "palindrome-linked-list", 236: "lowest-common-ancestor-of-a-binary-tree", 238: "product-of-array-except-self",
    239: "sliding-window-maximum", 240: "search-a-2d-matrix-ii", 279: "perfect-squares", 283: "move-zeroes",
    287: "find-the-duplicate-number", 295: "find-median-from-data-stream", 300: "longest-increasing-subsequence",
    322: "coin-change", 347: "top-k-frequent-elements", 394: "decode-string", 416: "partition-equal-subset-sum",
    437: "path-sum-iii", 438: "find-all-anagrams-in-a-string", 543: "diameter-of-binary-tree",
    560: "subarray-sum-equals-k", 739: "daily-temperatures", 763: "partition-labels", 994: "rotting-oranges",
    1143: "longest-common-subsequence",
}

CATEGORY_BY_ID: dict[int, str] = {
    # Day 1
    1: "哈希", 49: "哈希", 128: "哈希",
    283: "双指针", 11: "双指针", 15: "双指针", 42: "双指针",
    3: "滑动窗口", 438: "滑动窗口",
    560: "子串", 239: "子串", 76: "子串",
    # Day 2
    53: "普通数组", 56: "普通数组", 189: "普通数组", 238: "普通数组", 41: "普通数组",
    73: "矩阵", 54: "矩阵", 48: "矩阵", 240: "矩阵",
    # Day 3
    160: "链表", 206: "链表", 234: "链表", 141: "链表", 142: "链表",
    21: "链表", 2: "链表", 19: "链表", 24: "链表", 25: "链表",
    138: "链表", 148: "链表", 23: "链表", 146: "链表",
    # Day 4
    94: "二叉树", 104: "二叉树", 226: "二叉树", 101: "二叉树", 543: "二叉树",
    102: "二叉树", 108: "二叉树", 98: "二叉树", 230: "二叉树", 199: "二叉树",
    114: "二叉树", 105: "二叉树", 437: "二叉树", 236: "二叉树", 124: "二叉树",
    # Day 5
    200: "图论", 994: "图论", 207: "图论", 208: "图论",
    46: "回溯", 78: "回溯", 17: "回溯", 39: "回溯", 22: "回溯", 79: "回溯", 131: "回溯", 51: "回溯",
    35: "二分", 74: "二分", 34: "二分", 33: "二分", 153: "二分", 4: "二分",
    # Day 6
    20: "栈", 155: "栈", 394: "栈", 739: "栈", 84: "栈",
    215: "堆", 347: "堆", 295: "堆",
    121: "贪心", 55: "贪心", 45: "贪心", 763: "贪心",
    # Day 7
    70: "DP", 118: "DP", 198: "DP", 279: "DP", 322: "DP",
    139: "DP", 300: "DP", 152: "DP", 416: "DP", 32: "DP",
    62: "多维DP", 64: "多维DP", 5: "多维DP", 1143: "多维DP", 72: "多维DP",
    136: "技巧", 169: "技巧", 75: "技巧", 31: "技巧", 287: "技巧",
}


HEAD_RE = re.compile(r"^#\s*LC\s*(\d+)\.\s*(.+?)\s*[·•]\s*(\w+)\s*[·•]\s*(.+)$")
SOL_HEAD_RE = re.compile(
    r"^\s*#\s*解法\s*(\d+)\s*[::]?\s*([^—\-]*?)\s*[—\-]\s*(.+?)$"
)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def parse_first_comment(lines: list[str]) -> tuple[int, str, str, str]:
    """解析第一行 `# LC X. 中文名 · Easy · tags`。"""
    if lines:
        m = HEAD_RE.match(lines[0])
        if m:
            num = int(m.group(1))
            return num, m.group(2).strip(), m.group(3).strip(), m.group(4).strip()
    return 0, "", "Medium", ""


def extract_docstring(text: str) -> str:
    """提取顶部模块 docstring。"""
    m = re.search(r'^"""(.*?)"""', text, re.DOTALL | re.MULTILINE)
    return (m.group(1).strip() if m else "")


def parse_solution_methods(text: str) -> list[dict[str, Any]]:
    """从 class Solution 中提取每个 def 及其前的 # 解法 X 注释 + 代码。"""
    sols: list[dict[str, Any]] = []
    full_lines = text.split("\n")
    # 找 class Solution 起始行
    start = -1
    for i, ln in enumerate(full_lines):
        if re.match(r"^class\s+Solution\b", ln):
            start = i
            break
    if start < 0:
        return sols
    # 从下一行开始,逐行收集 class body:行首是 4 空格或空行
    body_lines: list[str] = []
    i = start + 1
    while i < len(full_lines):
        ln = full_lines[i]
        if ln == "" or ln.startswith("    "):
            body_lines.append(ln)
            i += 1
            continue
        # 遇到顶级行(class / def / 普通代码),停止
        break
    lines = body_lines

    # 寻找以 4 缩进开头的 def
    methods: list[tuple[int, str]] = []   # (line_idx, def_line)
    for i, line in enumerate(lines):
        if re.match(r"^\s{4}def\s+\w+\(", line):
            methods.append((i, line))
    methods.append((len(lines), ""))      # 哨兵

    for idx in range(len(methods) - 1):
        ln_i, def_line = methods[idx]
        ln_next = methods[idx + 1][0]
        # 抓 def 上方的连续注释(可能是 "# 解法 1: xxx — O(n)")
        head_lines = []
        j = ln_i - 1
        while j >= 0 and lines[j].strip().startswith("#"):
            head_lines.insert(0, lines[j].rstrip())
            j -= 1
        head = "\n".join(h.strip() for h in head_lines)

        # 取代码块(从 def 到下一个 def 之前),并把下一个 def 的注释头从尾部剥离
        end = ln_next
        # 跳过尾部空行
        while end > ln_i and lines[end - 1].strip() == "":
            end -= 1
        # 跳过尾部紧贴 def 的连续注释(它们属于"下一个 def 的头")
        while end > ln_i and lines[end - 1].strip().startswith("#"):
            end -= 1
        # 再次清空尾部空行
        while end > ln_i and lines[end - 1].strip() == "":
            end -= 1
        code_block = "\n".join(lines[ln_i:end]).rstrip()
        # 反缩进 4 空格
        code_block = "\n".join(
            l[4:] if l.startswith("    ") else l for l in code_block.split("\n")
        )

        # 解析方法名 / 复杂度
        m = re.match(r"\s{0,8}def\s+(\w+)\(", def_line)
        method_name = m.group(1) if m else "method"

        title = ""
        time_c = ""
        space_c = ""
        is_star = "★" in head

        # 试解析 "# 解法 1:xxx — O(n) / O(1)"
        m_h = re.search(r"#\s*解法\s*\d+\s*[::]\s*([^—\-]+?)\s*[—\-]\s*(.+?)$",
                        head, re.MULTILINE)
        if m_h:
            title = m_h.group(1).strip().replace("★", "").strip()
            cx = m_h.group(2).strip()
            # 提取时间/空间
            ts = re.findall(r"O\([^)]+\)|Θ\([^)]+\)", cx)
            if len(ts) >= 1:
                time_c = ts[0]
            if len(ts) >= 2:
                space_c = ts[1]
        else:
            # 退化:文件没用 # 解法 注释,根据方法名生成标题
            if method_name.endswith("_brute"):
                title = "暴力"
            elif "_recursive" in method_name:
                title = "递归"
            elif method_name.endswith(("_dp", "_dp1", "_dp2")):
                title = "DP"
            else:
                title = "主解法"

        sols.append({
            "method": method_name,
            "title": title or method_name,
            "time": time_c,
            "space": space_c,
            "starred": is_star,
            "code": code_block,
        })
    return sols


def parse_problem(py_path: Path, day: int, day_title: str) -> dict[str, Any]:
    text = py_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    num, title_zh, difficulty, tag_text = parse_first_comment(lines)
    if num == 0:
        # 用文件名兜底
        m = re.match(r"p(\d+)_", py_path.name)
        num = int(m.group(1)) if m else 0
    docstring = extract_docstring(text)
    sols = parse_solution_methods(text)

    # category 归类(用人工 map 兜底)
    category = CATEGORY_BY_ID.get(num, tag_text.split("/")[-1].strip() or "其他")

    # leetcode url:优先用权威题号->slug 映射(SLUG_BY_ID),
    # 仅当题号缺失时才退回文件名拼 slug(并告警,提醒补全映射)。
    leet_slug = SLUG_BY_ID.get(num)
    if not leet_slug:
        leet_slug = (py_path.stem.split("_", 1)[1] if "_" in py_path.stem else "").replace("_", "-")
        print(f"  ⚠ 题 {num} ({py_path.stem}) 缺少 SLUG_BY_ID 映射,退回文件名 slug='{leet_slug}',请补全。")
    leet_url = f"https://leetcode.cn/problems/{leet_slug}/"

    return {
        "id": num,
        "title": title_zh or py_path.stem,
        "difficulty": difficulty,
        "tags": [t.strip() for t in re.split(r"[/、,]", tag_text) if t.strip()],
        "day": day,
        "day_title": day_title,
        "category": category,
        "leetcode_url": leet_url,
        "filename": py_path.name,
        "doc": docstring,
        "solutions": sols,
        "raw_source": text,
        "viz": _viz_for(num),
    }


# ===== 可视化样例:链表 / 二叉树 / 数组 / 滑窗 =====
VIZ: dict[int, dict] = {
    # 链表
    206: {"type": "list", "data": [1, 2, 3, 4, 5], "label": "反转前"},
    21:  {"type": "list", "data": [1, 1, 2, 3, 4, 4], "label": "合并结果"},
    19:  {"type": "list", "data": [1, 2, 3, 4, 5], "label": "删除倒数第 2 个", "highlight": [3]},
    24:  {"type": "list", "data": [1, 2, 3, 4], "label": "两两交换前"},
    25:  {"type": "list", "data": [1, 2, 3, 4, 5], "label": "K=2 翻转前"},
    141: {"type": "list", "data": [3, 2, 0, -4], "cycle": True, "label": "环形链表"},
    142: {"type": "list", "data": [3, 2, 0, -4], "cycle": True, "label": "环入口=节点 1", "highlight": [1]},
    160: {"type": "list", "data": [4, 1, 8, 4, 5], "label": "示例"},
    234: {"type": "list", "data": [1, 2, 3, 2, 1], "label": "回文链表"},
    148: {"type": "list", "data": [4, 2, 1, 3], "label": "排序前"},
    23:  {"type": "list", "data": [1, 1, 2, 3, 4, 4, 5, 6], "label": "K=3 合并"},
    138: {"type": "list", "data": [7, 13, 11, 10, 1], "label": "随机链表"},
    2:   {"type": "list", "data": [2, 4, 3], "label": "342(低位在前)"},
    146: {"type": "list", "data": [4, 3, 2, 1], "label": "LRU(头最新)"},
    # 二叉树
    94:  {"type": "tree", "data": [1, None, 2, 3], "label": "示例"},
    104: {"type": "tree", "data": [3, 9, 20, None, None, 15, 7], "label": "深度=3"},
    226: {"type": "tree", "data": [4, 2, 7, 1, 3, 6, 9], "label": "翻转前"},
    101: {"type": "tree", "data": [1, 2, 2, 3, 4, 4, 3], "label": "对称树"},
    543: {"type": "tree", "data": [1, 2, 3, 4, 5], "label": "直径=3"},
    102: {"type": "tree", "data": [3, 9, 20, None, None, 15, 7], "label": "层序示例"},
    98:  {"type": "tree", "data": [2, 1, 3], "label": "合法 BST"},
    230: {"type": "tree", "data": [3, 1, 4, None, 2], "label": "BST"},
    199: {"type": "tree", "data": [1, 2, 3, None, 5, None, 4], "label": "右视图=[1,3,4]", "highlight": [1, 3, 4]},
    114: {"type": "tree", "data": [1, 2, 5, 3, 4, None, 6], "label": "展开前"},
    105: {"type": "tree", "data": [3, 9, 20, None, None, 15, 7], "label": "构造结果"},
    437: {"type": "tree", "data": [10, 5, -3, 3, 2, None, 11, 3, -2, None, 1], "label": "路径示例"},
    236: {"type": "tree", "data": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "label": "LCA 示例"},
    124: {"type": "tree", "data": [-10, 9, 20, None, None, 15, 7], "label": "最大路径=42"},
    108: {"type": "tree", "data": [0, -3, 9, -10, None, 5], "label": "由 [-10,-3,0,5,9] 构造"},
    # 数组 / 滑窗
    1:   {"type": "array", "data": [2, 7, 11, 15],
          "highlight": [0, 1],
          "pointers": [{"idx": 0, "label": "i=0"}, {"idx": 1, "label": "i=1"}],
          "label": "target=9 → seen[2]=0 命中"},
    283: {"type": "frames", "label": "双指针扫描",
          "frames": [
              {"type": "array", "data": [0, 1, 0, 3, 12],
               "pointers": [{"idx": 0, "label": "slow"}, {"idx": 0, "label": "fast", "color": "#ea580c"}],
               "note": "初始: slow=fast=0"},
              {"type": "array", "data": [1, 0, 0, 3, 12],
               "pointers": [{"idx": 1, "label": "slow"}, {"idx": 1, "label": "fast", "color": "#ea580c"}],
               "note": "fast=1 是非零,swap 后 slow 推进"},
              {"type": "array", "data": [1, 3, 0, 0, 12],
               "pointers": [{"idx": 2, "label": "slow"}, {"idx": 3, "label": "fast", "color": "#ea580c"}],
               "note": "fast 跳过零,在 fast=3 处 swap"},
              {"type": "array", "data": [1, 3, 12, 0, 0],
               "pointers": [{"idx": 3, "label": "slow"}, {"idx": 4, "label": "fast", "color": "#ea580c"}],
               "note": "扫描完成: 非零左聚,零右移"},
          ]},
    11:  {"type": "array", "data": [1, 8, 6, 2, 5, 4, 8, 3, 7],
          "highlight": [1, 8],
          "pointers": [{"idx": 1, "label": "l=1"}, {"idx": 8, "label": "r=8"}],
          "label": "(8-1)·min(8,7) = 49"},
    42:  {"type": "array", "data": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], "label": "可接 6 单位水"},
    3:   {"type": "frames", "label": "滑窗扫描 abcabcbb",
          "frames": [
              {"type": "array", "data": ["a", "b", "c", "a", "b", "c", "b", "b"],
               "windowL": 0, "windowR": 2,
               "pointers": [{"idx": 0, "label": "l"}, {"idx": 2, "label": "r", "color": "#ea580c"}],
               "note": "扩到 'abc',长度 3"},
              {"type": "array", "data": ["a", "b", "c", "a", "b", "c", "b", "b"],
               "windowL": 1, "windowR": 3,
               "pointers": [{"idx": 1, "label": "l"}, {"idx": 3, "label": "r", "color": "#ea580c"}],
               "note": "r=3 遇到重复 'a',l 跳到 1"},
              {"type": "array", "data": ["a", "b", "c", "a", "b", "c", "b", "b"],
               "windowL": 4, "windowR": 6,
               "pointers": [{"idx": 4, "label": "l"}, {"idx": 6, "label": "r", "color": "#ea580c"}],
               "note": "继续扩;最长仍是 3"},
          ]},
    239: {"type": "array", "data": [1, 3, -1, -3, 5, 3, 6, 7],
          "windowL": 0, "windowR": 2,
          "pointers": [{"idx": 0, "label": "l"}, {"idx": 2, "label": "r", "color": "#ea580c"}],
          "label": "k=3 滑窗 → 队头是 max=3"},
    560: {"type": "array", "data": [1, 1, 1], "label": "k=2 → 子数组数=2"},
    53:  {"type": "array", "data": [-2, 1, -3, 4, -1, 2, 1, -5, 4], "windowL": 3, "windowR": 6, "label": "最大和=6"},
    189: {"type": "array", "data": [1, 2, 3, 4, 5, 6, 7], "label": "右移 3 后 = [5,6,7,1,2,3,4]"},
    238: {"type": "array", "data": [1, 2, 3, 4], "label": "答案=[24,12,8,6]"},
    41:  {"type": "array", "data": [3, 4, -1, 1], "label": "缺失=2"},
    121: {"type": "array", "data": [7, 1, 5, 3, 6, 4], "highlight": [1, 4], "label": "买入=1, 卖出=6"},
    136: {"type": "array", "data": [4, 1, 2, 1, 2], "highlight": [0], "label": "落单=4"},
    169: {"type": "array", "data": [2, 2, 1, 1, 1, 2, 2], "highlight": [0, 1, 5, 6], "label": "众数=2"},
    75:  {"type": "array", "data": [2, 0, 2, 1, 1, 0], "label": "颜色分类前"},
    287: {"type": "array", "data": [1, 3, 4, 2, 2], "highlight": [3, 4], "label": "重复=2"},
}


def _viz_for(num: int) -> dict | None:
    return VIZ.get(num)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../hot100",
                    help="hot100 项目路径(默认 ../hot100)")
    ap.add_argument("--dst", default=".",
                    help="lc100 站点根目录(默认当前)")
    args = ap.parse_args()

    src = Path(args.src).expanduser().resolve()
    dst = Path(args.dst).expanduser().resolve()
    print(f"src = {src}\ndst = {dst}")

    problems_dir = dst / "data" / "problems"
    problems_dir.mkdir(parents=True, exist_ok=True)
    sols_dir = dst / "solutions"
    sols_dir.mkdir(parents=True, exist_ok=True)

    # 读取手写双版本思路 + 复杂度推导
    expl_path = dst / "data" / "explanations.json"
    explanations: dict[str, dict] = {}
    if expl_path.exists():
        explanations = json.loads(expl_path.read_text(encoding="utf-8"))

    # 读取手写「代码逐行讲解 + 注意点」(独立文件,重建时不会丢)
    ce_path = dst / "data" / "code_explain.json"
    code_explains: dict[str, dict] = {}
    if ce_path.exists():
        code_explains = json.loads(ce_path.read_text(encoding="utf-8"))

    all_problems: list[dict[str, Any]] = []
    days: dict[int, dict[str, Any]] = {}

    for day_dirname, (day_idx, day_title) in DAY_LABEL.items():
        day_path = src / day_dirname
        if not day_path.exists():
            print(f"⚠️  missing {day_path}")
            continue
        day_problems: list[int] = []
        for py in sorted(day_path.glob("p*.py")):
            data = parse_problem(py, day_idx, day_title)
            # 把解法代码标准化成 LeetCode 可直接提交的 class Solution(方法名规范化、内联依赖、补 import)
            standardize_problem(data)
            # 合并手写解释
            expl = explanations.get(str(data["id"]))
            if expl and not str(expl.get("short", "")).startswith("_"):
                data["explanation"] = expl
            # 合并代码逐行讲解
            ce = code_explains.get(str(data["id"]))
            if ce:
                data["code_explain"] = ce
            (problems_dir / f"p{data['id']:04d}.json").write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            shutil.copy(py, sols_dir / py.name)
            # 索引摘要
            # 搜索索引文本:把题面、思路、复杂度、解法标题拼起来
            search_blob = " ".join([
                data["title"],
                " ".join(data["tags"]),
                data["category"],
                data.get("doc", ""),
                (data.get("explanation", {}) or {}).get("short", ""),
                " ".join((data.get("explanation", {}) or {}).get("long", []) or []),
                " ".join(s.get("title", "") for s in data["solutions"]),
            ])
            all_problems.append({
                "id": data["id"],
                "title": data["title"],
                "difficulty": data["difficulty"],
                "category": data["category"],
                "day": data["day"],
                "day_title": data["day_title"],
                "filename": data["filename"],
                "n_sols": len(data["solutions"]),
                "tags": data["tags"],
                "leetcode_url": data["leetcode_url"],
                "has_expl": "explanation" in data,
                "search": search_blob.lower(),
            })
            day_problems.append(data["id"])
        days[day_idx] = {
            "day": day_idx,
            "title": day_title,
            "dir": day_dirname,
            "problem_ids": day_problems,
        }

    # 汇总索引
    (dst / "data" / "problems.json").write_text(
        json.dumps(sorted(all_problems, key=lambda x: x["id"]),
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (dst / "data" / "days.json").write_text(
        json.dumps(days, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 拷贝可视化模式文档
    viz_src = src / "_visualizations"
    viz_dst = dst / "data" / "patterns"
    if viz_src.exists():
        viz_dst.mkdir(parents=True, exist_ok=True)
        for md in viz_src.glob("*.md"):
            shutil.copy(md, viz_dst / md.name)

    print(f"✅ 生成 {len(all_problems)} 题数据")
    print(f"   - {dst / 'data' / 'problems.json'}")
    print(f"   - {problems_dir}/p*.json")
    print(f"   - {sols_dir}/")


if __name__ == "__main__":
    main()
