'''
One of the 60-character strings in this file (4.txt) has been encrypted by
single-character XOR.

Find it.

Created on Sep 1, 2014

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import cryptopals.scoring
import sys

from set1.challenge3 import guess_xor_key


def main(args):
    ''' Search the given files for a single-byte XOR encrypted string.

    :param args: Command-line arguments.
    '''
    for filename in args:
        with open(filename) as fp:
            lines = fp.readlines()

        plain_lines = []
        for ciphertext in lines:
            ciphertext = ciphertext.strip()
            (_, best_string) = guess_xor_key(ciphertext)
            freq_score = cryptopals.scoring.score_freq(bytearray(best_string.encode('ascii')))
            if freq_score == 0:
                continue

            plain_lines.append((freq_score, best_string))

        # Print best string and its score from this file.
        print('String in {0}: {1}'.format(filename, max(plain_lines)))

if __name__ == '__main__':
    main(sys.argv[1:])
