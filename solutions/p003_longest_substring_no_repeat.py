# LC 3. 无重复字符的最长子串 · Medium · 滑动窗口
"""
🔹 题面
    返回最长不含重复字符的子串长度。

🔹 直觉
    维护一个窗口 [l, r],其中无重复;r 右移时若遇到重复字符,把 l 跳到该
    字符上次位置 +1。**l 只前进不后退**。

🔹 复杂度 O(n) / O(min(n, Σ))
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last: dict[str, int] = {}
        l = best = 0
        for r, c in enumerate(s):
            if c in last and last[c] >= l:
                l = last[c] + 1
            last[c] = r
            best = max(best, r - l + 1)
        return best


def _test() -> None:
    sol = Solution()
    assert sol.lengthOfLongestSubstring("abcabcbb") == 3
    assert sol.lengthOfLongestSubstring("bbbbb") == 1
    assert sol.lengthOfLongestSubstring("pwwkew") == 3
    assert sol.lengthOfLongestSubstring("") == 0
    print("✅ p003 通过")


if __name__ == "__main__":
    _test()
