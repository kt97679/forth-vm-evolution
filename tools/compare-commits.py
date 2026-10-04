#!/usr/bin/env python3
"""compare-commits.py OLD NEW [--systems s0-cell,s6-cv8b] [--workloads parse,corpus]
                              [--rounds N]

Two commits, each built in a git worktree of its own, timed against each
other on the same workloads fed on standard input. The measure is the
process's own CPU time (tools/cputime.c), OLD and NEW alternating run by
run, the best of N each; printed: NEW / OLD per system and workload, and
whether the two printed the same. For the figures in FINDINGS-*.md that
compare a change with the build before it - each such figure names the
command that reproduces it (prompts/07-git-handoff: a figure measured
with something that is not in the repository is not supported).

Calibration (prompts/03-audit-tooling), in every row: each round runs OLD
twice and NEW once, in rotating order, so each row has its own OLD against
itself - same system, workload and session. A difference no larger than
that row's own distance from 1.000 is noise; the row says which. (At
Iteration 6 one calibration on the first workload served all rows, and
corpus - the shortest - was judged by fib's noise.)

Workloads: parse, fib, loop (bench/*.fth) and corpus (tests/corpus/core.fth),
taken from NEW's tree. Systems: names as in build/ - X-64 with X-s64.img;
s7-* run on spn-64, s8-* on s8-spncv8-64. BENCH_CPU=N pins to a core.
"""
import math, os, re, shutil, subprocess, sys, tempfile, time

def opt(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and not sys.argv[i - 1].startswith('--')]
if len(args) != 2: sys.exit(__doc__)
OLD, NEW = args
SYSTEMS = opt('--systems', 's0-cell,s4-cv8,s6-cv8b,s8-spncv8').split(',')
WORK = opt('--workloads', 'parse,corpus').split(',')
ROUNDS = int(opt('--rounds', '12'))
def quiet_cpu():
    """As the evolver pins (lab/evolve/evolve.py, quiet_cpu): BENCH_CPU if
    set, else the core that with its hyperthread sibling was least busy
    over one second, never core 0 by choice. Unpinned, the first check of
    s6 on the Ryzen calibrated at 1.030 (Iteration 6)."""
    if not shutil.which('taskset'): return [], 'not pinned (no taskset)'
    if os.environ.get('BENCH_CPU'): return ['taskset', '-c', os.environ['BENCH_CPU']], 'pinned to cpu %s (BENCH_CPU)' % os.environ['BENCH_CPU']
    def busy():
        b = {}
        for l in open('/proc/stat'):
            f = l.split()
            if re.match(r'cpu\d+$', f[0]):
                v = list(map(int, f[1:])); b[int(f[0][3:])] = (sum(v) - v[3] - v[4], sum(v))
        return b
    a = busy(); time.sleep(1); b = busy()
    load = {c: (b[c][0] - a[c][0]) / max(b[c][1] - a[c][1], 1) for c in b}
    def sib(c):
        try:
            out = set()
            for part in open('/sys/devices/system/cpu/cpu%d/topology/thread_siblings_list' % c).read().strip().split(','):
                lo, _, hi = part.partition('-'); out |= set(range(int(lo), int(hi or lo) + 1))
            return out
        except OSError: return {c}
    score = {c: sum(load.get(x, 0) for x in sib(c)) for c in load}
    c = min([c for c in score if c != 0] or list(score), key=lambda c: (score[c], c))
    return ['taskset', '-c', str(c)], 'pinned to cpu %d, the quietest with its sibling (%.0f%% busy; BENCH_CPU=N to choose)' % (c, 100 * score[c])
PIN, PINNED = quiet_cpu()
print(PINNED, file=sys.stderr, flush=True)

def git(*a, cwd=ROOT):
    return subprocess.run(['git'] + list(a), cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()

def engine(build, name):
    for e in (name + '-64', 'spn-64' if name.startswith('s7') else '', 's8-spncv8-64' if name.startswith('s8') else ''):
        if e and os.path.exists(os.path.join(build, e)): return os.path.join(build, e)
    sys.exit('no engine for %s in %s' % (name, build))

def run(cmd, inp, cwd):
    r = subprocess.run(PIN + [CPUT] + cmd, cwd=cwd, input=inp, capture_output=True)
    m = re.search(rb'^CPUNS (\d+)', r.stderr, re.M)
    if not m: sys.exit('no CPU time from %s: %r' % (' '.join(cmd), r.stderr[-200:]))
    return int(m.group(1)), r.stdout

tmp = tempfile.mkdtemp(prefix='cmp-')
trees = {}
try:
    for label, rev in (('old', OLD), ('new', NEW)):
        sha = git('rev-parse', '--short', rev)
        t = os.path.join(tmp, label)
        git('worktree', 'add', '--detach', t, sha)
        print('building %s %s ...' % (label, sha), file=sys.stderr, flush=True)
        b = subprocess.run(['bash', 'tools/build-stages.sh'], cwd=t, env=dict(os.environ, LAYOUTS='1'), capture_output=True)
        if b.returncode: sys.exit('build of %s failed:\n%s' % (sha, b.stdout.decode(errors='replace')[-600:]))
        trees[label] = (sha, os.path.join(t, 'build'))
    CPUT = os.path.join(trees['new'][1], 'cputime')
    inputs = {w: open(os.path.join(tmp, 'new', 'tests', 'corpus', 'core.fth') if w == 'corpus'
                      else os.path.join(tmp, 'new', 'bench', w + '.fth'), 'rb').read() for w in WORK}
    def triple(old, new, w):
        """best CPU ns of OLD, NEW and OLD again, rotating the order each
        round; do OLD and NEW print the same?"""
        runs = [old, new, old]; best = [1 << 62] * 3; outs = [None] * 3
        for r_ in range(ROUNDS):
            for k in [(r_ + j) % 3 for j in range(3)]:
                build, sysname = runs[k]
                ns, out = run([engine(build, sysname), os.path.join(build, sysname + '-s64.img')], inputs[w], os.path.join(build, 'work'))
                best[k] = min(best[k], ns); outs[k] = out
        return best, outs[0] == outs[1]
    model = next((l.split(':', 1)[1].strip() for l in open('/proc/cpuinfo') if l.startswith('model name')), '?')
    L = ['# %s against %s' % (trees['new'][0], trees['old'][0]), '',
         'machine: %s; %d rounds; %s; every figure MEASURED: the process\'s own CPU time,' % (model, ROUNDS, PINNED),
         'best of the rounds, workloads fed on standard input. Reproduce: `tools/compare-commits.py %s %s --systems %s --workloads %s --rounds %d`.'
         % (trees['old'][0], trees['new'][0], ','.join(SYSTEMS), ','.join(WORK), ROUNDS), '',
         'Each row is its own calibration: old against itself, in the same rounds. A change counts as beyond noise only if larger than both that and 2%% - one old-against-old pair is a single draw of the noise, not its width, and the project\'s run-to-run noise is about 2%% (results/evolve-knockout-amd-ryzen-7-pro-8840hs.md); on the VM, corpus alone moved from 0.996 to 1.010 between two sessions.' % (), '',
         '| system | workload | old ms | new ms | new / old | old / old | beyond noise? | same output |', '|---|---|---|---|---|---|---|---|']
    print('\n'.join(L), flush=True)
    for s_ in SYSTEMS:
        for w in WORK:
            (o, n, o2), same = triple((trees['old'][1], s_), (trees['new'][1], s_), w)
            change, noise = abs(math.log(n / o)), max(abs(math.log(o2 / o)), math.log(1.02))
            line = '| %s | %s | %.2f | %.2f | **%.3f** | %.3f | %s | %s |' % (s_, w, o / 1e6, n / 1e6, n / o, o2 / o, 'yes' if change > noise else 'no', 'yes' if same else 'NO')
            print(line, flush=True); L.append(line)
finally:
    for label in ('old', 'new'):
        subprocess.run(['git', 'worktree', 'remove', '--force', os.path.join(tmp, label)], cwd=ROOT, capture_output=True)
    subprocess.run(['git', 'worktree', 'prune'], cwd=ROOT, capture_output=True)
    shutil.rmtree(tmp, ignore_errors=True)
