# LC 53. 最大子数组和 · Medium · DP / 分治
"""
🔹 题面
    返回连续子数组最大和。

🔹 解法对比
    | 方法              | 时间       | 空间   | 备注                            |
    |-------------------|------------|--------|---------------------------------|
    | 暴力枚举所有区间  | O(n²)      | O(1)   | 容易写错(累加 vs 重新算)      |
    | 前缀和 + 极值     | O(n)       | O(n)   | 等价于"前缀和减去之前最小"      |
    | Kadane DP ★      | O(n)       | O(1)   | 一次扫描,空间最优              |
    | 分治              | O(n log n) | O(log n) | 经典分治套路(线段树思路)    |

🔹 Kadane 直觉
    f(i) = max(nums[i], f(i-1) + nums[i])
    "前面累计到我这,要么和我搭伙,要么我重新开始。"
"""


class Solution:
    # 解法 1:Kadane DP ★ — O(n) / O(1)
    def maxSubArray(self, nums: list[int]) -> int:
        cur = best = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)
            best = max(best, cur)
        return best

    # 解法 2:前缀和 + 维护历史最小前缀 — O(n) / O(1)
    def maxSubArray_prefix(self, nums: list[int]) -> int:
        s, min_pre, best = 0, 0, nums[0]
        for x in nums:
            s += x
            best = max(best, s - min_pre)
            min_pre = min(min_pre, s)
        return best

    # 解法 3:分治 — O(n log n) / O(log n)
    def maxSubArray_divide(self, nums: list[int]) -> int:
        def solve(l, r):
            if l == r:
                return nums[l], nums[l], nums[l], nums[l]
            m = (l + r) // 2
            l_total, l_left, l_right, l_max = solve(l, m)
            r_total, r_left, r_right, r_max = solve(m + 1, r)
            total = l_total + r_total
            left = max(l_left, l_total + r_left)
            right = max(r_right, r_total + l_right)
            best = max(l_max, r_max, l_right + r_left)
            return total, left, right, best
        return solve(0, len(nums) - 1)[3]


def _test() -> None:
    s = Solution()
    cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1], 1),
        ([5, 4, -1, 7, 8], 23),
        ([-1, -2], -1),
    ]
    for arg, want in cases:
        for fn in (s.maxSubArray, s.maxSubArray_prefix, s.maxSubArray_divide):
            assert fn(arg) == want, f"{fn.__name__} {arg}"
    print("✅ p053 通过 3 解法")


if __name__ == "__main__":
    _test()
