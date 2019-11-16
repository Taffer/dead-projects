#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
In this assignment you will implement one or more algorithms for the travelling
salesman problem, such as the dynamic programming algorithm covered in the
video lectures. Here is a data file describing a TSP instance. The first line
indicates the number of cities. Each city is a point in the plane, and each
subsequent line indicates the x- and y-coordinates of a single city.

The distance between two cities is defined as the Euclidean distance --- that
is, two cities at locations (x,y) and (z,w) have distance (xâˆ’z)2+(yâˆ’w)2
between them. [That is, square root of (x - z)^2 + (y - w)^2.]

In the box below, type in the minimum cost of a travelling salesman tour for
this instance, rounded down to the nearest integer.

OPTIONAL: If you want bigger data sets to play with, check out the TSP
instances from around the world here. The smallest data set (Western Sahara)
has 29 cities, and most of the data sets are much bigger than that. What's the
largest of these data sets that you're able to solve --- using dynamic
programming or, if you like, a completely different method?

HINT: You might experiment with ways to reduce the data set size. For example,
trying plotting the points. Can you infer any structure of the optimal
solution? Can you use that structure to speed up your algorithm?
'''

import itertools
import math
import numpy
import sys


class Traveller(object):
    ''' Travelling Salesperson Problem implementation '''
    def __init__(self, filename):
        ''' Load TSP data from filename. '''
        self.cities = []  # list of (x, y) co-ords
        self.distances = {}  # (city index 1, city index 2): distance

        num_cities = 0
        with open(filename) as tsp_file:
            for line in tsp_file.readlines():
                if line[0] == '#':
                    continue
                if len(line.strip()) == 0:
                    continue

                parts = line.split()
                if len(parts) == 1 and num_cities == 0:
                    num_cities = int(parts[0])
                elif len(parts) == 2:
                    self.cities.append((float(parts[0]), float(parts[1])))
                else:
                    raise ValueError("Can't parse line: %s" % (line))

        if len(self.cities) != num_cities:
            raise ValueError('Expected %s cities but found %s' % (num_cities, len(self.cities)))

    def distance(self, index_1, index_2):
        ''' Calculate the distance between city1 and city2. '''
        if (index_1, index_2) in self.distances:
            return self.distances[(index_1, index_2)]

        city1 = self.cities[index_1]
        city2 = self.cities[index_2]

        result = math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

        self.distances[(index_1, index_2)] = result

        return result

    def subsets(self, src, length):
        ''' Return all subsets of the set of cities, all must contain city src, with specified length. '''
        return [x for x in itertools.combinations(range(len(self.cities)), length) if src in x]

    def tsp(self):
        ''' Compute the minimum cost of the TSP tour. '''
        n = len(self.cities)

        A_prev = {}  # A[subset] = list of [0 .. n] destinations

        subsets = self.subsets(0, 1)
        s = subsets[0]

        # Set up base case.
        A_prev[s] = numpy.repeat(numpy.inf, n)
        A_prev[s][0] = 0.0

        # Work it.
        for m in range(2, n + 1):
            print 'm = %s' % (m)

            A = {}
            sets = self.subsets(0, m)
            for s in sets:
                A[s] = numpy.repeat(numpy.inf, n)

                for j in [x for x in s if x != 0]:
                    jless_s = list(s[:])
                    jless_s.remove(j)
                    jless_s = tuple(jless_s)

                    distances = []
                    for k in jless_s:
                        delta = A_prev[jless_s][k] + self.distance(k, j)
                        distances.append(delta)

                    #A[s][j] = min([(A[jless_s][k] + self.distance(k, j)) for k in s if k != j])
                    A[s][j] = min(distances)

            del(A_prev)
            A_prev = A

        results = []
        sets = self.subsets(0, n)
        for j in range(1, n):
            results.append(A[sets[0]][j] + self.distance(j, 0))

        result = min(results)

        try:
            return int(result)  # returns floor(result) as an integer
        except OverflowError:
            return 'inf'


def main(args):
    for filename in args:
        tsp = Traveller(filename)
        print '%s has %s cities' % (filename, len(tsp.cities))

        result = tsp.tsp()
        print '=> shortest tour: %s' % (result)


if __name__ == '__main__':
    main(sys.argv[1:])
