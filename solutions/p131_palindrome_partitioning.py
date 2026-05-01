# LC 131. 分割回文串 · Medium · 回溯
"""
🔹 直觉
    枚举切割点 i:s[start..i] 若为回文,递归处理 s[i+1..]。
"""


class Solution:
    def partition(self, s: str) -> list[list[str]]:
        ans, path = [], []
        n = len(s)

        def is_pal(l, r):
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1; r -= 1
            return True

        def bt(start):
            if start == n:
                ans.append(path[:])
                return
            for end in range(start, n):
                if is_pal(start, end):
                    path.append(s[start:end + 1])
                    bt(end + 1)
                    path.pop()

        bt(0)
        return ans


def _test() -> None:
    s = Solution()
    assert sorted(s.partition("aab")) == sorted([["a", "a", "b"], ["aa", "b"]])
    assert s.partition("a") == [["a"]]
    print("✅ p131 通过")


if __name__ == "__main__":
    _test()
