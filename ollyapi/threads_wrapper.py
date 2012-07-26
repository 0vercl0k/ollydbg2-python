#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    threads_wrapper.py - Functions used to manipulate/play with threads.
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
from threads_constants import *

# stdapi (void) Resumeallthreads(void);
Resumeallthreads_TYPE = WINFUNCTYPE(None)
Resumeallthreads  = Resumeallthreads_TYPE(resolve_api('Resumeallthreads'))

# stdapi (t_reg *) Threadregisters(ulong threadid);
Threadregisters_TYPE = WINFUNCTYPE(POINTER(t_reg), c_ulong)
Threadregisters = Threadregisters_TYPE(resolve_api('Threadregisters'))

# stdapi (ulong) Getcputhreadid(void);
Getcputhreadid_TYPE = WINFUNCTYPE(c_ulong)
Getcputhreadid = Getcputhreadid_TYPE(resolve_api('Getcputhreadid'))

def ResumeAllThreads():
    Resumeallthreads()

def ThreadRegisters(threadid):
    """
    Get the registers (SEE/FPU/General registers/etc) for the current thread debugged
    """
    return Threadregisters(c_ulong(threadid)).contents

def GetCpuThreadId():
    """
    Get the TID of the current thread
    """
    return Getcputhreadid()
