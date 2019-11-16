#!/usr/bin/env python2.7
# encoding: utf-8
''' Walk the given paths, looking for missing cover art.

This assumes that you've got a UTF-8 filesystem and a terminal that can print
UTF-8 characters.
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import re
import sys
import time


class CoverSearch(object):
    ''' Search for acceptable covers in a directory tree. '''

    # Acceptable cover image names. These are regexes, obviously.
    _COVER_NAMES = [r'artwork\.(jpg|png)',
                    r'cover\.(jpg|png)',  # MusicBrainz Picard names them thusly.
                    r'folder\.(jpg|png)',
                    r'front\.(jpg|png)'
                    ]

    def __init__(self, cover_patterns=None, ignore_case=True, verbose=0):
        ''' Create a CoverSearch.

        If you pass your own iterable of cover_patterns, those regexes will
        be compiled with the re.IGNORECASE option if ignore_case is True;
        desktop filesystems are mostly case-insensitive, which is why it's
        True by default. Set it to False if you've got a UNIX filesystem.

        :param cover_patterns: Iterable of regular expressions for matching cover names.
        :param ignore_case: If true, ignore case while comparing.
        :param verbose: The verbosity level (0 = quiet).
        '''
        self.verbose = verbose

        if ignore_case:
            flag = re.IGNORECASE
        else:
            flag = 0

        if cover_patterns is None:
            self.cover_patterns = [re.compile(x, flag) for x in CoverSearch._COVER_NAMES]
        else:
            self.cover_patterns = [re.compile(x, flag) for x in cover_patterns]

    def find_names(self, names):
        ''' Return True if one of the names matches one of the patterns.

        :param names: An iterable of name strings.
        '''
        # FIXME: There must be a smarter way of doing this... either a smart way
        #        to glue everything together into one match() or a way to do
        #        "if regex in sequence"...
        for name in names:
            for pattern in self.cover_patterns:
                if pattern.match(name) is not None:
                    return True

        # Worst-case is len(names) * len(self.cover_patterns) iterations.
        return False

    def cover_search(self, path):
        ''' Walk the given path, looking for missing cover art.

        Returns a list of paths that don't contain a cover.

        :param path: The path to recursively search.
        '''
        no_covers = []
        for (root, dirs, files) in os.walk(path, followlinks=True):
            # Skip dirs with no files.
            if len(files) == 0:
                if self.verbose > 1:
                    print('{0} has no files.'.format(root))
                continue

            # Skip .path directories.
            remove_dotpaths = []
            for dirname in dirs:
                uni_dirname = dirname.decode('utf8', 'xmlcharrefreplace')
                if uni_dirname.startswith('.'):
                    if self.verbose > 1:
                        print('Skipping {0}...'.format(uni_dirname).encode('utf8', 'xmlcharrefreplace'))
                    remove_dotpaths.append(dirname)
            for dirname in remove_dotpaths:
                dirs.remove(dirname)

            uni_files = [x.decode('utf8', 'xmlcharrefreplace') for x in files]
            found = self.find_names(uni_files)
            if found and self.verbose > 2:
                uni_root = root.decode('utf8', 'xmlcharrefreplace')
                print('Found cover for {0}.'.format(uni_root).encode('utf8', 'xmlcharrefreplace'))
            elif not found:
                if self.verbose > 1:
                    uni_root = root.decode('utf8', 'xmlcharrefreplace')
                    print('No covers in {0}.'.format(uni_root).encode('utf8', 'xmlcharrefreplace'))
                no_covers.append(root)

        return no_covers


def main(argv):
    ''' Walk the paths, looking for missing cover art. '''
    parser = argparse.ArgumentParser(description="Find albums that appear to be missing cover art.")
    parser.add_argument('-v', '--verbose', dest='verbose', help='Be verbose.', action='count')
    parser.add_argument(dest='paths', help='Paths to search.', metavar='path', nargs='+')

    args = parser.parse_args(argv)

    cover_search = CoverSearch(verbose=args.verbose)

    no_covers = set([])
    start_walk = time.time()
    for arg_path in args.paths:
        no_covers.update(cover_search.cover_search(arg_path))

    if args.verbose > 0:
        print('{0:f} seconds to walk the directories.'.format(time.time() - start_walk))

    # Print the folders missing covers.
    if len(no_covers) == 1:
        print('1 directory missing covers:')
    elif len(no_covers) > 0:
        print('{0} directories missing covers:'.format(len(no_covers)))

    for path in sorted(no_covers):
        print(path)


if __name__ == "__main__":
    main(sys.argv[1:])
