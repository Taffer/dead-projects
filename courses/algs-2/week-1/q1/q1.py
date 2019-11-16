#!/usr/bin/env python
'''
In this programming problem and the next you'll code up the greedy algorithms
from lecture for minimizing the weighted sum of completion times.. Download
the text file here. This file describes a set of jobs with positive and
integral weights and lengths. It has the format

[number_of_jobs]
[job_1_weight] [job_1_length]
[job_2_weight] [job_2_length]
...
For example, the third line of the file is "74 59", indicating that the second
job has weight 74 and length 59. You should NOT assume that edge weights or
lengths are distinct.

Your task in this problem is to run the greedy algorithm that schedules jobs
in decreasing order of the difference (weight - length). Recall from lecture
that this algorithm is not always optimal. IMPORTANT: if two jobs have equal
difference (weight - length), you should schedule the job with higher weight
first. Beware: if you break ties in a different way, you are likely to get the
wrong answer. You should report the sum of weighted completion times of the
resulting schedule --- a positive integer --- in the box below.

ADVICE: If you get the wrong answer, try out some small test cases to debug
your algorithm (and post your test cases to the discussion forum)!
'''

import sys


class Job(object):
    def __init__(self, weight, length):
        self.weight = weight
        self.length = length
        self.score = weight - length

    def __str__(self):
        return '(%s, %s) = %s' % (self.weight, self.length, self.score)

    @staticmethod
    def sort(lhs, rhs):
        ''' Sort two Jobs based on their score. '''
        delta = lhs.score - rhs.score
        if delta == 0:
            # Scores are the same!
            delta = lhs.weight - rhs.weight
        return delta


def parse_input(filename):
    ''' Parse input file into list of Jobs. '''
    num_jobs = 0
    jobs = []
    with open(filename) as fp:
        for line in fp.readlines():
            if line[0] == '#':
                continue

            parts = line.split()
            if len(parts) == 1:
                if num_jobs == 0:
                    num_jobs = int(parts[0])
                else:
                    raise ValueError('Already saw num_jobs (%s), got another: %s' % (num_jobs, line))
            elif len(parts) == 2:
                jobs.append(Job(int(parts[0]), int(parts[1])))
            else:
                raise ValueError('Invalid line: %s' % (line))

    if num_jobs != len(jobs):
        raise ValueError('Expected %s jobs but got %s' % (num_jobs, len(jobs)))

    return jobs


def main(args):
    for filename in args:
        jobs = parse_input(filename)
        print '%s jobs in %s' % (len(jobs), filename)

        x = 0
        completion_times = 0
        weighted_times = 0
        for job in sorted(jobs, cmp=Job.sort, reverse=True):
            x += 1
            completion_times += job.length
            weighted_times += completion_times * job.weight

        print 'Weighted time total: %s' % (weighted_times)


if __name__ == '__main__':
    main(sys.argv[1:])
