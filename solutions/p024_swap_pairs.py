# LC 24. 两两交换链表中的节点 · Medium · 链表
"""
🔹 题面
    两两交换相邻节点(不许只换值)。

🔹 解法对比
    | 方法     | 时间 | 空间    | 备注          |
    |----------|------|---------|---------------|
    | 迭代 ★  | O(n) | O(1)    | 哨兵 + prev   |
    | 递归     | O(n) | O(n) 栈 | 优雅           |
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import ListNode, build_list, list_to_array


class Solution:
    # 解法 1:迭代 ★ — O(n) / O(1)
    def swapPairs(self, head):
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next and prev.next.next:
            a, b = prev.next, prev.next.next
            prev.next = b
            a.next = b.next
            b.next = a
            prev = a
        return dummy.next

    # 解法 2:递归 — O(n) / O(n)
    def swapPairs_rec(self, head):
        if not head or not head.next:
            return head
        nxt = head.next
        head.next = self.swapPairs_rec(nxt.next)
        nxt.next = head
        return nxt


def _test() -> None:
    s = Solution()
    cases = [([1, 2, 3, 4], [2, 1, 4, 3]), ([], []), ([1], [1]), ([1, 2, 3], [2, 1, 3])]
    for arg, want in cases:
        for fn in (s.swapPairs, s.swapPairs_rec):
            assert list_to_array(fn(build_list(arg))) == want
    print("✅ p024 通过 2 解法")


if __name__ == "__main__":
    _test()
