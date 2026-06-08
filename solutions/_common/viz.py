"""ASCII 可视化工具:链表 / 二叉树 / 滑动窗口轨迹。

不依赖任何第三方库,直接 print。
"""
from __future__ import annotations
from typing import Optional
from .ds import ListNode, TreeNode, list_to_array


# ---------- 链表 ----------
def show_list(head: Optional[ListNode], title: str = "") -> None:
    if title:
        print(f"[{title}]")
    arr = list_to_array(head)
    if not arr:
        print("  ∅\n")
        return
    cells = [f" {v} " for v in arr]
    line1 = "┌" + "┬".join("─" * len(c) for c in cells) + "┐"
    line2 = "│" + "│".join(cells) + "│"
    line3 = "└" + "┴".join("─" * len(c) for c in cells) + "┘"
    arrows = "  " + "   ".join("→" for _ in arr[:-1])
    print(line1)
    print(line2)
    print(line3)
    if arrows.strip():
        print(arrows)
    print()


# ---------- 二叉树 ----------
def show_tree(root: Optional[TreeNode], title: str = "") -> None:
    """美化打印二叉树:每层居中。"""
    if title:
        print(f"[{title}]")
    if not root:
        print("  ∅\n")
        return

    def height(n: Optional[TreeNode]) -> int:
        return 0 if not n else 1 + max(height(n.left), height(n.right))

    h = height(root)
    width = (1 << h) * 4
    levels: list[list[Optional[TreeNode]]] = [[root]]
    for _ in range(h - 1):
        nxt = []
        for n in levels[-1]:
            nxt.append(n.left if n else None)
            nxt.append(n.right if n else None)
        levels.append(nxt)

    for d, lvl in enumerate(levels):
        slot = width // (len(lvl) + 1)
        line = ""
        for n in lvl:
            cell = str(n.val) if n else "·"
            line += " " * (slot - len(cell) // 2) + cell
        print(line)
    print()


# ---------- 滑动窗口轨迹 ----------
def show_window(arr: list, l: int, r: int, note: str = "") -> None:
    """打印 [l, r] 区间高亮:    [1  2  3  4  5]  -> 高亮 l..r."""
    cells = [f"{v:>2}" for v in arr]
    base = "  ".join(cells)
    cursor = []
    for i, c in enumerate(cells):
        if l <= i <= r:
            cursor.append("^^")
        else:
            cursor.append("  ")
    print(base)
    print("  ".join(cursor), note)


# ---------- 自测 demo ----------
def _demo() -> None:
    from .ds import build_list, build_tree
    print("== 链表 ==")
    show_list(build_list([1, 2, 3, 4, 5]), "原链表")
    print("== 二叉树 ==")
    show_tree(build_tree([3, 9, 20, None, None, 15, 7]), "示例")
    print("== 滑动窗口 ==")
    arr = [1, 3, -1, -3, 5, 3, 6, 7]
    for r in range(len(arr)):
        show_window(arr, max(0, r - 2), r, f"窗口大小=3, r={r}")


if __name__ == "__main__":
    _demo()
