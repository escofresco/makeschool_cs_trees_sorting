#!python
from sorting_iterative import is_sorted, insertion_sort
#from sorting_iterative import merge_sort_it
from random import randint, shuffle

def merge(items1, items2):
    """Merge given lists of items, each assumed to already be in sorted order,
    and return a new list containing all items in sorted order.
    Running time:
    TODO: Memory usage: ??? Why and under what conditions?"""
    assert is_sorted(items1)
    assert is_sorted(items2)
    aux = []
    i = j = 0

    while i < len(items1) and j < len(items2):
        if items1[i] < items2[j]:
            aux.append(items1[i])
            i += 1
        else:
            aux.append(items2[j])
            j += 1
    aux.extend(items1[i:] or items2[j:])
    assert is_sorted(aux)
    return aux

def split_sort_merge(items):
    """Sort given items by splitting list into two approximately equal halves,
    sorting each with an iterative sorting algorithm, and merging results into
    a list in sorted order.
    Running time:   O(n^2) See insertion sort.
    Memory usage:   O(n) An auxiliar array is created for each merge. """
    left, right = items[:len(items)//2], items[len(items)//2:]
    insertion_sort(left)
    insertion_sort(right)
    items[:] = merge(left, right)


def merge_sort(items):
    """Sort given items by splitting list into two approximately equal halves,
    sorting each recursively, and merging results into a list in sorted order.
    TODO: Running time: ??? Why and under what conditions?
    TODO: Memory usage: ??? Why and under what conditions?"""

    if len(items) < 2:
        return

    # Split items list into approximately equal halves
    left, right = items[:len(items)//2], items[len(items)//2:]

    ## Merge both
    merge_sort(left)
    merge_sort(right)

    items[:] = merge(left, right)


def partition(items, low, high):
    """Return index `p` after in-place partitioning given items in range
    `[low...high]` by choosing a pivot randomly from
    that range, moving pivot into index `p`, items less than pivot into range
    `[low...p-1]`, and items greater than pivot into range `[p+1...high]`.
    Running time: O(high-low) Every element from low to high must be viewed.
    Memory usage: O(1) Elements are moved across pivot in-place."""
    # 4 5 5 2 95 20
    # ^   ^ ^
    #
    #
    # low = 0
    # high = 5
    ## Designate items[low] as pivot
    i = low+1
    j = high

    while True:

        while i < high+1 and items[i] <= items[low]:
            i += 1

        while j > low and items[j] > items[low]:
            j -= 1

        if j < i:
            break
        print(items, i, j)
        items[i], items[j] = items[j], items[i]
    items[low], items[j] = items[j], items[low]
    return j


def quick_sort(items, low=None, high=None):
    """Sort given items in place by partitioning items in range `[low...high]`
    around a pivot item and recursively sorting each remaining sublist range.
    Best case running time:     O(nlgn) When items is shuffled, it is partitioned
                                roughly in half each time.
    Worst case running time:    O(n^2) When items is in each because each
                                element will get partitioned.
    Memory usage:               O(1) Shuffling is done in-place. """

    if None in (low, high):
        #items[:] = list(set(items))
        #shuffle(items) # Make sure that pivots are placed randomly
        low = 0
        high = len(items) - 1

    if high <= low:
        ## Check if list or range is so small it's already sorted (base case)
        return
    # Partition items in-place around a pivot and get index of pivot
    pivot = partition(items, low, high)

    ## Sort each sublist range by recursively calling quick sort
    quick_sort(items, low, pivot-1)
    quick_sort(items, pivot+1, high)
