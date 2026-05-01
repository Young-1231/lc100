# LC 15. 三数之和 · Medium · 双指针
"""
🔹 题面
    返回所有不重复三元组 (a,b,c),其中 a+b+c=0。

🔹 解法对比
    | 方法              | 时间   | 空间   | 备注                    |
    |-------------------|--------|--------|-------------------------|
    | 暴力三重循环+set  | O(n³)  | O(n)   | 排序后 set 去重         |
    | 排序 + 双指针 ★  | O(n²)  | O(1)   | 经典模板,面试首选      |
    | 排序 + 哈希       | O(n²)  | O(n)   | 固定 a,在剩余里 2Sum   |

🔹 直觉(双指针)
    排序后固定 i,问题退化为"在 i+1..n-1 找两数之和 = -nums[i]" → 双指针。

🔹 三处去重(出错率最高)
    1) i 跳过相同的 (i>0 and nums[i]==nums[i-1])
    2) 找到答案后 l 推进时跳过相同的
    3) 找到答案后 r 退后时跳过相同的
"""


class Solution:
    # 解法 1:暴力 + set 去重 — O(n³) / O(n)
    def threeSum_brute(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        out: set[tuple[int, int, int]] = set()
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        out.add(tuple(sorted((nums[i], nums[j], nums[k]))))
        return [list(t) for t in out]

    # 解法 2:排序 + 双指针 ★ — O(n²) / O(1)
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        n, ans = len(nums), []
        for i in range(n - 2):
            if nums[i] > 0:
                break
            if i and nums[i] == nums[i - 1]:
                continue
            l, r, target = i + 1, n - 1, -nums[i]
            while l < r:
                s = nums[l] + nums[r]
                if s == target:
                    ans.append([nums[i], nums[l], nums[r]])
                    l += 1; r -= 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
                    while l < r and nums[r] == nums[r + 1]:
                        r -= 1
                elif s < target:
                    l += 1
                else:
                    r -= 1
        return ans

    # 解法 3:排序 + 哈希(每对 a, b 在剩余里查 -a-b)— O(n²) / O(n)
    def threeSum_hash(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        n, ans = len(nums), []
        for i in range(n - 2):
            if nums[i] > 0:
                break
            if i and nums[i] == nums[i - 1]:
                continue
            seen: set[int] = set()
            j = i + 1
            while j < n:
                want = -nums[i] - nums[j]
                if want in seen:
                    ans.append([nums[i], want, nums[j]])
                    while j + 1 < n and nums[j + 1] == nums[j]:
                        j += 1
                seen.add(nums[j])
                j += 1
        return ans


def _norm(x):
    return sorted(tuple(sorted(t)) for t in x)


def _test() -> None:
    s = Solution()
    cases = [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([], []),
        ([0, 0, 0], [[0, 0, 0]]),
        ([0, 0, 0, 0], [[0, 0, 0]]),
    ]
    for arg, want in cases:
        for fn in (s.threeSum, s.threeSum_brute, s.threeSum_hash):
            assert _norm(fn(arg[:])) == _norm(want)
    print("✅ p015 通过 3 解法")


if __name__ == "__main__":
    _test()
