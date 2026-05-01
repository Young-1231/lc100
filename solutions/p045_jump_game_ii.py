# LC 45. 跳跃游戏 II · Medium · 贪心 / BFS
"""
🔹 题面
    返回到达末尾的最少跳跃次数。

🔹 解法对比
    | 方法           | 时间  | 空间 | 备注                  |
    |----------------|-------|------|-----------------------|
    | DP             | O(n²) | O(n) | f[i] = 到 i 的最少步  |
    | 贪心层次BFS ★ | O(n)  | O(1) | 维护当前层 end / 下一层 farthest |
"""


class Solution:
    # 解法 1:贪心层次 BFS ★ — O(n) / O(1)
    def jump(self, nums: list[int]) -> int:
        steps = end = farthest = 0
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == end:
                steps += 1
                end = farthest
        return steps

    # 解法 2:DP — O(n²) / O(n)
    def jump_dp(self, nums: list[int]) -> int:
        n = len(nums)
        INF = float("inf")
        f = [INF] * n
        f[0] = 0
        for i in range(n):
            for j in range(1, nums[i] + 1):
                if i + j < n:
                    f[i + j] = min(f[i + j], f[i] + 1)
        return int(f[-1])


def _test() -> None:
    s = Solution()
    cases = [([2, 3, 1, 1, 4], 2), ([2, 3, 0, 1, 4], 2), ([1], 0)]
    for arg, want in cases:
        for fn in (s.jump, s.jump_dp):
            assert fn(arg) == want
    print("✅ p045 通过 2 解法")


if __name__ == "__main__":
    _test()
