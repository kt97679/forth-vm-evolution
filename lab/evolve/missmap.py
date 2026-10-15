#!/usr/bin/env python3
"""missmap.py [--runs N] [IDS...] [DB.jsonl...] - which handlers mispredict (Iteration 294).

counters.py found the evolved designs losing an estimated 9-24% of their cycles on the
interpreter's workloads, kernel and corpus, to branch misses, s6 1-3%
(results/counters-amd-ryzen-7-pro-8840hs.md). This says where. For each design - s6, and
the newest front's fastest with the JIT, fastest without, smallest, as counters.py picks
them - its engine is built with -g (EVOLVE_CFLAGS; debug information changes no
instruction), perf record samples its user-space branch misses on each workload, and
perf report gives each sample's source line; a line is charged to the handler whose
label (L_x:, or a tail engine's function H_x) comes last before it in that source.
Samples outside the engine's source - the JIT's code - are counted apart. The table: per
design and workload, the handlers with the most misses and their share.

Like counters.py it needs perf, and kernel.perf_event_paranoid at 2 or less: next-run.sh
asks sudo for it before its chain detaches (perf-hold.py), and run in a terminal it asks
itself. Output: markdown on stdout.
"""
import collections, os, re, subprocess, sys
ARGS = sys.argv[1:]                          # counters.py takes sys.argv as it imports
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ['EVOLVE_CFLAGS'] = (os.environ.get('EVOLVE_CFLAGS', '') + ' -g').strip()   # before evolve is imported
import counters as C                         # find_perf, PerfHold, PerfAccess
import evolve as E                           # after EVOLVE_CFLAGS, which it reads as it imports
RUNS, PERIOD, TOP = 1, 500, 10
if '--runs' in ARGS: i = ARGS.index('--runs'); RUNS = int(ARGS[i + 1]); del ARGS[i:i + 2]
WORKLOADS = ['kernel', 'corpus']

LABEL = re.compile(r'^\s*(L_\w+)\s*:|^static\b[^(;]*\bvoid\s+(H_\w+)\s*\(')
def labels_of(path, cache={}):
    """Line number -> the handler whose label comes last at or before it, for one source."""
    if path not in cache:
        marks = []
        for n, l in enumerate(open(path, errors='replace'), 1):
            m = LABEL.match(l)
            if m: marks.append((n, m.group(1) or m.group(2)))
        cache[path] = marks
    return cache[path]
def handler(srcdir, file, line):
    p = next((q for q in (file, os.path.join(srcdir, os.path.basename(file)), os.path.join(E.ROOT, 'engine', os.path.basename(file)))
              if os.path.isabs(q) and os.path.exists(q)), None)
    if not p: return None
    best = None
    for n, name in labels_of(p):
        if n > line: break
        best = name
    return best or '(before any handler)'

REPORT = re.compile(r'^\s*([\d.]+)%\s+(\d+)\s+(\S+?):(\d+)\s*$')
def misses(eng, img, wl, pw, srcdir, perf):
    """Handler -> sampled misses, for one workload."""
    data = os.path.join(pw, 'missmap.data'); got = collections.Counter()
    for _ in range(RUNS):
        r = subprocess.run([perf, 'record', '-q', '-e', 'branch-misses:u', '-c', str(PERIOD), '-o', data, '--', eng, img],
                           input=E.program(wl), cwd=pw, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if r.returncode: sys.exit('missmap: perf record exited %d on %s - perf said:\n%s' % (r.returncode, wl, r.stderr.decode(errors='replace')[-1500:]))
        r = subprocess.run([perf, 'report', '-i', data, '--stdio', '--no-children', '--sort', 'srcline', '-F', 'overhead,sample,srcline'],
                           capture_output=True, text=True, cwd=pw)
        if r.returncode: sys.exit('missmap: perf report exited %d - perf said:\n%s' % (r.returncode, r.stderr[-1500:]))
        for l in r.stdout.splitlines():
            m = REPORT.match(l)
            if m: got[handler(srcdir, m.group(3), int(m.group(4))) or '(no line in the engine\'s source: the JIT\'s code, or unresolved)'] += int(m.group(2))
            elif re.match(r'^\s*[\d.]+%\s+\d+\s+\S', l): got['(no source line)'] += int(l.split()[1])
    return got

if __name__ == '__main__':
    PERF, PERF_VERSION, tried = C.find_perf()
    for c, why in tried: print('missmap: %s does not run: %s' % (c, why), file=sys.stderr)
    if not PERF: sys.exit('missmap: no perf runs here - on Ubuntu: sudo apt install linux-tools-$(uname -r)')
    E.setup()
    designs = C.pick_designs(ARGS) if hasattr(C, 'pick_designs') else None
    if designs is None:
        designs = [('s6', dict(E.HUMAN['s6-cv8b']))]
        path, recs = E.newest_front()
        if recs:
            jit = [r for r in recs if r['genome'].get('jit')]; nojit = [r for r in recs if not r['genome'].get('jit')]
            for tag, pool, key in (('fastest, JIT', jit, 'speed'), ('fastest, no JIT', nojit, 'speed'), ('smallest', recs, 'total')):
                if pool:
                    r = min(pool, key=lambda r: r.get(key) or 9e9); designs.append((r['id'], r['genome']))
    hold = os.environ.get('PERF_HOLD_START')
    print('# Branch misses by handler - lab/evolve/missmap.py\n')
    print('Sampled every %d user-space branch misses (perf record), %d run(s) a workload, by %s (%s); a sample\'s source line charged to the handler whose label precedes it. Host: %s.\n'
          % (PERIOD, RUNS, PERF, PERF_VERSION, open('/proc/cpuinfo').read().split('model name')[1].split(':', 1)[1].split('\n')[0].strip() if os.path.exists('/proc/cpuinfo') else '?'))
    with (C.PerfHold(hold, os.environ['PERF_HOLD_DONE']) if hold else C.PerfAccess()) as access:
        for name, g in designs:
            access.keep()
            d = os.path.join(E.EV, 'missmap-' + name.replace(' ', ''))
            eng, img = E.build(E.canon(g), d); pw = E.private_work(d)     # build() says where they are
            if os.path.exists(eng + '.full'): eng += '.full'   # the same code with its symbols and -g's lines: build() strips
                                                              # the engine it measures (Iteration 297: the first laptop run's
                                                              # samples all came back without a source line)
            for wl in WORKLOADS:
                got = misses(eng, img, wl, pw, d, PERF)
                tot = sum(got.values()) or 1
                print('## %s on %s - %d samples\n\n| handler | samples | share |\n|---|---|---|' % (name, wl, tot))
                for h, n in got.most_common(TOP): print('| %s | %d | %.1f%% |' % (h, n, 100.0 * n / tot))
                print()
