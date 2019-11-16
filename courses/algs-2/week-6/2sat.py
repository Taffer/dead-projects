#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
In this assignment you will implement one or more algorithms for the 2SAT
problem. Here are 6 different 2SAT instances: #1 #2 #3 #4 #5 #6.

The file format is as follows. In each instance, the number of variables
and the number of clauses is the same, and this number is specified on the
first line of the file. Each subsequent line specifies a clause via its two
literals, with a number denoting the variable and a "-" sign denoting logical
"not". For example, the second line of the first data file is "-16808 75250",
which indicates the clause ¬x16808∨x75250.

Your task is to determine which of the 6 instances are satisfiable, and which
are unsatisfiable. In the box below, enter a 6-bit string, where the ith bit
should be 1 if the ith instance is satisfiable, and 0 otherwise. For example,
if you think that the first 3 instances are satisfiable and the last 3 are not,
then you should enter the string 111000 in the box below.

DISCUSSION: This assignment is deliberately open-ended, and you can implement
whichever 2SAT algorithm you want. For example, 2SAT reduces to computing the
strongly connected components of a suitable graph (with two vertices per
variable and two directed edges per clause, you should think through the
details). This might be an especially attractive option for those of you who
coded up an SCC algorithm for Part I of this course. Alternatively, you can
use Papadimitriou's randomized local search algorithm. (The algorithm from
lecture might be too slow, so you might want to make one or more simple
modifications to it to ensure that it runs in a reasonable amount of time.) A
third approach is via backtracking. In lecture we mentioned this approach only
in passing; see the DPV book, for example, for more details.
'''
# ∨ = OR

import bitarray
import math
import random
import sys


class TwoSat(object):
    ''' 2SAT. '''
    def __init__(self, filename):
        ''' Load a 2SAT problem from the specified file. '''
        self.bits = None  # bitarray of predicates
        self.important = set([])  # predicates actually used in clauses
        self.clauses = set([])  # list of (x,y) clauses; -x = not x

        with open(filename) as a_file:
            for line in a_file.readlines():
                if line[0] == '#' or len(line.strip()) == 0:
                    continue

                parts = line.split()
                if len(parts) == 1:
                    # The number of predicates.
                    self.bits = bitarray.bitarray(int(parts[0]) + 1)  # +1 because Python is 0-based
                elif len(parts) == 2:
                    # A clause.
                    x = int(parts[0])
                    y = int(parts[1])

                    self.clauses.add((x, y))

                    self.important.add(abs(x))
                    self.important.add(abs(y))
                else:
                    raise ValueError("Can't parse line: %s" % (line))

        # Pre-process a bit; remove always negative and always positive preds
        # after setting their bits appropriately.
        pre_clauses = len(self.clauses)

        while True:
            self.clauses = set([x for x in self.clauses if not x[0] == -x[1]])  # redundant: x | !x

            preds = set([])
            for item in self.clauses:
                preds.add(item[0])
                preds.add(item[1])
    
            neg = set([x for x in preds if x < 0 and abs(x) not in preds])
            pos = set([x for x in preds if x > 0 and -x not in preds])

            if len(neg) == 0 and len(pos) == 0:
                break
    
            for bit in neg:  # These ones always have to be negative.
                self.bits[abs(bit)] = False
                self.important.discard(abs(bit))
            for bit in pos:  # These ones always have to be positive.
                self.bits[bit] = True
                self.important.discard(bit)
            #print 'Removed %s predicates' % (len(neg) + len(pos))

            # Remove clauses that are always true now.
            nuke = set([])
            for item in neg:
                nuke.add(abs(item))
                nuke.add(item)
            for item in pos:
                nuke.add(item)
                nuke.add(-item)
            self.clauses = set([x for x in self.clauses if x[0] not in nuke and x[1] not in nuke])
            #print 'Removed %s clauses.' % (pre_clauses - len(self.clauses))

        # We're only interested in predicates that can affect the outcome
        # (that is, ones that are in clauses).
        self.important = set([])
        for item in self.clauses:
            self.important.add(abs(item[0]))
            self.important.add(abs(item[1]))

    def randomize_bits(self):
        ''' Randomize the interesting bits in our bitset. '''
        bit = [False, True]
        for idx in self.important:
            self.bits[idx] = random.choice(bit)

    def check_clauses(self):
        ''' Return a list of unsatisfied clauses. '''
        unsatisfied = []
        for (x, y) in self.clauses:
            if x < 0:
                x_val = not self.bits[abs(x)]
            else:
                x_val = self.bits[x]
            if y < 0:
                y_val = not self.bits[abs(y)]
            else:
                y_val = self.bits[y]
            if not (x_val | y_val):
                unsatisfied.append((x, y))

        return unsatisfied

    def solve(self):
        ''' Return True if this 2SAT is satisfiable, else False.

        Papadimitriou's algorithm.
        '''
        iterations = 1
        for idx in xrange(int(math.log(len(self.bits), 2))):
            self.randomize_bits()
            unsatisfied = self.check_clauses()
            if len(unsatisfied) == 0:
                # You got lucky!
                #print 'Solved in %s iterations (LUCKY!).' % (iterations)
                return True

            inner = 0
            while inner <= (2 * len(self.important) ** 2):
            #for inner in xrange(2 * (len(self.important) ** 2)):
                # We only need to flip the important bits, not all bits ever.
                flipper = random.choice(unsatisfied)
                which = abs(random.choice(flipper))
                self.bits[which] = not self.bits[which]

                unsatisfied = self.check_clauses()
                if len(unsatisfied) == 0:
                    #print 'Solved in %s iterations.' % (iterations)
                    return True

                iterations += 1
                inner += 1

        return False

def main(args):
    for filename in args:
        prob = TwoSat(filename)
        #print '%s => %s predicates, %s clauses' % (filename, len(prob.important), len(prob.clauses))
        solution = prob.solve()
        print '%s => %s' % (filename, 1 if solution else 0)


if __name__ == '__main__':
    main(sys.argv[1:])
