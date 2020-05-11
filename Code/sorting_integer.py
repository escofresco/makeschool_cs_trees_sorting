#!python
from collections import deque

from sorting_iterative import insertion_sort

def counting_sort(numbers):
    """Sort given numbers (integers) by counting occurrences of each number,
    then looping over counts and copying that many numbers into output list.
    Running time: O(n + (max(n) - min(n)))
    Memory usage: O(n + (max(n) - min(n)))"""

    if len(numbers) < 2:
        ## Already sorted
        return numbers
    min_ = float('inf')
    max_ = float('-inf')

    for num in numbers:
        min_ = min(min_, num)
        max_ = max(max_, num)
    counts = [0] * (max_ - min_ + 1)

    for number in numbers:
        counts[number - min_] += 1
    new_numbers = []

    for i, count in enumerate(counts):
        new_numbers.extend([i + min_]*count)
    numbers[:] = new_numbers

def bucket_sort(numbers, num_buckets=10):
    """Sort given numbers by distributing into buckets representing subranges,
    then sorting each bucket and concatenating all buckets in sorted order.
    Running time:   O( (n/k)^2 * k) ) = O(n^2 / k)
                    –> k is the number of buckets
                    Buckets have size n/k. Insertion sort is quadratic in
                    the worst cast, therefore each bucket has (n/k)^2 runtime.
    Memory usage:   O(n)"""
    buckets = [deque() for _ in range(num_buckets)]
    smallest = float('inf')
    largest = float('-inf')

    for number in numbers:
        smallest = min(smallest, number)
        largest = max(largest, number)

    for i, number in enumerate(numbers):
        buckets[number // num_buckets].appendleft(number)

    res = []
    for bucket in buckets:
        insertion_sort(bucket)
        res.extend(bucket)
    numbers[:] = res
