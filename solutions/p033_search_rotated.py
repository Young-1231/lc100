# LC 33. 搜索旋转排序数组 · Medium · 二分
"""
🔹 直觉
    每一步看 nums[l..mid] 与 nums[mid..r] 哪一段是升序的:
        若左半升序:target 在 [nums[l], nums[mid]) 内 → 走左
        否则:右半必升序,target 在 (nums[mid], nums[r]] 内 → 走右
"""


class Solution:
    def search(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                return m
            if nums[l] <= nums[m]:                # 左半升序
                if nums[l] <= target < nums[m]:
                    r = m - 1
                else:
                    l = m + 1
            else:                                  # 右半升序
                if nums[m] < target <= nums[r]:
                    l = m + 1
                else:
                    r = m - 1
        return -1


def _test() -> None:
    s = Solution()
    assert s.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert s.search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert s.search([1], 0) == -1
    assert s.search([1], 1) == 0
    print("✅ p033 通过")


if __name__ == "__main__":
    _test()
