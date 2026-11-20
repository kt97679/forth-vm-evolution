#!/usr/bin/env python3
"""results/drafts/bss-pages-713.py REPO ID - the engine's data and BSS pages a start-up touches (pagemap) and the symbols on each (engine.full's nm) (Iteration 713, early-games-713.md)."""
import json, os, subprocess, sys, tempfile, shutil, time, struct
ROOT, ID = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(ROOT, 'lab/evolve')); sys.argv = ['x']
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
r = [json.loads(l) for l in open(os.path.join(ROOT, 'results/followup-seed96-roles-b.md')) if l.startswith('{"') and ('"%s"' % ID) in l][0]
dd = tempfile.mkdtemp(prefix='bss-'); eng, img = E.build(E.canon(r['genome']), dd); pw = E.private_work(dd)
nm = subprocess.run(['nm', '-S', '-n', eng + '.full'], capture_output=True, text=True).stdout
syms = []
for l in nm.split('\n'):
    f = l.split()
    if len(f) == 4 and f[2] in 'bBdD': syms.append((int(f[0], 16), int(f[1], 16), f[2], f[3]))
print('symbols in .data/.bss with sizes: %d (nm %s)' % (len(syms), 'ok' if syms else 'none - stripped?'))
inp = (E.KERNEL_IN if os.environ.get('KW') else b'')
p = subprocess.Popen([eng, img], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=pw, env={'PATH': '/usr/bin:/bin'})
p.stdin.write(inp); p.stdin.flush(); time.sleep(1.5)
maps = [l.split() for l in open('/proc/%d/maps' % p.pid).read().split('\n') if l]
present = set()
with open('/proc/%d/pagemap' % p.pid, 'rb') as pm:
    for m in maps:
        a, b = (int(x, 16) for x in m[0].split('-'))
        if b - a > 1 << 24 or a >= 1 << 40: continue
        for pg in range(a >> 12, b >> 12):
            pm.seek(pg * 8); bb = pm.read(8)
            if len(bb) < 8: continue
            v = struct.unpack('<Q', bb)[0]
            if v >> 63 or (v >> 62) & 1: present.add(pg)
p.stdin.close(); p.wait()
lo = min(s[0] for s in syms) >> 12 if syms else 0; hi = max(s[0] + s[1] for s in syms) >> 12 if syms else 0
print('symbols:', ', '.join('%s %s %d @%x' % (s[2], s[3], s[1], s[0]) for s in syms))
print('pages in the range %d, touched %d' % (hi - lo + 1, sum(1 for pg in range(lo, hi + 1) if pg in present)))
for pg in [x for x in range(lo, hi + 1) if x in present]:
    on = [s for s in syms if s[0] >> 12 <= pg <= (s[0] + max(s[1], 1) - 1) >> 12]
    big = sorted(on, key=lambda s: -s[1])[:4]
    print('page %x %s  %s' % (pg, 'TOUCHED' if pg in present else '   -   ', ', '.join('%s %s(%d)' % (s[2], s[3], s[1]) for s in big)))
shutil.rmtree(dd, ignore_errors=True)
