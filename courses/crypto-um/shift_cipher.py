#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Shift cipher

Given k in 0 ... 25, encrypt string.lowercase strings by shifting k positions.

See also rot-13.

Created on June 8, 2015

@author: chrish
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import string  # pylint: disable=W0402

ASCII_DELTA = ord('a')  # Shift 'a' to 0 using this delta.


def shift_enc(enc_key, message):
    ''' Shift-encrypt message message using key enc_key. '''
    ciphertext = []
    for line in message:
        if line in string.lowercase:
            ciphertext.append(chr(ASCII_DELTA + ((ord(line) - ASCII_DELTA + enc_key) % 26)))
        else:
            ciphertext.append('_')

    return ''.join(ciphertext)


def vigenere_enc(enc_key, message):
    ''' Vigenere-encrypt message message using key enc_key. '''
    key_idx = 0
    ciphertext = []
    for line in message:
        ciphertext.append(shift_enc(ord(enc_key[key_idx % len(enc_key)]) - ASCII_DELTA, line))
        key_idx += 1

    return ''.join(ciphertext)


def main():
    # print(shift_enc(13, 'cryptoisfun'))
    print(vigenere_enc('spy', 'seeyouatnoon'))


if __name__ == '__main__':
    main()
