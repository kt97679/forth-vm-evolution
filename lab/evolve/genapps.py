#!/usr/bin/env python3
"""lab/evolve/genapps.py [--rounds R] [--sizes] [--cells 8|4] [--systems A,B] [--apps A,B] [--out FILE] - generic applications
on the ten designs and on outside Forths (Iteration 674: step 1 after relf's report - measure application code
generically, relf's shell left out of it).

The lab scores a design's size as its engine and its 9 KB kernel image, and its speed on workloads whose hot code is
mostly the kernel's or a few lines long; an application compiled at run time - most of any real image - is never
scored. This measures it, on seven generic programs: the lab's own sim16, gc16, scan and evo (the selection's apps),
wordfreq and minif (held out), and Ertl's brainless (held out; a chess program, 128 KB of source). Each runs on:
s6 (the lab's hand-made top stage), the ten designs of designs/ (their Makefiles' engines, image.img), relf's CV8 at
vendor/relf/UPSTREAM's commit (relf64, cc -O2 as relf builds it, and relfasm64, relf's assembler engine) on relf's
own kernel64.img, and gforth-fast (0.7.3 here). With --cells 4: s6, the designs' forth32 and image32.img, relf32.

Per program and system:
  code    the bytes the program's load adds to the dictionary, less its data - code, names and headers: HERE's
          advance over the load, less what the program's own ALLOT , and C, laid (counted by a second load with
          those three redefined, through their old xts - relf's colon definitions see themselves)
  data    those ALLOT , and C, bytes (the same on every system with the same cell width: a check)
  load    CPU time of the load (prelude, then the program compiled), the median of R rounds
  run     CPU time of the program's benchmark: the median of the full runs less the median of the loads
  start   CPU time of BYE alone (20 runs, the median)
The output of every full run is checked against the program's known result. All runs are pinned to one CPU
(taskset -c 1), each the child's user and system time (getrusage); systems interleaved, their order rotated each
round. The OWN programs need no prelude anywhere; brainless loads after the lab's appbench prelude (extend.4,
coreext.4 and stubs; its source folded to upper case, as appbench.py does) on the lab's systems, after
lab/evolve/genapps/relf-prelude.fth (relf's own extend.4, then the dozen words its kernel lacks, in Forth) on relf,
and as written on gforth. Writes FILE (default build/genapps/results-CELLS.json); genapps-report.py tabulates it.
"""
import argparse, json, os, re, resource, shutil, statistics, subprocess, sys, tempfile, time
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
sys.path.insert(0, os.path.join(HERE_, 'appbench')); from fold import fold
sys.path.insert(0, HERE_); import appsize    # Iteration 677: the size count, shared with evolve.py
DESIGNS = ['smallest', 'least-memory', 'portable-small', 'portable-knee', 'portable-arm', 'portable-fastest',
           'best-all-round', 'small-jit', 'fastest-x86-64', 'fastest-x86-32']
# name: (files, benchmark call, the result's line) - the calls about 2/5 of appbench.py's (about a second on the
# knee); a result must be the same on every system (s6's, the first)
APPS = {'sim16': ('sim16.fth', '25 BENCH', r'SIM16 SIEVE \d+ FIB \d+ STEPS \d+'),
        'gc16': ('gc16.fth', '20000 BENCH', r'GC16 GCS \d+ FREED \d+ CHECK \d+'),
        'scan': ('scan.fth', '250 BENCH', r'SCAN NFA \d+ DFA \d+ IDENT \d+ NUMBER \d+ SPACE \d+ ERRS \d+ CHECK \d+'),
        'evo': ('evo.fth', '1200 BENCH', r'EVO BEST \d+ AT \d+ CHECK \d+'),
        'wordfreq': ('wordfreq.fth', '60 BENCH', r'WORDFREQ WORDS \d+ DISTINCT \d+ TOP \d+ CHECK \d+'),
        'minif': ('minif.fth', '2500 BENCH', r'MINIF CHECK \d+ ERRS \d+ DEFS \d+'),
        'brainless': ('benchmark.fs', 'BENCHMARK', r'\d+ nodes .* \d+ evals'),   # 110023 and 163278 at 8-byte cells
        'shellmix': ('shellmix.fth', '10000 SHELLMIX', r'10000 50005000 \d+ 80000')}   # 685: relf 953's, relfsh's mix (held out)
ap = argparse.ArgumentParser(usage=__doc__.split('\n')[0])
ap.add_argument('--rounds', type=int, default=5); ap.add_argument('--cells', type=int, default=8, choices=(8, 4))
ap.add_argument('--sizes', action='store_true');   # 677: the sizes alone (appsize-check.py)
ap.add_argument('--systems', default=''); ap.add_argument('--apps', default=','.join(APPS)); ap.add_argument('--out', default='')
a = ap.parse_args()
B = os.path.join(ROOT, 'build'); W = os.path.join(B, 'genapps', 'work-%d' % a.cells)
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
def sh(cmd, cwd=None, inp=None, timeout=900):
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    p = subprocess.run(['taskset', '-c', '1'] + cmd, cwd=cwd or W, input=inp, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=timeout)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime), p.stdout.decode('latin-1')

# ---- the work directory: the programs (folded for the lab and relf, as written for gforth), the preludes, relf
for f in os.listdir(os.path.join(HERE_, 'apps')):
    if f.endswith('.fth'): shutil.copy(os.path.join(HERE_, 'apps', f), W)
os.makedirs(os.path.join(W, 'gf'))
hexfix = lambda t: re.sub(r'(?<![\w$])\$([0-9A-F]+)\b', lambda m: str(int(m.group(1), 16)), t)
bl = os.path.join(HERE_, 'apps', 'brainless')
for f in os.listdir(bl):
    data = open(os.path.join(bl, f), 'rb').read(); shutil.copy(os.path.join(bl, f), os.path.join(W, 'gf'))
    if re.search(r'\.(fs|f|fth)$', f, re.I): data = hexfix(fold(data.decode('latin-1'))).encode('latin-1')
    open(os.path.join(W, f), 'wb').write(data)
for f in [v[0] for k, v in APPS.items() if k != 'brainless']: shutil.copy(os.path.join(W, f), os.path.join(W, 'gf'))   # 685: the table's
for f in ('extend.4', 'coreext.4'): shutil.copy(os.path.join(ROOT, 'forth', f), W)
shutil.copy(os.path.join(HERE_, 'appbench', 'prelude.fth'), os.path.join(W, 'lab-prelude.fth'))
RT = os.path.join(ROOT, 'vendor', 'relf', 'tree'); RC = open(os.path.join(ROOT, 'vendor', 'relf', 'UPSTREAM')).read()
RCOMMIT = re.search(r'commit\s+(\w{7})', RC).group(1)
shutil.copy(os.path.join(RT, 'forth', 'extend.4'), os.path.join(W, 'relf-extend.4'))
shutil.copy(os.path.join(HERE_, 'genapps', 'relf-prelude.fth'), W)
rtree = os.path.join(W, 'relf-tree'); shutil.copytree(RT, rtree, symlinks=True)
want = ['relf64', 'relfasm64'] if a.cells == 8 else ['relf32']
if not a.systems or [n for n in a.systems.split(',') if n.startswith('relf')]:    # 677: only when asked for
    subprocess.run(['make', '-s'] + want, cwd=rtree, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ---- the systems: name -> (kind, command, engine file, image file)
SYS = {}
if a.cells == 8:
    SYS['s6'] = ('lab', [os.path.join(B, 's6-cv8b-64'), os.path.join(B, 's6-cv8b-s64.img')])
    for d in DESIGNS: SYS[d] = ('lab', [os.path.join(ROOT, 'designs', d, 'forth'), os.path.join(ROOT, 'designs', d, 'image.img')])
    SYS['relf64'] = ('relf', [os.path.join(rtree, 'relf64'), os.path.join(rtree, 'forth', 'kernel64.img')])
    SYS['relfasm64'] = ('relf', [os.path.join(rtree, 'relfasm64'), os.path.join(rtree, 'forth', 'kernel64.img')])
    if shutil.which('gforth-fast'): SYS['gforth-fast'] = ('gforth', [shutil.which('gforth-fast')])
else:
    SYS['s6'] = ('lab', [os.path.join(B, 's6-cv8b-32'), os.path.join(B, 's6-cv8b-s32.img')])
    for d in DESIGNS: SYS[d] = ('lab', [os.path.join(ROOT, 'designs', d, 'forth32'), os.path.join(ROOT, 'designs', d, 'image32.img')])
    SYS['relf32'] = ('relf', [os.path.join(rtree, 'relf32'), os.path.join(rtree, 'forth', 'kernel32.img')])
if a.systems: SYS = {k: v for k, v in SYS.items() if k in a.systems.split(',')}
for k, (kind, cmd) in SYS.items():
    for f in cmd:
        if not os.path.exists(f): sys.exit('genapps: no %s (%s) - build it first' % (f, k))
apps = a.apps.split(',')

# ---- the drivers: one file per system kind, program and mode
def driver(kind, app, mode):
    f, call, _ = APPS[app]
    pre = ''
    if app == 'brainless': pre = {'lab': 'S" lab-prelude.fth" INCLUDED\n', 'relf': 'S" relf-prelude.fth" INCLUDED\n', 'gforth': ''}[kind]
    inc = ('INCLUDE %s\n' % f) if app == 'brainless' else ('S" %s" INCLUDED\n' % f)
    t = pre
    if mode in ('size', 'count'): t = appsize.text(inc, mode, pre)       # Iteration 677: appsize.py's, as evolve.py's
    elif mode == 'load': t += inc + 'BYE\n'
    elif mode == 'full': t += inc + (call.lower() if kind == 'gforth' and app == 'brainless' else call) + ' CR\n' + 'BYE\n'
    name = appsize.driver_name(app, mode, kind)
    d = os.path.join(W, 'gf') if kind == 'gforth' else W
    open(os.path.join(d, name), 'w').write(t)
    return name
def run(sysname, app, mode):
    kind, cmd = SYS[sysname]
    if mode == 'start':
        if kind == 'gforth': return sh(cmd + ['-e', 'bye'])
        return sh(cmd, inp=b'BYE\n')
    name = driver(kind, app, mode)
    if kind == 'gforth': return sh(cmd + [name], cwd=os.path.join(W, 'gf'))
    return sh(cmd, inp=('S" %s" INCLUDED\n' % name).encode())

# ---- sizes (deterministic): HERE's advance with and without the counting words
R = {'cells': a.cells, 'relf': RCOMMIT, 'rounds': a.rounds, 'apps': apps, 'systems': {}, 'when': time.strftime('%Y-%m-%d %H:%M')}
for s, (kind, cmd) in SYS.items():
    e = {'engine': os.path.getsize(cmd[0]), 'image': os.path.getsize(cmd[1]) if len(cmd) > 1 else None, 'apps': {}}
    if kind == 'lab':     # the engine as packed (designs/elf_tight.py), as the lab and relf's report count it
        tmp = os.path.join(W, 'tight')
        if subprocess.run([sys.executable, os.path.join(ROOT, 'designs', 'elf_tight.py'), cmd[0], tmp], stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL).returncode == 0: e['engine_tight'] = os.path.getsize(tmp)
    for app in apps:
        _, o1 = run(s, app, 'size'); _, o2 = run(s, app, 'count')
        v = appsize.parse(o1, o2)
        if not v: sys.exit('genapps: %s on %s: no size\n%s\n%s' % (app, s, o1[-600:], o2[-600:]))
        total, data = v
        e['apps'][app] = {'total': total, 'data': data, 'code': total - data, 'load': [], 'full': []}
    R['systems'][s] = e
    print('genapps: %-16s sizes %s' % (s, ' '.join('%s %d' % (k, v['code']) for k, v in e['apps'].items())), flush=True)

if a.sizes:
    out = a.out or os.path.join(B, 'genapps', 'sizes-%d.json' % a.cells); json.dump(R, open(out, 'w'), indent=1)
    sys.exit(print('genapps: wrote %s' % out))
# ---- times: R rounds, systems interleaved and rotated; every full run's result checked
names = list(SYS); RESULT = {}
for rnd in range(a.rounds):
    order = names[rnd % len(names):] + names[:rnd % len(names)]
    for app in apps:
        for s in order:
            t, o = run(s, app, 'load'); R['systems'][s]['apps'][app]['load'].append(t)
            t, o = run(s, app, 'full'); m = list(re.finditer(APPS[app][2], o))
            if not m: sys.exit('genapps: %s on %s: no result\n%s' % (app, s, o[-800:]))
            got = re.sub(r'\(\d+ Hz\)|\d+ ms', '', m[-1].group(0))   # the last match: brainless's whole run, its own times out
            if RESULT.setdefault(app, got) != got: sys.exit('genapps: %s on %s: %r, not %r' % (app, s, got, RESULT[app]))
            R['systems'][s]['apps'][app]['full'].append(t)
    print('genapps: round %d of %d done' % (rnd + 1, a.rounds), flush=True)
for s in names:
    st = [run(s, None, 'start')[0] for _ in range(20)]
    R['systems'][s]['start'] = statistics.median(st)
    for app in apps:
        v = R['systems'][s]['apps'][app]
        v['load_med'] = statistics.median(v['load']); v['full_med'] = statistics.median(v['full'])
        v['run'] = v['full_med'] - v['load_med']
out = a.out or os.path.join(B, 'genapps', 'results-%d.json' % a.cells)
R['results'] = RESULT
json.dump(R, open(out, 'w'), indent=1)
print('genapps: wrote %s' % out)
