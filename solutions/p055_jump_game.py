# LC 55. 跳跃游戏 · Medium · 贪心
"""
🔹 题面
    站在 0,nums[i] 表示从 i 最远可跳的步数,问能否跳到末尾。

🔹 解法对比
    | 方法     | 时间 | 空间 | 备注                              |
    |----------|------|------|-----------------------------------|
    | DP       | O(n²)| O(n) | f[i] = 是否可达                    |
    | 贪心 ★  | O(n) | O(1) | 维护"已知可达最远",超出即失败    |
"""


class Solution:
    # 解法 1:贪心 ★ — O(n) / O(1)
    def canJump(self, nums: list[int]) -> bool:
        reach = 0
        for i, x in enumerate(nums):
            if i > reach:
                return False
            reach = max(reach, i + x)
        return True

    # 解法 2:DP — O(n²) / O(n)
    def canJump_dp(self, nums: list[int]) -> bool:
        n = len(nums)
        f = [False] * n
        f[0] = True
        for i in range(n):
            if not f[i]:
                continue
            for j in range(1, nums[i] + 1):
                if i + j < n:
                    f[i + j] = True
                if i + j >= n - 1:
                    return True
        return f[n - 1]


def _test() -> None:
    s = Solution()
    cases = [([2, 3, 1, 1, 4], True), ([3, 2, 1, 0, 4], False), ([0], True)]
    for arg, want in cases:
        for fn in (s.canJump, s.canJump_dp):
            assert fn(arg) is want
    print("✅ p055 通过 2 解法")


if __name__ == "__main__":
    _test()
