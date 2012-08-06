#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    utils_constants.py - The constants used by the utils functions.
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

# Max length of argument string
ARGLEN = 1024

# User-defined comment
NM_COMMENT = 0x30
# User-defined label
NM_LABEL   = 0x21

# Used by Run() function
(
    # No process to debug
    STAT_IDLE,

    # Loading new process
    STAT_LOADING,

    # Attaching to the running process
    STAT_ATTACHING,

    # All threads are running -- f9
    STAT_RUNNING,

    # Single thread is running
    STAT_RUNTHR,

    # Stepping into, single thread -- f7
    STAT_STEPIN,

    # Stepping over, single thread -- f8
    STAT_STEPOVER,

    # Animating into, single thread
    STAT_ANIMIN,

    # Animating over, single thread
    STAT_ANIMOVER,

    # Tracing into, single thread
    STAT_TRACEIN,

    # Tracing over, single thread
    STAT_TRACEOVER,

    # SFX using run trace, single thread
    STAT_SFXRUN,

    # SFX using hit trace, single thread
    STAT_SFXHIT,

    # SFX to known entry, single thread
    STAT_SFXKNOWN,

    # Stepping until return, single thread
    STAT_TILLRET,

    # Stepping over return, single thread
    STAT_OVERRET,

    # Stepping till user code, single thread
    STAT_TILLUSER,

    # Process is requested to pause
    STAT_PAUSING,

    # Process paused on debugging event
    STAT_PAUSED,

    # Process is terminated but in memory
    STAT_FINISHED,

    STAT_CLOSING
) = range(0, 21)


class t_exe(Structure):
    """
    Description of executable module
    Size: 532
    """
    _pack_ = 4
    _fields_ = [
        # Module base
        ('base', c_ulong),

        # Module size
        ('size', c_ulong),

        # Whether base is already adjusted
        ('adjusted', c_int),

        # Full module path
        ('path', c_wchar * MAXPATH),
    ]

class t_jmp(Structure):
    """
    Descriptor of recognized jump or call
    Size: 9
    """
    _pack_ = 1
    _fields_ = [
        # Address of jump/call command
        ('from', c_ulong),

        # Adress of jump/call destination
        ('dest', c_ulong),

        # Jump/call type, one of JT_xxx
        ('type', c_ubyte)
    ]

class t_jmpdata(Structure):
    """
    Jump table
    Size: 44bytes
    """
    _pack_ = 4
    _fields_ = [
        # Base of module owning jump table
        ('modbase', c_ulong),

        # Size of module owning jump table
        ('modsize', c_ulong),

        # Jump data, sorted by source
        ('jmpdata', POINTER(t_jmp)),

        # Indices to jmpdata, sorted by dest
        ('jmpindex', POINTER(c_int)),

        # Total number of elements in arrays
        ('maxjmp', c_int),

        # Number of used elements in arrays
        ('njmp', c_int),

        # Number of sorted elements in arrays
        ('nsorted', c_int),

        # Do not sort data implicitly
        ('dontsort', c_int),

        # Pointed modules, unsorted
        ('exe', POINTER(t_exe)),

        # Allocated number of elements in exe
        ('maexe',  c_int),

        # Number of used elements in exe
        ('nexe', c_int)
    ]

class t_netstream(Structure):
    """
    Location of default .NET stream
    Size: 8bytes
    """
    _pack_ = 4
    _fields_ = [
        # Base address in memory
        ('base', c_ulong),

        # Stream size, bytes
        ('size', c_ulong)
    ]

class t_metadata(Structure):
    """
    Descriptor of .NET MetaData table
    Size: 16bytes
    """
    _pack_ = 4
    _fields_ = [
        # Location in memory or NULL if absent
        ('base', c_ulong),

        # Number of rows or 0 if absent
        ('rowcount', c_ulong),

        # Size of single row, bytes, or 0
        ('rowsize', c_ulong),

        # Offset of name field
        ('nameoffs', c_ushort),

        # Size of name or 0 if absent
        ('namesize', c_ushort)
    ]

class t_secthdr(Structure):
    """
    Extract from IMAGE_SECTION_HEADER
    Size: 48bytes
    """
    _pack_ = 4
    _fields_ = [
        # Null-terminated section name
        ('sectname', c_wchar * 12),

        # Address of section in memory
        ('base', c_ulong),

        # Size of section loaded into memory
        ('size', c_ulong),

        # Set of SHT_xxx
        ('type', c_ulong),

        # Offset of section in file
        ('fileoffset', c_ulong),

        # Size of section in file
        ('rawsize', c_ulong),

        # Set of IMAGE_SCN_xxx
        ('characteristics', c_ulong)
    ]

class t_nested(Structure):
    """
    Descriptor of nested data
    Size: 24bytes
    """
    _pack_ = 4
    _fields_ = [
        # Actual number of elements
        ('n', c_int),

        # Maximal number of elements
        ('nmax', c_int),

        # Size of single element
        ('itemsize', c_ulong),

        # Ordered nested data
        ('data', c_void_p),

        # Changes on each modification
        ('version', c_ulong),

        # Destructor function or NULL -- XXX: create a pointer function type
        ('destfunc', c_ulong),
    ]

class t_simple(Structure):
    """
    Simple data container
    Size: 20bytes
    """
    _pack_ = 4
    _fields_ = [
        # Data heap
        ('heap', POINTER(c_ubyte)),

        # Size of data element, bytes
        ('itemsize', c_ulong),

        # Size of allocated data heap, items
        ('maxitem', c_int),

        # Actual number of data items
        ('nitem', c_int),

        # Whether data is sorted
        ('sorted', c_int)
    ]

class t_sorted(Structure):
    """
    Descriptor of sorted data
    Size: 68bytes
    """
    _pack_ = 4
    _fields_ = [
        # Actual number of entries
        ('n', c_int),

        # Maximal number of entries
        ('nmax', c_int),

        # Size of single entry
        ('itemsize', c_ulong),

        # Storage mode, set of SDM_xxx
        ('mode', c_int),

        # Sorted data, NULL if SDM_INDEXED
        ('data', c_void_p),

        # NBLOCK sorted data blocks, or NULL
        ('block', POINTER(c_void_p)),

        # Number of allocated blocks
        ('nblock', c_int),

        # Changes on each modification
        ('version', c_ulong),

        # Pointers to data, sorted by address
        ('dataptr', POINTER(c_void_p)),

        # Index of selected entry
        ('selected', c_int),

        # Base address of selected entry
        ('seladdr', c_ulong),

        # Subaddress of selected entry
        ('selsubaddr', c_ulong),

        # Function which sorts data or NULL -- XXX: should create a function pointer type
        ('sortfunc', POINTER(c_void_p)),

        # Destructor function or NULL -- XXX: should create a function pointer type
        ('destfunc', POINTER(c_void_p)),

        # Sorting criterium (column)
        ('sort', c_int),

        # Whether indexes are sorted
        ('sorted', c_int),

        # Indexes, sorted by criterium
        ('sortindex', POINTER(c_int))
    ]

# Max number of saved called modules
NCALLMOD = 24
# Max length of short or module name
SHORTNAME = 32
# Number of default .NET streams
NETSTREAM = 5
# Number of .NET MetaData tables
MDTCOUNT = 64

class t_module(Structure):
    """
    Descriptor of executable module
    Size: 4016bytes
    """
    _pack_ = 4
    _fields_ = [
        # Base address of module
        ('base', c_ulong),

        # Size of memory occupied by module
        ('size', c_ulong),

        # Service information, TY_xxx+MOD_xxx
        ('type', c_ulong),

        # Short name of the module
        ('modname', c_wchar * SHORTNAME),

        # Full name of the module
        ('path', c_wchar * MAXPATH),

        # Version of executable file     
        ('version', c_wchar * TEXTLEN),

        # Base of image in executable file      
        ('fixupbase', c_ulong),

        # Base address of module code block
        ('codebase', c_ulong),

        # Size of module code block
        ('codesize', c_ulong),

        # Address of <ModuleEntryPoint> or 0
        ('entry', c_ulong),

        # Address of SFX-packed entry or 0
        ('sfxentry', c_ulong),

        # Address of WinMain or 0
        ('winmain', c_ulong),

        # Base address of module data block
        ('database', c_ulong),

        # Base address of export data table
        ('edatabase', c_ulong),

        # Size of export data table
        ('edatasize', c_ulong),

        # Base address of import data table
        ('idatatable', c_ulong),

        # Base of Import Address Table
        ('iatbase', c_ulong),

        # Size of IAT
        ('iatsize', c_ulong),

        # Base address of relocation table
        ('relocbase', c_ulong),

        # Size of relocation table
        ('relocsize', c_ulong),

        # Base address of resources
        ('resbase', c_ulong),

        # Size of resources
        ('ressize', c_ulong),

        # Base address of TLS directory table
        ('tlsbase', c_ulong),

        # Size of TLS directory table
        ('tlssize', c_ulong),

        # Address of first TLS callback or 0
        ('tlscallback', c_ulong),

        # .NET entry (MOD_NETAPP only)
        ('netentry', c_ulong),

        # .NET CLI header base (MOD_NETAPP)
        ('clibase', c_ulong),

        # .NET CLI header base (MOD_NETAPP)
        ('clisize', c_ulong),

        # Locations of default .NET streams
        ('netstr', t_netstream * NETSTREAM),

        # Descriptors of .NET MetaData tables
        ('metadata', t_metadata * MDTCOUNT),

        # Base of memory block with SFX
        ('sfxbase', c_ulong),

        # Size of memory block with SFX
        ('sfxsize', c_ulong),

        # Size of PE header in file
        ('rawhdrsize', c_ulong),

        # Size of PE header in memory
        ('memhdrsize', c_ulong),

        # Number of sections in the module
        ('nsect', c_int),

        # Extract from section headers
        ('sect', POINTER(t_secthdr)),

        # Number of 32-bit fixups
        ('nfixup', c_int),

        # Array of 32-bit fixups
        ('fixup', POINTER(c_ulong)),

        # Jumps and calls from this module
        ('jumps', t_jmpdata),

        # Loop brackets
        ('loopnest', t_nested),

        # Call argument brackets
        ('argnest', t_nested),

        # Predicted ESP, EBP & results (sd_pred)
        ('predict', t_simple),

        # Resource strings (t_string)
        ('strings', t_sorted),

        # UDD-relevant data is changed
        ('saveudd', c_int),

        # No. of called modules (max. NCALLMOD)
        ('ncallmod', c_int),

        # List of called modules
        ('callmod', ((c_wchar * NCALLMOD) * SHORTNAME))
    ]

t_module_p = POINTER(t_module)

class t_operand_u(Union):
    """
    Value of operand
    Size: 16bytes
    """
    _pack_ = 1
    _fields_ = [
        # Value of operand (integer form)
        ('u', c_ulong),
        # Value of operand (signed form)
        ('s', c_long),
        # Value of operand (general form)
        ('value', c_byte * 16)
    ]

class t_operand(Structure):
    """
    Description of disassembled operand
    Size: 1120bytes
    """
    _pack_ = 4
    _fields_ = [
        # Description of operand.

        # Operand features, set of OP_xxx
        ('features', c_ulong),
        # Operand type, set of B_xxx
        ('arg', c_ulong),
        # DEC_INT, DEC_FLOAT or DEC_UNKNOWN
        ('optype', c_int),
        # Total size of data, bytes
        ('opsize', c_int),
        # Size of element (opsize exc. MMX/SSE)
        ('granularity', c_int),
        # REG_xxx (also ESP in POP) or REG_UNDEF
        ('reg', c_int),
        # List of used regs (not in address!)
        ('uses', c_ulong),
        # List of modified regs (not in addr!)
        ('modifies', c_ulong),

        # Description of memory address.

        # Selector (SEG_xxx)
        ('seg', c_int),
        # Scales of registers in memory address
        ('scale', c_byte * NREG),
        # List of registers used in address
        ('aregs', c_ulong),
        # Constant or const part of address
        ('opconst', c_ulong),

        # Value of operand.

        # Offset to selector (usually addr)
        ('offset', c_ulong),
        # Immediate selector in far jump/call
        ('selector', c_ulong),
        # Address of operand in memory
        ('addr', c_ulong),
        # Value of operand
        ('u', t_operand_u),
        # Actual memory (if OP_ACTVALID)
        ('actual', c_byte * 16),

        # Textual decoding.

        # Operand, decoded to text
        ('text', c_wchar * TEXTLEN),
        # Commented address and contents
        ('comment', c_wchar * TEXTLEN)
    ]

# Maximal allowed number of operands
NOPERAND = 4

class t_disasm(Structure):
    """
    Disassembled command
    Size: 6348bytes
    """
    _pack_ = 4
    _fields_ = [
        # In the case that DA_HILITE flag is set, fill these members before calling
        # Disasm(). Parameter hilitereg has priority over hiliteindex.

        # One of OP_SOMEREG if reg highlighting
        ('hilitereg', c_ulong),
        # Index of register to highlight
        ('hiregindex', c_int),
        # Index of highlighting scheme (0: none)
        ('hiliteindex', c_int),

        # Starting from this point, no need to initialize the members of t_disasm.

        # Address of first command byte
        ('ip', c_ulong),
        # Full length of command, bytes
        ('size', c_ulong),
        # Type of command, D_xxx
        ('cmdtype', c_ulong),
        # List of prefixes, set of PF_xxx
        ('prefixes', c_ulong),
        # Number of prefixes, including SSE2
        ('nprefix', c_ulong),
        # Offset of first 4-byte fixup or -1
        ('memfixup', c_ulong),
        # Offset of second 4-byte fixup or -1
        ('immfixup', c_ulong),
        # Set of DAE_xxx
        ('errors', c_int),
        # Set of DAW_xxx
        ('warnings', c_int),

        # Note that used registers are those which contents is necessary to create
        # result. Modified registers are those which value is changed. For example,
        # command MOV EAX,[EBX+ECX] uses EBX and ECX and modifies EAX. Command
        # ADD ESI,EDI uses ESI and EDI and modifies ESI.
        
        # List of used registers
        ('uses', c_ulong),
        # List of modified registers
        ('modifies', c_ulong),

        # Useful shortcuts.

        # Condition, one of DAF_xxx
        ('condition', c_int),
        # Jump/call destination or 0
        ('jmpaddr', c_ulong),
        # Constant in memory address or 0
        ('memconst', c_ulong),
        # Data size in ENTER/RETN/RETF
        ('stackinc', c_ulong),

        # Operands.
        ('op', t_operand * NOPERAND),

        # Textual decoding.

        # Hex dump of the command
        ('dump', c_wchar * TEXTLEN),
        # Fully decoded command as text
        ('result', c_wchar * TEXTLEN),
        # Mask to highlight result
        ('mask', c_byte * TEXTLEN),
        # Mask corresponds to result
        ('maskvalid', c_int),
        # Comment that applies to whole command
        ('comment', c_wchar * TEXTLEN)
    ]

t_disasm_p = POINTER(t_disasm)

class t_predict_stack(Structure):
    """
    Size: 12bytes
    """
    _pack_ = 4
    _fields_ = [
        # Offset of data on stack (signed!)
        ('soffset', c_long),
        # State of stack data, set of PST_xxx
        ('sstate', c_ulong),
        # Constant related to stack data
        ('sconst', c_ulong)
    ]

class t_predict_mem(Structure):
    """
    Size: 12bytes
    """
    _pack_ = 4
    _fields_ = [
        # Address of doubleword variable
        ('maddr', c_ulong),
        # State of memory, set of PST_xxx
        ('mstate', c_ulong),
        # Constant related to memory data
        ('mconst', c_ulong)
    ]

# Number of predicted stack entries
NSTACK  = 12
# Max no. of predicted stack mod addr
NSTKMOD = 24
# Number of predicted memory locations
NMEM    = 2

class t_predict(Structure):
    """
    Prediction of execution
    Size: 372bytes
    """
    _pack_ = 4
    _fields_ = [
        # Predicted EIP or NULL if uncertain
        ('addr', c_ulong),
        # Must be 1
        ('one', c_ulong),
        # Type of prediction, TY_xxx/PR_xxx
        ('type', c_ulong),
        # State of register, set of PST_xxx
        ('rstate', c_ulong * NREG),
        # Constant related to register
        ('rconst', c_ulong * NREG),
        # State of EIP after jump or return
        ('jmpstate', c_ulong),
        # Constant related to jump or return
        ('jmpconst', c_ulong),
        # Offset of ESP at PUSH EBP
        ('espatpushbp', c_ulong),
        # Number of valid stack entries
        ('nstack', c_int),
        ('stack', t_predict_stack * NSTACK),
        # Number of valid stkmod addresses
        ('nstkmod', c_int),
        # Addresses of stack modifications
        ('stkmod', c_ulong * NSTKMOD),
        # Number of valid memory entries
        ('nmem', c_int),
        ('mem', t_predict_mem * NMEM),
        # State of result of command execution
        ('resstate', c_ulong),
        # Constant related to result
        ('resconst', c_ulong)
    ]

t_predict_p = POINTER(t_predict)

class t_modop(Structure):
    """
    Operand in assembler model
    Size: 17bytes
    """
    _pack_ = 1
    _fields_ = [
        # Operand features, set of AMP_xxx
        ('features', c_byte),
        # (Pseudo)register operand
        ('reg', c_byte),
        # Scales of (pseudo)registers in address
        ('scale', c_byte * NPSEUDO),
        # Constant or const part of address
        ('opconst', c_ulong)
    ]

t_modop_p = POINTER(t_modop)

# Maximal length of valid 80x86 command
MAXCMDSIZE = 16
# Maximal allowed number of operands
NOPERAND = 4

class t_asmmod(Structure):
    """
    Description of assembled command
    Size: 108bytes
    """
    _pack_ = 1
    _fields_ = [
        # Binary code
        ('code', c_byte * MAXCMDSIZE),
        # Mask for binary code (0: bit ignored)
        ('mask', c_byte * MAXCMDSIZE),
        # List of prefixes, set of PF_xxx
        ('prefixes', c_ulong),
        # Length of code w/o prefixes, bytes
        ('ncode', c_byte),
        # Code features, set of AMF_xxx
        ('features', c_byte),
        # Postbyte (if AMF_POSTBYTE set)
        ('postbyte', c_byte),
        # Number of operands (no pseudooperands)
        ('nop', c_byte),
        # Description of operands
        ('op', t_modop * NOPERAND)
    ]

t_asmmod_p = POINTER(t_asmmod)