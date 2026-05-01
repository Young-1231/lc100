# LC 322. 零钱兑换 · Medium · 完全背包
"""
🔹 解法对比
    | 方法                | 时间       | 空间      | 备注                |
    |---------------------|------------|-----------|---------------------|
    | DFS + 记忆化(自顶) | O(amount·c)| O(amount) | 直观,递归栈        |
    | DP 完全背包 ★      | O(amount·c)| O(amount) | 工程首选            |

🔹 状态
    f[x] = 1 + min{ f[x - c] | c ∈ coins }
"""
from functools import lru_cache


class Solution:
    # 解法 1:DP 完全背包 ★ — O(amount·c)
    def coinChange(self, coins: list[int], amount: int) -> int:
        INF = amount + 1
        f = [0] + [INF] * amount
        for x in range(1, amount + 1):
            for c in coins:
                if c <= x:
                    f[x] = min(f[x], f[x - c] + 1)
        return -1 if f[amount] == INF else f[amount]

    # 解法 2:DFS + 记忆化 — O(amount·c)
    def coinChange_memo(self, coins: list[int], amount: int) -> int:
        @lru_cache(None)
        def dfs(x):
            if x == 0:
                return 0
            if x < 0:
                return -1
            best = float("inf")
            for c in coins:
                sub = dfs(x - c)
                if sub != -1:
                    best = min(best, sub + 1)
            return best if best != float("inf") else -1
        return dfs(amount)


def _test() -> None:
    s = Solution()
    cases = [
        (([1, 2, 5], 11), 3),
        (([2], 3), -1),
        (([1], 0), 0),
    ]
    for args, want in cases:
        for fn in (s.coinChange, s.coinChange_memo):
            assert fn(*args) == want
    print("✅ p322 通过 2 解法")


if __name__ == "__main__":
    _test()
