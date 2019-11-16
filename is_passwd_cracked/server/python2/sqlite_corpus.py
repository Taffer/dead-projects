'''
Create a corpus stored in SQLite compatible with is_password_cracked.Checker.

Created on Sep 13, 2014

@author: https://github.com/Taffer
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import sqlite3
import unittest


class Corpus(object):
    ''' Manage a password corpus stored in SQLite. '''
    def __init__(self, sqlite_connection, query='SELECT COUNT(*) FROM passwd WHERE plaintext = ?;'):
        ''' Create a SQLite-based Corpus.

        Uses the specified query to look up plaintext passwords in a table;
        if you supply a query, it must accept one parameter (the plaintext
        password) and return 0 if the password is not present, and any other
        value if the password does exist in the table.

        :param sqlite_file: A sqlite3 Connection object.
        :param query: A query that returns 0 when a password is not present, not-0 when it is present.
        '''
        self.database = sqlite_connection
        self.cursor = self.database.cursor()
        self.query = query

    def __contains__(self, item):
        ''' Return True if item is in the corpus, else False.

        :param item: The item to check for.
        '''
        result = self.cursor.execute(self.query, (item,))
        if result.fetchone() == (0,):
            return False

        return True

    @staticmethod
    def from_file(sqlite_file, query='SELECT COUNT(*) FROM passwd WHERE plaintext = ?;'):
        ''' Create a Corpus from a given SQLite file.

        :param sqlite_file: Path to a SQLite file containing a password database.
        :param query: A query that returns 0 when a password is not present, not-0 when it is present.
        '''
        database = sqlite3.connect(sqlite_file)
        return Corpus(database, query)


class CorpusTests(unittest.TestCase):
    ''' Test the SQLite Corpus. '''
    def test_empty(self):
        ''' Test an empty database. '''
        database = sqlite3.connect(':memory:')
        cursor = database.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS passwd (plaintext text);')
        database.commit()

        sqlite_corpus = Corpus(database)
        self.assertFalse('password' in sqlite_corpus, '"password" should not be in an empty corpus')

        database.close()

    def test_obvious(self):
        ''' Test a corpus with some obvious values in it. '''
        database = sqlite3.connect(':memory:')
        cursor = database.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS passwd (plaintext text);')
        cursor.execute("INSERT INTO passwd VALUES ('password');")
        cursor.execute("INSERT INTO passwd VALUES ('12345');")
        database.commit()

        sqlite_corpus = Corpus(database)
        self.assertTrue('password' in sqlite_corpus, '"password" should be in the obvious corpus')
        self.assertTrue('12345' in sqlite_corpus, '"12345" should be in the obvious corpus')
        self.assertFalse('hunter' in sqlite_corpus, '"hunter" should not be in the obvious corpus')

        database.close()
