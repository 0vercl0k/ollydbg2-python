from ctypes import *
from breakpoints_constants import *

kernel32 = windll.kernel32

def resolve_api(n):
    """
    Retrieve dynamically the function address exported
    by OllyDbg
    """
    addr = kernel32.GetProcAddress(
        kernel32.GetModuleHandleA(0),
        n
    )
    assert(addr != 0)
    return addr


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

# stdapi (ulong) Readmemory(void *buf,ulong addr,ulong size,int mode);
Readmemory_TYPE = WINFUNCTYPE(c_ulong, c_void_p, c_ulong, c_ulong, c_int)
Readmemory = Readmemory_TYPE(resolve_api('Readmemory'))

# stdapi (ulong) Writememory(const void *buf,ulong addr,ulong size,int mode);
Writememory_TYPE = WINFUNCTYPE(c_ulong, c_void_p, c_ulong, c_ulong, c_int)
Writememory = Writememory_TYPE(resolve_api('Writememory'))

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

def WriteMemory(addr, buff, size, mode = 0):
    """
    Write directly in the memory of the process
    """
    b = create_string_buffer(buff)
    return Writememory(
        addressof(b),
        c_ulong(addr),
        c_ulong(size),
        c_int(mode)
    )

def ReadMemory(addr, size, mode = 0):
    """
    Read the memory of the process at a specific address
    """
    buff = create_string_buffer(size)
    Readmemory(
        addressof(buff),
        c_ulong(addr),
        c_ulong(size),
        c_int(mode)
    )
    return buff.raw

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
