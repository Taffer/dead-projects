# -*- coding: utf-8 -*-
''' Useful, general bits from Matasano's CryptoPals challenge.

http://cryptopals.com/

Created on Feb 10, 2015

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import base64


def fixed_xor(bytes1, bytes2):
    ''' XOR the bytes in bytes1 with the bytes in bytes2.

    :param bytes1: bytearray
    :param bytes2: bytearray

    :returns: bytearray of bytes1 XOR bytes2
    '''
    if len(bytes1) != len(bytes2):
        raise ValueError('Input byte streams must be the same size.')

    bytes_out = bytearray(len(bytes1))

    for idx in xrange(len(bytes_out)):
        bytes_out[idx] = bytes1[idx] ^ bytes2[idx]

    return bytes_out


def hex2base64(hex_string):
    ''' Convert a given hex string into base64 encoded bytes.

    :param hex_string: A string of hex digits representing bytes.

    :returns: A string of base64 encoded bytes.
    '''
    hexbytes = bytearray.fromhex(hex_string)
    return base64.b64encode(hexbytes)


def repeating_key_xor(key_bytes, plaintext):
    ''' Encrypt plaintext bytes using XOR and the given key bytes.

    Returns encrypted ciphertext bytes.

    :param key_bytes: bytearray to use as a repeating key.
    :param plaintext: bytearray to encrypt.
    '''
    encrypted = bytearray(len(plaintext))
    key_idx = 0
    for idx in xrange(len(plaintext)):
        encrypted[idx] = plaintext[idx] ^ key_bytes[key_idx]

        # Next key byte:
        key_idx += 1
        key_idx = key_idx % (len(key_bytes))

    return encrypted
