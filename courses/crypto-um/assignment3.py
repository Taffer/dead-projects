#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Jun 27, 2015

@author: chrish

From the look of the sample code, the oracle is probably vulnerable to buffer
overflow attacks. Probably not a good idea to DOS the server during the
course, right?
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import binascii
import proj3.oracle
import string  # pylint: disable=W0402

AES_BLOCK = 16  # 16 bytes == 128 bits == AES block size
SEARCH_BYTES = bytearray(string.printable)  # Speed up by ordering this by letter frequency...

# Two message blocks, M1, M2
#
# C1 = IV
# C2 = M1 XOR C0
# C3 = M2 XOR C1
#
# Changing bytes at the end of C1 lets us divine M2 thanks to the CBC
# avalanche effect.
#
#                                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
#                                0 1 2 3 4 5 6 7 8 9 a b c d e f 0 1 2 3 4 5 6 7 8 9 a b c d e f 0 1 2 3 4 5 6 7 8 9 a b c d e f
#                               IVIVIVIVIVIVIVIVIVIVIVIVIVIVIVIVC1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C2C2C2C2C2C2C2C2C2C2C2C2C2C2C2C2
CIPHERTEXT = bytearray.fromhex('9F0B13944841A832B2421B9EAF6D9836813EC9D944A5C8347A7CA69AA34D8DC0DF70E343C4000A2AE35874CE75E64C31')
#                                                                                                padding: 0b0b0b0b0b0b0b0b0b0b0b
#
# IV    = 9F0B13944841A832B2421B9EAF6D9836
# C1[x] = E_k(PT1[x] ^ IV[x])
# C2[x] = E_k(PT2[x] ^ C1[x])
#
# c2[0x0f] = E_k(p2[0x0f] ^ C1[0x0f])
#     0x31 = E_k(p2[0x0f] ^ 0xc0)
#     0x31 = E_k(0x0b ^ 0xc0)
#     0x31 = E_k(0xcb)
#
# Sooo... c1[-1] ... c1[-padding] += 1, then c1[-padding -1] = x ^ 0x0c


def hexify(some_bytes):
    ''' Convert bytes into a hex string for printing.

    :param some_bytes: A bytearray.
    '''
    return binascii.hexlify(some_bytes)


def addbyte(val):
    ''' Return (val + 1) % 256.
    '''
    return (val + 1) % 256


def guess_padding(oracle, ciphertext, blocksize=AES_BLOCK, debug=False):
    ''' Guess how much padding is in the last block.

    Returns 1 <= x <= blocksize, or -1 if you're doing it wrong.

    :param oracle: The padding oracle.
    :param ciphertext: The ciphertext to examine.
    :param blocksize: Bytes/block in the ciphertext.
    :param debug: If debug, then be noisy.
    '''
    num_blocks = len(ciphertext) // blocksize
    second_last_block = blocksize * (num_blocks - 2)

    # Check baseline.
    if oracle.send(ciphertext, num_blocks) == 0:  # Get IndexError here if the server goes down...
        raise ValueError('Invalid ciphertext')

    # Clone the ciphertext so we can mess with it.
    mutated = ciphertext[:]

    offset = 0
    while offset < blocksize:
        mutated[second_last_block + offset] = 0x20
        retval = oracle.send(mutated, num_blocks)  # Get IndexError here if the server goes down...
        if debug:
            print('Offest  : {0}'.format(offset))
            print('Retval  : {0}'.format(retval))
            print('Original: {0}'.format(hexify(ciphertext)))
            print('Mutant  : {0}'.format(hexify(mutated)))
        if retval == 0:
            return blocksize - offset
        offset += 1

    return -1


def guess_block(oracle, iv, block, blocksize=AES_BLOCK, debug=False):  # pylint: disable=C0103,R0912
    ''' Guess the plaintext in block.

    :param oracle: a padding oracle
    :param iv: the initialization vector for block
    :param block: the ciphertext block to decrypt
    :param blocksize: Bytes/block in the ciphertext.
    :param debug: If debug, then be noisy.
    '''
    # Sanity
    if len(iv) != len(block) and len(block) != blocksize:
        msg = 'Invalid block size: IV = {0} bytes, block = {1} bytes, blocksize = {2} bytes'.format(len(iv), len(block), blocksize)
        raise ValueError(msg)

    mutant_iv = iv[:]  # A copy so we can muck with it.

    # If this isn't currently valid, our padding is going to be 0; that is,
    # we'll have to start right at the last character.
    if oracle.send(iv + block, 2) == 0:  # Get IndexError here if the server goes down...
        padding = 0
    else:
        if debug:
            print('guess_block: Block has valid padding, finding size...')
        padding = guess_padding(oracle, iv + block, blocksize)

    if debug:
        print('guess_block: padding is {0}'.format(hex(padding)))

    plaintext = bytearray(blocksize)  # Output plaintext array.
    for idx in range(-padding, 0):
        plaintext[idx] = padding  # Ended with appropriate padding bytes.

    while padding < blocksize:
        # Bump up the existing padding.
        if debug:
            print('padding: {0}, IV: {1}'.format(hex(padding), hexify(mutant_iv)))

        for idx in range(-padding, 0):
            mutant_iv[idx] = mutant_iv[idx] ^ padding ^ (padding + 1)

        padding += 1
        end_offset = -padding  # Last character.

        if debug:
            print('padding: {0}, IV: {1}'.format(hex(padding), hexify(mutant_iv)))

        found = False
        for val in SEARCH_BYTES:
            new_byte = val ^ padding ^ iv[end_offset]
            mutant_iv[end_offset] = new_byte
            check = oracle.send(mutant_iv + block, 2)  # Get IndexError here if the server goes down...

            if check:
                plaintext[end_offset] = val
                found = True
                if debug:
                    print('Byte found at {0}: {1}'.format(hex(padding), hex(val)))
                break

        if not found:
            print('No byte found at padding {0}'.format(hex(padding)))

    return plaintext


def main():
    block_size = int(len(CIPHERTEXT) / 3)  # Assuming the send() in the sample isn't lying about # of blocks.
    print('CIPHERTEXT length: {0}, block size: {1}'.format(len(CIPHERTEXT), block_size))
    iv = CIPHERTEXT[:16]  # pylint: disable=C0103
    ct1 = CIPHERTEXT[16:32]
    ct2 = CIPHERTEXT[32:]

    try:
        oracle = proj3.oracle.Oracle()
        if oracle.connect() == -1:
            print('No oracle.')
            return

        pt2 = guess_block(oracle, ct1, ct2)  # Guess final block's contents.
        print('pt2 = {0}'.format(hexify(pt2)))

        pt1 = guess_block(oracle, iv, ct1)  # Guess the first block's contents.
        print('pt1 = {0}'.format(hexify(pt1)))

        # Check padding.
        padding = pt2[-1]
        for idx in range(-padding, 0):
            if pt2[idx] != padding:
                print('Invalid padding, sorry.')
                return

        plaintext = pt1 + pt2[:-padding]
        print('Got plaintext: "{0}"'.format(''.join([chr(x) for x in plaintext])))

    except IndexError as exc:
        print('Got IndexError, server probably hung up on us...')
        print('{0}'.format(exc))

    finally:
        # Don't bail until we've cleaned up, not friendly to leave the socket
        # open...
        oracle.disconnect()


if __name__ == '__main__':
    main()
