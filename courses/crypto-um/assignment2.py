#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Assignment #2 for Jonathan Katz' Cryptography course on Coursera.

Recovering a key that's been used repeatedly.

Created on Jun 20, 2015

@author: chrish
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import assignment1
import string  # pylint: disable=w0402

# All of these were encrypted using the same key.
#
#                                 0         1         2         3         4         5         6
#                                 01234567890123456789012345678901234567890123456789012345678901
CIPHERTEXTS = [bytearray.fromhex('BB3A65F6F0034FA957F6A767699CE7FABA855AFB4F2B520AEAD612944A801E'),
               bytearray.fromhex('BA7F24F2A35357A05CB8A16762C5A6AAAC924AE6447F0608A3D11388569A1E'),
               bytearray.fromhex('A67261BBB30651BA5CF6BA297ED0E7B4E9894AA95E300247F0C0028F409A1E'),
               bytearray.fromhex('A57261F5F0004BA74CF4AA2979D9A6B7AC854DA95E305203EC8515954C9D0F'),
               bytearray.fromhex('BB3A70F3B91D48E84DF0AB702ECFEEB5BC8C5DA94C301E0BECD241954C831E'),
               bytearray.fromhex('A6726DE8F01A50E849EDBC6C7C9CF2B2A88E19FD423E0647ECCB04DD4C9D1E'),
               bytearray.fromhex('BC7570BBBF1D46E85AF9AA6C7A9CEFA9E9825CFD5E3A0047F7CD009305A71E')]

KEYLEN = 31  # Specified in the problem.

LOWERCASE = bytearray(string.lowercase)
PUNCTUATION = bytearray(string.punctuation)

# Things we know about ASCII and the ciphertexts:
#
# A ^ A = 0 ; if there's a 00 byte in the ciphertext, the key at that point
#             matches the plaintext. Matches found in #3 and #6...
#
# [A-Z] ^ space = [a-z]
#
# c[x] ^ k[x] = byte starts with 0 bit means both are ASCII letters
# c[x] ^ k[x] = byte starts with 1 bit means one is a
#
# CIPHERTEXTS[x] ^ CIPHERTEXTS[y] = PLAINTEXT[x] ^ PLAINTEXT[y]
#
# So, if we can recover a plaintext, we can easily recover the key.


def guess_pt(ciphertext, samples):
    ''' Try to guess the plaintext for ciphertext, using samples for comparisons.

    :param ciphertext: bytearray of the ciphertext we want to recover.
    :param samples: Additional ciphertexts to help recover the plaintext bytes.
    '''
    # Sanity
    for sam in samples:
        if len(sam) != len(ciphertext):
            raise ValueError('ciphertext and samples must all be the same length')

    plaintext = bytearray(len(ciphertext))

    pts = [xor_bytes(ciphertext, x) for x in samples]

    # For each pt in len(pts), if pts[pt][x] == 0x00, ciphertext[x] == samples[pts][x]

    # Find likely spaces...
    target_count = 3 * len(samples) / 4  # try 75%...
    for idx in xrange(len(plaintext)):
        count = 0
        letters = 0
        for idx2 in xrange(len(pts)):
            if pts[idx2][idx] & 0b10000000:
                count += 1
            elif pts[idx2][idx] & 0b10000000 == 0:
                letters += 1
        plaintext[idx] = count
        if count >= target_count:
            plaintext[idx] = ' '
        elif letters >= target_count:
            plaintext[idx] = ord('A')

    # Find

    return plaintext


def recover_key(keylen, ciphertexts):
    ''' Attempt to recover the most likely key used to encrypt ciphertexts.

    :param keylen: Length of the key used
    :param ciphertexts: Collection of ciphertexts encrypted with the same key.
    '''
    # guesses = [ guesses per ciphertext ]
    # guesses per ciphertext = [ guesses per byte ]
    # guesses per byte = [ potential key bytes ]
    guesses = [assignment1.guess_xor_key(keylen, x, False) for x in ciphertexts]

    # Refine the guesses.
    second_guesses = []
    for idx in xrange(0, keylen):
        guess_stream = [guesses[idx][x] for x in xrange(len(guesses[idx]))]
        byte_set = set(guess_stream[0])
        for streamed in guess_stream[1:]:
            byte_set.union(set(streamed))

        checked = []
        for check in byte_set:
            found = [True for x in xrange(keylen) if guesses[idx][x] == check]
            if len(found) == keylen:
                checked.append(check)
        second_guesses.append(checked)

    return second_guesses


def xor_bytes(ba1, ba2):
    ''' XOR two byte arrays of the same length.

    :param ba1: Byte array
    :param ba2: Byte array
    '''
    if len(ba1) != len(ba2):
        raise ValueError('bytearrays must be the same length')

    result = bytearray(len(ba1))
    for idx in xrange(len(result)):
        result[idx] = ba1[idx] ^ ba2[idx]

    return result


def most_common(items):
    ''' Return the most common item in items.

    :param items: list of items.
    '''
    if len(items) < 1:
        raise ValueError('empty set')
    elif len(items) == 1:
        return items[0]

    return max(set(items), key=items.count)


def is_alpha(ascii_value):
    ''' Is ascii_value an ASCII character if we chr(ascii_value)?

    :param ascii_value: The value to test.
    '''
    if ascii_value >= 0x41 and ascii_value <= 0x5a:
        return True
    elif ascii_value >= 0x61 and ascii_value <= 0x7a:
        return True

    return False


def test_message(target, ciphertexts):
    ''' Re-use code from other crypto class. :-)

    :param target: The plaintext we want to recover.
    :param ciphertexts: Additional ciphertexts created with the same key.
    '''
    xor_punctuation = bytearray([x ^ 0x20 for x in PUNCTUATION])
    spaces = bytearray(' '.encode('utf-8') * len(target))

    message_bytes = []  # array of strings, each char is likely to be a character in the output

    for ciphertext in ciphertexts:
        target_ciphertext = xor_bytes(target, ciphertext)

        potentials = []
        xor_s1 = xor_bytes(target_ciphertext, spaces)
        for a_byte in xor_s1:
            if is_alpha(a_byte):
                potentials.append(a_byte)
            elif a_byte in xor_punctuation:
                potentials.append(a_byte)
            else:
                potentials.append(0x20)

        message_bytes.append(potentials)

    plaintext_bytes = []  # Decrypted message, hopefully.

    for i in range(len(target)):
        chars = []
        for j in range(len(message_bytes)):
            a_byte = message_bytes[j][i]
            if is_alpha(a_byte) or a_byte in xor_punctuation:
                chars.append(a_byte)

        if len(chars) == 0:
            plaintext_bytes.append(0x00)
        else:
            plaintext_bytes.append(most_common(chars))

    return bytearray(plaintext_bytes)


def guess_plaintexts():
    ''' Attempt to guess one of the plaintexts so we can recover the key.
    '''
    recovered = [test_message(CIPHERTEXTS[0], CIPHERTEXTS[1:])]
    for idx in range(1, len(CIPHERTEXTS)):
        recovered.append(test_message(CIPHERTEXTS[idx], CIPHERTEXTS[:idx] + CIPHERTEXTS[idx + 1:]))

    # Guesses!
    # 0         1         2         3 - recovered[0]
    # 0123456789012345678901234567890
    # \hamcp\a\n\ngyahs\cr\ttmissio\\ ends with NUL?
    #  hamcp a ning a secret mission.
    recovered[0][10] = ord('i')
    recovered[0][13] = 0x20
    recovered[0][15] = 0x20
    recovered[0][17] = ord('e')
    recovered[0][20] = ord('e')
    recovered[0][22] = 0x20
    recovered[0][29] = ord('n')
    recovered[0][30] = ord('.')

    # 0         1         2         3 - recovered[1]
    # 0123456789012345678901234567890
    # \etisn\h\n\nlyapeesoeotootrusn\
    #  etisn h n nlyapeesoe to trust.
    recovered[1][21] = 0x20
    recovered[1][24] = 0x20
    recovered[1][29] = ord('t')
    recovered[1][30] = ord('.')

    # 0         1         2         3 - recovered[2]
    # 0123456789012345678901234567890
    # \hehcu\r\n\eplane\st\oplsecre\\
    # The current plan is top secret. <-- VICTORY!
    recovered[2][0] = ord('T')
    recovered[2][3] = 0x20
    recovered[2][6] = ord('r')
    recovered[2][8] = ord('e')
    recovered[2][10] = ord('t')
    recovered[2][11] = 0x20
    recovered[2][16] = 0x20
    recovered[2][17] = ord('i')
    recovered[2][19] = 0x20
    recovered[2][20] = ord('t')
    recovered[2][23] = 0x20
    recovered[2][29] = ord('t')
    recovered[2][30] = ord('.')

    # 0         1         2         3 - recovered[3]
    # 0123456789012345678901234567890
    # \hencs\o\l\eweame\tt\otdoethi\\
    recovered[3][30] = ord('.')

    # 0         1         2         3 - recovered[4]
    # 0123456789012345678901234567890
    # \hthin\h\h\ygshou\dt\ollowahi\\
    recovered[4][30] = ord('.')

    # 0         1         2         3 - recovered[5]
    # 0123456789012345678901234567890
    # \hisci\h\u\erytha\st\atlonehi\\
    # This is \u\erytha\st\at one i\.
    recovered[5][0] = ord('T')
    recovered[5][4] = 0x20
    recovered[5][6] = ord('s')
    recovered[5][7] = 0x20
    recovered[5][23] = 0x20
    recovered[5][27] = 0x20
    recovered[5][30] = ord('.')

    # 0         1         2         3 - recovered[6]
    # 0123456789012345678901234567890
    # \othon\h\a\etyise\et\erlthani\\
    # Both n\h\a\etyise\et\erlthani\.
    recovered[6][0] = ord('B')
    recovered[6][4] = 0x20
    recovered[6][30] = ord('.')

    return recovered


def main():
    guessed_plaintexts = guess_plaintexts()
    recovered_key = xor_bytes(guessed_plaintexts[2], CIPHERTEXTS[2])

    messages = [xor_bytes(recovered_key, x) for x in CIPHERTEXTS]

    for idx in range(len(CIPHERTEXTS)):
        print('{0}: {1}'.format(idx, messages[idx]))


if __name__ == '__main__':
    main()
