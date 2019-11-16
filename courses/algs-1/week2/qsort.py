''' Quicksort!
'''

import sys


def load_data(filename):
    with open(filename) as stream:
        lines = stream.readlines()
    return [int(x.strip()) for x in lines if len(x.strip()) > 0]


def choose_pivot(array):
    # First version, use 1st entry.
    #return array[0]

    # Second version, use last entry.
    #return array[-1]

    # Third version, use middle value of 1st, last, middle.
    length = len(array)
    if length % 2 == 0:
        mid = len(array) / 2 - 1
    else:
        mid = len(array) / 2
    v = [array[0], array[-1], array[mid]]
    v.sort()
    return v[1]


def partition(array, left, right):
    pivot = array[left]
    i = left + 1

    for j in range(left + 1, right):
        if array[j] < pivot:
            array[j], array[i] = array[i], array[j]
            i += 1
    array[left], array[i - 1] = array[i - 1], array[left]


def quicksort(array, left=None, right=None):
    if left is None:
        left = 0
    if right is None:
        right = len(array)

    chunk = array[left:right]
    length = len(chunk)

    if length < 2:
        return 0

    p = choose_pivot(chunk)
    p_idx = array.index(p)

    # Stash the pivot as the first item in the array.
    if p_idx != left:
        array[left], array[p_idx] = array[p_idx], array[left]

    partition(array, left, right)
    p_idx = array.index(p)

    counter = len(array[left:left + p_idx - left])
    counter += quicksort(array, left, left + p_idx - left)
    counter += len(array[left + p_idx + 1 - left:right])
    counter += quicksort(array, left + p_idx + 1 - left, right)

    return counter

def main(argv):
    for arg in argv:
        int_array = load_data(arg)
        print "%s has %s entries" % (arg, len(int_array))
        count = quicksort(int_array)
        print "--> %s comparisons" % (count)

    #a = [3, 8, 2, 5, 1, 4, 7, 6]
    #count = quicksort(a)
    #print a, count

if __name__ == "__main__":
    main(sys.argv[1:])
