# LC 105. 从前序与中序构造二叉树 · Medium · 递归 + 哈希
"""
🔹 题面
    给定前序与中序数组,构造唯一二叉树。

🔹 解法对比
    | 方法            | 时间 | 空间 | 备注              |
    |-----------------|------|------|-------------------|
    | 递归 + 哈希 ★  | O(n) | O(n) | 哈希 inorder 索引 |
    | 迭代 + 栈       | O(n) | O(n) | 巧用前序 + 栈     |

🔹 递归直觉
    前序首元素是根,中序里左侧是左子树、右侧是右子树。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import TreeNode, tree_to_level


class Solution:
    # 解法 1:递归 + 哈希 ★ — O(n) / O(n)
    def buildTree(self, preorder: list[int], inorder: list[int]):
        idx = {v: i for i, v in enumerate(inorder)}

        def build(pl, pr, il, ir):
            if pl > pr:
                return None
            root_val = preorder[pl]
            i = idx[root_val]
            left_len = i - il
            return TreeNode(
                root_val,
                build(pl + 1, pl + left_len, il, i - 1),
                build(pl + left_len + 1, pr, i + 1, ir),
            )

        return build(0, len(preorder) - 1, 0, len(inorder) - 1)

    # 解法 2:迭代 + 栈 — O(n) / O(n)
    # 思路:沿着 preorder 顺序,栈顶始终是"当前最深的左链节点"。
    # 当 inorder 当前指向的值等于栈顶值时,说明左链结束,弹栈直到不等,再把下一个 pre 值挂到右子树。
    def buildTree_iter(self, preorder: list[int], inorder: list[int]):
        if not preorder:
            return None
        root = TreeNode(preorder[0])
        st = [root]
        in_i = 0
        for v in preorder[1:]:
            node = st[-1]
            if node.val != inorder[in_i]:
                node.left = TreeNode(v)
                st.append(node.left)
            else:
                while st and st[-1].val == inorder[in_i]:
                    node = st.pop()
                    in_i += 1
                node.right = TreeNode(v)
                st.append(node.right)
        return root


def _test() -> None:
    s = Solution()
    cases = [
        (([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]), [3, 9, 20, None, None, 15, 7]),
        (([], []), []),
        (([-1], [-1]), [-1]),
    ]
    for args, want in cases:
        for fn in (s.buildTree, s.buildTree_iter):
            assert tree_to_level(fn(*args)) == want
    print("✅ p105 通过 2 解法")


if __name__ == "__main__":
    _test()
