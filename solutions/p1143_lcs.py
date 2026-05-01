# LC 1143. 最长公共子序列 · Medium · 多维 DP
"""
🔹 状态
    f[i][j] = LCS(text1[:i], text2[:j])
    text1[i-1] == text2[j-1] → f[i][j] = f[i-1][j-1] + 1
    否则 f[i][j] = max(f[i-1][j], f[i][j-1])
"""


class Solution:
    def longestCommonSubsequence(self, a: str, b: str) -> int:
        m, n = len(a), len(b)
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    f[i][j] = f[i - 1][j - 1] + 1
                else:
                    f[i][j] = max(f[i - 1][j], f[i][j - 1])
        return f[m][n]


def _test() -> None:
    s = Solution()
    assert s.longestCommonSubsequence("abcde", "ace") == 3
    assert s.longestCommonSubsequence("abc", "abc") == 3
    assert s.longestCommonSubsequence("abc", "def") == 0
    print("✅ p1143 通过")


if __name__ == "__main__":
    _test()
