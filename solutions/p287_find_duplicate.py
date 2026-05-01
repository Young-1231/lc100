# LC 287. 寻找重复数 · Medium · Floyd 链表环
"""
🔹 题面
    长度 n+1 数组,值 ∈ [1,n],只有一个数重复(可重复多次)。要求 O(1) 空间、不修改原数组。

🔹 直觉(把数组当作"函数")
    把 i 视作"指针",nums[i] 视作"它指向的下一个位置"。
    存在重复 ⟺ 这张图存在环。
    用 Floyd 龟兔找入环点(参考 LC 142),即重复值。
"""


class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        slow = fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow


def _test() -> None:
    s = Solution()
    assert s.findDuplicate([1, 3, 4, 2, 2]) == 2
    assert s.findDuplicate([3, 1, 3, 4, 2]) == 3
    assert s.findDuplicate([1, 1]) == 1
    assert s.findDuplicate([1, 1, 2]) == 1
    print("✅ p287 通过")


if __name__ == "__main__":
    _test()
