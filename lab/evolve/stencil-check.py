#!/usr/bin/env python3
"""stencil-check.py [--cc 'gcc -m32 -fno-pie'] [FLAGS ...] - are SPN's stencils safe to copy? (Iteration 463)

The JIT copies each stencil's machine code out of the engine - from its start to its last jump to a marker (NEXT or
JUMP), or for EXIT to its ret - and patches its holes (engine/jit.c, jit_scan). That is right only if nothing in the
copied part leaves it: Gforth's relocatability rule (Ertl and Paysan, "Code-Copying Compilation in Production", 2025).
Two ways to leave, both read here from the object file - exactly, by objdump, not by guessing at bytes:
- a relocation in the copied part whose target is not a marker - a call GCC put in (memset, __stack_chk_fail,
  mcount), a constant in .rodata (copy-and-patch's insight: references out are the relocations);
- a branch in the copied part to an address in the function outside the copied part - a cold block GCC placed after
  the last jump (a stack-protector failure path), which the JIT does not copy.
Compiles engine/spn-stencils.c alone with the flags given; exit 1 if any stencil is not safe to copy.
"""
import os, re, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
args = sys.argv[1:]; cc = ['gcc']
if args[:1] == ['--cc']: cc = args[1].split(); args = args[2:]
flags = args or ['-O2', '-DJITX=1', '-DJITINL=1', '-DJITLOOP=1']
flags = [f for f in flags if f not in ('-ffunction-sections', '-fdata-sections')]   # 557: they only place functions, and
# put each in its own .text.* - this reads .text, so a design's own flags read 0 stencils, "every one safe" vacuously
HOLES = set(re.findall(r'#define JIT_(?:IMM|RP|TH|EX|RS)64\s+0x([0-9a-fA-F]+)', open(os.path.join(ROOT, 'engine', 'jit.c')).read()))
MARKERS = ('spn_next', 'spn_jump', 'spn_call')
with tempfile.TemporaryDirectory() as d:
    o = os.path.join(d, 'st.o')
    r = subprocess.run(cc + flags + ['-I', os.path.join(ROOT, 'engine'), '-c', '-o', o, os.path.join(ROOT, 'engine', 'spn-stencils.c')], capture_output=True, text=True)
    if r.returncode: sys.exit('stencil-check: did not compile: ' + r.stderr.strip()[-300:])
    dis = subprocess.run(['objdump', '-dr', '--no-show-raw-insn', '-j', '.text', o], capture_output=True, text=True).stdout
funcs, cur = {}, None                        # name -> list of (addr, text, [relocation targets])
for l in dis.split('\n'):
    m = re.match(r'^([0-9a-f]+) <([^>]+)>:$', l)
    if m: cur = m.group(2); funcs[cur] = []; continue
    if cur is None: continue
    m = re.match(r'^\s+([0-9a-f]+):\s+R_\S+\s+(\S+)', l)
    if m and funcs[cur]: funcs[cur][-1][2].append(re.sub(r'[-+]0x[0-9a-f]+$', '', m.group(2))); continue
    m = re.match(r'^\s+([0-9a-f]+):\s+(.*)$', l)
    if m: funcs[cur].append((int(m.group(1), 16), m.group(2).strip(), []))
bad = {}; twice = {}                      # twice: a value hole more than once in the copied part (557: jit.c patches every copy)
for name, ins in funcs.items():
    if not name.startswith('st_') or not ins: continue
    # the copied part, as jit_scan finds it: up to the last jmp to NEXT or JUMP; EXIT's to its first ret
    if name == 'st_exit': ends = [k for k, (a, t, rl) in enumerate(ins) if t.startswith('ret')][:1]
    else: ends = [k for k, (a, t, rl) in enumerate(ins) if t.startswith('jmp') and any(x in ('spn_next', 'spn_jump') for x in rl)][-1:]
    if not ends: continue                    # no shape the JIT reads: it is never used
    last = ends[0]; lo = ins[0][0]; hi = ins[last + 1][0] if last + 1 < len(ins) else ins[last][0] + 16
    for h in HOLES:
        k = sum(1 for a, t, rl in ins[:last + 1] if re.search(r'\$0x0*%s\b' % h.lower().lstrip('0'), t))
        if k > 1: twice[name] = k
    for a, t, rl in ins[:last + 1]:
        for x in rl:
            if x not in MARKERS: bad.setdefault(name, set()).add('refers to %s' % x)
        m = re.match(r'^(j\w+|call|loop\w*)\s+([0-9a-f]+) <', t)
        if m and not rl:
            tgt = int(m.group(2), 16)
            if not lo <= tgt < hi: bad.setdefault(name, set()).add('%s to +0x%x, past the copied part' % (m.group(1), tgt - lo))
stencils = sum(1 for n in funcs if n.startswith('st_'))
print('stencil-check (%s %s): %d stencils; %s' % (' '.join(cc), ' '.join(flags), stencils,
      'every one safe to copy' if not bad else '%d not safe to copy:' % len(bad)))
for n in sorted(bad): print('  %s - %s' % (n, '; '.join(sorted(bad[n]))))
if twice: print('  a value hole twice or more in the copied part - jit.c patches every copy (557): ' + ', '.join(sorted(twice)))
if not stencils: print('stencil-check: no stencil read - nothing checked (the flags?)')
sys.exit(1 if bad or not stencils else 0)
