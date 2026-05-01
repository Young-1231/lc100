# LC 2. 两数相加 · Medium · 链表模拟
"""
🔹 题面
    每个节点存一位数字、低位在前,返回它们之和的链表。

🔹 直觉
    从低位到高位逐位相加,carry 进位。

🔹 复杂度 O(max(m,n)) / O(1)(忽略输出)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import ListNode, build_list, list_to_array


class Solution:
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode()
        tail = dummy
        carry = 0
        while l1 or l2 or carry:
            a = l1.val if l1 else 0
            b = l2.val if l2 else 0
            s = a + b + carry
            carry, d = divmod(s, 10)
            tail.next = ListNode(d)
            tail = tail.next
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next
        return dummy.next


def _test() -> None:
    s = Solution()
    assert list_to_array(s.addTwoNumbers(build_list([2, 4, 3]), build_list([5, 6, 4]))) == [7, 0, 8]
    assert list_to_array(s.addTwoNumbers(build_list([0]), build_list([0]))) == [0]
    assert list_to_array(s.addTwoNumbers(build_list([9, 9]), build_list([1]))) == [0, 0, 1]
    print("✅ p002 通过")


if __name__ == "__main__":
    _test()
