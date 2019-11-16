'''
Pug's server, a WSGI application.

Created on Oct 11, 2014

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = '0.0.1'

import config
import filters
import flask
import jinja2.environment

from flask.templating import render_template

try:
    import local_config  # pylint: disable=F0401
except ImportError:
    local_config = None  # pylint: disable=C0103


class PugServer(flask.Flask):  # pylint: disable=R0904
    ''' Handle processing all of the Pug endpoints. '''

    def __init__(self):
        ''' Constructor '''
        super(PugServer, self).__init__('Pug')

        self.config.from_object(config)
        if local_config is not None:
            # Overrides, if present.
            self.config.from_object(local_config)

        self.static = {}
        self.collect_static()

        self.collect_filters()

    def __collect_bootstrap(self):
        ''' Collect the bits Bootstrap needs. '''
        if self.config['BOOTSTRAP_CDN'] is False:
            # Use local Bootstrap files.
            self.logger.info('Using local Bootstrap files.')
            local_bs = self.config['BOOTSTRAP_LOCAL']
            self.static['bootstrap'] = {x: flask.url_for('static', filename=local_bs[x]) for x in local_bs}
        else:
            self.logger.info('Using CDN Bootstrap files.')
            self.static['bootstrap'] = self.config['BOOTSTRAP_REMOTE']

        self.logger.debug('Bootstrap files: {0}'.format(self.static['bootstrap']))

    def __collect_html5_fixes(self):
        ''' HTML5 fixes for browsers who can't render good and want to learn to do other things good too. '''
        if self.config['HTML5_CDN'] is False:
            # Use local HTML5 fixes.
            self.logger.info('Using local HTML5 fixes.')
            self.static['html5shiv'] = flask.url_for('static', filename=self.config['HTML5_LOCAL']['html5shiv'])
            self.static['respond'] = flask.url_for('static', filename=self.config['HTML5_LOCAL']['respond'])
        else:
            self.logger.info('Using CDN HTML 5 fixes.')
            self.static['html5shiv'] = self.config['HTML5_REMOTE']['html5shiv']
            self.static['respond'] = self.config['HTML5_REMOTE']['respond']

        self.logger.debug('html5shiv: {0}'.format(self.static['html5shiv']))
        self.logger.debug('respond: {0}'.format(self.static['respond']))

    def __collect_jquery(self):
        ''' Collect the bits jQuery needs. '''
        if self.config['JQUERY_CDN'] is False:
            # Use local.
            self.logger.info('Using local jQuery files.')
            self.static['jquery'] = flask.url_for('static', filename=self.config['JQUERY_LOCAL'])
        else:
            self.logger.info('Using CDN jQuery files.')
            self.static['jquery'] = self.config['JQUERY_REMOTE']

        self.logger.debug('jQuery: {0}'.format(self.static['jquery']))

    def collect_static(self):
        ''' Collect all of our static resources. '''
        with self.test_request_context():
            # favicon.ico
            self.static['favicon.ico'] = flask.url_for('static', filename='icons/pug.ico')
            self.static['favicon.png'] = flask.url_for('static', filename='icons/pug.png')

            self.__collect_bootstrap()
            self.__collect_html5_fixes()
            self.__collect_jquery()

    def collect_filters(self):
        ''' Load our custom filters into Jinja's filter cache. '''
        self.jinja_env.filters['emoji'] = filters.emojize
        self.jinja_env.filters['markdown'] = filters.markdown

    #########################################################################
    # Endpoint methods.

    def handle_root(self):
        ''' Respond to requests for /. '''
        return render_template('index.html', static=self.static, title=None)

    def handle_favicon(self, obsolete=False):
        ''' Provide the favicon.

        :param obsolete: Provide the obsolete favicon.ico.
        '''
        if obsolete:
            return flask.send_file(self.static['favicon.ico'], 'image/x-icon')

        return flask.send_file(self.static['favicon.png'], 'image/png')

    def handle_api(self, version, method):
        ''' Handle API requests on /api/{version}/{method}.

        The version param lets us safely make new APIs that are incompatible
        with the older ones, and deprecate them sensibly.

        :param version: API version number.
        :param method: API method name.
        '''
        if version == 1:  # Current API version.
            print('/api/{0}/{1}'.format(version, method))

        # Unknown or unsupported version.
        flask.abort(400)  # Bad Request


# The only global you'll find in Pug.
app = PugServer()  # pylint: disable=C0103


@app.route('/')
def request_root():
    ''' Requests for /. '''
    return app.handle_root()


@app.route('/favicon.ico')
def request_favicon_obsolete():
    ''' Requests for favicon.ico. '''
    return app.handle_favicon(True)


@app.route('/favicon.png')
def request_favicon():
    ''' Requests for favicon.png. '''
    return app.handle_favicon()


@app.route('/api/<int:version>/<method>', methods=['GET', 'POST'])
def request_api(version, method):
    ''' API requests. '''
    return app.handle_api(version, method)
