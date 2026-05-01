# LC 230. BST 中第 K 小元素 · Medium · 中序
"""
🔹 直觉
    BST 中序就是升序;迭代中序边走边数 k。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree


class Solution:
    def kthSmallest(self, root, k: int) -> int:
        stack, cur = [], root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            k -= 1
            if k == 0:
                return cur.val
            cur = cur.right
        return -1


def _test() -> None:
    s = Solution()
    assert s.kthSmallest(build_tree([3, 1, 4, None, 2]), 1) == 1
    assert s.kthSmallest(build_tree([5, 3, 6, 2, 4, None, None, 1]), 3) == 3
    print("✅ p230 通过")


if __name__ == "__main__":
    _test()
