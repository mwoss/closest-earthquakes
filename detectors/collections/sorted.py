import heapq
from copy import deepcopy
from typing import List, TypeVar, Optional

T = TypeVar('T')

#
# class LimitedHeapSet:
#     """Sorted collection based on heap data structure. Contains only unique entries."""
#
#     def __init__(self):
#         self.heap = []
#         self._unique_values = set()
#
#     def add(self, elem: T):
#         """
#         Add new element to collection if value is not present in heap
#         :param elem: Hashable element
#         :return: None
#         """
#         if elem not in self._unique_values:
#             heapq.heappush(self.heap, elem)
#             self._unique_values.add(elem)
#
#     def pop(self) -> Optional[T]:
#         """
#         Retrieves and removes the top element of heap return None if heap is empty
#         :return: Head element, None if heap is empty
#         """
#         try:
#             elem = heapq.heappop(self.heap)
#             self._unique_values.remove(elem)
#         except IndexError:
#             return None
#         return elem
#
#     def as_ordered_list(self) -> List[T]:
#         """
#         Return collection elements in sorted increasing order.
#         :return: List[T] with collection elements
#         """
#         result = []
#         temp_heap = deepcopy(self.heap)
#         while temp_heap:
#             result.append(heapq.heappop(self.heap))
#         return result


class LimitedHeapSet:
    """Sorted collection based on heap data structure. Contains only unique entries."""

    def __init__(self, maxsize: int):
        self.maxsize = maxsize
        self._heap = []
        self._unique_values = set()

    def add(self, elem: T):
        """
        Add new element to collection if value is not present in heap
        :param elem: Hashable element
        :return: None
        """
        if elem not in self._unique_values:
            if len(self._heap) < self.maxsize:
                heapq.heappush(self._heap, elem)
            elif self._heap[0] > elem:
                heapq.heappushpop(self._heap, elem)
            self._unique_values.add(elem)

    def pop(self) -> Optional[T]:
        """
        Retrieves and removes the top element of heap return None if heap is empty
        :return: Head element, None if heap is empty
        """
        try:
            elem = heapq.heappop(self._heap)
            self._unique_values.remove(elem)
        except IndexError:
            return None
        return elem

    def as_ordered_list(self) -> List[T]:
        """
        Return collection elements in sorted increasing order.
        :return: List[T] with collection elements
        """
        result = []
        temp_heap = deepcopy(self._heap)
        while temp_heap:
            result.append(heapq.heappop(self._heap))
        return result
