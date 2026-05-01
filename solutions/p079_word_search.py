# LC 79. 单词搜索 · Medium · 回溯 + 矩阵
"""
🔹 直觉
    枚举起点 → DFS 四向走;走过的格子原地"涂色"防止重复,回溯时还原。
"""


class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        m, n = len(board), len(board[0])

        def dfs(i, j, k):
            if k == len(word):
                return True
            if i < 0 or j < 0 or i >= m or j >= n or board[i][j] != word[k]:
                return False
            board[i][j] = "#"
            ok = (dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1)
                  or dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1))
            board[i][j] = word[k]
            return ok

        return any(dfs(i, j, 0) for i in range(m) for j in range(n))


def _test() -> None:
    s = Solution()
    b = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    assert s.exist([row[:] for row in b], "ABCCED") is True
    assert s.exist([row[:] for row in b], "SEE") is True
    assert s.exist([row[:] for row in b], "ABCB") is False
    print("✅ p079 通过")


if __name__ == "__main__":
    _test()
