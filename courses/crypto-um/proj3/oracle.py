# -*- coding: utf-8 -*-
'''
Padding oracle network interface.
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import socket


class Oracle(object):
    ''' Not the bad kind of Oracle. '''

    def __init__(self):
        self.socket = None

    def connect(self, server=('52.7.91.172', 80)):
        ''' Connect to the Oracle. '''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(server)
        except socket.error as exc:
            print('Unable to connect: {0}'.format(exc))
            return -1

        print("Connected to server successfully.")

        return 0

    def disconnect(self):
        ''' Disconnect from the Oracle. '''
        if self.socket is None:
            print("[WARNING]: You haven't connected to the server yet.")
            return -1

        self.socket.close()
        print("Connection closed successfully.")

        return 0

    # Packet Structure: < num_blocks(1) || ciphertext(16*num_blocks) || null-terminator(1) >
    def send(self, ctext, num_blocks):
        ''' Send to the Oracle. '''
        if self.socket is None:
            print("[WARNING]: You haven't connected to the server yet.")
            return -1

        msg = ctext[:]
        msg.insert(0, num_blocks)
        msg.append(0)

        self.socket.send(bytearray(msg))
        recvbit = self.socket.recv(2)

        try:
            return int(recvbit)
        except ValueError:
            return int(recvbit[0])
