# LC 279. 完全平方数 · Medium · DP / BFS
"""
🔹 题面
    n 拆成尽量少的完全平方数之和。

🔹 直觉
    f(i) = 1 + min{ f(i - k²) },k² ≤ i。
"""


class Solution:
    def numSquares(self, n: int) -> int:
        f = [0] + [float("inf")] * n
        for i in range(1, n + 1):
            k = 1
            while k * k <= i:
                f[i] = min(f[i], f[i - k * k] + 1)
                k += 1
        return f[n]


def _test() -> None:
    s = Solution()
    assert s.numSquares(12) == 3
    assert s.numSquares(13) == 2
    assert s.numSquares(1) == 1
    print("✅ p279 通过")


if __name__ == "__main__":
    _test()
