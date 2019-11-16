# -*- coding: utf-8 -*-
'''
Padding oracle network interface.
'''

from __future__ import absolute_import, division, print_function, unicode_literals

from oracle import Oracle  # @UnresolvedImport pylint: disable=F0401
import sys


def main():
    if len(sys.argv) < 2:
        data = bytearray('I, the server, hereby agree that I will pay $100 to this student.'.encode('ascii'))
        data = data[:32]
    else:
        data_file = open(sys.argv[1])
        data = data_file.read()
        data_file.close()

    try:
        oracle = Oracle()
        oracle.connect()

        tag = oracle.mac(data, len(data))

        ret = oracle.vrfy(data, len(data), tag)
        print(ret)
        if ret == 1:
            print("Message verified successfully!")
        else:
            print("Message verification failed.")

    finally:
        oracle.disconnect()


if __name__ == '__main__':
    main()
