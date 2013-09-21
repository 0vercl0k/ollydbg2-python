#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    hackyou_re300.py - A little script to show how you could pwn the reverse300 
#    challenge from http://hackyou.ctf.su 2012.
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
password, password_len = '', 0

class HitBreakpointManager():
    """Trigger callback when hitting a breakpoint"""
    def __init__(self):
        self.breakpoints = [
        ]

    def add(self, bp, callback):
        """Add a breakpoint/callback in the hit list"""
        # bp must be an instance of Breakpoint
        assert(isinstance(bp, Breakpoint) == True)

        self.breakpoints.append({
            'instance' : bp,
            'address' : bp.get_address(),
            'callback' : callback
        }) 

    def clean(self):
        """Remove properly the breakpoints"""
        for entry in self.breakpoints:
            entry['instance'].remove()

    def go(self):
        """Launch the process until the process is dead"""
        while IsDebuggeeFinished() != True:
            Run__()
            for entry in self.breakpoints:
                if entry['address'] == GetEip():
                    # We can launch the callback associated with this breakpoint
                    entry['callback']()

        self.clean()

# thx awe o\ -- http://blog.w3challs.com/index.php?post/2012/10/13/HackYou-CTF-Reverse100%2C-Reverse200%2C-Reverse300-Writeups
 
def callback_compare_password():
    global password, password_len
 
    SetEdx(GetEax())
 
    if password_len in (4, 9):
        password += '-'
        password_len += 1
 
    password += chr(GetEax())
    password_len += 1
 
    print '[+] %s' % password

def main():
    # Setting a fake serial in argument
    SetArguments('hackyou 0123-4567-8910')

    # Now lets get the password
    manager = HitBreakpointManager()

    # http://blog.w3challs.com/index.php?post/2012/10/13/HackYou-CTF-Reverse100%2C-Reverse200%2C-Reverse300-Writeups
    manager.add(SoftwareBreakpoint(0x401113), callback_compare_password)
    manager.add(SoftwareBreakpoint(0x4011D5), callback_compare_password)
    manager.add(SoftwareBreakpoint(0x401297), callback_compare_password)

    manager.go()

    print 'OK, here is the serial: %s' % password
    return 1

if __name__ == '__main__':
    main()