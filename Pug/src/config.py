'''
Pug general configuration settings.

To override any of these, copy the setting to a file named local_config.py in
the same directory. Any setting in local_config.py will override any setting
in this config.py file.

Created on Oct 11, 2014

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = '0.0.1'

# Bootstrap - http://getbootstrap.com/
#
# Set BOOTSTRAP_CDN to True if you want to load Bootstrap's files from their
# CDN, otherwise they'll be loaded from the local copies. Using the local
# copies is more secure.
BOOTSTRAP_CDN = False

BOOTSTRAP_LOCAL = {'stylesheet': 'bootstrap-3.2.0-dist/css/bootstrap.min.css',
                   'theme': 'bootstrap-3.2.0-dist/css/bootstrap-theme.min.css',
                   'script': 'bootstrap-3.2.0-dist/css/bootstrap.min.js'
                   }

BOOTSTRAP_REMOTE = {'stylesheet': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css',
                    'theme': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css',
                    'script': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js'
                    }

# Compatibility for ye olde browsers that people are forced to use.
#
# Set HTML5_CDN to True if you want these loaded from their CDN, otherwise
# they'll be loaded from the local copies. Using the local copies is more
# secure.
HTML5_CDN = False

HTML5_LOCAL = {'html5shiv': 'js/html5shiv.min.js',
               'respond': 'js/respond.min.js'
               }

HTML5_REMOTE = {'html5shiv': 'https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js',
                'respond': 'https://oss.maxcdn.com/respond/1.4.2/respond.min.js',
                }

# jQuery
#
# Set JQUERY_CDN to True if you want these loaded from their CDN, otherwise
# they'll be loaded from the local copies. Using the local copies is more
# secure.
JQUERY_CDN = False

JQUERY_LOCAL = 'js/jquery.min.js'
JQUERY_REMOTE = 'https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js'

# External modules
#
# Path to the external modules. This will be made into an absolute path before
# it's added to Python's module path.
EXTERNAL_MODULES = './external'
