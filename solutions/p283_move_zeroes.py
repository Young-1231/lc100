# LC 283. 移动零 · Easy · 双指针
"""
🔹 题面
    原地把 0 移到末尾,保持非零元素相对顺序。

🔹 直觉
    "快慢指针":slow 指向下一个非零落点,fast 扫描;遇到非零就交换。
    交换比赋零再补零更优(只 1 次写入)。

🔹 复杂度 O(n) / O(1)
"""


class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        slow = 0
        for fast in range(len(nums)):
            if nums[fast]:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                slow += 1


def _test() -> None:
    s = Solution()
    a = [0, 1, 0, 3, 12]
    s.moveZeroes(a)
    assert a == [1, 3, 12, 0, 0]
    a = [0]; s.moveZeroes(a); assert a == [0]
    a = [1, 2, 3]; s.moveZeroes(a); assert a == [1, 2, 3]
    print("✅ p283 通过")


if __name__ == "__main__":
    _test()
