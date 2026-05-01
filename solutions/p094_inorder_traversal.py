# LC 94. 二叉树的中序遍历 · Easy · 遍历
"""
🔹 题面
    返回中序遍历(左-根-右)结果。

🔹 解法对比
    | 方法     | 时间 | 空间      | 备注                            |
    |----------|------|-----------|---------------------------------|
    | 递归     | O(n) | O(h)      | 简洁                            |
    | 迭代+栈 ★| O(n) | O(h)      | 经典写法,一路向左,弹出向右     |
    | Morris   | O(n) | O(1)      | 临时改父指针,做完恢复;难度大   |
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree


class Solution:
    # 解法 1:迭代 + 栈 ★ — O(n) / O(h)
    def inorderTraversal(self, root) -> list[int]:
        out, stack, cur = [], [], root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            out.append(cur.val)
            cur = cur.right
        return out

    # 解法 2:递归 — O(n) / O(h)
    def inorderTraversal_rec(self, root) -> list[int]:
        out: list[int] = []

        def dfs(n):
            if not n:
                return
            dfs(n.left)
            out.append(n.val)
            dfs(n.right)

        dfs(root)
        return out

    # 解法 3:Morris 遍历 — O(n) / O(1)
    # 核心:对每个有左子树的节点,把它的"前驱(左子树最右)"的 right 接到自己,
    # 形成线索;遍历完左子树后顺着线索回到自己,再断开。
    def inorderTraversal_morris(self, root) -> list[int]:
        out: list[int] = []
        cur = root
        while cur:
            if cur.left:
                pred = cur.left
                while pred.right and pred.right is not cur:
                    pred = pred.right
                if pred.right is None:
                    pred.right = cur
                    cur = cur.left
                else:
                    pred.right = None       # 恢复
                    out.append(cur.val)
                    cur = cur.right
            else:
                out.append(cur.val)
                cur = cur.right
        return out


def _test() -> None:
    s = Solution()
    cases = [([1, None, 2, 3], [1, 3, 2]), ([], []), ([1], [1])]
    for arg, want in cases:
        for fn in (s.inorderTraversal, s.inorderTraversal_rec, s.inorderTraversal_morris):
            assert fn(build_tree(arg)) == want
    print("✅ p094 通过 3 解法")


if __name__ == "__main__":
    _test()
