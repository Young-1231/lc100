# LC 31. 下一个排列 · Medium · 双指针 + 反转
"""
🔹 直觉(三步)
    1. 从右往左找第一个 nums[i] < nums[i+1] 的 i;若不存在 → 整体已最大,直接反转得最小。
    2. 在 i 右侧从右往左找第一个 > nums[i] 的 j,swap(i, j)。
    3. 反转 i+1 之后的部分(原降序 → 升序,使新排列最接近原值)。
"""


class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        n = len(nums)
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        # 反转 i+1..n-1
        l, r = i + 1, n - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1; r -= 1


def _test() -> None:
    s = Solution()
    a = [1, 2, 3]; s.nextPermutation(a); assert a == [1, 3, 2]
    a = [3, 2, 1]; s.nextPermutation(a); assert a == [1, 2, 3]
    a = [1, 1, 5]; s.nextPermutation(a); assert a == [1, 5, 1]
    a = [1, 3, 2]; s.nextPermutation(a); assert a == [2, 1, 3]
    print("✅ p031 通过")


if __name__ == "__main__":
    _test()
