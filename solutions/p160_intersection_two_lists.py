# LC 160. 相交链表 · Easy · 双指针
"""
🔹 题面
    返回两个链表相交的起点;不相交返回 None。要求 O(1) 额外空间。

🔹 直觉(浪漫双指针)
    a 走 A 完了走 B,b 走 B 完了走 A。
    若相交,二者相遇于交点;若不相交,同时走到 None。
    总步数 = lenA + lenB,相同。

🔹 复杂度 O(m+n) / O(1)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import ListNode, build_list


class Solution:
    def getIntersectionNode(self, headA, headB):
        a, b = headA, headB
        while a is not b:
            a = a.next if a else headB
            b = b.next if b else headA
        return a


def _test() -> None:
    s = Solution()
    common = build_list([8, 4, 5])
    a = ListNode(4); a.next = ListNode(1); a.next.next = common
    b = ListNode(5); b.next = ListNode(6); b.next.next = ListNode(1); b.next.next.next = common
    assert s.getIntersectionNode(a, b) is common
    assert s.getIntersectionNode(build_list([1, 2]), build_list([3, 4])) is None
    print("✅ p160 通过")


if __name__ == "__main__":
    _test()
