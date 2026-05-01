# LC 141. 环形链表 · Easy · Floyd 龟兔
"""
🔹 题面
    判断链表是否有环。

🔹 解法对比
    | 方法            | 时间 | 空间 | 备注                        |
    |-----------------|------|------|-----------------------------|
    | 哈希记录访问过  | O(n) | O(n) | 直观                        |
    | Floyd 龟兔 ★   | O(n) | O(1) | 经典,面试默写              |
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_list


class Solution:
    # 解法 1:Floyd 龟兔 ★ — O(n) / O(1)
    def hasCycle(self, head) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    # 解法 2:哈希 — O(n) / O(n)
    def hasCycle_set(self, head) -> bool:
        seen = set()
        cur = head
        while cur:
            if id(cur) in seen:
                return True
            seen.add(id(cur))
            cur = cur.next
        return False


def _test() -> None:
    s = Solution()
    h = build_list([3, 2, 0, -4])
    h.next.next.next.next = h.next
    for fn in (s.hasCycle, s.hasCycle_set):
        assert fn(h) is True
        assert fn(build_list([1])) is False
        assert fn(None) is False
    print("✅ p141 通过 2 解法")


if __name__ == "__main__":
    _test()
