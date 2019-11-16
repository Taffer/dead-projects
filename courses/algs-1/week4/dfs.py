#!/usr/bin/env python
''' Depth-first search in Python.
'''

import sys

from collections import defaultdict
from scc import cmp_len, load_data, reverse_arcs


def kosaraju(g):
    ''' Return a list containing the SCCs in g. Each entry is a list of nodes.
    '''
    print "GRAPH:"
    print g

    # Reverse the arcs in g.
    g_rev = reverse_arcs(g)

    print "REVERSED:"
    print g_rev

    # Get finishing times for g_rev.
    finishing = dfs_loop(g_rev, finish_times=True)

    print "FINISHING TIMES:"
    print finishing

    # Run through g using the finishing times as index.
    n = g['max']
    finishing_indexes = [finishing[x] for x in xrange(n, 0, -1)]

    print "FINISHING INDEXES:"
    print finishing[1:]

    #leaders = dfs_loop(g, get_leaders=True, index=finishing_indexes)
    leaders = dfs_loop(g, get_leaders=True, index=finishing[1:])

    # Sort the leaders by size descending.
    sccs = [leaders[x] for x in leaders.keys()]
    sccs.sort(cmp=cmp_len, reverse=True)

    print 'Five largest SCCs: %s' % (','.join(["%s" % (len(x)) for x in sccs[0:5]]))


def dfs_loop(g, finish_times=False, get_leaders=False, index=None):
    ''' DFS-loop over graph g.
    '''
    n = g['max']
    explored = [False] * (n + 1)
    if index is None:
        nodes = xrange(n, 0, -1)
    else:
        nodes = index

    leaders = defaultdict(list)
    finishing = [-1] * (n + 1)
    s = { 't': 0, 's': None }

    for i in nodes:
        if explored[i] is False:
            s['s'] = i
            dfs_i(g, i, explored, s, leaders, finishing)

    if finish_times:
        return finishing
    if get_leaders:
        return leaders


def dfs_i(g, i, explored, s, leaders, finishing):
    ''' DFS over g starting at i, iteratively.
    '''
    nodes = [i]
    while len(nodes) > 0:
        x = nodes.pop()
        if explored[x] is True:
            continue

        explored[x] = True

        # Stack up the children.
        for j in reversed(g[x]):
            if explored[j] is False:
                nodes.append(j)

        # Visit node.
        leaders[s['s']].append(x)

        # Record finishing time.
        s['t'] += 1
        finishing[s['t']] = x


def main(argv):
    sys.setrecursionlimit(1000000)  # remember: ulimit -s 65532

    for arg in argv:
        graph = load_data(arg)
        print '%s graph has %s nodes' % (arg, len(graph))
        kosaraju(graph)


if __name__ == "__main__":
    #sys.argv.append('/Users/chrish/Dropbox/courses/algs-1/week4/SCC.txt')
    main(sys.argv[1:])
