#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    sym_wrappers.py - Useful wrapper for the Windows Symbol API
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
from sym_constants import *

# XXX: ctypes.wintypes doesn't exist in python 2.6
# BOOL WINAPI SymInitialize(
#   _In_      HANDLE hProcess,
#   _In_opt_  PCTSTR UserSearchPath,
#   _In_      BOOL fInvadeProcess
# );

# In [13]: wintypes.BOOL
# Out[13]: ctypes.c_long
# In [14]: wintypes.HANDLE
# Out[14]: ctypes.c_void_p
# In [15]: wintypes.LPCSTR
# Out[15]: ctypes.c_char_p
Syminitialize_TYPE = WINFUNCTYPE(c_long, c_void_p, c_char_p, c_long)
Syminitialize = Syminitialize_TYPE(resolve_api('SymInitialize', 'dbghelp.dll'))

# BOOL WINAPI SymFromAddr(
#   _In_       HANDLE hProcess,
#   _In_       DWORD64 Address,
#   _Out_opt_  PDWORD64 Displacement,
#   _Inout_    PSYMBOL_INFO Symbol
# );
Symfromaddr_TYPE = WINFUNCTYPE(c_long, c_void_p, c_longlong, c_longlong_p, symbol_info_p)
Symfromaddr = Symfromaddr_TYPE(resolve_api('SymFromAddr', 'dbghelp.dll'))

# BOOL WINAPI SymGetModuleInfo64(
#   _In_   HANDLE hProcess,
#   _In_   DWORD64 dwAddr,
#   _Out_  PIMAGEHLP_MODULE64 ModuleInfo
# );
Symgetmoduleinfo64_TYPE = WINFUNCTYPE(c_long, c_void_p, c_longlong, imagehlp_module64_p)
Symgetmoduleinfo64 = Symgetmoduleinfo64_TYPE(resolve_api('SymGetModuleInfo64', 'dbghelp.dll'))

def SymInitialize(hProcess, UserSearchPath = None, fInvadeProcess = True):
    """
    Initializes the symbol handler for a process.

    Note: OllyDBG seems to call this function, thus you shouldn't call it.
    """
    return Syminitialize(
        c_void_p(hProcess),
        c_char_p(UserSearchPath),
        c_long(fInvadeProcess)
    )

def SymFromAddr(hProcess, address):
    """
    Retrieves symbol information for the specified address.
    """
    displacement = c_longlong(0)

    # A pointer to a SYMBOL_INFO structure that provides information about the symbol.
    # The symbol name is variable in length; therefore this buffer must be large enough to hold the name stored at the end of the SYMBOL_INFO structure.
    # Be sure to set the MaxNameLen member to the number of bytes reserved for the name.
    buf = create_string_buffer(sizeof(symbol_info_t) + (MAX_SYM_NAME * sizeof(c_char)))
    p_symbol = cast(buf, symbol_info_p)
    p_symbol.contents.SizeOfStruct = c_ulong(sizeof(symbol_info_t))
    p_symbol.contents.MaxNameLen = MAX_SYM_NAME

    r = Symfromaddr(
        c_void_p(hProcess),
        c_longlong(address),
        c_longlong_p(displacement),
        p_symbol
    )

    if r == 0:
        return None

    # -4 because of the pad appended after our structure
    addr_s = addressof(buf) + sizeof(symbol_info_t) - 4
    s = (c_char * p_symbol.contents.NameLen).from_address(addr_s).value

    return {
        'struct' : p_symbol.contents,
        's' : s,
        'displacement' : displacement
    }

def SymGetModuleInfo64(hProcess, address):
    """
    Retrieves the module information of the specified module.
    """
    
    img = imagehlp_module64_t()
    img.SizeOfStruct = c_ulong(sizeof(imagehlp_module64_t))

    r = Symgetmoduleinfo64(
        c_void_p(hProcess),
        c_longlong(address),
        imagehlp_module64_p(img)
    )

    if r == 0:
        return None
    
    return img
