# LC 21. 合并两个有序链表 · Easy · 链表归并
"""
🔹 题面
    合并两个升序链表为一个新升序链表。

🔹 直觉
    哨兵节点 dummy,谁小接谁;末尾接剩余。

🔹 复杂度 O(m+n) / O(1)(若复用原节点)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import ListNode, build_list, list_to_array


class Solution:
    def mergeTwoLists(self, l1, l2):
        dummy = ListNode()
        tail = dummy
        while l1 and l2:
            if l1.val <= l2.val:
                tail.next, l1 = l1, l1.next
            else:
                tail.next, l2 = l2, l2.next
            tail = tail.next
        tail.next = l1 or l2
        return dummy.next


def _test() -> None:
    s = Solution()
    out = s.mergeTwoLists(build_list([1, 2, 4]), build_list([1, 3, 4]))
    assert list_to_array(out) == [1, 1, 2, 3, 4, 4]
    assert s.mergeTwoLists(None, None) is None
    assert list_to_array(s.mergeTwoLists(None, build_list([0]))) == [0]
    print("✅ p021 通过")


if __name__ == "__main__":
    _test()
