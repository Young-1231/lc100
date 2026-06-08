#!/usr/bin/env python3
"""生成并自测每题的三版代码 → data/modes.json

三版(见 docs/CODE-MODES.md):
  ① core      核心代码模式 —— 只有 Solution 核心方法,提交 LeetCode 用
  ② interview 面试版       —— 核心方法 + 内联示例调用,手撕完直接跑给面试官看
  ③ acm       机试版(ACM) —— 自包含 + 自己读 stdin / 写 stdout,对标华为机考

三版从同一份 core 拼出(DRY)。本脚本运行即自测:
  - 面试版:python 跑(无 stdin),stdout 须等于 demo_out
  - 机试版:echo sample_in | python,stdout 须等于 sample_out
  - 核心版:ast 语法检查
全部通过才写出 data/modes.json。

用法:python3 scripts/build_modes.py
"""
from __future__ import annotations
import ast
import json
import subprocess
import sys
from pathlib import Path

# 每题:core(必填)+ demo/demo_out(面试版)+ acm(机试版);
# prelude = 链表/树等内联定义(面试版 & 机试版共用);core_note = 核心版顶部注释
MODES: dict[int, dict] = {}

MODES[1] = {
    "core": '''class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
        return []''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.twoSum([2, 7, 11, 15], 9))   # [0, 1]
    print(s.twoSum([3, 2, 4], 6))        # [1, 2]''',
    "demo_out": "[0, 1]\n[1, 2]",
    "acm": {
        "stdin": "第 1 行:数组(空格分隔)\n第 2 行:target",
        "stdout": "命中的两个下标(空格分隔)",
        "sample_in": "2 7 11 15\n9",
        "sample_out": "0 1",
        "main": '''def main():
    nums = list(map(int, input().split()))
    target = int(input())
    print(*Solution().twoSum(nums, target))


if __name__ == "__main__":
    main()''',
    },
}

MODES[3] = {
    "core": '''class Solution:
    def lengthOfLongestSubstring(self, s):
        last = {}
        left = ans = 0
        for i, c in enumerate(s):
            if c in last and last[c] >= left:
                left = last[c] + 1
            last[c] = i
            ans = max(ans, i - left + 1)
        return ans''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.lengthOfLongestSubstring("abcabcbb"))   # 3
    print(s.lengthOfLongestSubstring("bbbbb"))       # 1
    print(s.lengthOfLongestSubstring("pwwkew"))      # 3''',
    "demo_out": "3\n1\n3",
    "acm": {
        "stdin": "一行字符串 s",
        "stdout": "最长无重复子串的长度",
        "sample_in": "abcabcbb",
        "sample_out": "3",
        "main": '''def main():
    s = input()
    print(Solution().lengthOfLongestSubstring(s))


if __name__ == "__main__":
    main()''',
    },
}

MODES[206] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(vals):
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out''',
    "core": '''class Solution:
    def reverseList(self, head):
        prev = None
        while head:
            head.next, prev, head = prev, head, head.next
        return prev''',
    "demo": '''if __name__ == "__main__":
    head = build_list([1, 2, 3, 4, 5])
    print(to_list(Solution().reverseList(head)))   # [5, 4, 3, 2, 1]''',
    "demo_out": "[5, 4, 3, 2, 1]",
    "acm": {
        "stdin": "一行:链表节点值(空格分隔);空链表为空行",
        "stdout": "反转后的链表(空格分隔)",
        "sample_in": "1 2 3 4 5",
        "sample_out": "5 4 3 2 1",
        "main": '''def main():
    vals = list(map(int, input().split()))
    print(*to_list(Solution().reverseList(build_list(vals))))


if __name__ == "__main__":
    main()''',
    },
}

MODES[104] = {
    "core_note": "# 二叉树节点 TreeNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": '''from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root''',
    "core": '''class Solution:
    def maxDepth(self, root):
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))''',
    "demo": '''if __name__ == "__main__":
    root = build_tree([3, 9, 20, None, None, 15, 7])
    print(Solution().maxDepth(root))   # 3''',
    "demo_out": "3",
    "acm": {
        "stdin": "一行:二叉树层序遍历,空节点用 null(空格分隔)",
        "stdout": "二叉树最大深度",
        "sample_in": "3 9 20 null null 15 7",
        "sample_out": "3",
        "main": '''def main():
    vals = [None if t == "null" else int(t) for t in input().split()]
    print(Solution().maxDepth(build_tree(vals)))


if __name__ == "__main__":
    main()''',
    },
}

# ==================== Day 1 续:哈希 / 双指针 / 滑窗 / 子串 ====================

MODES[49] = {
    "core": '''from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs):
        bucket = defaultdict(list)
        for s in strs:
            cnt = [0] * 26
            for c in s:
                cnt[ord(c) - 97] += 1
            bucket[tuple(cnt)].append(s)
        return list(bucket.values())''',
    "demo": '''if __name__ == "__main__":
    print(Solution().groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]''',
    "demo_out": "[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]",
    "acm": {
        "stdin": "一行:若干字符串(空格分隔)",
        "stdout": "每组异位词一行(组内空格分隔)",
        "sample_in": "eat tea tan ate nat bat",
        "sample_out": "eat tea ate\ntan nat\nbat",
        "main": '''def main():
    strs = input().split()
    for group in Solution().groupAnagrams(strs):
        print(*group)


if __name__ == "__main__":
    main()''',
    },
}

MODES[128] = {
    "core": '''class Solution:
    def longestConsecutive(self, nums):
        S = set(nums)
        best = 0
        for x in S:
            if x - 1 in S:
                continue
            y = x
            while y + 1 in S:
                y += 1
            best = max(best, y - x + 1)
        return best''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.longestConsecutive([100, 4, 200, 1, 3, 2]))          # 4
    print(s.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))  # 9''',
    "demo_out": "4\n9",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "最长连续序列长度",
        "sample_in": "100 4 200 1 3 2",
        "sample_out": "4",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(Solution().longestConsecutive(nums))


if __name__ == "__main__":
    main()''',
    },
}

MODES[283] = {
    "core": '''class Solution:
    def moveZeroes(self, nums):
        slow = 0
        for fast in range(len(nums)):
            if nums[fast]:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                slow += 1''',
    "demo": '''if __name__ == "__main__":
    nums = [0, 1, 0, 3, 12]
    Solution().moveZeroes(nums)
    print(nums)   # [1, 3, 12, 0, 0]''',
    "demo_out": "[1, 3, 12, 0, 0]",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "原地移动零后的数组(空格分隔)",
        "sample_in": "0 1 0 3 12",
        "sample_out": "1 3 12 0 0",
        "main": '''def main():
    nums = list(map(int, input().split()))
    Solution().moveZeroes(nums)
    print(*nums)


if __name__ == "__main__":
    main()''',
    },
}

MODES[11] = {
    "core": '''class Solution:
    def maxArea(self, h):
        i, j, best = 0, len(h) - 1, 0
        while i < j:
            best = max(best, (j - i) * min(h[i], h[j]))
            if h[i] < h[j]:
                i += 1
            else:
                j -= 1
        return best''',
    "demo": '''if __name__ == "__main__":
    print(Solution().maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))   # 49''',
    "demo_out": "49",
    "acm": {
        "stdin": "一行:高度数组(空格分隔)",
        "stdout": "最大盛水量",
        "sample_in": "1 8 6 2 5 4 8 3 7",
        "sample_out": "49",
        "main": '''def main():
    h = list(map(int, input().split()))
    print(Solution().maxArea(h))


if __name__ == "__main__":
    main()''',
    },
}

MODES[15] = {
    "core": '''class Solution:
    def threeSum(self, nums):
        nums.sort()
        n, ans = len(nums), []
        for i in range(n - 2):
            if nums[i] > 0:
                break
            if i and nums[i] == nums[i - 1]:
                continue
            l, r, target = i + 1, n - 1, -nums[i]
            while l < r:
                s = nums[l] + nums[r]
                if s == target:
                    ans.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
                    while l < r and nums[r] == nums[r + 1]:
                        r -= 1
                elif s < target:
                    l += 1
                else:
                    r -= 1
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().threeSum([-1, 0, 1, 2, -1, -4]))
    # [[-1, -1, 2], [-1, 0, 1]]''',
    "demo_out": "[[-1, -1, 2], [-1, 0, 1]]",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "每个三元组一行(空格分隔)",
        "sample_in": "-1 0 1 2 -1 -4",
        "sample_out": "-1 -1 2\n-1 0 1",
        "main": '''def main():
    nums = list(map(int, input().split()))
    for triple in Solution().threeSum(nums):
        print(*triple)


if __name__ == "__main__":
    main()''',
    },
}

MODES[42] = {
    "core": '''class Solution:
    def trap(self, h):
        l, r = 0, len(h) - 1
        lmax = rmax = ans = 0
        while l < r:
            if h[l] < h[r]:
                lmax = max(lmax, h[l])
                ans += lmax - h[l]
                l += 1
            else:
                rmax = max(rmax, h[r])
                ans += rmax - h[r]
                r -= 1
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # 6''',
    "demo_out": "6",
    "acm": {
        "stdin": "一行:高度数组(空格分隔)",
        "stdout": "可接雨水总量",
        "sample_in": "0 1 0 2 1 0 1 3 2 1 2 1",
        "sample_out": "6",
        "main": '''def main():
    h = list(map(int, input().split()))
    print(Solution().trap(h))


if __name__ == "__main__":
    main()''',
    },
}

MODES[438] = {
    "core": '''from collections import Counter


class Solution:
    def findAnagrams(self, s, p):
        m, n = len(p), len(s)
        if n < m:
            return []
        need = Counter(p)
        win = Counter(s[:m])
        ans = [0] if win == need else []
        for r in range(m, n):
            win[s[r]] += 1
            win[s[r - m]] -= 1
            if win[s[r - m]] == 0:
                del win[s[r - m]]
            if win == need:
                ans.append(r - m + 1)
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().findAnagrams("cbaebabacd", "abc"))   # [0, 6]''',
    "demo_out": "[0, 6]",
    "acm": {
        "stdin": "第 1 行:字符串 s\n第 2 行:模式串 p",
        "stdout": "所有异位词起始下标(空格分隔)",
        "sample_in": "cbaebabacd\nabc",
        "sample_out": "0 6",
        "main": '''def main():
    s = input()
    p = input()
    print(*Solution().findAnagrams(s, p))


if __name__ == "__main__":
    main()''',
    },
}

MODES[560] = {
    "core": '''from collections import defaultdict


class Solution:
    def subarraySum(self, nums, k):
        cnt = defaultdict(int)
        cnt[0] = 1
        s = ans = 0
        for x in nums:
            s += x
            ans += cnt[s - k]
            cnt[s] += 1
        return ans''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.subarraySum([1, 1, 1], 2))   # 2
    print(s.subarraySum([1, 2, 3], 3))   # 2''',
    "demo_out": "2\n2",
    "acm": {
        "stdin": "第 1 行:数组(空格分隔)\n第 2 行:k",
        "stdout": "和为 k 的连续子数组个数",
        "sample_in": "1 1 1\n2",
        "sample_out": "2",
        "main": '''def main():
    nums = list(map(int, input().split()))
    k = int(input())
    print(Solution().subarraySum(nums, k))


if __name__ == "__main__":
    main()''',
    },
}

MODES[239] = {
    "core": '''from collections import deque


class Solution:
    def maxSlidingWindow(self, nums, k):
        dq = deque()
        ans = []
        for i, x in enumerate(nums):
            while dq and nums[dq[-1]] <= x:
                dq.pop()
            dq.append(i)
            if dq[0] <= i - k:
                dq.popleft()
            if i >= k - 1:
                ans.append(nums[dq[0]])
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3))
    # [3, 3, 5, 5, 6, 7]''',
    "demo_out": "[3, 3, 5, 5, 6, 7]",
    "acm": {
        "stdin": "第 1 行:数组(空格分隔)\n第 2 行:k",
        "stdout": "每个窗口最大值(空格分隔)",
        "sample_in": "1 3 -1 -3 5 3 6 7\n3",
        "sample_out": "3 3 5 5 6 7",
        "main": '''def main():
    nums = list(map(int, input().split()))
    k = int(input())
    print(*Solution().maxSlidingWindow(nums, k))


if __name__ == "__main__":
    main()''',
    },
}

MODES[76] = {
    "core": '''from collections import Counter


class Solution:
    def minWindow(self, s, t):
        if len(s) < len(t):
            return ""
        need = Counter(t)
        kinds = len(need)
        have = {}
        valid = 0
        l = 0
        best_l, best_len = 0, float("inf")
        for r, c in enumerate(s):
            if c in need:
                have[c] = have.get(c, 0) + 1
                if have[c] == need[c]:
                    valid += 1
            while valid == kinds:
                if r - l + 1 < best_len:
                    best_l, best_len = l, r - l + 1
                lc = s[l]
                if lc in need:
                    if have[lc] == need[lc]:
                        valid -= 1
                    have[lc] -= 1
                l += 1
        return "" if best_len == float("inf") else s[best_l:best_l + best_len]''',
    "demo": '''if __name__ == "__main__":
    print(Solution().minWindow("ADOBECODEBANC", "ABC"))   # BANC''',
    "demo_out": "BANC",
    "acm": {
        "stdin": "第 1 行:字符串 s\n第 2 行:字符串 t",
        "stdout": "最小覆盖子串(无解输出空行)",
        "sample_in": "ADOBECODEBANC\nABC",
        "sample_out": "BANC",
        "main": '''def main():
    s = input()
    t = input()
    print(Solution().minWindow(s, t))


if __name__ == "__main__":
    main()''',
    },
}

# ==================== Day 2:数组 / 矩阵 ====================

MODES[53] = {
    "core": '''class Solution:
    def maxSubArray(self, nums):
        cur = best = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)
            best = max(best, cur)
        return best''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))   # 6
    print(s.maxSubArray([5, 4, -1, 7, 8]))                  # 23''',
    "demo_out": "6\n23",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "最大子数组和",
        "sample_in": "-2 1 -3 4 -1 2 1 -5 4",
        "sample_out": "6",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(Solution().maxSubArray(nums))


if __name__ == "__main__":
    main()''',
    },
}

MODES[56] = {
    "core": '''class Solution:
    def merge(self, intervals):
        intervals.sort(key=lambda x: x[0])
        out = []
        for s, e in intervals:
            if out and s <= out[-1][1]:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([s, e])
        return out''',
    "demo": '''if __name__ == "__main__":
    print(Solution().merge([[1, 3], [2, 6], [8, 10], [15, 18]]))
    # [[1, 6], [8, 10], [15, 18]]''',
    "demo_out": "[[1, 6], [8, 10], [15, 18]]",
    "acm": {
        "stdin": "第 1 行:区间数 n\n随后 n 行:每行一个区间(两个数,空格分隔)",
        "stdout": "合并后的区间,每行一个",
        "sample_in": "4\n1 3\n2 6\n8 10\n15 18",
        "sample_out": "1 6\n8 10\n15 18",
        "main": '''def main():
    n = int(input())
    intervals = [list(map(int, input().split())) for _ in range(n)]
    for s, e in Solution().merge(intervals):
        print(s, e)


if __name__ == "__main__":
    main()''',
    },
}

MODES[189] = {
    "core": '''class Solution:
    def rotate(self, nums, k):
        n = len(nums)
        k %= n
        nums.reverse()
        nums[:k] = reversed(nums[:k])
        nums[k:] = reversed(nums[k:])''',
    "demo": '''if __name__ == "__main__":
    nums = [1, 2, 3, 4, 5, 6, 7]
    Solution().rotate(nums, 3)
    print(nums)   # [5, 6, 7, 1, 2, 3, 4]''',
    "demo_out": "[5, 6, 7, 1, 2, 3, 4]",
    "acm": {
        "stdin": "第 1 行:数组(空格分隔)\n第 2 行:k",
        "stdout": "右移 k 位后的数组(空格分隔)",
        "sample_in": "1 2 3 4 5 6 7\n3",
        "sample_out": "5 6 7 1 2 3 4",
        "main": '''def main():
    nums = list(map(int, input().split()))
    k = int(input())
    Solution().rotate(nums, k)
    print(*nums)


if __name__ == "__main__":
    main()''',
    },
}

MODES[238] = {
    "core": '''class Solution:
    def productExceptSelf(self, nums):
        n = len(nums)
        ans = [1] * n
        for i in range(1, n):
            ans[i] = ans[i - 1] * nums[i - 1]
        right = 1
        for i in range(n - 1, -1, -1):
            ans[i] *= right
            right *= nums[i]
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().productExceptSelf([1, 2, 3, 4]))   # [24, 12, 8, 6]''',
    "demo_out": "[24, 12, 8, 6]",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "除自身外的乘积数组(空格分隔)",
        "sample_in": "1 2 3 4",
        "sample_out": "24 12 8 6",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(*Solution().productExceptSelf(nums))


if __name__ == "__main__":
    main()''',
    },
}

MODES[41] = {
    "core": '''class Solution:
    def firstMissingPositive(self, nums):
        n = len(nums)
        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                j = nums[i] - 1
                nums[i], nums[j] = nums[j], nums[i]
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.firstMissingPositive([1, 2, 0]))          # 3
    print(s.firstMissingPositive([3, 4, -1, 1]))      # 2
    print(s.firstMissingPositive([7, 8, 9, 11, 12]))  # 1''',
    "demo_out": "3\n2\n1",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "缺失的第一个正数",
        "sample_in": "3 4 -1 1",
        "sample_out": "2",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(Solution().firstMissingPositive(nums))


if __name__ == "__main__":
    main()''',
    },
}

MODES[73] = {
    "core": '''class Solution:
    def setZeroes(self, m):
        rows, cols = len(m), len(m[0])
        first_row_zero = any(m[0][c] == 0 for c in range(cols))
        first_col_zero = any(m[r][0] == 0 for r in range(rows))
        for r in range(1, rows):
            for c in range(1, cols):
                if m[r][c] == 0:
                    m[r][0] = m[0][c] = 0
        for r in range(1, rows):
            for c in range(1, cols):
                if m[r][0] == 0 or m[0][c] == 0:
                    m[r][c] = 0
        if first_row_zero:
            for c in range(cols):
                m[0][c] = 0
        if first_col_zero:
            for r in range(rows):
                m[r][0] = 0''',
    "demo": '''if __name__ == "__main__":
    m = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    Solution().setZeroes(m)
    print(m)   # [[1, 0, 1], [0, 0, 0], [1, 0, 1]]''',
    "demo_out": "[[1, 0, 1], [0, 0, 0], [1, 0, 1]]",
    "acm": {
        "stdin": "第 1 行:行数 m 列数 n\n随后 m 行:每行 n 个数(空格分隔)",
        "stdout": "置零后的矩阵,每行一行",
        "sample_in": "3 3\n1 1 1\n1 0 1\n1 1 1",
        "sample_out": "1 0 1\n0 0 0\n1 0 1",
        "main": '''def main():
    rows, cols = map(int, input().split())
    m = [list(map(int, input().split())) for _ in range(rows)]
    Solution().setZeroes(m)
    for row in m:
        print(*row)


if __name__ == "__main__":
    main()''',
    },
}

MODES[54] = {
    "core": '''class Solution:
    def spiralOrder(self, m):
        if not m:
            return []
        top, bottom, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
        out = []
        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                out.append(m[top][c])
            top += 1
            for r in range(top, bottom + 1):
                out.append(m[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    out.append(m[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    out.append(m[r][left])
                left += 1
        return out''',
    "demo": '''if __name__ == "__main__":
    print(Solution().spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    # [1, 2, 3, 6, 9, 8, 7, 4, 5]''',
    "demo_out": "[1, 2, 3, 6, 9, 8, 7, 4, 5]",
    "acm": {
        "stdin": "第 1 行:行数 m 列数 n\n随后 m 行:每行 n 个数(空格分隔)",
        "stdout": "螺旋顺序(空格分隔)",
        "sample_in": "3 3\n1 2 3\n4 5 6\n7 8 9",
        "sample_out": "1 2 3 6 9 8 7 4 5",
        "main": '''def main():
    rows, cols = map(int, input().split())
    m = [list(map(int, input().split())) for _ in range(rows)]
    print(*Solution().spiralOrder(m))


if __name__ == "__main__":
    main()''',
    },
}

MODES[48] = {
    "core": '''class Solution:
    def rotate(self, m):
        n = len(m)
        for i in range(n):
            for j in range(i + 1, n):
                m[i][j], m[j][i] = m[j][i], m[i][j]
        for row in m:
            row.reverse()''',
    "demo": '''if __name__ == "__main__":
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Solution().rotate(m)
    print(m)   # [[7, 4, 1], [8, 5, 2], [9, 6, 3]]''',
    "demo_out": "[[7, 4, 1], [8, 5, 2], [9, 6, 3]]",
    "acm": {
        "stdin": "第 1 行:方阵阶数 n\n随后 n 行:每行 n 个数(空格分隔)",
        "stdout": "顺时针旋转 90° 后的矩阵,每行一行",
        "sample_in": "3\n1 2 3\n4 5 6\n7 8 9",
        "sample_out": "7 4 1\n8 5 2\n9 6 3",
        "main": '''def main():
    n = int(input())
    m = [list(map(int, input().split())) for _ in range(n)]
    Solution().rotate(m)
    for row in m:
        print(*row)


if __name__ == "__main__":
    main()''',
    },
}

MODES[240] = {
    "core": '''class Solution:
    def searchMatrix(self, m, target):
        if not m or not m[0]:
            return False
        i, j = 0, len(m[0]) - 1
        while i < len(m) and j >= 0:
            if m[i][j] == target:
                return True
            if m[i][j] > target:
                j -= 1
            else:
                i += 1
        return False''',
    "demo": '''if __name__ == "__main__":
    m = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16]]
    print(Solution().searchMatrix(m, 5))    # True''',
    "demo_out": "True",
    "acm": {
        "stdin": "第 1 行:行数 m 列数 n\n随后 m 行:每行 n 个数\n最后一行:target",
        "stdout": "是否存在 target(true / false)",
        "sample_in": "3 4\n1 4 7 11\n2 5 8 12\n3 6 9 16\n5",
        "sample_out": "true",
        "main": '''def main():
    rows, cols = map(int, input().split())
    m = [list(map(int, input().split())) for _ in range(rows)]
    target = int(input())
    print("true" if Solution().searchMatrix(m, target) else "false")


if __name__ == "__main__":
    main()''',
    },
}

# ==================== Day 3:链表 ====================

_LL = '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(vals):
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out'''

MODES[2] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": _LL,
    "core": '''class Solution:
    def addTwoNumbers(self, l1, l2):
        dummy = tail = ListNode()
        carry = 0
        while l1 or l2 or carry:
            a = l1.val if l1 else 0
            b = l2.val if l2 else 0
            carry, d = divmod(a + b + carry, 10)
            tail.next = ListNode(d)
            tail = tail.next
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next
        return dummy.next''',
    "demo": '''if __name__ == "__main__":
    l1 = build_list([2, 4, 3])
    l2 = build_list([5, 6, 4])
    print(to_list(Solution().addTwoNumbers(l1, l2)))   # [7, 0, 8]''',
    "demo_out": "[7, 0, 8]",
    "acm": {
        "stdin": "第 1 行:l1 各位(低位在前,空格分隔)\n第 2 行:l2 各位",
        "stdout": "相加结果链表(低位在前,空格分隔)",
        "sample_in": "2 4 3\n5 6 4",
        "sample_out": "7 0 8",
        "main": '''def main():
    l1 = build_list(list(map(int, input().split())))
    l2 = build_list(list(map(int, input().split())))
    print(*to_list(Solution().addTwoNumbers(l1, l2)))


if __name__ == "__main__":
    main()''',
    },
}

MODES[19] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": _LL,
    "core": '''class Solution:
    def removeNthFromEnd(self, head, n):
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n + 1):
            fast = fast.next
        while fast:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return dummy.next''',
    "demo": '''if __name__ == "__main__":
    head = build_list([1, 2, 3, 4, 5])
    print(to_list(Solution().removeNthFromEnd(head, 2)))   # [1, 2, 3, 5]''',
    "demo_out": "[1, 2, 3, 5]",
    "acm": {
        "stdin": "第 1 行:链表值(空格分隔)\n第 2 行:n",
        "stdout": "删除倒数第 n 个后的链表(空格分隔)",
        "sample_in": "1 2 3 4 5\n2",
        "sample_out": "1 2 3 5",
        "main": '''def main():
    vals = list(map(int, input().split()))
    n = int(input())
    print(*to_list(Solution().removeNthFromEnd(build_list(vals), n)))


if __name__ == "__main__":
    main()''',
    },
}

MODES[21] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": _LL,
    "core": '''class Solution:
    def mergeTwoLists(self, l1, l2):
        dummy = tail = ListNode()
        while l1 and l2:
            if l1.val <= l2.val:
                tail.next, l1 = l1, l1.next
            else:
                tail.next, l2 = l2, l2.next
            tail = tail.next
        tail.next = l1 or l2
        return dummy.next''',
    "demo": '''if __name__ == "__main__":
    l1 = build_list([1, 2, 4])
    l2 = build_list([1, 3, 4])
    print(to_list(Solution().mergeTwoLists(l1, l2)))   # [1, 1, 2, 3, 4, 4]''',
    "demo_out": "[1, 1, 2, 3, 4, 4]",
    "acm": {
        "stdin": "第 1 行:l1(空格分隔)\n第 2 行:l2",
        "stdout": "合并后的有序链表(空格分隔)",
        "sample_in": "1 2 4\n1 3 4",
        "sample_out": "1 1 2 3 4 4",
        "main": '''def main():
    l1 = build_list(list(map(int, input().split())))
    l2 = build_list(list(map(int, input().split())))
    print(*to_list(Solution().mergeTwoLists(l1, l2)))


if __name__ == "__main__":
    main()''',
    },
}

MODES[23] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": _LL,
    "core": '''import heapq


class Solution:
    def mergeKLists(self, lists):
        h = []
        for i, head in enumerate(lists):
            if head:
                heapq.heappush(h, (head.val, i, head))
        dummy = t = ListNode()
        while h:
            v, i, node = heapq.heappop(h)
            t.next = node
            t = t.next
            if node.next:
                heapq.heappush(h, (node.next.val, i, node.next))
        return dummy.next''',
    "demo": '''if __name__ == "__main__":
    lists = [build_list([1, 4, 5]), build_list([1, 3, 4]), build_list([2, 6])]
    print(to_list(Solution().mergeKLists(lists)))
    # [1, 1, 2, 3, 4, 4, 5, 6]''',
    "demo_out": "[1, 1, 2, 3, 4, 4, 5, 6]",
    "acm": {
        "stdin": "第 1 行:链表数 k\n随后 k 行:每行一条链表(空格分隔,空行表示空链表)",
        "stdout": "合并后的有序链表(空格分隔)",
        "sample_in": "3\n1 4 5\n1 3 4\n2 6",
        "sample_out": "1 1 2 3 4 4 5 6",
        "main": '''def main():
    k = int(input())
    lists = [build_list(list(map(int, input().split()))) for _ in range(k)]
    print(*to_list(Solution().mergeKLists(lists)))


if __name__ == "__main__":
    main()''',
    },
}

MODES[24] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": _LL,
    "core": '''class Solution:
    def swapPairs(self, head):
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next and prev.next.next:
            a, b = prev.next, prev.next.next
            prev.next = b
            a.next = b.next
            b.next = a
            prev = a
        return dummy.next''',
    "demo": '''if __name__ == "__main__":
    head = build_list([1, 2, 3, 4])
    print(to_list(Solution().swapPairs(head)))   # [2, 1, 4, 3]''',
    "demo_out": "[2, 1, 4, 3]",
    "acm": {
        "stdin": "一行:链表值(空格分隔)",
        "stdout": "两两交换后的链表(空格分隔)",
        "sample_in": "1 2 3 4",
        "sample_out": "2 1 4 3",
        "main": '''def main():
    vals = list(map(int, input().split()))
    print(*to_list(Solution().swapPairs(build_list(vals))))


if __name__ == "__main__":
    main()''',
    },
}

MODES[25] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": _LL,
    "core": '''class Solution:
    def reverseKGroup(self, head, k):
        dummy = ListNode(0, head)
        group_prev = dummy
        while True:
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if not kth:
                    return dummy.next
            group_next = kth.next
            prev, cur = group_next, group_prev.next
            while cur is not group_next:
                nxt = cur.next
                cur.next = prev
                prev = cur
                cur = nxt
            tmp = group_prev.next
            group_prev.next = kth
            group_prev = tmp''',
    "demo": '''if __name__ == "__main__":
    head = build_list([1, 2, 3, 4, 5])
    print(to_list(Solution().reverseKGroup(head, 2)))   # [2, 1, 4, 3, 5]''',
    "demo_out": "[2, 1, 4, 3, 5]",
    "acm": {
        "stdin": "第 1 行:链表值(空格分隔)\n第 2 行:k",
        "stdout": "每 k 个一组翻转后的链表(空格分隔)",
        "sample_in": "1 2 3 4 5\n2",
        "sample_out": "2 1 4 3 5",
        "main": '''def main():
    vals = list(map(int, input().split()))
    k = int(input())
    print(*to_list(Solution().reverseKGroup(build_list(vals), k)))


if __name__ == "__main__":
    main()''',
    },
}

MODES[234] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": _LL + '''


def _reverse(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev''',
    "core": '''class Solution:
    def isPalindrome(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        right = _reverse(slow)
        left = head
        while right:
            if left.val != right.val:
                return False
            left = left.next
            right = right.next
        return True''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.isPalindrome(build_list([1, 2, 2, 1])))   # True
    print(s.isPalindrome(build_list([1, 2, 3])))      # False''',
    "demo_out": "True\nFalse",
    "acm": {
        "stdin": "一行:链表值(空格分隔)",
        "stdout": "是否回文(true / false)",
        "sample_in": "1 2 2 1",
        "sample_out": "true",
        "main": '''def main():
    vals = list(map(int, input().split()))
    print("true" if Solution().isPalindrome(build_list(vals)) else "false")


if __name__ == "__main__":
    main()''',
    },
}

# ---- Day 3 特殊 IO:环 / 相交 / 随机指针 / LRU ----

_CYC = '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_cycle(vals, pos):
    dummy = cur = ListNode()
    nodes = []
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
        nodes.append(cur)
    if pos >= 0 and nodes:
        cur.next = nodes[pos]
    return dummy.next'''

MODES[138] = {
    "core_note": "# 随机指针节点 Node 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": '''class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def build_random(rows):
    nodes = [Node(v) for v, _ in rows]
    for i, (_, r) in enumerate(rows):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if r != -1:
            nodes[i].random = nodes[r]
    return nodes[0] if nodes else None


def dump_random(head):
    idx = {}
    cur, i = head, 0
    while cur:
        idx[id(cur)] = i
        cur = cur.next
        i += 1
    out = []
    cur = head
    while cur:
        r = idx[id(cur.random)] if cur.random else -1
        out.append((cur.val, r))
        cur = cur.next
    return out''',
    "core": '''class Solution:
    def copyRandomList(self, head):
        if not head:
            return None
        m = {}
        cur = head
        while cur:
            m[cur] = Node(cur.val)
            cur = cur.next
        cur = head
        while cur:
            m[cur].next = m.get(cur.next)
            m[cur].random = m.get(cur.random)
            cur = cur.next
        return m[head]''',
    "demo": '''if __name__ == "__main__":
    head = build_random([(7, -1), (13, 0), (11, 4), (10, 2), (1, 0)])
    print(dump_random(Solution().copyRandomList(head)))
    # [(7, -1), (13, 0), (11, 4), (10, 2), (1, 0)]''',
    "demo_out": "[(7, -1), (13, 0), (11, 4), (10, 2), (1, 0)]",
    "acm": {
        "stdin": "第 1 行:节点数 n\n随后 n 行:`val random下标`(random 为 -1 表示 None)",
        "stdout": "复制后的链表,每行 `val random下标`",
        "sample_in": "5\n7 -1\n13 0\n11 4\n10 2\n1 0",
        "sample_out": "7 -1\n13 0\n11 4\n10 2\n1 0",
        "main": '''def main():
    n = int(input())
    rows = [tuple(map(int, input().split())) for _ in range(n)]
    res = Solution().copyRandomList(build_random(rows))
    for val, r in dump_random(res):
        print(val, r)


if __name__ == "__main__":
    main()''',
    },
}

MODES[141] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": _CYC,
    "core": '''class Solution:
    def hasCycle(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False''',
    "demo": '''if __name__ == "__main__":
    head = build_cycle([3, 2, 0, -4], 1)   # 尾节点连回下标 1
    print(Solution().hasCycle(head))        # True''',
    "demo_out": "True",
    "acm": {
        "stdin": "第 1 行:链表值(空格分隔)\n第 2 行:pos(环连接到的下标,-1 表示无环)",
        "stdout": "是否有环(true / false)",
        "sample_in": "3 2 0 -4\n1",
        "sample_out": "true",
        "main": '''def main():
    vals = list(map(int, input().split()))
    pos = int(input())
    print("true" if Solution().hasCycle(build_cycle(vals, pos)) else "false")


if __name__ == "__main__":
    main()''',
    },
}

MODES[142] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": _CYC,
    "core": '''class Solution:
    def detectCycle(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                p = head
                while p is not slow:
                    p = p.next
                    slow = slow.next
                return p
        return None''',
    "demo": '''if __name__ == "__main__":
    head = build_cycle([3, 2, 0, -4], 1)
    node = Solution().detectCycle(head)
    print(node.val if node else -1)   # 2''',
    "demo_out": "2",
    "acm": {
        "stdin": "第 1 行:链表值(空格分隔)\n第 2 行:pos(环连接到的下标,-1 表示无环)",
        "stdout": "环入口节点的值;无环输出 -1",
        "sample_in": "3 2 0 -4\n1",
        "sample_out": "2",
        "main": '''def main():
    vals = list(map(int, input().split()))
    pos = int(input())
    node = Solution().detectCycle(build_cycle(vals, pos))
    print(node.val if node else -1)


if __name__ == "__main__":
    main()''',
    },
}

MODES[146] = {
    "core_note": "# 题目要求设计数据结构,直接实现 LRUCache(get / put 均 O(1))",
    "core": '''class _Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, k=0, v=0):
        self.key, self.val = k, v
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}
        self.head, self.tail = _Node(), _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add(self, n):
        n.prev = self.head
        n.next = self.head.next
        self.head.next.prev = n
        self.head.next = n

    def _remove(self, n):
        n.prev.next = n.next
        n.next.prev = n.prev

    def get(self, key):
        if key not in self.map:
            return -1
        n = self.map[key]
        self._remove(n)
        self._add(n)
        return n.val

    def put(self, key, value):
        if key in self.map:
            n = self.map[key]
            n.val = value
            self._remove(n)
            self._add(n)
            return
        if len(self.map) >= self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
        n = _Node(key, value)
        self._add(n)
        self.map[key] = n''',
    "demo": '''if __name__ == "__main__":
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    print(c.get(1))    # 1
    c.put(3, 3)        # 淘汰 2
    print(c.get(2))    # -1
    print(c.get(3))    # 3''',
    "demo_out": "1\n-1\n3",
    "acm": {
        "stdin": "第 1 行:容量 capacity\n第 2 行:操作数 q\n随后 q 行:`put k v` 或 `get k`",
        "stdout": "每个 get 的返回值(空格分隔)",
        "sample_in": "2\n6\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2\nget 3",
        "sample_out": "1 -1 3",
        "main": '''def main():
    cap = int(input())
    q = int(input())
    cache = LRUCache(cap)
    out = []
    for _ in range(q):
        op = input().split()
        if op[0] == "put":
            cache.put(int(op[1]), int(op[2]))
        else:
            out.append(str(cache.get(int(op[1]))))
    print(*out)


if __name__ == "__main__":
    main()''',
    },
}

MODES[148] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": _LL + '''


def _merge(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next''',
    "core": '''class Solution:
    def sortList(self, head):
        if not head or not head.next:
            return head
        prev, slow, fast = None, head, head
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        prev.next = None
        return _merge(self.sortList(head), self.sortList(slow))''',
    "demo": '''if __name__ == "__main__":
    head = build_list([4, 2, 1, 3])
    print(to_list(Solution().sortList(head)))   # [1, 2, 3, 4]''',
    "demo_out": "[1, 2, 3, 4]",
    "acm": {
        "stdin": "一行:链表值(空格分隔)",
        "stdout": "升序排序后的链表(空格分隔)",
        "sample_in": "4 2 1 3",
        "sample_out": "1 2 3 4",
        "main": '''def main():
    vals = list(map(int, input().split()))
    print(*to_list(Solution().sortList(build_list(vals))))


if __name__ == "__main__":
    main()''',
    },
}

MODES[160] = {
    "core_note": "# 链表节点 ListNode 由 LeetCode 平台内置,提交时只需 Solution",
    "prelude": _LL + '''


def attach(only, common):
    if not only:
        return common
    t = only
    while t.next:
        t = t.next
    t.next = common
    return only''',
    "core": '''class Solution:
    def getIntersectionNode(self, headA, headB):
        a, b = headA, headB
        while a is not b:
            a = a.next if a else headB
            b = b.next if b else headA
        return a''',
    "demo": '''if __name__ == "__main__":
    common = build_list([8, 4, 5])
    a = attach(build_list([4, 1]), common)
    b = attach(build_list([5, 6, 1]), common)
    node = Solution().getIntersectionNode(a, b)
    print(node.val if node else "null")   # 8''',
    "demo_out": "8",
    "acm": {
        "stdin": "第 1 行:A 相交前独有部分\n第 2 行:B 相交前独有部分\n第 3 行:公共部分(相交后共享)",
        "stdout": "相交节点的值;不相交输出 null",
        "sample_in": "4 1\n5 6 1\n8 4 5",
        "sample_out": "8",
        "main": '''def main():
    a_only = list(map(int, input().split()))
    b_only = list(map(int, input().split()))
    common = build_list(list(map(int, input().split())))
    a = attach(build_list(a_only), common)
    b = attach(build_list(b_only), common)
    node = Solution().getIntersectionNode(a, b)
    print(node.val if node else "null")


if __name__ == "__main__":
    main()''',
    },
}


def _join(parts: list[str]) -> str:
    """用空行拼接非空片段,统一以单个换行收尾。"""
    return "\n\n".join(p.rstrip() for p in parts if p and p.strip()) + "\n"


def assemble(p: dict) -> tuple[str, str, str]:
    pre = p.get("prelude", "")
    core = p["core"]
    note = p.get("core_note", "")
    core_v = _join([note, core])
    interview = _join([pre, core, p["demo"]])
    acm = _join([pre, core, p["acm"]["main"]])
    return core_v, interview, acm


def _run(code: str, stdin: str = "") -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, "-c", code], input=stdin,
        capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def verify() -> tuple[dict, list[str]]:
    out: dict[str, object] = {
        "_doc": "每题三版代码:core 核心代码模式 / interview 面试版 / acm 机试版(ACM)。详见 docs/CODE-MODES.md。",
    }
    fails: list[str] = []
    for pid, p in sorted(MODES.items()):
        core_v, interview, acm = assemble(p)

        # ① 核心版:语法检查
        try:
            ast.parse(core_v)
        except SyntaxError as e:
            fails.append(f"p{pid:03d} 核心版语法错误: {e}")

        # ② 面试版:无 stdin 跑,stdout == demo_out
        rc, so, se = _run(interview)
        if rc != 0:
            fails.append(f"p{pid:03d} 面试版运行错误: {se.splitlines()[-1:] or ''}")
        elif so != p["demo_out"].strip():
            fails.append(f"p{pid:03d} 面试版输出不符: got={so!r} want={p['demo_out']!r}")

        # ③ 机试版:喂 sample_in,stdout == sample_out
        acm_io = p["acm"]
        rc, so, se = _run(acm, acm_io["sample_in"])
        if rc != 0:
            fails.append(f"p{pid:03d} 机试版运行错误: {se.splitlines()[-1:] or ''}")
        elif so != acm_io["sample_out"].strip():
            fails.append(f"p{pid:03d} 机试版输出不符: got={so!r} want={acm_io['sample_out']!r}")

        if not any(f.startswith(f"p{pid:03d}") for f in fails):
            print(f"  ✅ p{pid:03d}: 核心/面试/机试 三版通过")

        out[str(pid)] = {
            "core": core_v,
            "interview": interview,
            "acm": acm,
            "acm_io": {k: acm_io[k] for k in ("stdin", "stdout", "sample_in", "sample_out")},
        }
    return out, fails


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    print(f"自测 {len(MODES)} 题 × 三版:")
    out, fails = verify()
    if fails:
        print("\n❌ 失败:")
        for f in fails:
            print(f"  {f}")
        sys.exit(1)
    (root / "data" / "modes.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8",
    )
    print(f"\n✅ 全部通过,已写出 data/modes.json({len(MODES)} 题 × 三版)")


if __name__ == "__main__":
    main()
