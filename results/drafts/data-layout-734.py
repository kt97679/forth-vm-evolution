#!/usr/bin/env python3
"""results/drafts/data-layout-734.py BASE NEW [NAME ...] - the fixed data layout's step 1 measured (Iteration 734;
engine/data-layout.ld, results/drafts/early-games-713.md). BASE and NEW: two built trees (BASE without the layout);
each role (designs/NAME/record.json, default all ten) built by each tree's lab (evolve.build, a fresh process per tree),
then: the shipped engine's bytes; every selection workload's output hashed (the same in both, or a FAULT); its faults
(cputime's MINFLT - the lab's memory reading, KB = pages * 4), medians of RUNS (default 7); the record's rss as the lab
takes it (the largest over the selection's workloads but apps); a start-up's pages (BYE: faults, and the data and BSS
pages present, /proc/PID/pagemap); the corpus's instructions (cachegrind; 0 where it cannot run). HK_W4=1: 4-byte
cells. Prints one table and the differences. Run as the build user, python3 -B, from anywhere."""
import json, os, re, statistics, struct, subprocess, sys, time
if len(sys.argv) > 1 and sys.argv[1] == '--one':          # the child: one tree's numbers, as JSON on stdout
    ROOT, names = sys.argv[2], sys.argv[3:]
    sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); sys.argv = ['x']
    import evolve as E
    if os.environ.get('HK_W4'): os.environ.update(E.W4_ENV)
    E.setup()
    RUNS = int(os.environ.get('RUNS', '7')); env = {'PATH': '/usr/bin:/bin'}
    W = [w for w in E.WORK_SEL]
    def flt(eng, img, pw, inp):
        p = subprocess.run([E.CPUT, eng, img], input=inp, capture_output=True, cwd=pw, env=env, timeout=600)
        m = re.findall(rb'^MINFLT (\d+)', p.stderr, re.M)
        return int(m[-1]) if m else -1, p.stdout
    def pages(eng, img, pw):
        nm = subprocess.run(['nm', '-S', '-n', eng + '.full'], capture_output=True, text=True).stdout
        syms = [(int(f[0], 16), int(f[1], 16)) for f in (l.split() for l in nm.split('\n')) if len(f) == 4 and f[2] in 'bBdD']
        if not syms: return -1, -1
        lo, hi = min(a for a, s in syms) >> 12, max(a + s - 1 for a, s in syms) >> 12
        p = subprocess.Popen([eng, img], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=pw, env=env)
        time.sleep(1.0); present = 0
        try:
            with open('/proc/%d/pagemap' % p.pid, 'rb') as pm:
                for pg in range(lo, hi + 1):
                    pm.seek(pg * 8); v = struct.unpack('<Q', pm.read(8))[0]
                    present += bool(v >> 63 or (v >> 62) & 1)
        finally:
            p.stdin.close(); p.wait()
        return present, hi - lo + 1
    def ir(eng, img, pw, inp):
        p = subprocess.run(['valgrind', '--tool=cachegrind', '--cache-sim=no', '--cachegrind-out-file=/dev/null', eng, img],
                           input=inp, cwd=pw, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=3600)
        n = re.findall(rb'I\s+refs:\s+([\d,]+)', p.stderr)
        return int(n[-1].replace(b',', b'')) if n else 0
    out = {}
    for n in names:
        g = json.load(open(os.path.join(ROOT, 'designs', n, 'record.json')))['genome']
        d = os.path.join(E.EV, 'dlay-%s%s' % (n, '-w4' if os.environ.get('HK_W4') else ''))
        eng, img = E.build(E.canon(g), d); pw = E.private_work(d)
        r = {'engine': os.path.getsize(eng), 'w': {}}
        for w in ['BYE'] + W:
            inp = b'BYE\n' if w == 'BYE' else E.program(w)
            v = [flt(eng, img, pw, inp) for _ in range(RUNS if w != 'apps' else 3)]
            r['w'][w] = (statistics.median(x[0] for x in v), min(x[0] for x in v), max(x[0] for x in v),
                         __import__('hashlib').sha1(v[0][1]).hexdigest())
        r['rss'] = max(r['w'][w][0] for w in W if w != 'apps') * 4
        r['pages'] = pages(eng, img, pw)
        r['ir'] = ir(eng, img, pw, E.program('corpus'))
        out[n] = r
        print('# %s done' % n, file=sys.stderr, flush=True)
    print(json.dumps(out)); sys.exit(0)

BASE, NEW = sys.argv[1], sys.argv[2]
names = sys.argv[3:] or sorted(x for x in os.listdir(os.path.join(NEW, 'designs')) if os.path.exists(os.path.join(NEW, 'designs', x, 'record.json')))
R = {}
for t in (BASE, NEW):
    p = subprocess.run([sys.executable, '-B', os.path.abspath(__file__), '--one', t] + names, cwd=t, capture_output=True, text=True)
    if p.returncode: sys.exit('%s: %s' % (t, p.stderr[-2000:]))
    R[t] = json.loads(p.stdout.strip().split('\n')[-1])
a, b = R[BASE], R[NEW]
print('# The fixed data layout, step 1 (results/drafts/data-layout-734.py): %s against %s, %s cells, medians of %s runs\n'
      % (NEW, BASE, '4-byte' if os.environ.get('HK_W4') else '8-byte', os.environ.get('RUNS', '7')))
print('| role | engine B | outputs | start-up faults | start-up data+BSS pages present | rss KB (the record\'s reading) | the workloads\' faults, new - base | corpus instructions new / base |')
print('|---|---:|---|---:|---:|---:|---|---:|')
bad = 0
for n in names:
    x, y = a[n], b[n]
    same = all(x['w'][w][3] == y['w'][w][3] for w in x['w'] if w != 'BYE')
    bad += not same
    dw = ', '.join('%s %+g' % (w, y['w'][w][0] - x['w'][w][0]) for w in x['w'] if w != 'BYE')
    print('| %s | %d / %d | %s | %g -> %g | %d -> %d (of %d, %d) | %d -> %d | %s | %s |' % (
        n, x['engine'], y['engine'], 'same' if same else 'DIFFER', x['w']['BYE'][0], y['w']['BYE'][0],
        x['pages'][0], y['pages'][0], x['pages'][1], y['pages'][1], x['rss'], y['rss'], dw,
        '%.4f' % (y['ir'] / x['ir']) if x['ir'] and y['ir'] else '-'))
print('\ndata-layout: %s' % ('every output the same' if not bad else 'FAILED - %d roles differ' % bad))
sys.exit(1 if bad else 0)
