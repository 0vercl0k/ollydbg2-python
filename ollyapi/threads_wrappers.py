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
Resumeallthreads_TYPE = CFUNCTYPE(None)
Resumeallthreads  = Resumeallthreads_TYPE(resolve_api('Resumeallthreads'))

# stdapi (t_reg *) Threadregisters(ulong threadid);
Threadregisters_TYPE = CFUNCTYPE(t_reg_p, c_ulong)
Threadregisters = Threadregisters_TYPE(resolve_api('Threadregisters'))

# stdapi (ulong) Getcputhreadid(void);
Getcputhreadid_TYPE = CFUNCTYPE(c_ulong)
Getcputhreadid = Getcputhreadid_TYPE(resolve_api('Getcputhreadid'))

# oddata (ulong)   processid;            // Process ID of Debuggee or 0
processid = c_ulong.from_address(resolve_api('processid')).value

# oddata (HANDLE)  process;              // Handle of Debuggee or NULL
# XXX: ctypes.wintypes doesn't exist in python 2.6
# In [12]: wintypes.HANDLE
# Out[12]: ctypes.c_void_p
processhandle = c_void_p.from_address(resolve_api('process')).value

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

# The metaprogramming trick doesn't work because the ip field isn't in the t_reg.r array :(
def SetEip(eip = 0):
    """
    Modify the EIP register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    p_reg[0].ip = eip


def GetEip():
    """
    Get the EIP register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    return p_reg[0].ip

def GetProcessId():
    """
    Get the PID of the debuggee
    """
    return processid

def GetProcessHandle():
    """
    Get the handle on the debuggee (obtained via OpenProcess)
    """
    return processhandle

# metaprogramming magixx

def CreateRegisterSetter(reg_id, reg_name):
    """
    Create dynamically a setter function for an x86 register contained in t_reg.r
    """
    def template_func(reg_value):
        p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
        p_reg[0].r[reg_id] = reg_value

    f = template_func
    # adjust correctly the name of the futur function
    f.__name__ = 'Set%s' % reg_name.capitalize()
    f.__doc__  = 'Set the %s register' % reg_name.upper()

    return (f.__name__, f)

def CreateRegisterGetter(reg_id, reg_name):
    """
    Create dynamically a getter function for an x86 register contained in t_reg.r
    """
    def template_func():
        p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
        return p_reg[0].r[reg_id]

    f = template_func
    # adjust correctly the name of the futur function
    f.__name__ = 'Get%s' % reg_name.capitalize()
    f.__doc__  = 'Get the %s register' % reg_name.upper()

    return (f.__name__, f)

def BuildSettersGetters():
    """
    Create dynamically all the getters/setters function used to retrieve/set register value in
    t_reg.r
    """
    list_reg = [
        ('eax', REG_EAX),
        ('ecx', REG_ECX),
        ('edx', REG_EDX),
        ('ebx', REG_EBX),
        ('esp', REG_ESP),
        ('ebp', REG_EBP),
        ('esi', REG_ESI),
        ('edi', REG_EDI)
    ]

    for reg_name, reg_id in list_reg:
        # Build the setter
        n, f = CreateRegisterSetter(reg_id, reg_name)
        globals()[n] = f

        # Build the getter
        n, f = CreateRegisterGetter(reg_id, reg_name)
        globals()[n] = f

# it's a bit magic, instanciation of the functions!
BuildSettersGetters()