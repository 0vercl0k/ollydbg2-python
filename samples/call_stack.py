#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    call_stack.py - A simple script to display the call stack
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

def walk_stack(nb_max_frame = 100, nb_args = 4):
    """
    Walk on the stack & generate a call stack
    """
    frames_info = []
    args = []
    ebp = GetEbp()

    for i in range(nb_max_frame):
        # at EBP we have the SEBP
        sebp = ReadDwordMemory(ebp)
        # and right after the SEIP
        seip = ReadDwordMemory(ebp + 4)

        if sebp == 0 or seip == 0:
            break

        # if we have a stack-frame big enough to dump nb_arg
        if (sebp - (ebp + 8)) >= nb_args*4:
            args = [ReadDwordMemory(i) for i in range(ebp + 8, ebp + 8 + 4*nb_args, 4)]

        symbol = GetSymbolFromAddress(seip)
        frames_info.append({
            'return-address' : seip,
            'address' : sebp + 4,
            'symbol' : symbol if symbol != None else 'no symbol found',
            'args' : args
        })

        ebp = sebp

    return frames_info

def main():
    # We need to add some symbol to our sample:
    AddUserLabel(0x00401090, 'main')
    AddUserLabel(0x00401070, 'f')
    AddUserLabel(0x00401050, 'zerg')
    AddUserLabel(0x00401020, 'bla')
    AddUserLabel(0x00401000, 'r')

    # Goto in the deepest routine
    b = SoftwareBreakpoint(ResolveApiAddress('call_stack', 'r'))
    Run()
    b.remove()

    # now goto deep in printf
    b = SoftwareBreakpoint(ResolveApiAddress('ntdll', 'RtlEnterCriticalSection'))
    Run()
    b.remove()

    # OK now the call stack should be interesting!1!&
    call_stack = walk_stack()
    print "#%.2d %#.8x : %s" % (len(call_stack), GetEip(), GetSymbolFromAddress(GetEip()))
    for i in range(len(call_stack)):
        c = call_stack[i]
        ri = len(call_stack) - i - 1
        print '#%.2d %#.8x : %s (found @%#.8x)' % (ri, c['return-address'], c['symbol'], c['address'])

    return 1

if __name__ == '__main__':
    main()