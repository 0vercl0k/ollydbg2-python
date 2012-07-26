import sys
import os
from ollyapi import *

def display_registers(r):
    print 'EAX: %#.8x' % r.r[REG_EAX]
    print 'ECX: %#.8x' % r.r[REG_ECX]
    print 'EDX: %#.8x' % r.r[REG_EDX]
    print 'EBX: %#.8x' % r.r[REG_EBX]

    print 'ESP: %#.8x' % r.r[REG_ESP]
    print 'EBP: %#.8x' % r.r[REG_EBP]
    
    print 'ESI: %#.8x' % r.r[REG_ESI]
    print 'EDI: %#.8x' % r.r[REG_EDI]

def get_name_address_symbols(f):
    """
     Address         Publics by Value

     0001:00000000       sub_401000
     0001:00000010       sub_401010
     0001:0000002A       loc_40102A
     0001:00000040       sub_401040
     0001:00000090       loc_401090
     """
    sections = GetPESections()
    state = None
    symbols = []
    for line in f.readlines():
        line = line.strip()

        if line.startswith('Address'):
            state = 'PreMarkerOK'
            continue

        if line == '' and state == 'PreMarkerOK':
            state = 'MarkerOK'
            continue
        
        if line == '' and state == 'MarkerOK':
            break
        
        if state == 'MarkerOK':
            full_addr, name = line.split('       ', 2)
            segment_selector, addr = full_addr.split(':', 2)
            absolute_addr = 0
            absolute_addr = sections[int(segment_selector) - 1].base + int(addr, 16)
            symbols.append({
                'name' : name,
                'addr' : absolute_addr
            })

    return symbols

def callz():
    mapfile_path = 'b.map'
    f = open(mapfile_path, 'r')
    pair_address_symbol = get_name_address_symbols(f)
    for symbol in pair_address_symbol:
        AddUserLabel(symbol['addr'], symbol['name'])

s = GetPESections()
for i in s:
    print '%s - %#.8x' % (i.sectname, i.base)

#callz()
print 'symbol fully imported.'

regz = GetCurrentThreadRegisters()
display_registers(regz)

AddUserComment(regz.r[REG_EAX], 'hi this is EAX')
AddUserLabel(regz.r[REG_EAX], 'sup eax')

print ''.join('\\x%.2x' % ord(i) for i in ReadMemory(regz.r[REG_EAX], 16, 0))

WriteMemory(regz.r[REG_EAX], 'testin', 6)

print ''.join('\\x%.2x' % ord(i) for i in ReadMemory(regz.r[REG_EAX], 16, 0))

print '%#.8x' % ResolveApiAddress('kernel32', 'GetProcAddress')