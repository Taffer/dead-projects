'''
Check to see if a given password is known to be previously cracked.

The Checker object in here will support a corpus supplied as any data type
that supports the 'in' keyword (list, set, etc.). The from_file() static
method pulls a corpus from a text file as a convenience.

Created on Sep 13, 2014

@author: https://github.com/Taffer
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import unittest


class Checker(object):
    ''' Check to see if a given password has been previously cracked. '''
    def __init__(self, corpus):
        ''' Create an is_password_cracked.Checker.

        :param corpus: A password corpus. This must support the 'in' keyword.
        '''
        self.corpus = corpus

    def is_password_cracked(self, plaintext):
        ''' Is the given plaintext password known to be previously cracked?

        Returns True if plaintext is known to be cracked, False otherwise.

        :param plaintext: The password to check.
        '''
        return plaintext in self.corpus

    @staticmethod
    def from_file(filename):
        ''' Create a Checker with the corpus found in filename.

        :param filename: Uncompressed corpus, one password per line.
        '''
        corpus = set()
        with open(filename, 'rU') as corpus_file:
            for password in corpus_file.readlines():
                corpus.add(password)

        return Checker(corpus)


class CheckerTests(unittest.TestCase):
    ''' Tests for the Checker class. '''
    def test_from_file(self):
        ''' Test the from_file() method. '''
        checker = Checker.from_file('/dev/null')
        self.assertEqual(len(checker.corpus), 0, 'Corpus should be empty, has {0} entries.'.format(len(checker.corpus)))

    def test_empty(self):
        ''' Test with an empty corpus. '''
        checker = Checker([])
        self.assertFalse(checker.is_password_cracked('password'), '"password" should not be in the empty corpus.')

    def test_obvious(self):
        ''' Test with an obvious corpus. '''
        checker = Checker(['password', '12345'])
        self.assertTrue(checker.is_password_cracked('password'), '"password" should be in the obvious corpus.')
        self.assertTrue(checker.is_password_cracked('12345'), '"12345" should be in the obvious corpus.')
        self.assertFalse(checker.is_password_cracked('hunter'), '"hunter" should not be in the obvious corpus.')
