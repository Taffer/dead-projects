'''
WSGI application stub for Pug.

Created on Oct 11, 2014

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = '0.0.1'

import os
import sys

from config import EXTERNAL_MODULES  # @UnusedImport
try:
    from local_config import EXTERNAL_MODULES  # pylint: disable=F0401
except ImportError:
    # No EXTERNAL_MODULES in local_config (or no local_config).
    pass


def get_pug_path():
    ''' Return the directory that this file is in. '''
    pug_path = os.path.abspath(os.path.dirname(os.__file__))

    return pug_path


def fix_pug_path():
    ''' Fix sys.path so it includes this file's directory.

    This simplifies configuration so you don't need to muck with PYTHONPATH
    unless you want to store your local_config files somewhere else.
    '''
    pug_path = get_pug_path()
    if pug_path not in sys.path:
        sys.path.insert(0, pug_path)

    fix_externals_path()


def fix_externals_path():
    ''' Fix sys.path so it includes the projects in the external directory. '''
    module_dirs = ('CommonMark',
                   'emoji',
                   'is_passwd_cracked/server/python2'
                   )
    externals = [os.path.join(EXTERNAL_MODULES, module_dirs[x]) for x in module_dirs]
    pug_path = get_pug_path()

    for mod in externals:
        if os.path.isabs(mod):
            if mod not in sys.path:
                sys.path.append(mod)
        else:
            if os.path.isabs(EXTERNAL_MODULES):
                mod = os.path.normpath(os.path.join(EXTERNAL_MODULES, mod))
            else:
                mod = os.path.normpath(os.path.join(pug_path, EXTERNAL_MODULES, mod))

            if mod not in sys.path:
                sys.path.append(mod)


fix_pug_path()


from server import app as application  # @UnusedImport pylint: disable=W0611
