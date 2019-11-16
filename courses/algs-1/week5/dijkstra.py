#!/usr/bin/env python
''' Depth-first search in Python.
'''

import heapq
import sys


class WeightedGraph(object):
    ''' Weighted graph.
    '''

    def __init__(self, source):
        ''' Create a weighted graph from the source path.
        '''
        self.vertices = []  # == edges.keys()
        self.edges = {}  # vertex: [endpoints]
        self.weights = {}  # (u, v): weight for u->v edge

        self.load_data(source)

    def load_data(self, filename):
        ''' Load data from the specified filename.
        '''
        with open(filename) as a_file:
            line = a_file.readline()
            while line:
                if line[0] != '#':
                    # Each line is:
                    #
                    # head_vertex tail_vertex1,weight1 ...
                    parts = line.split()

                    head_vertex = int(parts[0])
                    self.vertices.append(head_vertex)
                    self.edges[head_vertex] = []

                    for edge_weight in parts[1:]:
                        tail_vertex, weight = [int(x) for x in
                                               edge_weight.split(',')]

                        self.edges[head_vertex].append(tail_vertex)
                        self.weights[(head_vertex, tail_vertex)] = weight

                line = file.readline()

    def shortest_paths(self, origin, default_distance=1000000):
        ''' Calculate the shortest paths for all nodes from origin.

        If there's no path from origin to a node, the length of the path
        will be set to default_distance.

        Returns a dictionary of destination: distance pairs.
        '''
        distances = dict((k, None) for k in self.edges)
        distances[origin] = 0  # distances from origin to key
        processed = [origin]  # vertices we've processed

        while len(processed) < len(self.vertices):
            # Find edge with the smallest total distance.
            heap = []
            for start in processed:
                for end in self.edges[start]:
                    if end in processed:
                        continue

                    this_len = distances[start] + self.weights[(start, end)]
                    heapq.heappush(heap, (this_len, end))

            if len(heap) == 0:
                # Everyone else isn't connected.
                break

            best_len, best_end = heapq.heappop(heap)

            # Add end_vertex to processed.
            processed.append(best_end)

            # Set distances[end_vertex] = length
            distances[best_end] = best_len

        # At the end, check for nodes we didn't visit.
        for node in self.vertices:
            if distances[node] is None:
                distances[node] = default_distance

        return distances


def main(argv):
    ''' Mainline!
    '''
    argv.reverse()

    while argv:
        filename = argv.pop()
        try:
            start_node = int(argv.pop())
        except IndexError:
            start_node = 1

        graph = WeightedGraph(filename)
        print '%s graph has %s nodes' % (filename, len(graph.vertices))

        dist = graph.shortest_paths(start_node)
        for k in sorted(dist.keys()):
            print "%s -> %s: %s" % (start_node, k, dist[k])

        if filename == 'dijkstraData.txt':
            results = []
            results = [str(dist[x]) for x in
                       (7, 37, 59, 82, 99, 115, 133, 165, 188, 197)]
            print ','.join(results)

if __name__ == "__main__":
    main(sys.argv[1:])
