#!/usr/bin/env python
# -*- coding: utf8 -*-

import gmpy2
one = gmpy2.mpz('1')


def factor_n1():
	'''
	Factoring challenge #1:

	The following modulus N is a products of two primes p and q where
	|p−q| < 2N^(1/4). Find the smaller of the two factors and enter it
	as a decimal integer.
	'''
	N = gmpy2.mpz('179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581')

	A = gmpy2.add(gmpy2.isqrt(N), one)

	x = gmpy2.isqrt(gmpy2.sub(gmpy2.mul(A, A), N))

	print 'Calculating first factors...'

	ticks = 0
	while True:
		p = gmpy2.sub(A, x)
		q = gmpy2.add(A, x)

		if gmpy2.is_prime(p) and gmpy2.is_prime(q) and gmpy2.mul(p, q) == N:
			print "p =", p, "q =", q, "ticks =", ticks
			return
		else:
			x = gmpy2.add(x, one)
			ticks += 1
			if ticks % 10000 == 0:
				print 'ticks:', ticks


def factor_n2():
	'''
	Factoring challenge #2:

	The following modulus N is a products of two primes p and q where
	|p−q| < 2^11 N^(1/4). Find the smaller of the two factors and enter
	it as a decimal integer.

	Hint: In this case A−sqrt(N)<2^20 so try scanning for A from sqrt(N)
	upwards, until you succeed in factoring N.
	'''
	N = gmpy2.mpz('648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877')

	A = gmpy2.add(gmpy2.isqrt(N), one)

	x = gmpy2.isqrt(gmpy2.sub(gmpy2.mul(A, A), N))

	print 'Calculating second factors...'

	ticks = 0
	q=gmpy2.mpz(A)
	while True:
		q = gmpy2.next_prime(q) #gmpy2.add(A, x)
		p = gmpy2.sub(A, gmpy2.sub(q, A)) #gmpy2.sub(A, x)

		#print "p is prime?", gmpy2.is_prime(p)
		#print "q is prime?", gmpy2.is_prime(q)

		#print "p*q:"
		#print gmpy2.mul(p,q)
		#print "N:"
		#print N
		#return

		if gmpy2.is_prime(p) and gmpy2.is_prime(q):
			print "p =", p, "q =", q, "ticks =", ticks
			if gmpy2.mul(p, q) == N:
				print 'Done!'
				return
		else:
			ticks += 1
			if ticks % 10000 == 0:
				print 'ticks:', ticks


def factor_n3():
	'''
	Factoring challenge #3: (extra credit)

	The following modulus N is a products of two primes p and q where
	|3p−2q| < N^(1/4). Find the smaller of the two factors and enter it as
	a decimal integer.

	Hint: Use the calculation below to show that sqrt(6N) is close to
	(3p+2q)/2 and then adapt the method above to factor N.
	'''
	N = gmpy2.mpz('720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929')

if __name__ == '__main__':
	factor_n2()
