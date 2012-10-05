#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    breakpoints_wrapper.py - You will find there all the wrapper of the OllyDBG2 API to play with breakpoints.
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
from ctypes import *
from common import *

# stdapi (int) Setint3breakpoint(ulong addr, ulong type, int fnindex, int limit, int count, ulong actions, wchar_t *condition, wchar_t *expression, wchar_t *exprtype);
Setint3breakpoint_TYPE = CFUNCTYPE(c_int, c_ulong, c_ulong, c_int, c_int, c_int, c_ulong, c_wchar_p, c_wchar_p, c_wchar_p)
Setint3breakpoint = Setint3breakpoint_TYPE(resolve_api('Setint3breakpoint'))

# stdapi (int) Sethardbreakpoint(int index,ulong size,ulong type,int fnindex,ulong addr,int limit,int count,ulong actions,wchar_t *condition,wchar_t *expression,wchar_t *exprtype);
Sethardbreakpoint_TYPE = CFUNCTYPE(c_int, c_int, c_ulong, c_ulong, c_int, c_ulong, c_int, c_int, c_ulong, c_wchar_p, c_wchar_p, c_wchar_p)
Sethardbreakpoint = Sethardbreakpoint_TYPE(resolve_api('Sethardbreakpoint'))

# stdapi (int) Removeint3breakpoint(ulong addr,ulong type);
Removeint3breakpoint_TYPE = CFUNCTYPE(c_int, c_ulong, c_ulong)
Removeint3breakpoint = Removeint3breakpoint_TYPE(resolve_api('Removeint3breakpoint'))

# stdapi (int) Removehardbreakpoint(int index);
Removehardbreakpoint_TYPE = CFUNCTYPE(c_int, c_int)
Removehardbreakpoint = Removehardbreakpoint_TYPE(resolve_api('Removehardbreakpoint'))

# stdapi (int) Findfreehardbreakslot(ulong type);
Findfreehardbreakslot_TYPE = CFUNCTYPE(c_int, c_ulong)
Findfreehardbreakslot = Findfreehardbreakslot_TYPE(resolve_api('Findfreehardbreakslot'))

# stdapi (int) Removemembreakpoint(ulong addr);
Removemembreakpoint_TYPE = CFUNCTYPE(c_ulong)
Removemembreakpoint = Removemembreakpoint_TYPE(resolve_api('Removemembreakpoint'))

# stdapi (int) Setmembreakpoint(ulong addr,ulong size,ulong type, int limit,int count,wchar_t *condition, wchar_t *expression,wchar_t *exprtype);
Setmembreakpoint_TYPE = CFUNCTYPE(c_int, c_ulong, c_ulong, c_ulong, c_int, c_int, c_wchar_p, c_wchar_p, c_wchar_p)
Setmembreakpoint = Setmembreakpoint_TYPE(resolve_api('Setmembreakpoint'))

def SetInt3Breakpoint(address, type_bp = 0, fnindex = 0, limit = 0, count = 0, actions = 0, condition = '', expression = '', exprtype = ''):
    """
    Python wrapper for the Setint3breakpoint function
    """
    return Setint3breakpoint(
        c_ulong(address),
        c_ulong(type_bp),
        c_int(fnindex),
        c_int(limit),
        c_int(count),
        c_ulong(actions),
        c_wchar_p(condition),
        c_wchar_p(expression),
        c_wchar_p(exprtype)
    )

def SetHardBreakpoint(address, index = 0, size = 0, type_ = 0, fnindex = 0, limit = 0, count = 0, actions = 0, condition = '', expression = '', exprtype = ''):
    """
    Set a hardware breakpoint
    """
    return Sethardbreakpoint(
        c_int(index),
        c_ulong(size),
        c_ulong(type_),
        c_int(fnindex),
        c_ulong(address),
        c_int(limit),
        c_int(count),
        c_ulong(actions),
        c_wchar_p(condition),
        c_wchar_p(expression),
        c_wchar_p(exprtype)
    )

def RemoveInt3Breakpoint(address, type_bp):
    """
    Remove software breakpoint
    """
    return Removeint3breakpoint(
        c_ulong(address),
        c_ulong(type_bp)
    )

def RemoveHardbreapoint(slot):
    """
    Remove hardware breakpoint
    """
    return Removehardbreakpoint(c_int(slot))

def FindFreeHardbreakSlot(type_):
    """
    Find a free slot to put your hardware breakpoint
    """
    return Findfreehardbreakslot(c_ulong(type_))

def SetMemoryBreakpoint(address, size = 1, type_ = 0, limit = 0, count = 0, condition = '', expression = '', exprtype = ''):
    """
    Set a memory breakpoint
    """
    return Setmembreakpoint(
        c_ulong(address),
        c_ulong(size),
        c_ulong(type_),
        c_int(limit),
        c_int(count),
        c_wchar_p(condition),
        c_wchar_p(expression),
        c_wchar_p(exprtype)
    )

def RemoveMemoryBreakpoint(addr):
    """
    Remove a memory breakpoint
    """
    return Removemembreakpoint(c_ulong(addr))
