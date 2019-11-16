#!/usr/bin/env python
'''
In this programming problem you'll code up Prim's minimum spanning tree
algorithm. Download the text file here. This file describes an undirected
graph with integer edge costs. It has the format

[number_of_nodes] [number_of_edges]
[one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]
[one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]
...
For example, the third line of the file is "2 3 -8874", indicating that there
is an edge connecting vertex #2 and vertex #3 that has cost -8874. You should
NOT assume that edge costs are positive, nor should you assume that they are
distinct.

Your task is to run Prim's minimum spanning tree algorithm on this graph. You
should report the overall cost of a minimum spanning tree --- an integer, which
may or may not be negative --- in the box below.

IMPLEMENTATION NOTES: This graph is small enough that the straightforward O(mn)
time implementation of Prim's algorithm should work fine. OPTIONAL: For those
of you seeking an additional challenge, try implementing a heap-based version.
The simpler approach, which should already give you a healthy speed-up, is to
maintain relevant edges in a heap (with keys = edge costs). The superior
approach stores the unprocessed vertices in the heap, as described in lecture.
Note this requires a heap that supports deletions, and you'll probably need to
maintain some kind of mapping between vertices and their positions in the heap.
'''

import heapq
import random
import sys


class Edge(object):
    ''' Edge with weight. '''
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight

    def __repr__(self):
        return '(%s, %s) %s' % (self.u, self.v, self.weight)

    def opposite(self):
        ''' Return an edge with u,v swapped. '''
        return Edge(self.v, self.u, self.weight)


class WeightedGraph(object):
    ''' Weighted graph.
    '''

    def __init__(self, source):
        ''' Create a weighted graph from the source path.
        '''
        self.vertices = []
        self.edges = []

        self.load_data(source)

    def __str__(self):
        return '''vertices: %s\nedges: %s''' % (self.vertices, self.edges)

    def load_data(self, filename):
        ''' Load data from the specified filename.
        '''
        num_nodes = 0
        num_edges = 0
        found_edges = 0

        with open(filename) as a_file:
            # Each line is:
            #
            # [number_of_nodes] [number_of_edges]
            # [one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]
            # [one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]
            for line in a_file.readlines():
                if line[0] != '#':
                    parts = line.split()

                    if len(parts) == 2:
                        if num_nodes != 0:
                            raise ValueError('Got number of nodes and edges again: %s' % (line))
                        num_nodes = int(parts[0])
                        num_edges = int(parts[1])

                    elif len(parts) == 3:
                        found_edges += 1

                        head_vertex = int(parts[0])
                        tail_vertex = int(parts[1])
                        weight = int(parts[2])

                        if head_vertex not in self.vertices:
                            self.vertices.append(head_vertex)
                        if tail_vertex not in self.vertices:
                            self.vertices.append(tail_vertex)

                        self.edges.append(Edge(head_vertex, tail_vertex, weight))

        found_nodes = len(self.vertices)
        if num_nodes != found_nodes:
            raise ValueError('Expected %s nodes, got %s' % (num_nodes, found_nodes))
        if num_edges != found_edges:
            raise ValueError('Expected %s edges, got %s' % (num_edges, found_edges))

    def find_cheapest(self, edges, seen):
        ''' Find the cheapest edge starting in seen and ending outside of seen. '''
        cheapest = None
        for edge in edges:
            swapped = edge.opposite()
            if edge.u in seen and edge.v not in seen:
                if cheapest is None:
                    cheapest = edge
                elif edge.weight < cheapest.weight:
                    cheapest = edge
            elif swapped.u in seen and swapped.v not in seen:
                if cheapest is None:
                    cheapest = swapped
                elif swapped.weight < cheapest.weight:
                    cheapest = swapped

        if cheapest is None:
            raise ValueError('Disconnected graph, get in the car!')

        return cheapest

    def prims(self):
        ''' Run Prim's algorithm over the graph to find a minimum spanning tree.

        Returns total cost of the MST.

        Prim's MST Algorithm
        - initialize X = [s] (s exists in V, chosen arbitrarily)
        - initialize T = [] (invariant: X is the set of vertices spanned by tree-so-far T)
        - while X <> V: (until all vertices are spanned)
             - let e = (u,v) be the cheapest edge of G with u in X and v outside of X
             - add e to T
             - add v to X

        Invariant #1 - elements in heap = vertices that aren't currently spanned (V - X)
        Invariant #2 - for v in V - X, key[v] = cheapest edge (u,v) with u in X
        Maintaining Invariant #2
        Issue: might need to recompute some keys to maintain Invariant #2 after each extract_min()
        Pseudocode:
        - when v added to X:
             - for each edge (v, w) in E:
                  - if w in V - X:
                       - delete w from heap
                       - recompute key[w] = min( key[w], Cvw )
                       - re-insert key[w] into the heap

        '''
        X = [random.choice(self.vertices)]  # start with a random vertex
        T = []
        while len(X) != len(self.vertices):
            # Find cheapest edge of G with u in X and v outside of X
            cheapest = self.find_cheapest(self.edges, X)

            T.append(cheapest)
            X.append(cheapest.v)

        print 'X: %s' % (X)
        print 'T: %s' % (T)

        total = 0
        for edge in T:
            total += edge.weight

        return total


def main(args):
    for filename in args:
        graph = WeightedGraph(filename)
        print '%s: %s' % (filename, graph.prims())


if __name__ == '__main__':
    main(sys.argv[1:])
