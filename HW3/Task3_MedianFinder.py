class MedianFinder:

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.data = []

    def addNum(self, num: int) -> None:
        if isinstance(num, int):
            self.data.append(num)
        else:
            raise ValueError

    def findMedian(self) -> float:
        self.data.sort()
        size = self.size()
        if size % 2 == 0:
            return sum(self.data[size // 2) - 1:int(size / 2) + 1]) / 2
        else:
            return self.data[int(size / 2)]

    def size(self)->int:
        return len(self.data)

obj = MedianFinder()
obj.addNum(1)
print(obj.findMedian())
obj.addNum(2)
print(obj.findMedian())
obj.addNum(3)
print(obj.findMedian())
