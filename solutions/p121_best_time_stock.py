# LC 121. 买卖股票的最佳时机 · Easy · 贪心 / 一次遍历
"""
🔹 直觉
    扫一遍:维护历史最低价 lo,答案 = max(p[i] - lo)。
"""


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        lo, best = float("inf"), 0
        for p in prices:
            lo = min(lo, p)
            best = max(best, p - lo)
        return best


def _test() -> None:
    s = Solution()
    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0
    assert s.maxProfit([]) == 0
    print("✅ p121 通过")


if __name__ == "__main__":
    _test()
