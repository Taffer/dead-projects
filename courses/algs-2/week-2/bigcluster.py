#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on 2013-09-15

@author: chrish

In this question your task is again to run the clustering algorithm from
lecture, but on a MUCH bigger graph. So big, in fact, that the distances (i.e.,
edge costs) are only defined implicitly, rather than being provided as an
explicit list.

The data set is here. The format is:
[# of nodes] [# of bits for each node's label]
[first bit of node 1] ... [last bit of node 1]
[first bit of node 2] ... [last bit of node 2]
...
For example, the third line of the file
"0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 1 0 1" denotes the 24 bits
associated with node #2.

The distance between two nodes u and v in this problem is defined as the
Hamming distance--- the number of differing bits --- between the two nodes'
labels. For example, the Hamming distance between the 24-bit label of node #2
above and the label "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1" is 3
(since they differ in the 3rd, 7th, and 21st bits).

The question is: what is the largest value of k such that there is a
k-clustering with spacing at least 3? That is, how many clusters are needed to
ensure that no pair of nodes with all but 2 bits in common get split into
different clusters?

NOTE: The graph implicitly defined by the data file is so big that you probably
can't write it out explicitly, let alone sort the edges by cost. So you will
have to be a little creative to complete this part of the question. For
example, is there some way you can identify the smallest distances without
explicitly looking at every pair of nodes?
'''

import sys
import uf


class Clusters(object):
    def __init__(self, filename):
        ''' Load clustering data from given file.

        self.nodes has the raw data (binary strings)
        self.points has the {value: [node numbers]}

        Since we're after all nodes within a Hamming distance of 2, we need to
        check all the nodes with a value with 1 or 2 bits different from the
        one we're looking at. There are ~300 to check each time. 24*23 / 2
        values to check each iteration.

        deltas = set()
        for bit1 in range(24):
            for bit2 in range(24):
                x = 1 << bit1 | 1 << bit2
                deltas.add(x)

        :param filename: Name of the file.
        '''
        self.values = []  # list of values
        self.points = {}  # dict of {value: [node numbers]}

        self.deltas = set()  # values we actually need to check
        for bit1 in range(24):
            for bit2 in range(24):
                x = 1 << bit1 | 1 << bit2
                self.deltas.add(x)

        self.min_value = 2 << 32
        self.max_value = 0

        self.load(filename)

    def load(self, filename):
        ''' Load clustering data.

        :param filename: Source of data.
        '''
        num_nodes = 0
        num_bits = 0
        x = 0

        with open(filename) as fp:
            for line in fp.readlines():
                if line[0] == '#':
                    continue
                parts = line.split()
                if len(parts) == 2:
                    if num_nodes == 0 and num_bits == 0:
                        num_nodes = int(parts[0])
                        num_bits = int(parts[1])
                    else:
                        raise ValueError('Found number of nodes again: %s' % (line))
                elif len(parts) == num_bits or len(parts) == 1:
                    binary = ''.join(line.split())
                    val = int(binary, 2)
                    if val > self.max_value:
                        self.max_value = val
                    if val < self.min_value:
                        self.min_value = val

                    self.values.append(val)
                    if val in self.points:
                        self.points[val].append(x)
                    else:
                        self.points[val] = [x]
                    x += 1

        if len(self.values) != num_nodes:
            raise ValueError('Expected %s nodes, got %s' % (num_nodes, len(self.values)))

    def cluster(self):
        ''' Cluster the nodes so the max distance is 3.
        '''
        all_nodes = range(len(self.values))

        # All nodes start in their own clusters.
        clusters = uf.UnionFind()
        clusters.insert_objects(all_nodes)  # The actual clusters.

        used_nodes = []

        for node in all_nodes:
            u_parent = clusters.find(node)

            # Find all the nodes near this one, and cluster them.
            for delta in self.deltas:
                val_plus = self.values[node] ^ delta

                if val_plus > self.max_value or val_plus < self.min_value:
                    continue

                checks = self.points[self.values[node]]
                if val_plus in self.points:
                    checks += self.points[val_plus]

                for item in checks:
                    v_parent = clusters.find(item)

                    if u_parent != v_parent:
                        clusters.union(node, item)
                        used_nodes.append(item)

        return clusters


def distance(x, y):
    ''' Compute Hamming distance for two integers.
    '''
    v = x ^ y
    dist = 0
    while v:
        v &= (v - 1)
        dist += 1

    return dist


def main(args):
    for filename in args:
        lumpy = Clusters(filename)
        print 'Loaded %s nodes from %s...' % (len(lumpy.values), filename)
        clusters = lumpy.cluster()
        #print clusters
        print 'k: %s' % (len(clusters.num_weights))


if __name__ == '__main__':
    main(sys.argv[1:])
