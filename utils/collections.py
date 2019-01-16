import heapq
from typing import List, TypeVar

T = TypeVar('T')


class UniqueSortedList:
    def __init__(self):
        self.heap = []
        self._unique_values = set()

    def add(self, elem: T):
        if elem not in self._unique_values:
            heapq.heappush(self.heap, elem)
            self._unique_values.add(elem)

    def pop(self) -> T:
        elem = heapq.heappop(self.heap)
        self._unique_values.remove(elem)
        return elem

    def ordered_result(self) -> List[T]:
        result = []
        while self.heap:
            result.append(heapq.heappop(self.heap))
        return result
