# LC 5. 最长回文子串 · Medium · 中心扩展 / DP / Manacher
"""
🔹 解法对比
    | 方法            | 时间   | 空间   | 备注                                  |
    |-----------------|--------|--------|---------------------------------------|
    | DP              | O(n²)  | O(n²)  | f[i][j] = f[i+1][j-1] && s[i]==s[j]   |
    | 中心扩展 ★     | O(n²)  | O(1)   | 面试默写,常数小                       |
    | Manacher        | O(n)   | O(n)   | 极致最优;实现细节多                  |
"""


class Solution:
    # 解法 1:中心扩展 ★ — O(n²) / O(1)
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""

        def expand(l, r):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1; r += 1
            return l + 1, r - 1

        bl, br = 0, 0
        for i in range(len(s)):
            for l0, r0 in (expand(i, i), expand(i, i + 1)):
                if r0 - l0 > br - bl:
                    bl, br = l0, r0
        return s[bl:br + 1]

    # 解法 2:DP — O(n²) / O(n²)
    def longestPalindrome_dp(self, s: str) -> str:
        n = len(s)
        if n < 2:
            return s
        f = [[False] * n for _ in range(n)]
        for i in range(n):
            f[i][i] = True
        bl, blen = 0, 1
        for L in range(2, n + 1):
            for i in range(n - L + 1):
                j = i + L - 1
                if s[i] != s[j]:
                    continue
                if L == 2 or f[i + 1][j - 1]:
                    f[i][j] = True
                    if L > blen:
                        bl, blen = i, L
        return s[bl:bl + blen]

    # 解法 3:Manacher — O(n) / O(n)
    def longestPalindrome_manacher(self, s: str) -> str:
        if not s:
            return ""
        t = "^#" + "#".join(s) + "#$"
        n = len(t)
        p = [0] * n
        c = r = 0
        for i in range(1, n - 1):
            mirror = 2 * c - i
            if i < r:
                p[i] = min(r - i, p[mirror])
            while t[i + p[i] + 1] == t[i - p[i] - 1]:
                p[i] += 1
            if i + p[i] > r:
                c, r = i, i + p[i]
        max_i = max(range(n), key=lambda i: p[i])
        start = (max_i - p[max_i]) // 2
        return s[start:start + p[max_i]]


def _test() -> None:
    s = Solution()
    cases = [
        ("babad", ("bab", "aba")),
        ("cbbd", ("bb",)),
        ("a", ("a",)),
        ("ac", ("a", "c")),
    ]
    for arg, wants in cases:
        for fn in (s.longestPalindrome, s.longestPalindrome_dp, s.longestPalindrome_manacher):
            got = fn(arg)
            assert got in wants, f"{fn.__name__}({arg}) -> {got}"
    print("✅ p005 通过 3 解法")


if __name__ == "__main__":
    _test()
