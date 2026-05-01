# LC 994. 腐烂的橘子 · Medium · 多源 BFS
"""
🔹 题面
    2 烂、1 鲜、0 空;每一分钟烂橘子四向感染。返回所有烂掉所需分钟,
    若无法全烂返回 -1。

🔹 直觉
    多源 BFS:把所有初始烂橘子一起入队作为第 0 层,层序扩展。
"""
from collections import deque


class Solution:
    def orangesRotting(self, g: list[list[int]]) -> int:
        m, n = len(g), len(g[0])
        q = deque()
        fresh = 0
        for i in range(m):
            for j in range(n):
                if g[i][j] == 2:
                    q.append((i, j))
                elif g[i][j] == 1:
                    fresh += 1
        if fresh == 0:
            return 0
        minutes = 0
        while q and fresh:
            for _ in range(len(q)):
                x, y = q.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and g[nx][ny] == 1:
                        g[nx][ny] = 2
                        fresh -= 1
                        q.append((nx, ny))
            minutes += 1
        return minutes if fresh == 0 else -1


def _test() -> None:
    s = Solution()
    assert s.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert s.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    assert s.orangesRotting([[0, 2]]) == 0
    print("✅ p994 通过")


if __name__ == "__main__":
    _test()
