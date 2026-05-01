# LC 239. 滑动窗口最大值 · Hard · 单调队列
"""
🔹 题面
    返回长度 k 的滑动窗口最大值序列。

🔹 直觉(单调递减队列)
    队列存的是**下标**,从队头到队尾对应的值**单调递减**。
    新元素入队时弹出所有比它小的尾部(它们将永远不会成为答案);
    队头若已超出窗口左界则弹出。窗口准备好后队头即最大值。

🔹 复杂度 O(n) / O(k)
    每个下标至多入/出队一次。

🔹 踩坑
    队列存下标,而不是值;否则无法判断是否过期。
"""
from collections import deque


class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        dq: deque[int] = deque()
        ans: list[int] = []
        for i, x in enumerate(nums):
            while dq and nums[dq[-1]] <= x:
                dq.pop()
            dq.append(i)
            if dq[0] <= i - k:
                dq.popleft()
            if i >= k - 1:
                ans.append(nums[dq[0]])
        return ans


def _test() -> None:
    s = Solution()
    assert s.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert s.maxSlidingWindow([1], 1) == [1]
    assert s.maxSlidingWindow([1, -1], 1) == [1, -1]
    print("✅ p239 通过")


if __name__ == "__main__":
    _test()
