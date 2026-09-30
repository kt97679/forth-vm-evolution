#!/usr/bin/env python3
"""spn-bench.py BUILD-DIR OUT.md [ROUNDS] [START-ROUNDS]

What tools/collect-results.sh does not measure, for the SPN stages and
the stages they are built on:

  image size
  start-up       CPU time to BYE
  end to end     CPU time of each workload, NOTHING subtracted - the stage
                 tables are net of start-up, and for SPN start-up is where
                 the translation happens
  memory         peak resident set; and resident memory by mapping, read
                 by each process from /proc/self/smaps just before it exits
  native code    bytes of native code at the end of each workload

Every runner - a stage's engine and layout variant with its image - is
checked for a correct result on every workload before anything is timed;
a runner that fails is left out and listed. Each round runs every runner
once, in a shuffled order, so drift in the machine lands on all of them
alike; each runner keeps its minimum. With layout variants (LAYOUTS=5 at
build time), a stage's figure is the median over its variants, and the
spread is their range - the per-build bias the project measures that way.
"""
import os, re, sys, random, shutil, statistics, subprocess, tempfile, time
sys.dont_write_bytecode = True          # no tools/__pycache__ in the tree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clockfit                         # CPU time vs cycles: the clock, or the kernel?

if len(sys.argv) < 3:
    sys.exit(__doc__)
O = os.path.abspath(sys.argv[1])
OUT = sys.argv[2]
ROUNDS = int(sys.argv[3]) if len(sys.argv) > 3 else 12
START_ROUNDS = int(sys.argv[4]) if len(sys.argv) > 4 else 40
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(O, 'work')
CPUT = os.path.join(O, 'cputime')
# BENCH_CPU: the core to pin to (tools/bench-laptop.sh picks the quietest).
CPU = os.environ.get('BENCH_CPU') or '0'   # set but empty: 0, not ''
PIN = ['taskset', '-c', CPU] if shutil.which('taskset') else []
SYSTEMS = ['s0-cell', 's5-cv8spec', 's6-cv8b', 's7-spn', 's8-spncv8', 's8-lazy', 's8-full']
SPN = {'s7-spn', 's8-spncv8', 's8-lazy', 's8-full'}
BASE = 's0-cell'
WORKLOADS = ['kernel', 'fib', 'corpus', 'parse']
MARK = {'fib': b'BENCH-DONE', 'parse': b'PARSE-DONE', 'corpus': b'CORPUS-REACHED-END'}
ERRS = re.compile(rb'INCORRECT RESULT: \{|WRONG NUMBER OF RESULTS: \{|Undefined word')

if not os.access(CPUT, os.X_OK):
    sys.exit('no %s - run tools/build-stages.sh first' % CPUT)

# ---- inputs ----------------------------------------------------------
T = tempfile.mkdtemp(prefix='spn-bench-')
def body(path):   # a workload's text without its final BYE
    return re.sub(r'\n\s*BYE\s*$', '\n', open(path, encoding='latin-1').read().rstrip() + '\n')
TEXT = {
    'bye':    'BYE\n',
    'fib':    open(os.path.join(ROOT, 'bench/fib.fth'), encoding='latin-1').read(),
    'parse':  open(os.path.join(ROOT, 'bench/parse.fth'), encoding='latin-1').read(),
    'corpus': open(os.path.join(ROOT, 'tests/corpus/core.fth'), encoding='latin-1').read()
              + '\nS" CORPUS-REACHED-END" TYPE CR\nBYE\n',
    'kernel': 'S" extend.4" INCLUDED\nS" cross.4" INCLUDED\n',
}
SMAPS = ('DECIMAL VARIABLE SMF CREATE SMB 4096 ALLOT\n'
         ': SMAPS S" /proc/self/smaps" R/O OPEN-FILE ABORT" no smaps" SMF !\n'
         '  BEGIN SMB 4096 SMF @ READ-FILE ABORT" read" DUP WHILE SMB SWAP TYPE REPEAT DROP\n'
         '  SMF @ CLOSE-FILE DROP ;\n')
NATIVE = '\nDECIMAL CODE-HERE @ CODE-BASE @ - . #NATIVE @ . CR\nBYE\n'
FILES = {}
def put(name, text):
    p = os.path.join(T, name + '.fth'); open(p, 'w', encoding='latin-1').write(text); FILES[name] = p
for k, v in TEXT.items(): put(k, v)
for k in ('bye', 'corpus'):
    put('smaps-' + k, SMAPS + ('' if k == 'bye' else body(FILES[k])) + '\nSMAPS\nBYE\n')
for k in ('bye', 'fib', 'parse', 'corpus'):
    put('native-' + k, ('' if k == 'bye' else body(FILES[k])) + NATIVE)
KIMG = os.path.join(W, 'kernel.img')
KREF = open(KIMG, 'rb').read()      # a kernel compile must reproduce this

# ---- running one thing -----------------------------------------------
def run(eng, img, name, wl=None):
    """-> (cpu ns or None, max rss KB or None, correct?, stdout,
           cycles or None, instructions or None) - the last two only where
           tools/cputime.c could open the hardware counters"""
    with open(FILES[name], 'rb') as f:
        try:
            p = subprocess.run(PIN + [CPUT, eng, img], stdin=f, cwd=W,
                               capture_output=True, timeout=600)
        except subprocess.TimeoutExpired:
            return None, None, False, b'', None, None
    m = re.search(rb'^CPUNS (\d+)', p.stderr, re.M)
    r = re.search(rb'^MAXRSS (\d+)', p.stderr, re.M)
    c = re.search(rb'^CYCLES (\d+)', p.stderr, re.M)
    i = re.search(rb'^INSTR (\d+)', p.stderr, re.M)
    ok = p.returncode == 0
    wl = wl or name
    if wl == 'kernel':
        ok = ok and open(KIMG, 'rb').read() == KREF
        open(KIMG, 'wb').write(KREF)
    elif wl in MARK:
        ok = ok and MARK[wl] in p.stdout and not ERRS.search(p.stdout)
    num = lambda x: int(x.group(1)) if x else None
    return num(m), num(r), ok, p.stdout, num(c), num(i)

def engines(s):
    out = []
    for suf in [''] + ['-v%d' % i for i in range(1, 10)]:
        e = os.path.join(O, '%s-64%s' % (s, suf))
        if os.access(e, os.X_OK): out.append(e)
    return out
IMG = {s: os.path.join(O, '%s-s64.img' % s) for s in SYSTEMS}
def image(s, e):
    """The image a runner uses: a variant engine's own, if it has one - an
    s8 image records the stencils of the engine it was built with - else
    the stage's."""
    v = os.path.basename(e)[len(s) + 3:]
    own = os.path.join(O, '%s-s64%s.img' % (s, v))
    return own if v and os.path.exists(own) else IMG[s]
RUNNERS = [(s, e) for s in SYSTEMS if os.path.exists(IMG[s]) for e in engines(s)]
if not RUNNERS:
    sys.exit('no stages built in %s' % O)

# ---- correctness first -----------------------------------------------
t0 = time.time()
print('checking %d runners on %d workloads ...' % (len(RUNNERS), len(WORKLOADS) + 1), flush=True)
EXCLUDED = []
GOOD = {}
for wl in ['bye'] + WORKLOADS:
    GOOD[wl] = []
    for s, e in RUNNERS:
        if run(e, image(s, e), wl)[2]: GOOD[wl].append((s, e))
        else: EXCLUDED.append((s, os.path.basename(e), wl))

# ---- timing ----------------------------------------------------------
METRICS = ('cpu', 'cyc', 'ins')        # CPU ns, cycles, instructions
def measure(wl, rounds):
    """-> {metric: {(stage, engine): minimum over the rounds}}"""
    best = {m: {} for m in METRICS}
    for r in range(rounds):
        order = list(GOOD[wl]); random.Random(1000 * r + len(wl)).shuffle(order)
        for s, e in order:
            res = run(e, image(s, e), wl)
            for m, v in zip(METRICS, (res[0], res[4], res[5])):
                if v is not None: best[m][(s, e)] = min(best[m].get((s, e), 1 << 62), v)
    return best
def summary(best):
    out = {}
    for s in SYSTEMS:
        v = [ns for (ss, e), ns in best.items() if ss == s]
        if v: out[s] = (statistics.median(v), min(v), max(v), len(v))
    return out
RAW = {}
print('start-up, %d rounds ...' % START_ROUNDS, flush=True)
RAW['bye'] = measure('bye', START_ROUNDS)
START = summary(RAW['bye']['cpu'])
E2E = {}
for wl in WORKLOADS:
    print('%s, %d rounds ...' % (wl, ROUNDS), flush=True)
    RAW[wl] = measure(wl, ROUNDS)
    E2E[wl] = summary(RAW[wl]['cpu'])
# Cycles and instructions count only if every runner has them - a table
# that mixed runners with and without would compare nothing.
HAVE_CYC = all(RAW[w]['cyc'] and RAW[w]['cyc'].keys() == RAW[w]['cpu'].keys()
               for w in ['bye'] + WORKLOADS)
if HAVE_CYC:
    START_C = summary(RAW['bye']['cyc'])
    E2E_C = {w: summary(RAW[w]['cyc']) for w in WORKLOADS}
    E2E_I = {w: summary(RAW[w]['ins']) for w in WORKLOADS}

# ---- memory and native code (variant 0 only) --------------------------
print('memory ...', flush=True)
RSS = {}
for s in SYSTEMS:
    if not os.path.exists(IMG[s]) or not engines(s): continue
    e = engines(s)[0]
    for wl in ['bye'] + WORKLOADS:
        vals = [run(e, image(s, e), wl)[1] for _ in range(3)]
        vals = [v for v in vals if v]
        if vals: RSS[(s, wl)] = min(vals)
def classify(out, eng):
    cats, cur = {}, None
    for line in out.decode('latin-1').split('\n'):
        m = re.match(r'^([0-9a-f]+)-([0-9a-f]+) (\S+) \S+ \S+ \S+\s*(.*)$', line)
        if m:
            size = (int(m.group(2), 16) - int(m.group(1), 16)) // 1024
            perm, name = m.group(3), m.group(4).strip()
            # The image memory is a static array: 16 MB in the CV8 engines,
            # 1 MB in the cell engine - the one unnamed mapping that large.
            if 'w' in perm and 'x' in perm:                  cur = 'native'
            elif name == '[heap]':                           cur = 'heap'
            elif name == '[stack]':                          cur = 'stack'
            elif name and os.path.basename(name) == os.path.basename(eng): cur = 'engine'
            elif '.so' in name or name.startswith('['):      cur = 'shlibs'
            elif not name and size >= 1000:                  cur = 'image'
            else:                                            cur = 'other'
            continue
        m = re.match(r'^Rss:\s+(\d+) kB', line)
        if m and cur: cats[cur] = cats.get(cur, 0) + int(m.group(1))
    return cats
SM = {}
NAT = {}
for s in SYSTEMS:
    if not os.path.exists(IMG[s]) or not engines(s): continue
    e = engines(s)[0]
    for wl in ('bye', 'corpus'):
        c = classify(run(e, image(s, e), 'smaps-' + wl, 'x')[3], e)
        if c: SM[(s, wl)] = c
    if s in SPN:
        for wl in ('bye', 'fib', 'parse', 'corpus'):
            # The engine's CR is \r\n: strip the \r before matching a line.
            out = run(e, image(s, e), 'native-' + wl, 'x')[3].decode('latin-1').replace('\r', '')
            m = re.findall(r'^(\d+) (\d+) *$', out, re.M)
            if m: NAT[(s, wl)] = (int(m[-1][0]), int(m[-1][1]))
shutil.rmtree(T, ignore_errors=True)

# ---- the report --------------------------------------------------------
def sh(cmd):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()
    except Exception: return ''
def rd(p):
    try: return open(p).read().strip()
    except Exception: return 'n/a'
ms = lambda ns: ns / 1e6
L = []
L.append('# SPN measurements: %s' % (sh("sed -n 's/^model name[ \\t]*: //p' /proc/cpuinfo | head -1") or 'unknown CPU'))
L.append('')
L.append('Generated by tools/spn-bench.py; the stage tables for the same build are')
L.append("tools/collect-results.sh's. Method: its docstring.")
L.append('')
L.append('    date        %s' % time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()))
L.append('    revision    %s' % (sh('cd %s && git describe --always --dirty 2>/dev/null' % ROOT) or 'n/a'))
L.append('    kernel      %s' % sh('uname -srm'))
L.append('    cc          %s' % sh('cc --version | head -1'))
L.append('    cores       %s    pinned to cpu %s' % (sh('nproc'), CPU if PIN else '- (no taskset)'))
# Start-up and memory depend on how the engines were linked: read it from
# the binary rather than trust the environment (ENGINE_RT, engine-rt.sh).
try:
    _dyn = b'ld-linux' in open(os.path.join(O, 's0-cell-64'), 'rb').read(65536)
    L.append('    engines     %s' % ('linked with the C library' if _dyn else
             'without the C library (ENGINE_RT=nolibc, engine/rt-linux-x86_64.c)'))
except OSError:
    pass
L.append('    counters    %s' % ('cycles and instructions (user space)' if HAVE_CYC else
         'unavailable - CPU time only (kernel.perf_event_paranoid %s)'
         % rd('/proc/sys/kernel/perf_event_paranoid')))
L.append('    governor    %s' % rd('/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor'))
L.append('    boost       %s' % rd('/sys/devices/system/cpu/cpufreq/boost'))
ac = sh('cat /sys/class/power_supply/A*/online 2>/dev/null | head -1')
L.append('    on AC       %s' % ({'1': 'yes', '0': 'NO - on battery'}.get(ac, 'unknown')))
L.append('    load        %s' % rd('/proc/loadavg'))
L.append('    rounds      %d end to end, %d start-up; variants per stage: %s' % (
    ROUNDS, START_ROUNDS, ', '.join('%s %d' % (s, len(engines(s))) for s in SYSTEMS if s in dict(RUNNERS))))
L.append('')
if EXCLUDED:
    L.append('**Left out - wrong result on a correctness check:** ' +
             ', '.join('%s (%s)' % (e, wl) for s, e, wl in EXCLUDED))
    L.append('')
L.append('## Image size and start-up')
L.append('')
L.append('    stage          image bytes   start-up ms   variants: min - max' + ('    Mcycles' if HAVE_CYC else ''))
for s in SYSTEMS:
    if s in START:
        med, lo, hi, n = START[s]
        L.append('    %-12s %12d   %10.2f     %.2f - %.2f' % (s, os.path.getsize(IMG[s]), ms(med), ms(lo), ms(hi))
                 + ('%15.3f' % (START_C[s][0] / 1e6) if HAVE_CYC and s in START_C else ''))
L.append('')
def e2e_table(E, unit, fmt='%.2f %.3f'):
    """One row per stage: the median over layout variants in UNIT, the
    ratio to BASE, and - with variants - half their range in percent."""
    L.append('    %-12s' % 'stage' + ''.join('%22s' % w for w in WORKLOADS))
    for s in SYSTEMS:
        if not any(s in E[w] for w in WORKLOADS): continue
        row = '    %-12s' % s
        for w in WORKLOADS:
            if s in E[w] and BASE in E[w]:
                med, lo, hi, n = E[w][s]
                cell = fmt % (unit(med), med / E[w][BASE][0])
                if n > 1: cell += ' +-%.0f%%' % (50.0 * (hi - lo) / med)
                row += '%22s' % cell
            else:
                row += '%22s' % '-'
        L.append(row)
    L.append('')

L.append('## End to end - CPU time, nothing subtracted')
L.append('')
L.append('Each cell: milliseconds, then the ratio to %s, then - with layout' % BASE)
L.append('variants - half their range as a percentage of the median.')
L.append('')
e2e_table(E2E, ms)
if HAVE_CYC:
    L.append('## End to end - cycles, nothing subtracted')
    L.append('')
    L.append('The same runs counted in user-space cycles: millions, then the ratio')
    L.append('to %s. Cycles do not depend on the clock, so boost, throttling and' % BASE)
    L.append('the governor drop out.')
    L.append('')
    e2e_table(E2E_C, lambda c: c / 1e6)
    L.append('## End to end - instructions')
    L.append('')
    L.append('Millions of user-space instructions, then the ratio to %s.' % BASE)
    L.append('Deterministic: the ranges show layout, not noise.')
    L.append('')
    e2e_table(E2E_I, lambda c: c / 1e6, '%.1f %.3f')
    # Why the two differ, and which to believe: tools/clockfit.py.
    L += clockfit.agreement(RAW, SYSTEMS, BASE, WORKLOADS)
    L += clockfit.clock(RAW, SYSTEMS, WORKLOADS)
L.append('## Memory')
L.append('')
L.append('Peak resident set, KB (variant 0, least of three runs):')
L.append('')
L.append('    %-12s' % 'stage' + ''.join('%9s' % w for w in ['bye'] + WORKLOADS))
for s in SYSTEMS:
    if any((s, w) in RSS for w in ['bye'] + WORKLOADS):
        L.append('    %-12s' % s + ''.join('%9s' % RSS.get((s, w), '-') for w in ['bye'] + WORKLOADS))
L.append('')
L.append('Resident KB by mapping at exit, from /proc/self/smaps (shared libraries')
L.append('are mapped read-only and shared between processes):')
L.append('')
cats = ['heap', 'native', 'image', 'engine', 'stack', 'other', 'shlibs']
L.append('image: dictionary, stacks and buffers; shlibs: shared libraries.')
L.append('')
L.append('    %-20s' % 'stage, workload' + ''.join('%9s' % c for c in cats) + '    total')
for (s, wl), c in SM.items():
    L.append('    %-20s' % ('%s %s' % (s, wl)) + ''.join('%9s' % c.get(k, 0) for k in cats) + '%9d' % sum(c.values()))
L.append('')
if NAT:
    L.append('Native code at the end of a workload - bytes, then words native:')
    L.append('')
    for s in SYSTEMS:
        if any((s, w) in NAT for w in ('bye', 'fib', 'parse', 'corpus')):
            L.append('    %-12s' % s + ''.join('%18s' % ('%s %d/%d' % ((w,) + NAT[(s, w)]) if (s, w) in NAT else '-')
                                                   for w in ('bye', 'fib', 'parse', 'corpus')))
    L.append('')
L.append('## Raw minima, ns')
L.append('')
L.append('Each runner\'s minimum; the medians and ranges above come from these.')
L.append('')
L.append('    workload  engine                 ns' + ('         cycles   instructions' if HAVE_CYC else ''))
for wl in ['bye'] + WORKLOADS:
    for (s, e), ns in sorted(RAW[wl]['cpu'].items()):
        extra = ('%15d%15d' % (RAW[wl]['cyc'][(s, e)], RAW[wl]['ins'].get((s, e), 0))
                 if HAVE_CYC else '')
        L.append('    %-9s %-18s %12d' % (wl if wl != 'bye' else 'start-up', os.path.basename(e), ns) + extra)
open(OUT, 'w').write('\n'.join(L) + '\n')
print('wrote %s in %.0f s' % (OUT, time.time() - t0))
