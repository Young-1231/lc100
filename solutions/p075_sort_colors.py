# LC 75. 颜色分类 · Medium · 三指针(荷兰国旗)
"""
🔹 直觉
    三指针:lo / mid / hi,扫描时
        nums[mid]==0 → swap(lo,mid), lo++, mid++
        nums[mid]==1 → mid++
        nums[mid]==2 → swap(mid,hi), hi--   (此时 mid 不动,因为换来的是未知)
"""


class Solution:
    def sortColors(self, nums: list[int]) -> None:
        lo, mid, hi = 0, 0, len(nums) - 1
        while mid <= hi:
            x = nums[mid]
            if x == 0:
                nums[lo], nums[mid] = nums[mid], nums[lo]
                lo += 1; mid += 1
            elif x == 1:
                mid += 1
            else:
                nums[mid], nums[hi] = nums[hi], nums[mid]
                hi -= 1


def _test() -> None:
    s = Solution()
    a = [2, 0, 2, 1, 1, 0]; s.sortColors(a); assert a == [0, 0, 1, 1, 2, 2]
    a = [2, 0, 1]; s.sortColors(a); assert a == [0, 1, 2]
    a = [0]; s.sortColors(a); assert a == [0]
    print("✅ p075 通过")


if __name__ == "__main__":
    _test()
