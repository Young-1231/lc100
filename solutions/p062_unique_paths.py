# LC 62. 不同路径 · Medium · 多维 DP
"""
🔹 直觉
    f[i][j] = f[i-1][j] + f[i][j-1];可滚动到一维。
    数学解:C(m+n-2, m-1)。
"""


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        f = [1] * n
        for _ in range(1, m):
            for j in range(1, n):
                f[j] += f[j - 1]
        return f[-1]


def _test() -> None:
    s = Solution()
    assert s.uniquePaths(3, 7) == 28
    assert s.uniquePaths(3, 2) == 3
    assert s.uniquePaths(1, 1) == 1
    print("✅ p062 通过")


if __name__ == "__main__":
    _test()
