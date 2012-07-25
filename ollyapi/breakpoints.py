from ctypes import *
from breakpoints_constants import *
from breakpoints_resolve import *

def bp_set(address, bp_type = BP_BREAK | BP_MANUAL):
    """
    Set a classical software breakpoint:
    Pause each time the breakpoint is reached.
    """
    return SetInt3Breakpoint(address, bp_type)

def bp_goto(address):
    """
    Set a software one-shot breakpoint at address, and
    run the process.
    """
    bp_set(address, OneShotBreakpoint)
    Run()


def AddUserComment(address, s):
    """
    Add a user comment at a specific address ; it's like using the shortcut ';'
    """
    return InsertNameW(
        address,
        NM_COMMENT,
        s
    )

def AddUserLabel(address, s):
    """
    Add a user label at a specific address ; it's like using the shortcut ':'
    """
    return InsertNameW(
        address,
        NM_LABEL,
        s
    )

def GetPESections():
    mod = FindMainModule()
    n = mod.nsect
    sections = []
    for i in range(n):
        section = mod.sect[i]
        sections.append(section)
    return sections
