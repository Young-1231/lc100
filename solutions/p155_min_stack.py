# LC 155. 最小栈 · Medium · 栈
"""
🔹 直觉
    用辅助栈,栈顶始终保存"截至目前的最小值"。
    或单栈中存对 (x, cur_min);技巧:差值栈也行。
"""


class MinStack:
    def __init__(self):
        self.s: list[int] = []
        self.m: list[int] = []           # 最小值栈

    def push(self, val: int) -> None:
        self.s.append(val)
        self.m.append(val if not self.m else min(val, self.m[-1]))

    def pop(self) -> None:
        self.s.pop()
        self.m.pop()

    def top(self) -> int:
        return self.s[-1]

    def getMin(self) -> int:
        return self.m[-1]


def _test() -> None:
    ms = MinStack()
    ms.push(-2); ms.push(0); ms.push(-3)
    assert ms.getMin() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.getMin() == -2
    print("✅ p155 通过")


if __name__ == "__main__":
    _test()
