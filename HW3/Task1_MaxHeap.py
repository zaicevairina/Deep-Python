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
                temp = A[i]
                A[i] = A[parent]
                A[parent] = temp
            i = parent
            parent = int((i - 1) / 2)

    def pop(self) -> int:
        val = self.heap[0]
        self.heap[0] = self.heap[len(self.heap) - 1]
        self.heap.pop()
        MaxHeap._heapify(0, iterable=self.heap)

        return val

    @staticmethod
    def _heapify(i, iterable):

        iterable_size = len(iterable)
        A = iterable
        l = 2 * i + 1
        r = 2 * i + 2
        largest = i
        if l < iterable_size and A[l] > A[largest]:
            temp = A[i]
            A[i] = A[l]
            A[l] = temp
            MaxHeap._heapify(l, iterable=iterable)

        if r < iterable_size and A[r] > A[largest]:
            temp = A[i]
            A[i] = A[r]
            A[r] = temp
            MaxHeap._heapify(r, iterable=iterable)

    def heapify(self, iterable) -> None:
        for i in range(len(iterable), -1, -1):
            MaxHeap._heapify(i, iterable=iterable)




