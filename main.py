import numpy as np
from itertools import product


class NonDominatedSort:

    def __init__(self, array: np.ndarray):
        self.array = array
        self.index_list = list(range(len(self.array)))

    @staticmethod
    def pareto_compare_strong(x: np.ndarray, y: np.ndarray):

        ndim_x = x.ndim
        ndim_y = y.ndim

        if (ndim_x == 1) & (ndim_y == 1):

            if np.all(x > y):
                return 1
            elif np.all(y > x):
                return -1
            else:
                return 0
        elif ndim_x == 1:
            comp_left = np.any(np.array([np.all(x > y_col) for y_col in y]))
            comp_right = np.any(np.array([np.all(x < y_col) for y_col in y]))

            if comp_left:
                return 1
            elif comp_right:
                return -1
            else:
                return 0

        elif ndim_y == 1:
            comp_left = np.any(np.array([np.all(x_col > y) for x_col in x]))
            comp_right = np.any(np.array([np.all(x_col < y) for x_col in x]))

            if comp_left:
                return 1
            elif comp_right:
                return -1
            else:
                return 0
        else:
            comp_left = np.any(np.array([np.all(x_col > y_col) for x_col, y_col in product(x, y)]))
            comp_right = np.any(np.array([np.all(x_col < y_col) for x_col, y_col in product(x, y)]))

            if comp_left:
                return 1
            elif comp_right:
                return -1
            else:
                return 0

    def merge_sort(self, index_list):

        if len(index_list) > 1:

            #  mid is the point where the array is divided into two subarrays
            mid = len(index_list) // 2
            le = index_list[:mid]
            ri = index_list[mid:]



            # Sort the two halves
            le = self.merge_sort(le)
            ri = self.merge_sort(ri)

            new_index_list = [None] * (len(le) + len(ri))

            i = j = k = 0

            # Until we reach either end of either L or M, pick larger among
            # elements L and M and place them in the correct position at A[p..r]
            while (i < len(le)) and (j < len(ri)):
                if self.pareto_compare_strong(self.array[le[i]], self.array[ri[j]]) == -1:
                    new_index_list[k] = le[i]
                    i += 1
                elif self.pareto_compare_strong(self.array[le[i]], self.array[ri[j]]) == 1:
                    new_index_list[k] = ri[j]
                    j += 1
                else:
                    if (type(le[i]) != list) & (type(ri[j]) != list):
                        to_insert = [le[i], ri[j]]
                    elif type(le[i]) != list:
                        to_insert = [*ri[j], le[i]]
                    elif type(ri[j]) != list:
                        to_insert = [*le[i], ri[j]]
                    else:
                        to_insert = [*le[i], *ri[j]]

                    new_index_list[k] = to_insert
                    i += 1
                    j += 1

                k += 1

            # When we run out of elements in either L or M,
            # pick up the remaining elements and put in A[p..r]
            while i < len(le):
                new_index_list[k] = le[i]
                i += 1
                k += 1

            while j < len(ri):
                new_index_list[k] = ri[j]
                j += 1
                k += 1

            new_index_list = [x for x in new_index_list if x is not None]

            return new_index_list

        else:

            return index_list


if __name__ == '__main__':
    print('starting')
    nds = NonDominatedSort(np.array([[0, 3, 2],
                                     [1, 1, 3],
                                     [2, 2, 1],
                                     [2, 1, 3],
                                     [3, 4, 5],
                                     [5, 5, 5],
                                     [5, 6, 7],

                                     ]))

    idx = nds.merge_sort(nds.index_list)
    print(idx)

    nds2 = NonDominatedSort(np.concatenate([np.random.randint(3, size=(10, 50)),
                                           np.random.randint(low=1,high=6,size=(15,50)),
                                           np.random.randint(low=7,high=20,size=(50,50))]))
    idx2 = nds2.merge_sort(nds2.index_list)

print(idx2)
