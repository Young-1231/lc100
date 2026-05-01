# LC 23. 合并 K 个升序链表 · Hard · 堆 / 分治
"""
🔹 题面
    合并 K 个升序链表,返回总升序链表。N 是总节点数,K 是链表数。

🔹 解法对比
    | 方法           | 时间        | 空间    | 备注                             |
    |----------------|-------------|---------|----------------------------------|
    | 顺次两两合并   | O(NK)       | O(1)    | 朴素                             |
    | 小顶堆 ★      | O(N log K)  | O(K)    | 每次取最小,分布式 / 大数据流也用 |
    | 分治两两归并   | O(N log K)  | O(log K)| 类似归并排序,递归栈              |

🔹 trick(Python heapq)
    ListNode 没定义 < ;入堆元组 (val, idx, node),idx 唯一防 tie。
"""
import heapq
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import ListNode, build_list, list_to_array


def _merge2(a, b):
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
    # 解法 1:小顶堆 ★ — O(N log K) / O(K)
    def mergeKLists(self, lists):
        h: list = []
        for i, head in enumerate(lists):
            if head:
                heapq.heappush(h, (head.val, i, head))
        dummy = ListNode()
        t = dummy
        while h:
            v, i, node = heapq.heappop(h)
            t.next = node
            t = t.next
            if node.next:
                heapq.heappush(h, (node.next.val, i, node.next))
        return dummy.next

    # 解法 2:分治两两归并 — O(N log K) / O(log K)
    def mergeKLists_divide(self, lists):
        if not lists:
            return None

        def go(l, r):
            if l == r:
                return lists[l]
            m = (l + r) // 2
            return _merge2(go(l, m), go(m + 1, r))

        return go(0, len(lists) - 1)

    # 解法 3:顺次两两合并 — O(NK) / O(1)
    def mergeKLists_seq(self, lists):
        head = None
        for l in lists:
            head = _merge2(head, l)
        return head


def _test() -> None:
    s = Solution()
    src = [[1, 4, 5], [1, 3, 4], [2, 6]]
    want = [1, 1, 2, 3, 4, 4, 5, 6]
    for fn in (s.mergeKLists, s.mergeKLists_divide, s.mergeKLists_seq):
        ls = [build_list(x) for x in src]
        assert list_to_array(fn(ls)) == want
    assert s.mergeKLists([]) is None
    assert s.mergeKLists([None]) is None
    print("✅ p023 通过 3 解法")


if __name__ == "__main__":
    _test()
