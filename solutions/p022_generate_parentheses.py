# LC 22. 括号生成 · Medium · 回溯
"""
🔹 直觉
    剩余左括号 > 0 才放 '(';剩余右括号 > 剩余左括号 才放 ')'(保证有效)。
"""


class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        ans, path = [], []

        def bt(left, right):
            if not left and not right:
                ans.append("".join(path))
                return
            if left > 0:
                path.append("(")
                bt(left - 1, right)
                path.pop()
            if right > left:
                path.append(")")
                bt(left, right - 1)
                path.pop()

        bt(n, n)
        return ans


def _test() -> None:
    s = Solution()
    assert sorted(s.generateParenthesis(3)) == sorted(["((()))", "(()())", "(())()", "()(())", "()()()"])
    assert s.generateParenthesis(1) == ["()"]
    print("✅ p022 通过")


if __name__ == "__main__":
    _test()
