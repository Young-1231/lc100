# LC 148. 排序链表 · Medium · 归并排序
"""
🔹 题面
    O(n log n) 时间排序链表。

🔹 解法对比
    | 方法                | 时间       | 空间      | 备注                  |
    |---------------------|------------|-----------|-----------------------|
    | 自顶向下归并 ★     | O(n log n) | O(log n)  | 递归栈                |
    | 自底向上归并        | O(n log n) | O(1)      | 严格 O(1) 非递归      |
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import ListNode, build_list, list_to_array


def _merge(a, b):
    dummy = ListNode()
    t = dummy
    while a and b:
        if a.val <= b.val:
            t.next, a = a, a.next
        else:
            t.next, b = b, b.next
        t = t.next
    t.next = a or b
    return dummy.next


class Solution:
    # 解法 1:自顶向下归并 ★ — O(n log n) / O(log n)
    def sortList(self, head):
        if not head or not head.next:
            return head
        prev, slow, fast = None, head, head
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        prev.next = None
        return _merge(self.sortList(head), self.sortList(slow))

    # 解法 2:自底向上归并 — O(n log n) / O(1)
    def sortList_iter(self, head):
        if not head or not head.next:
            return head
        # 求长度
        n = 0
        cur = head
        while cur:
            n += 1
            cur = cur.next
        dummy = ListNode(0, head)
        size = 1
        while size < n:
            prev = dummy
            cur = dummy.next
            while cur:
                left = cur
                right = self._split(left, size)
                cur = self._split(right, size)
                prev.next = _merge(left, right)
                while prev.next:
                    prev = prev.next
            size *= 2
        return dummy.next

    @staticmethod
    def _split(head, size):
        """走 size 步,在第 size 个之后切断,返回切断后的下一段头。"""
        for _ in range(size - 1):
            if not head:
                break
            head = head.next
        if not head:
            return None
        nxt = head.next
        head.next = None
        return nxt

    # 内部归并工具
    def _merge(self, a, b):
        return _merge(a, b)


def _test() -> None:
    s = Solution()
    for fn in (s.sortList, s.sortList_iter):
        assert list_to_array(fn(build_list([4, 2, 1, 3]))) == [1, 2, 3, 4]
        assert list_to_array(fn(build_list([-1, 5, 3, 4, 0]))) == [-1, 0, 3, 4, 5]
        assert list_to_array(fn(build_list([]))) == []
    print("✅ p148 通过 2 解法")


if __name__ == "__main__":
    _test()
