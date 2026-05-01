# LC 101. 对称二叉树 · Easy · 递归
"""
🔹 直觉
    左右子树是否互为镜像:
        same(a, b) ⇔ a.val == b.val ∧ same(a.left, b.right) ∧ same(a.right, b.left)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree


class Solution:
    def isSymmetric(self, root) -> bool:
        def same(a, b):
            if not a and not b:
                return True
            if not a or not b or a.val != b.val:
                return False
            return same(a.left, b.right) and same(a.right, b.left)
        return not root or same(root.left, root.right)


def _test() -> None:
    s = Solution()
    assert s.isSymmetric(build_tree([1, 2, 2, 3, 4, 4, 3])) is True
    assert s.isSymmetric(build_tree([1, 2, 2, None, 3, None, 3])) is False
    assert s.isSymmetric(None) is True
    print("✅ p101 通过")


if __name__ == "__main__":
    _test()
