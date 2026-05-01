# 二分查找 模式表

## 三种语义

```
找等于 X 的下标(可能不存在)
找第一个 ≥ X 的下标       ← lower_bound = bisect_left
找第一个 > X 的下标        ← upper_bound = bisect_right
```

## 红蓝染色法(灵神)

把数组想成左红(不满足)+ 右蓝(满足)的染色过程。
- l 为最后一个红;r 为第一个蓝。
- 我们要找"第一个蓝"。

```python
l, r = -1, n              # 闭右开
while l + 1 < r:
    m = (l + r) // 2
    if check(m):          # 蓝
        r = m
    else:                  # 红
        l = m
return r
```

## 对照 LC 题

| 题 | 用法 | 关键 |
| --- | --- | --- |
| 35 | lower_bound | 直接 bisect_left |
| 34 | first / last | bisect_left + bisect_right - 1 |
| 33 | 旋转数组定位 | 先判哪一半有序 |
| 153 | 旋转数组最小值 | 比较 nums[m] 与 nums[r] |
| 4 | 中位数 | 在短数组上二分切分点 |
| 74 | 矩阵当数组 | idx 转 (r, c) |
| 240 | Z 字搜索 | 不是二分,O(m+n) |

## 旋转数组左半 / 右半判别

```
nums = [4,5,6,7, 0,1,2]
              ↑
              mid

如果 nums[l] <= nums[mid]:
    左半 [l..mid] 是升序的
    判断 target 是否落在 [nums[l], nums[mid]) → 收缩 r;否则收缩 l
else:
    右半 [mid..r] 是升序的
    判断 target 是否落在 (nums[mid], nums[r]]
```
