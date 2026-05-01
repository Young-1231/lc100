# LC 394. 字符串解码 · Medium · 栈
"""
🔹 题面
    "3[a]2[bc]" → "aaabcbc";"2[abc]3[cd]ef" → "abcabccdcdcdef"。

🔹 直觉
    两个栈:数字栈 + 字符串栈。遇 [ 入栈,遇 ] 出栈拼接。
"""


class Solution:
    def decodeString(self, s: str) -> str:
        num_stack: list[int] = []
        str_stack: list[str] = []
        cur, k = "", 0
        for c in s:
            if c.isdigit():
                k = k * 10 + int(c)
            elif c == "[":
                num_stack.append(k); k = 0
                str_stack.append(cur); cur = ""
            elif c == "]":
                cur = str_stack.pop() + cur * num_stack.pop()
            else:
                cur += c
        return cur


def _test() -> None:
    s = Solution()
    assert s.decodeString("3[a]2[bc]") == "aaabcbc"
    assert s.decodeString("3[a2[c]]") == "accaccacc"
    assert s.decodeString("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert s.decodeString("abc") == "abc"
    print("✅ p394 通过")


if __name__ == "__main__":
    _test()
