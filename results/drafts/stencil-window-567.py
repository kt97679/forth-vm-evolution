#!/usr/bin/env python3
"""results/drafts/stencil-window-567.py - jit_scan's window against the stencils GCC makes (Iteration 567).

Over 84 flag sets (x86-64 and i386; alignhot's -falign-*=32 and 64; -O2, -O3, -Os; the flag genes' commonest sets;
every JIT define): each stencil's extent - its start to the end of its last exit (jmp NEXT or JUMP; EXIT's first ret),
what jit_scan must read - and lab/evolve/stencil-check.py at the old window (160) and at jit.c's (stencil-check reads
the window from the after-seed-81 batch on - jitscan-after-seed81.patch). Run from the tree:
    python3 results/drafts/stencil-window-567.py        (about four minutes)
Iteration 567's figures: the longest 146 bytes at 32-byte alignment, 242 at 64 (st_ummod, -Os); at 160, 17 of 84 sets
cut a stencil (st_execute 16, st_callx 4, st_ummod 1), all at 64; at 512, none.
"""
import os, re, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
E, SC = os.path.join(ROOT, 'engine'), os.path.join(ROOT, 'lab', 'evolve', 'stencil-check.py')
JD = ['-DJITX=1', '-DJITINL=1', '-DJITLOOP=1', '-DJITEXEC=1', '-DJITMUL=1', '-DJITFUSE=1']
def extents(cc, fl):
    with tempfile.TemporaryDirectory() as d:
        o = os.path.join(d, 's.o')
        if subprocess.run(cc.split() + fl + ['-I', E, '-c', '-o', o, os.path.join(E, 'spn-stencils.c')], capture_output=True).returncode: return {}
        dis = subprocess.run(['objdump', '-dr', '--no-show-raw-insn', '-j', '.text', o], capture_output=True, text=True).stdout
    f, cur = {}, None                       # name -> [start, last mnemonic, extent]
    for l in dis.split('\n'):
        m = re.match(r'^([0-9a-f]+) <([^>]+)>:$', l)
        if m: cur = m.group(2); f[cur] = [int(m.group(1), 16), None, None]; continue
        if cur is None: continue
        m = re.match(r'^\s+([0-9a-f]+):\s+R_\S+\s+(\S+)', l)
        if m and re.sub(r'[-+]0x[0-9a-f]+$', '', m.group(2)) in ('spn_next', 'spn_jump') and f[cur][1] == 'jmp':
            f[cur][2] = int(m.group(1), 16) + 4 - f[cur][0]; continue
        m = re.match(r'^\s+([0-9a-f]+):\s+(\S+)', l)
        if m:
            f[cur][1] = m.group(2)
            if cur == 'st_exit' and m.group(2).startswith('ret') and f[cur][2] is None: f[cur][2] = int(m.group(1), 16) + 1 - f[cur][0]
    return {k: v[2] for k, v in f.items() if k.startswith('st_') and v[2]}
def check(cc, fl, window):
    r = subprocess.run([sys.executable, SC, '--cc', cc] + fl, capture_output=True, text=True, env=dict(os.environ, STENCIL_WINDOW=window))
    return r.returncode, re.findall(r'^  (st_\w+) - ', r.stdout, re.M)
EXTRA = ([], ['-ftracer'], ['-fno-crossjumping', '-ftracer'], ['-fno-reorder-blocks'], ['-fno-gcse'], ['-fpeel-loops', '-fipa-cp-clone'], ['-fcf-protection=none'])
rows, cut = [], {'160': {}, '': {}}
for cc in ('gcc', 'gcc -m32 -fno-pie'):
    for a in ('32', '64'):
        for opt in ('-O2', '-O3', '-Os'):
            for x in EXTRA:
                fl = [opt] + x + JD + ['-falign-jumps=' + a, '-falign-labels=' + a, '-falign-functions=' + a]
                ex = extents(cc, fl); k = max(ex, key=ex.get) if ex else None
                rows.append((a, ex.get(k, 0), k, cc, ' '.join([opt] + x)))
                for w in cut:
                    rc, names = check(cc, fl, w)
                    if rc: cut[w]['%s %s %s' % (cc, a, ' '.join([opt] + x))] = names
for a in ('32', '64'):
    r = max((x for x in rows if x[0] == a), key=lambda x: x[1])
    print('alignment %s: the longest stencil %d bytes (%s; %s, %s)' % (a, r[1], r[2], r[3], r[4]))
for w, c in cut.items():
    names = [n for v in c.values() for n in v]
    print('stencil-check at %s: %d of %d flag sets cut a stencil%s' % (w or "jit.c's window", len(c), len(rows),
          ' - ' + ', '.join('%s %d' % (n, names.count(n)) for n in sorted(set(names))) if c else ''))
    for s in sorted(c): print('  %s: %s' % (s, ', '.join(c[s])))
