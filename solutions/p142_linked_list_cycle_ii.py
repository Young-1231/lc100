# LC 142. 环形链表 II · Medium · Floyd 数学
"""
🔹 题面
    返回入环节点。

🔹 解法对比
    | 方法            | 时间 | 空间 | 备注                  |
    |-----------------|------|------|-----------------------|
    | 哈希记录访问过  | O(n) | O(n) | 一目了然              |
    | Floyd 数学 ★   | O(n) | O(1) | 经典,理解入环点公式  |

🔹 Floyd 推导
    a = head→入环点距离, b = 入环点→相遇点, c = 相遇点→入环点。
    fast 走 2 * slow:a + b + k(b+c) = 2(a + b) → a = c + (k-1)(b+c)。
    所以让一个指针从 head、另一个从相遇点同步前进,必相遇于入环点。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_list


class Solution:
    # 解法 1:Floyd ★ — O(n) / O(1)
    def detectCycle(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                p = head
                while p is not slow:
                    p = p.next
                    slow = slow.next
                return p
        return None

    # 解法 2:哈希 — O(n) / O(n)
    def detectCycle_set(self, head):
        seen = set()
        cur = head
        while cur:
            if id(cur) in seen:
                return cur
            seen.add(id(cur))
            cur = cur.next
        return None


def _test() -> None:
    s = Solution()
    h = build_list([3, 2, 0, -4])
    h.next.next.next.next = h.next
    for fn in (s.detectCycle, s.detectCycle_set):
        assert fn(h) is h.next
        assert fn(build_list([1, 2])) is None
    print("✅ p142 通过 2 解法")


if __name__ == "__main__":
    _test()
