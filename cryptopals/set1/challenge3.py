'''
 The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt the
message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character
frequency is a good metric. Evaluate each output and choose the one with the
best score.

Created on Aug 17, 2014

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import cryptopals  # PyDev, go home, you're drunk: @UnusedImport
import cryptopals.scoring


def guess_xor_key(ciphertext, use_naiive=True, from_hex=True):
    ''' Try all bytes and return the results scored by English-ness.

    Returns (key, plaintext).

    :param ciphertext: Encrypted hex string to decode.
    '''

    best = 0
    best_string = ""
    xor_key = 0

    if from_hex:
        ciphertext = bytearray.fromhex(ciphertext)

    for xor in xrange(256):
        keytext = bytearray(chr(xor)) * len(ciphertext)
        plainbytes = cryptopals.fixed_xor(ciphertext, keytext)

        if use_naiive:
            score = cryptopals.scoring.score_naiive(plainbytes)
        else:
            score = cryptopals.scoring.score_freq(plainbytes)

        if score > best:
            best = score
            best_string = str(plainbytes)
            xor_key = xor

    return (xor_key, best_string)


def main():
    ''' Which one gives us better results? '''
    # Results with naiive scoring.
    (best_key, best_string) = guess_xor_key('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736', True)
    print('String with key {0}: {1}'.format(best_key, best_string))

    # Results with English character frequency scoring.
    (best_key, best_string) = guess_xor_key('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736', False)
    print('String with key {0}: {1}'.format(best_key, best_string))


if __name__ == '__main__':
    main()
