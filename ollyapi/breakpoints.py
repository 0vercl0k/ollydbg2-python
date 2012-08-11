#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    breakpoints.py - A python high level API to play with breakpoints in OllyDBG2
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
from breakpoints_wrappers import *
from utils_wrappers import Run
from threads_wrappers import GetEip

def bps_set(address, bp_type = BP_BREAK | BP_MANUAL):
    """
    Set a classical software breakpoint:
    Pause each time the breakpoint is reached.
    """
    return SetInt3Breakpoint(address, bp_type)

def bps_goto(address):
    """
    Set a software one-shot breakpoint at address, and
    run the process.
    """
    bps_set(address, OneShotBreakpoint)
    Run()

def bpsc_set(address, cond, bp_type = BP_MANUAL):
    """
    Set a software conditional breakpoint

    Note: it doesn't seem possible to have a software conditional OneShotBreakpoint 
    """
    return SetInt3Breakpoint(
        address,
        bp_type | BP_CONDBREAK | BP_COND,
        condition = cond
    )

def flags_to_hardwarebp_type(flags, is_conditional_bp = False):
    """
    Translate the flags 'rwx' in the proper hardware breakpoint types
    used internaly by OllyDbg
    """
    assert(flags in ['rw', 'w', 'wr', 'x'])

    # converting the flags into valid breakpoint type
    type_dword = BP_MANUAL | BP_BREAK
    if 'r' in flags:
        type_dword |= BP_READ

    if 'w' in flags:
        type_dword |= BP_WRITE

    if 'x' in flags:
        type_dword |= BP_EXEC

    if is_conditional_bp != '':
        type_dword |= BP_COND

    # ensure the size is 1byte if this is an execution breakpoint
    if type_dword == ExecutionBreakpoint or type_dword == ExecutionBreakpoint | BP_COND:
        size = 1

    return type_dword

def bph_set(address, flags, size = 1, slot = 0, condi = ''):
    """
    Set a hardware breakpoint
    """

    assert(size in [1, 2, 4])
    assert(slot in [0, 1, 2, 3])

    r = SetHardBreakpoint(
        address,
        slot,
        size,
        flags_to_hardwarebp_type(flags, condi != ''),
        0,
        0,
        0,
        condi,
        '',
        ''
    )

    return r

def bphc_set(address, flags, condi, size = 1, slot = 0):
    """
    Set a conditional hardware breakpoint
    """
    return bph_set(
        address,
        flags,
        size,
        slot,
        condi
    )

# WE NEED ABSTRACTION MAN

class Breakpoint(object):
    """
    """
    def __init__(self, address, type_bp, condition = None):
        self.address = address
        self.state = 'Disabled'
        self.type = type_bp
        self.is_conditional_bp = condition != None
        self.condition = '' if condition == None else condition

    def get_state(self):
        """
        Get the state of your breakpoint
        """
        return self.state

    def is_enabled(self):
        """
        Is the breakpoint enabled ?
        """
        return self.state == 'Enabled'

    def is_disabled(self):
        """
        Is the breakpoint disabled ?
        """
        return self.state == 'Disabled'

    def disable(self):
        """
        Disable the breakpoint
        """
        pass

    def remove(self):
        """
        Remove the breakpoint
        """
        pass

    def enable(self):
        """
        Enable the breakpoint
        """
        pass

    def goto(self):
        """
        Run the executable until we reach our breakpoint
        """
        while GetEip() != self.address:
            Run()

class SoftwareBreakpoint(Breakpoint):
    """
    A class to manipulate, play with software breakpoint

    TODO:
        - disable
        - .continue(x) -> let the breakpoint be hit x times
    """
    def __init__(self, address, condition = None):
        # if this is a classic breakpoint we need to set different flag
        t = BP_MANUAL | ((BP_COND | BP_CONDBREAK) if condition != None else BP_BREAK)

        # init internal state of the breakpoint
        super(SoftwareBreakpoint, self).__init__(address, t, condition)

        # enable directly the software breakpoint
        self.enable()

    def enable(self):
        if self.is_conditional_bp:
            bpsc_set(self.address, self.condition, self.type)
        else:
            bps_set(self.address, self.type)

        self.state = 'Enabled'

    def remove(self):
        # we remove the breakpoint only if it is enabled
        if self.state == 'Enabled':
            RemoveInt3Breakpoint(self.address, self.type)
            self.state = 'Disabled'

class HardwareBreakpoint(Breakpoint):
    """
    A class to manipulate, play with hardware breakpoint

    Note:
        - do not use .goto() if you have a read/write bp, because you don't know where
        the breakpoint is going to be hit
    """
    def __init__(self, address, flags = 'x', size = 1, slot = None, condition = None):
        # init internal state of the breakpoint
        super(HardwareBreakpoint, self).__init__(address, flags, condition)

        # keep in memory the flags view like 'rw' breakpoint, but translate it into something
        # ollydbg understands
        self.internal_type = flags_to_hardwarebp_type(self.type, self.is_conditional_bp)

        self.size = size
        self.slot = slot if slot != None else FindFreeHardbreakSlot(self.internal_type)
        if self.slot == -1:
            raise Exception('You have used all the available slot')
        
        self.enable()

    def enable(self):
        if self.is_conditional_bp:
            bphc_set(self.address, self.type, self.condition, self.size, self.slot)
        else:
            bph_set(self.address, self.type, self.size, self.slot)

        self.state = 'Enabled'

    def remove(self):
        if self.state == 'Enabled':
            RemoveHardbreapoint(self.slot)
            self.state = 'Disabled'
