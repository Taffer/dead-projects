#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on 2013-09-20

@author: chrish

In this programming problem and the next you'll code up the knapsack algorithm
from lecture. Let's start with a warm-up. Download the text file here. This
file describes a knapsack instance, and it has the following format:

[knapsack_size][number_of_items]
[value_1] [weight_1]
[value_2] [weight_2]
...
For example, the third line of the file is "50074 659", indicating that the
second item has value 50074 and size 659, respectively.

You can assume that all numbers are positive. You should assume that item
weights and the knapsack capacity are integers.

In the box below, type in the value of the optimal solution.

ADVICE: If you're not getting the correct answer, try debugging your algorithm
using some small test cases. And then post them to the discussion forum!

Q1 answer: 2493893
Q2 answer: 4243395
'''

import numpy
import sys


class Knapsack(object):
    def __init__(self, filename):
        self.data = []  # list of (value, size)
        self.capacity = 0
        self.items = 0

        self.load(filename)

    def load(self, filename):
        ''' Load knapsack data from the given file.

        :param filename: The file to load.
        '''
        with open(filename) as knapsack:
            for line in knapsack.readlines():
                if line[0] == '#':
                    continue

                parts = line.split()
                if len(parts) != 2:
                    raise ValueError("Can't parse line: %s" % (line))

                if self.capacity == 0:
                    self.capacity = int(parts[0])
                    self.items = int(parts[1])
                else:
                    self.data.append(tuple([int(x) for x in parts]))

        if self.items != len(self.data):
            raise ValueError('expected %s items but got %s' % (self.items, len(self.data)))

    def pack(self):
        ''' Pack the knapsack with the optimal collection of items. '''
        A = numpy.zeros((self.items, self.capacity), dtype=int)  # @UndefinedVariable
        for i in xrange(0, self.items):
            (value, weight) = self.data[i]
            for x in xrange(self.capacity):
                if weight > x:
                    A[i][x] = A[i - 1][x]
                else:
                    A[i][x] = max(A[i - 1][x], A[i - 1][x - weight] + value)
        return A[-1][-1]

    def big_pack(self):
        ''' Pack a huge knapsack. '''
        A_prev = numpy.zeros(self.capacity, dtype=int)  # previous line, A[i - 1] @UndefinedVariable
        for i in xrange(0, self.items):
            print i
            (value, weight) = self.data[i]
            A = numpy.zeros(self.capacity, dtype=int)  # current line, A @UndefinedVariable
            for x in xrange(self.capacity):
                if weight > x:
                    A[x] = A_prev[x]
                else:
                    A[x] = max(A_prev[x], A_prev[x - weight] + value)
            A_prev = A
        return A_prev[-1]


def main(args):
    import time
    for filename in args:
        sack = Knapsack(filename)
        print '%s has %s items and a capacity of %s' % (filename, sack.items, sack.capacity)
        try:
            start = time.time()
            value = sack.pack()
            delta = time.time() - start
            print 'max value: %s' % (value)
            print '%s seconds' % (delta)
        except Exception:
            print 'pack() failed'
        start = time.time()
        value = sack.big_pack()
        delta = time.time() - start
        print 'max value: %s' % (value)
        print '%s seconds' % (delta)


if __name__ == '__main__':
    main(sys.argv[1:])
