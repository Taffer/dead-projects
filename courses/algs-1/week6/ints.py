#!/usr/bin/env python
''' 2-SUM sort of problem.
'''

import sys


def load_ints(filename):
    ''' Load an array of ints from the given filename.
    '''
    int_array = []

    with open(filename) as a_file:
        line = a_file.readline()
        while line:
            if line[0] != '#':
                int_array.append(int(line))
            line = a_file.readline()

    return int_array


def two_sum(pool, t_min, t_max):
    '''
    Look for distinct values (x, y) in pool that add up
    to t_min <= t <= t_max.
    '''
    count = 0

    #pool_dict = {x: None for x in pool}
    pool_set = set(pool)
    pool_min = min(pool)

    for t in xrange(t_min, t_max + 1):
        # Count # of t that have x,y sums.

        for x in [x for x in pool if x <= t_max]:
            y = t - x
            if y < pool_min:
                continue
            if y == x:
                continue
            if y in pool_set:#_dict:
                count += 1
                break

    return count


def main(argv):
    ''' Mainline!
    '''
    argv.reverse()
    while argv:
        filename = argv.pop()
        min = int(argv.pop())
        max = int(argv.pop())

        all_ints = load_ints(filename)
        results = two_sum(all_ints, min, max)

        print 'Found %d matching sums' % (results)

if __name__ == "__main__":
    main(sys.argv[1:])
