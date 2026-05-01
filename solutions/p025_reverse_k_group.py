# LC 25. K 个一组翻转链表 · Hard · 链表
"""
🔹 题面
    每 K 个一组翻转节点;不足 K 不动。

🔹 解法对比
    | 方法    | 时间 | 空间   | 备注          |
    |---------|------|--------|---------------|
    | 迭代 ★ | O(n) | O(1)   | 工程实现      |
    | 递归    | O(n) | O(n/k) | 实现简洁       |
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import ListNode, build_list, list_to_array


class Solution:
    # 解法 1:迭代 ★ — O(n) / O(1)
    def reverseKGroup(self, head, k: int):
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
            group_prev = tmp

    # 解法 2:递归 — O(n) / O(n/k) 栈
    def reverseKGroup_rec(self, head, k: int):
        # 先看是否够 k 个
        cur = head
        for _ in range(k):
            if not cur:
                return head
            cur = cur.next
        # 反转前 k 个
        prev, cur = None, head
        for _ in range(k):
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        head.next = self.reverseKGroup_rec(cur, k)
        return prev


def _test() -> None:
    s = Solution()
    cases = [
        (([1, 2, 3, 4, 5], 2), [2, 1, 4, 3, 5]),
        (([1, 2, 3, 4, 5], 3), [3, 2, 1, 4, 5]),
        (([1, 2], 1), [1, 2]),
    ]
    for (arr, k), want in cases:
        for fn in (s.reverseKGroup, s.reverseKGroup_rec):
            assert list_to_array(fn(build_list(arr), k)) == want
    print("✅ p025 通过 2 解法")


if __name__ == "__main__":
    _test()
