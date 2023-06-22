from itertools import product
from itertools import chain
import numpy as np


class NonDominatedSort:

    def __init__(self, array: np.ndarray):
        self.array = array
        self.index_list = list(range(len(self.array)))
        self.pareto_compare = self.pareto_compare_strong
        self.reverse = False

    @staticmethod
    def pareto_compare_strong(x: np.ndarray, y: np.ndarray):

        """ this function applies the strong pareto dominance logic and checks whether two vectors, or two sets of
        vectors dominate one another or not. returns 0 if vectors are indifferent, 1 or -1 if one of the inputs
        strongly dominates"""

        ndim_x = x.ndim
        ndim_y = y.ndim

        # one to one, one to many, and many to many cases, in the case that different forms of vector comparisons
        # are required
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

    @staticmethod
    def pareto_compare_weak(x: np.ndarray, y: np.ndarray):

        """ this function applies the weak pareto dominance logic and checks whether two vectors, or two sets of
        vectors dominate one another or not. returns 0 if vectors are indifferent, 1 or -1 if one of the inputs
        weakly dominates"""

        ndim_x = x.ndim
        ndim_y = y.ndim

        # one to one, one to many, and many to many cases, in the case that different forms of vector comparisons
        # are required
        if (ndim_x == 1) & (ndim_y == 1):

            if np.all(x >= y) and np.any(x > y):
                return 1
            elif np.all(y >= x) and np.any(y > x):
                return -1
            else:
                return 0

        elif ndim_x == 1:
            comp_left = np.any(np.array([(np.all(x >= y_col) and np.any(x > y_col)) for y_col in y]))
            comp_right = np.any(np.array([(np.all(x <= y_col) and np.any(x < y_col)) for y_col in y]))

            if comp_left:
                return 1
            elif comp_right:
                return -1
            else:
                return 0

        elif ndim_y == 1:
            comp_left = np.any(np.array([(np.all(x_col >= y) and np.any(x_col > y)) for x_col in x]))
            comp_right = np.any(np.array([(np.all(x_col <= y) and np.any(x_col < y)) for x_col in x]))

            if comp_left:
                return 1
            elif comp_right:
                return -1
            else:
                return 0
        else:
            comp_left = np.any(
                np.array([(np.all(x_col >= y_col) and np.any(x_col > y_col)) for x_col, y_col in product(x, y)]))
            comp_right = np.any(
                np.array([(np.all(x_col <= y_col) and np.any(x_col < y_col)) for x_col, y_col in product(x, y)]))

            if comp_left:
                return 1
            elif comp_right:
                return -1
            else:
                return 0

    def __merge_sort(self, index_list):

        """Implements a modified merge sort algorithm for the custom ranking relation and in the case merging of
        indices to create pareto frontiers are required. Works recursively as the default merge sort algorithm, but
        returns the sub-arrays instead of modifying them in place"""

        if len(index_list) > 1:

            mid = len(index_list) // 2
            le = index_list[:mid]
            ri = index_list[mid:]

            le = self.__merge_sort(le)
            ri = self.__merge_sort(ri)

            new_index_list = [None] * (len(le) + len(ri))

            i = j = k = 0

            while (i < len(le)) and (j < len(ri)):
                if self.pareto_compare(self.array[le[i]], self.array[ri[j]]) == -1:
                    if self.reverse:
                        new_index_list[k] = ri[j]
                        j += 1
                    else:
                        new_index_list[k] = le[i]
                        i += 1
                elif self.pareto_compare(self.array[le[i]], self.array[ri[j]]) == 1:
                    if self.reverse:
                        new_index_list[k] = le[i]
                        i += 1
                    else:
                        new_index_list[k] = ri[j]
                        j += 1

                else:
                    # makes sure that correct assignments are made, we want to be able to insert lists
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

            while i < len(le):
                new_index_list[k] = le[i]
                i += 1
                k += 1

            while j < len(ri):
                new_index_list[k] = ri[j]
                j += 1
                k += 1

            # it is highly likely that the length of the index list is shorter after the operations
            new_index_list = [x for x in new_index_list if x is not None]

            return new_index_list

        else:

            return index_list

    def __check_rank_consistency(self, rank_a, rank_b):
        """Helper function required to check whether two sets should be merged or not, has a very specific use."""
        if self.pareto_compare(rank_a, rank_b) == 0:
            return False
        else:
            return True

    def sort(self, reverse=False, strong=True, n_rank=np.inf, n_rest=0, verbose=False):

        """Handles function arguments, does preprocessing and postprocessing of the index list
            reverse: True if minimization, False if maximization is desired
            strong: True for strong pareto dominance False for weak pareto dominance
            n_rank: number of pareto frontiers to return
            n_rest: number of remaining indices to return
            verbose: True if the user wants to see output on the console


            n_rank takes precedence over n_rest, if there are 3 ranks of pareto frontiers are found, if n_rank is 3,
            then_rest is ignored. Otherwise, returns the desired number of pareto frontiers and prints out the relevant
            information if verbose is set to True.

            The part that has nested if-else clauses makes sure that the correct number of remaining indices are given,
            It further makes sure that in the case of a split pareto frontier, the frontier consistency is maintained.

            An Example:
            Assume strong pareto dominance is required.

            frontier 1: [3 4 5]
            frontier 2: ([5,5,5],[5,6,7])

            In the case that [5,6,7] is removed due to a combination of n_rank and n_rest
            [3,4,5] and [5,5,5] have to be in the same frontier but without interference they can't be in the same
            frontier, postprocessing part makes sure that all the indices find themselves in the correct place in the end.


            """

        self.reverse = reverse
        self.pareto_compare = self.pareto_compare_strong if strong else self.pareto_compare_weak

        # This is where the actual sorting happens
        index_list = self.__merge_sort(self.index_list)
        index_list = [[x] if type(x) != list else x for x in index_list]

        max_number_of_ranks = len(index_list)

        if n_rank >= max_number_of_ranks:
            if verbose:
                print(f"Found {max_number_of_ranks} ranks, returning all of them.")
                print(f"The set of {n_rank} pareto frontier(s) is as follows: {index_list}")
                print('')

            return index_list
        else:

            rest = list(chain.from_iterable(index_list[n_rank:]))
            rest_ranks = index_list[n_rank:]
            if verbose:
                print(
                    f"Found {max_number_of_ranks} ranks and {len(rest)} rest but returning {n_rank}")

            if len(rest) >= n_rest:
                rest_new = []
                rest_length = len(rest_new)
                rest_idx = len(rest_ranks) - 1

                while (rest_length < n_rest) and (rest_idx >= 0):
                    length_to_add = len(rest_ranks[rest_idx])

                    if rest_length + length_to_add >= n_rest:
                        needed_count = n_rest - rest_length
                        needed_indices = [rest_ranks[rest_idx].pop() for x in range(needed_count)]
                        rest_new.append(needed_indices)

                        rest_length = sum([len(x) for x in rest_new])

                        check_consistency = self.__check_rank_consistency(
                            self.array[rest_ranks[rest_idx - 1]], self.array[rest_ranks[rest_idx]])

                        if (len(rest_ranks) > 1) and (not check_consistency):
                            rest_ranks[rest_idx - 1] = [*rest_ranks[rest_idx - 1], *rest_ranks[rest_idx]]
                            rest_ranks.pop(rest_idx)
                    else:

                        rest_new.append(rest_ranks.pop())
                        rest_length = len(rest_new)

                    rest_idx -= 1

                rest_new = list(chain.from_iterable(rest_new))
                index_list = index_list[:n_rank]
                index_list = [*index_list, *rest_ranks]

                rest_new
                if verbose:
                    print(f"The set of {n_rank} pareto frontier(s) is as follows: {index_list[:n_rank]}")
                    print(f'The sets that do not fit either description are: {rest_ranks}')
                    print(f'The rest of the indices are as follows: {rest_new}')
                    print('')

            else:
                if verbose:
                    print(f'Desired number of n_rest is greater than what is available, returning {len(rest)}')
                    print(f"The set of {n_rank} pareto frontier(s) is as follows: {index_list[:n_rank]}")
                    print(f'The rest of the indices are as follows: {rest}')
                    print('')

                index_list = index_list[:n_rank]

            return index_list
