# LC 51. N 皇后 · Hard · 回溯
"""
🔹 直觉
    按行放,每行枚举列;用三个集合记录"已用列"、"已用主对角线 r-c"、"已用副对角线 r+c"。
"""


class Solution:
    def solveNQueens(self, n: int) -> list[list[str]]:
        cols, diag1, diag2 = set(), set(), set()
        ans, board = [], [-1] * n

        def render():
            return [
                "".join("Q" if c == board[r] else "." for c in range(n))
                for r in range(n)
            ]

        def bt(r):
            if r == n:
                ans.append(render())
                return
            for c in range(n):
                if c in cols or (r - c) in diag1 or (r + c) in diag2:
                    continue
                board[r] = c
                cols.add(c); diag1.add(r - c); diag2.add(r + c)
                bt(r + 1)
                cols.remove(c); diag1.remove(r - c); diag2.remove(r + c)

        bt(0)
        return ans


def _test() -> None:
    s = Solution()
    assert len(s.solveNQueens(4)) == 2
    assert len(s.solveNQueens(1)) == 1
    assert len(s.solveNQueens(8)) == 92
    print("✅ p051 通过")


if __name__ == "__main__":
    _test()
