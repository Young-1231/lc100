# LC 169. 多数元素 · Easy · Boyer-Moore 投票
"""
🔹 直觉
    "众数计数 +1,他人 -1";票数为 0 时换候选。多数元素必然胜出。
"""


class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        cand, cnt = 0, 0
        for x in nums:
            if cnt == 0:
                cand = x
            cnt += 1 if x == cand else -1
        return cand


def _test() -> None:
    s = Solution()
    assert s.majorityElement([3, 2, 3]) == 3
    assert s.majorityElement([2, 2, 1, 1, 1, 2, 2]) == 2
    assert s.majorityElement([1]) == 1
    print("✅ p169 通过")


if __name__ == "__main__":
    _test()
