'''
Created on 2012-04-21

@author: chrish
'''

import math
import numbthy
import lrange


p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333

B = 2L ** 20L

w5hash = {}

# Find x such that h=g**x in Zp.


def invmodp(a, p):
    '''
    The multiplicitive inverse of a in the integers modulo p.
    Return b s.t.
    a * b == 1 mod p

    From: http://code.activestate.com/recipes/576737-inverse-modulo-p/
    '''

    r = a
    d = 1L
    for count in lrange.lrange(p):
        d = ((p // r + 1L) * d) % p
        r = (d * a) % p
        if r == 1L:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d


def build_hash():
    ''' Build a hash of h/g**x for x = 0 ... B
    '''
    inv_g = invmodp( g, p )

    for x1 in xrange(0, B):
        if x1 % 10000 == 0:
            print('add: ' + str(x1))

        #val = (h / g**x1) % p
        #val = (h * (g ** -x1)) % p
        #val = (h / numbthy.powmod( g, x1, p )) % p
        #val = (h * numbthy.powmod(g, -x1, p)) % p
        val = (h * numbthy.powmod(inv_g, x1, p)) % p

        w5hash[val] = x1


def search_hash():
    ''' search for g ** B ** x in hash for x = 0 ... B
    '''
    #g_B = numbthy.powmod(g, B, p)
    for x0 in xrange(0, B):
        if x0 % 10000 == 0:
            print('search: ' + str(x0))

        #val = (g ** (B * x0)) % p
        val = numbthy.powmod(g, B * x0, p)
        #val = numbthy.powmod(g_B, x0, p)

        if w5hash.has_key(val):
            print "x0:", x0
            print "x1:", w5hash[val]
            return ( x0, w5hash[val] )


def find_x((x0,x1)):
    return ( x0 * B + x1 ) % p


def main():
    print( 'Building hash...' )
    build_hash()

    print( 'Searching hash...' )
    result = search_hash()

    print( 'Calculating x...' )
    x = find_x(result)

    print( x )

    print "g^x % p", numbthy.powmod(g, x, p)
    print "      h", h


if __name__ == '__main__':
    main()
