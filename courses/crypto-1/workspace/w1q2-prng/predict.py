'''
Created on 2012-03-15

@author: chrish
'''

from prng import WeakPrng, P

values = [
          210205973,
          22795300,
          58776750,
          121262470,
          264731963,
          140842553,
          242590528,
          195244728,
          86752752
          ]

''' So, given the values, figure out x and y seeds in the WeakPrng, then you can predict the next value.
'''

w = WeakPrng( P )

# Print the output:
w.x = 89059908
w.y = values[0] ^ 89059908

for i in xrange( 0, len(values ) ):
    print i, w.nextPrng()

raise SystemExit

# find the seed:
print "Running"
for i in xrange(0,P):

    w.x = i
    w.y = values[0] ^ i

    if w.nextPrng() == values[1]:
        print "Candidate:", i
        break
