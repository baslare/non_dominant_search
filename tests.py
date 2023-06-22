import unittest
import numpy as np
from non_dom_sort import NonDominatedSort


class NonDominatedSortTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Tests the important functions using simple data"""
        cls.arr = np.array([[0, 3, 2],
                            [2, 2, 1],
                            [3, 1, 3],
                            [3, 4, 5],
                            [5, 5, 5],
                            [5, 6, 7]])

        cls.nds = NonDominatedSort(cls.arr)

    def test_pareto_compare_strong_1t1(self):
        """1 to 1 comparison for the strong case"""
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[0], self.arr[0]), 0)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[0], self.arr[3]), -1)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[3], self.arr[4]), 0)

    def test_pareto_compare_strong_1tm(self):
        """1 to many comparison for the strong case"""
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[[0, 1]], self.arr[3]), -1)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[2], self.arr[[0, 1]]), 0)

    def test_pareto_compare_strong_mtm(self):
        """Many to many comparison for the strong case"""
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[[0, 1, 2]], self.arr[[3, 4]]), -1)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[[0, 1, 2]], self.arr[[0, 1]]), 0)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[[3, 4]], self.arr[[0, 1]]), 1)

    def test_pareto_compare_strong_corner_cases(self):
        """Tests for some cases where strong and weak pareto dominance relation gives different results."""
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[0], self.arr[1]), 0)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[4], self.arr[5]), 0)

    def test_pareto_compare_weak1t1(self):
        self.assertEqual(NonDominatedSort.pareto_compare_weak(self.arr[0], self.arr[0]), 0)
        self.assertEqual(NonDominatedSort.pareto_compare_weak(self.arr[0], self.arr[3]), -1)
        self.assertEqual(NonDominatedSort.pareto_compare_weak(self.arr[3], self.arr[4]), -1)

    def test_pareto_compare_weak_1tm(self):
        self.assertEqual(NonDominatedSort.pareto_compare_weak(self.arr[[0, 1]], self.arr[3]), -1)
        self.assertEqual(NonDominatedSort.pareto_compare_weak(self.arr[2], self.arr[[0, 1]]), 0)

    def test_pareto_compare_weak_mtm(self):
        self.assertEqual(NonDominatedSort.pareto_compare_weak(self.arr[[0, 1, 2]], self.arr[[3, 4]]), -1)
        self.assertEqual(NonDominatedSort.pareto_compare_weak(self.arr[[0, 1, 2]], self.arr[[0, 1]]), 0)
        self.assertEqual(NonDominatedSort.pareto_compare_weak(self.arr[[3, 4]], self.arr[[0, 1]]), 1)

    def test_pareto_compare_weak_corner_cases(self):
        self.assertEqual(NonDominatedSort.pareto_compare_weak(self.arr[0], self.arr[1]), 0)
        self.assertEqual(NonDominatedSort.pareto_compare_weak(self.arr[4], self.arr[5]), -1)

    def test_sort_strong_min(self):
        """Tries the sorting algorithm using different arguments."""
        self.assertIn(self.nds.sort(), ([[1, 2, 0], [3], [4, 5]],
                                        [[1, 2, 0], [3, 4], [5]]))

    def test_sort_strong_max(self):
        self.assertIn(self.nds.sort(reverse=True), ([[4, 5], [3], [1, 2, 0]],
                                                    [[4, 5], [2, 3], [1, 0]]))

    def test_sort_weak_min(self):
        self.assertEqual(self.nds.sort(strong=False), [[1, 2, 0], [3], [4], [5]])

    def test_sort_weak_max(self):
        self.assertEqual(self.nds.sort(strong=False, reverse=True), [[5], [4], [3], [1, 2, 0]])


if __name__ == '__main__':
    unittest.main()
