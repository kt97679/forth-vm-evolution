#!/usr/bin/env python3
"""fsys-count.py ID [ID ...] --db FILE [--db FILE] [--levels 4,5] [--works kernel,corpus]
[--words N] - each design built at each fsys level with the engine's profiler:
per workload the dispatches (the profiler's per-address counts, summed), the
system calls (strace -f -c, on the same engine without VMPROF), and the
dispatches spent inside the I/O words (self cost by the converter's symbol
map: READ-LINE, READ, WRITE and every FS- word). Counted, not timed.
Scratch tool (Iteration 214): run in a tree with the batch applied."""
import bisect, collections, json, os, shutil, subprocess, sys
TREE = os.environ.get('TREE', '/tmp/batch43')
HERE = os.path.join(TREE, 'lab', 'evolve')
args = sys.argv[1:]
def opt(name, default=None, many=False):
    vals = []
    while name in args:
        i = args.index(name); vals.append(args[i + 1]); del args[i:i + 2]
    return vals if many else (vals[-1] if vals else default)
dbs = opt('--db', many=True)
levels = [int(x) for x in opt('--levels', '4,5').split(',')]
works = opt('--works', 'kernel,corpus').split(',')
nwords = int(opt('--words', '0')); ndiff = int(opt('--diff', '0'))
if not args or not dbs: sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
recs = {}
for db in dbs:
    for l in open(db):
        l = l.strip()
        if l.startswith('{'):
            try: r = json.loads(l); recs[r['id']] = r
            except ValueError: pass
IO = ('READ-LINE', 'READ', 'WRITE', 'TYPE', 'EMIT', 'SCAN', 'CMOVE', 'FS3', 'FS1', 'FS0')

def count(did, lev):
    g = E.canon(dict(recs[did]['genome'], fsys=lev))
    d = os.path.join(E.EV, 'fsyscount'); shutil.rmtree(d, ignore_errors=True)
    sm = d + '.sym'
    os.environ['SYMMAP'] = sm; E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False; del os.environ['SYMMAP']
    syms = []
    for l in open(sm):
        a, b, n = l.split(None, 2); syms.append((int(a), int(b), n.strip()))
    syms.sort(); starts = [s[0] for s in syms]
    many = collections.Counter(n for _, _, n in syms); seen = collections.Counter(); lab = []
    for a, b, n in syms:                 # a name defined again: name@1 the oldest (lowest address), @2 the next
        seen[n] += 1; lab.append(n if many[n] == 1 else '%s@%d' % (n, seen[n]))
    syms = [(a, b, l) for (a, b, _), l in zip(syms, lab)]
    pw = E.private_work(d); out = {}
    for w in works:
        pf = os.path.join(d, 'prof-' + w)
        r = E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=20, env=dict(os.environ, VMPROF=pf))
        ipc = collections.Counter()
        for line in open(pf):
            f = line.split()
            if f[0] == 'I': ipc[int(f[1])] += int(f[2])
        per = collections.Counter()
        for a, k in ipc.items():
            i = bisect.bisect_right(starts, a) - 1
            per[syms[i][2] if i >= 0 and syms[i][0] <= a < syms[i][1] else '?'] += k
        st = os.path.join(d, 'strace-' + w)
        subprocess.run(['strace', '-f', '-c', '-o', st, eng, img], cwd=pw, input=E.program(w),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=240)
        calls = collections.Counter()
        for line in open(st):
            f = line.split()
            if len(f) >= 5 and f[0][0].isdigit() and f[-1] != 'total':
                calls[f[-1]] = int(f[3])
        out[w] = (sum(ipc.values()), per, calls, len(r.stdout))
    shutil.rmtree(d, ignore_errors=True)
    return out

for did in args:
    res = {lev: count(did, lev) for lev in levels}
    print('## %s (%s)' % (did, ', '.join('%s=%s' % (k, recs[did]['genome'].get(k)) for k in ('kinput', 'kfast', 'jit', 'escape'))))
    for w in works:
        print('  %s:' % w)
        for lev in levels:
            tot, per, calls, nout = res[lev][w]
            io = sum(k for n, k in per.items() if n.startswith('FS-') or n.split('@')[0] in IO)
            print('    fsys %d: %11s dispatches, I/O words %10s; system calls %6d (read %d, lseek %d, write %d, mmap %d); stdout %d bytes'
                  % (lev, format(tot, ','), format(io, ','), sum(calls.values()), calls['read'], calls['lseek'],
                     calls['write'], calls['mmap'], nout))
        if nwords:
            names = set()
            for lev in levels: names |= {n for n, k in res[lev][w][1].items() if n.startswith('FS-') or n.split('@')[0] in IO}
            for n in sorted(names, key=lambda n: -max(res[lev][w][1][n] for lev in levels))[:nwords]:
                print('      %-14s ' % n + '  '.join('%10s' % format(res[lev][w][1][n], ',') for lev in levels))
        if ndiff and len(levels) > 1:
            a, b = res[levels[0]][w][1], res[levels[1]][w][1]
            print('      the most changed words, fsys %d -> %d:' % (levels[0], levels[1]))
            for n in sorted(set(a) | set(b), key=lambda n: -abs(b[n] - a[n]))[:ndiff]:
                print('      %-16s %10s %10s %+11s' % (n, format(a[n], ','), format(b[n], ','), format(b[n] - a[n], ',')))
