# 可视化与模式索引

| 文件 | 主题 |
| --- | --- |
| [01_window_patterns](01_window_patterns.md) | 滑动窗口 / 子串 |
| [02_linked_list_patterns](02_linked_list_patterns.md) | 链表 |
| [03_tree_patterns](03_tree_patterns.md) | 二叉树 |
| [04_dp_patterns](04_dp_patterns.md) | DP / 背包 |
| [05_backtrack_patterns](05_backtrack_patterns.md) | 回溯 |
| [06_binary_search_patterns](06_binary_search_patterns.md) | 二分查找 |
| [07_monotonic_stack_heap](07_monotonic_stack_heap.md) | 单调栈 / 堆 |

## 推荐阅读顺序

每天**先**读对应模式表(15 分钟),再做题。模式 → 题 → 题 → 模式回看。

## 个人错题本(用法建议)

在每题文件底部加一段:

```python
# 我的错题:
# - 没注意到 nums 可能为空 → 用 max() 报错。下次先 if not nums: return 0。
# - 双指针写成了 < 应该是 <=。
```
