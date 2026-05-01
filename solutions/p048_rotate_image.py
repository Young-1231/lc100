# LC 48. 旋转图像 · Medium · 矩阵
"""
🔹 题面
    将 n×n 矩阵原地顺时针旋转 90°。

🔹 直觉(转置 + 行翻转)
    顺时针 90° = 主对角线转置 + 每行反转。
    逆时针 90° = 副对角线转置 = 主转置 + 每列反转。

🔹 复杂度 O(n²) / O(1)
"""


class Solution:
    def rotate(self, m: list[list[int]]) -> None:
        n = len(m)
        for i in range(n):
            for j in range(i + 1, n):
                m[i][j], m[j][i] = m[j][i], m[i][j]
        for row in m:
            row.reverse()


def _test() -> None:
    s = Solution()
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    s.rotate(a)
    assert a == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    a = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
    s.rotate(a)
    assert a == [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]
    print("✅ p048 通过")


if __name__ == "__main__":
    _test()
