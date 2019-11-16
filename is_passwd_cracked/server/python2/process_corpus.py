#!/usr/bin/env python2.7
'''
Process one or more password list files into a corpus of unique passwords.

Requirements:
    * Python 2.7
    * https://github.com/ahupp/python-magic (pip install python-magic)

Created on Sep 13, 2014

@author: https://github.com/Taffer
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import bz2
import gzip
import hashlib
import magic
import sqlite3
import sys


def open_magic(filename):
    ''' Use magic to open bzip2'd, gzip'd, or uncompressed text files.

    :param filename: File to open.
    '''
    mime_type = magic.from_file(filename, mime=True)
    file_obj = None
    if mime_type == 'application/x-bzip2':
        file_obj = bz2.BZ2File(filename, 'rU')
    elif mime_type == 'application/x-gzip':
        file_obj = gzip.GzipFile(filename, 'rU')
    elif mime_type == 'text/plain':
        file_obj = open(filename)
    else:
        raise IOError('Unknown file type {0}: {1}'.format(mime_type, filename))

    return file_obj


def main():
    arg_parser = argparse.ArgumentParser(description='Import passwords listed one per line from the given files.',
                                         epilog="Corpus is printed to stdout if --sqlite or --file isn't specified.")
    arg_parser.add_argument('input_file', type=str, nargs='+',
                            help='Input password file (uncompressed, gzip, or bzip2), one password per line.')
    arg_parser.add_argument('--sha1', dest='use_sha1', action='store_true', default=False,
                            help='Store SHA1s of each password instead of plaintext.')
    output_group = arg_parser.add_argument_group()
    output_group.add_argument('--sqlite', dest='sqlite_file', type=str, nargs=1, help='Store the corpus to a new SQLite database.')
    output_group.add_argument('--file', dest='output_file', type=str, nargs=1, help='Store the corpus to a new file.')
    args = arg_parser.parse_args()

    unique_passwords = set()

    for filename in args.input_file:
        sys.stderr.write('Opening {0}...\n'.format(filename))
        with open_magic(filename) as passfile:
            total_lines = 0
            previous_unique = len(unique_passwords)

            for line in passfile.readlines():
                total_lines += 1
                this_pass = line.strip().lower()
                if args.use_sha1:
                    this_pass = hashlib.sha1(this_pass)
                unique_passwords.add(this_pass)

            sys.stderr.write('\t{0} new passwords in {1} lines\n'.format(len(unique_passwords) - previous_unique, total_lines))

    sys.stderr.write('{0} unique passwords found in {1} files.\n'.format(len(unique_passwords), len(args.input_file)))

    if args.sqlite_file:
        database = sqlite3.connect(args.sqlite_file[0])
        cursor = database.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS passwd (passwd text);')
        database.commit()

        # Sure this is inefficient, but I don't care.
        for password in unique_passwords:
            cursor.execute('INSERT INTO passwd VALUES(?);', (password,))
        database.commit()
        database.close()
    else:
        output_stream = sys.stdout
        if args.output_file:
            output_stream = open(args.output_file[0], 'w')

        for password in unique_passwords:
            output_stream.write('{0}\n'.format(password))

        if output_stream != sys.stdout:
            output_stream.close()


if __name__ == '__main__':
    main()
