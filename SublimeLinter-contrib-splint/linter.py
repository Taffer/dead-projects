# linter.py
#
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by chrish@pobox.com
# Copyright (c) 2015 chrish@pobox.com
#
# License: MIT

"""This module exports the Splint plugin class."""

from SublimeLinter.lint import Linter, util, highlight  # pylint: disable=F0401


class Splint(Linter):  # pylint: disable=W0232,R0903

    """Provides an interface to splint."""

    syntax = 'c'
    cmd = ('splint', '-quiet', '-linelen', '32767')
    executable = None
    defaults = {}

    version_args = 'help version'
    version_re = r'^Splint (?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 3.1.2'

    regex = r'^(?P<file>.+):(?P<line>[0-9]+):(?P<col>[0-9]+):(?P<message>.*)$'
    multiline = False
    default_type = highlight.WARNING

    line_col_base = (1, 1)
    tempfile_suffix = "-"
    error_stream = util.STREAM_STDOUT

    config_file = ('-f', '.splintrc', '~')

    module = 'splint'

    selectors = {}
    word_re = None
    inline_settings = None
    inline_overrides = None
    comment_re = None
    check_version = False
