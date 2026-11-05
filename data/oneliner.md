# LC100 · 一句话速记（Python 面试口述版）

> 选题来源：python版本.md（一句话版）+ 力扣100手撕.pdf（手撕PDF，仅取选题，内容为本站 Python 重写）。已逐题自测。由 `scripts/build_oneliner.py` 构建为 `data/oneliner.json`。
> 格式：`## 分类` → `### 题号. 标题` → `> 来源：…` → 口述思路 / 超短一句话版 / 代码 / 3 个核心要点 / (可选)追问 / (可选)另一种写法。
> 无 LeetCode 题号的手撕题用英文 id，如 `### singleton. 单例模式`。

## 哈希表

### 1. 两数之和

> 来源：一句话版

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

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版 · 手撕PDF

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

**另一种写法（桶排序，O(n)）** 下标是出现次数的桶，从高频桶往低频倒着取，取满 k 个即停。

```python
from collections import Counter

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        cnt = Counter(nums)
        buckets = [[] for _ in range(max(cnt.values()) + 1)]  # 下标 = 出现次数
        for x, c in cnt.items():
            buckets[c].append(x)
        ans = []
        for c in range(len(buckets) - 1, 0, -1):  # 从高频往低频取
            ans += buckets[c]
            if len(ans) >= k:  # 题目保证答案唯一，取满即停
                return ans[:k]
        return ans
```

***

### 128. 最长连续序列

> 来源：手撕PDF

**面试口述思路（哈希集合）** 把所有数放进哈希集合； 只从序列起点开始数：x-1 不在集合里，x 才是起点； 从起点不断查 x+1、x+2……，更新最长长度。

**超短一句话版** 哈希集合去重，只从 x-1 不存在的起点往后数，O(n)。

**代码**

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        st = set(nums)  # 去重 + O(1) 查找
        ans = 0
        for x in st:
            if x - 1 in st:  # 不是起点，跳过，避免重复数
                continue
            y = x + 1
            while y in st:  # 从起点往后数
                y += 1
            ans = max(ans, y - x)  # 序列为 [x, y)
        return ans
```

**3 个核心要点（面试官必问）**

* **只从起点开始数**：保证每个数最多被内层 while 访问一次，整体 O(n)；

* **遍历集合而非原数组**：原数组可能有大量重复值，遍历集合避免重复起点；

* **为什么不排序**：题目要求 O(n)，排序是 O(n log n)。

**面试追问应对（加分）** 若问「还有别的做法吗」，答：并查集把相邻的数合并，最后看最大集合大小，但写起来比哈希集合复杂。

***

### 146. LRU 缓存

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版 · 手撕PDF

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

**另一种写法（递归）** 小的当头，它的 next 交给递归去合并剩下的；空间 O(m+n) 递归栈。

```python
class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        if not l1:
            return l2
        if not l2:
            return l1
        if l1.val <= l2.val:  # 小的当头，剩下的递归合并
            l1.next = self.mergeTwoLists(l1.next, l2)
            return l1
        l2.next = self.mergeTwoLists(l1, l2.next)
        return l2
```

***

### 206. 反转链表

> 来源：一句话版 · 手撕PDF

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

**另一种写法（递归）** 先递归反转后面的部分，再让 head.next 指回 head；空间 O(n) 递归栈。

```python
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if not head or not head.next:  # 空或只剩一个节点
            return head
        new_head = self.reverseList(head.next)  # 先反转后面
        head.next.next = head  # 让后一个节点指回自己
        head.next = None  # 断开原指向，防止成环
        return new_head
```

***

### 141. 环形链表

> 来源：一句话版 · 手撕PDF

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

### 142. 环形链表 II

> 来源：手撕PDF

**面试口述思路（Floyd 判圈找入口）** 快慢指针先判环：快走两步、慢走一步，相遇说明有环； 相遇后，一个指针从头出发，slow 从相遇点出发，都每次走一步； 两者再次相遇的地方就是环入口。

**超短一句话版** 快慢指针先相遇，再让一个指针从头和 slow 同速走，相遇点即入口。

**代码**

```python
class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:  # 相遇，说明有环
                p = head
                while p is not slow:  # 头和相遇点同速走，在入口相遇
                    p = p.next
                    slow = slow.next
                return p
        return None  # 快指针走到头，无环
```

**3 个核心要点（面试官必问）**

* **数学推导**：设头到入口 a、入口到相遇点 b、环长 c，慢指针走了 a+b，快指针走了 2(a+b)，多出的 a+b 是环长的整数倍，所以从相遇点再走 a 步正好回到入口；

* **用 is 比较**：比较的是节点对象本身，不是节点的值；

* **无环情况**：fast 或 fast.next 先为 None，直接返回 None。

**面试追问应对（加分）** 若问「哈希表做法」，答：遍历时把节点放进 set，第一个重复出现的节点就是入口，O(n) 空间。

***

### 19. 删除链表的倒数第 N 个结点

> 来源：一句话版

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

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版 · 手撕PDF

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

### 5. 最长回文子串

> 来源：手撕PDF

**面试口述思路（中心扩展）** 枚举所有回文中心，共 2n-1 个（n 个单字符中心 + n-1 个双字符中心）； 从中心向两边扩展，直到两端字符不相等； 记录最长的长度和起点，最后切片返回。

**超短一句话版** 枚举 2n-1 个中心向两边扩，记录最长，O(n²) 时间 O(1) 空间。

**代码**

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        start, max_len = 0, 0

        def expand(l, r):  # 从中心向两边扩，返回回文长度
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return r - l - 1  # 跳出时 l、r 都多走了一步

        for i in range(len(s)):
            for l, r in ((i, i), (i, i + 1)):  # 奇数中心、偶数中心
                cur = expand(l, r)
                if cur > max_len:
                    max_len = cur
                    start = i - (cur - 1) // 2  # 由中心和长度反推起点
        return s[start:start + max_len]
```

**3 个核心要点（面试官必问）**

* **奇偶两种中心**：「aba」的中心是一个字符，「abba」的中心在两个字符之间，两种都要枚举；

* **长度公式 r - l - 1**：循环退出时 l、r 各多走了一步，所以长度是 (r-1) - (l+1) + 1；

* **起点反推**：start = i - (len-1)//2，奇偶两种中心都适用。

**面试追问应对（加分）** 若问「有没有 O(n) 解」，答：Manacher 算法利用已知回文的对称性跳过重复扩展，面试说出思路即可；DP 解法 dp[i][j] = s[i]==s[j] and dp[i+1][j-1] 也是 O(n²)，但要 O(n²) 空间。

***

## 滑动窗口

### 76. 最小覆盖子串

> 来源：一句话版

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

> 来源：一句话版

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

### 239. 滑动窗口最大值

> 来源：手撕PDF

**面试口述思路（单调队列）** 双端队列存下标，保持对应的值单调递减； 新元素入队前，把队尾比它小或相等的都弹掉； 队首下标滑出窗口就从队首弹出； 窗口长度够 k 后，队首就是当前窗口最大值。

**超短一句话版** 单调递减双端队列存下标，入队弹小、出窗弹头，队首即最大值，O(n)。

**代码**

```python
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        q = deque()  # 存下标，对应值单调递减，队首是窗口最大值
        ans = []
        for i, x in enumerate(nums):
            while q and nums[q[-1]] <= x:  # 队尾比新元素小，以后不可能再当最大值
                q.pop()
            q.append(i)
            if q[0] <= i - k:  # 队首滑出窗口
                q.popleft()
            if i >= k - 1:  # 窗口形成后记录答案
                ans.append(nums[q[0]])
        return ans
```

**3 个核心要点（面试官必问）**

* **为什么能弹掉队尾**：它比新元素小、又比新元素先离开窗口，之后任何窗口里都有新元素压着，永远当不了最大值；

* **存下标而不是值**：要靠下标判断队首是否已经滑出窗口；

* **复杂度 O(n)**：每个元素最多入队一次、出队一次。

**面试追问应对（加分）** 若问「能不能用堆」，答：最大堆存 (-值, 下标)，堆顶过期就弹掉，O(n log n)，不如单调队列。

***

## 单调栈

### 739. 每日温度

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版 · 手撕PDF

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

**另一种写法（双指针，O(1) 空间）** 左右双指针维护两侧最高，哪边矮就结算哪边这一格，不用栈。

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        pre_max = suf_max = 0  # 左侧最高、右侧最高
        ans = 0
        while left < right:
            pre_max = max(pre_max, height[left])
            suf_max = max(suf_max, height[right])
            if pre_max < suf_max:  # 左边矮，左边这格的水由 pre_max 决定
                ans += pre_max - height[left]
                left += 1
            else:  # 右边矮，右边这格由 suf_max 决定
                ans += suf_max - height[right]
                right -= 1
        return ans
```

***

## 二叉树和递归

### 94. 二叉树的中序遍历

> 来源：一句话版 · 手撕PDF

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

**另一种写法（递归）** 左、根、右三行递归，面试先写这个，再补迭代版。

```python
class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        ans = []

        def dfs(node):
            if not node:
                return
            dfs(node.left)  # 左
            ans.append(node.val)  # 根
            dfs(node.right)  # 右

        dfs(root)
        return ans
```

***

### 102. 二叉树的层序遍历

> 来源：手撕PDF

**面试口述思路（BFS 队列）** 根节点入队； 每轮先记下队列长度，就是当前层的节点数； 只弹出这么多个节点，收集值并把孩子入队； 一轮结束就得到一层。

**超短一句话版** BFS 队列，每轮先取队长作为本层节点数，弹完一层收一层。

**代码**

```python
from collections import deque

class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        ans = []
        q = deque([root])
        while q:
            vals = []
            for _ in range(len(q)):  # 只处理当前层的节点
                node = q.popleft()
                vals.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            ans.append(vals)
        return ans
```

**3 个核心要点（面试官必问）**

* **分层的关键**：range(len(q)) 在循环开始时就固定了次数，循环中新加入的孩子属于下一层；

* **用 deque**：popleft 是 O(1)，list.pop(0) 是 O(n)；

* **复杂度**：每个节点进出队一次，时间 O(n)，空间 O(w)，w 是树的最大宽度。

**面试追问应对（加分）** 若问「锯齿形 / 右视图」，答：锯齿形按层号奇偶把 vals 反转；右视图取每层最后一个值。

***

### 105. 从前序与中序遍历序列构造二叉树

> 来源：手撕PDF

**面试口述思路（前序定根，中序分左右）** 前序遍历的第一个元素是根； 在中序里找到根的位置，左边是左子树、右边是右子树； 用左子树的大小切分前序数组，递归构建左右子树。

**超短一句话版** 前序定根，中序分左右，用左子树大小切前序，递归建树。

**代码**

```python
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        index = {x: i for i, x in enumerate(inorder)}  # 值 -> 中序下标，O(1) 找根

        def build(pre_l, pre_r, in_l, in_r):  # 左闭右开区间
            if pre_l == pre_r:  # 空区间
                return None
            root_val = preorder[pre_l]  # 前序第一个是根
            k = index[root_val]  # 根在中序中的位置
            left_size = k - in_l  # 左子树大小
            root = TreeNode(root_val)
            root.left = build(pre_l + 1, pre_l + 1 + left_size, in_l, k)
            root.right = build(pre_l + 1 + left_size, pre_r, k + 1, in_r)
            return root

        return build(0, len(preorder), 0, len(inorder))
```

**3 个核心要点（面试官必问）**

* **哈希表加速找根**：预存中序下标，每次 O(1) 找到根，整体 O(n)；每次线性查找会变成 O(n²)；

* **区间切分**：左子树的前序是 [pre_l+1, pre_l+1+left_size)，右子树紧随其后到 pre_r；

* **前提**：节点值互不相同，才能在中序里唯一定位根。

**面试追问应对（加分）** 若问「中序 + 后序」，答：后序的最后一个是根，其余同理，就是 LC 106。

***

### 104. 二叉树的最大深度

> 来源：一句话版

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

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版

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

> 来源：一句话版 · 手撕PDF

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

### 79. 单词搜索

> 来源：手撕PDF

**面试口述思路（DFS 回溯）** 枚举每个格子作为起点； 当前格子等于 word[k] 才继续，并把格子临时置空，标记已访问； 向四个方向递归匹配 word[k+1]； 四个方向都失败就恢复格子，返回 False。

**超短一句话版** 每格出发 DFS，匹配就标记已访问往四周找下一个字符，失败回溯恢复。

**代码**

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])

        def dfs(i, j, k):  # board[i][j] 开始能否匹配 word[k:]
            if board[i][j] != word[k]:
                return False
            if k == len(word) - 1:  # 最后一个字符也匹配上了
                return True
            board[i][j] = ''  # 标记已访问
            for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= x < m and 0 <= y < n and dfs(x, y, k + 1):
                    board[i][j] = word[k]  # 返回前恢复
                    return True
            board[i][j] = word[k]  # 回溯：恢复现场
            return False

        return any(dfs(i, j, 0) for i in range(m) for j in range(n))
```

**3 个核心要点（面试官必问）**

* **原地标记**：把格子临时改成空字符代替 visited 数组，回溯时一定要改回来；

* **剪枝**：字符不匹配立刻返回；还可以先统计字符频次，board 里某个字符不够用就直接返回 False；

* **复杂度**：O(m·n·3^L)，L 是单词长度，除第一步外每步最多 3 个新方向。

**面试追问应对（加分）** 若问「还能怎么优化」，答：如果 word 末尾字符在 board 里出现得比开头少，把 word 反转再搜，起点更少。

***

### 131. 分割回文串

> 来源：手撕PDF

**面试口述思路（回溯枚举切点）** 从下标 i 开始，枚举这一段的结尾 j； 如果 s[i..j] 是回文，加入路径，从 j+1 继续切； 切到末尾记录一种方案，然后回溯撤销。

**超短一句话版** 回溯枚举每段结尾，是回文才切下一刀，切到末尾收集答案。

**代码**

```python
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        ans, path = [], []

        def dfs(i):  # 从下标 i 开始切
            if i == n:  # 切完了
                ans.append(path[:])
                return
            for j in range(i, n):  # 枚举这一段的结尾 j
                t = s[i:j + 1]
                if t == t[::-1]:  # 是回文才切
                    path.append(t)
                    dfs(j + 1)
                    path.pop()  # 回溯

        dfs(0)
        return ans
```

**3 个核心要点（面试官必问）**

* **枚举结尾**：每层递归决定「这一刀切在哪」，和子集、组合是同一个回溯模板；

* **回文判断可预处理**：dp[i][j] = s[i]==s[j] and dp[i+1][j-1]，判断降到 O(1)；

* **复杂度**：最坏 O(n·2^n)，比如全是同一个字符时每个位置都能切。

**面试追问应对（加分）** 若问「最少切几刀」，答：那是 LC 132，改成 DP：f[i] = min(f[j-1] + 1)，其中 s[j..i] 是回文。

***

### 200. 岛屿数量

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版

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

### 437. 路径总和 III

> 来源：手撕PDF

**面试口述思路（树上前缀和）** 根到当前节点的路径和记为前缀和 s； 查哈希表里 s - target 出现过几次，累加到答案； 把 s 计入哈希表后递归左右子树； 返回前撤销 s，保证表里只有当前路径上的前缀和。

**超短一句话版** 树上前缀和 + 哈希计数，查 s-target 的次数，递归回来记得撤销，O(n)。

**代码**

```python
from collections import defaultdict

class Solution:
    def pathSum(self, root: TreeNode, targetSum: int) -> int:
        cnt = defaultdict(int)  # 前缀和 -> 出现次数（只含当前路径）
        cnt[0] = 1  # 空前缀，处理从根开始的路径
        ans = 0

        def dfs(node, s):
            nonlocal ans
            if not node:
                return
            s += node.val  # 根到当前节点的前缀和
            ans += cnt[s - targetSum]  # 以当前节点结尾、和为 target 的路径数
            cnt[s] += 1
            dfs(node.left, s)
            dfs(node.right, s)
            cnt[s] -= 1  # 回溯：离开当前节点时撤销

        dfs(root, 0)
        return ans
```

**3 个核心要点（面试官必问）**

* **和「和为 K 的子数组」同一个套路**：把根到节点的路径看成数组，前缀和差值为 target 就是一条路径；

* **回溯撤销**：不撤销的话，兄弟分支的前缀和会混进来，算出不在同一条向下路径上的「假路径」；

* **cnt[0] = 1**：处理从根节点开始、整条路径和正好为 target 的情况。

**面试追问应对（加分）** 若问「暴力怎么做」，答：每个节点作为起点往下 DFS 统计，O(n²)。

***

## 动态规划

### 70. 爬楼梯

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版 · 手撕PDF

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

**另一种写法（O(n²) DP）** dp[i] 是以 nums[i] 结尾的 LIS 长度，枚举前面比它小的 nums[j] 转移；先说这个再优化到二分。

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = [1] * len(nums)  # dp[i]：以 nums[i] 结尾的 LIS 长度
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:  # 能接在 nums[j] 后面
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
```

***

### 139. 单词拆分

> 来源：手撕PDF

**面试口述思路（DP）** dp[i] 表示 s 的前 i 个字符能否被拆分； 枚举最后一个单词的起点 j，如果 dp[j] 为真且 s[j:i] 在字典里，dp[i] 就为真； 答案是 dp[n]。

**超短一句话版** dp[i] 看前 i 个字符能否拆，枚举最后一个单词 s[j:i]，dp[j] 为真且在字典里即可。

**代码**

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)  # 转集合，O(1) 查找
        max_len = max(map(len, words))  # 最长单词长度，用于剪枝
        n = len(s)
        dp = [False] * (n + 1)  # dp[i]：前 i 个字符能否拆分
        dp[0] = True  # 空串可拆分
        for i in range(1, n + 1):
            for j in range(i - 1, max(i - max_len, 0) - 1, -1):  # 最后一段长度不超过 max_len
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[n]
```

**3 个核心要点（面试官必问）**

* **dp[0] = True**：空串可以被拆分，是所有转移的起点；

* **字典转 set**：s[j:i] in words 变成 O(1) 查找，否则每次都要线性扫一遍列表；

* **最长单词剪枝**：最后一段不可能比最长单词还长，j 只需往回看 max_len 个位置。

**面试追问应对（加分）** 若问「要输出所有拆分方案」，答：那是 LC 140，改成记忆化 DFS，返回从位置 i 开始的所有拆法。

***

### 322. 零钱兑换

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版

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

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版

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

> 来源：一句话版 · 手撕PDF

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

**另一种写法（前缀和）** 子数组和 = 当前前缀和 - 之前最小前缀和，和「买卖股票」同一个模型。

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        ans = float('-inf')
        pre = 0  # 当前前缀和
        min_pre = 0  # 之前出现过的最小前缀和
        for x in nums:
            pre += x
            ans = max(ans, pre - min_pre)  # 以 x 结尾的最大子数组和
            min_pre = min(min_pre, pre)  # 先算答案再更新，保证子数组非空
        return ans
```

***

### 152. 乘积最大子数组

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版 · 手撕PDF

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版

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

> 来源：一句话版

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

### 234. 回文链表

> 来源：手撕PDF

**面试口述思路（快慢指针 + 反转后半段）** 快慢指针找到中点； 反转后半段链表； 前半段从头、后半段从反转后的头，逐个比较。

**超短一句话版** 快慢指针找中点，反转后半段，两半逐个比，O(n) 时间 O(1) 空间。

**代码**

```python
class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        # 1. 快慢指针找中点：slow 停在前半段末尾
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        # 2. 反转后半段
        prev, cur = None, slow.next
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        # 3. 两半逐个比较，后半段不比前半段长
        p, q = head, prev
        while q:
            if p.val != q.val:
                return False
            p, q = p.next, q.next
        return True
```

**3 个核心要点（面试官必问）**

* **中点的位置**：循环条件 fast.next and fast.next.next 让 slow 停在前半段末尾，奇数长度时中间节点归前半段，比较时以后半段为准；

* **为什么要反转**：单链表不能倒着走，反转后半段才能从尾往前比；

* **空间 O(1)**：转数组或递归都要 O(n) 空间；面试时最好提一句「比完再把后半段反转回来，恢复原链表」。

**面试追问应对（加分）** 若问「不改链表怎么做」，答：把值存进数组判断 vals == vals[::-1]，O(n) 空间；或者用递归在回溯时从尾往前比。

***

### 92. 翻转链表 II

> 来源：一句话版

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

### 25. K 个一组翻转链表

> 来源：手撕PDF

**面试口述思路（分组反转 + 接线）** 先遍历求长度 n，不足 k 个的尾巴不翻； 每组用反转链表的三步走翻 k 次； 翻完后，上一组的尾巴接本组新头，本组新尾接下一组的头。

**超短一句话版** 先数长度，够 k 个就组内反转，再用 p0 把上一组尾、本组头尾、下一组头接起来。

**代码**

```python
class Solution:
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        n = 0  # 先统计长度
        cur = head
        while cur:
            n += 1
            cur = cur.next

        dummy = ListNode(next=head)
        p0 = dummy  # 上一组的尾巴
        pre, cur = None, head
        while n >= k:  # 剩余够 k 个才翻
            n -= k
            for _ in range(k):  # 组内反转，同反转链表
                nxt = cur.next
                cur.next = pre
                pre = cur
                cur = nxt
            # 此时 pre 是本组新头，cur 是下一组的头，p0.next 是本组新尾
            tail = p0.next
            tail.next = cur  # 本组新尾接下一组
            p0.next = pre  # 上一组接本组新头
            p0 = tail  # p0 移到本组尾巴
        return dummy.next
```

**3 个核心要点（面试官必问）**

* **哑节点 + p0**：p0 始终指向上一组的尾巴，第一组的「上一组」就是 dummy，不用特判头节点；

* **接线顺序**：先用 tail 记住 p0.next（本组新尾），再 tail.next = cur、p0.next = pre，最后 p0 = tail；

* **复杂度**：每个节点只被反转一次，时间 O(n)，空间 O(1)。

**面试追问应对（加分）** 若问「不足 k 个也要翻」，答：把 n >= k 改成 n > 0，内层循环次数取 min(k, n)，最后一组剩多少翻多少。

***

## 数学

### 169. 多数元素

> 来源：一句话版

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

> 来源：一句话版

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

## 手撕基础

### 912. 快速排序（排序数组）

> 来源：手撕PDF

**面试口述思路（随机化快排）** 随机选一个基准 pivot 换到最左边； 双指针 i 从左找 ≥ pivot 的、j 从右找 ≤ pivot 的，找到就交换； 相遇后把 pivot 和 j 交换，pivot 归位； 递归排 pivot 左右两段。

**超短一句话版** 随机选基准，双指针把小的甩左、大的甩右，pivot 归位后递归两边，平均 O(n log n)。

**代码**

```python
import random

class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        def partition(left, right):
            i = random.randint(left, right)  # 随机选 pivot，防止有序数组退化
            nums[i], nums[left] = nums[left], nums[i]  # 换到最左边
            pivot = nums[left]
            i, j = left + 1, right
            while True:
                while i <= j and nums[i] < pivot:  # i 从左找第一个 >= pivot 的
                    i += 1
                while i <= j and nums[j] > pivot:  # j 从右找第一个 <= pivot 的
                    j -= 1
                if i >= j:  # 相遇或交叉，退出
                    break
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1
            nums[left], nums[j] = nums[j], nums[left]  # pivot 归位到 j
            return j

        def quick_sort(left, right):
            if left >= right:  # 区间长度 <= 1，不用排
                return
            p = partition(left, right)
            quick_sort(left, p - 1)
            quick_sort(p + 1, right)

        quick_sort(0, len(nums) - 1)
        return nums
```

**3 个核心要点（面试官必问）**

* **随机化 pivot**：固定选第一个元素时，有序数组每次只能切掉一个元素，退化成 O(n²)；随机选让期望复杂度回到 O(n log n)；

* **等于 pivot 也停下交换**：i、j 遇到等于 pivot 的元素都停下互换，大量重复元素时两边也能均分，避免退化；

* **复杂度与稳定性**：平均 O(n log n)、最坏 O(n²)，空间 O(log n) 递归栈，不稳定排序。

**面试追问应对（加分）** 若问「全是重复元素怎么办」，答：用三路快排把 = pivot 的元素聚在中间，只递归 < pivot 和 > pivot 两段。

***

### 215. 数组中的第K个最大元素

> 来源：手撕PDF

**面试口述思路（快速选择）** 第 k 大等价于升序排序后下标 n-k 的元素； 用快排的 partition 随机选 pivot 分区，pivot 归位到 j； j 等于 n-k 直接返回，j 大了去左边找，小了去右边找。

**超短一句话版** 快速选择：partition 后 pivot 落在 j，和 n-k 比较只走一边，平均 O(n)。

**代码**

```python
import random

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        target = len(nums) - k  # 第 k 大 = 升序后下标 n-k
        left, right = 0, len(nums) - 1
        while True:
            # 分区：同快排，随机 pivot + 双指针
            i = random.randint(left, right)
            nums[i], nums[left] = nums[left], nums[i]
            pivot = nums[left]
            i, j = left + 1, right
            while True:
                while i <= j and nums[i] < pivot:
                    i += 1
                while i <= j and nums[j] > pivot:
                    j -= 1
                if i >= j:
                    break
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1
            nums[left], nums[j] = nums[j], nums[left]  # pivot 归位到 j
            if j == target:  # 正好是目标位置
                return nums[j]
            if j > target:  # 目标在左半边
                right = j - 1
            else:  # 目标在右半边
                left = j + 1
```

**3 个核心要点（面试官必问）**

* **只走一边**：和快排不同，每次只需处理目标所在的一侧，期望 n + n/2 + n/4 + … = O(n)，最坏 O(n²)；

* **随机 pivot 必不可少**：LeetCode 有专门卡固定 pivot 的有序 / 重复数据，不随机会超时；

* **和堆的取舍**：维护大小为 k 的最小堆是 O(n log k)，不改原数组、适合数据流；快速选择更快但会打乱数组。

**面试追问应对（加分）** 若问「能不能用堆」，答：最小堆只留 k 个，堆顶就是第 k 大；Python 里 `heapq.nlargest(k, nums)[-1]` 一行即可。

***

### singleton. 单例模式

> 来源：手撕PDF

**面试口述思路（双重检查锁）** 类变量 _instance 保存唯一实例； 重写 __new__，已有实例就直接返回； 多线程下用双重检查加锁，防止两个线程同时创建出两个实例。

**超短一句话版** 类变量存唯一实例，__new__ 里双重检查加锁，保证全局只有一个对象。

**代码**

```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:  # 第一次检查：已创建就直接返回，避免每次都加锁
            with cls._lock:  # 加锁，防止多线程同时创建
                if cls._instance is None:  # 第二次检查：拿到锁后再确认一次
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**3 个核心要点（面试官必问）**

* **为什么检查两次**：外层检查让已创建后的调用不用抢锁；内层检查防止两个线程都通过了外层、排队拿锁后各建一个；

* **__init__ 每次都会执行**：每次 Singleton() 都会调用 __init__，初始化逻辑要么做成幂等，要么也放进 __new__ 里只做一次；

* **Python 的更简写法**：模块本身就是天然单例（import 只执行一次），也可以用装饰器或元类实现。

**面试追问应对（加分）** 若问「饿汉式和懒汉式」，答：饿汉式类加载时就创建，天然线程安全但可能用不上；懒汉式第一次用才创建，需要加锁保证线程安全。

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
| 手撕基础 | 快排分区、快速选择、单例双重检查 |
