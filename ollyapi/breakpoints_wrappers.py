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

# stdapi (void) Resumeallthreads(void);
Resumeallthreads_TYPE = WINFUNCTYPE(None)
Resumeallthreads  = Resumeallthreads_TYPE(resolve_api('Resumeallthreads'))

# stdapi (int) Run(t_status status,int pass);
Run_TYPE = WINFUNCTYPE(c_int, c_int, c_int)
Run_ = Run_TYPE(resolve_api('Run'))

# stdapi (t_reg *) Threadregisters(ulong threadid);
Threadregisters_TYPE = WINFUNCTYPE(POINTER(t_reg), c_ulong)
Threadregisters = Threadregisters_TYPE(resolve_api('Threadregisters'))

# stdapi (ulong) Getcputhreadid(void);
Getcputhreadid_TYPE = WINFUNCTYPE(c_ulong)
Getcputhreadid = Getcputhreadid_TYPE(resolve_api('Getcputhreadid'))

# stdapi (int) Expression(t_result *result, wchar_t *expression, uchar *data, ulong base, ulong size, ulong threadid, ulong a, ulong b, ulong mode);
Expression_TYPE = WINFUNCTYPE(c_int, POINTER(t_result), c_wchar_p, c_void_p, c_ulong, c_ulong, c_ulong, c_ulong, c_ulong, c_ulong)
Expression_ = Expression_TYPE(resolve_api('Expression'))

# stdapi (int) InsertnameW(ulong addr,int type,wchar_t *s);
InsertnameW_TYPE = WINFUNCTYPE(c_int, c_ulong, c_int, c_wchar_p)
InsertnameW = InsertnameW_TYPE(resolve_api('InsertnameW'))

# stdapi (t_module *) Findmainmodule(void);
Findmainmodule_TYPE = WINFUNCTYPE(POINTER(t_module))
Findmainmodule = Findmainmodule_TYPE(resolve_api('Findmainmodule'))


# stdapi (ulong)   Assemble(wchar_t *src,ulong ip,uchar *buf,ulong nbuf,int mode,
#                    wchar_t *errtxt);
# stdapi (ulong)   Disasm(uchar *cmd,ulong cmdsize,ulong cmdip,uchar *cmddec,
#                    t_disasm *cmdda,int cmdmode,t_reg *cmdreg,
#                    t_predict *cmdpredict);

def FindMainModule():
    r = Findmainmodule()
    #XXX: check NULL return
    return r.contents

def InsertNameW(addr, type_, s):
    return InsertnameW(
        c_ulong(addr),
        c_int(type_),
        c_wchar_p(s)
    )

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

def Expression(result, expression, data, base, size, threadid, a, b, mode):
    """
    Let OllyDbg evaluate an expression for you:
        * get an exported function address easily thanks to the notation module.function_name
    """
    r = Expression_(
        byref(result),
        c_wchar_p(expression),
        c_void_p(data),
        c_ulong(base),
        c_ulong(size),
        c_ulong(threadid),
        c_ulong(a),
        c_ulong(b),
        c_ulong(mode)
    )

    if result.value == 'Unrecognized identifier':
        return None

    return r

def ResolveApiAddress(module, function):
    """
    Get the address of a specific API exported by a specific module thanks to their names
    """
    r = t_result()
    ret = Expression(
        r,
        '%s.%s' % (module, function),
        0,
        0,
        0,
        GetCpuThreadId(),
        0,
        0,
        0
    )

    if r.datatype == EXPR_DWORD:
        return r.u.u

    return None

def GetCurrentThreadRegisters():
    """
    Retrieve the register for the current thread debugged
    """
    current_tid = GetCpuThreadId()
    if current_tid == 0:
        return None
    return ThreadRegisters(current_tid)

def Run(status = STAT_RUNNING, pass_ = 0):
    """
    Run the process, step-in, step-over, whatever
    """
    Run_(c_int(status), c_int(pass_))

def ResumeAllThreads():
    Resumeallthreads()

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
