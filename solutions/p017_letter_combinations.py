# LC 17. 电话号码的字母组合 · Medium · 回溯
"""
🔹 直觉
    逐位选取该数字对应字母,DFS。
"""


_KEY = {
    "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
    "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
}


class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        if not digits:
            return []
        ans, path = [], []

        def bt(i):
            if i == len(digits):
                ans.append("".join(path))
                return
            for c in _KEY[digits[i]]:
                path.append(c)
                bt(i + 1)
                path.pop()

        bt(0)
        return ans


def _test() -> None:
    s = Solution()
    assert sorted(s.letterCombinations("23")) == sorted(
        ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    )
    assert s.letterCombinations("") == []
    assert s.letterCombinations("2") == ["a", "b", "c"]
    print("✅ p017 通过")


if __name__ == "__main__":
    _test()
