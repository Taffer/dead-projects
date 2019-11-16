#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# OpenAchivement web service package.

'''
Created on Mar 6, 2014

@author: Chris
'''

import achievement.config
import flask
import sys

try:
    import achievement.local_config
    local_config = achievement.local_config
except ImportError:
    local_config = None


class OpenAchivementServer(flask.Flask):
    def __init__(self):
        super(OpenAchivementServer, self).__init__(__name__)

        # Load our configuration.
        self.config.from_object(achievement.config)
        if local_config is not None:
            # Override with local configuration, if any.
            self.config.from_object(local_config)


app = OpenAchivementServer()


def main():
    ''' Run the OpenAchievement server. '''
    if '--help' in sys.argv:
        print('Use --debug to enable debugging.')
        print('Use --local to allow access from localhost only.')

    if '--debug' in sys.argv:
        # Absolutely DO NOT turn this on in production unless you want
        # arbitrary Python executing in your cloud.
        app.debug = True
        port = app.config['DEBUG_PORT']
    else:
        port = app.config['SERVER_PORT']

    if '--local' in sys.argv:
        app.run(port=port)
    else:
        app.run(host='0.0.0.0', port=port)  # Note that this is visible to everyone on your subnet.


if __name__ == '__main__':
    main()
