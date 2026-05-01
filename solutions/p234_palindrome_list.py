# LC 234. 回文链表 · Easy · 快慢指针 + 反转
"""
🔹 题面
    判断单链表是否回文。

🔹 解法对比
    | 方法                | 时间 | 空间 | 备注                       |
    |---------------------|------|------|----------------------------|
    | 复制到数组对撞      | O(n) | O(n) | 写法最直观                  |
    | 快慢指针+反转后半 ★ | O(n) | O(1) | 经典,需小心还原(若题面要求)|
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_list


def _reverse(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


class Solution:
    # 解法 1:快慢指针 + 反转后半 ★ — O(n) / O(1)
    def isPalindrome(self, head) -> bool:
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
        return True

    # 解法 2:复制到数组双指针 — O(n) / O(n)
    def isPalindrome_array(self, head) -> bool:
        a = []
        cur = head
        while cur:
            a.append(cur.val)
            cur = cur.next
        l, r = 0, len(a) - 1
        while l < r:
            if a[l] != a[r]:
                return False
            l += 1; r -= 1
        return True


def _test() -> None:
    s = Solution()
    cases = [([1, 2, 2, 1], True), ([1, 2], False), ([1], True), ([1, 2, 3, 2, 1], True)]
    for arg, want in cases:
        for fn in (s.isPalindrome_array,):       # 测原数组解法
            assert fn(build_list(arg)) is want
        # 反转法会破坏链表,每次重建
        assert s.isPalindrome(build_list(arg)) is want
    print("✅ p234 通过 2 解法")


if __name__ == "__main__":
    _test()
