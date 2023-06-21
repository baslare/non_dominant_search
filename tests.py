import unittest
import numpy as np
from main import NonDominatedSort


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.arr = np.array([[0, 3, 2],
                            [2, 2, 1],
                            [3, 1, 3],
                            [3, 4, 5],
                            [5, 5, 5],
                            [5, 6, 7]])

    def test_pareto_compare_strong(self):
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[0], self.arr[0]), 0)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[0], self.arr[3]), -1)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[3], self.arr[4]), 0)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[[0, 1]], self.arr[3]), -1)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[2], self.arr[[0, 1]]), 0)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[[0, 1, 2]], self.arr[[3, 4]]), -1)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[[0, 1, 2]], self.arr[[0, 1]]), 0)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[[3, 4]], self.arr[[0, 1]]), 1)
        self.assertEqual(NonDominatedSort.pareto_compare_strong(self.arr[0], self.arr[1]), 0)

if __name__ == '__main__':
    unittest.main()
