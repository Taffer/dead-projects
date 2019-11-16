''' Randomized Contraction Algorithm
'''

import random
import sys


def find_mincut(graph):
    random.seed()

    while len(graph.keys()) > 2:
        # Pick random edge with vertices (u, v).
        u = random.choice(graph.keys())
        v = random.choice(graph[u])

        # Merge (u, v) into a single vertex.
        ends = graph.pop(v)
        for pt in ends:
            ticks = graph[pt].count(v)
            for _ in range(0, ticks):
                j = graph[pt].index(v)
                graph[pt][j] = u

        graph[u] += ends

        # Remove any self loops.
        while graph[u].count(u) > 0:
            graph[u].remove(u)

    return max([len(graph[x]) for x in graph.keys()])


def load_data(filename):
    with open(filename) as stream:
        lines = stream.readlines()

    graph = {}

    for l in lines:
        if len(l.strip()) <= 0:
            continue

        parts = [int(x) for x in l.split()]
        graph[parts[0]] = parts[1:]

    return graph


def main(argv):
    for arg in argv:
        mincut = None
        for s in range(0, 100):
            graph = load_data(arg)
            verts = graph.keys()
            if mincut is None:
                mincut = len(verts) ** 2
                print "%s has %s vertices" % (arg, len(verts))

            cut = find_mincut(graph)
            if cut < mincut:
                mincut = cut

        print "min cut is: %s" % (mincut)

if __name__ == "__main__":
    #sys.argv.append('/Users/chrish/Dropbox/courses/algs-1/week3/square.txt')
    main(sys.argv[1:])
