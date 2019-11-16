# -*- coding: utf-8 -*-
'''
Padding oracle network interface.
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import socket


class Oracle(object):
    def __init__(self):
        self.mac_sock = None
        self.vrfy_sock = None

    def connect(self, host_ip='52.7.91.172'):
        self.mac_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.vrfy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.mac_sock.connect((host_ip, 81))
            self.vrfy_sock.connect((host_ip, 82))
        except socket.error as exc:
            print('Unable to connect to {0}: {1}'.format(host_ip, exc))
            return -1

        print("Connected to server successfully.")

        return 0

    def disconnect(self):
        if not self.mac_sock or not self.vrfy_sock:
            print("[WARNING]: You haven't connected to the server yet.")
            return -1

        self.mac_sock.close()
        self.vrfy_sock.close()

        print("Connection closed successfully.")

        return 0

    # Packet Structure: < mlength(1) || message(mlength) || null-terminator(1) >
    def mac(self, message, mlength):
        if not self.mac_sock or not self.vrfy_sock:
            print("[WARNING]: You haven't connected to the server yet.")
            return -1

        out = bytearray(message)
        out.insert(0, mlength)
        out.append(0)

        self.mac_sock.send(bytearray(out))
        tag = self.mac_sock.recv(16)

        return bytearray(tag)

    # Packet Structure: < mlength(1) || message(mlength) || tag(16) || null-terminator(1) >
    def vrfy(self, message, mlength, tag):
        if not self.mac_sock or not self.vrfy_sock:
            print("[WARNING]: You haven't conected to the server yet.")
            return -1

        out = bytearray(message)
        out.insert(0, mlength)
        out += tag
        out.append(0)

        self.vrfy_sock.send(bytearray(out))
        match = self.vrfy_sock.recv(2)

        return int(match.strip('\0'))
