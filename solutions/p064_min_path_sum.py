# LC 64. 最小路径和 · Medium · 多维 DP
"""
🔹 状态
    f[i][j] = grid[i][j] + min(f[i-1][j], f[i][j-1])
"""


class Solution:
    def minPathSum(self, g: list[list[int]]) -> int:
        m, n = len(g), len(g[0])
        f = list(g[0])
        for j in range(1, n):
            f[j] += f[j - 1]
        for i in range(1, m):
            f[0] += g[i][0]
            for j in range(1, n):
                f[j] = g[i][j] + min(f[j], f[j - 1])
        return f[-1]


def _test() -> None:
    s = Solution()
    assert s.minPathSum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    assert s.minPathSum([[1, 2, 3], [4, 5, 6]]) == 12
    print("✅ p064 通过")


if __name__ == "__main__":
    _test()
