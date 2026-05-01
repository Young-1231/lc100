# LC 240. 搜索二维矩阵 II · Medium · 矩阵
"""
🔹 题面
    每行升序、每列升序,搜索目标 target。

🔹 直觉(Z 字搜索)
    从右上角出发:
        m[i][j] == target → 找到
        m[i][j]  > target → j-=1   (该列下方都更大,可剪)
        m[i][j]  < target → i+=1
    每步至少减少一个维度,O(m+n)。

🔹 复杂度 O(m+n) / O(1)
"""


class Solution:
    def searchMatrix(self, m: list[list[int]], target: int) -> bool:
        if not m or not m[0]:
            return False
        i, j = 0, len(m[0]) - 1
        while i < len(m) and j >= 0:
            if m[i][j] == target:
                return True
            if m[i][j] > target:
                j -= 1
            else:
                i += 1
        return False


def _test() -> None:
    s = Solution()
    M = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22],
         [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
    assert s.searchMatrix(M, 5) is True
    assert s.searchMatrix(M, 20) is False
    assert s.searchMatrix([], 1) is False
    print("✅ p240 通过")


if __name__ == "__main__":
    _test()
