# LC 438. 找到字符串中所有字母异位词 · Medium · 滑动窗口
"""
🔹 题面
    s 中所有 p 的异位词起始下标。

🔹 直觉
    定长滑窗(长度 = len(p)),用计数器对比即可。
    优化:维护一个 diff = "still_needed" 数,= 0 时即匹配。

🔹 复杂度 O(n) / O(Σ=26)
"""
from collections import Counter


class Solution:
    def findAnagrams(self, s: str, p: str) -> list[int]:
        m, n = len(p), len(s)
        if n < m:
            return []
        need = Counter(p)
        win = Counter(s[:m])
        ans = [0] if win == need else []
        for r in range(m, n):
            win[s[r]] += 1
            win[s[r - m]] -= 1
            if win[s[r - m]] == 0:
                del win[s[r - m]]
            if win == need:
                ans.append(r - m + 1)
        return ans


def _test() -> None:
    s = Solution()
    assert s.findAnagrams("cbaebabacd", "abc") == [0, 6]
    assert s.findAnagrams("abab", "ab") == [0, 1, 2]
    assert s.findAnagrams("a", "ab") == []
    print("✅ p438 通过")


if __name__ == "__main__":
    _test()
