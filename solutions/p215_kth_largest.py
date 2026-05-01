# LC 215. 数组中的第 K 个最大元素 · Medium · 堆 / 快选
"""
🔹 解法对比
    | 方法                | 时间(平均) | 空间       | 备注                       |
    |---------------------|--------------|------------|----------------------------|
    | 排序                | O(n log n)   | O(1) 原地  | 最简单                     |
    | 小顶堆 维持大小 K ★| O(n log k)   | O(k)       | 大数据流首选(在线)       |
    | 快速选择            | O(n) 期望    | O(log n) 栈| 最优期望;最坏 O(n²)       |
"""
import heapq
import random


class Solution:
    # 解法 1:排序 — O(n log n)
    def findKthLargest_sort(self, nums: list[int], k: int) -> int:
        return sorted(nums)[-k]

    # 解法 2:小顶堆 ★ — O(n log k)
    def findKthLargest(self, nums: list[int], k: int) -> int:
        h: list[int] = []
        for x in nums:
            heapq.heappush(h, x)
            if len(h) > k:
                heapq.heappop(h)
        return h[0]

    # 解法 3:快速选择 — O(n) 平均
    def findKthLargest_quick(self, nums: list[int], k: int) -> int:
        nums = nums[:]
        target = len(nums) - k

        def partition(l, r):
            p = random.randint(l, r)
            nums[p], nums[r] = nums[r], nums[p]
            pivot = nums[r]
            store = l
            for i in range(l, r):
                if nums[i] < pivot:
                    nums[store], nums[i] = nums[i], nums[store]
                    store += 1
            nums[store], nums[r] = nums[r], nums[store]
            return store

        l, r = 0, len(nums) - 1
        while True:
            p = partition(l, r)
            if p == target:
                return nums[p]
            if p < target:
                l = p + 1
            else:
                r = p - 1


def _test() -> None:
    s = Solution()
    cases = [
        (([3, 2, 1, 5, 6, 4], 2), 5),
        (([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4),
        (([1], 1), 1),
    ]
    for args, want in cases:
        for fn in (s.findKthLargest, s.findKthLargest_sort, s.findKthLargest_quick):
            assert fn(*args) == want
    print("✅ p215 通过 3 解法")


if __name__ == "__main__":
    _test()
