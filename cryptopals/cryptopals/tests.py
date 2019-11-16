# -*- coding: utf-8 -*-
'''
Created on Feb 10, 2015

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import cryptopals  # PyDev, go home, you're drunk: @UnusedImport
import cryptopals.scoring
import time
import unittest


class TestSet1(unittest.TestCase):
    ''' Test the challenges from Set 1: http://cryptopals.com/sets/1/ '''

    def test_hex2base64(self):
        ''' Test the hex2base64 function from Set 1, Challenge 1. '''
        input_str = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
        expected_str = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

        output_str = cryptopals.hex2base64(input_str)
        self.assertEqual(output_str, expected_str, "converted bytes didn't match expected, it's broken")

    def test_fixed_xor(self):
        ''' Test the fixed_xor() function from Set 1, Challenge 2. '''
        input1 = bytearray.fromhex('1c0111001f010100061a024b53535009181c')
        input2 = bytearray.fromhex('686974207468652062756c6c277320657965')
        expected = bytearray.fromhex('746865206b696420646f6e277420706c6179')

        output = cryptopals.fixed_xor(input1, input2)
        self.assertEqual(output, expected, 'XOR produced invalid output')

    # Speed tests; these are generally pretty slow, so you don't want to run
    # them every time.

    @unittest.skip('Time consuming: bytearray is almost 1.5x faster.')
    def test_hex2base64_speed(self):
        ''' Try to figure out how fast/slow hex2base64 implementations are in Python. '''
        iterations = 1000000
        input_str = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

        def old_hex2base64(hex_string):
            ''' Convert the given hex string to base64 encoded bytes.

            :param hex_string: A string of hexadecimal numbers representing bytes.
            '''
            hex_bytes = hex_string.decode('hex')
            base64_string = base64.b64encode(hex_bytes)

            return base64_string

        idx = 0
        old_start = time.time()
        while idx < iterations:
            _ = old_hex2base64(input_str)
            idx += 1
        old_delta = time.time() - old_start

        idx = 0
        new_start = time.time()
        while idx < iterations:
            _ = cryptopals.hex2base64(input_str)
            idx += 1
        new_delta = time.time() - new_start

        print('bytearray version: {0}s, string.decode version: {1}s'.format(new_delta, old_delta))
        self.assertTrue(new_delta < old_delta, "new {0}s, old {1}s".format(new_delta, old_delta))

    @unittest.skip('Time consuming: bytearray is more than 10x faster.')
    def test_old_fixed_xor(self):
        ''' See if the new bytearray implementation is faster than the old string implementation. '''
        iterations = 100000
        input1_str = '1c0111001f010100061a024b53535009181c'
        input2_str = '686974207468652062756c6c277320657965'
        input1_ba = bytearray.fromhex(input1_str)
        input2_ba = bytearray.fromhex(input2_str)

        def old_fixed_xor(buff1, buff2):
            ''' XOR two equal-length buffers by byte.

            :param buff1: First buffer of hex digits.
            :param buff2: Second buffer of hex digits.
            '''
            if len(buff1) != len(buff2):
                raise ValueError('Buffers must be equal size ({0} vs {1}.'.format(len(buff1), len(buff2)))

            bytes1 = buff1.decode('hex')
            bytes2 = buff2.decode('hex')

            buff3 = ''.join([chr(ord(bytes1[x]) ^ ord(bytes2[x])).encode('hex') for x in xrange(len(bytes1))])

            return buff3

        idx = 0
        old_start = time.time()
        while idx < iterations:
            _ = old_fixed_xor(input1_str, input2_str)
            idx += 1
        old_delta = time.time() - old_start

        idx = 0
        new_start = time.time()
        while idx < iterations:
            _ = cryptopals.fixed_xor(input1_ba, input2_ba)
            idx += 1
        new_delta = time.time() - new_start

        print('bytearray version: {0}s, string version: {1}s'.format(new_delta, old_delta))
        self.assertTrue(new_delta < old_delta, "new {0}s, old {1}s".format(new_delta, old_delta))


class TestScoring(unittest.TestCase):
    ''' Test the string scoring methods created for Set 1, Challenge 3. '''
    def test_naiive_unprintable(self):
        ''' Ignore unprintable strings. '''
        score = cryptopals.scoring.score_naiive(bytearray.fromhex('deadbeef'))
        self.assertEqual(score, 0, 'deadbeef scored {0} instead of 0'.format(score))

    def test_naiive(self):
        ''' Does a string produce a result? '''
        score_alpha = cryptopals.scoring.score_naiive(bytearray('deadbeef is an ASCII string'.encode('ascii')))
        score_punct = cryptopals.scoring.score_naiive(bytearray('... --- ...'.encode('ascii')))

        self.assertGreater(score_alpha, 0, 'ASCII string score is {0}'.format(score_alpha))
        self.assertLess(score_punct, 0, 'Punctuation score is {0}'.format(score_punct))

    def test_naiive_relative(self):
        ''' Test two strings against each other. '''
        score_alpha = cryptopals.scoring.score_naiive(bytearray('deadbeef is an ASCII string'.encode('ascii')))
        score_punct = cryptopals.scoring.score_naiive(bytearray('... --- ...'.encode('ascii')))
        score_deadbeef = cryptopals.scoring.score_naiive(bytearray.fromhex('deadbeef'))

        self.assertGreater(score_alpha, score_punct,
                           'punct ({0}) is greater than ASCII ({1}) somehow'.format(score_punct, score_alpha))
        self.assertGreater(score_alpha, score_deadbeef,
                           'deadbeef ({0}) is greater than ASCII ({1}) somehow'.format(score_deadbeef, score_alpha))

    def test_hamming(self):
        ''' Test the Hamming distance calculator. '''
        str1 = bytearray('this is a test'.encode('ascii'))
        str2 = bytearray('wokka wokka!!!'.encode('ascii'))
        expected = 37

        retval = cryptopals.scoring.hamming_distance(str1, str2)
        self.assertEqual(expected, retval, 'Hamming distance was {0} instead of {1}'.format(retval, expected))


if __name__ == "__main__":
    unittest.main()
