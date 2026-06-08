"""每道题的标准模板。复制此文件,改文件名为 pXXX_xxx.py。

文件命名:p<编号3位>_<下划线英文名>.py,例如 p001_two_sum.py。
"""
# ============================================================
# 题号 / 题名 / 难度 / 标签
# 链接: https://leetcode.cn/problems/two-sum/
# ============================================================
"""
🔹 题面
    输入: nums=[2,7,11,15], target=9
    输出: [0,1]

🔹 直觉
    用一句话讲清楚为什么这样做。

🔹 解法演进
    解法1 暴力        O(n^2)  / O(1)
    解法2 排序+双指针  O(n log n) / O(n)
    解法3 哈希一遍    O(n)   / O(n)  ← 最优

🔹 踩坑
    - 同一元素不能用两次
    - 索引顺序

🔹 同类变体
    167. 两数之和 II - 已排序
    653. 两数之和 IV - BST
"""
from __future__ import annotations


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for i, x in enumerate(nums):
            if (j := seen.get(target - x)) is not None:
                return [j, i]
            seen[x] = i
        return []


# ---------- 自测 ----------
def _test() -> None:
    s = Solution()
    cases = [
        (([2, 7, 11, 15], 9), [0, 1]),
        (([3, 2, 4], 6), [1, 2]),
        (([3, 3], 6), [0, 1]),
    ]
    for (args, expect) in cases:
        got = s.twoSum(*args)
        assert got == expect, f"{args} -> {got} != {expect}"
    print(f"✅ {__file__.split('/')[-1]} 全部通过 ({len(cases)} 用例)")


if __name__ == "__main__":
    _test()
