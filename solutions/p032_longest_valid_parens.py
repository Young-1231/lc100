# LC 32. 最长有效括号 · Hard · DP / 栈
"""
🔹 题面
    返回最长有效括号子串长度。

🔹 解法对比
    | 方法            | 时间 | 空间 | 备注                          |
    |-----------------|------|------|-------------------------------|
    | 栈(下标)★    | O(n) | O(n) | 栈底放"上一个未匹配位置"     |
    | DP              | O(n) | O(n) | f[i] 表 s[..i] 以 i 结尾的最长有效  |
    | 双向计数(贪心) | O(n) | O(1) | 左右各扫一次,计 ( 与 )       |
"""


class Solution:
    # 解法 1:栈 ★ — O(n) / O(n)
    def longestValidParentheses(self, s: str) -> int:
        st = [-1]
        ans = 0
        for i, c in enumerate(s):
            if c == "(":
                st.append(i)
            else:
                st.pop()
                if not st:
                    st.append(i)
                else:
                    ans = max(ans, i - st[-1])
        return ans

    # 解法 2:DP — O(n) / O(n)
    # 当 s[i]==')':
    #   若 s[i-1]=='(': f[i] = f[i-2] + 2
    #   若 s[i-1]==')' 且 s[i-f[i-1]-1]=='(': f[i] = f[i-1] + 2 + f[i-f[i-1]-2]
    def longestValidParentheses_dp(self, s: str) -> int:
        n = len(s)
        f = [0] * n
        ans = 0
        for i in range(1, n):
            if s[i] != ')':
                continue
            if s[i - 1] == '(':
                f[i] = (f[i - 2] if i >= 2 else 0) + 2
            elif i - f[i - 1] - 1 >= 0 and s[i - f[i - 1] - 1] == '(':
                f[i] = f[i - 1] + 2 + (f[i - f[i - 1] - 2] if i - f[i - 1] - 2 >= 0 else 0)
            ans = max(ans, f[i])
        return ans

    # 解法 3:双向计数 — O(n) / O(1)
    def longestValidParentheses_count(self, s: str) -> int:
        ans = l = r = 0
        for c in s:
            if c == '(': l += 1
            else: r += 1
            if l == r: ans = max(ans, 2 * r)
            elif r > l: l = r = 0
        l = r = 0
        for c in reversed(s):
            if c == '(': l += 1
            else: r += 1
            if l == r: ans = max(ans, 2 * l)
            elif l > r: l = r = 0
        return ans


def _test() -> None:
    s = Solution()
    cases = [("(()", 2), (")()())", 4), ("", 0), ("()(()", 2), ("()(())", 6)]
    for arg, want in cases:
        for fn in (s.longestValidParentheses, s.longestValidParentheses_dp, s.longestValidParentheses_count):
            assert fn(arg) == want, f"{fn.__name__}({arg!r}) -> {fn(arg)} != {want}"
    print("✅ p032 通过 3 解法")


if __name__ == "__main__":
    _test()
