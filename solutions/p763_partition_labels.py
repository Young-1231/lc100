# LC 763. 划分字母区间 · Medium · 贪心
"""
🔹 题面
    把 s 划分尽量多的片段,要求同一字母只出现在一个片段里。

🔹 直觉
    预处理每个字母的最远下标 last[c]。扫描时维护当前段右界 end:
        end = max(end, last[s[i]])
    i == end 时收一段。
"""


class Solution:
    def partitionLabels(self, s: str) -> list[int]:
        last = {c: i for i, c in enumerate(s)}
        ans, start, end = [], 0, 0
        for i, c in enumerate(s):
            end = max(end, last[c])
            if i == end:
                ans.append(end - start + 1)
                start = i + 1
        return ans


def _test() -> None:
    s = Solution()
    assert s.partitionLabels("ababcbacadefegdehijhklij") == [9, 7, 8]
    assert s.partitionLabels("eccbbbbdec") == [10]
    print("✅ p763 通过")


if __name__ == "__main__":
    _test()
