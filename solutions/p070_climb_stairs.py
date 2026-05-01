# LC 70. 爬楼梯 · Easy · DP
"""
🔹 题面
    每次爬 1 或 2 阶,n 阶有多少种爬法。

🔹 解法对比
    | 方法            | 时间       | 空间 | 备注              |
    |-----------------|------------|------|-------------------|
    | DP 滚动两个变量 ★| O(n)      | O(1) | 斐波那契          |
    | 矩阵快速幂      | O(log n)   | O(1) | 极致最优;复杂度炫技|
    | Binet 通项公式  | O(1)       | O(1) | 浮点精度问题      |
"""


class Solution:
    # 解法 1:DP 滚动 ★ — O(n) / O(1)
    def climbStairs(self, n: int) -> int:
        a, b = 1, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    # 解法 2:矩阵快速幂 — O(log n) / O(1)
    # [[1,1],[1,0]]^n · [1,0]^T 的第二项 = F(n+1)。
    def climbStairs_matpow(self, n: int) -> int:
        def mul(A, B):
            return [
                [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]],
            ]
        def matpow(A, p):
            R = [[1, 0], [0, 1]]
            while p:
                if p & 1:
                    R = mul(R, A)
                A = mul(A, A)
                p >>= 1
            return R
        if n == 0:
            return 1
        M = matpow([[1, 1], [1, 0]], n)
        return M[0][0]


def _test() -> None:
    s = Solution()
    cases = [(2, 2), (3, 3), (5, 8), (1, 1), (10, 89)]
    for arg, want in cases:
        for fn in (s.climbStairs, s.climbStairs_matpow):
            assert fn(arg) == want
    print("✅ p070 通过 2 解法")


if __name__ == "__main__":
    _test()
