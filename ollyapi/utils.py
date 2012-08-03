#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    utils.py - High level API for the utils functions.
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
from utils_wrappers import *

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
    """
    Get all the PE sections of your executable
    Each entry is a t_secthdr
    """
    mod = FindMainModule()
    n = mod.nsect
    sections = []
    for i in range(n):
        section = mod.sect[i]
        sections.append(section)
    return sections

def GetEntryPoint():
    """
    Get the address of the entry point of your executable
    """
    mod = FindMainModule()
    return mod.entry

def StepInto():
    """
    Step-into, exactly the same when you hit F7
    """
    Run(STAT_STEPIN)

def StepOver():
    """
    Step-over, exactly the same when you hit F8
    """
    Run(STAT_STEPOVER)

def ExecuteUntilRet():
    """
    Execute until RET instruction, exactly the same when you hit ctrl+F9
    """
    Run(STAT_TILLRET)

def Disass(c, address = 0):
    """
    A high level version of the disass function ; this one is able to disassemble
    more than one instruction.
    """
    sizeof_disassembled_stuff = 0
    complete_disass = []
    sizeof_to_disass = len(c)

    while sizeof_disassembled_stuff != sizeof_to_disass:
        size_current_instruction, disass = Disasm_(c, address + sizeof_disassembled_stuff)
        
        # don't want unicode string
        disass = str(disass)

        # The engine didn't find a valid x86 code
        if disass == '???':
            break

        # In the other case, we have valid assembly code
        complete_disass.append({
            'text' : disass,
            'size' : size_current_instruction    
        })

        sizeof_disassembled_stuff += size_current_instruction
        c = c[size_current_instruction:]

    return complete_disass
