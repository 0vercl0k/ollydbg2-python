#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    sym.py - High level API to play with the Windows Symbol API
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

import sys
from sym_wrappers import *
import threads

def GetSymbolFromAddress(address):
    """
    Retrieve symbol information from an address
    Example:
    GetSymbolFromAddress(0x) = ntdll!Kibla+0xdd
    """
    handle_process = threads.GetProcessHandle()
    address_info = SymFromAddr(handle_process, address)
    s = None
    
    if address_info != None:
        symbol_name, offset = address_info['s'], address_info['displacement'].value
        print address_info['struct'].ModBase
        module_info = SymGetModuleInfo64(handle_process, address_info['struct'].ModBase)

        if module_info != None:
            s = '%s!%s+%#.8x' % (module_info.ModuleName, symbol_name, offset)
        else:
            s = '%s+%#.8x' % (symbol_name, offset)

    return s
