# LC 11. 盛最多水的容器 · Medium · 双指针
"""
🔹 题面
    两条垂线与 x 轴构成容器,选两条使盛水最多。area = (j-i)*min(h[i],h[j])。

🔹 解法对比
    | 方法            | 时间   | 空间  | 备注                            |
    |-----------------|--------|-------|---------------------------------|
    | 暴力枚举两线对  | O(n²)  | O(1)  | 思路直接                        |
    | 双指针贪心 ★   | O(n)   | O(1)  | 移动较矮一侧才有可能更优        |

🔹 双指针正确性
    若移动较高一侧:宽度减小,高度仍受较矮限制,面积只会减小。
    所以放弃较矮一侧不会错过最优解(贪心反证)。
"""


class Solution:
    # 解法 1:暴力 — O(n²) / O(1)
    def maxArea_brute(self, h: list[int]) -> int:
        n, best = len(h), 0
        for i in range(n):
            for j in range(i + 1, n):
                best = max(best, (j - i) * min(h[i], h[j]))
        return best

    # 解法 2:双指针 ★  — O(n) / O(1)
    def maxArea(self, h: list[int]) -> int:
        i, j, best = 0, len(h) - 1, 0
        while i < j:
            best = max(best, (j - i) * min(h[i], h[j]))
            if h[i] < h[j]:
                i += 1
            else:
                j -= 1
        return best


def _test() -> None:
    s = Solution()
    cases = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
    ]
    for arg, want in cases:
        for fn in (s.maxArea, s.maxArea_brute):
            assert fn(arg) == want
    print("✅ p011 通过 2 解法")


if __name__ == "__main__":
    _test()
