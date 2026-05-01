# LC 74. 搜索二维矩阵 · Medium · 二分
"""
🔹 直觉
    把 m×n 矩阵当成一根升序数组,下标 idx → (idx // n, idx % n)。
"""


class Solution:
    def searchMatrix(self, m: list[list[int]], target: int) -> bool:
        if not m or not m[0]:
            return False
        rows, cols = len(m), len(m[0])
        l, r = 0, rows * cols - 1
        while l <= r:
            mid = (l + r) // 2
            v = m[mid // cols][mid % cols]
            if v == target:
                return True
            if v < target:
                l = mid + 1
            else:
                r = mid - 1
        return False


def _test() -> None:
    s = Solution()
    M = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    assert s.searchMatrix(M, 3) is True
    assert s.searchMatrix(M, 13) is False
    assert s.searchMatrix([[1]], 1) is True
    print("✅ p074 通过")


if __name__ == "__main__":
    _test()
