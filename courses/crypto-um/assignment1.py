#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Assignment #1 for Jonathan Katz' Cryptography course on Coursera.

Created on Jun 14, 2015

@author: chrish
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import string  # For string.printable. pylint: disable=W0402

PRINTABLE_BYTES = bytearray(string.printable)
UPPERCASE_BYTES = bytearray(string.uppercase)

# English letter frequencies for top 12 letters.
#
# Source: https://en.wikipedia.org/wiki/Letter_frequency
ETAOIN_SHRDLU = [etaoin / 100.0 for etaoin in [12.702, 9.056, 8.167, 7.507, 6.966, 6.749, 6.327, 6.094, 5.987, 4.253, 4.025, 2.758]]
ETAOIN_SUM = sum(ETAOIN_SHRDLU)

# Target ciphertext.
#
# Assumptions:
#
#    * English plaintext
#    * No newlines encoded inside.
CIPHERTEXT = '''F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7EFFD673BE4ACF7BE8923CAB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF5B9A7CFEDF3EB850D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE6BF0D138A84CC931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF9226BE5BDE3FF7DD21ED56CF71F5C036A94D963FF8D473A351CE3FE5DA3CB84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451D47EFD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47AF59232A35A9A7AE7D33FB85FCE7AF5923AA31EDB3FF7D33ABF52C33FF0D673A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA36ED68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC93FE5DA3CB859D26BB1C63CED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A85A963FF3C727ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44DDF3FF5D73EA250C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87AB1D021A255DF71B1C436BF479A7AF0C13AA14794'''  # pylint: disable=C0301


def get_frequencies(bytestream):
    ''' Get the frequencies of each byte.

    :param bytestream: Bytes to examine. Use bytearray for sanity.
    '''
    if bytestream is None or len(bytestream) < 1:
        raise ValueError('empty bytestream')

    count = float(len(bytestream))
    byte_counts = {k: 0 for k in range(256)}
    for byte in bytestream:
        byte_counts[byte] += 1

    freqs = [(float(byte_counts[k]) / count) ** 2 for k in range(256)]

    return freqs


def sum_frequencies(bytestream):
    ''' Calculate the sum(freq^2) for frequencies of bytestream.

    :param bytestream: Bytes to examine. Use bytearray for sanity.
    '''
    if bytestream is None or len(bytestream) < 1:
        raise ValueError('empty bytestream')

    return sum(get_frequencies(bytestream))


def split_bytes(step, bytestream):
    ''' Split a bytestream into step sections.

    :param step: Number of sections to split into.
    :param bytestream: Bytes to split. Use bytearray for sanity.
    '''
    if bytestream is None or len(bytestream) < 1:
        raise ValueError('empty bytestream')
    if step < 1:
        raise ValueError('step must be > 0')

    sections = []
    for i in range(step):
        sections.append([bytestream[x] for x in range(i, len(bytestream), step)])

    return sections


def naiive_guess_keylen(min_key, max_key, ciphertext):
    ''' Attempt to naiively guess the length of the key used to encrypt ciphertext.

    This is considered naiive because it doesn't take into account the known
    frequencies of letters in English text. Hopefully the result will be good
    enough.

    :param min_key: Minimum key length to test.
    :param max_key: Maximum key length to test.
    :param ciphertext: The ciphertext we're examining. Use bytearray for sanity.
    '''
    if ciphertext is None or len(ciphertext) == 0:
        raise ValueError('You must specify a ciphertext.')
    if min_key > max_key or min_key < 1:
        raise ValueError('min key must be 1 or larger; max key must be >= min key')

    if isinstance(ciphertext, str):
        ciphertext = bytearray(ciphertext)
    elif isinstance(ciphertext, unicode):
        ciphertext = bytearray(ciphertext.encode('utf-8'))

    idx = min_key
    best_len = 0
    best_freq = 0.0
    while idx <= max_key:
        chunks = split_bytes(idx, ciphertext)
        chunk_sums = [sum_frequencies(chunks[x]) for x in range(len(chunks))]

        avg_freq = sum(chunk_sums) / float(len(chunk_sums))
        if avg_freq > best_freq:
            best_len = idx
            best_freq = avg_freq

        idx += 1

    return best_len


def guess_keylen(min_key, max_key, ciphertext):
    ''' Attempt to guess the length of the key using English character frequency.

    :param min_key: Minimum key length to test.
    :param max_key: Maximum key length to test.
    :param ciphertext: The ciphertext we're examining. Use bytearray for sanity.
    '''
    if ciphertext is None or len(ciphertext) == 0:
        raise ValueError('You must specify a ciphertext.')
    if min_key > max_key or min_key < 1:
        raise ValueError('min key must be 1 or larger; max key must be >= min key')

    if isinstance(ciphertext, str):
        ciphertext = bytearray(ciphertext)
    elif isinstance(ciphertext, unicode):
        ciphertext = bytearray(ciphertext.encode('utf-8'))

    idx = min_key
    best_len = 0
    best_delta = 100.0
    while idx <= max_key:
        chunks = split_bytes(idx, ciphertext)
        chunk_freqs = [get_frequencies(x) for x in chunks]

        # There's probably a more clever method, but this is clear...
        freqs = []
        for i in range(256):
            freqs.append(sum([float(chunk_freqs[x][i]) for x in range(idx)]) / float(idx))

        # Compare the top x values to the top x frequencies of letters in
        # English text.
        freq_sum = sum([x for x in reversed(sorted(freqs))][:len(ETAOIN_SHRDLU)])
        delta = abs(ETAOIN_SUM - freq_sum)
        if delta < best_delta:
            best_delta = delta
            best_len = idx

        idx += 1

    return best_len


def guess_xor_key(keylen, ciphertext, print_me=True):
    ''' Guess the key XOR'd with ciphertext.

    :param keylen: Length of the key in bytes.
    :param ciphertext: The text we're attempting to decrypt. Use bytearray for sanity.
    :param print_me: Print guesses to use brain for pattern matching.
    '''
    if keylen < 1:
        raise ValueError('key length must be > 0')

    if isinstance(ciphertext, str):
        ciphertext = bytearray(ciphertext)
    elif isinstance(ciphertext, unicode):
        ciphertext = bytearray(ciphertext.encode('utf-8'))

    chunks = split_bytes(keylen, ciphertext)
    # keybytes = [guess_keybyte(chunks[x]) for x in range(len(chunks))]
    keybytes = [guess_keybyte2(chunks[x]) for x in range(len(chunks))]

    if print_me:
        for idx in range(keylen):
            for a_byte in keybytes[idx]:
                print_byte_guess(chunks[idx], a_byte, idx, keylen)

    return keybytes


def print_byte_guess(stream, guess, offset, keylen):
    ''' Print stream decrypted by guess, with blanks for the unknown bytes.

    :param stream: A ciphertext stream.
    :param guess: A guessed key byte.
    :param idx: Offset of this stream in the full ciphertext.
    :param keylen: Guessed length of the key.
    '''
    plaintext = decrypt(bytearray([guess]), stream)
    if not is_printable(plaintext):
        return
    output = ['{0}{1}{2}'.format(' ' * offset, chr(plaintext[x]), ' ' * (keylen - offset)) for x in range(len(plaintext))]
    print('=' * 78)
    print('{0} = {1}? ->'.format(offset, hex(guess)))
    print(''.join(output))
    _ = raw_input('Hit Enter.')


def is_printable(bytestream):
    ''' Are all bytes in bytestream printable ASCII?

    :param bytestream: Bytes to check.
    '''
    for check in bytestream:
        if check not in PRINTABLE_BYTES:
            return False

    return True


def guess_keybyte(bytestream):
    ''' Guess the best byte used as a key on bytestream.

    WARNING: Can return a tuple if multiple bytes look equally good.

    :param bytestream: Stream of ciphertext bytes to examine.
    '''
    if bytestream is None or len(bytestream) < 1:
        raise ValueError('empty bytestream')

    freqs = []
    for idx in range(256):
        testkey = bytearray([idx] * len(bytestream))
        testtext = bytearray([bytestream[x] ^ testkey[x] for x in range(len(bytestream))])

        # If the testtext has unprintable characters, this one gets 0.
        if not is_printable(testtext):
            freqs.append(0.0)
        else:
            freqs.append(sum_frequencies(testtext))

    best_freq = max(freqs)  # TODO: Maybe round freqs to 5 decimals instead of 'exact'?
    keybytes = []
    for idx in range(256):
        if freqs[idx] == best_freq:
            keybytes.append(idx)

    return keybytes


def guess_keybyte2(bytestream):
    ''' Guess the best byte used as a key on bytestream, using English letter frequencies.

    WARNING: Can return a tuple if multiple bytes look equally good.

    :param bytestream: Stream of ciphertext bytes to examine.
    '''
    if bytestream is None or len(bytestream) < 1:
        raise ValueError('empty bytestream')

    best_delta = 100.0
    deltas = []
    for idx in range(256):
        testkey = bytearray([idx] * len(bytestream))
        testtext = bytearray([bytestream[x] ^ testkey[x] for x in range(len(bytestream))])

        freqs = get_frequencies(testtext)

        # Compare the top x values to the top x frequencies of letters in
        # English text.
        freq_sum = sum([x for x in reversed(sorted(freqs))][:len(ETAOIN_SHRDLU)])
        delta = abs(ETAOIN_SUM - freq_sum)
        deltas.append(delta)
        if delta < best_delta:
            best_delta = delta

    keybytes = []
    for idx in range(256):
        if deltas[idx] == best_delta:
            keybytes.append(idx)

    return keybytes


def combine(seq1, seq2):
    ''' Combine two iterables. '''
    for idx1 in seq1:
        for idx2 in seq2:
            if isinstance(idx1, tuple):
                yield idx1 + (idx2,)
            else:
                yield (idx1, idx2)


def decrypt(enc_key, ciphertext):
    ''' Decrypt ciphertext with the given encryption key.

    :param enc_key: Encryption key. Use bytearray for sanity.
    :param ciphertext: Data to decrypt. Use bytearray for sanity.
    '''
    idx = 0
    plaintext = bytearray(len(ciphertext))
    while idx < len(ciphertext):
        plaintext[idx] = enc_key[idx % len(enc_key)] ^ ciphertext[idx]
        idx += 1

    return plaintext


def main():
    ''' Try to decipher CIPHERTEXT. '''
    ciphertext = bytearray.fromhex(CIPHERTEXT.encode('utf-8'))

    # Ok, so from running the code below, it looks like naiive_guess_keylen()
    # and guess_keylen() are both correct at 7 bytes.
    #
    # Specific key bytes chosen by running guess_keybyte2() modified to print
    # the results of each byte, then using my brain to decide which byte is
    # most likely. Guessing the first word in the plaintext was key here. :)
    keybytes = bytearray([0xba, 0x1f, 0x91, 0xb2, 0x53, 0xcd, 0x3e])
    plaintext = decrypt(keybytes, ciphertext)
    print('plaintext: {0}'.format(plaintext))
    raise KeyboardInterrupt

    # These return the same key length for this ciphertext, so either:
    #
    # 1) The naiive_guess_keylen() works pretty well.
    # 2) The guess_keylen() makes the same mistake.
    #
    # keylen = naiive_guess_keylen(1, 13, ciphertext)
    keylen = guess_keylen(1, 13, ciphertext)
    print('Apparent key length: {0}'.format(keylen))

    keybytes = guess_xor_key(keylen, ciphertext)
    # plaintext = decrypt(keybytes, ciphertext)
    # print('{0} -> {1}'.format(keybytes, plaintext))

    # Our CIPHERTEXT is comparitively small, so we've got a number of
    # candidates for each byte of the key.
    all_keys = keybytes[0]
    for idx in range(1, keylen):
        all_keys = [x for x in combine(all_keys, keybytes[idx])]
    print('# of possible keys: {0}'.format(len(all_keys)))

    # This is going to be a lot of output...
    skipped = 0
    for a_key in all_keys:
        # Let's assume that plaintext[0] needs to be an upper-case letter.
        plaintext = decrypt(a_key, ciphertext)
        if plaintext[0] in UPPERCASE_BYTES:
            print('{0} -> {1}'.format(a_key, plaintext))
        else:
            skipped += 1
            if skipped % 1000 == 0:
                print('{0} skipped keys'.format(skipped))


if __name__ == '__main__':
    main()
