# LC 136. 只出现一次的数字 · Easy · 位运算
"""
🔹 直觉
    XOR 性质:a^a=0, a^0=a。所有数 XOR 起来,成对的抵消,留下落单的。
"""
from functools import reduce
from operator import xor


class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        return reduce(xor, nums)


def _test() -> None:
    s = Solution()
    assert s.singleNumber([2, 2, 1]) == 1
    assert s.singleNumber([4, 1, 2, 1, 2]) == 4
    assert s.singleNumber([1]) == 1
    print("✅ p136 通过")


if __name__ == "__main__":
    _test()
