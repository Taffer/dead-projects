#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on 2013-09-15

@author: chrish

In this programming problem and the next you'll code up the clustering
algorithm from lecture for computing a max-spacing k-clustering. Download the
text file here. This file describes a distance function (equivalently, a
complete graph with edge costs). It has the following format:

[number_of_nodes]
[edge 1 node 1] [edge 1 node 2] [edge 1 cost]
[edge 2 node 1] [edge 2 node 2] [edge 2 cost]
...
There is one edge (i,j) for each choice of 1≤i<j≤n, where n is the number of
nodes. For example, the third line of the file is "1 3 5250", indicating that
the distance between nodes 1 and 3 (equivalently, the cost of the edge (1,3))
is 5250. You can assume that distances are positive, but you should NOT assume
that they are distinct.

Your task in this problem is to run the clustering algorithm from lecture on
this data set, where the target number k of clusters is set to 4. What is the
maximum spacing of a 4-clustering?

ADVICE: If you're not getting the correct answer, try debugging your algorithm
using some small test cases. And then post them to the discussion forum!
'''

import heapq
import sys
import uf


class Clusters(object):
    def __init__(self, filename):
        ''' Load clustering data from given file.

        :param filename: Name of the file.
        '''
        self.nodes = []  # list of nodes
        self.edges = []  # list of edges (u, v)
        self.costs = {}  # (u, v): cost for each edge, and (v, u): cost too

        self.load(filename)

    def cluster(self, k):
        ''' Cluster the nodes into k clusters.

        :param k: Number of clusters.
        '''
        # All nodes start in their own clusters.
        clusters = uf.UnionFind()
        clusters.insert_objects(self.nodes)  # The actual clusters.

        cost_heap = []
        for edge in self.edges:
            cost_heap.append((self.costs[edge], edge))
        heapq.heapify(cost_heap)

        while len(clusters.num_weights) > k:
            (_, (u, v)) = heapq.heappop(cost_heap)
            u_parent = clusters.find(u)
            v_parent = clusters.find(v)
            if u_parent != v_parent:
                clusters.union(u, v)

        return clusters

    def max_spacing(self, clusters):
        ''' Figure out the maximum spacing between these clusters.

        Since we're using Kruskal's, the spacing is the cost of the first
        edge we find with end points in different clusters. <-- hint from
        the forums.

        :param: k clusters from cluster()
        '''
        cost_heap = []
        for edge in self.edges:
            cost_heap.append((self.costs[edge], edge))
        heapq.heapify(cost_heap)

        while len(cost_heap) > 0:
            (cost, (u, v)) = heapq.heappop(cost_heap)
            u_parent = clusters.find(u)
            v_parent = clusters.find(v)
            if u_parent != v_parent:
                return cost

    def load(self, filename):
        ''' Load clustering data.

        :param filename: Source of data.
        '''
        num_nodes = 0

        with open(filename) as fp:
            x = 0
            for line in fp.readlines():
                if line[0] == '#':
                    continue
                parts = line.split()
                if len(parts) == 1:
                    if num_nodes == 0:
                        num_nodes = int(parts[0])
                    else:
                        raise ValueError('Found number of nodes again: %s' % (line))
                elif len(parts) == 3:
                    u = int(parts[0])
                    v = int(parts[1])
                    cost = int(parts[2])

                    if u not in self.nodes:
                        self.nodes.append(u)
                    if v not in self.nodes:
                        self.nodes.append(v)

                    self.costs[(u, v)] = cost
                    self.costs[(v, u)] = cost

                    if (u, v) not in self.edges:
                        self.edges.append((u, v))

                x += 1

                if x % 1000 == 0:
                    print x

        if len(self.nodes) != num_nodes:
            raise ValueError('Expected %s nodes, got %s' % (num_nodes, len(self.nodes)))


def main(args):
    for filename in args:
        lumpy = Clusters(filename)
        print 'Loaded %s nodes with %s edges from %s...' % (len(lumpy.nodes), len(lumpy.edges), filename)
        k_clusters = lumpy.cluster(4)
        print 'Max spacing: %s' % (lumpy.max_spacing(k_clusters))


if __name__ == '__main__':
    main(sys.argv[1:])
