import numpy as np
from non_dom_sort import NonDominatedSort
import timeit

if __name__ == '__main__':
    print('starting')
    nds = NonDominatedSort(np.array([[0, 3, 2],
                                     [2, 2, 1],
                                     [3, 1, 3],
                                     [3, 4, 5],
                                     [5, 5, 5],
                                     [5, 6, 7],

                                     ]))

    sort1 = nds.sort(reverse=False, strong=True, verbose=True)
    sort2 = nds.sort(reverse=True, verbose=True)
    sort3 = nds.sort(reverse=True, strong=False, verbose=True)
    sort4 = nds.sort(strong=False, verbose=True)
    sort5 = nds.sort(reverse=True, strong=False, n_rank=1, n_rest=2, verbose=True)

    nds2 = NonDominatedSort(np.concatenate([np.random.randint(3, size=(10, 50)),
                                            np.random.randint(low=1, high=6, size=(15, 50)),
                                            np.random.randint(low=7, high=20, size=(50, 50))]))

    idx2 = nds2.sort(reverse=True, n_rank=1, n_rest=5, strong=True, verbose=True)

    nds3 = NonDominatedSort(np.concatenate([np.random.randint(30, size=(100, 5000)),
                                            np.random.randint(low=31, high=60, size=(150, 5000)),
                                            np.random.randint(low=61, high=200, size=(500, 5000))]))

    print(f"the sorting needed: {timeit.timeit(nds3.sort, globals=globals(), number=1)} seconds")
    # takes around 5 seconds to sort the big arrays

    nds4 = NonDominatedSort(np.concatenate([np.random.randint(100, size=(1000, 3)),
                                            np.random.randint(low=31, high=60, size=(1500, 3)),
                                            np.random.randint(low=61, high=200, size=(5000, 3))]))

    print(f"the sorting needed: {timeit.timeit(nds4.sort, globals=globals(), number=1)} seconds")
    # takes around 3.6 seconds to sort a high number of small arrays
