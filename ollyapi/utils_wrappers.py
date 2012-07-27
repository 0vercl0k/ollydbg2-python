#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    utils_wrappers.py - All the functions that don't belong to other modules.
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
from utils_constants import *

# stdapi (int) InsertnameW(ulong addr,int type,wchar_t *s);
InsertnameW_TYPE = WINFUNCTYPE(c_int, c_ulong, c_int, c_wchar_p)
InsertnameW = InsertnameW_TYPE(resolve_api('InsertnameW'))

# stdapi (int) Run(t_status status,int pass);
Run_TYPE = WINFUNCTYPE(c_int, c_int, c_int)
Run_ = Run_TYPE(resolve_api('Run'))

# stdapi (t_module *) Findmainmodule(void);
Findmainmodule_TYPE = WINFUNCTYPE(POINTER(t_module))
Findmainmodule = Findmainmodule_TYPE(resolve_api('Findmainmodule'))

# stdapi (int)     Checkfordebugevent(void);
Checkfordebugevent_TYPE = WINFUNCTYPE(c_int)
Checkfordebugevent = Checkfordebugevent_TYPE(resolve_api('Checkfordebugevent'))

def InsertNameW(addr, type_, s):
    """
    That function is used to add label and comment directly on the disassembly
    (like with the shortcut ':' or ';')
    """
    return InsertnameW(
        c_ulong(addr),
        c_int(type_),
        c_wchar_p(s)
    )

def Run(status = STAT_RUNNING, pass_ = 0):
    """
    Run the process, step-in, step-over, whatever
    """
    Run_(c_int(status), c_int(pass_))

    # required in order to update the state of the thread registers (retrieved with Threadregisters for example)
    # BTW, not sure it's supposed to be done this way though, I've found that in an OllyDBG2 reverse-engineering session.
    CheckForDebugEvent()

def FindMainModule():
    """
    Get a cool structure filled with juicy information concerning
    the process being debugged ; you can find its ImageBase, real ImageBase, etc.
    Check t_module structure definition
    """
    r = Findmainmodule()
    #XXX: check NULL return
    return r.contents

def CheckForDebugEvent():
    """
    Hum, this method seems to be very important, one of its purpose
    is to updated the thread registers retrieved thanks to Threadregisters()
    """
    return Checkfordebugevent()