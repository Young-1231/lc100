# LC 236. 二叉树的最近公共祖先 · Medium · 递归
"""
🔹 直觉
    后序:在每节点处问"左右子树各自找到了 p 还是 q"。
        - 都找到 → 当前就是 LCA
        - 只一边找到 → 把那个返回上去
        - 都没找到 → 返回 None
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree, TreeNode


class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if not root or root is p or root is q:
            return root
        l = self.lowestCommonAncestor(root.left, p, q)
        r = self.lowestCommonAncestor(root.right, p, q)
        if l and r:
            return root
        return l or r


def _find(root, val):
    if not root:
        return None
    if root.val == val:
        return root
    return _find(root.left, val) or _find(root.right, val)


def _test() -> None:
    s = Solution()
    t = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p, q = _find(t, 5), _find(t, 1)
    assert s.lowestCommonAncestor(t, p, q).val == 3
    p, q = _find(t, 5), _find(t, 4)
    assert s.lowestCommonAncestor(t, p, q).val == 5
    print("✅ p236 通过")


if __name__ == "__main__":
    _test()
