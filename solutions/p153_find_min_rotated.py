# LC 153. 寻找旋转排序数组中的最小值 · Medium · 二分
"""
🔹 直觉
    比较 nums[mid] 与 nums[r]:
        > nums[r] → 最小在右半,l = mid + 1
        ≤ nums[r] → 最小在左半(含 mid),r = mid
    数组无重复,严格成立。
"""


class Solution:
    def findMin(self, nums: list[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            m = (l + r) // 2
            if nums[m] > nums[r]:
                l = m + 1
            else:
                r = m
        return nums[l]


def _test() -> None:
    s = Solution()
    assert s.findMin([3, 4, 5, 1, 2]) == 1
    assert s.findMin([4, 5, 6, 7, 0, 1, 2]) == 0
    assert s.findMin([11, 13, 15, 17]) == 11
    print("✅ p153 通过")


if __name__ == "__main__":
    _test()
