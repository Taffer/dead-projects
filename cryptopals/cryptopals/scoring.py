# -*- coding: utf-8 -*-
''' Methods for scoring the relative goodness of strings.

Note that scores are relative to other scores *from the same method*.

Score from one method have no relation to scores from a different method.

Created on Feb 10, 2015

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import string


# Assumption is that mostly text and whitespace is good, but mostly
# punctuation is bad.
GOOD_CHARS = bytearray(string.ascii_letters)
GOOD_CHARS.extend(string.digits)
GOOD_CHARS.extend(string.whitespace)
BAD_CHARS = bytearray(string.punctuation)

PRINTABLE_CHARS = bytearray(string.printable)


def score_naiive(score_bytes):
    ''' Score the given byte string naiively.

    Assumes the target string is English.

    Returns a score; scores are relative to each other and have no relation
    to anything. Returns 0 if a string isn't made up of printable characters.

    :param score_bytes: A bytearray.
    '''
    # Since we're looking at simple English phrases, anything that comes
    # out all 7-bit ASCII printables is probably the right thing.
    #
    # To focus in on what we're after, we probably want a large ratio of
    # letters and numbers to punctuation and whitespace.
    score = 0
    for c in score_bytes:
        if c not in PRINTABLE_CHARS:
            # Unprintable character, keep looking for that key...
            return 0
        if c in GOOD_CHARS:
            score += 1
        if c in BAD_CHARS:
            score -= 1

    return score


FREQUENT_CHARS_UPPER = bytearray('ETAOINSHRDLU'.encode('ascii'))
FREQUENT_CHARS_LOWER = bytearray('ETAOINSHRDLU'.lower().encode('ascii'))


def score_freq(score_bytes):
    ''' Score the given byte string by English letter frequency.

    Assumes the target string is English. "ETAOIN SHRDLU"

    Returns a score; scores are relative to each other and have no relation
    to anything. Returns 0 if a string isn't made up of printable characters.

    :param score_bytes: A string of bytes or bytearray.
    '''
    score = 0
    for c in score_bytes:
        if c not in PRINTABLE_CHARS:
            return 0
        if c in FREQUENT_CHARS_UPPER:
            # More-frequent gives you more score.
            score += len(FREQUENT_CHARS_UPPER) - FREQUENT_CHARS_UPPER.index(chr(c))
        elif c in FREQUENT_CHARS_LOWER:
            # More-frequent gives you more score.
            score += len(FREQUENT_CHARS_LOWER) - FREQUENT_CHARS_LOWER.index(chr(c))

    return score


def hamming_distance(bytes1, bytes2):
    ''' Find the Hamming distance between two strings of bytes.

    :param bytes1: A bytearray.
    :param bytes2: A bytearray.
    '''
    if len(bytes1) != len(bytes2):
        raise ValueError('Byte arrays must be the same length')

    delta = bytearray([bytes1[x] ^ bytes2[x] for x in xrange(len(bytes1))])

    return sum([bin(x).count('1') for x in delta])
