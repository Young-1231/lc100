# LC100 · 一句话速记（Python 面试口述版）

> 来源：python版本.md，已修复代码换行/缩进并逐题自测。由 `scripts/build_oneliner.py` 构建为 `data/oneliner.json`。
> 格式：`## 分类` → `### 题号. 标题` → 口述思路 / 超短一句话版 / 代码 / 3 个核心要点 / (可选)追问。

## 哈希表

### 1. 两数之和

**面试口述思路（哈希表版）** 遍历数组，用哈希表记录「数值→下标」； 对于每个数，检查「目标值 - 当前数」是否在哈希表中； 若在，直接返回两个下标；若不在，将当前数存入哈希表。

**超短一句话版** 哈希表存数值找差值，O(1) 查找，两数之和一边走一边查。

**代码**

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}  # 哈希表：数值 -> 下标
        for i, x in enumerate(nums):
            if target - x in seen:  # 查差值是否已见过
                return [seen[target - x], i]
            seen[x] = i  # 存入当前数
```

**3 个核心要点（面试官必问）**

* **查找方式**：哈希表实现 O(1) 查找，比暴力双循环 O(n²) 更优；

* **一边遍历一边存入**：避免用同一个元素两次（如 nums\[i] + nums\[i] 不合法）；

* **返回值是下标**：找到的是两个数对应的下标，而非数值本身。

**面试追问应对（加分）** 若问「为什么不用双指针」，答：双指针需排序后会改变下标关系，哈希表保留下标且只需一遍遍历。

***

### 3. 无重复字符的最长子串

**面试口述思路（滑动窗口）** 右指针扩展窗口，左指针收缩去重； 用哈希表记录字符出现情况； 右指针每移一位检查是否重复，若重复则左指针收缩直到无重复。

**超短一句话版** 滑动窗口扩右收左，哈希表记录字符最新位置，重复则收缩。

**代码**

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index = {}  # 哈希表：字符 -> 最新下标
        left = 0  # 左指针
        max_len = 0  # 最长长度
        for right, ch in enumerate(s):  # 右指针扩展
            if ch in char_index and char_index[ch] >= left:  # 字符在窗口内重复
                left = char_index[ch] + 1  # 收缩左指针
            char_index[ch] = right  # 更新字符最新位置
            max_len = max(max_len, right - left + 1)  # 更新最大长度
        return max_len
```

**3 个核心要点（面试官必问）**

* **收缩条件**：char\_index\[ch] >= left 说明字符在当前窗口内出现过，需要收缩左指针；

* **更新位置**：每轮都把 char\_index\[ch] 更新为最新下标，保证记录的是最近一次出现的位置；

* **最长长度**：每次迭代都更新 max\_len，确保记录的是全局最长的无重复子串长度。

***

### 347. 前 K 个高频元素

**面试口述思路（堆排序）** 先用 Counter 统计每个数的出现频率； 维护一个大小为 K 的最小堆； 遍历的过程中保持堆的大小为 K，最后堆里的元素就是频率最高的 K 个。

**超短一句话版** Counter 统计频率，最小堆保留 K 个最大，O(NlogK)。

**代码**

```python
import heapq
from collections import Counter

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)  # 统计频率
        heap = []  # 最小堆，存(count, num)
        for num, count in freq.items():
            heapq.heappush(heap, (count, num))  # 插入堆
            if len(heap) > k:  # 保持堆大小为k
                heapq.heappop(heap)  # 弹出最小的
        return [num for count, num in heap]  # 返回堆中的数
```

**3 个核心要点（面试官必问）**

* **堆排序规则**：用元组 (count, num) 入堆，Python 最小堆按 count 从小到大排序，count 最小的会被最先弹出；

* **维护大小为 K**：堆满后每次 push 新元素会自动 pop 掉 count 最小的，保证堆里始终是频率最大的 K 个；

* **最终结果**：遍历完成后，堆中剩余的 K 个元素就是出现频率最高的 K 个数，无需再排序。

***

### 146. LRU 缓存

**面试口述思路（哈希表+双向链表）** 哈希表提供 O(1) 查找； 双向链表维护访问顺序（头最新，尾最旧）； get 时将节点移到头，put 时新节点放头，超容量删尾节点。

**超短一句话版** 哈希表 O(1) 查找，双向链表维护顺序，头最新尾最旧。

**代码**

```python
class DLinkedNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # 哈希表：key -> 节点
        self.head = DLinkedNode()  # 虚拟头
        self.tail = DLinkedNode()  # 虚拟尾
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)  # 从原位置移除
            self._add_to_head(node)  # 移到头部
            return node.val
        return -1

    def put(self, key: int, val: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = val
            self._remove(node)
            self._add_to_head(node)
        else:
            node = DLinkedNode(key, val)
            self.cache[key] = node
            self._add_to_head(node)
            if len(self.cache) > self.capacity:
                removed = self.tail.prev  # 移除最久未使用的
                self._remove(removed)
                del self.cache[removed.key]
```

**3 个核心要点（面试官必问）**

* **双向链表顺序**：头部是最近访问的节点，尾部是最久未使用的节点，删除操作在 tail.prev 进行；

* **哈希表作用**：key → 节点，实现 O(1) 时间复杂度的查找、插入、删除；

* **容量超限处理**：删除 tail.prev（最久未使用的节点）后，同时从哈希表中移除对应的 key，保持一致性。

***

## 双指针

### 21. 合并两个有序链表

**面试口述思路（迭代版）** 新建 dummy 节点，用 cur 指针链接结果； 比较 l1 和 l2 的头节点，小的接入 cur 后移； 最后把剩余的链表接入。

**超短一句话版** 双指针比较，小的接入指针后移，迭代合并。

**代码**

```python
class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode()  # 哑节点
        cur = dummy
        while l1 and l2:  # 比较两链表头
            if l1.val <= l2.val:
                cur.next = l1
                l1 = l1.next
            else:
                cur.next = l2
                l2 = l2.next
            cur = cur.next
        cur.next = l1 or l2  # 接入剩余部分
        return dummy.next
```

**3 个核心要点（面试官必问）**

* **哑节点作用**：统一处理头节点为空的边界情况，cur = dummy 起步，return dummy.next 即为结果；

* **循环终止条件**：while l1 and l2 同时不为空时才比较，任一为空则直接接入剩余部分；

* **时间空间复杂度**：时间 O(n+m)（两链表长度之和），空间 O(1)（仅用指针，无额外数组）。

***

### 206. 反转链表

**面试口述思路（迭代版）** 用 prev、cur 双指针； 逐个反转指针方向：cur.next = prev； prev、cur 同时后移。

**超短一句话版** prev、cur 双指针，逐个反转指针方向。

**代码**

```python
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev = None
        cur = head
        while cur:
            next_node = cur.next  # 保存下一个
            cur.next = prev  # 反转指针
            prev = cur  # prev后移
            cur = next_node  # cur后移
        return prev  # prev是新头
```

**3 个核心要点（面试官必问）**

* **核心操作三步曲**：next\_node = cur.next → cur.next = prev → prev = cur → cur = next\_node；

* **最终 prev 指向新头**：循环结束时 prev 指向原链表的尾节点，即新链表的头节点；

* **空间时间复杂度**：空间 O(1)（仅用三个指针），时间 O(n)（遍历一次链表）。

***

### 141. 环形链表

**面试口述思路（Floyd 快慢指针）** 快指针每次走两步，慢指针每次走一步； 若链表有环，两指针必相遇； 相遇则有环，否则无环。

**超短一句话版** 快慢指针赛跑，有环必相遇，O(n)。

**代码**

```python
class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        fast = slow = head  # 初始化快慢指针
        while fast and fast.next:  # 快指针能走
            fast = fast.next.next  # 快走两步
            slow = slow.next  # 慢走一步
            if fast == slow:  # 相遇
                return True
        return False
```

**3 个核心要点（面试官必问）**

* **快慢指针速度差**：快指针每次走两步，慢指针每次走一步，相对速度为 1，有环必相遇；

* **无环情况处理**：快指针会先走到 None（链表尾部），while fast and fast.next 条件不满足时退出循环；

* **相遇即有环**：快慢指针相遇说明存在环，返回 True；正常走到终点则无环，返回 False。

***

### 19. 删除链表的倒数第 N 个结点

**面试口述思路（快慢指针）** 快慢指针初始都指向 dummy； 快指针先走 n+1 步，然后快慢一起走； 当快到末尾时，慢指针的下一个就是待删除节点。

**超短一句话版** 快指针先走 n+1 步，双指针齐走，快到末尾时慢指针指向待删节点。

**代码**

```python
class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        dummy = ListNode(next=head)  # 哑节点
        fast = slow = dummy
        for _ in range(n + 1):  # 快指针先走n+1步
            fast = fast.next
        while fast:  # 双指针齐走
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next  # 删除节点
        return dummy.next
```

**3 个核心要点（面试官必问）**

* **哑节点必要性**：统一处理「删除头节点」这种边界情况，无需单独判断，代码更简洁；

* **快指针先走 n+1 步**：使得 slow 最终指向待删除节点的前一个位置，便于执行删除操作；

* **时间空间复杂度**：时间 O(n)（遍历一次），空间 O(1)（仅用指针），最常用的标准双指针套路。

***

### 15. 三数之和

**面试口述思路（排序+双指针）** 排序数组，遍历第一个数，双指针找两数之和等于负的第一个数； 去重：跳过相同的第一个数、两数之和相同的组合； 结果存储三元组。

**超短一句话版** 排序后遍历 a，双指针找 b+c=-a，去重跳过相同值。

**代码**

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()  # 排序
        result = []
        n = len(nums)
        for i in range(n - 2):  # 遍历第一个数
            if nums[i] > 0:  # 优化：第一个数大于0则无解
                break
            if i > 0 and nums[i] == nums[i - 1]:  # 去重
                continue
            left = i + 1
            right = n - 1
            while left < right:  # 双指针找另外两个数
                s = nums[i] + nums[left] + nums[right]
                if s == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif s < 0:
                    left += 1
                else:
                    right -= 1
        return result
```

**3 个核心要点（面试官必问）**

* **排序的必要性**：排序后方便用双指针，且相同元素相邻，便于去重；

* **去重策略**：外层跳过重复的 nums\[i]，内层 while 跳过重复的 nums\[left] 和 nums\[right]；

* **三数之和为零**：若 nums\[i] > 0 则后面全是正数，不可能凑出零，直接 break 优化。

***

### 11. 盛最多水的容器

**面试口述思路（双指针收窄）** 左右指针向中间收敛； 每次移动短板（因为水高由短板决定，移动长板不可能增加面积）； 记录最大面积。

**超短一句话版** 双指针收窄，移动短板更新最大面积，O(n)。

**代码**

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        max_area = 0
        while left < right:
            area = min(height[left], height[right]) * (right - left)  # 计算面积
            max_area = max(max_area, area)  # 更新最大
            if height[left] < height[right]:  # 移动短板
                left += 1
            else:
                right -= 1
        return max_area
```

**3 个核心要点（面试官必问）**

* **短板决定高度**：水的容量由较短的那根柱子决定，移动长板不可能增加水量（高度不会变高）；

* **为何移动短板**：移动短板后，新的较短板可能变高，从而增大水量，需要尝试；

* **双指针收敛**：左右指针向中间收敛，每次移动一端，直到相遇为止，保证找到全局最大。

***

## 滑动窗口

### 76. 最小覆盖子串

**面试口述思路（滑动窗口）** 右指针扩展窗口，左指针收缩去优化； 用哈希表记录窗口内字符数量和需要的字符数量； 当窗口包含所有目标字符时收缩左指针。

**超短一句话版** 滑动窗口扩右收左，哈希表比较窗口与目标字符数，包含则收左。

**代码**

```python
from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need = Counter(t)  # 需要的字符计数
        window = Counter()  # 窗口内字符计数
        left = 0
        valid = 0  # 已满足的字符种类数
        min_len = float('inf')
        min_start = 0
        for right, c in enumerate(s):  # 扩右指针
            if c in need:
                window[c] += 1
                if window[c] == need[c]:  # 该字符满足
                    valid += 1
            while valid == len(need):  # 包含所有字符，收左指针
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_start = left
                c_left = s[left]
                if c_left in need:
                    if window[c_left] == need[c_left]:
                        valid -= 1
                    window[c_left] -= 1
                left += 1
        return s[min_start:min_start + min_len] if min_len != float('inf') else ''
```

**3 个核心要点（面试官必问）**

* **双计数器设计**：need 记录目标字符的需求量，window 记录窗口内的数量，valid 记录已满足需求的字符种类数；

* **收缩窗口的时机**：当 valid == len(need)（所有字符都已满足）时，尝试收缩左边界寻找更优解；

* **收缩时的细节**：如果 window\[c\_left] == need\[c\_left]，收缩后该字符就不满足了，需要 valid--。

***

### 209. 长度最小的子数组

**面试口述思路（滑动窗口）** 右指针扩展窗口，累加和； 当窗口和 >= target 时收缩左指针更新最短长度； 直到窗口和 < target 继续扩展右指针。

**超短一句话版** 滑动窗口扩右收左，和大于目标时收缩更新最短长度。

**代码**

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        cur_sum = 0  # 当前窗口和
        min_len = float('inf')
        for right in range(len(nums)):  # 扩右指针
            cur_sum += nums[right]
            while cur_sum >= target:  # 收左指针
                min_len = min(min_len, right - left + 1)
                cur_sum -= nums[left]
                left += 1
        return min_len if min_len != float('inf') else 0
```

**3 个核心要点（面试官必问）**

* **扩右收左循环**：外层 for 扩右指针累加和，内层 while 收左指针直到和小于 target；

* **何时收缩**：cur\_sum >= target 时才收缩左边界，此时窗口已满足条件，记录长度后尝试缩小；

* **复杂度分析**：每个元素最多进入和离开窗口各一次，时间 O(n)，空间 O(1)，优于暴力枚举所有子数组。

***

## 单调栈

### 739. 每日温度

**面试口述思路（单调栈）** 栈存温度索引，遍历温度数组； 当前温度比栈顶高时，弹出栈顶计算距离； 栈顶索引对应的等待天数 = 当前索引 - 栈顶索引。

**超短一句话版** 单调递减栈，栈顶是等待升温的天数，当前更高则弹出计算。

**代码**

```python
class Solution:
    def dailyTemperatures(self, T: List[int]) -> List[int]:
        n = len(T)
        result = [0] * n
        stack = []  # 存索引，单调递减
        for i, temp in enumerate(T):
            while stack and T[stack[-1]] < temp:  # 比栈顶高则弹出
                prev = stack.pop()
                result[prev] = i - prev  # 计算距离
            stack.append(i)
        return result
```

**3 个核心要点（面试官必问）**

* **单调递减栈**：栈内元素对应的温度严格递减，栈顶是当前还没找到更高温度的「待升温」日子；

* **弹出时机**：当前温度 T\[i] 比栈顶对应温度高时，说明栈顶那天等到了升温，弹出并计算等待天数；

* **存索引而非温度**：栈中存放下标 i，弹出 prev 后用 i - prev 即可得到天数差值。

***

### 84. 柱状图中最大的矩形

**面试口述思路（单调栈）** 数组两侧补 0，方便处理边界； 单调递增栈，存索引； 遇到更小的柱就弹出，计算以弹出柱为高度的矩形最大面积。

**超短一句话版** 单调递增栈，两侧补0，弹出时计算面积，宽度 = 右边界 - 左边界 - 1。

**代码**

```python
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        heights = [0] + heights + [0]  # 两侧补0
        stack = [0]  # 栈，存索引
        max_area = 0
        for i in range(1, len(heights)):
            while heights[i] < heights[stack[-1]]:  # 遇到更小的柱
                h = heights[stack.pop()]  # 弹出高度
                w = i - stack[-1] - 1  # 宽度
                max_area = max(max_area, h * w)
            stack.append(i)
        return max_area
```

**3 个核心要点（面试官必问）**

* **两侧补 0 的作用**：在最左边和最右边各加一个高度为 0 的柱，确保所有柱最终都能弹出，避免边界处理；

* **宽度计算公式**：弹出时宽度 = 当前索引 i - 新栈顶索引 stack\[-1] - 1，即「右边界 - 左边界 - 1」；

* **单调递增栈**：栈内高度严格递增，遇到更小的柱时触发弹出，计算以弹出柱为高度的矩形最大面积。

***

### 42. 接雨水

**面试口述思路（单调栈）** 单调递减栈； 遇到比栈顶高的柱就形成低洼，计算雨水量； 水量 = 宽度 × (min(左柱, 右柱) - 低洼高度)。

**超短一句话版** 单调递减栈，形成低洼时累加雨水量。

**代码**

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        stack = []  # 单调递减栈，存索引
        water = 0
        for i, h in enumerate(height):
            while stack and h > height[stack[-1]]:  # 比栈顶高形成低洼
                bottom = stack.pop()
                if not stack:  # 没有左边界
                    break
                w = i - stack[-1] - 1  # 宽度
                cur_h = min(h, height[stack[-1]]) - height[bottom]  # 高度
                water += w * cur_h
            stack.append(i)
        return water
```

**3 个核心要点（面试官必问）**

* **形成低洼的条件**：当前高度 h > height\[stack\[-1]] 时，形成低洼（凹槽），可以接雨水；

* **左右边界确定**：弹出低洼 bottom 后，新的栈顶 stack\[-1] 就是左边界，当前索引 i 是右边界；

* **能接水的高度**：cur\_h = min(左边界高度, 右边界高度) - 低洼高度，bottom 不高于两侧，cur\_h ≥ 0；遇到等高柱时为 0，不影响结果。

***

## 二叉树和递归

### 94. 二叉树的中序遍历

**面试口述思路（栈模拟）** 模拟递归：左子树一直入栈； 弹出节点访问，然后右子树入栈； 直到栈空且节点为空。

**超短一句话版** 栈模拟递归：一路向左入栈，弹出访问再转向右子树，O(n)。

**代码**

```python
class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        result = []
        stack = []
        cur = root
        while cur or stack:
            while cur:  # 左子树全部入栈
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()  # 弹出访问
            result.append(cur.val)
            cur = cur.right  # 处理右子树
        return result
```

**3 个核心要点（面试官必问）**

* **外层循环条件**：while cur or stack，保证左子树全部入栈后，栈空且节点空时才退出；

* **内层 while 的作用**：把当前节点的所有左子节点全部入栈，实现「左子树优先」的遍历顺序；

* **弹出后的处理**：弹出节点访问其值后，立即转向处理右子树，切换到右子树继续同样的流程。

***

### 104. 二叉树的最大深度

**面试口述思路（递归）** 递归返回左右子树最大深度 +1； 空节点返回 0。

**超短一句话版** 递归返回左右最大深度+1，O(n)。

**代码**

```python
class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:  # 递归终止
            return 0
        return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1
```

**3 个核心要点（面试官必问）**

* **递归终止条件**：空节点返回深度 0，这是递归的「锚点」，所有递归最终都会走到这里；

* **每个节点深度公式**：max(左子树深度, 右子树深度) + 1，+1 是因为要算上当前节点本身这一层；

* **后序遍历顺序**：先递归处理左右子树（子问题），再返回当前节点的深度，符合自底向上的计算逻辑。

***

### 101. 对称二叉树

**面试口述思路（递归）** 递归比较左子树和右子树是否互为镜像； 两节点都空返回 True，一方空返回 False； 值相等且内外都镜像才对称。

**超短一句话版** 递归比较左右子树是否互为镜像，O(n)。

**代码**

```python
class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        def check(p, q):
            if not p and not q:  # 两节点都空
                return True
            if not p or not q:  # 一方空
                return False
            return p.val == q.val and check(p.left, q.right) and check(p.right, q.left)
        return check(root.left, root.right) if root else True
```

**3 个核心要点（面试官必问）**

* **递归比较顺序**：每次递归比较 (p.left, q.right) 和 (p.right, q.left)，即「外对外、内对内」的镜像比较；

* **递归终止情况**：两个节点都为空返回 True（对称），只有一个为空返回 False（不对称）；

* **对称条件**：节点值相等 AND 左子树和右子树都对称，三者缺一不可。

***

### 236. 二叉树的最近公共祖先

**面试口述思路（后序递归）** 用后序遍历递归找 p/q； 若当前节点是 p/q 或空，直接返回； 递归左右子树，若左右都有结果，当前是祖先； 若只有一边有结果，返回那一边。

**超短一句话版** 后序递归找 p/q，左右都找到则当前是祖先，只找到一边返回那一边。

**代码**

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root or root == p or root == q:  # 终止条件
            return root
        left = self.lowestCommonAncestor(root.left, p, q)  # 递归左
        right = self.lowestCommonAncestor(root.right, p, q)  # 递归右
        if not left:  # 左子树没找到
            return right
        if not right:  # 右子树没找到
            return left
        return root  # 左右都找到，当前是祖先
```

**3 个核心要点（面试官必问）**

* **终止条件设计**：找到 p 或 q 或空节点就立即返回，是递归的「锚点」，避免无效搜索；

* **后序遍历的必要性**：先递归找子树结果，再判断当前节点，符合「自底向上」找祖先的逻辑；

* **核心判断逻辑**：左右都有结果 → 当前是最近公共祖先；只有一边有 → 祖先在这一侧，返回那一边的结果。

***

### 235. 二叉搜索树的最近公共祖先

**面试口述思路（BST特性）** 利用 BST 特性：p/q 都在左子树则向左，都在右子树则向右； 否则当前节点即为最近公共祖先。

**超短一句话版** BST 特性：pq 同侧就往那侧走，分叉处即为祖先，O(H)。

**代码**

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        while root:
            if p.val < root.val and q.val < root.val:  # 都在左
                root = root.left
            elif p.val > root.val and q.val > root.val:  # 都在右
                root = root.right
            else:  # 分叉点
                return root
        return root
```

**3 个核心要点（面试官必问）**

* **利用 BST 有序性**：左子树所有节点值 < 根节点值 < 右子树所有节点值，可根据 p、q 与当前节点值的大小关系判断方向；

* **同侧递归**：p 和 q 都小于当前节点则走向左子树，都大于则走向右子树；

* **分叉点即祖先**：一旦 p、q 分布在当前节点两侧，当前节点就是最近公共祖先，无需继续向下。

***

### 124. 二叉树的最大路径和

**面试口述思路（后序递归）** 后序递归计算每个节点贡献的最大路径； 节点的最大贡献 = max(0, 左贡献, 右贡献) + 节点值； 最大路径 = max(全局最大, 左贡献 + 右贡献 + 节点值)。

**超短一句话版** 后序递归，贡献为 max(0,左,右)+节点值，路径和为左右贡献+节点值。

**代码**

```python
class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        self.max_sum = float('-inf')

        def dfs(node):
            if not node:
                return 0
            left = max(0, dfs(node.left))  # 左贡献，负则取0
            right = max(0, dfs(node.right))  # 右贡献，负则取0
            self.max_sum = max(self.max_sum, left + right + node.val)  # 更新全局最大
            return max(left, right) + node.val  # 返回该节点能提供的最大贡献

        dfs(root)
        return self.max_sum
```

**3 个核心要点（面试官必问）**

* **负贡献的取舍**：max(0, left) 和 max(0, right) 确保只取正贡献，负值路径不贡献甚至拖累，直接当 0 处理；

* **全局最大更新时机**：在「左右贡献 + 当前节点值」处更新，因为这是以当前节点为根的完整路径；

* **返回值含义**：返回的是该节点能向上提供的最大贡献 = max(左贡献, 右贡献) + 节点值，用于父节点计算。

***

### 98. 验证二叉搜索树

**面试口述思路（递归传界）** 递归传递上下界，判断节点值是否在界内； 左子树用 (lower, node.val)，右子树用 (node.val, upper)。

**超短一句话版** 递归传上下界判断，O(n)。

**代码**

```python
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        def dfs(node, lower, upper):
            if not node:
                return True
            if node.val <= lower or node.val >= upper:  # 不在界内
                return False
            return dfs(node.left, lower, node.val) and dfs(node.right, node.val, upper)
        return dfs(root, float('-inf'), float('inf'))
```

**3 个核心要点（面试官必问）**

* **上下界传递**：递归时传递 (lower, upper) 边界，当前节点值必须在界内才合法，否则不是 BST；

* **初始边界设定**：根节点的界是 (-∞, +∞)，用 float('-inf') 和 float('inf') 表示；

* **BST 的充要条件**：左子树所有节点值 < 当前节点值 < 右子树所有节点值，递归验证左右子树也必须满足。

***

### 230. 二叉搜索树中第K小的元素

**面试口述思路（中序遍历）** BST 中序遍历为升序； 中序遍历到第 k 个节点即为第 k 小； 可提前终止遍历。

**超短一句话版** BST 中序遍历升序，第 k 个即为第 k 小，O(H+k)。

**代码**

```python
class Solution:
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        stack = []
        cur = root
        count = 0
        while cur or stack:
            while cur:  # 左子树入栈
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()  # 弹出访问
            count += 1
            if count == k:  # 第k个
                return cur.val
            cur = cur.right  # 处理右子树
        return -1
```

**3 个核心要点（面试官必问）**

* **中序遍历顺序**：BST 中序遍历（左 → 根 → 右）恰好是节点值升序排列；

* **计数提前终止**：count 记录已访问节点数，当 count == k 时说明已到第 k 小，直接返回，无需遍历完整棵树；

* **栈的作用**：用栈模拟递归，左子树全部入栈后弹出访问，再转向右子树，节省递归栈空间。

***

### 450. 删除二叉搜索树中的节点

**面试口述思路（递归）** 找到目标节点，按三种情况处理：

* 叶节点：直接删除；

* 只有左/右子树：用子树替换；

* 有两子树：用后继节点（右子树最左）替换。

**超短一句话版** 找到节点分三类处理：叶节点直删，有子树用子树替，有两子树用后继替。

**代码**

```python
class Solution:
    def deleteNode(self, root: TreeNode, key: int) -> TreeNode:
        if not root:
            return None
        if key < root.val:  # 在左子树
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:  # 在右子树
            root.right = self.deleteNode(root.right, key)
        else:  # 找到目标
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            successor = root.right
            while successor.left:  # 找后继
                successor = successor.left
            root.val = successor.val  # 替换值
            root.right = self.deleteNode(root.right, successor.val)  # 删除后继
        return root
```

**3 个核心要点（面试官必问）**

* **后继节点的定义**：右子树中最左（最小）的节点，用于替换被删除节点，保持 BST 的有序性；

* **三种删除情况**：叶节点直接删除返回空，有单子树返回该子树，有两子树用后继替换值后递归删除后继节点；

* **递归删除后继**：替换值后，调用 deleteNode 递归删除后继节点，保证 BST 结构完整。

***

## 回溯和DFS

### 46. 全排列

**面试口述思路（回溯）** 递归枚举每个位置可以放的数； 用 used 数组标记已用过的数； 选一个数进入下一层，撤销选择。

**超短一句话版** 回溯枚举每个位置可放的数，used 数组去重。

**代码**

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []
        used = [False] * len(nums)  # 标记已使用的数

        def backtrack():
            if len(path) == len(nums):  # 满了
                result.append(path[:])
                return
            for i in range(len(nums)):
                if used[i]:  # 已用过则跳过
                    continue
                used[i] = True  # 选
                path.append(nums[i])
                backtrack()
                path.pop()  # 撤销
                used[i] = False

        backtrack()
        return result
```

**3 个核心要点（面试官必问）**

* **used 数组作用**：标记每个位置的数字是否已被使用，确保每个数字在同一路径中只使用一次；

* **递归终止条件**：path 长度等于 nums 长度时，说明已选满一个排列，加入结果；

* **撤销选择的重要性**：回溯的核心，递归前后 used 和 path 的状态必须一致，保证不同分支不受影响。

***

### 39. 组合总和

**面试口述思路（回溯）** 排序数组，DFS 回溯； 每个元素可重复选，target 减当前值； target 为 0 则加入结果，target < 0 则剪枝。

**超短一句话版** 排序后回溯，每个数可重复选，target 减到 0 则加入。

**代码**

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()  # 排序
        result = []

        def backtrack(start, target, path):
            if target == 0:  # 找到解
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > target:  # 剪枝
                    break
                path.append(candidates[i])
                backtrack(i, target - candidates[i], path)  # i不是i+1，可重复选
                path.pop()

        backtrack(0, target, [])
        return result
```

**3 个核心要点（面试官必问）**

* **排序后剪枝**：数组升序排列后，当 candidates\[i] > target 时直接 break，因为后面更大的数也不可能凑出目标；

* **可重复选的实现**：递归时传 i 而非 i+1，允许同一元素在同一路径中重复使用；

* **target 状态更新**：每选一个数就从 target 中减去该值，递归终止条件 target == 0 时找到一个合法组合。

***

### 78. 子集

**面试口述思路（回溯）** 每个元素都有选和不选两种情况； 回溯收集所有路径； 从 start 往后枚举下一个选谁，递归树上每个节点都是一个子集。

**超短一句话版** 回溯每个元素选或不选，收集所有路径。

**代码**

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []

        def backtrack(start):
            result.append(path[:])  # 每个节点都加入结果
            for i in range(start, len(nums)):
                path.append(nums[i])  # 选
                backtrack(i + 1)  # 不回头
                path.pop()  # 撤销

        backtrack(0)
        return result
```

**3 个核心要点（面试官必问）**

* **每层节点都加入结果**：与全排列不同，子集问题在递归的每一步都要把当前 path 加入结果（包括空集）；

* **不回头原则**：递归传 i+1，确保只向后选择，避免重复使用前面的数；

* **收集全部路径**：通过「选」和「不选」两条分支遍历所有情况，最终 result 包含 2^n 个子集。

***

### 22. 括号生成

**面试口述思路（回溯）** 递归构建括号序列； 左括号数 < n 可加，右括号数 < 左括号数可加； 左右都用完时加入结果。

**超短一句话版** 回溯递归构建，左括号数小于 n 可加，右括号数小于左括号可加。

**代码**

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []

        def backtrack(left, right, path):
            if len(path) == 2 * n:  # 满了
                result.append(path)
                return
            if left < n:  # 可加左括号
                backtrack(left + 1, right, path + '(')
            if right < left:  # 可加右括号
                backtrack(left, right + 1, path + ')')

        backtrack(0, 0, '')
        return result
```

**3 个核心要点（面试官必问）**

* **右括号限制**：right < left 确保右括号数量永不超出左括号，保证生成的括号序列合法；

* **递归树结构**：深度为 2n（n 个左括号 + n 个右括号），每层有两种选择分支；

* **有效括号性质**：合法括号序列的充要条件是「任意前缀中右括号数 ≤ 左括号数，且左右各 n 个」，这是剪枝的核心依据。

***

### 200. 岛屿数量

**面试口述思路（DFS 沉没）** 遍历网格，遇 '1' 则 DFS 沉没整个岛屿（标记为 '0'）； 每沉没一次岛屿数 +1。

**超短一句话版** DFS 沉没岛屿，每找到一片岛屿 +1，O(m\*n)。

**代码**

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        count = 0
        m, n = len(grid), len(grid[0])

        def dfs(i, j):
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == '0':  # 边界或水
                return
            grid[i][j] = '0'  # 沉没
            dfs(i + 1, j)
            dfs(i - 1, j)
            dfs(i, j + 1)
            dfs(i, j - 1)

        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':  # 发现岛屿
                    count += 1
                    dfs(i, j)  # 沉没
        return count
```

**3 个核心要点（面试官必问）**

* **沉没操作的目的**：将发现的岛屿全部标记为 '0'，避免后续遍历重复计算同一岛屿；

* **四方向DFS**：从每个 '1' 出发向四个方向递归沉没，确保整个岛屿被标记；

* **岛屿计数时机**：在主循环中发现 '1' 时 count++，然后立即调用 dfs 沉没该岛屿的所有格子。

***

### 113. 路径总和 II

**面试口述思路（DFS）** DFS 记录路径，累加路径和； 到达叶子节点且和等于 target 则加入结果； 回溯撤销选择。

**超短一句话版** DFS 记录路径，叶子节点且和等于目标则加入结果。

**代码**

```python
class Solution:
    def pathSum(self, root: TreeNode, targetSum: int) -> List[List[int]]:
        result = []

        def dfs(node, path, cur_sum):
            if not node:
                return
            cur_sum += node.val
            path.append(node.val)
            if not node.left and not node.right and cur_sum == targetSum:  # 叶子且和匹配
                result.append(path[:])
            dfs(node.left, path, cur_sum)
            dfs(node.right, path, cur_sum)
            path.pop()  # 撤销

        dfs(root, [], 0)
        return result
```

**3 个核心要点（面试官必问）**

* **path\[:] 复制切片**：将当前 path 复制一份加入结果，否则后续 pop 会修改已加入的结果；

* **必须到叶子节点**：只有左右子树都不存在的节点才可能是完整路径的终点，保证路径从根到叶；

* **回溯撤销选择**：递归返回后执行 path.pop()，恢复递归前的状态，保证同一节点可被多条路径使用。

***

## 动态规划

### 70. 爬楼梯

**面试口述思路（DP）** dp\[i] = 到达第 i 阶的方法数； dp\[i] = dp\[i-1] + dp\[i-2]（斐波那契）； 初始 dp\[1]=1, dp\[2]=2。

**超短一句话版** dp\[i]=dp\[i-1]+dp\[i-2]，斐波那契。

**代码**

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]
```

**3 个核心要点（面试官必问）**

* **递推公式来源**：到达第 i 阶可以从 i-1 阶走一步或从 i-2 阶走两步，所以 dp\[i] = dp\[i-1] + dp\[i-2]；

* **空间优化**：只与前两项有关，可将数组压缩为两个变量，将空间从 O(n) 降到 O(1)；

* **时间复杂度**：遍历一次即可，时间 O(n)，优于递归加记忆化的方式。

***

### 300. 最长递增子序列

**面试口述思路（二分+贪心）** dp\[k] 存长度为 k+1 的递增子序列的最小末尾； 二分查找插入位置，dp\[pos] = num； 最终最长长度就是 dp 数组长度。

**超短一句话版** 贪心+二分，dp 存最小末尾值，O(nlogn)。

**代码**

```python
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = []  # dp[i]是长度为i+1的递增子序列的最小末尾
        for num in nums:
            pos = bisect.bisect_left(dp, num)  # 二分查找位置
            if pos == len(dp):
                dp.append(num)
            else:
                dp[pos] = num
        return len(dp)
```

**3 个核心要点（面试官必问）**

* **dp 的含义**：dp\[i] 表示长度为 i+1 的递增子序列的最小末尾值，用于二分查找时的比较；

* **二分查找位置**：用 bisect\_left 找第一个 >= num 的位置，若在末尾则扩展 dp，否则更新该位置的值为更小的 num；

* **最终结果**：dp 的长度即为最长递增子序列的长度，无需额外计算。

***

### 322. 零钱兑换

**面试口述思路（完全背包 DP）** dp\[i] = 凑成金额 i 所需的最少硬币数； 完全背包：每个硬币可以选多次； dp\[i] = min(dp\[i], dp\[i-coin] + 1)。

**超短一句话版** 完全背包，dp\[i] 为凑成 i 所需最少硬币数。

**代码**

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)  # dp[i]凑成i所需最少硬币
        dp[0] = 0  # 基础
        for coin in coins:
            for i in range(coin, amount + 1):  # 正序，完全背包
                dp[i] = min(dp[i], dp[i - coin] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1
```

**3 个核心要点（面试官必问）**

* **dp\[0] = 0 的意义**：金额为 0 时不需要任何硬币，这是动态规划的base case；

* **完全背包内层正序**：因为硬币可以重复使用，内层循环从 coin 到 amount 正序遍历，确保每种硬币可用多次；

* **dp\[amount] 为 inf 的处理**：若最终值仍为 inf，说明无法凑出该金额，返回 -1。

***

### 1143. 最长公共子序列

**面试口述思路（DP）** dp\[i]\[j] = text1 前 i 个和 text2 前 j 个的最长公共子序列； 若相等则 +1，否则取 max(上, 左)。

**超短一句话版** dp\[i]\[j] 为前 i 和前 j 的最长公共子序列，相等则 +1，否则取 max。

**代码**

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:  # 相等
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:  # 不等
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]
```

**3 个核心要点（面试官必问）**

* **dp 数组多一行一列**：方便处理边界条件，dp\[i]\[j] 对应 text1\[0:i] 和 text2\[0:j] 的 LCS 长度；

* **字符相等时**：从 dp\[i-1]\[j-1] + 1，表示两个字符匹配，LCS 长度加一；

* **字符不等时**：从 dp\[i-1]\[j] 和 dp\[i]\[j-1] 中取较大值，因为最后一位不匹配时结果继承二者之一。

***

### 72. 编辑距离

**面试口述思路（DP）** dp\[i]\[j] = word1 前 i 个变成 word2 前 j 个的最少操作数； 删除/插入/替换三种操作取最小； 若字符相等则直接继承 dp\[i-1]\[j-1]。

**超短一句话版** dp\[i]\[j] 前 i 变 j 最少操作，删插替取最小，O(m\*n)。

**代码**

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i  # 删除i个字符
        for j in range(n + 1):
            dp[0][j] = j  # 插入j个字符
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]  # 相等不操作
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1  # 删插替
        return dp[m][n]
```

**3 个核心要点（面试官必问）**

* **边界条件设定**：dp\[i]\[0] = i 表示将前 i 个字符全部删去，dp\[0]\[j] = j 表示全部插入；

* **三种操作取最小**：删除（从上方来）、插入（从左方来）、替换（从左上方来），取三者最小代价再加 1；

* **字符相等时不操作**：word1\[i-1] == word2\[j-1] 时直接继承 dp\[i-1]\[j-1]，无需额外操作。

***

### 198. 打家劫舍

**面试口述思路（DP）** dp\[i] = 到第 i 间房能偷的最大金额； dp\[i] = max(dp\[i-1], dp\[i-2] + nums\[i])； 只与前两间房有关，可以压缩空间。

**超短一句话版** dp\[i]=max(dp\[i-1], dp\[i-2]+nums\[i])，维护前两个状态。

**代码**

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        prev = nums[0]  # dp[i-2]
        curr = max(nums[0], nums[1])  # dp[i-1]
        for i in range(2, len(nums)):
            prev, curr = curr, max(curr, prev + nums[i])  # 选或不选第i间
        return curr
```

**3 个核心要点（面试官必问）**

* **状态压缩**：只与前两间房有关，用 prev（dp\[i-2]）和 curr（dp\[i-1]）两个变量滚动更新，空间 O(1)；

* **状态转移公式**：dp\[i] = max(不偷第 i 间, 偷第 i 间) = max(dp\[i-1], dp\[i-2] + nums\[i])；

* **初始化**：prev = nums\[0]（只有第一间），curr = max(nums\[0], nums\[1])（前两间取较大）。

***

### 121. 买卖股票的最佳时机

**面试口述思路（贪心）** 维护最低价格和最大利润； 遍历时更新最低价格，计算当前利润取最大。

**超短一句话版** 贪心维护最低价和最大利润，O(n)。

**代码**

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float('inf')  # 最低价
        max_profit = 0  # 最大利润
        for price in prices:
            min_price = min(min_price, price)  # 更新最低价
            max_profit = max(max_profit, price - min_price)  # 更新利润
        return max_profit
```

**3 个核心要点（面试官必问）**

* **一遍遍历的优势**：只需维护一个最低价格变量，遍历一次即可找到最大利润，时间 O(n)；

* **最低价的含义**：min\_price 记录遍历到当前为止的最低价格，保证在最低价买入；

* **利润计算**：price - min\_price 是以当前价格卖出能获得的最大利润，实时更新全局最大 profit。

***

### 122. 买卖股票的最佳时机 II

**面试口述思路（贪心）** 累加所有上升段的利润； 只要第二天比第一天高就前一天买第二天卖。

**超短一句话版** 累加所有上升段利润，贪心。

**代码**

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:  # 上升段
                profit += prices[i] - prices[i - 1]
        return profit
```

**3 个核心要点（面试官必问）**

* **贪心核心思想**：累加所有上升段利润，等价于把每个正差值都收入囊中；

* **为何上升段就累加**：prices\[i] > prices\[i-1] 时前一天买、今天卖，利润必然为正；

* **无限次交易**：不限制买卖次数，所以每个上升段都可以独立分割计算，无需考虑跨段持有。

***

### 53. 最大子数组和

**面试口述思路（贪心/DP）** cur\_sum 记录以当前元素结尾的最大子序和； 若 cur\_sum < 0，则重新从当前元素开始； res 记录出现过的最大 cur\_sum。

**超短一句话版** 贪心，cur\_sum 为以 i 结尾的最大子序和，负则重新开始。

**代码**

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = nums[0]  # 全局最大
        cur_sum = nums[0]  # 以i结尾的最大子序和
        for i in range(1, len(nums)):
            cur_sum = max(nums[i], cur_sum + nums[i])  # 负则重新开始
            max_sum = max(max_sum, cur_sum)  # 更新全局最大
        return max_sum
```

**3 个核心要点（面试官必问）**

* **负和重新开始**：若 cur\_sum < 0，说明之前累加的和对后续是负贡献，直接从当前元素重新开始；

* **全局最大记录**：max\_sum 记录遍历过程中出现过的最大 cur\_sum，即为最大子序和；

* **cur\_sum 更新规则**：max(nums\[i], cur\_sum + nums\[i])，比较「从当前重新开始」和「继续累加」两种选择。

***

### 152. 乘积最大子数组

**面试口述思路（DP）** 同时维护最大和最小乘积（因为负数会使最大变最小）； 若当前数为负，交换 max\_prod 和 min\_prod； 更新 max\_prod = max(当前数, max\_prod \* 当前数)。

**超短一句话版** 维护最大和最小乘积（负数会使最大变最小）。

**代码**

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        max_prod = min_prod = nums[0]  # 同时记录最大和最小
        result = nums[0]
        for i in range(1, len(nums)):
            if nums[i] < 0:  # 负数交换最大最小
                max_prod, min_prod = min_prod, max_prod
            max_prod = max(nums[i], max_prod * nums[i])
            min_prod = min(nums[i], min_prod * nums[i])
            result = max(result, max_prod)
        return result
```

**3 个核心要点（面试官必问）**

* **为何同时记录最大最小**：负数乘负数会变成正数，最大值遇到负数会变成最小值，最小值遇到负数会变成最大值；

* **交换时机**：当前数为负时，交换 max\_prod 和 min\_prod，确保 max\_prod 始终是「以当前结尾的最大乘积」；

* **result 更新**：每轮都更新 result = max(result, max\_prod)，确保记录的是全局最大乘积。

***

### 312. 戳气球

**面试口述思路（区间 DP）** dp\[i]\[j] = 开区间 (i,j) 内能戳破的最大金币； 枚举最后一个戳破的气球 k，转移取最大； dp\[i]\[j] = max(dp\[i]\[k] + dp\[k]\[j] + nums\[i]\*nums\[k]\*nums\[j])。

**超短一句话版** 区间 DP 开区间 (i,j) 最大金币，枚举最后戳破 k，O(n³)。

**代码**

```python
class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        nums = [1] + nums + [1]  # 两端补1
        n = len(nums)
        dp = [[0] * n for _ in range(n)]
        for length in range(2, n):  # 枚举长度
            for i in range(n - length):
                j = i + length
                for k in range(i + 1, j):  # 枚举分割点
                    dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])
        return dp[0][n - 1]
```

**3 个核心要点（面试官必问）**

* **两端补 1 的作用**：在原数组两端各加一个虚拟气球，简化边界处理，使每戳一个气球都能获得 nums\[i]\*nums\[k]\*nums\[j] 的金币；

* **开区间的含义**：dp\[i]\[j] 表示开区间 (i, j) 内能戳破的最大金币数，i 和 j 本身不被戳破；

* **枚举最后一个戳破的气球**：遍历所有可能的 k，计算 dp\[i]\[k] + dp\[k]\[j] + nums\[i]\*nums\[k]\*nums\[j] 取最大值。

***

### 354. 俄罗斯套娃信封

**面试口述思路（排序+LIS）** 按宽升序，高降序排列； 问题转化为对高求最长递增子序列（因为同宽时高递减，不会被选中）。

**超短一句话版** 宽升序高降序排，转化为高维度 LIS，O(nlogn)。

**代码**

```python
import bisect

class Solution:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        envelopes.sort(key=lambda x: (x[0], -x[1]))  # 宽升序，高降序
        dp = []  # 存递增序列的最小末尾
        for _, h in envelopes:
            pos = bisect.bisect_left(dp, h)  # 对高求LIS
            if pos == len(dp):
                dp.append(h)
            else:
                dp[pos] = h
        return len(dp)
```

**3 个核心要点（面试官必问）**

* **排序策略**：宽升序、高降序，确保同宽的信封只选一个（高降序使后面的高不可能接在前面高的后面）；

* **转化为 LIS**：排序后问题转化为对高求最长递增子序列，同宽不互选保证了贪心正确性；

* **二分 O(nlogn)**：对高用二分查找插入位置求 LIS，总时间复杂度 O(nlogn)，优于 O(n²) 的 DP。

***

## 二分查找

### 33. 搜索旋转排序数组

**面试口述思路（二分）** 在旋转数组中二分，判断哪半边有序； 根据 target 落在有序半边还是无序半边收缩边界。

**超短一句话版** 二分判断哪半边有序，target 在有序半边则收缩边界，O(logn)。

**代码**

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            if nums[left] <= nums[mid]:  # 左半边有序
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:  # 右半边有序
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1
```

**3 个核心要点（面试官必问）**

* **如何判断有序半边**：通过 nums\[left] <= nums\[mid] 判断左半边是否升序有序；

* **收缩边界的依据**：若 target 落在有序半边（nums\[left] <= target < nums\[mid]），则在该半边继续二分；

* **注意 <= 的等号**：nums\[left] <= nums\[mid] 必须带等号，left == mid 时左半边只有一个元素，也算有序。

***

### 34. 在排序数组中查找元素的第一个和最后一个位置

**面试口述思路（二分变形）** 二分找左边界：target <= nums\[mid] 时收缩右边界； 二分找右边界：target >= nums\[mid] 时收缩左边界。

**超短一句话版** 二分变形找左右边界，左边界 target<=mid 收缩右，右边界 >=mid 收左。

**代码**

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def find_bound(nums, target, left):
            lo, hi = 0, len(nums)
            while lo < hi:
                mid = (lo + hi) // 2
                if nums[mid] > target or (left and nums[mid] == target):
                    hi = mid
                else:
                    lo = mid + 1
            return lo

        left = find_bound(nums, target, True)
        if left == len(nums) or nums[left] != target:
            return [-1, -1]
        right = find_bound(nums, target, False)
        return [left, right - 1]
```

**3 个核心要点（面试官必问）**

* **左右边界条件不同**：找左边界时 target <= nums\[mid] 收缩右边界，找右边界时 target >= nums\[mid] 收缩左边界；

* **返回值细节**：find\_bound(..., False) 返回第一个 > target 的下标，减一才是最后一个 target 的下标；

* **判空必要性**：若左边界越界或 nums\[left] != target，直接返回 \[-1, -1]，避免无效访问。

***

### 4. 寻找两个正序数组的中位数

**面试口述思路（二分）** 二分短数组找分割线； 将两数组划分为左右两部分，使左边元素数 = 右边元素数； 左边最大 <= 右边最小时找到正确分割，计算中位数。

**超短一句话版** 二分短数组找分割线，左边元素数等于右边，左边 max <= 右边 min 则找到。

**代码**

```python
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        if len(nums1) > len(nums2):  # 确保nums1是短的
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        left = 0
        right = m
        while left <= right:
            i = (left + right) // 2  # nums1的分割位置
            j = (m + n + 1) // 2 - i  # nums2的分割位置
            nums1_left_max = float('-inf') if i == 0 else nums1[i - 1]
            nums1_right_min = float('inf') if i == m else nums1[i]
            nums2_left_max = float('-inf') if j == 0 else nums2[j - 1]
            nums2_right_min = float('inf') if j == n else nums2[j]
            if nums1_left_max <= nums2_right_min and nums2_left_max <= nums1_right_min:
                if (m + n) % 2 == 0:
                    return (max(nums1_left_max, nums2_left_max) + min(nums1_right_min, nums2_right_min)) / 2
                else:
                    return max(nums1_left_max, nums2_left_max)
            elif nums1_left_max > nums2_right_min:
                right = i - 1
            else:
                left = i + 1
        return 0.0
```

**3 个核心要点（面试官必问）**

* **二分短数组原因**：确保时间复杂度 O(log(min(m,n)))，二分较长数组没有意义；

* **分割线条件**：左边所有元素个数 = 右边所有元素个数（偶数），或左边 = 右边+1（奇数），通过 i 和 j 配合实现；

* **找到条件**：nums1\_left\_max <= nums2\_right\_min 且 nums2\_left\_max <= nums1\_right\_min 时，分割线正确，中位数在边界处计算。

***

## 前缀和

### 560. 和为 K 的子数组

**面试口述思路（前缀和+哈希）** 前缀和思想：从头累加到当前位置的和； 若之前某个前缀和 = 当前前缀和 - k，则这段子数组和为 k； 用哈希表记录前缀和出现次数。

**超短一句话版** 前缀和+哈希表，查「当前和 - k」出现过几次，O(n)。

**代码**

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix = {0: 1}  # 前缀和->次数
        cur = 0
        count = 0
        for num in nums:
            cur += num  # 累加前缀和
            count += prefix.get(cur - k, 0)  # 找差值
            prefix[cur] = prefix.get(cur, 0) + 1  # 存入当前和
        return count
```

**3 个核心要点（面试官必问）**

* **初始化 prefix = {0: 1} 的含义**：前缀和为 0 出现一次，用于处理从数组开头到当前位置恰好和为 k 的情况；

* **cur - k 的含义**：若之前某处前缀和为 cur - k，加上当前元素后子数组和恰好为 k，count 累加该前缀和出现的次数；

* **哈希表实时更新**：每遍历一个元素就将当前前缀和的出现次数 +1，保证后续元素能查到所有历史前缀和。

***

### 525. 连续数组

**面试口述思路（前缀和+哈希）** 将 0 变为 -1，转化为求和为 0 的最长子数组； 用哈希表记录前缀和第一次出现的位置； 当前和已见过则更新最长长度。

**超短一句话版** 0 变 -1 后求和为 0 最长子数组，哈希表存前缀和首次位置，O(n)。

**代码**

```python
class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        prefix = {0: -1}  # 前缀和->首次位置
        cur = 0
        max_len = 0
        for i, num in enumerate(nums):
            cur += 1 if num == 1 else -1  # 0变-1
            if cur in prefix:
                max_len = max(max_len, i - prefix[cur])
            else:
                prefix[cur] = i  # 首次出现
        return max_len
```

**3 个核心要点（面试官必问）**

* **0 变 -1 的原理**：将问题转化为求「和为 0 的最长子数组」，因为 1 的个数 - 0 的个数 = 0 等价于前缀和相同；

* **首次出现位置记录**：哈希表只记录每个前缀和第一次出现的位置，确保子数组长度最大；

* **max\_len 更新规则**：当前前缀和已见过时，用 i - prefix\[cur] 计算长度，取较大值保留。

***

## 贪心

### 55. 跳跃游戏

**面试口述思路（贪心）** 维护能到达的最远位置； 遍历每个位置，更新最远距离； 若最远距离 >= 末尾，则可达。

**超短一句话版** 贪心维护最远可达位置，逐位置更新，能到末尾即成功。

**代码**

```python
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_reach = 0  # 最远可达位置
        for i, jump in enumerate(nums):
            if i > max_reach:  # 当前位置不可达
                return False
            max_reach = max(max_reach, i + jump)  # 更新最远
            if max_reach >= len(nums) - 1:  # 能到末尾
                return True
        return True
```

**3 个核心要点（面试官必问）**

* **max\_reach 的含义**：记录从已遍历位置出发能到达的最远下标，每次更新为 max(max\_reach, i + nums\[i])；

* **不可达判断**：若 i > max\_reach，说明当前位置在当前能到达范围之外，直接返回 False；

* **提前返回**：若 max\_reach >= len(nums) - 1，说明已能到达或超过末尾，直接返回 True。

***

### 56. 合并区间

**面试口述思路（排序+合并）** 按起点排序； 遍历区间，当前区间起点 <= 上个区间终点则合并（更新终点为较大值）； 否则开新区间。

**超短一句话版** 按起点排序，合并相交的区间，O(nlogn)。

**代码**

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
        intervals.sort(key=lambda x: x[0])  # 按起点排序
        result = [intervals[0]]
        for start, end in intervals[1:]:
            if start <= result[-1][1]:  # 重叠
                result[-1][1] = max(result[-1][1], end)
            else:
                result.append([start, end])
        return result
```

**3 个核心要点（面试官必问）**

* **排序的必要性**：按起点排序后，相交的区间必然连续，便于一次遍历完成合并；

* **合并判断条件**：当前区间起点 start <= 上个区间终点 result\[-1]\[1] 时，两者重叠需合并；

* **合并后终点取值**：合并后终点取 max(原终点, 新终点)，确保覆盖两个区间的范围。

***

### 134. 加油站

**面试口述思路（贪心）** 若总油量 >= 总消耗，则必有解； 从 0 开始累加，若油量不足则起点移到下一站，重置油量。

**超短一句话版** 总油量够必有解，累加油量不足则换起点，O(n)。

**代码**

```python
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total = 0  # 总油量-总消耗
        cur = 0  # 当前累计
        start = 0  # 起点
        for i in range(len(gas)):
            cur += gas[i] - cost[i]
            total += gas[i] - cost[i]
            if cur < 0:  # 从start到i都不行
                start = i + 1
                cur = 0
        return start if total >= 0 else -1
```

**3 个核心要点（面试官必问）**

* **total >= 0 的意义**：遍历一圈后总油量 >= 总消耗，是存在有效解的必要条件，若不满足直接返回 -1；

* **cur < 0 的含义**：说明从当前起点 start 到位置 i 之间，没有任何点能作为起点（油量不够），将起点移到 i+1；

* **贪心正确性**：若 start 到 i 的油量累计为负，则 start 之前的所有点作为起点到 i 必然也为负，不可能成功。

***

## 位运算

### 136. 只出现一次的数字

**面试口述思路（异或）** 异或运算：相同数字异或为 0，0 异或任何数为其本身； 所有数字异或，结果为只出现一次的数。

**超短一句话版** 全员异或，相同为 0，0 异或不变，O(n) O(1)。

**代码**

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        result = 0
        for num in nums:
            result ^= num  # 异或
        return result
```

**3 个核心要点（面试官必问）**

* **异或的数学性质**：满足交换律 a^b^c = a^c^b，结合律 a^(b^c) = (a^b)^c，相同数异或为 0；

* **成对抵消原理**：所有出现两次的数字异或后相互抵消为 0，只剩出现一次的那个数；

* **与 0 异或不变**：0 ^ x = x，保证最终结果就是只出现一次的数字。

***

### 231. 2的幂

**面试口述思路（位运算）** n & (n-1) 会消掉最低位的 1； 若结果为 0，则 n 是 2 的幂。

**超短一句话版** n & (n-1) 消掉最低位的 1，为 0 则是 2 的幂。

**代码**

```python
class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and (n & (n - 1)) == 0
```

**3 个核心要点（面试官必问）**

* **2 的幂的二进制特征**：恰好只有一位为 1（如 8 = 1000），而其他数至少有两位为 1；

* **n-1 的作用**：n-1 会把最低位的 1 变成 0，其后所有位变成 1（如 8-1 = 7 = 0111）；

* **n & (n-1) 的结果**：消掉最低位的 1 后，若结果为 0，说明原数只有这一位 1，即为 2 的幂。

***

## 图论

### 207. 课程表

**面试口述思路（拓扑排序）** 建图：邻接表 + 入度数组； BFS：入度为 0 的课程入队，学完一门减少后续入度； 能学完所有课程则无环。

**超短一句话版** 拓扑排序 BFS，入度 0 入队，学完减入度，无环则全部学完。

**代码**

```python
from collections import deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]  # 邻接表
        indegree = [0] * numCourses  # 入度
        for u, v in prerequisites:
            graph[v].append(u)  # v->u
            indegree[u] += 1
        queue = deque([i for i in range(numCourses) if indegree[i] == 0])  # 入度0入队
        visited = 0
        while queue:
            course = queue.popleft()
            visited += 1
            for next_course in graph[course]:
                indegree[next_course] -= 1
                if indegree[next_course] == 0:
                    queue.append(next_course)
        return visited == numCourses
```

**3 个核心要点（面试官必问）**

* **入度为 0 的课程**：表示没有前置课程要求，可以直接学习，是拓扑排序的起点；

* **学完减入度的原理**：学完一门课后，其指向的后续课程的前置要求减少一个，若减为 0 则变成新的可学课程；

* **visited == numCourses 的判断**：若最终访问的课程数等于总课程数，说明所有课程都能学完，即图中无环；若有环则某些课程入度永远不为 0。

***

## 前缀树

### 208. 实现 Trie（前缀树）

**面试口述思路（字典树）** 每个节点含字典存子节点和 isEnd 标记； insert 遍历字符逐层创建/移动； search/startsWith 遍历字符判断存在和前缀。

**超短一句话版** 字典树存子节点和结束标记，insert 逐层创建，search/prefix 遍历判断。

**代码**

```python
class Trie:
    def __init__(self):
        self.children = {}  # 子节点
        self.is_end = False  # 是否结束

    def insert(self, word: str) -> None:
        node = self
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._search_prefix(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._search_prefix(prefix) is not None

    def _search_prefix(self, prefix: str):
        node = self
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

**3 个核心要点（面试官必问）**

* **节点结构**：每个节点包含 children 字典（存储子节点）和 is\_end 标记（标记是否是某单词的结尾）；

* **查找失败条件**：\_search\_prefix 遍历过程中若字符不在 children 中，说明前缀不存在，直接返回 None；

* **search 与 startsWith 的区别**：search 要求完整匹配（is\_end 为 True），startsWith 只要求前缀路径存在，不要求 is\_end。

***

## 链表

### 2. 两数相加

**面试口述思路（链表模拟）** 从链表头开始逐位相加，用 carry 保存进位； 每位结果 = (l1.val + l2.val + carry) % 10，进位 = // 10； 创建新链表节点串联结果，遍历完还需处理最后的 carry。

**超短一句话版** 逐位相加模拟手算，进位 carry 保留，和为(和+进位)%10，进位为 //10。

**代码**

```python
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode()  # 哑节点
        cur = dummy
        carry = 0
        while l1 or l2 or carry:  # 继续条件
            s = (l1.val if l1 else 0) + (l2.val if l2 else 0) + carry
            carry = s // 10  # 进位
            cur.next = ListNode(s % 10)
            cur = cur.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return dummy.next
```

**3 个核心要点（面试官必问）**

* **while 循环条件**：l1 or l2 or carry，任一链表未遍历完或还有进位都要继续，确保不漏掉最后的进位节点；

* **dummy 哑节点作用**：统一头节点的创建逻辑，cur 指针负责逐位构建新链表，return dummy.next 即为结果；

* **None 处理技巧**：l1.val if l1 else 0，当某链表已遍历完时视为 0，避免空指针异常。

***

### 92. 翻转链表 II

**面试口述思路（哑节点+局部反转）** 哑节点指向链表头，先找到反转起始位置的前一个节点； cur 固定为区间第一个节点，每次把 cur 的下一个节点「头插」到 pre 后面，共 right - left 次； 头插过程中链表始终连着，无需额外拼接，返回哑节点的 next。

**超短一句话版** 哑节点定位前驱 pre，头插法把区间节点逐个挪到 pre 后，共 right-left 次。

**代码**

```python
class Solution:
    def reverseBetween(self, head: ListNode, left: int, right: int) -> ListNode:
        dummy = ListNode(next=head)  # 哑节点
        pre = dummy
        for _ in range(left - 1):  # 找到前驱
            pre = pre.next

        cur = pre.next  # 反转区间的第一个节点
        for _ in range(right - left):  # 头插法局部反转
            next_node = cur.next
            cur.next = next_node.next
            next_node.next = pre.next
            pre.next = next_node

        return dummy.next
```

**3 个核心要点（面试官必问）**

* **pre 指针的作用**：pre 固定在反转区间前一个节点不动，只通过移动其他指针完成局部反转；

* **插入反转的核心操作**：每次把 cur.next（即 next\_node）插入到 pre 后面，实现区间的就地反转；

* **循环次数**：反转循环执行 right - left 次，因为区间内有 n 个节点，需要反转 n-1 条指针。

***

## 数学

### 169. 多数元素

**面试口述思路（Boyer-Moore 投票）** 候选人票数抵消后剩的即为多数； count 为 0 时换候选人。

**超短一句话版** Boyer-Moore 投票，候选人票数抵消后剩的即为多数。

**代码**

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        count = 0
        candidate = None
        for num in nums:
            if count == 0:  # 换候选人
                candidate = num
            count += 1 if num == candidate else -1  # 票数抵消
        return candidate
```

**3 个核心要点（面试官必问）**

* **票数抵消思想**：相同数投赞成票，不同数投反对票，票数抵消后剩下的候选人就是出现次数 > n/2 的那个；

* **count == 0 换候选人**：说明之前的候选人在前面的子数组中已被完全抵消，需要重新选候选人；

* **为何能保证找到多数**：多数元素出现次数 > n/2，其票数抵消后必然有剩余，遍历完数组后留下的就是答案。

***

### 202. 快乐数

**面试口述思路（快慢指针）** 将数各位平方和作为下一个数； 快指针走两步，慢指针走一步； 若为快乐数则会到 1，否则进入循环。

**超短一句话版** 快慢指针检测循环，1 为终止状态。

**代码**

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        def next_num(x):
            return sum(int(d) ** 2 for d in str(x))

        slow = n
        fast = next_num(n)
        while fast != 1 and slow != fast:
            slow = next_num(slow)  # 慢走一步
            fast = next_num(next_num(fast))  # 快走两步
        return fast == 1
```

**3 个核心要点（面试官必问）**

* **快乐数的定义**：将各位数字平方和作为下一个数，不断迭代，最终若能到 1 则为快乐数；

* **循环判断**：非快乐数会陷入循环（不会到 1），快慢指针最终会在循环中相遇；

* **终止条件**：快慢指针相遇时若 fast == 1 说明是快乐数，否则进入循环的不是快乐数。

***

## 总结

| 分类 | 核心方法 |
| --- | --- |
| 哈希表 | O(1) 查找、计数、去重 |
| 双指针 | 收窄、比较、交换 |
| 滑动窗口 | 扩右收左、包含则收 |
| 单调栈 | 单调递增/递减、下一个更大/更小 |
| 二叉树 | 递归、层序、后序、DFS |
| 回溯 | 选或不选、路径记录、去重 |
| 动态规划 | 最优子结构、状态转移、压缩 |
| 二分查找 | 有序分割、边界收缩 |
| 前缀和 | 差分、哈希表统计 |
| 贪心 | 局部最优、全局最优 |
| 位运算 | 异或、移位、掩码 |
| 图论 | BFS、拓扑排序、连通性 |
| 前缀树 | 字典树、前缀匹配 |
| 链表 | 虚拟头结点、局部反转 |
| 数学 | 投票、快慢指针 |
