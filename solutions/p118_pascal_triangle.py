# LC 118. 杨辉三角 · Easy · DP
"""
🔹 直觉
    每一行首尾为 1,中间 = 上一行相邻两数之和。
"""


class Solution:
    def generate(self, n: int) -> list[list[int]]:
        out: list[list[int]] = []
        for r in range(n):
            row = [1] * (r + 1)
            for c in range(1, r):
                row[c] = out[r - 1][c - 1] + out[r - 1][c]
            out.append(row)
        return out


def _test() -> None:
    s = Solution()
    assert s.generate(5) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    assert s.generate(1) == [[1]]
    assert s.generate(0) == []
    print("✅ p118 通过")


if __name__ == "__main__":
    _test()
