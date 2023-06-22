# Non Dominated Sort

Hi!
The submission comes in three different files, main.py where several instances of sorting run and there are a few performance checks.
The only required package is numpy. I used a virtual environment for the project, and only numpy is in requirements.txt

non_dom_sort.py hosts the main class and all the associated functions.
tests.py has the unit tests that are integral to the functioning of the sorting algorithm.


## Approach

I chose to implement a divide-and-conquer approach and used a modified merge sort algorithm to do the actual sorting. But the important thing was 
to prudently define the comparison relation. We need to compare vectors and possibly set of vectors to find out wheter there is an indifference 
relationship or one side dominates the other.

Merge sort does what it usually does recursively but index lists had to change their sizes due to merging indices induced by the indifference relation (this is core considering the problem is about 
finding pareto frontiers, which are defined by indifference relations by definition)
These lists of indices were required to reference constant vector values and that's why I decided to implement a class to make sure that I had everything in place when I needed them.

numpy's any and all functions are particularly handy for providing fast and vectorized array comparisons. Hence the requirement to include numpy.

The nature of the problem gives rise to multiple possible solutions.

vector 0 = [0, 3, 2] \
vector 1 = [2, 2, 1] \
vector 2 = [3, 1, 3] \
vector 3 = [3, 4, 5] \
vector 4 = [5, 5, 5] \
vector 5 = [5, 6, 7] 


In our cute example, in the minimization case with strong pareto dominance both [0,1,2],[3],[4,5] and [0,1,2].[3,4],[5] are equivalent solutions.
But not [0,1,2],[3,4,5] since vector 3 dominates vector 5 but not vector 4, for this reason they can't be in the same frontier.

## Instructions

As it is merely a function and not a program itself, I didn't think it was necessary to use CLI to do the sorting, as it is most likely an intermediary function in a bigger process.
I used pyCharm to write, run and test the functions. So any IDE should be able to do the job.

The inputs are row based, since numpy is much easier to work with row based inputs when not taking them from an outside file or dataframe.

You can still do the tests on the command line though, simply by

```
python -m unittest tests.py 
```


## Results

The function handles pretty much everything quite well including desired keyword arguments like n_rest and n_rank.
there is some inefficiency concerning n_rest since I chose to post-process the sorted list and discount any unwanted elements.
It could be possible to seperate the n_rest during sorting, but the framework I used necessitated seperating them after the sorting happened.

in main.py you can try the function with larger arrays too. Considering it needs to compare big vectors a high number of times, it seems to perform satisfactorily.

