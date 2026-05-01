# LC 46. 全排列 · Medium · 回溯
"""
🔹 题面
    返回 nums(无重复)的全部排列。

🔹 解法对比
    | 方法           | 时间    | 空间   | 备注                  |
    |----------------|---------|--------|-----------------------|
    | 回溯 + used ★ | O(n·n!) | O(n)   | 通用模板               |
    | 交换法回溯     | O(n·n!) | O(n)   | 原地不需 used,常数更优 |
"""


class Solution:
    # 解法 1:回溯 + used ★ — O(n·n!) / O(n)
    def permute(self, nums: list[int]) -> list[list[int]]:
        n, ans = len(nums), []
        path, used = [], [False] * n

        def bt():
            if len(path) == n:
                ans.append(path[:])
                return
            for i in range(n):
                if used[i]:
                    continue
                used[i] = True
                path.append(nums[i])
                bt()
                path.pop()
                used[i] = False

        bt()
        return ans

    # 解法 2:交换法回溯 — O(n·n!) / O(n)
    def permute_swap(self, nums: list[int]) -> list[list[int]]:
        nums = nums[:]
        ans, n = [], len(nums)

        def bt(i):
            if i == n:
                ans.append(nums[:])
                return
            for j in range(i, n):
                nums[i], nums[j] = nums[j], nums[i]
                bt(i + 1)
                nums[i], nums[j] = nums[j], nums[i]

        bt(0)
        return ans


def _test() -> None:
    s = Solution()
    want = sorted([[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
    for fn in (s.permute, s.permute_swap):
        assert sorted(fn([1, 2, 3])) == want
        assert fn([1]) == [[1]]
    print("✅ p046 通过 2 解法")


if __name__ == "__main__":
    _test()
