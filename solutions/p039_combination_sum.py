# LC 39. 组合总和 · Medium · 回溯
"""
🔹 题面
    candidates 中可重复使用元素,凑出 target 的所有组合。

🔹 直觉
    起点剪枝:每层从 i 开始,允许重复(下一层仍从 i),避免出现 [2,3] 与 [3,2]。
"""


class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        candidates.sort()
        ans, path = [], []

        def bt(start, remain):
            if remain == 0:
                ans.append(path[:])
                return
            for i in range(start, len(candidates)):
                x = candidates[i]
                if x > remain:
                    break
                path.append(x)
                bt(i, remain - x)
                path.pop()

        bt(0, target)
        return ans


def _test() -> None:
    s = Solution()
    assert sorted(s.combinationSum([2, 3, 6, 7], 7)) == sorted([[2, 2, 3], [7]])
    assert sorted(s.combinationSum([2, 3, 5], 8)) == sorted([[2, 2, 2, 2], [2, 3, 3], [3, 5]])
    assert s.combinationSum([2], 1) == []
    print("✅ p039 通过")


if __name__ == "__main__":
    _test()
