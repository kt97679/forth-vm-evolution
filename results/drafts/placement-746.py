#!/usr/bin/env python3
"""results/drafts/placement-746.py INPUT KEPT-OLD KEPT-NEW [KEPT-OLD KEPT-NEW ...] (Iteration 746) - is a speed change
between two builds of one design its instructions or its code's place? For each pair of kept builds (lab/evolve/design.py
ID --db DB --keep DIR loop, in a worktree at each commit): the instructions on INPUT (cachegrind's Ir - exact), the
engine's size, where virtual_machine starts (engine.full's symbols; modulo 64, the cache line), and its body compared
with addresses taken out (data addresses, branch targets as offsets from the function's start): how many of its
instructions differ, and the first offset that does. Run as the build user; valgrind and objdump on the PATH.

Iteration 746 (results/drafts/scalecheck-746.md): f0ab9ee997, c15ec6a706 and e2b7c31a92 at seed 96's tree (67767161)
and the after-seed-96 batch's (7081f965), INPUT the loop workload cut to two BENCHes (the same source in both trees)."""
import difflib, os, re, subprocess, sys


def ir(k, inp):
    p = subprocess.run(['valgrind', '--tool=cachegrind', '--cache-sim=no', '--cachegrind-out-file=/dev/null',
                        os.path.join(k, 'engine'), os.path.join(k, 'image.img')], input=inp, cwd=os.path.join(k, 'work'),
                       capture_output=True, timeout=1200)
    m = re.search(rb'I\s+refs:\s+([\d,]+)', p.stderr)
    return int(m.group(1).replace(b',', b'')) if m else None


def body(k):
    out = subprocess.run(['objdump', '-d', '--no-show-raw-insn', '--disassemble=virtual_machine', os.path.join(k, 'engine.full')],
                         capture_output=True, text=True).stdout
    lines = [l for l in out.splitlines() if re.match(r'\s+[0-9a-f]+:\t', l)]
    start = int(lines[0].split(':')[0], 16)
    ins = []
    for l in lines:
        a, txt = l.split(':\t', 1)
        txt = re.sub(r'\s+<[^>]*>', '', txt); txt = re.sub(r'#.*$', '', txt)
        txt = re.sub(r'-?0x[0-9a-f]+\(%rip\)', 'D(%rip)', txt)
        txt = re.sub(r'\b(0x)?([0-9a-f]{6,})\b', lambda m: '+%d' % (int(m.group(2), 16) - start)
                     if abs(int(m.group(2), 16) - start) < 1 << 20 else m.group(0), txt)
        ins.append((int(a, 16) - start, txt.strip()))
    return start, ins


inp = open(sys.argv[1], 'rb').read()
for a, b in zip(sys.argv[2::2], sys.argv[3::2]):
    ia, ib = ir(a, inp), ir(b, inp)
    sa, A = body(a); sb, B = body(b)
    sm = difflib.SequenceMatcher(None, [t for o, t in A], [t for o, t in B], autojunk=False)
    ch = [op for op in sm.get_opcodes() if op[0] != 'equal']
    first = A[ch[0][1]][0] if ch and ch[0][1] < len(A) else None
    print('%s -> %s' % (os.path.basename(a), os.path.basename(b)))
    print('  instructions on the input %s -> %s (%+d); engine %d -> %d B' % (format(ia, ','), format(ib, ','), ib - ia,
          os.path.getsize(os.path.join(a, 'engine')), os.path.getsize(os.path.join(b, 'engine'))))
    print('  virtual_machine at 0x%x (line offset %d) -> 0x%x (%d); %d -> %d instructions, %d differ, the first at +%s'
          % (sa, sa % 64, sb, sb % 64, len(A), len(B), sum(max(i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in ch), first))
