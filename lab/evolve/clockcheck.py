#!/usr/bin/env python3
"""clockcheck.py [--sample N] [--rounds R] [--workers K] DB [DB ...] - is the fast end's offset the clock? (Iteration 527)

The fast end comes out ~7% slower measured after a run than in it (rule 3). Ruled out: noise and lucky readings (513),
co-runners that only benchmark (520: alone and beside three, 1.2% apart), a rebuild (521: byte-identical). Five answers
from other models (results/drafts/ask-cpu-state-answers-526.md) put the clock first: under the run's compiles the cores
hold a lower sustained clock; alone one boosts; s6, the more compute-bound, gains more from a higher clock than a design
whose time is partly stalls - so the ratio rises when quiet. Their test, and this: the N fastest of the first database's
front, each measured as the run measures it (R rounds, paired with s6, alternating), in six blocks - alone, beside K
benchmark co-runners, beside K compile co-runners (building front designs, as the run's workers do), then the same in
reverse - recording for every run its CPU time and, when the counters are readable, its cycles, and the measured core's
reported clock before each block. If the cycle ratio holds where the time ratio moves, the offset is the clock.

Cycles need kernel.perf_event_paranoid at most 2: in next-run.sh's chain, root's lab/evolve/perf-hold.py holds it while
this measures, as for counters.py (Iteration 545 - sudo asks once, at the chain's start); otherwise the time alone is
recorded and the report says so. --self-test: the hold's handshake, against a stand-in for perf-hold.py, and the split's parse. From Iteration 554 a second table: the cost a design and s6 both pay outside their user-space work, from the time and the user-space cycles, beside getrusage's system time (cputime prints its two parts). stdout: the
report; stderr: progress.
"""
import contextlib, json, math, os, random, re, shutil, statistics, subprocess, sys, time

@contextlib.contextmanager
def held(start, done, C):
    # Iteration 545: the chain's hold (counters.PerfHold, as counters.py and missmap.py take it) while this measures;
    # none, or one that fails, and the clock test runs on the time alone
    h = None
    if start and start != 'none':
        try: h = C.PerfHold(start, done).__enter__()
        except SystemExit: print('clockcheck: perf-hold.py did not set kernel.perf_event_paranoid (runs/perf-hold.log) - the time alone', file=sys.stderr)
    try: yield h
    finally:
        if h: h.__exit__()

def split(err):
    """cputime's user and system parts of a run, ns (Iteration 554); None, None from an older cputime."""
    u = re.search(rb'^USERNS (\d+)', err, re.M); s = re.search(rb'^SYSNS (\d+)', err, re.M)
    return (int(u.group(1)), int(s.group(1))) if u and s else (None, None)
def both_pay(x):
    """The time a workload's run costs a design and s6 alike outside their user-space work, us (Iteration 554): with the
    time ratio t and the user-space cycle ratio c at one clock, s6's time x (t - c)/(1 - c). None without cycles."""
    if not (x.get('dc') and x.get('sc')): return None
    t, c = x['dt'] / x['st'], x['dc'] / x['sc']
    return x['st'] * (t - c) / (1 - c) / 1e3 if c < 0.9 else None
if sys.argv[1:] == ['--self-test']:
    import tempfile, threading
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import counters as C
    t = tempfile.mkdtemp(); C.PARANOID = os.path.join(t, 'paranoid'); open(C.PARANOID, 'w').write('4\n')
    st, dn = os.path.join(t, 'hold.start'), os.path.join(t, 'hold.done')
    def root():                             # perf-hold.py's half: 2 once START names a pid, the old value back at DONE
        while not os.path.exists(st): time.sleep(0.01)
        open(C.PARANOID, 'w').write('2\n')
        while not os.path.exists(dn): time.sleep(0.01)
        open(C.PARANOID, 'w').write('4\n')
    th = threading.Thread(target=root, daemon=True); th.start()
    with held(st, dn, C): inside = open(C.PARANOID).read().strip()
    th.join(5); ok1 = inside == '2' and open(C.PARANOID).read().strip() == '4' and open(st).read().strip() == str(os.getpid())
    os.remove(st); os.remove(dn)
    C.time = type('T', (), {'sleep': staticmethod(lambda s: None)})     # no holder: PerfHold gives up at once
    with held(st, dn, C) as h2: ok2 = h2 is None and open(C.PARANOID).read().strip() == '4'
    with held('none', 'none', C) as h3: ok3 = h3 is None and not os.path.exists(os.path.join(t, 'none'))
    shutil.rmtree(t)
    ok4 = (split(b'CPUNS 9\nUSERNS 7\nSYSNS 2\n') == (7, 2) and split(b'CPUNS 9\n') == (None, None) and
           abs(both_pay(dict(dt=1.47e6, st=1e7, dc=116, sc=1000)) - 350.68) < 0.1 and both_pay(dict(dt=1, st=2, dc=None, sc=None)) is None)
    print('clockcheck --self-test: the hold %s (2 while it measures, 4 after); no holder %s, none %s (the time alone); the split %s'
          % tuple('ok' if v else 'FAIL' for v in (ok1, ok2, ok3, ok4)))
    sys.exit(0 if ok1 and ok2 and ok3 and ok4 else 1)
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; opt = {'--sample': '8', '--rounds': '3', '--workers': '3'}
for k in list(opt):
    if k in args: i = args.index(k); opt[k] = args[i + 1]; del args[i:i + 2]
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
N, ROUNDS, K = int(opt['--sample']), int(opt['--rounds']), int(opt['--workers'])
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
def say(*a): print(*a, file=sys.stderr, flush=True)

R = {}
for l in open(args[0]):
    try: r = json.loads(l)
    except ValueError: continue
    if r.get('id'): R[r['id']] = r
ok = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and r.get('total') and r.get('rss')]
front = sorted(E.first_front(ok, R), key=lambda i: R[i]['speed'])
pick = front[:N]
try: paranoid = int(open('/proc/sys/kernel/perf_event_paranoid').read())
except (OSError, ValueError): paranoid = None
say('clockcheck.py: %d designs; %d co-runners; %d rounds; perf_event_paranoid %s' % (len(pick), K, ROUNDS, paranoid))

LAST = [None]; orig_sh = E.sh
def sh_keep(argv, *a, **k):
    r = orig_sh(argv, *a, **k); LAST[0] = r; return r
E.sh = sh_keep
def one(e, i, p, w):
    t = E.run_metric(e, i, p, w)        # the run's own metric (CPU time unless EVOLVE_METRIC=cycles)
    err = LAST[0].stderr if LAST[0] is not None else b''
    ns = re.search(rb'^CPUNS (\d+)', err, re.M); cy = re.search(rb'^CYCLES (\d+)', err, re.M)
    return (int(ns.group(1)) if ns else t), (int(cy.group(1)) if cy else None), *split(err)
def paired(eng, img, pw):
    d_t, d_c, s_t, s_c = {}, {}, {}, {}
    d_u, d_s, s_u, s_s = {}, {}, {}, {}         # Iteration 554: user and system apart
    for r_ in range(ROUNDS):
        for w in E.WORK_SEL:
            pair = [((eng, img, pw), d_t, d_c, d_u, d_s), (E.REF, s_t, s_c, s_u, s_s)]
            for (e, i, p), st, sc, su, ss in (pair if r_ % 2 == 0 else pair[::-1]):
                t, c, u, s = one(e, i, p, w); st.setdefault(w, []).append(t)
                if c: sc.setdefault(w, []).append(c)
                if u is not None: su.setdefault(w, []).append(u); ss.setdefault(w, []).append(s)
    def ratio(a, b):
        ws = [w for w in E.WORK_SEL if w in a and w in b]
        if len(ws) < len(E.WORK_SEL): return None
        return math.exp(sum(math.log(statistics.median(a[w]) / statistics.median(b[w])) for w in ws) / len(ws))
    mean = lambda x: sum(x) / len(x)        # Iteration 554: each workload's medians - time and user-space cycles, design and
    sp = {w: dict(dt=statistics.median(d_t[w]), st=statistics.median(s_t[w]),       # s6 - and getrusage's system part, sampled
                  dc=statistics.median(d_c[w]) if w in d_c else None, sc=statistics.median(s_c[w]) if w in s_c else None,  # at the
                  ds=mean(d_s[w]) if w in d_s else None, ss=mean(s_s[w]) if w in s_s else None)  # tick: a mean, not a median
          for w in E.WORK_SEL if w in d_t and w in s_t}
    return ratio(d_t, s_t), ratio(d_c, s_c), sp

cpus = sorted(os.sched_getaffinity(0)); mine = int(E.PIN[-1]) if E.PIN else None
def sib(c):
    try: return {int(x) for x in open('/sys/devices/system/cpu/cpu%d/topology/thread_siblings_list' % c).read().replace('-', ',').split(',') if x.strip()}
    except (OSError, ValueError): return {c}
others = [c for c in cpus if mine is None or c not in sib(mine)]
def mhz():
    c = mine if mine is not None else 0
    try:
        for blk in open('/proc/cpuinfo').read().split('\n\n'):
            if re.search(r'^processor\s*:\s*%d$' % c, blk, re.M):
                m = re.search(r'^cpu MHz\s*:\s*([\d.]+)', blk, re.M); return float(m.group(1)) if m else None
    except OSError: return None
prog = os.path.join(E.EV, 'clockcheck-prog'); os.makedirs(prog, exist_ok=True)
for w in E.WORK_SEL: open(os.path.join(prog, w + '.fth'), 'wb').write(E.program(w, single=True))
bench = os.path.join(prog, 'bench.sh')
open(bench, 'w').write('while true; do for w in %s; do "$1" "$2" < %s/$w.fth > /dev/null 2>&1; done; done\n' % (' '.join(E.WORK_SEL), prog))
builder = os.path.join(prog, 'build.py')
open(builder, 'w').write('''import json, os, random, shutil, sys
sys.argv = ['x']; sys.path.insert(0, %r); import evolve as E
gs = json.load(open(%r)); n = int(os.environ.get('CC_N', '0')); rnd = random.Random(n)
while True:
    d = os.path.join(E.EV, 'clockcheck-cc%%d' %% n); shutil.rmtree(d, ignore_errors=True)
    try: E.build(E.canon(rnd.choice(gs)), d)
    except Exception: pass
''' % (HERE, os.path.join(prog, 'genomes.json')))
json.dump([R[i]['genome'] for i in front[:40]], open(os.path.join(prog, 'genomes.json'), 'w'))
def start(kind):
    hs = []
    for n in range(K):
        pin = ['taskset', '-c', str(others[n % len(others)])] if others and shutil.which('taskset') else []
        if kind == 'bench': cmd = pin + ['sh', bench, E.REF[0], E.REF[1]]
        else: cmd = pin + [sys.executable, builder]
        hs.append(subprocess.Popen(cmd, cwd=E.REF[2], env=dict(os.environ, CC_N=str(n)), stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, start_new_session=True))
    time.sleep(3.0)
    return hs
def stop(hs):
    for h in hs:
        try: os.killpg(h.pid, 9)
        except OSError: pass
    for h in hs: h.wait()

ORDER = ['alone', 'bench', 'compile', 'compile', 'bench', 'alone']
rows = []; SPLIT = {}                       # SPLIT: a condition's blocks, each {workload: paired()'s medians and means}
import counters as C
HOLD = contextlib.ExitStack(); HOLD.enter_context(held(os.environ.get('PERF_HOLD_START'), os.environ.get('PERF_HOLD_DONE'), C))
for i in pick:
    d = os.path.join(E.EV, 'clockcheck-' + i); shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(E.canon(R[i]['genome']), d); pw = E.private_work(d)
        got = {c: [] for c in ('alone', 'bench', 'compile')}
        for c in ORDER:
            hs = start(c) if c != 'alone' else []
            f = mhz(); tr, cr, sp = paired(eng, img, pw); stop(hs)
            got[c].append((tr, cr, f)); SPLIT.setdefault(c, []).append(sp)
        res = {}
        for c, v in got.items():
            tr = [x[0] for x in v if x[0]]; cr = [x[1] for x in v if x[1]]; fs = [x[2] for x in v if x[2]]
            res[c] = (math.sqrt(tr[0] * tr[1]) if len(tr) == 2 else None, math.sqrt(cr[0] * cr[1]) if len(cr) == 2 else None,
                      statistics.mean(fs) if fs else None)
        rows.append((i, R[i]['speed'], res))
        say('  %s in the run %.4f | ' % (i, R[i]['speed']) + ' | '.join('%s time %s cycles %s %sMHz' % (c, '%.4f' % res[c][0] if res[c][0] else '-',
            '%.4f' % res[c][1] if res[c][1] else '-', '%.0f' % res[c][2] if res[c][2] else '-') for c in ('alone', 'bench', 'compile')))
    except Exception as x:
        say('  %s: %s' % (i, str(x)[:120]))
    shutil.rmtree(d, ignore_errors=True)
HOLD.close()                                # the setting back now (perf-hold.py), before the report
shutil.rmtree(prog, ignore_errors=True)
for n in range(K): shutil.rmtree(os.path.join(E.EV, 'clockcheck-cc%d' % n), ignore_errors=True)

def med(xs):
    xs = sorted(x for x in xs if x)
    return statistics.median(xs) if xs else None
def f3(x): return '%.3f' % x if x else '-'
print('# The clock test: the fast end alone, beside benchmarks, beside compiles (lab/evolve/clockcheck.py)\n')
print('The %d fastest of %s\'s front, each measured as the run measures it (%d rounds, paired with hand-made s6), in six '
      'blocks - alone, beside %d benchmark co-runners, beside %d compile co-runners, and back - each condition the geometric '
      'mean of its two blocks. A ratio is design/s6, lower faster; cycles counted in user space when the counters are '
      'readable (perf_event_paranoid here: %s). MHz: the measured core\'s reported clock before each block.\n' % (len(rows), args[0], ROUNDS, K, K, paranoid))
print('| design | in the run | alone: time | cycles | MHz | benchmarks: time | cycles | MHz | compiles: time | cycles | MHz |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for i, s, res in rows:
    print('| %s | %.4f | ' % (i, s) + ' | '.join('%s | %s | %s' % (f3(res[c][0]), f3(res[c][1]), '%.0f' % res[c][2] if res[c][2] else '-') for c in ('alone', 'bench', 'compile')) + ' |')
if rows:
    m = {c: (med([res[c][0] / s for _, s, res in rows if res[c][0]]), med([res[c][1] for _, _, res in rows]) and
             med([res[c][1] / res['alone'][1] for _, _, res in rows if res[c][1] and res['alone'][1]]),
             med([res[c][0] / res['alone'][0] for _, _, res in rows if res[c][0] and res['alone'][0]])) for c in ('alone', 'bench', 'compile')}
    print('\n**Medians** - time against the run: alone %s, beside benchmarks %s, beside compiles %s; time against alone: '
          'benchmarks %s, compiles %s; cycles against alone: benchmarks %s, compiles %s.\n' % (
          f3(m['alone'][0]), f3(m['bench'][0]), f3(m['compile'][0]), f3(m['bench'][2]), f3(m['compile'][2]), f3(m['bench'][1]), f3(m['compile'][1])))
    tc, cc = m['compile'][2], m['compile'][1]
    if tc and abs(tc - 1) >= 0.03 and cc and abs(cc - 1) < abs(tc - 1) / 2:
        print('**Reading**: beside compiles the time ratio moves %+.1f%% and the cycle ratio %+.1f%% - **the clock**: '
              'the run\'s speed is the speed at its load\'s clock.' % (100 * (tc - 1), 100 * (cc - 1)))
    elif tc and abs(tc - 1) >= 0.03:
        print('**Reading**: beside compiles the time ratio moves %+.1f%%%s - contention from the compiles, not only the '
              'clock.' % (100 * (tc - 1), (' and the cycles %+.1f%%' % (100 * (cc - 1))) if cc else ' (no cycles counted)'))
    else:
        print('**Reading**: compiles move the ratio %s - not the cause; the offset lies elsewhere (the moment: a run\'s '
              'hours of load, the machine\'s state after it).' % ('by %+.1f%%' % (100 * (tc - 1)) if tc else 'not measurably'))
if any(SPLIT.values()):                      # Iteration 554: the cost a design and s6 both pay, and where it lies
    W = [w for w in E.WORK_SEL if any(w in sp for v in SPLIT.values() for sp in v)]
    at = lambda c, w: [sp[w] for sp in SPLIT.get(c, []) if w in sp]
    md = lambda xs: statistics.median(xs) if xs else None
    mn = lambda xs: sum(xs) / len(xs) if xs else None
    fu = lambda v: '%.0f' % v if v is not None else '-'
    print('\n**The cost both pay** (Iteration 554 - results/drafts/fast-end-offset-554.md): a workload\'s run costs a design '
          'and s6 alike some time outside their user-space work; with the time ratio t and the user-space cycle ratio c at one '
          'clock it is s6\'s time x (t - c)/(1 - c) - medians over the designs\' blocks, in microseconds (no cycles, no '
          'figure). Seed 75\'s re-measure moved it by about 300 us on bubble and 75 on kernel: a cost that large or larger can '
          'carry the offset, one far smaller cannot. The system time is getrusage\'s split, which the kernel samples at its '
          'tick: means over every run, a coarse check of where the cost lies.\n')
    print('| workload | s6 time, ms | alone: time ratio | cycle ratio | the cost both pay, us | beside compiles: the cost, us | system time, us: s6 | the designs |')
    print('|---|---|---|---|---|---|---|---|')
    for w in W:
        a = at('alone', w); s6 = md([x['st'] for x in a])
        print('| %s | %s | %s | %s | %s | %s | %s | %s |' % (w, '%.1f' % (s6 / 1e6) if s6 else '-', f3(md([x['dt'] / x['st'] for x in a])),
              f3(md([x['dc'] / x['sc'] for x in a if x['dc'] and x['sc']])), fu(md([v for v in map(both_pay, a) if v is not None])),
              fu(md([v for v in map(both_pay, at('compile', w)) if v is not None])), fu(mn([x['ss'] / 1e3 for x in a if x['ss'] is not None])),
              fu(mn([x['ds'] / 1e3 for x in a if x['ds'] is not None]))))
