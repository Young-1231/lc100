# LC 72. 编辑距离 · Medium · 多维 DP
"""
🔹 解法对比
    | 方法            | 时间    | 空间   | 备注                  |
    |-----------------|---------|--------|-----------------------|
    | DP 二维 ★      | O(mn)   | O(mn)  | 易理解,可回溯路径    |
    | DP 滚动一维     | O(mn)   | O(min(m,n))| 空间最优          |

🔹 状态
    f[i][j] = word1[:i] → word2[:j] 的最少操作。
"""


class Solution:
    # 解法 1:二维 DP ★ — O(mn) / O(mn)
    def minDistance(self, a: str, b: str) -> int:
        m, n = len(a), len(b)
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            f[i][0] = i
        for j in range(n + 1):
            f[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    f[i][j] = f[i - 1][j - 1]
                else:
                    f[i][j] = 1 + min(f[i - 1][j - 1], f[i - 1][j], f[i][j - 1])
        return f[m][n]

    # 解法 2:滚动一维 — O(mn) / O(n)
    def minDistance_1d(self, a: str, b: str) -> int:
        m, n = len(a), len(b)
        if m < n:
            a, b = b, a
            m, n = n, m
        prev = list(range(n + 1))
        for i in range(1, m + 1):
            cur = [i] + [0] * n
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    cur[j] = prev[j - 1]
                else:
                    cur[j] = 1 + min(prev[j - 1], prev[j], cur[j - 1])
            prev = cur
        return prev[n]


def _test() -> None:
    s = Solution()
    cases = [
        (("horse", "ros"), 3),
        (("intention", "execution"), 5),
        (("", "abc"), 3),
        (("abc", ""), 3),
    ]
    for args, want in cases:
        for fn in (s.minDistance, s.minDistance_1d):
            assert fn(*args) == want
    print("✅ p072 通过 2 解法")


if __name__ == "__main__":
    _test()
