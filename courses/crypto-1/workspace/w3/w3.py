'''
Created on 2012-04-01

@author: chrish
'''

import gdbm
from Crypto.Hash import SHA256

# Birthday attack:
#
# 1) 2^(n/2) distinct random messages
# 2) calculate hash for each; if hash exists in DB already, done
# 3) goto 1

fifty_bits = 0x3ffffffffffff

def get50bits(s):
    ''' Given a hex-encoded bytestream, return 50 least-significant bits.
    '''
    return hex(int(s[-14:],16) & fifty_bits)


def main():
    keys = gdbm.open("/tmp/w3.keys", "nfu")

    for i in xrange(0, 2**25):
        s = str(i)

        hasher = SHA256.new()
        hasher.update(s)
        k = get50bits(hasher.digest().encode('hex'))

        if i % 10240 == 0:
            print "Generating...", i, k

        try:
            print keys[k], "collides with", s, "using key", k
        except KeyError:
            keys[k] = s

    x = 2**25
    counter = 0
    while counter < 5:
        x += 1

        s = str(x)

        hasher = SHA256.new()
        hasher.update(s)
        k = get50bits(hasher.digest().encode('hex'))

        if x % 10240L == 0L:
            print "Searching...", s, k

        try:
            print keys[k], "collides with", s, "using key", k
        except KeyError:
            pass


if __name__ == "__main__":
    main()

