# LC 41. 缺失的第一个正数 · Hard · 原地哈希
"""
🔹 题面
    O(n) 时间,O(1) 额外空间,找最小缺失的正整数。

🔹 解法对比
    | 方法                | 时间  | 空间  | 备注                           |
    |---------------------|-------|-------|--------------------------------|
    | 排序后扫            | O(n log n) | O(1) | 不满足"O(n) 时间"严格要求      |
    | 哈希 set            | O(n)  | O(n)  | 不满足"O(1) 空间"严格要求      |
    | 原地标记(取反)    | O(n)  | O(1)  | 把"出现过 v"转化为 nums[v-1] 取负 |
    | 原地置换 ★         | O(n)  | O(1)  | 把 v 放到下标 v-1 处            |

🔹 置换法直觉
    答案一定在 [1, n+1]。把值 v ∈ [1,n] 放到下标 v-1 处:
        while 1 ≤ nums[i] ≤ n and nums[nums[i]-1] != nums[i]:
            swap(nums[i], nums[nums[i]-1])
    扫描:第一个 nums[i] != i+1 的位置 → 答案 i+1;若全对 → 答案 n+1。
"""


class Solution:
    # 解法 1:原地置换 ★ — O(n) / O(1)
    def firstMissingPositive(self, nums: list[int]) -> int:
        n = len(nums)
        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                j = nums[i] - 1
                nums[i], nums[j] = nums[j], nums[i]
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1

    # 解法 2:原地标记取负 — O(n) / O(1)
    # 第一遍把 ≤0 与 >n 的替换为 n+1;第二遍把"出现过 v"对应的 nums[v-1] 取负;
    # 第三遍找第一个 > 0 的位置即缺失值。
    def firstMissingPositive_mark(self, nums: list[int]) -> int:
        n = len(nums)
        for i in range(n):
            if nums[i] <= 0:
                nums[i] = n + 1
        for i in range(n):
            v = abs(nums[i])
            if v <= n:
                nums[v - 1] = -abs(nums[v - 1])
        for i in range(n):
            if nums[i] > 0:
                return i + 1
        return n + 1


def _test() -> None:
    s = Solution()
    cases = [
        ([1, 2, 0], 3),
        ([3, 4, -1, 1], 2),
        ([7, 8, 9, 11, 12], 1),
        ([1], 2),
        ([2, 1], 3),
    ]
    for arg, want in cases:
        for fn in (s.firstMissingPositive, s.firstMissingPositive_mark):
            assert fn(arg[:]) == want
    print("✅ p041 通过 2 解法")


if __name__ == "__main__":
    _test()
