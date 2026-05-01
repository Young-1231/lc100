# LC 20. 有效的括号 · Easy · 栈
"""
🔹 直觉
    左括号入栈;右括号必须匹配栈顶,否则失败。最终栈空才合法。
"""


class Solution:
    def isValid(self, s: str) -> bool:
        m = {")": "(", "]": "[", "}": "{"}
        st: list[str] = []
        for c in s:
            if c in m:
                if not st or st.pop() != m[c]:
                    return False
            else:
                st.append(c)
        return not st


def _test() -> None:
    s = Solution()
    assert s.isValid("()") is True
    assert s.isValid("()[]{}") is True
    assert s.isValid("(]") is False
    assert s.isValid("([)]") is False
    assert s.isValid("{[]}") is True
    assert s.isValid("") is True
    print("✅ p020 通过")


if __name__ == "__main__":
    _test()
