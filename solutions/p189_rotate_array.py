# LC 189. 轮转数组 · Medium · 数组技巧
"""
🔹 题面
    向右轮转数组 k 步。

🔹 解法对比
    | 方法               | 时间 | 空间 | 备注                  |
    |--------------------|------|------|-----------------------|
    | 借助新数组         | O(n) | O(n) | 思路最直接            |
    | 三次反转 ★        | O(n) | O(1) | 经典技巧,面试首选    |
    | 环状替换           | O(n) | O(1) | 数学优雅,边界细节多  |

🔹 三次反转思路
    1. 整体反转
    2. 反转前 k 个
    3. 反转后 n-k 个
"""
from math import gcd


class Solution:
    # 解法 1:借助新数组 — O(n) / O(n)
    def rotate_extra(self, nums: list[int], k: int) -> None:
        n = len(nums)
        k %= n
        nums[:] = nums[-k:] + nums[:-k]

    # 解法 2:三次反转 ★ — O(n) / O(1)
    def rotate(self, nums: list[int], k: int) -> None:
        n = len(nums)
        k %= n
        nums.reverse()
        nums[:k] = reversed(nums[:k])
        nums[k:] = reversed(nums[k:])

    # 解法 3:环状替换 — O(n) / O(1)
    def rotate_cyclic(self, nums: list[int], k: int) -> None:
        n = len(nums)
        k %= n
        cnt = gcd(k, n)
        for start in range(cnt):
            cur, prev = start, nums[start]
            while True:
                nxt = (cur + k) % n
                nums[nxt], prev = prev, nums[nxt]
                cur = nxt
                if cur == start:
                    break


def _test() -> None:
    s = Solution()
    cases = [
        (([1, 2, 3, 4, 5, 6, 7], 3), [5, 6, 7, 1, 2, 3, 4]),
        (([-1, -100, 3, 99], 2), [3, 99, -1, -100]),
        (([1, 2], 3), [2, 1]),
    ]
    for (arr, k), want in cases:
        for fn in (s.rotate, s.rotate_extra, s.rotate_cyclic):
            a = arr[:]
            fn(a, k)
            assert a == want, f"{fn.__name__}({arr}, {k}) -> {a}"
    print("✅ p189 通过 3 解法")


if __name__ == "__main__":
    _test()
