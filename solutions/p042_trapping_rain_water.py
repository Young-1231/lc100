# LC 42. 接雨水 · Hard · 双指针 / 单调栈 / DP
"""
🔹 题面
    每根柱子宽 1,数组 height 表示高度,求总接雨水量。

🔹 解法对比
    | 方法              | 时间  | 空间  | 备注                                |
    |-------------------|-------|-------|-------------------------------------|
    | 暴力(每格找两侧)| O(n²) | O(1)  | 思路最直接                          |
    | 前后缀最大数组    | O(n)  | O(n)  | 易理解,空间换时间                  |
    | 双指针 ★         | O(n)  | O(1)  | 面试首选                            |
    | 单调栈            | O(n)  | O(n)  | 凹槽逐层结算,可练单调栈思维        |

🔹 直觉
    某位置可接水 = min(leftMax, rightMax) - height。
    双指针正确性:若 h[l] < h[r],l 处右侧"必有 ≥ h[r] 的墙",
    所以 l 处水位完全由 lmax 决定,可安全推进左指针。
"""
from __future__ import annotations


class Solution:
    # 解法 1:暴力 — O(n²) / O(1)
    def trap_brute(self, h: list[int]) -> int:
        n, ans = len(h), 0
        for i in range(n):
            lmax = max(h[:i + 1])
            rmax = max(h[i:])
            ans += min(lmax, rmax) - h[i]
        return ans

    # 解法 2:前后缀最大数组 — O(n) / O(n)
    def trap_prefix(self, h: list[int]) -> int:
        n = len(h)
        if n < 3:
            return 0
        L = [0] * n
        R = [0] * n
        L[0] = h[0]
        for i in range(1, n):
            L[i] = max(L[i - 1], h[i])
        R[-1] = h[-1]
        for i in range(n - 2, -1, -1):
            R[i] = max(R[i + 1], h[i])
        return sum(min(L[i], R[i]) - h[i] for i in range(n))

    # 解法 3:双指针 ★ — O(n) / O(1)
    def trap(self, h: list[int]) -> int:
        l, r = 0, len(h) - 1
        lmax = rmax = ans = 0
        while l < r:
            if h[l] < h[r]:
                lmax = max(lmax, h[l])
                ans += lmax - h[l]
                l += 1
            else:
                rmax = max(rmax, h[r])
                ans += rmax - h[r]
                r -= 1
        return ans

    # 解法 4:单调栈 — O(n) / O(n)
    def trap_stack(self, h: list[int]) -> int:
        st: list[int] = []
        ans = 0
        for i, x in enumerate(h):
            while st and h[st[-1]] < x:
                bottom = st.pop()
                if not st:
                    break
                left = st[-1]
                w = i - left - 1
                ans += w * (min(h[left], x) - h[bottom])
            st.append(i)
        return ans


def _test() -> None:
    s = Solution()
    cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([], 0),
        ([1], 0),
        ([3, 0, 0, 2, 0, 4], 10),
    ]
    for arg, want in cases:
        for fn in (s.trap, s.trap_brute, s.trap_prefix, s.trap_stack):
            got = fn(arg)
            assert got == want, f"{fn.__name__}({arg}) -> {got} != {want}"
    print("✅ p042 通过 4 解法 × 5 用例")


if __name__ == "__main__":
    _test()
