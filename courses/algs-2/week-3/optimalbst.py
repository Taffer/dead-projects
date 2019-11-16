#!/usr/bin/env python
# Attempt to calculate the min avg. search time for an optimal BST

A = []
for i in range(8):  # 0 - 7
	A.append([0] * 8)
print A

# n = 7, nodes 1 - 7 are the data, nodes[0] = junk
#nodes = [0, 0.05, 0.4, 0.08, 0.04, 0.10, 0.10, 0.23]
nodes = [0, .2, .05, .17, .1, .2, .03, .25]

def get(i, j):
	if i >= len(A):
		return 0
	if j >= len(A[i]):
		return 0
	return A[i][j]

for S in range(7):
	for i in range(1, 8):
		if (i + S) >= len(A[i]):
			continue
		print 'A[%s][%s]' % (i, i + S)
		A[i][i + S] = min([(sum([nodes[k] for k in range(i, i + S)]) + get(i, r - 1) + get(r + 1, i + S)) for r in range(i, i + S + 1)])

for row in A:
	print row

