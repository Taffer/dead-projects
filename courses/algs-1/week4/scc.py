''' Finding Strongly-Connected Components of a graph

Kosaraju's Two-Pass Algorithm
'''

import sys

from collections import defaultdict, deque


def load_data(filename):
    graph = defaultdict(list)

    max = 0

    with open(filename) as stream:
        l = stream.readline()
        while l:
            parts = [int(x) for x in l.split()]
            graph[parts[0]].append(parts[1])

            if parts[0] > max:
                max = parts[0]

            l = stream.readline()

    graph['max'] = max

    # Graph is now a dict of:
    #
    # { vertex: [tail1, tail2, ... tailn], }
    #
    # for all edges vertex, {tails}
    return graph


def reverse_arcs(g):
    ''' Return a new graph based on g with all arcs reversed.
    '''
    ret = defaultdict(list)
    for u in xrange(1, g['max'] + 1):
        for v in g[u]:
            ret[v].append(u)
    ret['max'] = g['max']
    return ret


def cmp_len(a, b):
    ''' Sort comparer for lengths of items.
    '''
    if len(a) > len(b):
        return 1
    elif len(a) < len(b):
        return -1
    else:
        return 0


# State for Kosaraju's versions of DFS_loop() and DFS()
def make_state():
    ''' Return a fresh state container.
    '''
    state = {}
    state['t'] = 0
    state['s'] = None
    state['explored'] = []
    state['finishing'] = {}  # finishing[t] = node with finishing time t
    state['leaders'] = {}  # leaders[i] = [list of nodes where i is the leader]

    return state


def kosaraju(g):
    ''' Return a list containing the SCCs in g. Each entry is a list of nodes.
    '''
    global finishing
    global leaders

    # Create g_rev from g with all arcs reversed.
    g_rev = reverse_arcs(g)

    # Run DFS_loop on g_rev to get finishing times.
    first_run = make_state()
    DFS_loop(g_rev, first_run)

    # Run DFS_loop on g using the finishing times as index.
    second_run = make_state()
    DFS_loop(g, second_run, indexes=first_run['finishing'])

    # Collect SCCs grouped by their leader.
    sccs = [second_run['leaders'][x] for x in second_run['leaders'].keys()]
    sccs.sort(cmp=cmp_len, reverse=True)

    return sccs


def DFS_loop(g, state, indexes=None):
    ''' Loop over graph g doing depth-first search on unexplored nodes.
    '''
    n = g['max']
    if indexes is None:
        items = range(n, 0, -1)
    else:
        items = [indexes[x] for x in xrange(n, 0, -1)]

    for i in items:
        if i not in state['explored']:
            state['s'] = i
            DFS_recursive(g, i, state)
            #DFS_iter(g, i, state)
            #DFS_iter2(g, i, state)


def DFS_iter2(g, i, state):
    ''' Non-recursive depth-first search on g starting at i.

    list nodes_to_visit = {root};
    while( nodes_to_visit isn't empty ) {
        currentnode = nodes_to_visit.first();
        nodes_to_visit.prepend( currentnode.children );
        //do something
    }
    '''
    to_visit = deque([i])
    while len(to_visit) > 0:
        current = to_visit.popleft()
        if current in state['explored']:
            continue

        state['explored'].append(current)

        print 'visit %s' % (current)

        if state['s'] in state['leaders']:
            state['leaders'][state['s']].append(current)
        else:
            state['leaders'][state['s']] = [current,]

        for j in reversed(g[current]):
            if j not in state['explored']:
                to_visit.appendleft(j)

        state['t'] += 1
        state['finishing'][state['t']] = current


def DFS_iter(g, i, state):
    ''' Non-recursive depth-first search on g starting at i.
    '''
    print "%s/%s explored" % (len(state['explored']), len(g))

    nodes_to_visit = deque([i])
    while nodes_to_visit:
        visit = nodes_to_visit.popleft()
        if visit in state['explored']:
            continue

        print "visit %s" % (visit)
        state['explored'].append(visit)

        if state['s'] in state['leaders']:
            state['leaders'][state['s']].append(visit)
        else:
            state['leaders'][state['s']] = [visit,]

        if visit not in g:
            # In case there are holes in the input data.
            g[visit] = []

        for j in reversed(g[visit]):
            if j not in state['explored']:
                nodes_to_visit.appendleft(j)

        state['t'] += 1
        state['finishing'][state['t']] = i


def DFS_recursive(g, i, state):
    ''' Do a depth-first search on graph g starting at node i.
    '''

    state['explored'].append(i)

    if state['s'] in state['leaders']:
        state['leaders'][state['s']].append(i)
    else:
        state['leaders'][state['s']] = [i,]

    for j in g[i]:
        if j not in state['explored']:
            DFS_recursive(g, j, state)

    state['t'] += 1
    state['finishing'][state['t']] = i


def main(argv):
    sys.setrecursionlimit(1000000)  # remember: ulimit -s 65532

    for arg in argv:
        graph = load_data(arg)
        print '%s graph has %s nodes' % (arg, graph['max'])
        sccs = kosaraju(graph)
        print "Five largest SCCs:", ','.join([str(len(x)) for x in sccs[0:5]])


if __name__ == "__main__":
    #sys.argv.append('/Users/chrish/Dropbox/courses/algs-1/week4/SCC.txt')
    main(sys.argv[1:])
