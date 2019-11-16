''' Calculate # of inversions in an array of integers.
'''

import sys

def load_data(filename):
    with open(filename) as stream:
        lines = stream.readlines()
    return [int(x.strip()) for x in lines if len(x.strip()) > 0]

def count_inv(an_array):
    (result, count) = inv_sort(an_array)
    return count

def inv_sort(an_array, count=0):
    if len(an_array) == 1:
        return (an_array, count)

    half = len(an_array) / 2
    left = an_array[:half]
    right = an_array[half:]

    (sorted_left, count) = inv_sort(left, count)
    (sorted_right, count) = inv_sort(right, count)

    return merge(sorted_left, sorted_right, count)

def merge(left, right, count):
    max = len(left) + len(right)
    i = 0
    j = 0
    result = []

    while len(result) < max:
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:  # left[i] >= right[j]
            result.append(right[j])
            j += 1
            count += len(left) - i

        if i == len(left):
            result += right[j:]
        if j == len(right):
            result += left[i:]

    return (result, count)

def main(argv):
    for arg in argv:
        int_array = load_data(arg)
        inversions = count_inv(int_array)
        print "%s: %s" % (arg, inversions)

if __name__ == "__main__":
    main(sys.argv[1:])
