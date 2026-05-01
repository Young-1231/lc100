# LC 739. 每日温度 · Medium · 单调栈
"""
🔹 题面
    返回每天距下一个更高温度的天数。

🔹 直觉
    维护"温度递减"的下标栈。新的更高温度时,把栈中所有 ≤ 它的弹出,
    并填它们的答案。
"""


class Solution:
    def dailyTemperatures(self, t: list[int]) -> list[int]:
        n = len(t)
        ans = [0] * n
        st: list[int] = []
        for i, x in enumerate(t):
            while st and t[st[-1]] < x:
                j = st.pop()
                ans[j] = i - j
            st.append(i)
        return ans


def _test() -> None:
    s = Solution()
    assert s.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert s.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert s.dailyTemperatures([30, 60, 90]) == [1, 1, 0]
    print("✅ p739 通过")


if __name__ == "__main__":
    _test()
