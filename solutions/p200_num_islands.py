# LC 200. 岛屿数量 · Medium · DFS / BFS / 并查集
"""
🔹 解法对比
    | 方法    | 时间    | 空间    | 备注                       |
    |---------|---------|---------|----------------------------|
    | DFS ★  | O(mn)   | O(mn) 栈| 经典,代码最短              |
    | BFS     | O(mn)   | O(min(m,n)) | 队列宽度受限           |
    | 并查集  | O(mn α) | O(mn)   | 适合"动态加陆地"扩展        |
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import UnionFind
from collections import deque


class Solution:
    # 解法 1:DFS ★ — O(mn) / O(mn)
    def numIslands(self, grid: list[list[str]]) -> int:
        if not grid:
            return 0
        m, n = len(grid), len(grid[0])

        def dfs(i, j):
            if i < 0 or j < 0 or i >= m or j >= n or grid[i][j] != '1':
                return
            grid[i][j] = '0'
            dfs(i + 1, j); dfs(i - 1, j); dfs(i, j + 1); dfs(i, j - 1)

        cnt = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    cnt += 1
                    dfs(i, j)
        return cnt

    # 解法 2:BFS — O(mn) / O(min(m,n))
    def numIslands_bfs(self, grid: list[list[str]]) -> int:
        if not grid:
            return 0
        m, n = len(grid), len(grid[0])
        cnt = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] != '1':
                    continue
                cnt += 1
                q = deque([(i, j)])
                grid[i][j] = '0'
                while q:
                    x, y = q.popleft()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == '1':
                            grid[nx][ny] = '0'
                            q.append((nx, ny))
        return cnt

    # 解法 3:并查集 — O(mn α) / O(mn)
    def numIslands_uf(self, grid: list[list[str]]) -> int:
        if not grid:
            return 0
        m, n = len(grid), len(grid[0])
        uf = UnionFind(m * n)
        zeros = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '0':
                    zeros += 1
                    continue
                for di, dj in ((1, 0), (0, 1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == '1':
                        uf.union(i * n + j, ni * n + nj)
        return uf.count - zeros


def _test() -> None:
    s = Solution()
    g1 = [["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"],
          ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]
    g2 = [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"],
          ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]
    for fn in (s.numIslands, s.numIslands_bfs, s.numIslands_uf):
        assert fn([row[:] for row in g1]) == 1
        assert fn([row[:] for row in g2]) == 3
    print("✅ p200 通过 3 解法")


if __name__ == "__main__":
    _test()
