# 回溯 模式表

## 通用模板

```python
def backtrack(state, choices):
    if 终止条件:
        ans.append(state.snapshot())
        return
    for choice in choices_at(state):
        if 剪枝:
            continue
        do(choice)
        backtrack(state, choices)
        undo(choice)        # ← 回溯
```

## 几种"形状"

| 形状 | 关键控制 | 例题 |
| --- | --- | --- |
| **排列**(全部位置) | used[] 防重 | 46, 47 |
| **组合**(单调起点) | start ≤ i,递归从 i 或 i+1 | 39, 77, 78 |
| **子集**(选/不选) | 二叉决策 / 增量构造 | 78, 90 |
| **切割** | 当前位置切一刀 | 131 |
| **棋盘** | 行扫描 + 列/对角线集合 | 51 |
| **路径**(DFS+visited) | 网格四向 + 涂色还原 | 79 |

## 39 vs 40 vs 77 速辨

| 题号 | 数组特点 | 同元素是否可重复用 | 是否需排序 + 去重相同分支 |
| --- | --- | --- | --- |
| 39 组合总和 | 无重复 | 是 | 否(数组无重复) |
| 40 组合总和 II | 有重复 | 否(每元素 ≤1 次) | **是**:`if i>start and a[i]==a[i-1]: continue` |
| 77 组合 | 1..n | 否 | 不需要 |

## N 皇后 列/对角线判断

设皇后位于 (r, c)。
- 同列:`c`
- 主对角线("\\"方向):**`r - c`** 相等
- 副对角线("/"方向):**`r + c`** 相等

```python
cols, diag1, diag2 = set(), set(), set()
def bt(r):
    if r == n:
        ...
    for c in range(n):
        if c in cols or (r-c) in diag1 or (r+c) in diag2:
            continue
        cols.add(c); diag1.add(r-c); diag2.add(r+c)
        bt(r+1)
        cols.remove(c); diag1.remove(r-c); diag2.remove(r+c)
```
