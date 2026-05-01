# LC 76. 最小覆盖子串 · Hard · 滑动窗口
"""
🔹 题面
    在 s 中找出包含 t 全部字符(含重复)的最短子串。

🔹 解法对比
    | 方法                            | 时间          | 空间        | 备注                |
    |---------------------------------|---------------|-------------|---------------------|
    | 暴力枚举所有子串                | O(n²·|Σ|)     | O(|Σ|)      | 仅做正确性参考      |
    | 滑动窗口(Counter 比较)        | O(n·|Σ|)      | O(|Σ|)      | 直观,常数大        |
    | 滑动窗口 + valid 计数 ★        | O(n + |t|)    | O(|Σ|)      | 工程最优            |

🔹 直觉
    维护 need(目标计数),valid(已满足"种数")。
    r 扩大直到 valid == 不同字符数;l 收缩直到刚好不满足。
"""
from collections import Counter


class Solution:
    # 解法 1:滑窗 + valid 计数 ★  — O(n + |t|) / O(|Σ|)
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""
        need = Counter(t)
        kinds = len(need)
        have: dict[str, int] = {}
        valid = 0
        l = 0
        best_l, best_len = 0, float("inf")
        for r, c in enumerate(s):
            if c in need:
                have[c] = have.get(c, 0) + 1
                if have[c] == need[c]:
                    valid += 1
            while valid == kinds:
                if r - l + 1 < best_len:
                    best_l, best_len = l, r - l + 1
                lc = s[l]
                if lc in need:
                    if have[lc] == need[lc]:
                        valid -= 1
                    have[lc] -= 1
                l += 1
        return "" if best_len == float("inf") else s[best_l:best_l + best_len]

    # 解法 2:滑窗 + Counter 直接对比 — O(n·|Σ|)
    def minWindow_naive(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""
        need = Counter(t)
        win: Counter = Counter()
        l = 0
        best = (float("inf"), 0, 0)
        for r, c in enumerate(s):
            win[c] += 1
            while all(win[k] >= v for k, v in need.items()):
                if r - l + 1 < best[0]:
                    best = (r - l + 1, l, r + 1)
                win[s[l]] -= 1
                l += 1
        return "" if best[0] == float("inf") else s[best[1]:best[2]]


def _test() -> None:
    s = Solution()
    cases = [
        (("ADOBECODEBANC", "ABC"), "BANC"),
        (("a", "a"), "a"),
        (("a", "aa"), ""),
    ]
    for args, want in cases:
        for fn in (s.minWindow, s.minWindow_naive):
            assert fn(*args) == want
    print("✅ p076 通过 2 解法")


if __name__ == "__main__":
    _test()
