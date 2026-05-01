# LC 128. 最长连续序列 · Medium · 哈希
"""
🔹 题面
    O(n) 找出未排序数组中最长连续元素序列长度。

🔹 直觉
    将数组扔进 set。只从"序列起点"出发计数(x-1 不在 set 中),保证每个元素最多被
    访问 2 次,均摊 O(n)。

🔹 复杂度  O(n) / O(n)

🔹 踩坑
    - 必须先判断 x-1 not in S,否则 O(n²)。
    - 重复元素 set 自动去重,无需特别处理。
"""


class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        S = set(nums)
        best = 0
        for x in S:
            if x - 1 in S:
                continue            # 不是序列起点,跳过
            y = x
            while y + 1 in S:
                y += 1
            best = max(best, y - x + 1)
        return best


def _test() -> None:
    s = Solution()
    assert s.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
    assert s.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert s.longestConsecutive([]) == 0
    print("✅ p128 通过")


if __name__ == "__main__":
    _test()
