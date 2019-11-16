'''
Created on 2012-03-17

@author: chrish
'''

m1 = "attack at dawn"
m2 = "attack at dusk"

ct1 = "6c73d5240a948c86981bc294814d".decode('hex')

from useful.bits import strxor

k = strxor(ct1,m1)

ct2 = strxor(k,m2)

print ct2.encode('hex')
