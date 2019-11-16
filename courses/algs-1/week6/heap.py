#!/usr/bin/env python
''' Median Maintenance problem.
'''

import heapq
import sys


def load_ints(filename):
    ''' Load an array of ints from the given filename.
    '''
    int_array = []

    with open(filename) as a_file:
        line = a_file.readline()
        while line:
            if line[0] != '#':
                int_array.append(int(line))
            line = a_file.readline()

    return int_array


class MinHeap(object):
    ''' Heap supporting extract-minimum.
    '''
    def __init__(self):
        self.heap = []

    def insert(self, x):
        heapq.heappush(self.heap, x)

    def extract(self):
        return heapq.heappop(self.heap)

    def peek(self):
        return self.heap[0]

    def len(self):
        return len(self.heap)


class MaxHeap(object):
    ''' Heap supporting extract-maximum.
    '''
    def __init__(self):
        self.heap = []

    def insert(self, x):
        heapq.heappush(self.heap, -x)

    def extract(self):
        return -heapq.heappop(self.heap)

    def peek(self):
        return -self.heap[0]

    def len(self):
        return len(self.heap)


def median_heap(int_array):
    ''' Do the median maintenance bit.
    '''
    heap_low = MaxHeap()
    heap_high = MinHeap()
    medians = 0
    for x in int_array:
        # Put x into a heap.
        if heap_low.len() > 0 and x <= heap_low.peek():
            heap_low.insert(x)
        else:
            heap_high.insert(x)

        # Rebalance if necessary.
        delta = heap_low.len() - heap_high.len()
        if delta > 1:
            # Take one from low, add to high.
            tmp = heap_low.extract()
            heap_high.insert(tmp)
        elif delta < -1:
            # Take one from high, add to low.
            tmp = heap_high.extract()
            heap_low.insert(tmp)
        else:
            # Delta is 1, 0, -1, we're OK.
            pass

        # Where's the median?
        delta = heap_low.len() - heap_high.len()
        if delta == 1 or delta == 0:
            medians += heap_low.peek()
        elif delta == -1:
            medians += heap_high.peek()
        else:
            raise ValueError('delta confusing me: %s' % (delta))

    return medians


def main(argv):
    ''' Mainline!
    '''
    for arg in argv:
        all_ints = load_ints(arg)
        result = median_heap(all_ints)

        print 'result = %s, mod 10000 = %s' % (result, result % 10000)

if __name__ == "__main__":
    main(sys.argv[1:])
