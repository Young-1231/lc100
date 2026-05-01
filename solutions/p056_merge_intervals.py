# LC 56. 合并区间 · Medium · 排序
"""
🔹 题面
    合并重叠区间。
        [[1,3],[2,6],[8,10],[15,18]] → [[1,6],[8,10],[15,18]]

🔹 解法对比
    | 方法            | 时间       | 空间   | 备注                       |
    |-----------------|------------|--------|----------------------------|
    | 排序 + 一次扫描 ★| O(n log n) | O(1)   | 通用,代码简洁              |
    | 扫描线(差分)  | O(n + V)   | O(V)   | 当区间端点值范围 V 较小时   |

🔹 排序合并直觉
    按起点排序后,逐个尝试与"末尾区间"合并。
"""


class Solution:
    # 解法 1:排序 + 扫描 ★ — O(n log n) / O(1)
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort(key=lambda x: x[0])
        out: list[list[int]] = []
        for s, e in intervals:
            if out and s <= out[-1][1]:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([s, e])
        return out

    # 解法 2:扫描线(差分计数)— O(n + V) / O(V)
    # 区间内 +1,出区间 -1;非零段即合并后的区间。仅在端点范围有限时实用。
    def merge_sweep(self, intervals: list[list[int]]) -> list[list[int]]:
        if not intervals:
            return []
        events = []
        for s, e in intervals:
            events.append((s, 0))      # 起
            events.append((e, 1))      # 终(注意闭区间,稳定排序)
        events.sort()
        out, cnt, cur_s = [], 0, None
        for x, t in events:
            if t == 0:
                if cnt == 0:
                    cur_s = x
                cnt += 1
            else:
                cnt -= 1
                if cnt == 0:
                    out.append([cur_s, x])
        # 合并相邻共端点(对闭区间)
        merged: list[list[int]] = []
        for s, e in out:
            if merged and s <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], e)
            else:
                merged.append([s, e])
        return merged


def _test() -> None:
    s = Solution()
    cases = [
        ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
        ([[1, 4], [4, 5]], [[1, 5]]),
        ([[1, 4], [2, 3]], [[1, 4]]),
        ([[1, 4]], [[1, 4]]),
    ]
    for arg, want in cases:
        for fn in (s.merge, s.merge_sweep):
            assert fn([x[:] for x in arg]) == want
    print("✅ p056 通过 2 解法")


if __name__ == "__main__":
    _test()
