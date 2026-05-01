# LC 84. 柱状图中最大的矩形 · Hard · 单调栈
"""
🔹 解法对比
    | 方法            | 时间   | 空间  | 备注                       |
    |-----------------|--------|-------|----------------------------|
    | 暴力枚举区间    | O(n²)  | O(1)  | n ≤ 10⁴ 可过                |
    | 单调栈 ★       | O(n)   | O(n)  | 经典递增栈 + 两哨兵         |
"""


class Solution:
    # 解法 1:暴力 — O(n²) / O(1)
    def largestRectangleArea_brute(self, h: list[int]) -> int:
        n, ans = len(h), 0
        for i in range(n):
            mn = h[i]
            for j in range(i, n):
                mn = min(mn, h[j])
                ans = max(ans, mn * (j - i + 1))
        return ans

    # 解法 2:单调栈 ★ — O(n) / O(n)
    def largestRectangleArea(self, h: list[int]) -> int:
        h = [0] + h + [0]
        st: list[int] = []
        ans = 0
        for i, x in enumerate(h):
            while st and h[st[-1]] > x:
                top = st.pop()
                w = i - st[-1] - 1
                ans = max(ans, h[top] * w)
            st.append(i)
        return ans


def _test() -> None:
    s = Solution()
    cases = [
        ([2, 1, 5, 6, 2, 3], 10),
        ([2, 4], 4),
        ([1], 1),
        ([1, 1], 2),
    ]
    for arg, want in cases:
        for fn in (s.largestRectangleArea, s.largestRectangleArea_brute):
            assert fn(arg) == want
    print("✅ p084 通过 2 解法")


if __name__ == "__main__":
    _test()
