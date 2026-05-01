# LC 437. 路径总和 III · Medium · 前缀和 + 哈希
"""
🔹 题面
    任意"自上而下"路径的节点和等于 targetSum 的路径数(可不到根/不到叶)。

🔹 直觉
    把二叉树看成"从根到 X"的前缀和。当前节点累计和 = curSum,
    若存在 prefix[curSum - target] 个祖先,则有那么多条新路径。
    DFS 进入时 +1,回溯时 -1(避免兄弟分支互相影响)。

🔹 复杂度 O(n) / O(h)
"""
from collections import defaultdict
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree


class Solution:
    def pathSum(self, root, targetSum: int) -> int:
        cnt = defaultdict(int)
        cnt[0] = 1
        ans = 0

        def dfs(n, cur):
            nonlocal ans
            if not n:
                return
            cur += n.val
            ans += cnt[cur - targetSum]
            cnt[cur] += 1
            dfs(n.left, cur)
            dfs(n.right, cur)
            cnt[cur] -= 1

        dfs(root, 0)
        return ans


def _test() -> None:
    s = Solution()
    assert s.pathSum(build_tree([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1]), 8) == 3
    assert s.pathSum(build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]), 22) == 3
    assert s.pathSum(None, 0) == 0
    print("✅ p437 通过")


if __name__ == "__main__":
    _test()
