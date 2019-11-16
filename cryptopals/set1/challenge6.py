# -*- coding: utf-8 -*-
'''
Created on Feb 15, 2015

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import cryptopals.scoring
import sys

from set1.challenge3 import guess_xor_key


def norm_distance(chunk1, chunk2):
    ''' Return the normalized Hamming distance.

    :param chunk1: A piece of a byte array.
    :param chunk2: A piece of a byte array.
    '''
    keysize = len(chunk1)
    if keysize != len(chunk2):
        raise ValueError('Chunks much be the same length.')

    return float(cryptopals.scoring.hamming_distance(chunk1, chunk2)) / float(keysize)


def best_of_two(data):
    ''' Find the best-guess keysize using two substrings.

    :param data: Byte array.
    '''
    best_keysize = 0
    smallest_norm = 10000.0  # Way bigger than our valid values; max is 8.0...
    for keysize in xrange(2, 40):
        clip1 = data[0:keysize]
        clip2 = data[keysize:keysize * 2]

        norm = norm_distance(clip1, clip2)

        if norm < smallest_norm:
            smallest_norm = norm
            best_keysize = keysize

    return best_keysize


def best_three(data):
    ''' Find the three best-guess keysizes.

    :param data: Byte array.
    '''
    sizes = []
    for keysize in xrange(2, 40):
        clip1 = data[0:keysize]
        clip2 = data[keysize:keysize * 2]

        norm = norm_distance(clip1, clip2)

        sizes.append((norm, keysize))

    return sorted(sizes)[:3]


def best_of_four(data):
    ''' Find the best-guess keysize using four chunks.

    :param data: Byte array.
    '''
    best_keysize = 0
    smallest_norm = 10000.0  # Way bigger than our valid values; max is 8.0...
    for keysize in xrange(2, 40):
        clip1 = data[0:keysize]
        clip2 = data[keysize:keysize * 2]
        clip3 = data[keysize * 2:keysize * 3]
        clip4 = data[keysize * 3:keysize * 4]

        norms = [norm_distance(clip1, clip2) / float(keysize),
                 norm_distance(clip1, clip3) / float(keysize),
                 norm_distance(clip1, clip4) / float(keysize),
                 norm_distance(clip2, clip3) / float(keysize),
                 norm_distance(clip2, clip4) / float(keysize),
                 norm_distance(clip3, clip4) / float(keysize)]
        norm = float(sum(norms)) / float(len(norms))

        if norm < smallest_norm:
            smallest_norm = norm
            best_keysize = keysize

    return best_keysize


def chunks(data, length):
    ''' A generator that yields chunks of length.

    :param data: The data to split; anything that works with slices.
    :param length: The length of each chunk.
    '''
    for idx in xrange(0, len(data), length):
        yield bytearray(data[idx: idx + length])


def transposed_chunks(chunks):
    ''' Return a list of bytearrays of transposed bytes from each chunk.

    :param chunks: List of bytearrays to transpose.
    '''
    last_short = len(chunks[0]) != len(chunks[-1])
    for idx in xrange(0, len(chunks[0])):
        if last_short:
            yield bytearray([x[idx] for x in chunks[:-1]])
        else:
            yield bytearray([x[idx] for x in chunks])


def guess_key(data, keysize):
    ''' Guess the XOR repeating key.

    :param data: The data to decrypt.
    :param keysize: The key size to use.
    '''
    print('Trying with keysize = {0}'.format(keysize))

    # Split data into keysize-sized blocks.
    parts = [x for x in chunks(data, keysize)]

    print('len(parts) = {0}'.format(len(parts)))

    # Transpose the blocks.
    trans = [x for x in transposed_chunks(parts)]

    print('len(trans) = {0}'.format(len(trans)))

    keyparts = bytearray()
    for block in trans:
        (piece, _) = guess_xor_key(block, use_naiive=False, from_hex=False)
        keyparts.append(piece)

    plaintext = cryptopals.repeating_key_xor(keyparts, data)

    return plaintext


def main(args):
    if len(args) != 1:
        raise ValueError('You must specify a filename.')

    with open(args[0]) as fp:
        data = bytearray(base64.b64decode(fp.read()))

    # Try the other algs if one doesn't work out...

    # FIXME: None of these produce a good answer... maybe the best*() methods
    #        aren't implemented correctly?

    # Best of two block compares.
    keysize_guess = best_of_two(data)
    plaintext = guess_key(data, keysize_guess)

    print('Plaintext for {0}:'.format(keysize_guess))
    print(str(plaintext))

    # Top 3 results.
    keysize_guesses = best_three(data)
    for (_, keysize_guess) in keysize_guesses:
        plaintext = guess_key(data, keysize_guess)

        print('Plaintext for {0}:'.format(keysize_guess))
        print(str(plaintext))

    # Best of four block compares.
    keysize_guess = best_of_four(data)
    plaintext = guess_key(data, keysize_guess)

    print('Plaintext for {0}:'.format(keysize_guess))
    print(str(plaintext))


if __name__ == '__main__':
    main(sys.argv[1:])
