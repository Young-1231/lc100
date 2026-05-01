# LC 238. 除自身以外数组的乘积 · Medium · 前缀积
"""
🔹 题面
    返回 ans[i] = 除 nums[i] 以外所有数的乘积,要求 O(n),不能用除法。

🔹 直觉
    左前缀积 + 右后缀积。两次遍历,空间利用 ans 复用即 O(1) 额外空间。

🔹 复杂度 O(n) / O(1) 额外空间(ans 不计)

🔹 踩坑
    不能用除法是因为存在 0;并且整体乘积可能溢出语义(题面要求)。
"""


class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        ans = [1] * n
        # 左前缀积:ans[i] = ∏ nums[0..i-1]
        for i in range(1, n):
            ans[i] = ans[i - 1] * nums[i - 1]
        # 右乘累计
        right = 1
        for i in range(n - 1, -1, -1):
            ans[i] *= right
            right *= nums[i]
        return ans


def _test() -> None:
    s = Solution()
    assert s.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert s.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    print("✅ p238 通过")


if __name__ == "__main__":
    _test()
