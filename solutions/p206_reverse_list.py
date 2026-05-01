# LC 206. 反转链表 · Easy · 链表基础
"""
🔹 题面
    反转单链表。

🔹 解法对比
    | 方法     | 时间 | 空间    | 备注                        |
    |----------|------|---------|-----------------------------|
    | 迭代 ★  | O(n) | O(1)    | 三指针 prev/cur/nxt          |
    | 递归     | O(n) | O(n) 栈 | 优雅,深递归可能爆栈        |
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_list, list_to_array


class Solution:
    # 解法 1:迭代 ★ — O(n) / O(1)
    def reverseList(self, head):
        prev, cur = None, head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        return prev

    # 解法 2:递归 — O(n) / O(n)
    def reverseList_recursive(self, head):
        if not head or not head.next:
            return head
        new_head = self.reverseList_recursive(head.next)
        head.next.next = head
        head.next = None
        return new_head


def _test() -> None:
    s = Solution()
    for fn in (s.reverseList, s.reverseList_recursive):
        assert list_to_array(fn(build_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
        assert list_to_array(fn(build_list([]))) == []
        assert list_to_array(fn(build_list([1]))) == [1]
    print("✅ p206 通过 2 解法")


if __name__ == "__main__":
    _test()
