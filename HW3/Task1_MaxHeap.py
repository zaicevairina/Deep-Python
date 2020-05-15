class MaxHeap:
    def __init__(self) -> None:
        self.heap = []

    def push(self, val: int) -> None:
        i = len(self.heap)
        A = self.heap
        A.append(val)
        parent = int((i - 1) / 2)
        while parent >= 0 and i > 0:
            if A[i] > A[parent]:
                A[i], A[parent] = A[parent], A[i]
            i = parent
            parent = int((i - 1) / 2)

    def pop(self) -> int:
        val = self.heap[0]
        self.heap[0] = self.heap[len(self.heap) - 1]
        self.heap.pop()
        self._heapify(0, iterable=self.heap)
        return val

    def _heapify(self, i:int, iterable)-> None:

        iterable_size = len(iterable)
        A = iterable
        l = 2 * i + 1
        r = 2 * i + 2
        largest = i
        if l < iterable_size and A[l] > A[largest]:
            A[i], A[l] = A[l], A[i]
            self._heapify(l, iterable)

        if r < iterable_size and A[r] > A[largest]:
            A[i], A[r] = A[r], A[i]
            self._heapify(r, iterable)

    def heapify(self, iterable=None) -> None:
        if iterable is None:
            iterable = self.heap
            for i in range(len(iterable), -1, -1):
                self._heapify(i, iterable)
        else:
            for i in range(len(iterable), -1, -1):
                self._heapify(i, iterable)
            return iterable


heap = MaxHeap()
heap.push(1)
heap.push(7)
print(heap.heap)
heap.push(3)
print(heap.heap)
heap.push(5)
print(heap.heap)
heap.push(4)
print(heap.heap)
heap.push(8)
print(heap.heap)
heap.push(10)
print(heap.heap)

x = heap.pop()
print(heap.heap)
x = heap.pop()
print(heap.heap)
x = heap.pop()
print(heap.heap)

print(heap.heapify([1, 2, 35, 6, 7, 8]))
