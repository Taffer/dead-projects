#!/usr/bin/python
# -*- coding: utf-8 -*-
''' Algs 2, Week 4:

In this assignment you will implement one or more algorithms for the all-pairs
shortest-path problem. Here are data files describing three graphs: graph #1;
graph #2; graph #3.

The first line indicates the number of vertices and edges, respectively. Each
subsequent line describes an edge (the first two numbers are its tail and head,
respectively) and its length (the third number). NOTE: some of the edge lengths
are negative. NOTE: These graphs may or may not have negative-cost cycles.

Your task is to compute the "shortest shortest path". Precisely, you must first
identify which, if any, of the three graphs have no negative cycles. For each
such graph, you should compute all-pairs shortest paths and remember the
smallest one (i.e., compute min u,v ∈ V d(u,v), where d(u,v) denotes the
shortest-path distance from u to v).

If each of the three graphs has a negative-cost cycle, then enter "NULL" in the
box below. If exactly one graph has no negative-cost cycles, then enter the
length of its shortest shortest path in the box below. If two or more of the
graphs have no negative-cost cycles, then enter the smallest of the lengths of
their shortest shortest paths in the box below.
'''

import numpy
import sys


class Graph(object):
    def __init__(self, filename):
        ''' Load a Graph from the given file. '''
        self.num_vertices = 0
        self.num_edges = 0
        self.vertices = {}  # vertex # : [vertexes it points to]
        self.edges = {}  # (u, v): cost

        with open(filename) as g_file:
            for line in g_file.readlines():
                if line[0] == '#':
                    continue
                if len(line.strip()) == 0:
                    continue

                parts = line.split()
                if len(parts) == 2 and self.num_vertices == 0 and self.num_edges == 0:
                    self.num_vertices = int(parts[0])
                    self.num_edges = int(parts[1])
                elif len(parts) == 3:
                    tail = int(parts[0])
                    head = int(parts[1])
                    cost = int(parts[2])

                    if tail not in self.vertices:
                        self.vertices[tail] = []
                    if head not in self.vertices:
                        self.vertices[head] = []

                    self.vertices[tail].append(head)
                    self.edges[(tail, head)] = cost
                else:
                    raise ValueError("Can't parse line: %s" % (line))

            if len(self.vertices) != self.num_vertices:
                raise ValueError('Expected %s vertices but got %s' % (self.num_vertices, len(self.vertices)))
            if len(self.edges) != self.num_edges:
                raise ValueError('Expected %s edges but got %s' % (self.num_edges, len(self.edges)))

    def apsp_min(self):
        ''' Computer all-pairs shortest paths for the graph.

        Rather than mucking about with floats and "real" infinity, we'll just
        use None to mean Infinity.
        '''
        n = self.num_vertices + 1  # Python's 0-based, but our data is 1-based.
        #A = numpy.zeros((n, n, n), dtype=int)
        A_k = numpy.zeros((n, n), dtype=int)
        A_prev = numpy.zeros((n, n), dtype=int)

        # NB: A's first index is k (that is A[k][i][j]).

        # Initialize A.
        for i in xrange(1, n):
            for j in xrange(1, n):
                if i == j:
                    #A[0][i][j] = 0
                    A_prev[i][j] = 0
                elif (i, j) in self.edges:
                    #A[0][i][j] = self.edges[(i, j)]
                    A_prev[i][j] = self.edges[(i, j)]
                else:
                    #A[0][i][j] = sys.maxint
                    A_prev[i][j] = sys.maxint

        # Chug through the data.
        for k in xrange(1, n):
            for i in xrange(1, n):
                for j in xrange(1, n):
                    #c1 = A[k - 1][i][j]
                    #f1 = A[k - 1][i][k]
                    #f2 = A[k - 1][k][j]
                    c1 = A_prev[i][j]
                    f1 = A_prev[i][k]
                    f2 = A_prev[k][j]
                    if f1 == sys.maxint or f2 == sys.maxint:
                        c2 = sys.maxint
                    else:
                        c2 = f1 + f2
                    #A[i][j][k] = min(A[i][j][k - 1], A[i][k][k - 1] + A[k][j][k - 1])
                    A_k[i][j] = min(c1, c2)

            A_prev = A_k

        # Check for negative-cost cycles.
        for i in xrange(1, n):
            if A_k[i][i] < 0:
                return 'Negative-cost Cycle'

        # A[i][j][-1] = result for all
        result = min([min(x) for x in A_k])

        return result


def main(args):
    ''' Find the shortest of the shortest paths, or identify a negative-cost cycle. '''
    for filename in args:
        G = Graph(filename)
        print 'In %s, G has %s vertices and %s edges' % (filename, G.num_vertices, G.num_edges)
        min_path = G.apsp_min()
        print 'Minimum path in G is: %s' % (min_path)


if __name__ == '__main__':
    main(sys.argv[1:])
