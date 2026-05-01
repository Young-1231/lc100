# LC 198. 打家劫舍 · Medium · DP
"""
🔹 题面
    相邻房屋不能同时偷,求最大金额。

🔹 解法对比
    | 方法            | 时间 | 空间 | 备注                  |
    |-----------------|------|------|-----------------------|
    | DP 二维数组     | O(n) | O(n) | f[i] = max(f[i-1], f[i-2]+a[i]) |
    | 滚动两变量 ★   | O(n) | O(1) | 经典空间压缩          |
"""


class Solution:
    # 解法 1:滚动变量 ★ — O(n) / O(1)
    def rob(self, nums: list[int]) -> int:
        a = b = 0
        for x in nums:
            a, b = b, max(b, a + x)
        return b

    # 解法 2:二维 DP 数组 — O(n) / O(n)
    def rob_dp(self, nums: list[int]) -> int:
        if not nums:
            return 0
        n = len(nums)
        f = [0] * (n + 1)
        f[1] = nums[0]
        for i in range(2, n + 1):
            f[i] = max(f[i - 1], f[i - 2] + nums[i - 1])
        return f[n]


def _test() -> None:
    s = Solution()
    cases = [([1, 2, 3, 1], 4), ([2, 7, 9, 3, 1], 12), ([], 0), ([5], 5)]
    for arg, want in cases:
        for fn in (s.rob, s.rob_dp):
            assert fn(arg) == want
    print("✅ p198 通过 2 解法")


if __name__ == "__main__":
    _test()
