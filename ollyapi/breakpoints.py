#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    breakpoints.py - A python high level API to play with breakpoints in OllyDBG2
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
from breakpoints_wrappers import *
from utils_wrappers import CheckForDebugEvent
from utils import Run

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
