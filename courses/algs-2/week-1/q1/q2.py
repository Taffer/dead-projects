#!/usr/bin/env python
'''
For this problem, use the same data set as in the previous problem. Your task
now is to run the greedy algorithm that schedules jobs (optimally) in
decreasing order of the ratio (weight/length). In this algorithm, it does not
matter how you break ties. You should report the sum of weighted completion
times of the resulting schedule --- a positive integer --- in the box below.
'''

import sys


class Job(object):
    def __init__(self, weight, length):
        self.weight = weight
        self.length = length
        self.score = float(weight) / float(length)

    def __str__(self):
        return '(%s, %s) = %s' % (self.weight, self.length, self.score)

    @staticmethod
    def sort(lhs, rhs):
        ''' Sort two Jobs based on their score. '''
        delta = lhs.score - rhs.score
        if delta < 0.0:
            return -1
        elif delta > 0.0:
            return 1

        return 0


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
