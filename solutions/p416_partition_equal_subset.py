# LC 416. 分割等和子集 · Medium · 0-1 背包
"""
🔹 直觉
    总和奇数直接 False。否则求是否存在子集和 = total // 2。
    一维 0-1 背包,容量 = target,逆序更新。

🔹 状态
    f[v] 是否可凑出和 v;f[v] |= f[v - x]。
"""


class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        s = sum(nums)
        if s & 1:
            return False
        target = s // 2
        f = [False] * (target + 1)
        f[0] = True
        for x in nums:
            for v in range(target, x - 1, -1):
                f[v] = f[v] or f[v - x]
        return f[target]


def _test() -> None:
    s = Solution()
    assert s.canPartition([1, 5, 11, 5]) is True
    assert s.canPartition([1, 2, 3, 5]) is False
    assert s.canPartition([1, 1]) is True
    print("✅ p416 通过")


if __name__ == "__main__":
    _test()
