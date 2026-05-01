# LC 347. 前 K 个高频元素 · Medium · 堆 / 桶排序
"""
🔹 题面
    返回出现频率前 K 高的元素。

🔹 解法对比
    | 方法                 | 时间      | 空间 | 备注                       |
    |----------------------|-----------|------|----------------------------|
    | 排序                 | O(n log n)| O(n) | 简单                       |
    | 小顶堆 维持大小 K ★ | O(n log k)| O(n+k)| 大数据流首选                |
    | 桶排序(频次桶)     | O(n)      | O(n) | 频次范围 ≤ n,严格 O(n)    |
"""
from collections import Counter
import heapq


class Solution:
    # 解法 1:小顶堆 ★ — O(n log k)
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        cnt = Counter(nums)
        return [x for x, _ in heapq.nlargest(k, cnt.items(), key=lambda kv: kv[1])]

    # 解法 2:桶排序 — O(n)
    def topKFrequent_bucket(self, nums: list[int], k: int) -> list[int]:
        cnt = Counter(nums)
        buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
        for x, c in cnt.items():
            buckets[c].append(x)
        out: list[int] = []
        for f in range(len(buckets) - 1, 0, -1):
            for x in buckets[f]:
                out.append(x)
                if len(out) == k:
                    return out
        return out


def _test() -> None:
    s = Solution()
    cases = [
        (([1, 1, 1, 2, 2, 3], 2), {1, 2}),
        (([1], 1), {1}),
        (([4, 1, -1, 2, -1, 2, 3], 2), {-1, 2}),
    ]
    for args, want in cases:
        for fn in (s.topKFrequent, s.topKFrequent_bucket):
            assert set(fn(*args)) == want
    print("✅ p347 通过 2 解法")


if __name__ == "__main__":
    _test()
