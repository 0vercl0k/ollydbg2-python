#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    layers.py - A script to bypass the layers in layers.exe
#    Copyright (C) 2012 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from ollyapi import *
from binascii import unhexlify
from time import time

def main():
    t1 = time()
    n_layers = 0
    pattern_layer = 'E800000000' # call $+1
    are_we_done = False

    while are_we_done == False:
        pattern = ReadMemory(5)
        if pattern != unhexlify(pattern_layer):
            are_we_done = True
        else:
            end_current_layer = FindHex('E2FA') # LOOP
            assert(end_current_layer != 0)

            b = HardwareBreakpoint(end_current_layer + 2)
            b.goto()
            b.remove()
            n_layers += 1

    print "OK, I think I've passed all the %d layers (in %f s), HF!" % (n_layers, time() - t1)
    return 1

if __name__ == '__main__':
    main()
