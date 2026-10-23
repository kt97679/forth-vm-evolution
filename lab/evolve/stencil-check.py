#!/usr/bin/env python3
"""stencil-check.py [--cc 'gcc -m32 -fno-pie'] [FLAGS ...] - are SPN's stencils safe to copy? (Iteration 463)

The JIT copies each stencil's machine code out of the engine and patches its holes (engine/jit.c). That is right only
if nothing in a stencil points out of it except the three markers (spn_next, spn_jump, spn_call), which are the holes
for control. Gforth's rule (Ertl and Paysan, "Code-Copying Compilation in Production", 2025): a snippet that refers to
anything outside itself through a PC-relative address - a call GCC put there (memset, __stack_chk_fail, mcount), a
constant in .rodata - is not relocatable. Copy-and-patch finds such references exactly: they are the object file's
relocations (Xu and Kjolstad 2021; CPython's JIT). So: compile engine/spn-stencils.c alone with the flags given, read
its relocations and symbols, and list every relocation inside a stencil whose target is not a marker. Exit 1 if any.
"""
import os, re, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
args = sys.argv[1:]; cc = ['gcc']
if args[:1] == ['--cc']: cc = args[1].split(); args = args[2:]
flags = args or ['-O2', '-DJITX=1', '-DJITINL=1', '-DJITLOOP=1']
MARKERS = {'spn_next', 'spn_jump', 'spn_call'}
with tempfile.TemporaryDirectory() as d:
    o = os.path.join(d, 'st.o')
    r = subprocess.run(cc + flags + ['-I', os.path.join(ROOT, 'engine'), '-c', '-o', o, os.path.join(ROOT, 'engine', 'spn-stencils.c')], capture_output=True, text=True)
    if r.returncode: sys.exit('stencil-check: did not compile: ' + r.stderr.strip()[-300:])
    syms = subprocess.run(['readelf', '-sW', o], capture_output=True, text=True).stdout
    rels = subprocess.run(['readelf', '-rW', o], capture_output=True, text=True).stdout
funcs = []                                    # (start, end, name) of every function in .text
for l in syms.split('\n'):
    f = l.split()
    if len(f) >= 8 and f[3] == 'FUNC' and f[6] not in ('UND', 'ABS'):
        funcs.append((int(f[1], 16), int(f[1], 16) + int(f[2]), f[7]))
bad, n, sec = [], 0, None
for l in rels.split('\n'):
    m = re.match(r"Relocation section '([^']+)'", l)
    if m: sec = m.group(1); continue
    f = l.split()
    if sec not in ('.rela.text', '.rel.text') or len(f) < 5 or not re.match(r'^[0-9a-f]+$', f[0]): continue
    off = int(f[0], 16); target = f[4] if len(f) > 4 else '?'; n += 1
    fn = next((name for a, b, name in funcs if a <= off < b), None)
    if fn and fn.startswith('st_') and target not in MARKERS: bad.append((fn, f[2], target))
stencils = sum(1 for _, _, name in funcs if name.startswith('st_'))
print('stencil-check (%s %s): %d stencils, %d code relocations; %s' % (' '.join(cc), ' '.join(flags), stencils, n,
      'all to the markers - every stencil safe to copy' if not bad else '%d not safe to copy:' % len(set(b[0] for b in bad))))
for fn in sorted(set(b[0] for b in bad)):
    print('  %s -> %s' % (fn, ', '.join(sorted(set('%s (%s)' % (t, k) for f2, k, t in bad if f2 == fn)))))
sys.exit(1 if bad else 0)
