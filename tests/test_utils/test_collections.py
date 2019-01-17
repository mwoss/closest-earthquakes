from unittest import TestCase

from detectors.collections.sorted import LimitedMinSet


class TestLimitedMinSet(TestCase):
    def test_pop_should_return_none_with_empty_heap(self):
        min_set = LimitedMinSet(maxsize=3)

        elem = min_set.pop()

        self.assertIsNone(elem)

    def test_result_should_contains_k_elements(self):
        unsorted = [5, 4, 1, 2, 3]
        size = 2
        min_set = LimitedMinSet(maxsize=size)

        for elem in unsorted:
            min_set.add(elem)

        self.assertEqual(len(min_set), size)

    def test_result_should_contains_sorted_elements(self):
        unsorted = [5, 4, 1, 2, 3]
        min_set = LimitedMinSet(maxsize=5)

        for elem in unsorted:
            min_set.add(elem)

        self.assertListEqual(min_set.as_ordered_list(), sorted(unsorted))

    def test_result_should_contains_unique_values(self):
        min_set = LimitedMinSet(maxsize=5)

        for elem in [1, 1, 1]:
            min_set.add(elem)

        expected_result = [1]
        self.assertListEqual(min_set.as_ordered_list(), expected_result)

    def test_negative_maxsize_should_rise_exception(self):
        with self.assertRaises(ValueError):
            LimitedMinSet(maxsize=-5)
