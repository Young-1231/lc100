# LC 1. 两数之和 · Easy · 哈希
# https://leetcode.cn/problems/two-sum/
"""
🔹 题面
    给定 nums 和 target,返回两数下标使其和为 target,假设有且仅有一个解。

🔹 解法对比
    | 方法           | 时间       | 空间   | 备注                       |
    |----------------|------------|--------|----------------------------|
    | 暴力双循环     | O(n²)      | O(1)   | 简单直接                   |
    | 排序 + 双指针  | O(n log n) | O(n)   | 需保留原下标               |
    | 一遍哈希 ★    | O(n)       | O(n)   | 面试默写解法               |

🔹 直觉
    枚举 x,只需问"之前是否见过 target - x"。set/dict 是常数时间问答机。

🔹 踩坑
    - 必须先查表再写入,避免同一元素自己配自己。
    - 题目假设唯一解;若多解需返回全部,需把 dict[val] 改 list。

🔹 同类
    167(已排序双指针)、653(BST 双指针)
"""
from __future__ import annotations


class Solution:
    # 解法 1:暴力 — O(n²) / O(1)
    def twoSum_brute(self, nums: list[int], target: int) -> list[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

    # 解法 2:排序 + 双指针 — O(n log n) / O(n)
    # 把 (val, idx) 排序后用左右指针;命中后返回原下标
    def twoSum_two_pointer(self, nums: list[int], target: int) -> list[int]:
        idx = sorted(range(len(nums)), key=lambda i: nums[i])
        l, r = 0, len(nums) - 1
        while l < r:
            s = nums[idx[l]] + nums[idx[r]]
            if s == target:
                return sorted([idx[l], idx[r]])
            if s < target:
                l += 1
            else:
                r -= 1
        return []

    # 解法 3:一遍哈希 ★  — O(n) / O(n)
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for i, x in enumerate(nums):
            if (j := seen.get(target - x)) is not None:
                return [j, i]
            seen[x] = i
        return []


def _test() -> None:
    s = Solution()
    cases = [
        (([2, 7, 11, 15], 9), [0, 1]),
        (([3, 2, 4], 6), [1, 2]),
        (([3, 3], 6), [0, 1]),
        (([-1, -2, -3, -4, -5], -8), [2, 4]),
    ]
    for args, want in cases:
        for fn in (s.twoSum, s.twoSum_brute, s.twoSum_two_pointer):
            got = fn(*args)
            assert got == want, f"{fn.__name__}{args} -> {got} != {want}"
    print(f"✅ p001 通过 {len(cases)} 用例 × 3 解法")


if __name__ == "__main__":
    _test()
