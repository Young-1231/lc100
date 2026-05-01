# LC 4. 寻找两个正序数组的中位数 · Hard · 二分
"""
🔹 题面
    O(log min(m,n)) 求两个升序数组合并后的中位数。

🔹 直觉(短数组上二分切分点)
    把两数组各切一刀,左半总长 = (m+n+1)//2。
    设 i 为短数组的左半长度,j = 总左半长度 - i。
    要求 max(left) ≤ min(right) 即可:
        A[i-1] ≤ B[j]   且   B[j-1] ≤ A[i]
    若 A[i-1] > B[j],i 太大,r = i - 1;反之 l = i + 1。

🔹 复杂度 O(log min(m,n))
"""


class Solution:
    def findMedianSortedArrays(self, a: list[int], b: list[int]) -> float:
        if len(a) > len(b):
            a, b = b, a
        m, n = len(a), len(b)
        half = (m + n + 1) // 2
        l, r = 0, m
        INF = float("inf")
        while l <= r:
            i = (l + r) // 2
            j = half - i
            aL = a[i - 1] if i > 0 else -INF
            aR = a[i] if i < m else INF
            bL = b[j - 1] if j > 0 else -INF
            bR = b[j] if j < n else INF
            if aL <= bR and bL <= aR:
                if (m + n) & 1:
                    return float(max(aL, bL))
                return (max(aL, bL) + min(aR, bR)) / 2
            if aL > bR:
                r = i - 1
            else:
                l = i + 1
        return 0.0


def _test() -> None:
    s = Solution()
    assert s.findMedianSortedArrays([1, 3], [2]) == 2.0
    assert s.findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    assert s.findMedianSortedArrays([], [1]) == 1.0
    assert s.findMedianSortedArrays([2], []) == 2.0
    print("✅ p004 通过")


if __name__ == "__main__":
    _test()
