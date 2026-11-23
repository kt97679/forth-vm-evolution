#!/usr/bin/env python3
"""results/drafts/jit-guard-739.py MASTER SLIM [NAME ...] - the JIT roles' stack gap priced (Iteration 739;
results/drafts/data-layout2-738.txt's finding). On the JIT roles without the guard gene (default small-jit,
fastest-x86-32, fastest-x86-64) three variants, each built by its tree's lab (evolve.build, a fresh process per tree):
  base   MASTER, the role as designs/NAME/record.json has it;
  guard  MASTER, the same genome with guard=1 (the gene: two guard pages, the handler's own stack, unchecked pushes);
  slim   SLIM, a tree whose engine gives X_JIT designs without the gene one unreadable page at the data stack's floor
         and the handler on its own stack (the interpreter's checks kept, its bound a page higher).
For each: the shipped engine's bytes; every selection workload's output hashed (a FAULT if it differs from base's);
the record's rss (cputime's MINFLT, the largest median over the workloads but apps, KB); corpus and kernel
instructions (cachegrind; not at 4-byte cells); and the stacks' traps - status and stderr's last line for a runaway
push (in a loop and by recursion), native recursion, both underflows and 25 FIB. HK_W4=1: 4-byte cells. RUNS (7).
Run as the build user, python3 -B."""
import hashlib, json, os, re, statistics, subprocess, sys
TRAPS = [('push loop', ': OVF BEGIN 1 0 UNTIL ; OVF'), ('push recursion', ': P2 1 RECURSE DROP ; P2'),
         ('native recursion', ': R3 RECURSE 1 ; R3'), ('data underflow', ': UND BEGIN DROP 0 UNTIL ; UND'),
         ('return underflow', ': UNR BEGIN R> DROP 0 UNTIL ; UNR'),
         ('25 FIB', ': FIB DUP 2 < IF EXIT THEN DUP 1- RECURSE SWAP 2 - RECURSE + ; 25 FIB . CR')]
if len(sys.argv) > 1 and sys.argv[1] == '--one':          # the child: one tree's variants, as JSON on stdout
    ROOT, variants, names = sys.argv[2], sys.argv[3].split(','), sys.argv[4:]
    sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); sys.argv = ['x']
    import evolve as E
    W4 = bool(os.environ.get('HK_W4'))
    if W4: os.environ.update(E.W4_ENV)
    E.setup()
    RUNS = int(os.environ.get('RUNS', '7')); env = {'PATH': '/usr/bin:/bin'}
    def flt(eng, img, pw, inp):
        p = subprocess.run([E.CPUT, eng, img], input=inp, capture_output=True, cwd=pw, env=env, timeout=600)
        m = re.findall(rb'^MINFLT (\d+)', p.stderr, re.M)
        return int(m[-1]) if m else -1, p.stdout
    def ir(eng, img, pw, inp):
        p = subprocess.run(['valgrind', '--tool=cachegrind', '--cache-sim=no', '--cachegrind-out-file=/dev/null', eng, img],
                           input=inp, cwd=pw, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=3600)
        n = re.findall(rb'I\s+refs:\s+([\d,]+)', p.stderr)
        return int(n[-1].replace(b',', b'')) if n else 0
    def trap(eng, img, pw, src):
        try: p = subprocess.run([eng, img], input=(src + '\n').encode(), capture_output=True, cwd=pw, env=env, timeout=20)
        except subprocess.TimeoutExpired: return 'timeout', ''
        last = [l for l in (p.stdout + p.stderr).decode('latin-1').replace('\r', '').split('\n') if l.strip() and not l.startswith('Welcome')]
        return p.returncode, last[-1][:60] if last else ''
    out = {}
    for v in variants:
        for n in names:
            g = dict(json.load(open(os.path.join(ROOT, 'designs', n, 'record.json')))['genome'])
            if v == 'guard': g['guard'] = 1
            d = os.path.join(E.EV, 'jg-%s-%s%s' % (v, n, '-w4' if W4 else ''))
            eng, img = E.build(E.canon(g), d); pw = E.private_work(d)
            r = {'engine': os.path.getsize(eng), 'w': {}, 'ir': {}, 'traps': {}}
            for w in E.WORK_SEL:
                vv = [flt(eng, img, pw, E.program(w)) for _ in range(RUNS if w != 'apps' else 3)]
                r['w'][w] = (statistics.median(x[0] for x in vv), hashlib.sha1(vv[0][1]).hexdigest())
            r['rss'] = max(r['w'][w][0] for w in E.WORK_SEL if w != 'apps') * 4
            if not W4:
                for w in ('corpus', 'kernel'): r['ir'][w] = ir(eng, img, pw, E.program(w))
            for k, src in TRAPS: r['traps'][k] = trap(eng, img, pw, src)
            out['%s %s' % (v, n)] = r
            print('# %s %s done' % (v, n), file=sys.stderr, flush=True)
    print(json.dumps(out)); sys.exit(0)

MASTER, SLIM = sys.argv[1], sys.argv[2]
names = sys.argv[3:] or ['small-jit', 'fastest-x86-32', 'fastest-x86-64']
R = {}
for t, vs in ((MASTER, 'base,guard'), (SLIM, 'slim')):
    p = subprocess.run([sys.executable, '-B', os.path.abspath(__file__), '--one', t, vs] + names, cwd=t, capture_output=True, text=True)
    if p.returncode: sys.exit('%s: %s' % (t, p.stderr[-2000:]))
    R.update(json.loads(p.stdout.strip().split('\n')[-1]))
W4 = bool(os.environ.get('HK_W4'))
print('# The JIT roles\' stack gap priced (results/drafts/jit-guard-739.py): %s cells, medians of %s runs\n'
      % ('4-byte' if W4 else '8-byte', os.environ.get('RUNS', '7')))
print('| role | variant | engine B | outputs | rss KB | corpus instr. / base | kernel instr. / base |')
print('|---|---|---:|---|---:|---:|---:|')
bad = 0
for n in names:
    b = R['base ' + n]
    for v in ('base', 'guard', 'slim'):
        x = R['%s %s' % (v, n)]
        same = all(x['w'][w][1] == b['w'][w][1] for w in b['w'])
        bad += not same
        rel = lambda w: '%.4f' % (x['ir'][w] / b['ir'][w]) if x['ir'].get(w) and b['ir'].get(w) else '-'
        print('| %s | %s | %d (%+d) | %s | %d | %s | %s |' % (n, v, x['engine'], x['engine'] - b['engine'],
              'same' if same else 'DIFFER', x['rss'], rel('corpus'), rel('kernel')))
print('\n| role | variant | ' + ' | '.join(k for k, _ in TRAPS) + ' |')
print('|---|---|' + '---|' * len(TRAPS))
for n in names:
    for v in ('base', 'guard', 'slim'):
        x = R['%s %s' % (v, n)]
        print('| %s | %s | %s |' % (n, v, ' | '.join('%s %s' % (x['traps'][k][0], x['traps'][k][1].replace('relf: ', '').replace('|', '/'))
                                                     for k, _ in TRAPS)))
print('\njit-guard: %s' % ('every output the same as base' if not bad else 'FAILED - %d variants differ' % bad))
sys.exit(1 if bad else 0)
