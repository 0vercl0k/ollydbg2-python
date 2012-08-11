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
Threadregisters_TYPE = WINFUNCTYPE(t_reg_p, c_ulong)
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

def SetEax(eax = 0):
    """
    Modify the EAX register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    p_reg[0].r[REG_EAX] = eax

def SetEbx(ebx = 0):
    """
    Modify the EBX register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    p_reg[0].r[REG_EBX] = ebx

def SetEcx(ecx = 0):
    """
    Modify the ECX register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    p_reg[0].r[REG_ECX] = ecx

def SetEdx(edx = 0):
    """
    Modify the EDX register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    p_reg[0].r[REG_EDX] = edx

def SetEsi(esi = 0):
    """
    Modify the ESI register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    p_reg[0].r[REG_ESI] = esi

def SetEdi(edi = 0):
    """
    Modify the EDI register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    p_reg[0].r[REG_EDI] = edi

def SetEsp(esp = 0):
    """
    Modify the ESP register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    p_reg[0].r[REG_ESP] = esp

def SetEbp(ebp = 0):
    """
    Modify the EBP register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    p_reg[0].r[REG_EBP] = ebp

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

def GetEsp():
    """
    Get the ESP register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    return p_reg[0].r[REG_ESP]

def GetEdi():
    """
    Get the EDI register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    return p_reg[0].r[REG_EDI]

def GetEax():
    """
    Get the EAX register
    """
    p_reg = Threadregisters(c_ulong(GetCpuThreadId()))
    return p_reg[0].r[REG_EAX]
