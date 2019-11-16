'''
Created on 2012-04-10

@author: chrish

A web site administrator found these log entries in a web server log. After 
some digging, the admin realized that the first log entry is an AES CBC 
encryption with random IV of some secret data (the ciphertext is hex encoded 
and appears right after the "GET /"). The secret data contains private user 
data that should only be known to the web site.

After more digging the admin realized that the web site is vulnerable to a 
CBC padding oracle attack. In particular, when a decrypted CBC ciphertext 
ends in an invalid pad the web server returns a 403 error code (forbidden 
request). When the CBC padding is valid, but the message is malformed the web 
server returns a 404 error code (URL not found). To her horror, the admin 
realized that the log entries following the first entry are a result of a 
remote CBC padding oracle attack on the ciphertext in the first log entry.

See if you can use the given log entries to recover the decryption of the 
ciphertext in the first log entry. Keep in mind that the first ciphertext 
block is the random IV. The decrypted message is ASCII encoded.

The log entries file is available here.

We discussed CBC padding oracle attacks in Lecture 7.6, but if you want to 
read more about them, please see Vaudenay's paper.
'''

log_lines = open("../../Week 4/proj4-log.txt").readlines()
print len(log_lines)
parts = log_lines[0].split()
ct = parts[-3][1:]              # quick and dirty!

attempts = []
for line in log_lines[1:]:
    parts = line.split()
    attempts.append( ( parts[-3][1:33], parts[-3][-32:], parts[-1] ) ) # attempt, status

print "Found", len(attempts), "attempts to decrypt", len(ct), "byte ciphertext."
'''
for each attempt a, a[:32] = pad attack, a[32:] = 32 bytes of the ct
if status = 403, invalid pad
if status = 404, padding valid, message malformed
'''
for (iv,c,status) in attempts:
    if status == '404':
        print iv,c
