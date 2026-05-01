# LC 207. 课程表 · Medium · 拓扑排序
"""
🔹 题面
    判断是否可修完所有课;前置 [a, b] 表示 b → a。

🔹 解法对比
    | 方法           | 时间    | 空间   | 备注                     |
    |----------------|---------|--------|--------------------------|
    | Kahn(入度+BFS) ★| O(V+E) | O(V+E) | 工程首选;可顺便给出 topo 序 |
    | DFS 三色染色   | O(V+E)  | O(V+E) | 0 未访问 / 1 在栈 / 2 完成 |
"""
from collections import defaultdict, deque


class Solution:
    # 解法 1:Kahn ★ — O(V+E) / O(V+E)
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        g = defaultdict(list)
        indeg = [0] * numCourses
        for a, b in prerequisites:
            g[b].append(a)
            indeg[a] += 1
        q = deque(i for i, d in enumerate(indeg) if d == 0)
        seen = 0
        while q:
            u = q.popleft()
            seen += 1
            for v in g[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return seen == numCourses

    # 解法 2:DFS 三色染色 — O(V+E) / O(V+E)
    def canFinish_dfs(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        g = defaultdict(list)
        for a, b in prerequisites:
            g[b].append(a)
        color = [0] * numCourses           # 0 未访问 / 1 路径中 / 2 完成

        def dfs(u):
            if color[u] == 1:
                return False               # 回边 → 有环
            if color[u] == 2:
                return True
            color[u] = 1
            for v in g[u]:
                if not dfs(v):
                    return False
            color[u] = 2
            return True

        return all(dfs(u) for u in range(numCourses))


def _test() -> None:
    s = Solution()
    cases = [
        ((2, [[1, 0]]), True),
        ((2, [[1, 0], [0, 1]]), False),
        ((4, [[1, 0], [2, 1], [3, 2]]), True),
    ]
    for args, want in cases:
        for fn in (s.canFinish, s.canFinish_dfs):
            assert fn(*args) is want
    print("✅ p207 通过 2 解法")


if __name__ == "__main__":
    _test()
