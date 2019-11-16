#!/usr/bin/env python2.7
'''
Run a local Pug server for debugging purposes.

Note that this toy webserver is not suitable to testing or production. Use
a real WSGI host for those.

Created on Oct 11, 2014

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = '0.0.1'

import server


def main():
    ''' Create a Pug server and run it in debug mode. '''
    pug = server.app
    print('Starting debug Pug on: http://localhost:8000/')
    pug.run(debug=True, port=8000)


if __name__ == '__main__':
    main()
