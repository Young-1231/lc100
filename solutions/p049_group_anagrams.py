# LC 49. 字母异位词分组 · Medium · 哈希
"""
🔹 题面
    把字符串数组按字母异位词分组。

🔹 解法对比
    | 方法                  | 时间          | 空间   | 备注                       |
    |-----------------------|---------------|--------|----------------------------|
    | 排序作 key            | O(n·k log k)  | O(n·k) | 简洁,普适(支持任意字符)|
    | 计数元组作 key ★     | O(n·k)        | O(n·k) | 仅小写字母时更快            |

    n=字符串数,k=字符串平均长度。

🔹 直觉
    异位词 ≡ 排序后字符串相同 ≡ 字符计数元组相同。让"特征"做哈希键。

🔹 踩坑
    - tuple(count) 作 key:list 不可哈希。
"""
from collections import defaultdict


class Solution:
    # 解法 1:排序作 key — O(n·k log k) / O(n·k)
    def groupAnagrams_sort(self, strs: list[str]) -> list[list[str]]:
        bucket: dict[str, list[str]] = defaultdict(list)
        for s in strs:
            bucket["".join(sorted(s))].append(s)
        return list(bucket.values())

    # 解法 2:计数元组作 key ★  — O(n·k) / O(n·k)
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        bucket: dict[tuple, list[str]] = defaultdict(list)
        for s in strs:
            cnt = [0] * 26
            for c in s:
                cnt[ord(c) - 97] += 1
            bucket[tuple(cnt)].append(s)
        return list(bucket.values())


def _norm(out):
    return sorted(sorted(g) for g in out)


def _test() -> None:
    s = Solution()
    arg = ["eat", "tea", "tan", "ate", "nat", "bat"]
    want = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    for fn in (s.groupAnagrams, s.groupAnagrams_sort):
        assert _norm(fn(arg)) == _norm(want)
    assert s.groupAnagrams([""]) == [[""]]
    print("✅ p049 通过 2 解法")


if __name__ == "__main__":
    _test()
