# LC 300. 最长递增子序列 · Medium · DP / 贪心+二分
"""
🔹 题面
    返回最长严格递增子序列的长度。

🔹 解法对比
    | 方法               | 时间        | 空间 | 备注                        |
    |--------------------|-------------|------|-----------------------------|
    | DP 标准            | O(n²)       | O(n) | f[i] = max{f[j]+1 | a[j]<a[i]} |
    | 贪心 + 二分(patience)★| O(n log n) | O(n) | 维护"长度→最小末尾"           |

🔹 贪心 + 二分思想
    tails[k] = 当前长度为 k+1 的 LIS 的最小末尾。
    新元素 x 用 bisect_left 找位置;若可追加则增加长度。
    注意:tails 不一定是真正的 LIS,但长度正确。
"""
from bisect import bisect_left


class Solution:
    # 解法 1:贪心 + 二分 ★ — O(n log n) / O(n)
    def lengthOfLIS(self, nums: list[int]) -> int:
        tails: list[int] = []
        for x in nums:
            i = bisect_left(tails, x)
            if i == len(tails):
                tails.append(x)
            else:
                tails[i] = x
        return len(tails)

    # 解法 2:DP — O(n²) / O(n)
    def lengthOfLIS_dp(self, nums: list[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        f = [1] * n
        for i in range(1, n):
            for j in range(i):
                if nums[j] < nums[i]:
                    f[i] = max(f[i], f[j] + 1)
        return max(f)


def _test() -> None:
    s = Solution()
    cases = [
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),
        ([0, 1, 0, 3, 2, 3], 4),
        ([7, 7, 7, 7], 1),
        ([], 0),
    ]
    for arg, want in cases:
        for fn in (s.lengthOfLIS, s.lengthOfLIS_dp):
            assert fn(arg) == want
    print("✅ p300 通过 2 解法")


if __name__ == "__main__":
    _test()
