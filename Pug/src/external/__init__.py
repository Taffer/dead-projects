# -*- coding: utf-8 -*-
'''
Created on Oct 19, 2014

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

__version__ = '0.0.1'

_EXTERNAL_PATHS = ('CommonMark',
                   'emoji',
                   'is_passwd_cracked/server/python2')


def external_paths():
    ''' Add external paths to sys.path if necessary. '''
    for ext_path in _EXTERNAL_PATHS:
        prefix = os.path.dirname(__file__)
        full_path = os.path.join(prefix, ext_path)
        if full_path not in sys.path:
            sys.path.append(full_path)

external_paths()


import CommonMark  # pylint: disable=F0401
import emoji  # pylint: disable=F0401
import is_password_cracked  # pylint: disable=F0401
