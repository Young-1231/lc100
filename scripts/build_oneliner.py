#!/usr/bin/env python3
"""构建「一句话速记」板块:data/oneliner.md -> data/oneliner.json,并逐题自测代码。

    python3 scripts/build_oneliner.py

oneliner.md 格式:
    ## 分类
    ### 题号. 标题            (无题号的手撕题用英文 id,如 singleton)
    > 来源：一句话版 · 手撕PDF
    **面试口述思路（方法）** 步骤1； 步骤2； ...
    **超短一句话版** 一句话
    **代码**  ```python ... ```
    **3 个核心要点（面试官必问）**  * **要点**：说明
    **面试追问应对（加分）** 可选
    **另一种写法（方法）** 说明 + ```python ...```  可选

热度 hot = 出现在几份资料里(一句话版 / 手撕PDF / 官方 Hot 100),3 = 三份都收录。
"""
from __future__ import annotations

import json
import re
import sys
from collections import deque
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "oneliner.md"
OUT = ROOT / "data" / "oneliner.json"
PROBLEMS = ROOT / "data" / "problems.json"

# 不在本站 Hot 100 题单里的题,补 leetcode.cn slug + 难度
EXTRA = {
    912: ("sort-an-array", "Medium"),
    "singleton": (None, "Medium"),
    92: ("reverse-linked-list-ii", "Medium"),
    113: ("path-sum-ii", "Medium"),
    122: ("best-time-to-buy-and-sell-stock-ii", "Medium"),
    134: ("gas-station", "Medium"),
    202: ("happy-number", "Easy"),
    209: ("minimum-size-subarray-sum", "Medium"),
    231: ("power-of-two", "Easy"),
    235: ("lowest-common-ancestor-of-a-binary-search-tree", "Medium"),
    312: ("burst-balloons", "Hard"),
    354: ("russian-doll-envelopes", "Hard"),
    450: ("delete-node-in-a-bst", "Medium"),
    525: ("contiguous-array", "Medium"),
}


def unescape(s: str) -> str:
    return re.sub(r"\\([\[\]_*])", r"\1", s).strip()


def parse_points(block: str) -> list[dict]:
    pts = []
    for line in block.splitlines():
        m = re.match(r"\s*\*\s+\*\*(.+?)\*\*[：:]\s*(.*)$", line)
        if m:
            pts.append({"k": unescape(m.group(1)), "v": unescape(m.group(2)).rstrip("；;。") + "。"})
    return pts


SOURCE_NAMES = {"一句话版": "py", "手撕PDF": "pdf"}


def parse_item(head: str, body: str) -> dict:
    m = re.match(r"(\w+)\.\s+(.+)", head)
    pid = int(m.group(1)) if m.group(1).isdigit() else m.group(1)
    title = m.group(2).strip()

    sm = re.search(r"^> 来源：(.+)$", body, re.M)
    sources = [SOURCE_NAMES[x.strip()] for x in sm.group(1).split("·")]
    body = body[:sm.start()] + body[sm.end():]

    alt = None
    am = re.search(r"\*\*另一种写法（(.+?)）\*\*(.*?)```python\n(.*?)```", body, re.S)
    if am:
        alt = {"method": am.group(1).strip(), "desc": unescape(am.group(2)), "code": am.group(3).rstrip("\n")}
        body = body[:am.start()] + body[am.end():]

    code_m = re.search(r"```python\n(.*?)```", body, re.S)
    code = code_m.group(1).rstrip("\n")
    before, after = body[:code_m.start()], body[code_m.end():]

    oral_m = re.search(r"\*\*面试口述思路（(.+?)）\*\*(.*?)\*\*超短一句话版\*\*", before, re.S)
    method = oral_m.group(1).strip()
    oral_raw = oral_m.group(2)
    # 正文中的 "* xxx" 子列表与 "；" 分隔的步骤统一拆成步骤数组
    steps = []
    for line in oral_raw.splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^\*\s+", "", line)
        steps += [unescape(s) for s in re.split(r"[；;]\s*", line) if s.strip()]
    steps = [s.rstrip("。：:") for s in steps]

    one = before[oral_m.end():]
    one = unescape(one.split("**代码**")[0])

    pts_block, follow = after, ""
    fm = re.search(r"\*\*面试追问应对（加分）\*\*(.*)", after, re.S)
    if fm:
        pts_block, follow = after[:fm.start()], unescape(fm.group(1).replace("***", ""))
    points = parse_points(pts_block)
    assert len(points) == 3, (pid, points)
    return {"id": pid, "title": title, "method": method, "steps": steps,
            "oneliner": one, "code": code, "points": points, "followup": follow,
            "alt": alt, "sources": sources}


def parse(md: str) -> dict:
    cats, items, summary = [], [], []
    for block in re.split(r"^## ", md, flags=re.M)[1:]:
        name, rest = block.split("\n", 1)
        name = name.strip()
        if name == "总结":
            for line in rest.splitlines():
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) == 2 and cells[0] not in ("分类", "---"):
                    summary.append(cells)
            continue
        ids = []
        for sec in re.split(r"^### ", rest, flags=re.M)[1:]:
            head, body = sec.split("\n", 1)
            it = parse_item(head.strip(), body)
            it["category"] = name
            items.append(it)
            ids.append(it["id"])
        cats.append({"name": name, "ids": ids})
    return {"categories": cats, "items": items, "summary": summary}


def enrich(data: dict) -> None:
    probs = {p["id"]: p for p in json.loads(PROBLEMS.read_text(encoding="utf-8"))}
    for it in data["items"]:
        p = probs.get(it["id"])
        if p:
            it.update(in_site=True, difficulty=p["difficulty"], leetcode_url=p["leetcode_url"], day=p["day"])
        else:
            slug, diff = EXTRA[it["id"]]
            it.update(in_site=False, difficulty=diff,
                      leetcode_url=f"https://leetcode.cn/problems/{slug}/" if slug else None)
        it["hot"] = len(it["sources"]) + (1 if p else 0)


# ===================== 自测 =====================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def L(xs):
    d = cur = ListNode()
    for x in xs:
        cur.next = ListNode(x)
        cur = cur.next
    return d.next


def LL(h):
    out = []
    while h:
        out.append(h.val)
        h = h.next
    return out


def T(xs):
    """层序数组 -> 树(None 为空)。"""
    if not xs or xs[0] is None:
        return None
    nodes = [TreeNode(x) if x is not None else None for x in xs]
    kids = deque(nodes[1:])
    for n in nodes:
        if n is None:
            continue
        if kids:
            n.left = kids.popleft()
        if kids:
            n.right = kids.popleft()
    return nodes[0]


def find(root, v):
    if not root:
        return None
    if root.val == v:
        return root
    return find(root.left, v) or find(root.right, v)


def inorder(r):
    return inorder(r.left) + [r.val] + inorder(r.right) if r else []


def S():
    return NS["Solution"]()


def srt(x):
    return sorted(sorted(i) if isinstance(i, list) else i for i in x)


NS: dict = {}

TESTS = {
    1: lambda: sorted(S().twoSum([2, 7, 11, 15], 9)) == [0, 1] and sorted(S().twoSum([3, 3], 6)) == [0, 1],
    3: lambda: [S().lengthOfLongestSubstring(s) for s in ("abcabcbb", "bbbbb", "pwwkew", "", "abba")] == [3, 1, 3, 0, 2],
    347: lambda: sorted(S().topKFrequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2],
    146: lambda: (lambda c: (c.put(1, 1), c.put(2, 2), c.get(1) == 1, c.put(3, 3), c.get(2) == -1,
                             c.put(4, 4), c.get(1) == -1, c.get(3) == 3, c.get(4) == 4))(NS["LRUCache"](2))[2::2] == (True,) * 4
                  and (lambda c: (c.put(1, 1), c.put(2, 2), c.get(1), c.put(3, 3), c.get(2)))(NS["LRUCache"](2))[4] == -1,
    21: lambda: LL(S().mergeTwoLists(L([1, 2, 4]), L([1, 3, 4]))) == [1, 1, 2, 3, 4, 4],
    206: lambda: LL(S().reverseList(L([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1] and S().reverseList(None) is None,
    141: lambda: (lambda h: (setattr(h.next.next.next, "next", h.next), S().hasCycle(h))[1])(L([3, 2, 0, -4]))
                 and not S().hasCycle(L([1])),
    19: lambda: LL(S().removeNthFromEnd(L([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5] and LL(S().removeNthFromEnd(L([1]), 1)) == [],
    15: lambda: srt(S().threeSum([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]] and S().threeSum([0, 0, 0, 0]) == [[0, 0, 0]],
    11: lambda: S().maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49,
    76: lambda: S().minWindow("ADOBECODEBANC", "ABC") == "BANC" and S().minWindow("a", "aa") == "",
    209: lambda: S().minSubArrayLen(7, [2, 3, 1, 2, 4, 3]) == 2 and S().minSubArrayLen(11, [1, 1, 1]) == 0,
    739: lambda: S().dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0],
    84: lambda: S().largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10 and S().largestRectangleArea([2, 4]) == 4,
    42: lambda: S().trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6 and S().trap([4, 2, 0, 3, 2, 5]) == 9,
    94: lambda: S().inorderTraversal(T([1, None, 2, 3])) == [1, 3, 2],
    104: lambda: S().maxDepth(T([3, 9, 20, None, None, 15, 7])) == 3 and S().maxDepth(None) == 0,
    101: lambda: S().isSymmetric(T([1, 2, 2, 3, 4, 4, 3])) and not S().isSymmetric(T([1, 2, 2, None, 3, None, 3])),
    236: lambda: (lambda r: S().lowestCommonAncestor(r, find(r, 5), find(r, 1)).val == 3
                  and S().lowestCommonAncestor(r, find(r, 5), find(r, 4)).val == 5)(T([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])),
    235: lambda: (lambda r: S().lowestCommonAncestor(r, find(r, 2), find(r, 8)).val == 6
                  and S().lowestCommonAncestor(r, find(r, 2), find(r, 4)).val == 2)(T([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])),
    124: lambda: S().maxPathSum(T([-10, 9, 20, None, None, 15, 7])) == 42 and S().maxPathSum(T([-3])) == -3,
    98: lambda: S().isValidBST(T([2, 1, 3])) and not S().isValidBST(T([5, 1, 4, None, None, 3, 6])),
    230: lambda: S().kthSmallest(T([5, 3, 6, 2, 4, None, None, 1]), 3) == 3,
    450: lambda: inorder(S().deleteNode(T([5, 3, 6, 2, 4, None, 7]), 3)) == [2, 4, 5, 6, 7]
                 and inorder(S().deleteNode(T([5, 3, 6, 2, 4, None, 7]), 5)) == [2, 3, 4, 6, 7],
    46: lambda: srt(S().permute([1, 2, 3])) == srt([[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]) and len(S().permute([1, 2, 3])) == 6,
    39: lambda: srt(S().combinationSum([2, 3, 6, 7], 7)) == [[2, 2, 3], [7]],
    78: lambda: len(S().subsets([1, 2, 3])) == 8 and srt(S().subsets([1, 2])) == [[], [1], [1, 2], [2]],
    22: lambda: sorted(S().generateParenthesis(3)) == sorted(["((()))", "(()())", "(())()", "()(())", "()()()"]),
    200: lambda: S().numIslands([list("11000"), list("11000"), list("00100"), list("00011")]) == 3,
    113: lambda: S().pathSum(T([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]), 22) == [[5, 4, 11, 2], [5, 8, 4, 5]],
    70: lambda: [S().climbStairs(n) for n in (1, 2, 3, 5)] == [1, 2, 3, 8],
    300: lambda: S().lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4 and S().lengthOfLIS([7, 7, 7]) == 1,
    322: lambda: S().coinChange([1, 2, 5], 11) == 3 and S().coinChange([2], 3) == -1 and S().coinChange([1], 0) == 0,
    1143: lambda: S().longestCommonSubsequence("abcde", "ace") == 3 and S().longestCommonSubsequence("abc", "def") == 0,
    72: lambda: S().minDistance("horse", "ros") == 3 and S().minDistance("intention", "execution") == 5,
    198: lambda: S().rob([1, 2, 3, 1]) == 4 and S().rob([2, 7, 9, 3, 1]) == 12 and S().rob([5]) == 5,
    121: lambda: S().maxProfit([7, 1, 5, 3, 6, 4]) == 5 and S().maxProfit([7, 6, 4, 3, 1]) == 0,
    122: lambda: S().maxProfit([7, 1, 5, 3, 6, 4]) == 7 and S().maxProfit([1, 2, 3, 4, 5]) == 4,
    53: lambda: S().maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6 and S().maxSubArray([-1]) == -1,
    152: lambda: S().maxProduct([2, 3, -2, 4]) == 6 and S().maxProduct([-2, 0, -1]) == 0 and S().maxProduct([-2, 3, -4]) == 24,
    312: lambda: S().maxCoins([3, 1, 5, 8]) == 167 and S().maxCoins([1, 5]) == 10,
    354: lambda: S().maxEnvelopes([[5, 4], [6, 4], [6, 7], [2, 3]]) == 3 and S().maxEnvelopes([[1, 1], [1, 1]]) == 1,
    33: lambda: S().search([4, 5, 6, 7, 0, 1, 2], 0) == 4 and S().search([4, 5, 6, 7, 0, 1, 2], 3) == -1 and S().search([3, 1], 1) == 1,
    34: lambda: S().searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4] and S().searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1] and S().searchRange([], 0) == [-1, -1],
    4: lambda: S().findMedianSortedArrays([1, 3], [2]) == 2 and S().findMedianSortedArrays([1, 2], [3, 4]) == 2.5,
    560: lambda: S().subarraySum([1, 1, 1], 2) == 2 and S().subarraySum([1, 2, 3], 3) == 2,
    525: lambda: S().findMaxLength([0, 1]) == 2 and S().findMaxLength([0, 1, 0]) == 2 and S().findMaxLength([0, 1, 1, 1, 1, 1, 0, 0, 0]) == 6,
    55: lambda: S().canJump([2, 3, 1, 1, 4]) and not S().canJump([3, 2, 1, 0, 4]),
    56: lambda: S().merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]] and S().merge([[1, 4], [4, 5]]) == [[1, 5]],
    134: lambda: S().canCompleteCircuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3 and S().canCompleteCircuit([2, 3, 4], [3, 4, 3]) == -1,
    136: lambda: S().singleNumber([4, 1, 2, 1, 2]) == 4,
    231: lambda: [S().isPowerOfTwo(n) for n in (1, 16, 3, 0, -8)] == [True, True, False, False, False],
    207: lambda: S().canFinish(2, [[1, 0]]) and not S().canFinish(2, [[1, 0], [0, 1]]),
    208: lambda: (lambda t: (t.insert("apple"), t.search("apple"), t.search("app"), t.startsWith("app"),
                            t.insert("app"), t.search("app")))(NS["Trie"]())[1:] == (True, False, True, None, True),
    2: lambda: LL(S().addTwoNumbers(L([2, 4, 3]), L([5, 6, 4]))) == [7, 0, 8] and LL(S().addTwoNumbers(L([9, 9]), L([1]))) == [0, 0, 1],
    92: lambda: LL(S().reverseBetween(L([1, 2, 3, 4, 5]), 2, 4)) == [1, 4, 3, 2, 5] and LL(S().reverseBetween(L([5]), 1, 1)) == [5],
    169: lambda: S().majorityElement([2, 2, 1, 1, 1, 2, 2]) == 2,
    202: lambda: S().isHappy(19) and not S().isHappy(2),
    # ---- 手撕PDF 新增 ----
    912: lambda: all(S().sortArray(a[:]) == sorted(a) for a in
                     ([5, 2, 3, 1], [5, 1, 1, 2, 0, 0], [1], [], [3, 3, 3, 3], list(range(50, 0, -1)),
                      [7, -2, 9, -2, 0, 7, 7, 1])),
    215: lambda: S().findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5 and S().findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
                 and S().findKthLargest([1] * 50, 7) == 1,
    "singleton": lambda: (lambda C: C() is C() and C._instance is not None)(NS["Singleton"])
                         and _threaded_singleton(NS["Singleton"]),
    5: lambda: S().longestPalindrome("babad") in ("bab", "aba") and S().longestPalindrome("cbbd") == "bb"
               and S().longestPalindrome("a") == "a" and S().longestPalindrome("forgeeksskeegfor") == "geeksskeeg",
    139: lambda: S().wordBreak("leetcode", ["leet", "code"]) and S().wordBreak("applepenapple", ["apple", "pen"])
                 and not S().wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"]),
    239: lambda: S().maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7] and S().maxSlidingWindow([1], 1) == [1]
                 and S().maxSlidingWindow([9, 8, 9, 8], 2) == [9, 9, 9],
    128: lambda: S().longestConsecutive([100, 4, 200, 1, 3, 2]) == 4 and S().longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
                 and S().longestConsecutive([]) == 0,
    234: lambda: S().isPalindrome(L([1, 2, 2, 1])) and not S().isPalindrome(L([1, 2])) and S().isPalindrome(L([1]))
                 and S().isPalindrome(L([1, 2, 3, 2, 1])) and not S().isPalindrome(L([1, 2, 3, 1])),
    142: lambda: (lambda h: (setattr(h.next.next.next, "next", h.next), S().detectCycle(h).val)[1])(L([3, 2, 0, -4])) == 2
                 and S().detectCycle(L([1, 2])) is None
                 and (lambda h: (setattr(h.next, "next", h), S().detectCycle(h))[1] is h)(L([1, 2])),
    25: lambda: LL(S().reverseKGroup(L([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
                and LL(S().reverseKGroup(L([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]
                and LL(S().reverseKGroup(L([1, 2]), 1)) == [1, 2],
    102: lambda: S().levelOrder(T([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]] and S().levelOrder(None) == [],
    105: lambda: (lambda r: _levels(r) == [3, 9, 20, None, None, 15, 7])(S().buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]))
                 and S().buildTree([-1], [-1]).val == -1,
    437: lambda: S().pathSum(T([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1]), 8) == 3
                 and S().pathSum(T([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]), 22) == 3,
    79: lambda: (lambda b: S().exist([r[:] for r in b], "ABCCED") and S().exist([r[:] for r in b], "SEE")
                 and not S().exist([r[:] for r in b], "ABCB"))([list("ABCE"), list("SFCS"), list("ADEE")]),
    131: lambda: srt(S().partition("aab")) == [["a", "a", "b"], ["aa", "b"]] and S().partition("a") == [["a"]],
}

# 另一种写法用同一组用例
ALT_IDS = {42, 53, 206, 21, 347, 94, 300}


def _levels(root):
    """树 -> 层序数组(去掉末尾 None),用于比较构建结果。"""
    out, q = [], deque([root])
    while q:
        n = q.popleft()
        out.append(n.val if n else None)
        if n:
            q.extend([n.left, n.right])
    while out and out[-1] is None:
        out.pop()
    return out


def _threaded_singleton(cls):
    import threading
    cls._instance = None
    got, barrier = [], threading.Barrier(8)

    def worker():
        barrier.wait()
        got.append(cls())

    ts = [threading.Thread(target=worker) for _ in range(8)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return all(x is got[0] for x in got)


def run_one(pid, title, code) -> bool:
    NS.clear()
    NS.update(List=List, Optional=Optional, ListNode=ListNode, TreeNode=TreeNode)
    try:
        exec(compile(code, f"<{pid}>", "exec"), NS)
        if bool(TESTS[pid]()):
            return True
    except Exception as e:  # noqa: BLE001
        print(f"  ✗ #{pid} {title}: {type(e).__name__}: {e}")
    print(f"  ✗ #{pid} {title} 自测失败")
    return False


def selftest(items: list[dict]) -> int:
    fails = 0
    for it in items:
        fails += not run_one(it["id"], it["title"], it["code"])
        if it.get("alt"):
            fails += not run_one(it["id"], it["title"] + "(另一种写法)", it["alt"]["code"])
    alts = {it["id"] for it in items if it.get("alt")}
    assert alts == ALT_IDS, alts ^ ALT_IDS
    return fails


def main() -> int:
    data = parse(SRC.read_text(encoding="utf-8"))
    enrich(data)
    fails = selftest(data["items"])
    n = len(data["items"])
    if fails:
        print(f"自测失败 {fails}/{n},未写出 JSON")
        return 1
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n_alt = sum(1 for it in data["items"] if it.get("alt"))
    print(f"✓ {n} 题 + {n_alt} 个另一种写法自测通过 → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
