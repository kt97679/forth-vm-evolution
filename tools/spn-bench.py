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

if len(sys.argv) < 3:
    sys.exit(__doc__)
O = os.path.abspath(sys.argv[1])
OUT = sys.argv[2]
ROUNDS = int(sys.argv[3]) if len(sys.argv) > 3 else 12
START_ROUNDS = int(sys.argv[4]) if len(sys.argv) > 4 else 40
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(O, 'work')
CPUT = os.path.join(O, 'cputime')
PIN = ['taskset', '-c', '0'] if shutil.which('taskset') else []
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
    """-> (cpu ns or None, max rss KB or None, correct?, stdout)"""
    with open(FILES[name], 'rb') as f:
        try:
            p = subprocess.run(PIN + [CPUT, eng, img], stdin=f, cwd=W,
                               capture_output=True, timeout=600)
        except subprocess.TimeoutExpired:
            return None, None, False, b''
    m = re.search(rb'^CPUNS (\d+)', p.stderr, re.M)
    r = re.search(rb'^MAXRSS (\d+)', p.stderr, re.M)
    ok = p.returncode == 0
    wl = wl or name
    if wl == 'kernel':
        ok = ok and open(KIMG, 'rb').read() == KREF
        open(KIMG, 'wb').write(KREF)
    elif wl in MARK:
        ok = ok and MARK[wl] in p.stdout and not ERRS.search(p.stdout)
    return (int(m.group(1)) if m else None), (int(r.group(1)) if r else None), ok, p.stdout

def engines(s):
    out = []
    for suf in [''] + ['-v%d' % i for i in range(1, 10)]:
        e = os.path.join(O, '%s-64%s' % (s, suf))
        if os.access(e, os.X_OK): out.append(e)
    return out
IMG = {s: os.path.join(O, '%s-s64.img' % s) for s in SYSTEMS}
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
        if run(e, IMG[s], wl)[2]: GOOD[wl].append((s, e))
        else: EXCLUDED.append((s, os.path.basename(e), wl))

# ---- timing ----------------------------------------------------------
def measure(wl, rounds):
    best = {}
    for r in range(rounds):
        order = list(GOOD[wl]); random.Random(1000 * r + len(wl)).shuffle(order)
        for s, e in order:
            ns = run(e, IMG[s], wl)[0]
            if ns is not None: best[(s, e)] = min(best.get((s, e), 1 << 62), ns)
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
START = summary(RAW['bye'])
E2E = {}
for wl in WORKLOADS:
    print('%s, %d rounds ...' % (wl, ROUNDS), flush=True)
    RAW[wl] = measure(wl, ROUNDS)
    E2E[wl] = summary(RAW[wl])

# ---- memory and native code (variant 0 only) --------------------------
print('memory ...', flush=True)
RSS = {}
for s in SYSTEMS:
    if not os.path.exists(IMG[s]) or not engines(s): continue
    e = engines(s)[0]
    for wl in ['bye'] + WORKLOADS:
        vals = [run(e, IMG[s], wl)[1] for _ in range(3)]
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
        c = classify(run(e, IMG[s], 'smaps-' + wl, 'x')[3], e)
        if c: SM[(s, wl)] = c
    if s in SPN:
        for wl in ('bye', 'fib', 'parse', 'corpus'):
            # The engine's CR is \r\n: strip the \r before matching a line.
            out = run(e, IMG[s], 'native-' + wl, 'x')[3].decode('latin-1').replace('\r', '')
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
L.append('    cores       %s    pinned to cpu 0: %s' % (sh('nproc'), 'yes' if PIN else 'no (no taskset)'))
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
L.append('    stage          image bytes   start-up ms   variants: min - max')
for s in SYSTEMS:
    if s in START:
        med, lo, hi, n = START[s]
        L.append('    %-12s %12d   %10.2f     %.2f - %.2f' % (s, os.path.getsize(IMG[s]), ms(med), ms(lo), ms(hi)))
L.append('')
L.append('## End to end - CPU time, nothing subtracted')
L.append('')
L.append('Each cell: milliseconds, then the ratio to %s, then - with layout' % BASE)
L.append('variants - half their range as a percentage of the median.')
L.append('')
hdr = '    %-12s' % 'stage' + ''.join('%22s' % w for w in WORKLOADS)
L.append(hdr)
for s in SYSTEMS:
    if not any(s in E2E[w] for w in WORKLOADS): continue
    row = '    %-12s' % s
    for w in WORKLOADS:
        if s in E2E[w] and BASE in E2E[w]:
            med, lo, hi, n = E2E[w][s]
            cell = '%.2f %.3f' % (ms(med), med / E2E[w][BASE][0])
            if n > 1: cell += ' +-%.0f%%' % (50.0 * (hi - lo) / med)
            row += '%22s' % cell
        else:
            row += '%22s' % '-'
    L.append(row)
L.append('')
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
L.append('    workload  engine                 ns')
for wl in ['bye'] + WORKLOADS:
    for (s, e), ns in sorted(RAW[wl].items()):
        L.append('    %-9s %-18s %12d' % (wl if wl != 'bye' else 'start-up', os.path.basename(e), ns))
open(OUT, 'w').write('\n'.join(L) + '\n')
print('wrote %s in %.0f s' % (OUT, time.time() - t0))
