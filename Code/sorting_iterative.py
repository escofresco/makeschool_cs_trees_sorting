#!python
from collections import namedtuple

def is_sorted(items):
    """Return a boolean indicating whether given items are in sorted order.
    Running time:   O(n) Every item has to be compared to guaratee that it's
                    sorted.
    Memory usage:   Θ(1) The number of variables doesn't change with the size
                    of the input."""
    for i in range(0, len(items)-1):
        ## Go through every 2 elements
        if items[i] > items[i+1]:
            ## Descending pair
            return False
    return True # Strictly ascending


def bubble_sort(items):
    """Sort given items by swapping adjacent items that are out of order, and
    repeating until all items are in sorted order.
    Running time:   O(n^2) When items is descending, this will be at most
                    quadratic, but the function will exit once a sorted
                    permutation is found.
    Memory usage:   Θ(1) Swapping is done in-place."""
    is_sorted = True # items is assumed sorted by default
    cur_index = 0

    while True:
        ## Continue making passes through items until it ends up sorted.
        if cur_index >= len(items) - 1:
            ## The end of items has been reached
            if is_sorted:
                ## Descending pair not found, so items is sorted.
                return
            is_sorted = True # reset to default
            cur_index = 0 # reset to beginning

        if items[cur_index+1] < items[cur_index]:
            ## Descending pair
            is_sorted = False
            items[cur_index], items[cur_index+1] = (items[cur_index+1],
                                                    items[cur_index])
        cur_index += 1



def selection_sort(items):
    """Sort given items by finding minimum item, swapping it with first
    unsorted item, and repeating until all items are in sorted order.
    Running time:   Θ(n^2) The number of comparisons doesn't change for
                    different permutations of items – it's strictly quadratic.
    Memory usage:   Θ(1) Swapping is done in-place."""
    MinElm = namedtuple('MinElm', 'index key')

    for i, elm in enumerate(items):
        ## Maintain selection sort invariant by using i to partition items
        ## into sorted on the left, unsorted on the right
        # Track min on right half of partition
        next_min = MinElm(i, elm)

        for j in range(i+1, len(items)):
            ## Find the next min in unsorted items
            # Update next_min
            next_min = min(MinElm(j, items[j]), next_min, key=lambda o:o.key)
        # Swap partition element with next minimum element
        items[i], items[next_min.index] = items[next_min.index], items[i]


def insertion_sort(items):
    """Sort given items by taking first unsorted item, inserting it in sorted
    order in front of items, and repeating until all items are in order.
    Running time:   O(n^2) When items is descending, every element must be
                    inserted into the first position.
    Memory usage:   Θ(1) Sorting is done in-place."""

    for i in range(1, len(items)):
        ## Go through every yet-to-be-sorted element, inserting into
        ## the sorted array up to i

        while i > 0 and items[i] < items[i-1]:
            items[i], items[i-1] = items[i-1], items[i] # Bubble down
            i -= 1

def merge(items, start, end, subarray_size):
    """Merges two sorted subarrays in items, given the start of the first
    subarray and the end of the second."""
    mid = start + subarray_size
    assert is_sorted(items[start:mid])
    assert is_sorted(items[start+subarray_size:end])

    aux = []
    i = start
    j = mid

    while i < mid and j < end:
        if items[i] < items[j]:
            aux.append(items[i])
            i += 1
        else:
            aux.append(items[j])
            j += 1
    aux.extend(items[i:mid] or items[j:end])
    assert is_sorted(aux)

    ## Overwrite elements in subarrays in their correctly sorted order
    for i in range(start, end):
        items[i] = aux[i-start]


def bottom_up_merge_sort(items):
    """Bottom-up merge sort takes lgn passes to sort subarrays of doubling size,
    while there's a final subarray equalling the size of items.
    """
    subarray_size = 1

    while subarray_size < len(items)//2:
        ## Continue making passes through items until the subarray size is
        ## the size of items, since this means items is finally sorted.
        for i in range(0, len(items), subarray_size):
            merge(items, i, i+subarray_size*2, subarray_size)
        subarray_size *= 2
