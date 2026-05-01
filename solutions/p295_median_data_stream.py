# LC 295. 数据流的中位数 · Hard · 双堆
"""
🔹 直觉
    维护两个堆:
        lo:大顶堆(存小一半);hi:小顶堆(存大一半)。
    保证 |lo| - |hi| ∈ {0,1}。中位数 = lo 顶 或 (lo顶+hi顶)/2。

🔹 trick(Python 没大顶堆)
    把 lo 入负值实现大顶。
"""
import heapq


class MedianFinder:
    def __init__(self):
        self.lo: list[int] = []        # 大顶(存负)
        self.hi: list[int] = []        # 小顶

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2


def _test() -> None:
    mf = MedianFinder()
    mf.addNum(1); mf.addNum(2)
    assert mf.findMedian() == 1.5
    mf.addNum(3)
    assert mf.findMedian() == 2.0
    print("✅ p295 通过")


if __name__ == "__main__":
    _test()
