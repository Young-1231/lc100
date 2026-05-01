# LC 152. 乘积最大子数组 · Medium · DP
"""
🔹 题面
    返回乘积最大的连续子数组的乘积。

🔹 解法对比
    | 方法                | 时间 | 空间 | 备注                          |
    |---------------------|------|------|-------------------------------|
    | 双状态 DP(滚动)★ | O(n) | O(1) | 同时维护 fmax / fmin(负数翻转) |
    | DP 数组             | O(n) | O(n) | 同上,但显式存数组             |

🔹 直觉
    维护"截至当前的最大乘积 fmax"和"最小乘积 fmin"。负负得正,
    遇负数时 (fmax * x) 可能成为新的最小,(fmin * x) 反而成为新的最大。
"""


class Solution:
    # 解法 1:双状态 DP 滚动 ★ — O(n) / O(1)
    def maxProduct(self, nums: list[int]) -> int:
        fmax = fmin = ans = nums[0]
        for x in nums[1:]:
            cands = (x, fmax * x, fmin * x)
            fmax = max(cands)
            fmin = min(cands)
            ans = max(ans, fmax)
        return ans

    # 解法 2:DP 数组(更直观)— O(n) / O(n)
    def maxProduct_dp(self, nums: list[int]) -> int:
        n = len(nums)
        mx = nums[:]
        mn = nums[:]
        for i in range(1, n):
            cands = (nums[i], mx[i - 1] * nums[i], mn[i - 1] * nums[i])
            mx[i] = max(cands)
            mn[i] = min(cands)
        return max(mx)


def _test() -> None:
    s = Solution()
    cases = [
        ([2, 3, -2, 4], 6),
        ([-2, 0, -1], 0),
        ([-2, 3, -4], 24),
        ([0, 2], 2),
    ]
    for arg, want in cases:
        for fn in (s.maxProduct, s.maxProduct_dp):
            assert fn(arg) == want
    print("✅ p152 通过 2 解法")


if __name__ == "__main__":
    _test()
