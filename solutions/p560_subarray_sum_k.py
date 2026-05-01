# LC 560. 和为 K 的子数组 · Medium · 子串/前缀和
"""
🔹 题面
    返回数组中和为 k 的连续子数组数量(可负)。

🔹 直觉
    令 p[i] 为前缀和,则 p[r]-p[l] = k → p[l] = p[r]-k。
    扫描时维护 "出现过的前缀和 → 次数" 哈希,常数时间统计。

🔹 复杂度 O(n) / O(n)

🔹 踩坑
    - 元素可负,**滑窗不可用**;只能前缀和+哈希。
    - 初始化 cnt[0]=1 表示空前缀,这样能统计从下标 0 起的子数组。
"""
from collections import defaultdict


class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        cnt = defaultdict(int)
        cnt[0] = 1
        s = ans = 0
        for x in nums:
            s += x
            ans += cnt[s - k]
            cnt[s] += 1
        return ans


def _test() -> None:
    s = Solution()
    assert s.subarraySum([1, 1, 1], 2) == 2
    assert s.subarraySum([1, 2, 3], 3) == 2
    assert s.subarraySum([-1, -1, 1], 0) == 1
    print("✅ p560 通过")


if __name__ == "__main__":
    _test()
