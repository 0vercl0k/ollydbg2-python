#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    sym_constants.py - Structure need to call the Symbol API
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

MAX_SYM_NAME = 2000

class symbol_info_t(Structure):
    """
    Contains symbol information.
    Size: 88bytes
    """
    _pack_ = 8
    _fields_ = [
        # The size of the structure, in bytes. This member must be set to sizeof(SYMBOL_INFO).
        # Note that the total size of the data is the SizeOfStruct + (MaxNameLen - 1) * sizeof(TCHAR).
        # The reason to subtract one is that the first character in the name is accounted for in the size of the structure.
        ('SizeOfStruct', c_ulong),

        # A unique value that identifies the type data that describes the symbol. This value does not persist between sessions.
        ('TypeIndex', c_ulong),

        # This member is reserved for system use.
        ('Reserved', c_longlong * 2),

        # The unique value for the symbol. The value associated with a symbol is not guaranteed to be the same each time you run the process.
        # For PDB symbols, the index value for a symbol is not generated until the symbol is enumerated or retrieved through a search by name or address.
        # The index values for all CodeView and COFF symbols are generated when the symbols are loaded.
        ('Index', c_ulong),

        # The symbol size, in bytes.
        # This value is meaningful only if the module symbols are from a pdb file; otherwise, this value is typically zero and should be ignored.
        ('Size', c_ulong),

        # The base address of the module that contains the symbol.
        ('ModBase', c_longlong),

        ('Flags', c_ulong),

        # The value of a constant.
        ('Value', c_longlong),

        # The virtual address of the start of the symbol.
        ('Address', c_longlong),

        # The register.
        ('Register', c_ulong),

        # The DIA scope.
        # For more information, see the Debug Interface Access SDK in the Visual Studio documentation. 
        # (This resource may not be available in some languages and countries.)
        ('Scope', c_ulong),

        # The PDB classification.
        # These values are defined in Dbghelp.h in the SymTagEnum enumeration type.
        ('Tag', c_ulong),

        # The length of the name, in characters, not including the null-terminating character.
        # addr_array = addressof(struct) + sizeof(ULONG) + sizeof(ULONG)
        # s = string_at(addr_array)
        ('NameLen', c_ulong),

        # The size of the Name buffer, in characters.
        # If this member is 0, the Name member is not used.
        ('MaxNameLen', c_ulong),

        # The name of the symbol.
        # The name can be undecorated if the SYMOPT_UNDNAME option is used with the SymSetOptions function.
        ('Name', c_char * 1)
    ]

symbol_info_p = POINTER(symbol_info_t)

class guid_t(Structure):
    """
    GUIDs identify objects such as interfaces, manager entry-point vectors (EPVs), and class objects.
    A GUID is a 128-bit value consisting of one group of 8 hexadecimal digits,
    followed by three groups of 4 hexadecimal digits each, followed by one group of 12 hexadecimal digits.
    The following example GUID shows the groupings of hexadecimal digits in a GUID: 6B29FC40-CA47-1067-B31D-00DD010662DA

    Size: 16bytes
    """
    _pack_ = 4
    _fields_ = [
        ('Data1', c_ulong),
        ('Data2', c_ushort),
        ('Data3', c_ushort),
        ('Data4', c_char * 8)
    ]

class imagehlp_module64_t(Structure):
    """
    Contains module information.
    Size: 1672
    """
    _pack_ = 8
    _fields_ = [
        # The size of the structure, in bytes.
        # The caller must set this member to sizeof(IMAGEHLP_MODULE64).
        ('SizeOfStruct', c_ulong),

        # The base virtual address where the image is loaded.
        ('BaseOfImage', c_longlong),

        # The size of the image, in bytes.
        ('ImageSize', c_ulong),

        # The date and timestamp value.
        # The value is represented in the number of seconds elapsed since midnight (00:00:00), January 1, 1970, 
        # Universal Coordinated Time, according to the system clock.
        # The timestamp can be printed using the C run-time (CRT) function ctime.
        ('TimeDateStamp', c_ulong),

        # The checksum of the image.
        # This value can be zero.
        ('CheckSum', c_ulong),

        # The number of symbols in the symbol table.
        # The value of this parameter is not meaningful when SymPdb is specified as the value of the SymType parameter.
        ('NumSyms', c_ulong),

        # The type of symbols that are loaded.
        ('SymType', c_int),

        # The module name.
        ('ModuleName', c_char * 32),

        # The image name. The name may or may not contain a full path.
        ('ImageName', c_char * 256),

        # The full path and file name of the file from which symbols were loaded.
        ('LoadedImageName', c_char * 256),

        # The full path and file name of the .pdb file.
        ('LoadedPdbName', c_char * 256),

        # The signature of the CV record in the debug directories.
        ('CVSig', c_ulong),

        # The contents of the CV record.
        ('CVData', c_char * (MAX_PATH * 3)),

        # The PDB signature.
        ('PdbSig', c_ulong),

        # The PDB signature (Visual C/C++ 7.0 and later)
        ('PdbSig70', guid_t),

        # The DBI age of PDB.
        ('PdbAge', c_ulong),

        # A value that indicates whether the loaded PDB is unmatched.
        ('PdbUnmatched', c_long),

        # A value that indicates whether the loaded DBG is unmatched.
        ('DbgUnmatched', c_long),

        # A value that indicates whether line number information is available.
        ('LineNumbers', c_long),

        # A value that indicates whether symbol information is available.
        ('GlobalSymbols', c_long),

        # A value that indicates whether type information is available.
        ('TypeInfo', c_long),

        # A value that indicates whether the .pdb supports the source server.
        ('SourceIndexed', c_long),

        # A value that indicates whether the module contains public symbols.
        ('Publics', c_long),
    ]

imagehlp_module64_p = POINTER(imagehlp_module64_t)
