'''
Here is the opening stanza of an important work of the English language:

Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal

Encrypt it, under the key "ICE", using repeating-key XOR.

In repeating-key XOR, you'll sequentially apply each byte of the key; the first
byte of plaintext will be XOR'd against I, the next C, the next E, then I again
for the 4th byte, and so on.

It should come out to:

0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

Created on Sep 1, 2014

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import cryptopals


def main():
    ''' Encrypt some strings with repeating-key XOR. '''
    input1 = bytearray("Burning 'em, if you ain't quick and nimble".encode('ascii'))
    expected1 = bytearray.fromhex('0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622632427276527')
    input2 = bytearray('I go crazy when I hear a cymbal'.encode('ascii'))
    expected2 = bytearray.fromhex('2b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f')
    input_key = bytearray('ICE'.encode('ascii'))

    output1 = cryptopals.repeating_key_xor(input_key, input1)
    output1e = cryptopals.repeating_key_xor(input_key, output1)
    output2 = cryptopals.repeating_key_xor(input_key, input2)
    output2e = cryptopals.repeating_key_xor(input_key, output2)

    # So, this is weird... I believe I've implemented it correctly but it
    # doesn't match the expected output. Reversing the encryption works
    # fine so... are you trolling us, Matasano? Or did I screw something up?
    #
    # As it turns out, the expected strings are incorrect; if you decode:
    #
    # 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622632427276527
    # 2b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f
    #
    # You get:
    #
    # Burning 'em, if you ain't quick and n
    # ble\nI go crazy when I hear a cymbal
    #
    # Actual expected should be:
    #
    # 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20
    # 0063222663263b223f30633221262b690a652126243b632469203c24212425

    print('input1    : {0}'.format(str(input1)))
    print('output1   : {0}'.format(str(output1).encode('hex')))
    print('exptected1: {0}'.format(str(expected1).encode('hex')))
    print('reversed  : {0}'.format(str(output1e)))
    print('')
    print('input2    : {0}'.format(str(input2)))
    print('output2   : {0}'.format(str(output2).encode('hex')))
    print('exptected2: {0}'.format(str(expected2).encode('hex')))
    print('reversed  : {0}'.format(str(output2e)))


if __name__ == '__main__':
    main()
