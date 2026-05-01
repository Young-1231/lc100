# LC 35. 搜索插入位置 · Easy · 二分
"""
🔹 直觉
    标准 lower_bound:返回第一个 ≥ target 的位置。
"""


class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums)
        while l < r:
            m = (l + r) // 2
            if nums[m] < target:
                l = m + 1
            else:
                r = m
        return l


def _test() -> None:
    s = Solution()
    assert s.searchInsert([1, 3, 5, 6], 5) == 2
    assert s.searchInsert([1, 3, 5, 6], 2) == 1
    assert s.searchInsert([1, 3, 5, 6], 7) == 4
    assert s.searchInsert([1, 3, 5, 6], 0) == 0
    print("✅ p035 通过")


if __name__ == "__main__":
    _test()
