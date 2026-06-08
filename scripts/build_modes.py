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
