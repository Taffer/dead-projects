#!/bin/sh
#
# Run pylint with Pug's .pylintrc.
#
# Quotes around path names in here because Cygwin.

pylint "--rcfile=$(dirname $0)/.pylintrc" --output-format=colorized $@;
