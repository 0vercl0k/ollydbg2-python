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
from breakpoints_constants import *

# stdapi (int) Setint3breakpoint(ulong addr, ulong type, int fnindex, int limit, int count, wchar_t *condition, wchar_t *expression, wchar_t *exprtype);
Setint3breakpoint_TYPE = WINFUNCTYPE(c_int, c_ulong, c_ulong, c_int, c_int, c_int, c_wchar_p, c_wchar_p, c_wchar_p)
Setint3breakpoint = Setint3breakpoint_TYPE(resolve_api('Setint3breakpoint'))

def SetInt3Breakpoint(address, type_bp = 0, fnindex = 0, limit = 0, count = 0, condition = '', expression = '', exprtype = ''):
    """
    Python wrapper for the Setint3breakpoint function
    """
    return Setint3breakpoint(
        c_ulong(address),
        c_ulong(type_bp),
        c_int(fnindex),
        c_int(limit),
        c_int(count),
        c_wchar_p(condition),
        c_wchar_p(expression),
        c_wchar_p(exprtype)
    )
