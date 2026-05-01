# LC 19. 删除链表的倒数第 N 个结点 · Medium · 双指针 / 哨兵
"""
🔹 题面
    一次扫描删掉倒数第 N 个节点。

🔹 直觉
    哨兵 + 快慢指针:fast 先走 n+1 步,然后 fast/slow 同步,fast=None 时 slow.next 即待删。

🔹 复杂度 O(L) / O(1)

🔹 踩坑
    必须用 dummy,否则删除头节点要分支处理。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import ListNode, build_list, list_to_array


class Solution:
    def removeNthFromEnd(self, head, n: int):
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n + 1):
            fast = fast.next
        while fast:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return dummy.next


def _test() -> None:
    s = Solution()
    assert list_to_array(s.removeNthFromEnd(build_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    assert list_to_array(s.removeNthFromEnd(build_list([1]), 1)) == []
    assert list_to_array(s.removeNthFromEnd(build_list([1, 2]), 1)) == [1]
    assert list_to_array(s.removeNthFromEnd(build_list([1, 2]), 2)) == [2]
    print("✅ p019 通过")


if __name__ == "__main__":
    _test()
