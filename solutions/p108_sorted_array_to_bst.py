# LC 108. 将有序数组转换为二叉搜索树 · Easy · 递归构造
"""
🔹 直觉
    取中点为根,左右半分别递归,自然平衡。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import TreeNode


class Solution:
    def sortedArrayToBST(self, nums: list[int]):
        def build(l, r):
            if l > r:
                return None
            m = (l + r) // 2
            return TreeNode(nums[m], build(l, m - 1), build(m + 1, r))
        return build(0, len(nums) - 1)


def _test() -> None:
    from _common.ds import tree_to_level
    s = Solution()
    out = tree_to_level(s.sortedArrayToBST([-10, -3, 0, 5, 9]))
    assert out == [0, -10, 5, None, -3, None, 9] or out == [0, -3, 9, -10, None, 5]
    assert s.sortedArrayToBST([]) is None
    print("✅ p108 通过")


if __name__ == "__main__":
    _test()
