# LC 78. 子集 · Medium · 回溯/位掩码/迭代
"""
🔹 解法对比
    | 方法          | 时间       | 空间   | 备注                   |
    |---------------|------------|--------|------------------------|
    | 迭代倍增 ★   | O(n·2ⁿ)    | O(n·2ⁿ)| 最简洁:ans 反复 ×2     |
    | 回溯(选/不选)| O(n·2ⁿ)   | O(n)   | 通用框架               |
    | 位掩码        | O(n·2ⁿ)    | O(n)   | 用 i 的二进制选元素    |
"""


class Solution:
    # 解法 1:迭代倍增 ★ — O(n·2ⁿ) / O(n·2ⁿ)
    def subsets(self, nums: list[int]) -> list[list[int]]:
        out = [[]]
        for x in nums:
            out += [s + [x] for s in out]
        return out

    # 解法 2:回溯 — O(n·2ⁿ) / O(n)
    def subsets_backtrack(self, nums: list[int]) -> list[list[int]]:
        ans, path = [], []

        def bt(i):
            if i == len(nums):
                ans.append(path[:])
                return
            bt(i + 1)
            path.append(nums[i])
            bt(i + 1)
            path.pop()

        bt(0)
        return ans

    # 解法 3:位掩码 — O(n·2ⁿ) / O(n)
    def subsets_bitmask(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        out = []
        for mask in range(1 << n):
            sub = [nums[i] for i in range(n) if mask & (1 << i)]
            out.append(sub)
        return out


def _test() -> None:
    s = Solution()
    want = sorted(map(sorted, [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]))
    for fn in (s.subsets, s.subsets_backtrack, s.subsets_bitmask):
        assert sorted(map(sorted, fn([1, 2, 3]))) == want
        assert fn([]) == [[]]
    print("✅ p078 通过 3 解法")


if __name__ == "__main__":
    _test()
