# LC 139. 单词拆分 · Medium · DP
"""
🔹 状态
    f[i] 表示 s[:i] 是否可拆;
    f[i] = ∃ j: f[j] ∧ s[j:i] ∈ wordDict
"""


class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)
        max_len = max((len(w) for w in words), default=0)
        n = len(s)
        f = [False] * (n + 1)
        f[0] = True
        for i in range(1, n + 1):
            for j in range(max(0, i - max_len), i):
                if f[j] and s[j:i] in words:
                    f[i] = True
                    break
        return f[n]


def _test() -> None:
    s = Solution()
    assert s.wordBreak("leetcode", ["leet", "code"]) is True
    assert s.wordBreak("applepenapple", ["apple", "pen"]) is True
    assert s.wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    print("✅ p139 通过")


if __name__ == "__main__":
    _test()
