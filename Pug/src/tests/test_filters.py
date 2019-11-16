# -*- coding: utf-8 -*-
'''
Created on Oct 19, 2014

@author: Chris
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import filters
import unittest


class TestFilters(unittest.TestCase):
    ''' Test the custom filters. '''

    def test_unknown_emoji(self):
        ''' Test the Emoji filter with an unknown shortcut. '''
        unknown_emoji = filters.emojize(':bella_is_my_pug:')
        self.assertEqual(unknown_emoji, ':bella_is_my_pug:', 'Unknown emoji mutated')

    def test_no_emoji(self):
        ''' Test the Emoji filter plain text. '''
        not_emoji = filters.emojize('Some text with no ghost in it.')
        self.assertEqual(not_emoji, 'Some text with no ghost in it.', 'Non-emoji text mutated')

    def test_valid_emoji(self):
        ''' Test the Emoji filter with a valid shortcut. '''
        valid_emoji = filters.emojize(':ghost:')
        self.assertEqual(valid_emoji, u'\U0001f47b', ':ghost: turned into something weird')

    def test_no_markdown(self):
        ''' Test the markdown filter with plain text. '''
        no_markdown = filters.markdown('Hi')
        self.assertEqual(no_markdown, '<p>Hi</p>\n', 'Plain text mutated')

    def test_valid_markdown(self):
        ''' Test the markdown filter with valid CommonMark text. '''
        valid_markdown = filters.markdown('*Hi*')
        self.assertEqual(valid_markdown, '<p><em>Hi</em></p>\n', '*Hi* turned into something weird')

    def test_markdown_emoji(self):
        ''' Test the markdown filter with Emoji in it. '''
        emoji_markdown = filters.markdown('Hi :ghost:')
        self.assertEqual(emoji_markdown, u'<p>Hi \U0001f47b</p>\n', 'Hi :ghost: mutated')
