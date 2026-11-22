#!/usr/bin/env python3
"""lab/evolve/data-layout-check.py MAP [MAP ...] | --self-test - engine/data-layout.ld checked on a link map (ld -Map; Iteration 734):
each of .bss.hot, .bss.tab, .bss and .bss.big with its members (name, size), and a FAULT for a member of 4 KB or more
outside .bss.big (t_obuf and heads excepted: .bss.tab's end, by design) or one of 512 B or more in .bss.hot (a name engine/data-layout.ld's lists missed). Exit 1 on a fault.
--self-test: two roles built by the lab with a map, checked (run-tests)."""
import os, re, shutil, sys, tempfile

OUT = ('.bss.hot', '.bss.tab', '.bss', '.bss.big')
bad = 0
maps = sys.argv[1:]
if maps[:1] == ['--self-test']:
    # run-tests: two roles built by the lab with a link map beside them - best-all-round (the JIT, the tag, tos: every
    # buffer the engine has) and least-memory (GCC) - and checked; on a host without GNU ld's script (EVOLVE_LIBC,
    # profiling) nothing is linked by it and there is nothing to check
    import json
    ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); sys.argv = ['x']
    import evolve as E
    E.setup(); tmp = tempfile.mkdtemp(prefix='dlc-'); maps = []
    for n in ('best-all-round', 'least-memory'):
        g = json.load(open(os.path.join(ROOT, 'designs', n, 'record.json')))['genome']
        m = os.path.join(tmp, n + '.map'); E._EXTRA_CFLAGS[:] = ['-Wl,-Map=' + m]
        E.build(E.canon(g), os.path.join(tmp, n)); maps.append(m)
    E._EXTRA_CFLAGS[:] = []
for path in maps:
    lines = open(path).read().split('\n')
    cur, mem, size = None, {k: [] for k in OUT}, {}
    i = 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r'^(\.\S+)\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)', l)
        m1 = re.match(r'^(\.\S+)\s*$', l)
        if m or m1:          # an output section: its name at the line's start (the address on the next line if long)
            name = (m or m1).group(1)
            if m1 and i + 1 < len(lines):
                m2 = re.match(r'^\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)', lines[i + 1])
                if m2: size[name] = int(m2.group(2), 16)
            elif m: size[name] = int(m.group(3), 16)
            cur = name if name in OUT else None
            i += 1; continue
        if cur:
            m = re.match(r'^ (\.bss\S*|COMMON)\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)', l)
            m1 = re.match(r'^ (\.bss\S*|COMMON)\s*$', l)
            if m1 and i + 1 < len(lines):
                m2 = re.match(r'^\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)', lines[i + 1])
                if m2: m, i = (m1.group(1), int(m2.group(2), 16)), i + 1
            elif m: m = (m.group(1), int(m.group(3), 16))
            if m and m[1]: mem[cur].append(m)
        i += 1
    print('%s:' % path)
    for k in OUT:
        if k not in size and not mem[k]: continue
        ms = sorted(mem[k], key=lambda x: -x[1])
        print('  %-9s %7d B  %3d members: %s' % (k, size.get(k, 0), len(ms), ', '.join('%s %d' % (n[5:] or n, s) for n, s in ms[:12]) + (' ...' if len(ms) > 12 else '')))
        for n, s in ms:
            if (k != '.bss.big' and s >= 4096 and not (k == '.bss.tab' and re.search(r'(^|\.)(t_obuf|heads)(\.\d+)?$', n[5:]))) or (k == '.bss.hot' and s >= 512):
                print('  FAULT     %s (%d B) in %s - engine/data-layout.ld names it nowhere it belongs' % (n, s, k)); bad += 1
if 'tmp' in dir(): shutil.rmtree(tmp, ignore_errors=True)
print('data-layout-check: %s' % ('PASS - %d links, every buffer of 4 KB or more in .bss.big' % len(maps) if not bad else 'FAILED - %d' % bad))
sys.exit(1 if bad else 0)
