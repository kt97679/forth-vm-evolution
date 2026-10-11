#!/usr/bin/env python3
"""tools/elf_tight.py - an executable as it ships (Iteration 149): the ELF
header, the program headers and the bytes they load - nothing after them.
The section headers, their names, the symbol tables and the compiler's
.comment are for tools (nm, objdump, gdb), not for the kernel, which loads a
file from its program headers alone - SmithForth's hand-made ELF is the
proof (dacvs.neocities.org/SF). What runs is the same bytes; keep the full
file for analysis. ELF32 and ELF64, little-endian; anything else untouched.

    python3 tools/elf_tight.py IN [OUT]      OUT defaults to IN, rewritten
"""
import struct, sys

def tighten(data):
    """The tight form of an ELF file's bytes, or None if it is not one this knows."""
    if len(data) < 52 or data[:4] != b'\x7fELF' or data[5] != 1: return None
    if data[4] == 2:      # ELF64: e_phoff 0x20, e_phentsize/e_phnum 0x36, e_shoff 0x28, e_shentsize.. 0x3A
        phoff, = struct.unpack_from('<Q', data, 0x20); phent, phnum = struct.unpack_from('<HH', data, 0x36)
        segs = [struct.unpack_from('<IIQQQQ', data, phoff + i * phent) for i in range(phnum)]
        spans = [(s[2], s[5]) for s in segs]                        # (p_offset, p_filesz)
        sh_off, sh_fields, sh_size = 0x28, 0x3A, 8
    elif data[4] == 1:    # ELF32: e_phoff 0x1C, e_phentsize/e_phnum 0x2A, e_shoff 0x20, e_shentsize.. 0x2E
        phoff, = struct.unpack_from('<I', data, 0x1C); phent, phnum = struct.unpack_from('<HH', data, 0x2A)
        segs = [struct.unpack_from('<IIIII', data, phoff + i * phent) for i in range(phnum)]
        spans = [(s[1], s[4]) for s in segs]
        sh_off, sh_fields, sh_size = 0x20, 0x2E, 4
    else:
        return None
    if not segs: return None
    end = max([phoff + phnum * phent] + [o + n for o, n in spans if n])   # every segment with file bytes
    out = bytearray(data[:min(end, len(data))])
    out[sh_off:sh_off + sh_size] = bytes(sh_size)                  # e_shoff
    out[sh_fields:sh_fields + 6] = bytes(6)                        # e_shentsize, e_shnum, e_shstrndx
    return bytes(out)

if __name__ == '__main__':
    src = sys.argv[1]; dst = sys.argv[2] if len(sys.argv) > 2 else src
    data = open(src, 'rb').read(); t = tighten(data)
    if t is None: sys.exit('%s: not a little-endian ELF32/ELF64 - left as it is' % src)
    import os
    mode = os.stat(src).st_mode
    open(dst, 'wb').write(t); os.chmod(dst, mode)
    print('%s: %d -> %d bytes' % (dst, len(data), len(t)))
