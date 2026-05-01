# LC 54. 螺旋矩阵 · Medium · 模拟
"""
🔹 题面
    顺时针螺旋打印矩阵元素。

🔹 直觉(边界收缩)
    维护 top/bottom/left/right 四个边界,每打印一条边后收缩一格,
    遇到 top>bottom 或 left>right 退出。

🔹 复杂度 O(mn) / O(1)
"""


class Solution:
    def spiralOrder(self, m: list[list[int]]) -> list[int]:
        if not m:
            return []
        top, bottom, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
        out: list[int] = []
        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                out.append(m[top][c])
            top += 1
            for r in range(top, bottom + 1):
                out.append(m[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    out.append(m[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    out.append(m[r][left])
                left += 1
        return out


def _test() -> None:
    s = Solution()
    assert s.spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert s.spiralOrder([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    print("✅ p054 通过")


if __name__ == "__main__":
    _test()
