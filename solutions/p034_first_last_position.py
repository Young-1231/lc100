# LC 34. 在排序数组中查找元素的第一个和最后一个位置 · Medium · 二分
"""
🔹 直觉
    两次 lower_bound:
        first = bisect_left(nums, target)
        last  = bisect_right(nums, target) - 1
"""
from bisect import bisect_left, bisect_right


class Solution:
    def searchRange(self, nums: list[int], target: int) -> list[int]:
        l = bisect_left(nums, target)
        if l == len(nums) or nums[l] != target:
            return [-1, -1]
        return [l, bisect_right(nums, target) - 1]


def _test() -> None:
    s = Solution()
    assert s.searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert s.searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
    assert s.searchRange([], 0) == [-1, -1]
    print("✅ p034 通过")


if __name__ == "__main__":
    _test()
