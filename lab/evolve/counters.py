#!/usr/bin/env python3
"""counters.py [--runs N] [IDS...] - where the cycles go: hardware counters for the
designs on the selection workloads (Iteration 278; the laptop's - perf, real hardware).

The question, open since Iteration 243 (Ertl & Paysan): is an interpreted design
held back by mispredicted dispatch branches, or by the chain of dependent updates
to the instruction pointer - the question behind the deferred "IP-update loop form"
(Iteration 260), and gotodup's (copying the dispatch into more handlers predicts
better on some cores)? For each design and selection workload, `perf stat` counts
user-space cycles, instructions, branches and branch misses, the median of N runs:
instructions per cycle, and branch misses per thousand instructions. Low IPC with
few misses points at the dependency chain; many misses at prediction.

The designs: IDS, or from the newest run's front (evolve.newest_front) - the
fastest with the JIT, the fastest without it, the smallest - and hand-made s6.
Database paths, which next-run.sh's experiment passes, are not designs: ignored.

It needs perf - on Ubuntu, once: `sudo apt install linux-tools-common
linux-tools-$(uname -r)` - and user-space counters, which Ubuntu's default
kernel.perf_event_paranoid (4) refuses. So, for its own run only (Iteration 279,
the owner: not changed globally): run in a terminal, it asks sudo once at its
start, sets 2, and puts the old value back when it ends - normally, on an error, on Ctrl-C, on
SIGTERM or SIGHUP - and reads the setting back to check. If the restore fails it
says so, on the terminal, with the command that does it; a reboot restores it
too (the setting is not saved). A counter perf cannot read stops the tool: no
figure from nothing. In next-run.sh's chain, which runs in the background where
sudo cannot ask, next-run.sh asks before it detaches and leaves perf-hold.py to
hold the setting (Iteration 282). lab/evolve/RUNNING.md, "Between runs", says
when and how.

    sh lab/evolve/next-run.sh experiment counters.py       a pack to send back
"""
import atexit, os, platform, shutil, signal, statistics, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
args = sys.argv[1:]; sys.argv = [sys.argv[0]]
RUNS = 5
if '--runs' in args: i = args.index('--runs'); RUNS = int(args[i + 1]); del args[i:i + 2]
IDS = [a for a in args if not a.endswith('.jsonl') and not os.path.exists(a)]
EVENTS = ['cycles:u', 'instructions:u', 'branches:u', 'branch-misses:u']

def parse(text):
    """perf stat -x, output -> {event: count}; exits on a counter it could not read."""
    vals = {}
    for line in text.splitlines():
        f = line.split(',')
        if len(f) < 3 or f[2] not in EVENTS: continue
        if not f[0].strip().isdigit():
            sys.exit('counters: perf could not read %s (%s) - user-space counters need '
                     '`sudo sysctl kernel.perf_event_paranoid=2`, and real hardware' % (f[2], f[0].strip() or 'empty'))
        vals[f[2]] = int(f[0])
    missing = [e for e in EVENTS if e not in vals]
    if missing: sys.exit('counters: perf gave no count for %s' % ', '.join(missing))
    return vals

PARANOID = '/proc/sys/kernel/perf_event_paranoid'
def say(msg):
    """To the terminal: next-run.sh sends this tool's output and errors to files."""
    try:
        with open('/dev/tty', 'w') as t: t.write('counters: %s\n' % msg)
    except OSError: print('counters: %s' % msg, file=sys.stderr)

class PerfAccess:
    """User-space counters for this run only - the setting as it was, after (Iteration 279)."""
    def __init__(self, want=2): self.want, self.changed = want, False
    def read(self): return int(open(PARANOID).read())
    def _set(self, v): return subprocess.run(['sudo', '-n', 'sysctl', '-q', '-w', 'kernel.perf_event_paranoid=%d' % v]).returncode == 0 and self.read() == v
    def __enter__(self):
        self.old = self.read()
        if self.old <= self.want: return self                     # counters allowed already: nothing to change
        say('kernel.perf_event_paranoid is %d; setting %d for this measurement only, restored after - sudo asks once' % (self.old, self.want))
        if subprocess.run(['sudo', '-v']).returncode: sys.exit('counters: sudo refused, or no terminal to ask on - nothing changed')
        if not self._set(self.want): sys.exit('counters: could not set kernel.perf_event_paranoid=%d - nothing measured' % self.want)
        self.changed = True
        for s_ in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP): signal.signal(s_, self._on_signal)
        atexit.register(self.restore)
        return self
    def keep(self):
        """Between designs: keep sudo's credentials fresh, so the restore needs no password."""
        if self.changed: subprocess.run(['sudo', '-n', '-v'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    def restore(self):
        if not self.changed: return
        self.changed = False
        if self._set(self.old): say('kernel.perf_event_paranoid restored to %d' % self.old)
        else: say('COULD NOT RESTORE kernel.perf_event_paranoid to %d (it is %d) - run: sudo sysctl kernel.perf_event_paranoid=%d (a reboot restores it too)' % (self.old, self.read(), self.old))
    def _on_signal(self, signum, frame):
        self.restore(); sys.exit(128 + signum)
    def __exit__(self, *exc): self.restore()

class PerfHold:
    """In next-run.sh's chain (Iteration 282): root's perf-hold.py, started where sudo could
    ask, sets the counters while this measures - announce, wait for it, say done."""
    def __init__(self, start, done): self.start, self.done = start, done
    def __enter__(self):
        with open(self.start, 'w') as f: f.write('%d\n' % os.getpid())
        for _ in range(60):
            if int(open(PARANOID).read()) <= 2: return self
            time.sleep(0.5)
        self.__exit__(); sys.exit('counters: perf-hold.py did not set kernel.perf_event_paranoid (see runs/perf-hold.log) - nothing measured')
    def keep(self): pass
    def __exit__(self, *exc):
        with open(self.done, 'w') as f: f.write('done\n')
        for _ in range(20):
            if int(open(PARANOID).read()) > 2: break
            time.sleep(0.25)
        print('counters: kernel.perf_event_paranoid is %s after the measurement (perf-hold.py)' % open(PARANOID).read().strip(), file=sys.stderr)

if __name__ == '__main__':
    PERF = shutil.which('perf')
    if not PERF: sys.exit('counters: no perf - on Ubuntu: sudo apt install linux-tools-common linux-tools-$(uname -r)')
    import evolve as E
    E.setup()
    designs = [('s6', dict(E.HUMAN['s6-cv8b']))]
    if IDS: designs += [(i, E.recorded_genome(i)) for i in IDS]
    else:
        path, recs = E.newest_front()
        jit = [r for r in recs if r['genome'].get('jit')]; interp = [r for r in recs if not r['genome'].get('jit')]
        picks = ([min(jit, key=lambda r: r['speed'])] if jit else []) + ([min(interp, key=lambda r: r['speed'])] if interp else []) + [min(recs, key=lambda r: r['total'])]
        for r in picks:
            if r['id'] not in [d[0] for d in designs]: designs.append((r['id'], r['genome']))
    rows = []
    hold = os.environ.get('PERF_HOLD_START')        # next-run.sh's chain: perf-hold.py holds it; else ask sudo here
    with (PerfHold(hold, os.environ['PERF_HOLD_DONE']) if hold else PerfAccess()) as access:
        r = subprocess.run([PERF, 'stat', '-x', ',', '-e', ','.join(EVENTS), '--', 'true'], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if r.returncode: sys.exit('counters: perf does not run here (exit %d) - perf said:\n%s\non Ubuntu: sudo apt install linux-tools-$(uname -r), for the kernel running now'
                                  % (r.returncode, r.stderr.decode(errors='replace')[-1500:]))
        parse(r.stderr.decode(errors='replace'))     # Iteration 283: perf tried once on `true` before anything is built
        for name, g in designs:
            access.keep()
            if g is None: sys.exit('counters: no recorded design %s' % name)
            d = os.path.join(E.EV, 'counters'); shutil.rmtree(d, ignore_errors=True)
            eng, img = E.build(E.canon(g), d); pw = E.private_work(d)
            for wl in E.WORK_SEL:
                runs = []
                for _ in range(RUNS):
                    r = subprocess.run([PERF, 'stat', '-x', ',', '-e', ','.join(EVENTS), '--', eng, img], input=E.program(wl),
                                       cwd=pw, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=600)
                    if r.returncode: sys.exit('counters: perf exited %d running %s on %s - perf said:\n%s' % (r.returncode, name, wl, r.stderr.decode(errors='replace')[-1500:]))
                    runs.append(parse(r.stderr.decode(errors='replace')))
                rows.append((name, wl, {e: statistics.median(x[e] for x in runs) for e in EVENTS}))
            shutil.rmtree(d, ignore_errors=True)
    print('# Hardware counters - designs on the selection workloads (lab/evolve/counters.py)\n')
    print('User-space counts, the median of %d runs. Host: %s, %s.\n' % (RUNS, platform.platform(), platform.processor() or platform.machine()))
    print('| design | workload | cycles (M) | instructions per cycle | branch misses per 1k instructions | misses per branch |')
    print('|---|---|---|---|---|---|')
    for name, wl, m in rows:
        c, i, b, bm = (m[e] for e in EVENTS)
        print('| %s | %s | %.1f | %.2f | %.2f | %.2f%% |' % (name, wl, c / 1e6, i / c, 1000.0 * bm / i, 100.0 * bm / b))
