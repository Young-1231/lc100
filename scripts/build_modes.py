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

# ==================== Day 4:二叉树 ====================

_TREE = '''from collections import deque


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
    return root


def tree_to_level(root):
    out, q = [], deque([root])
    while q:
        node = q.popleft()
        if node:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


def parse_tree():
    return build_tree([None if t == "null" else int(t) for t in input().split()])


def fmt_level(root):
    return " ".join("null" if v is None else str(v) for v in tree_to_level(root))'''

_TN = "# 二叉树节点 TreeNode 由 LeetCode 平台内置,提交时只需 Solution"

MODES[94] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def inorderTraversal(self, root):
        out, stack, cur = [], [], root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            out.append(cur.val)
            cur = cur.right
        return out''',
    "demo": '''if __name__ == "__main__":
    print(Solution().inorderTraversal(build_tree([1, None, 2, 3])))   # [1, 3, 2]''',
    "demo_out": "[1, 3, 2]",
    "acm": {
        "stdin": "一行:二叉树层序遍历,空节点用 null(空格分隔)",
        "stdout": "中序遍历(空格分隔)",
        "sample_in": "1 null 2 3", "sample_out": "1 3 2",
        "main": '''def main():
    print(*Solution().inorderTraversal(parse_tree()))


if __name__ == "__main__":
    main()''',
    },
}

MODES[98] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def isValidBST(self, root):
        def ok(n, lo, hi):
            if not n:
                return True
            if n.val <= lo or n.val >= hi:
                return False
            return ok(n.left, lo, n.val) and ok(n.right, n.val, hi)
        return ok(root, float("-inf"), float("inf"))''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.isValidBST(build_tree([2, 1, 3])))                     # True
    print(s.isValidBST(build_tree([5, 1, 4, None, None, 3, 6])))   # False''',
    "demo_out": "True\nFalse",
    "acm": {
        "stdin": "一行:二叉树层序遍历,空节点用 null(空格分隔)",
        "stdout": "是否为合法 BST(true / false)",
        "sample_in": "2 1 3", "sample_out": "true",
        "main": '''def main():
    print("true" if Solution().isValidBST(parse_tree()) else "false")


if __name__ == "__main__":
    main()''',
    },
}

MODES[101] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def isSymmetric(self, root):
        def same(a, b):
            if not a and not b:
                return True
            if not a or not b or a.val != b.val:
                return False
            return same(a.left, b.right) and same(a.right, b.left)
        return not root or same(root.left, root.right)''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.isSymmetric(build_tree([1, 2, 2, 3, 4, 4, 3])))          # True
    print(s.isSymmetric(build_tree([1, 2, 2, None, 3, None, 3])))    # False''',
    "demo_out": "True\nFalse",
    "acm": {
        "stdin": "一行:二叉树层序遍历,空节点用 null(空格分隔)",
        "stdout": "是否对称(true / false)",
        "sample_in": "1 2 2 3 4 4 3", "sample_out": "true",
        "main": '''def main():
    print("true" if Solution().isSymmetric(parse_tree()) else "false")


if __name__ == "__main__":
    main()''',
    },
}

MODES[102] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def levelOrder(self, root):
        if not root:
            return []
        out, q = [], deque([root])
        while q:
            level = []
            for _ in range(len(q)):
                n = q.popleft()
                level.append(n.val)
                if n.left:
                    q.append(n.left)
                if n.right:
                    q.append(n.right)
            out.append(level)
        return out''',
    "demo": '''if __name__ == "__main__":
    print(Solution().levelOrder(build_tree([3, 9, 20, None, None, 15, 7])))
    # [[3], [9, 20], [15, 7]]''',
    "demo_out": "[[3], [9, 20], [15, 7]]",
    "acm": {
        "stdin": "一行:二叉树层序遍历,空节点用 null(空格分隔)",
        "stdout": "层序遍历,每层一行(空格分隔)",
        "sample_in": "3 9 20 null null 15 7", "sample_out": "3\n9 20\n15 7",
        "main": '''def main():
    for level in Solution().levelOrder(parse_tree()):
        print(*level)


if __name__ == "__main__":
    main()''',
    },
}

MODES[105] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def buildTree(self, preorder, inorder):
        idx = {v: i for i, v in enumerate(inorder)}

        def build(pl, pr, il, ir):
            if pl > pr:
                return None
            root_val = preorder[pl]
            i = idx[root_val]
            left_len = i - il
            return TreeNode(
                root_val,
                build(pl + 1, pl + left_len, il, i - 1),
                build(pl + left_len + 1, pr, i + 1, ir),
            )

        return build(0, len(preorder) - 1, 0, len(inorder) - 1)''',
    "demo": '''if __name__ == "__main__":
    root = Solution().buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    print(tree_to_level(root))   # [3, 9, 20, None, None, 15, 7]''',
    "demo_out": "[3, 9, 20, None, None, 15, 7]",
    "acm": {
        "stdin": "第 1 行:前序遍历\n第 2 行:中序遍历(均空格分隔)",
        "stdout": "构造的树层序遍历(null 表示空)",
        "sample_in": "3 9 20 15 7\n9 3 15 20 7", "sample_out": "3 9 20 null null 15 7",
        "main": '''def main():
    pre = list(map(int, input().split()))
    ino = list(map(int, input().split()))
    print(fmt_level(Solution().buildTree(pre, ino)))


if __name__ == "__main__":
    main()''',
    },
}

MODES[108] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def sortedArrayToBST(self, nums):
        def build(l, r):
            if l > r:
                return None
            m = (l + r) // 2
            return TreeNode(nums[m], build(l, m - 1), build(m + 1, r))
        return build(0, len(nums) - 1)''',
    "demo": '''if __name__ == "__main__":
    root = Solution().sortedArrayToBST([-10, -3, 0, 5, 9])
    print(tree_to_level(root))   # [0, -10, 5, None, -3, None, 9]''',
    "demo_out": "[0, -10, 5, None, -3, None, 9]",
    "acm": {
        "stdin": "一行:升序数组(空格分隔)",
        "stdout": "构造的 BST 层序(null 表示空)",
        "sample_in": "-10 -3 0 5 9", "sample_out": "0 -10 5 null -3 null 9",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(fmt_level(Solution().sortedArrayToBST(nums)))


if __name__ == "__main__":
    main()''',
    },
}

MODES[114] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def flatten(self, root):
        self.prev = None

        def dfs(n):
            if not n:
                return
            dfs(n.right)
            dfs(n.left)
            n.right = self.prev
            n.left = None
            self.prev = n

        dfs(root)''',
    "demo": '''if __name__ == "__main__":
    root = build_tree([1, 2, 5, 3, 4, None, 6])
    Solution().flatten(root)
    print(tree_to_level(root))   # [1, None, 2, None, 3, None, 4, None, 5, None, 6]''',
    "demo_out": "[1, None, 2, None, 3, None, 4, None, 5, None, 6]",
    "acm": {
        "stdin": "一行:二叉树层序遍历,空节点用 null(空格分隔)",
        "stdout": "展开为右斜链表后的层序(null 表示空)",
        "sample_in": "1 2 5 3 4 null 6", "sample_out": "1 null 2 null 3 null 4 null 5 null 6",
        "main": '''def main():
    root = parse_tree()
    Solution().flatten(root)
    print(fmt_level(root))


if __name__ == "__main__":
    main()''',
    },
}

MODES[124] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def maxPathSum(self, root):
        self.best = float("-inf")

        def gain(n):
            if not n:
                return 0
            l = max(0, gain(n.left))
            r = max(0, gain(n.right))
            self.best = max(self.best, n.val + l + r)
            return n.val + max(l, r)

        gain(root)
        return self.best''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.maxPathSum(build_tree([1, 2, 3])))                         # 6
    print(s.maxPathSum(build_tree([-10, 9, 20, None, None, 15, 7])))   # 42''',
    "demo_out": "6\n42",
    "acm": {
        "stdin": "一行:二叉树层序遍历,空节点用 null(空格分隔)",
        "stdout": "最大路径和",
        "sample_in": "-10 9 20 null null 15 7", "sample_out": "42",
        "main": '''def main():
    print(Solution().maxPathSum(parse_tree()))


if __name__ == "__main__":
    main()''',
    },
}

MODES[199] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def rightSideView(self, root):
        if not root:
            return []
        out, q = [], deque([root])
        while q:
            sz = len(q)
            for i in range(sz):
                n = q.popleft()
                if i == sz - 1:
                    out.append(n.val)
                if n.left:
                    q.append(n.left)
                if n.right:
                    q.append(n.right)
        return out''',
    "demo": '''if __name__ == "__main__":
    print(Solution().rightSideView(build_tree([1, 2, 3, None, 5, None, 4])))   # [1, 3, 4]''',
    "demo_out": "[1, 3, 4]",
    "acm": {
        "stdin": "一行:二叉树层序遍历,空节点用 null(空格分隔)",
        "stdout": "右视图(从顶到底,空格分隔)",
        "sample_in": "1 2 3 null 5 null 4", "sample_out": "1 3 4",
        "main": '''def main():
    print(*Solution().rightSideView(parse_tree()))


if __name__ == "__main__":
    main()''',
    },
}

MODES[226] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def invertTree(self, root):
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root''',
    "demo": '''if __name__ == "__main__":
    root = Solution().invertTree(build_tree([4, 2, 7, 1, 3, 6, 9]))
    print(tree_to_level(root))   # [4, 7, 2, 9, 6, 3, 1]''',
    "demo_out": "[4, 7, 2, 9, 6, 3, 1]",
    "acm": {
        "stdin": "一行:二叉树层序遍历,空节点用 null(空格分隔)",
        "stdout": "翻转后的树层序(null 表示空)",
        "sample_in": "4 2 7 1 3 6 9", "sample_out": "4 7 2 9 6 3 1",
        "main": '''def main():
    print(fmt_level(Solution().invertTree(parse_tree())))


if __name__ == "__main__":
    main()''',
    },
}

MODES[230] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def kthSmallest(self, root, k):
        stack, cur = [], root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            k -= 1
            if k == 0:
                return cur.val
            cur = cur.right
        return -1''',
    "demo": '''if __name__ == "__main__":
    root = build_tree([3, 1, 4, None, 2])
    print(Solution().kthSmallest(root, 1))   # 1''',
    "demo_out": "1",
    "acm": {
        "stdin": "第 1 行:BST 层序(null 表示空)\n第 2 行:k",
        "stdout": "第 k 小的元素",
        "sample_in": "3 1 4 null 2\n1", "sample_out": "1",
        "main": '''def main():
    root = parse_tree()
    k = int(input())
    print(Solution().kthSmallest(root, k))


if __name__ == "__main__":
    main()''',
    },
}

MODES[236] = {
    "core_note": _TN,
    "prelude": _TREE + '''


def find_node(root, val):
    if not root:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)''',
    "core": '''class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if not root or root is p or root is q:
            return root
        l = self.lowestCommonAncestor(root.left, p, q)
        r = self.lowestCommonAncestor(root.right, p, q)
        if l and r:
            return root
        return l or r''',
    "demo": '''if __name__ == "__main__":
    root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p = find_node(root, 5)
    q = find_node(root, 1)
    print(Solution().lowestCommonAncestor(root, p, q).val)   # 3''',
    "demo_out": "3",
    "acm": {
        "stdin": "第 1 行:树层序(null 表示空)\n第 2 行:p 的值\n第 3 行:q 的值",
        "stdout": "最近公共祖先的值",
        "sample_in": "3 5 1 6 2 0 8 null null 7 4\n5\n1", "sample_out": "3",
        "main": '''def main():
    root = parse_tree()
    p = int(input())
    q = int(input())
    ans = Solution().lowestCommonAncestor(root, find_node(root, p), find_node(root, q))
    print(ans.val)


if __name__ == "__main__":
    main()''',
    },
}

MODES[437] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''from collections import defaultdict


class Solution:
    def pathSum(self, root, targetSum):
        cnt = defaultdict(int)
        cnt[0] = 1
        ans = 0

        def dfs(n, cur):
            nonlocal ans
            if not n:
                return
            cur += n.val
            ans += cnt[cur - targetSum]
            cnt[cur] += 1
            dfs(n.left, cur)
            dfs(n.right, cur)
            cnt[cur] -= 1

        dfs(root, 0)
        return ans''',
    "demo": '''if __name__ == "__main__":
    root = build_tree([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1])
    print(Solution().pathSum(root, 8))   # 3''',
    "demo_out": "3",
    "acm": {
        "stdin": "第 1 行:树层序(null 表示空)\n第 2 行:targetSum",
        "stdout": "和为 targetSum 的路径数",
        "sample_in": "10 5 -3 3 2 null 11 3 -2 null 1\n8", "sample_out": "3",
        "main": '''def main():
    root = parse_tree()
    target = int(input())
    print(Solution().pathSum(root, target))


if __name__ == "__main__":
    main()''',
    },
}

MODES[543] = {
    "core_note": _TN, "prelude": _TREE,
    "core": '''class Solution:
    def diameterOfBinaryTree(self, root):
        self.best = 0

        def depth(n):
            if not n:
                return 0
            l = depth(n.left)
            r = depth(n.right)
            self.best = max(self.best, l + r)
            return 1 + max(l, r)

        depth(root)
        return self.best''',
    "demo": '''if __name__ == "__main__":
    print(Solution().diameterOfBinaryTree(build_tree([1, 2, 3, 4, 5])))   # 3''',
    "demo_out": "3",
    "acm": {
        "stdin": "一行:二叉树层序遍历,空节点用 null(空格分隔)",
        "stdout": "直径(最长路径的边数)",
        "sample_in": "1 2 3 4 5", "sample_out": "3",
        "main": '''def main():
    print(Solution().diameterOfBinaryTree(parse_tree()))


if __name__ == "__main__":
    main()''',
    },
}

# ==================== Day 5:图论 / 回溯 / 二分 ====================

_KEY = '''_KEY = {
    "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
    "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
}'''

MODES[200] = {
    "core": '''class Solution:
    def numIslands(self, grid):
        if not grid:
            return 0
        m, n = len(grid), len(grid[0])

        def dfs(i, j):
            if i < 0 or j < 0 or i >= m or j >= n or grid[i][j] != "1":
                return
            grid[i][j] = "0"
            dfs(i + 1, j)
            dfs(i - 1, j)
            dfs(i, j + 1)
            dfs(i, j - 1)

        cnt = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == "1":
                    cnt += 1
                    dfs(i, j)
        return cnt''',
    "demo": '''if __name__ == "__main__":
    grid = [
        ["1", "1", "0"],
        ["1", "0", "0"],
        ["0", "0", "1"],
    ]
    print(Solution().numIslands(grid))   # 2''',
    "demo_out": "2",
    "acm": {
        "stdin": "第 1 行:行数 m 列数 n\n随后 m 行:每行 n 个字符(0 / 1,连续无空格)",
        "stdout": "岛屿数量",
        "sample_in": "3 3\n110\n100\n001", "sample_out": "2",
        "main": '''def main():
    m, n = map(int, input().split())
    grid = [list(input()) for _ in range(m)]
    print(Solution().numIslands(grid))


if __name__ == "__main__":
    main()''',
    },
}

MODES[994] = {
    "core": '''from collections import deque


class Solution:
    def orangesRotting(self, g):
        m, n = len(g), len(g[0])
        q = deque()
        fresh = 0
        for i in range(m):
            for j in range(n):
                if g[i][j] == 2:
                    q.append((i, j))
                elif g[i][j] == 1:
                    fresh += 1
        if fresh == 0:
            return 0
        minutes = 0
        while q and fresh:
            for _ in range(len(q)):
                x, y = q.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and g[nx][ny] == 1:
                        g[nx][ny] = 2
                        fresh -= 1
                        q.append((nx, ny))
            minutes += 1
        return minutes if fresh == 0 else -1''',
    "demo": '''if __name__ == "__main__":
    print(Solution().orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))   # 4''',
    "demo_out": "4",
    "acm": {
        "stdin": "第 1 行:行数 m 列数 n\n随后 m 行:每行 n 个数(0空/1鲜/2腐,空格分隔)",
        "stdout": "全部腐烂所需分钟数;无法全烂输出 -1",
        "sample_in": "3 3\n2 1 1\n1 1 0\n0 1 1", "sample_out": "4",
        "main": '''def main():
    m, n = map(int, input().split())
    g = [list(map(int, input().split())) for _ in range(m)]
    print(Solution().orangesRotting(g))


if __name__ == "__main__":
    main()''',
    },
}

MODES[207] = {
    "core": '''from collections import defaultdict, deque


class Solution:
    def canFinish(self, numCourses, prerequisites):
        g = defaultdict(list)
        indeg = [0] * numCourses
        for a, b in prerequisites:
            g[b].append(a)
            indeg[a] += 1
        q = deque(i for i, d in enumerate(indeg) if d == 0)
        seen = 0
        while q:
            u = q.popleft()
            seen += 1
            for v in g[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return seen == numCourses''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.canFinish(2, [[1, 0]]))           # True
    print(s.canFinish(2, [[1, 0], [0, 1]]))   # False''',
    "demo_out": "True\nFalse",
    "acm": {
        "stdin": "第 1 行:课程数 numCourses\n第 2 行:先修关系数 e\n随后 e 行:每行 `a b`(学 a 前需先学 b)",
        "stdout": "能否修完所有课程(true / false)",
        "sample_in": "2\n1\n1 0", "sample_out": "true",
        "main": '''def main():
    num = int(input())
    e = int(input())
    prer = [list(map(int, input().split())) for _ in range(e)]
    print("true" if Solution().canFinish(num, prer) else "false")


if __name__ == "__main__":
    main()''',
    },
}

MODES[208] = {
    "core_note": "# 题目要求设计前缀树,直接实现 Trie",
    "core": '''class Trie:
    def __init__(self):
        self.children = {}
        self.end = False

    def insert(self, word):
        node = self
        for c in word:
            if c not in node.children:
                node.children[c] = Trie()
            node = node.children[c]
        node.end = True

    def _find(self, word):
        node = self
        for c in word:
            if c not in node.children:
                return None
            node = node.children[c]
        return node

    def search(self, word):
        node = self._find(word)
        return node is not None and node.end

    def startsWith(self, prefix):
        return self._find(prefix) is not None''',
    "demo": '''if __name__ == "__main__":
    t = Trie()
    t.insert("apple")
    print(t.search("apple"))      # True
    print(t.search("app"))        # False
    print(t.startsWith("app"))    # True
    t.insert("app")
    print(t.search("app"))        # True''',
    "demo_out": "True\nFalse\nTrue\nTrue",
    "acm": {
        "stdin": "第 1 行:操作数 q\n随后 q 行:`insert w` / `search w` / `startsWith p`",
        "stdout": "每个 search / startsWith 的结果(true / false,空格分隔)",
        "sample_in": "5\ninsert apple\nsearch apple\nsearch app\nstartsWith app\ninsert app",
        "sample_out": "true false true",
        "main": '''def main():
    q = int(input())
    t = Trie()
    out = []
    for _ in range(q):
        op = input().split()
        if op[0] == "insert":
            t.insert(op[1])
        elif op[0] == "search":
            out.append("true" if t.search(op[1]) else "false")
        else:
            out.append("true" if t.startsWith(op[1]) else "false")
    print(*out)


if __name__ == "__main__":
    main()''',
    },
}

MODES[46] = {
    "core": '''class Solution:
    def permute(self, nums):
        n, ans = len(nums), []
        path, used = [], [False] * n

        def bt():
            if len(path) == n:
                ans.append(path[:])
                return
            for i in range(n):
                if used[i]:
                    continue
                used[i] = True
                path.append(nums[i])
                bt()
                path.pop()
                used[i] = False

        bt()
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().permute([1, 2, 3]))
    # [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]''',
    "demo_out": "[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "全部排列,每个一行(空格分隔)",
        "sample_in": "1 2 3", "sample_out": "1 2 3\n1 3 2\n2 1 3\n2 3 1\n3 1 2\n3 2 1",
        "main": '''def main():
    nums = list(map(int, input().split()))
    for p in Solution().permute(nums):
        print(*p)


if __name__ == "__main__":
    main()''',
    },
}

MODES[78] = {
    "core": '''class Solution:
    def subsets(self, nums):
        out = [[]]
        for x in nums:
            out += [s + [x] for s in out]
        return out''',
    "demo": '''if __name__ == "__main__":
    print(Solution().subsets([1, 2, 3]))
    # [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]''',
    "demo_out": "[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "全部子集,每个一行(空集为空行,空格分隔)",
        "sample_in": "1 2 3", "sample_out": "\n1\n2\n1 2\n3\n1 3\n2 3\n1 2 3",
        "main": '''def main():
    nums = list(map(int, input().split()))
    for s in Solution().subsets(nums):
        print(*s)


if __name__ == "__main__":
    main()''',
    },
}

MODES[17] = {
    "prelude": _KEY,
    "core": '''class Solution:
    def letterCombinations(self, digits):
        if not digits:
            return []
        ans, path = [], []

        def bt(i):
            if i == len(digits):
                ans.append("".join(path))
                return
            for c in _KEY[digits[i]]:
                path.append(c)
                bt(i + 1)
                path.pop()

        bt(0)
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().letterCombinations("23"))
    # ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']''',
    "demo_out": "['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']",
    "acm": {
        "stdin": "一行:数字串 digits(2-9)",
        "stdout": "全部字母组合(空格分隔)",
        "sample_in": "23", "sample_out": "ad ae af bd be bf cd ce cf",
        "main": '''def main():
    digits = input()
    print(*Solution().letterCombinations(digits))


if __name__ == "__main__":
    main()''',
    },
}

MODES[39] = {
    "core": '''class Solution:
    def combinationSum(self, candidates, target):
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
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().combinationSum([2, 3, 6, 7], 7))   # [[2, 2, 3], [7]]''',
    "demo_out": "[[2, 2, 3], [7]]",
    "acm": {
        "stdin": "第 1 行:候选数(空格分隔)\n第 2 行:target",
        "stdout": "全部组合,每个一行(空格分隔)",
        "sample_in": "2 3 6 7\n7", "sample_out": "2 2 3\n7",
        "main": '''def main():
    candidates = list(map(int, input().split()))
    target = int(input())
    for comb in Solution().combinationSum(candidates, target):
        print(*comb)


if __name__ == "__main__":
    main()''',
    },
}

MODES[22] = {
    "core": '''class Solution:
    def generateParenthesis(self, n):
        ans, path = [], []

        def bt(left, right):
            if not left and not right:
                ans.append("".join(path))
                return
            if left > 0:
                path.append("(")
                bt(left - 1, right)
                path.pop()
            if right > left:
                path.append(")")
                bt(left, right - 1)
                path.pop()

        bt(n, n)
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().generateParenthesis(3))
    # ['((()))', '(()())', '(())()', '()(())', '()()()']''',
    "demo_out": "['((()))', '(()())', '(())()', '()(())', '()()()']",
    "acm": {
        "stdin": "一行:括号对数 n",
        "stdout": "全部合法括号串(空格分隔)",
        "sample_in": "3", "sample_out": "((())) (()()) (())() ()(()) ()()()",
        "main": '''def main():
    n = int(input())
    print(*Solution().generateParenthesis(n))


if __name__ == "__main__":
    main()''',
    },
}

MODES[79] = {
    "core": '''class Solution:
    def exist(self, board, word):
        m, n = len(board), len(board[0])

        def dfs(i, j, k):
            if k == len(word):
                return True
            if i < 0 or j < 0 or i >= m or j >= n or board[i][j] != word[k]:
                return False
            board[i][j] = "#"
            ok = (dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1)
                  or dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1))
            board[i][j] = word[k]
            return ok

        return any(dfs(i, j, 0) for i in range(m) for j in range(n))''',
    "demo": '''if __name__ == "__main__":
    board = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    print(Solution().exist(board, "ABCCED"))   # True''',
    "demo_out": "True",
    "acm": {
        "stdin": "第 1 行:行数 m 列数 n\n随后 m 行:每行 n 个字符(连续无空格)\n最后一行:word",
        "stdout": "是否存在该单词(true / false)",
        "sample_in": "3 4\nABCE\nSFCS\nADEE\nABCCED", "sample_out": "true",
        "main": '''def main():
    m, n = map(int, input().split())
    board = [list(input()) for _ in range(m)]
    word = input()
    print("true" if Solution().exist(board, word) else "false")


if __name__ == "__main__":
    main()''',
    },
}

MODES[131] = {
    "core": '''class Solution:
    def partition(self, s):
        ans, path = [], []
        n = len(s)

        def is_pal(l, r):
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True

        def bt(start):
            if start == n:
                ans.append(path[:])
                return
            for end in range(start, n):
                if is_pal(start, end):
                    path.append(s[start:end + 1])
                    bt(end + 1)
                    path.pop()

        bt(0)
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().partition("aab"))   # [['a', 'a', 'b'], ['aa', 'b']]''',
    "demo_out": "[['a', 'a', 'b'], ['aa', 'b']]",
    "acm": {
        "stdin": "一行:字符串 s",
        "stdout": "全部回文分割方案,每个一行(子串空格分隔)",
        "sample_in": "aab", "sample_out": "a a b\naa b",
        "main": '''def main():
    s = input()
    for part in Solution().partition(s):
        print(*part)


if __name__ == "__main__":
    main()''',
    },
}

MODES[51] = {
    "core": '''class Solution:
    def solveNQueens(self, n):
        cols, diag1, diag2 = set(), set(), set()
        ans, board = [], [-1] * n

        def render():
            return [
                "".join("Q" if c == board[r] else "." for c in range(n))
                for r in range(n)
            ]

        def bt(r):
            if r == n:
                ans.append(render())
                return
            for c in range(n):
                if c in cols or (r - c) in diag1 or (r + c) in diag2:
                    continue
                board[r] = c
                cols.add(c)
                diag1.add(r - c)
                diag2.add(r + c)
                bt(r + 1)
                cols.remove(c)
                diag1.remove(r - c)
                diag2.remove(r + c)

        bt(0)
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().solveNQueens(4))
    # [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]''',
    "demo_out": "[['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]",
    "acm": {
        "stdin": "一行:棋盘大小 n",
        "stdout": "第 1 行解的个数;随后每个解的 n 行棋盘,解与解之间空行分隔",
        "sample_in": "4", "sample_out": "2\n.Q..\n...Q\nQ...\n..Q.\n\n..Q.\nQ...\n...Q\n.Q..",
        "main": '''def main():
    n = int(input())
    sols = Solution().solveNQueens(n)
    print(len(sols))
    for i, board in enumerate(sols):
        if i:
            print()
        for row in board:
            print(row)


if __name__ == "__main__":
    main()''',
    },
}

# ---- Day 5 二分查找 ----

MODES[35] = {
    "core": '''class Solution:
    def searchInsert(self, nums, target):
        l, r = 0, len(nums)
        while l < r:
            m = (l + r) // 2
            if nums[m] < target:
                l = m + 1
            else:
                r = m
        return l''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.searchInsert([1, 3, 5, 6], 5))   # 2
    print(s.searchInsert([1, 3, 5, 6], 2))   # 1''',
    "demo_out": "2\n1",
    "acm": {
        "stdin": "第 1 行:升序数组(空格分隔)\n第 2 行:target",
        "stdout": "插入位置下标",
        "sample_in": "1 3 5 6\n5", "sample_out": "2",
        "main": '''def main():
    nums = list(map(int, input().split()))
    target = int(input())
    print(Solution().searchInsert(nums, target))


if __name__ == "__main__":
    main()''',
    },
}

MODES[74] = {
    "core": '''class Solution:
    def searchMatrix(self, m, target):
        if not m or not m[0]:
            return False
        rows, cols = len(m), len(m[0])
        l, r = 0, rows * cols - 1
        while l <= r:
            mid = (l + r) // 2
            v = m[mid // cols][mid % cols]
            if v == target:
                return True
            if v < target:
                l = mid + 1
            else:
                r = mid - 1
        return False''',
    "demo": '''if __name__ == "__main__":
    m = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    print(Solution().searchMatrix(m, 3))    # True''',
    "demo_out": "True",
    "acm": {
        "stdin": "第 1 行:行数 m 列数 n\n随后 m 行:每行 n 个数\n最后一行:target",
        "stdout": "是否存在 target(true / false)",
        "sample_in": "3 4\n1 3 5 7\n10 11 16 20\n23 30 34 60\n3", "sample_out": "true",
        "main": '''def main():
    rows, cols = map(int, input().split())
    mat = [list(map(int, input().split())) for _ in range(rows)]
    target = int(input())
    print("true" if Solution().searchMatrix(mat, target) else "false")


if __name__ == "__main__":
    main()''',
    },
}

MODES[34] = {
    "core": '''from bisect import bisect_left, bisect_right


class Solution:
    def searchRange(self, nums, target):
        l = bisect_left(nums, target)
        if l == len(nums) or nums[l] != target:
            return [-1, -1]
        return [l, bisect_right(nums, target) - 1]''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.searchRange([5, 7, 7, 8, 8, 10], 8))   # [3, 4]
    print(s.searchRange([5, 7, 7, 8, 8, 10], 6))   # [-1, -1]''',
    "demo_out": "[3, 4]\n[-1, -1]",
    "acm": {
        "stdin": "第 1 行:升序数组(空格分隔)\n第 2 行:target",
        "stdout": "首末位置下标(空格分隔)",
        "sample_in": "5 7 7 8 8 10\n8", "sample_out": "3 4",
        "main": '''def main():
    nums = list(map(int, input().split()))
    target = int(input())
    print(*Solution().searchRange(nums, target))


if __name__ == "__main__":
    main()''',
    },
}

MODES[33] = {
    "core": '''class Solution:
    def search(self, nums, target):
        l, r = 0, len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                return m
            if nums[l] <= nums[m]:
                if nums[l] <= target < nums[m]:
                    r = m - 1
                else:
                    l = m + 1
            else:
                if nums[m] < target <= nums[r]:
                    l = m + 1
                else:
                    r = m - 1
        return -1''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.search([4, 5, 6, 7, 0, 1, 2], 0))   # 4
    print(s.search([4, 5, 6, 7, 0, 1, 2], 3))   # -1''',
    "demo_out": "4\n-1",
    "acm": {
        "stdin": "第 1 行:旋转排序数组(空格分隔)\n第 2 行:target",
        "stdout": "target 的下标;不存在输出 -1",
        "sample_in": "4 5 6 7 0 1 2\n0", "sample_out": "4",
        "main": '''def main():
    nums = list(map(int, input().split()))
    target = int(input())
    print(Solution().search(nums, target))


if __name__ == "__main__":
    main()''',
    },
}

MODES[153] = {
    "core": '''class Solution:
    def findMin(self, nums):
        l, r = 0, len(nums) - 1
        while l < r:
            m = (l + r) // 2
            if nums[m] > nums[r]:
                l = m + 1
            else:
                r = m
        return nums[l]''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.findMin([3, 4, 5, 1, 2]))         # 1
    print(s.findMin([4, 5, 6, 7, 0, 1, 2]))   # 0''',
    "demo_out": "1\n0",
    "acm": {
        "stdin": "一行:旋转排序数组(空格分隔)",
        "stdout": "最小值",
        "sample_in": "3 4 5 1 2", "sample_out": "1",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(Solution().findMin(nums))


if __name__ == "__main__":
    main()''',
    },
}

MODES[4] = {
    "core": '''class Solution:
    def findMedianSortedArrays(self, a, b):
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
        return 0.0''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.findMedianSortedArrays([1, 3], [2]))      # 2.0
    print(s.findMedianSortedArrays([1, 2], [3, 4]))   # 2.5''',
    "demo_out": "2.0\n2.5",
    "acm": {
        "stdin": "第 1 行:有序数组 a(空格分隔,可空行)\n第 2 行:有序数组 b",
        "stdout": "两数组合并后的中位数",
        "sample_in": "1 3\n2", "sample_out": "2.0",
        "main": '''def main():
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    print(Solution().findMedianSortedArrays(a, b))


if __name__ == "__main__":
    main()''',
    },
}

# ==================== Day 6:栈 / 堆 / 贪心 ====================

MODES[20] = {
    "core": '''class Solution:
    def isValid(self, s):
        m = {")": "(", "]": "[", "}": "{"}
        st = []
        for c in s:
            if c in m:
                if not st or st.pop() != m[c]:
                    return False
            else:
                st.append(c)
        return not st''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.isValid("()[]{}"))   # True
    print(s.isValid("(]"))       # False''',
    "demo_out": "True\nFalse",
    "acm": {
        "stdin": "一行:括号串 s",
        "stdout": "是否有效(true / false)",
        "sample_in": "()[]{}", "sample_out": "true",
        "main": '''def main():
    s = input()
    print("true" if Solution().isValid(s) else "false")


if __name__ == "__main__":
    main()''',
    },
}

MODES[155] = {
    "core_note": "# 题目要求设计 O(1) 取最小值的栈,直接实现 MinStack",
    "core": '''class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []

    def push(self, val):
        self.stack.append(val)
        if not self.mins or val <= self.mins[-1]:
            self.mins.append(val)
        else:
            self.mins.append(self.mins[-1])

    def pop(self):
        self.stack.pop()
        self.mins.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.mins[-1]''',
    "demo": '''if __name__ == "__main__":
    st = MinStack()
    st.push(-2)
    st.push(0)
    st.push(-3)
    print(st.getMin())   # -3
    st.pop()
    print(st.top())      # 0
    print(st.getMin())   # -2''',
    "demo_out": "-3\n0\n-2",
    "acm": {
        "stdin": "第 1 行:操作数 q\n随后 q 行:`push v` / `pop` / `top` / `getMin`",
        "stdout": "每个 top / getMin 的结果(空格分隔)",
        "sample_in": "7\npush -2\npush 0\npush -3\ngetMin\npop\ntop\ngetMin",
        "sample_out": "-3 0 -2",
        "main": '''def main():
    q = int(input())
    st = MinStack()
    out = []
    for _ in range(q):
        op = input().split()
        if op[0] == "push":
            st.push(int(op[1]))
        elif op[0] == "pop":
            st.pop()
        elif op[0] == "top":
            out.append(str(st.top()))
        else:
            out.append(str(st.getMin()))
    print(*out)


if __name__ == "__main__":
    main()''',
    },
}

MODES[394] = {
    "core": '''class Solution:
    def decodeString(self, s):
        num_stack, str_stack = [], []
        cur, k = "", 0
        for c in s:
            if c.isdigit():
                k = k * 10 + int(c)
            elif c == "[":
                num_stack.append(k)
                k = 0
                str_stack.append(cur)
                cur = ""
            elif c == "]":
                cur = str_stack.pop() + cur * num_stack.pop()
            else:
                cur += c
        return cur''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.decodeString("3[a]2[bc]"))       # aaabcbc
    print(s.decodeString("2[abc]3[cd]ef"))   # abcabccdcdcdef''',
    "demo_out": "aaabcbc\nabcabccdcdcdef",
    "acm": {
        "stdin": "一行:编码字符串 s",
        "stdout": "解码后的字符串",
        "sample_in": "3[a]2[bc]", "sample_out": "aaabcbc",
        "main": '''def main():
    s = input()
    print(Solution().decodeString(s))


if __name__ == "__main__":
    main()''',
    },
}

MODES[739] = {
    "core": '''class Solution:
    def dailyTemperatures(self, t):
        n = len(t)
        ans = [0] * n
        st = []
        for i, x in enumerate(t):
            while st and t[st[-1]] < x:
                j = st.pop()
                ans[j] = i - j
            st.append(i)
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]))
    # [1, 1, 4, 2, 1, 1, 0, 0]''',
    "demo_out": "[1, 1, 4, 2, 1, 1, 0, 0]",
    "acm": {
        "stdin": "一行:每日温度(空格分隔)",
        "stdout": "每天需等待的天数(空格分隔)",
        "sample_in": "73 74 75 71 69 72 76 73", "sample_out": "1 1 4 2 1 1 0 0",
        "main": '''def main():
    t = list(map(int, input().split()))
    print(*Solution().dailyTemperatures(t))


if __name__ == "__main__":
    main()''',
    },
}

MODES[84] = {
    "core": '''class Solution:
    def largestRectangleArea(self, h):
        h = [0] + h + [0]
        st = []
        ans = 0
        for i, x in enumerate(h):
            while st and h[st[-1]] > x:
                top = st.pop()
                w = i - st[-1] - 1
                ans = max(ans, h[top] * w)
            st.append(i)
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().largestRectangleArea([2, 1, 5, 6, 2, 3]))   # 10''',
    "demo_out": "10",
    "acm": {
        "stdin": "一行:柱高数组(空格分隔)",
        "stdout": "最大矩形面积",
        "sample_in": "2 1 5 6 2 3", "sample_out": "10",
        "main": '''def main():
    h = list(map(int, input().split()))
    print(Solution().largestRectangleArea(h))


if __name__ == "__main__":
    main()''',
    },
}

MODES[215] = {
    "core": '''import heapq


class Solution:
    def findKthLargest(self, nums, k):
        h = []
        for x in nums:
            heapq.heappush(h, x)
            if len(h) > k:
                heapq.heappop(h)
        return h[0]''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.findKthLargest([3, 2, 1, 5, 6, 4], 2))               # 5
    print(s.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))      # 4''',
    "demo_out": "5\n4",
    "acm": {
        "stdin": "第 1 行:数组(空格分隔)\n第 2 行:k",
        "stdout": "第 k 大的元素",
        "sample_in": "3 2 1 5 6 4\n2", "sample_out": "5",
        "main": '''def main():
    nums = list(map(int, input().split()))
    k = int(input())
    print(Solution().findKthLargest(nums, k))


if __name__ == "__main__":
    main()''',
    },
}

MODES[347] = {
    "core": '''import heapq
from collections import Counter


class Solution:
    def topKFrequent(self, nums, k):
        cnt = Counter(nums)
        return [x for x, _ in heapq.nlargest(k, cnt.items(), key=lambda kv: kv[1])]''',
    "demo": '''if __name__ == "__main__":
    print(Solution().topKFrequent([1, 1, 1, 2, 2, 3], 2))   # [1, 2]''',
    "demo_out": "[1, 2]",
    "acm": {
        "stdin": "第 1 行:数组(空格分隔)\n第 2 行:k",
        "stdout": "前 k 个高频元素(按频率降序,空格分隔)",
        "sample_in": "1 1 1 2 2 3\n2", "sample_out": "1 2",
        "main": '''def main():
    nums = list(map(int, input().split()))
    k = int(input())
    print(*Solution().topKFrequent(nums, k))


if __name__ == "__main__":
    main()''',
    },
}

MODES[295] = {
    "core_note": "# 题目要求设计数据流中位数结构,直接实现 MedianFinder(对顶双堆)",
    "core": '''import heapq


class MedianFinder:
    def __init__(self):
        self.small = []   # 大根堆(存负数),保存较小一半
        self.large = []   # 小根堆,保存较大一半

    def addNum(self, num):
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2''',
    "demo": '''if __name__ == "__main__":
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    print(mf.findMedian())   # 1.5
    mf.addNum(3)
    print(mf.findMedian())   # 2.0''',
    "demo_out": "1.5\n2.0",
    "acm": {
        "stdin": "第 1 行:操作数 q\n随后 q 行:`addNum v` / `findMedian`",
        "stdout": "每个 findMedian 的结果(空格分隔)",
        "sample_in": "5\naddNum 1\naddNum 2\nfindMedian\naddNum 3\nfindMedian",
        "sample_out": "1.5 2.0",
        "main": '''def main():
    q = int(input())
    mf = MedianFinder()
    out = []
    for _ in range(q):
        op = input().split()
        if op[0] == "addNum":
            mf.addNum(int(op[1]))
        else:
            out.append(str(mf.findMedian()))
    print(*out)


if __name__ == "__main__":
    main()''',
    },
}

MODES[121] = {
    "core": '''class Solution:
    def maxProfit(self, prices):
        lo, best = float("inf"), 0
        for p in prices:
            lo = min(lo, p)
            best = max(best, p - lo)
        return best''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.maxProfit([7, 1, 5, 3, 6, 4]))   # 5
    print(s.maxProfit([7, 6, 4, 3, 1]))      # 0''',
    "demo_out": "5\n0",
    "acm": {
        "stdin": "一行:每日股价(空格分隔)",
        "stdout": "最大利润",
        "sample_in": "7 1 5 3 6 4", "sample_out": "5",
        "main": '''def main():
    prices = list(map(int, input().split()))
    print(Solution().maxProfit(prices))


if __name__ == "__main__":
    main()''',
    },
}

MODES[55] = {
    "core": '''class Solution:
    def canJump(self, nums):
        reach = 0
        for i, x in enumerate(nums):
            if i > reach:
                return False
            reach = max(reach, i + x)
        return True''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.canJump([2, 3, 1, 1, 4]))   # True
    print(s.canJump([3, 2, 1, 0, 4]))   # False''',
    "demo_out": "True\nFalse",
    "acm": {
        "stdin": "一行:跳跃数组(空格分隔)",
        "stdout": "能否到达终点(true / false)",
        "sample_in": "2 3 1 1 4", "sample_out": "true",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print("true" if Solution().canJump(nums) else "false")


if __name__ == "__main__":
    main()''',
    },
}

MODES[45] = {
    "core": '''class Solution:
    def jump(self, nums):
        steps = end = farthest = 0
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == end:
                steps += 1
                end = farthest
        return steps''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.jump([2, 3, 1, 1, 4]))   # 2
    print(s.jump([2, 3, 0, 1, 4]))   # 2''',
    "demo_out": "2\n2",
    "acm": {
        "stdin": "一行:跳跃数组(空格分隔)",
        "stdout": "到达终点的最少跳数",
        "sample_in": "2 3 1 1 4", "sample_out": "2",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(Solution().jump(nums))


if __name__ == "__main__":
    main()''',
    },
}

MODES[763] = {
    "core": '''class Solution:
    def partitionLabels(self, s):
        last = {c: i for i, c in enumerate(s)}
        ans, start, end = [], 0, 0
        for i, c in enumerate(s):
            end = max(end, last[c])
            if i == end:
                ans.append(end - start + 1)
                start = i + 1
        return ans''',
    "demo": '''if __name__ == "__main__":
    print(Solution().partitionLabels("ababcbacadefegdehijhklij"))   # [9, 7, 8]''',
    "demo_out": "[9, 7, 8]",
    "acm": {
        "stdin": "一行:字符串 s",
        "stdout": "各片段长度(空格分隔)",
        "sample_in": "ababcbacadefegdehijhklij", "sample_out": "9 7 8",
        "main": '''def main():
    s = input()
    print(*Solution().partitionLabels(s))


if __name__ == "__main__":
    main()''',
    },
}

# ==================== Day 7:DP / 多维 DP / 技巧 ====================

MODES[70] = {
    "core": '''class Solution:
    def climbStairs(self, n):
        a, b = 1, 1
        for _ in range(n):
            a, b = b, a + b
        return a''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.climbStairs(2))   # 2
    print(s.climbStairs(3))   # 3''',
    "demo_out": "2\n3",
    "acm": {
        "stdin": "一行:台阶数 n",
        "stdout": "爬到顶的方法数",
        "sample_in": "3", "sample_out": "3",
        "main": '''def main():
    n = int(input())
    print(Solution().climbStairs(n))


if __name__ == "__main__":
    main()''',
    },
}

MODES[118] = {
    "core": '''class Solution:
    def generate(self, n):
        out = []
        for r in range(n):
            row = [1] * (r + 1)
            for c in range(1, r):
                row[c] = out[r - 1][c - 1] + out[r - 1][c]
            out.append(row)
        return out''',
    "demo": '''if __name__ == "__main__":
    print(Solution().generate(5))
    # [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]''',
    "demo_out": "[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]",
    "acm": {
        "stdin": "一行:行数 numRows",
        "stdout": "杨辉三角,每行一行(空格分隔)",
        "sample_in": "5", "sample_out": "1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1",
        "main": '''def main():
    n = int(input())
    for row in Solution().generate(n):
        print(*row)


if __name__ == "__main__":
    main()''',
    },
}

MODES[198] = {
    "core": '''class Solution:
    def rob(self, nums):
        a = b = 0
        for x in nums:
            a, b = b, max(b, a + x)
        return b''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.rob([1, 2, 3, 1]))      # 4
    print(s.rob([2, 7, 9, 3, 1]))   # 12''',
    "demo_out": "4\n12",
    "acm": {
        "stdin": "一行:每户金额(空格分隔)",
        "stdout": "最大偷窃金额",
        "sample_in": "2 7 9 3 1", "sample_out": "12",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(Solution().rob(nums))


if __name__ == "__main__":
    main()''',
    },
}

MODES[279] = {
    "core": '''class Solution:
    def numSquares(self, n):
        f = [0] + [float("inf")] * n
        for i in range(1, n + 1):
            k = 1
            while k * k <= i:
                f[i] = min(f[i], f[i - k * k] + 1)
                k += 1
        return f[n]''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.numSquares(12))   # 3
    print(s.numSquares(13))   # 2''',
    "demo_out": "3\n2",
    "acm": {
        "stdin": "一行:整数 n",
        "stdout": "和为 n 的完全平方数最少个数",
        "sample_in": "12", "sample_out": "3",
        "main": '''def main():
    n = int(input())
    print(Solution().numSquares(n))


if __name__ == "__main__":
    main()''',
    },
}

MODES[322] = {
    "core": '''class Solution:
    def coinChange(self, coins, amount):
        INF = amount + 1
        f = [0] + [INF] * amount
        for x in range(1, amount + 1):
            for c in coins:
                if c <= x:
                    f[x] = min(f[x], f[x - c] + 1)
        return -1 if f[amount] == INF else f[amount]''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.coinChange([1, 2, 5], 11))   # 3
    print(s.coinChange([2], 3))          # -1''',
    "demo_out": "3\n-1",
    "acm": {
        "stdin": "第 1 行:硬币面额(空格分隔)\n第 2 行:总金额 amount",
        "stdout": "凑出金额的最少硬币数;无解输出 -1",
        "sample_in": "1 2 5\n11", "sample_out": "3",
        "main": '''def main():
    coins = list(map(int, input().split()))
    amount = int(input())
    print(Solution().coinChange(coins, amount))


if __name__ == "__main__":
    main()''',
    },
}

MODES[139] = {
    "core": '''class Solution:
    def wordBreak(self, s, wordDict):
        words = set(wordDict)
        max_len = max((len(w) for w in words), default=0)
        n = len(s)
        f = [False] * (n + 1)
        f[0] = True
        for i in range(1, n + 1):
            for j in range(max(0, i - max_len), i):
                if f[j] and s[j:i] in words:
                    f[i] = True
                    break
        return f[n]''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.wordBreak("leetcode", ["leet", "code"]))                       # True
    print(s.wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"])) # False''',
    "demo_out": "True\nFalse",
    "acm": {
        "stdin": "第 1 行:字符串 s\n第 2 行:词典单词(空格分隔)",
        "stdout": "能否由词典拼出(true / false)",
        "sample_in": "leetcode\nleet code", "sample_out": "true",
        "main": '''def main():
    s = input()
    words = input().split()
    print("true" if Solution().wordBreak(s, words) else "false")


if __name__ == "__main__":
    main()''',
    },
}

MODES[300] = {
    "core": '''from bisect import bisect_left


class Solution:
    def lengthOfLIS(self, nums):
        tails = []
        for x in nums:
            i = bisect_left(tails, x)
            if i == len(tails):
                tails.append(x)
            else:
                tails[i] = x
        return len(tails)''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]))   # 4
    print(s.lengthOfLIS([0, 1, 0, 3, 2, 3]))             # 4''',
    "demo_out": "4\n4",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "最长严格递增子序列长度",
        "sample_in": "10 9 2 5 3 7 101 18", "sample_out": "4",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(Solution().lengthOfLIS(nums))


if __name__ == "__main__":
    main()''',
    },
}

MODES[152] = {
    "core": '''class Solution:
    def maxProduct(self, nums):
        fmax = fmin = ans = nums[0]
        for x in nums[1:]:
            cands = (x, fmax * x, fmin * x)
            fmax = max(cands)
            fmin = min(cands)
            ans = max(ans, fmax)
        return ans''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.maxProduct([2, 3, -2, 4]))   # 6
    print(s.maxProduct([-2, 0, -1]))     # 0''',
    "demo_out": "6\n0",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "最大乘积子数组的积",
        "sample_in": "2 3 -2 4", "sample_out": "6",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(Solution().maxProduct(nums))


if __name__ == "__main__":
    main()''',
    },
}

MODES[416] = {
    "core": '''class Solution:
    def canPartition(self, nums):
        s = sum(nums)
        if s & 1:
            return False
        target = s // 2
        f = [False] * (target + 1)
        f[0] = True
        for x in nums:
            for v in range(target, x - 1, -1):
                f[v] = f[v] or f[v - x]
        return f[target]''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.canPartition([1, 5, 11, 5]))   # True
    print(s.canPartition([1, 2, 3, 5]))    # False''',
    "demo_out": "True\nFalse",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "能否分成两个等和子集(true / false)",
        "sample_in": "1 5 11 5", "sample_out": "true",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print("true" if Solution().canPartition(nums) else "false")


if __name__ == "__main__":
    main()''',
    },
}

MODES[32] = {
    "core": '''class Solution:
    def longestValidParentheses(self, s):
        st = [-1]
        ans = 0
        for i, c in enumerate(s):
            if c == "(":
                st.append(i)
            else:
                st.pop()
                if not st:
                    st.append(i)
                else:
                    ans = max(ans, i - st[-1])
        return ans''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.longestValidParentheses("(()"))      # 2
    print(s.longestValidParentheses(")()())"))   # 4''',
    "demo_out": "2\n4",
    "acm": {
        "stdin": "一行:括号串 s",
        "stdout": "最长有效括号子串长度",
        "sample_in": "(()", "sample_out": "2",
        "main": '''def main():
    s = input()
    print(Solution().longestValidParentheses(s))


if __name__ == "__main__":
    main()''',
    },
}

# ---- Day 7 多维 DP / 技巧 ----

MODES[62] = {
    "core": '''class Solution:
    def uniquePaths(self, m, n):
        f = [1] * n
        for _ in range(1, m):
            for j in range(1, n):
                f[j] += f[j - 1]
        return f[-1]''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.uniquePaths(3, 7))   # 28
    print(s.uniquePaths(3, 2))   # 3''',
    "demo_out": "28\n3",
    "acm": {
        "stdin": "一行:行数 m 列数 n(空格分隔)",
        "stdout": "从左上到右下的不同路径数",
        "sample_in": "3 7", "sample_out": "28",
        "main": '''def main():
    m, n = map(int, input().split())
    print(Solution().uniquePaths(m, n))


if __name__ == "__main__":
    main()''',
    },
}

MODES[64] = {
    "core": '''class Solution:
    def minPathSum(self, g):
        m, n = len(g), len(g[0])
        f = list(g[0])
        for j in range(1, n):
            f[j] += f[j - 1]
        for i in range(1, m):
            f[0] += g[i][0]
            for j in range(1, n):
                f[j] = g[i][j] + min(f[j], f[j - 1])
        return f[-1]''',
    "demo": '''if __name__ == "__main__":
    print(Solution().minPathSum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]))   # 7''',
    "demo_out": "7",
    "acm": {
        "stdin": "第 1 行:行数 m 列数 n\n随后 m 行:每行 n 个数(空格分隔)",
        "stdout": "左上到右下的最小路径和",
        "sample_in": "3 3\n1 3 1\n1 5 1\n4 2 1", "sample_out": "7",
        "main": '''def main():
    m, n = map(int, input().split())
    g = [list(map(int, input().split())) for _ in range(m)]
    print(Solution().minPathSum(g))


if __name__ == "__main__":
    main()''',
    },
}

MODES[5] = {
    "core": '''class Solution:
    def longestPalindrome(self, s):
        if not s:
            return ""

        def expand(l, r):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return l + 1, r - 1

        bl, br = 0, 0
        for i in range(len(s)):
            for l0, r0 in (expand(i, i), expand(i, i + 1)):
                if r0 - l0 > br - bl:
                    bl, br = l0, r0
        return s[bl:br + 1]''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.longestPalindrome("babad"))   # bab
    print(s.longestPalindrome("cbbd"))    # bb''',
    "demo_out": "bab\nbb",
    "acm": {
        "stdin": "一行:字符串 s",
        "stdout": "最长回文子串",
        "sample_in": "babad", "sample_out": "bab",
        "main": '''def main():
    s = input()
    print(Solution().longestPalindrome(s))


if __name__ == "__main__":
    main()''',
    },
}

MODES[1143] = {
    "core": '''class Solution:
    def longestCommonSubsequence(self, a, b):
        m, n = len(a), len(b)
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    f[i][j] = f[i - 1][j - 1] + 1
                else:
                    f[i][j] = max(f[i - 1][j], f[i][j - 1])
        return f[m][n]''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.longestCommonSubsequence("abcde", "ace"))   # 3
    print(s.longestCommonSubsequence("abc", "def"))      # 0''',
    "demo_out": "3\n0",
    "acm": {
        "stdin": "第 1 行:字符串 a\n第 2 行:字符串 b",
        "stdout": "最长公共子序列长度",
        "sample_in": "abcde\nace", "sample_out": "3",
        "main": '''def main():
    a = input()
    b = input()
    print(Solution().longestCommonSubsequence(a, b))


if __name__ == "__main__":
    main()''',
    },
}

MODES[72] = {
    "core": '''class Solution:
    def minDistance(self, a, b):
        m, n = len(a), len(b)
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            f[i][0] = i
        for j in range(n + 1):
            f[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    f[i][j] = f[i - 1][j - 1]
                else:
                    f[i][j] = 1 + min(f[i - 1][j - 1], f[i - 1][j], f[i][j - 1])
        return f[m][n]''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.minDistance("horse", "ros"))            # 3
    print(s.minDistance("intention", "execution"))  # 5''',
    "demo_out": "3\n5",
    "acm": {
        "stdin": "第 1 行:字符串 a\n第 2 行:字符串 b",
        "stdout": "把 a 变成 b 的最少编辑距离",
        "sample_in": "horse\nros", "sample_out": "3",
        "main": '''def main():
    a = input()
    b = input()
    print(Solution().minDistance(a, b))


if __name__ == "__main__":
    main()''',
    },
}

MODES[136] = {
    "core": '''from functools import reduce
from operator import xor


class Solution:
    def singleNumber(self, nums):
        return reduce(xor, nums)''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.singleNumber([2, 2, 1]))         # 1
    print(s.singleNumber([4, 1, 2, 1, 2]))   # 4''',
    "demo_out": "1\n4",
    "acm": {
        "stdin": "一行:数组(空格分隔,只有一个数出现一次)",
        "stdout": "只出现一次的数",
        "sample_in": "4 1 2 1 2", "sample_out": "4",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(Solution().singleNumber(nums))


if __name__ == "__main__":
    main()''',
    },
}

MODES[169] = {
    "core": '''class Solution:
    def majorityElement(self, nums):
        cand, cnt = 0, 0
        for x in nums:
            if cnt == 0:
                cand = x
            cnt += 1 if x == cand else -1
        return cand''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.majorityElement([3, 2, 3]))               # 3
    print(s.majorityElement([2, 2, 1, 1, 1, 2, 2]))   # 2''',
    "demo_out": "3\n2",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "多数元素(出现次数 > n/2)",
        "sample_in": "2 2 1 1 1 2 2", "sample_out": "2",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(Solution().majorityElement(nums))


if __name__ == "__main__":
    main()''',
    },
}

MODES[75] = {
    "core": '''class Solution:
    def sortColors(self, nums):
        lo, mid, hi = 0, 0, len(nums) - 1
        while mid <= hi:
            x = nums[mid]
            if x == 0:
                nums[lo], nums[mid] = nums[mid], nums[lo]
                lo += 1
                mid += 1
            elif x == 1:
                mid += 1
            else:
                nums[mid], nums[hi] = nums[hi], nums[mid]
                hi -= 1''',
    "demo": '''if __name__ == "__main__":
    nums = [2, 0, 2, 1, 1, 0]
    Solution().sortColors(nums)
    print(nums)   # [0, 0, 1, 1, 2, 2]''',
    "demo_out": "[0, 0, 1, 1, 2, 2]",
    "acm": {
        "stdin": "一行:颜色数组(0/1/2,空格分隔)",
        "stdout": "原地排序后的数组(空格分隔)",
        "sample_in": "2 0 2 1 1 0", "sample_out": "0 0 1 1 2 2",
        "main": '''def main():
    nums = list(map(int, input().split()))
    Solution().sortColors(nums)
    print(*nums)


if __name__ == "__main__":
    main()''',
    },
}

MODES[31] = {
    "core": '''class Solution:
    def nextPermutation(self, nums):
        n = len(nums)
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        l, r = i + 1, n - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1''',
    "demo": '''if __name__ == "__main__":
    nums = [1, 2, 3]
    Solution().nextPermutation(nums)
    print(nums)   # [1, 3, 2]''',
    "demo_out": "[1, 3, 2]",
    "acm": {
        "stdin": "一行:数组(空格分隔)",
        "stdout": "字典序下一个排列(空格分隔)",
        "sample_in": "1 2 3", "sample_out": "1 3 2",
        "main": '''def main():
    nums = list(map(int, input().split()))
    Solution().nextPermutation(nums)
    print(*nums)


if __name__ == "__main__":
    main()''',
    },
}

MODES[287] = {
    "core": '''class Solution:
    def findDuplicate(self, nums):
        slow = fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow''',
    "demo": '''if __name__ == "__main__":
    s = Solution()
    print(s.findDuplicate([1, 3, 4, 2, 2]))   # 2
    print(s.findDuplicate([3, 1, 3, 4, 2]))   # 3''',
    "demo_out": "2\n3",
    "acm": {
        "stdin": "一行:数组(空格分隔,n+1 个数取值 1..n)",
        "stdout": "重复的数",
        "sample_in": "1 3 4 2 2", "sample_out": "2",
        "main": '''def main():
    nums = list(map(int, input().split()))
    print(Solution().findDuplicate(nums))


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
