import heapq
from typing import TypeVar, Optional, List

T = TypeVar('T')


class HeapObj:
    """Object for proper MinSet functioning, because Python does not provide max heap implementation"""

    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return self.val > other.val

    def __eq__(self, other):
        return self.val == other.val


class LimitedMinSet:
    """
    Sorted collection based on heap data structure.
    LimitedMinSet main functionality is to store 'maxsize' smallest elements.
    Collection can store maximally 'maxsize' elements in one time. Collection contains only unique entries
    """

    def __init__(self, maxsize: int):
        self.maxsize = maxsize
        self._heap = []
        self._unique_values = set()

    def __len__(self) -> int:
        return len(self._heap)

    @property
    def maxsize(self) -> int:
        return self._maxsize

    @maxsize.setter
    def maxsize(self, size: int):
        if size < 0:
            raise ValueError(f"Negative maxsize value. Maxsize always have to be greater than 0")
        self._maxsize = size

    def add(self, elem: T):
        """
        Add new element to collection if value is not present in heap.
        After reaching maxsize, only values smaller than heap head are added to collection (heap head is removed).
        :param elem: Hashable element
        :return: None
        """
        if elem not in self._unique_values:
            if len(self._heap) < self.maxsize:
                heapq.heappush(self._heap, HeapObj(elem))
            elif elem < self._heap[0].val:
                heapq.heappushpop(self._heap, HeapObj(elem))
            self._unique_values.add(elem)

    def pop(self) -> Optional[T]:
        """
        Retrieves and removes the top element of heap return None if heap is empty
        :return: Head element, None if heap is empty
        """
        try:
            elem = heapq.heappop(self._heap).val
            self._unique_values.remove(elem)
        except IndexError:
            return None
        return elem

    def as_ordered_list(self) -> List[T]:
        """
        Return collection elements in sorted increasing order.
        Heap is emptied after conversion.
        :return: List[T] with collection elements
        """
        result = []
        while self._heap:
            result.append(heapq.heappop(self._heap).val)
        return result[::-1]
