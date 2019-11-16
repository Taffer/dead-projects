# -*- coding: utf-8 -*-
'''
Padding oracle network interface.
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import proj3.oracle
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python sample.py <filename>")
        sys.exit(-1)

    data = open(sys.argv[1]).read()

    ctext = bytearray.fromhex(data.strip())  # [(int(data[i:i + 2], 16)) for i in range(0, len(data), 2)]

    the_oracle = proj3.oracle.Oracle()
    the_oracle.connect()

    retval = the_oracle.send(ctext, 3)
    if retval == 1:
        print('Oracle returned: Success (1)')
    else:
        print("Oracle returned: Failure ({0})".format(retval))

    the_oracle.disconnect()


if __name__ == '__main__':
    main()
