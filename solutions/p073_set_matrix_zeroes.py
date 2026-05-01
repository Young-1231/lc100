# LC 73. 矩阵置零 · Medium · 矩阵原地标记
"""
🔹 题面
    若 m[i][j]=0,把第 i 行和第 j 列全部置零。

🔹 解法对比
    | 方法                | 时间   | 空间    | 备注                          |
    |---------------------|--------|---------|-------------------------------|
    | 标记数组(行/列)   | O(mn)  | O(m+n)  | 直观                          |
    | 第 0 行/列做标记 ★  | O(mn)  | O(1)    | 单独保存"首行/首列是否含 0"   |

🔹 直觉
    用第 0 行 / 第 0 列做标记位;但要单独保存"第 0 行 / 第 0 列本身是否含 0"。
"""


class Solution:
    # 解法 1:O(1) 空间 ★
    def setZeroes(self, m: list[list[int]]) -> None:
        rows, cols = len(m), len(m[0])
        first_row_zero = any(m[0][c] == 0 for c in range(cols))
        first_col_zero = any(m[r][0] == 0 for r in range(rows))
        for r in range(1, rows):
            for c in range(1, cols):
                if m[r][c] == 0:
                    m[r][0] = m[0][c] = 0
        for r in range(1, rows):
            for c in range(1, cols):
                if m[r][0] == 0 or m[0][c] == 0:
                    m[r][c] = 0
        if first_row_zero:
            for c in range(cols):
                m[0][c] = 0
        if first_col_zero:
            for r in range(rows):
                m[r][0] = 0

    # 解法 2:用 set 记录要清零的行/列 — O(mn) / O(m+n)
    def setZeroes_sets(self, m: list[list[int]]) -> None:
        rows, cols = len(m), len(m[0])
        zr, zc = set(), set()
        for r in range(rows):
            for c in range(cols):
                if m[r][c] == 0:
                    zr.add(r); zc.add(c)
        for r in range(rows):
            for c in range(cols):
                if r in zr or c in zc:
                    m[r][c] = 0


def _test() -> None:
    s = Solution()
    cases = [
        ([[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
        ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]], [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]),
    ]
    for arg, want in cases:
        for fn in (s.setZeroes, s.setZeroes_sets):
            a = [row[:] for row in arg]
            fn(a)
            assert a == want
    print("✅ p073 通过 2 解法")


if __name__ == "__main__":
    _test()
