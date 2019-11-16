# -*- coding: utf-8 -*-
#
# OpenAchivement configuration.
#
# This file contains the default configuration settings for the
# OpenAchievement server.
#
# To specify your site's host name, administration email, PGP keys,
# SMTP server settings, etc. create a local_config.py in this
# directory containing the appropriate settings.
#
# PROTIP: Don't check your credentials and private keys into GitHub. :-)

'''
Created on Mar 8, 2014

@author: Chris
'''

# Server settings.
DEBUG_PORT = 8000  # Development
SERVER_PORT = 80  # Production

SERVER_HOSTNAME = 'localhost.localdomain'  # Fully-qualified domain name.

# Email settings.
ADMIN_EMAIL = 'root@localhost'  # Email address in the From: field and site mailto: links.

SMTP_HOSTNAME = 'localhost'  # Out-going email server hostname.
SMTP_PORT = 587  # Out-going email server port.
SMTP_USERID = 'mail@localhost'  # User ID for authenticating with SMTP_HOSTNAME.
SMTP_PASSWD = 'mail_password'  # Password for SMTP_USERID
