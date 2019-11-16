# -*- coding: utf-8 -*-
'''
Created on Oct 19, 2014

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import external
import jinja2.filters
import re

__version__ = '0.0.1'


def emojize(text):
    ''' Convert emoji shortcuts into Unicode characters.

    This is a custom version of external.emoji.emojize() that doesn't eat
    unknown shortcuts.

    :param text: The text to convert.
    '''
    pattern = re.compile('(:[a-z0-9\+\-_]+:)')

    def emorepl(match):
        ''' Closure for our substitution. '''
        value = match.group(1)

        if value in external.emoji.code.emojiCodeDict:
            return external.emoji.code.emojiCodeDict[value]
        else:
            # This branch is the change.
            return value

    return pattern.sub(emorepl, text)


def markdown(text):
    ''' Convert CommonMark formatted text into HTML.

    Text is first passed through an HTML escaper, then the CommonMark parser.

    :param text: The text to convert.
    '''
    result = jinja2.filters.do_forceescape(text)  # HTML-safe!
    result = emojize(result)  # Emoji

    marker = external.CommonMark.DocParser()
    tree = marker.parse(result)

    markup = external.CommonMark.HTMLRenderer()
    return markup.render(tree)
