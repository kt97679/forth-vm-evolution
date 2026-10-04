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

Calibration (prompts/03-audit-tooling): OLD against itself, on the first
system and workload, must come out 1.000 within the noise; the distance
from 1.000 is the size of a difference that means nothing.

Workloads: parse, fib, loop (bench/*.fth) and corpus (tests/corpus/core.fth),
taken from NEW's tree. Systems: names as in build/ - X-64 with X-s64.img;
s7-* run on spn-64, s8-* on s8-spncv8-64. BENCH_CPU=N pins to a core.
"""
import os, re, shutil, subprocess, sys, tempfile, time

def opt(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and not sys.argv[i - 1].startswith('--')]
if len(args) != 2: sys.exit(__doc__)
OLD, NEW = args
SYSTEMS = opt('--systems', 's0-cell,s4-cv8,s6-cv8b,s8-spncv8').split(',')
WORK = opt('--workloads', 'parse,corpus').split(',')
ROUNDS = int(opt('--rounds', '12'))
PIN = ['taskset', '-c', os.environ['BENCH_CPU']] if os.environ.get('BENCH_CPU') and shutil.which('taskset') else []

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
    def pair(a, b, w):
        """best CPU ns of a and of b, alternating; their outputs equal?"""
        best, outs = [1 << 62, 1 << 62], [None, None]
        for r_ in range(ROUNDS):
            for k in ((0, 1) if r_ % 2 == 0 else (1, 0)):
                build, sysname = (a, b)[k]
                ns, out = run([engine(build, sysname), os.path.join(build, sysname + '-s64.img')], inputs[w], os.path.join(build, 'work'))
                best[k] = min(best[k], ns); outs[k] = out
        return best, outs[0] == outs[1]
    model = next((l.split(':', 1)[1].strip() for l in open('/proc/cpuinfo') if l.startswith('model name')), '?')
    L = ['# %s against %s' % (trees['new'][0], trees['old'][0]), '',
         'machine: %s; %d rounds, alternating; %s; every figure MEASURED: the process\'s own CPU time,'
         % (model, ROUNDS, ' '.join(PIN) or 'not pinned'),
         'best of the rounds, workloads fed on standard input. Reproduce: `tools/compare-commits.py %s %s --systems %s --workloads %s --rounds %d`.'
         % (trees['old'][0], trees['new'][0], ','.join(SYSTEMS), ','.join(WORK), ROUNDS), '']
    (c0, c1), _ = pair((trees['old'][1], SYSTEMS[0]), (trees['old'][1], SYSTEMS[0]), WORK[0])
    L += ['calibration: %s on %s, old against itself - expected 1.000, measured %.3f' % (SYSTEMS[0], WORK[0], c1 / c0), '',
          '| system | workload | old ms | new ms | new / old | same output |', '|---|---|---|---|---|---|']
    print('\n'.join(L), flush=True)
    for s_ in SYSTEMS:
        for w in WORK:
            (o, n), same = pair((trees['old'][1], s_), (trees['new'][1], s_), w)
            line = '| %s | %s | %.2f | %.2f | **%.3f** | %s |' % (s_, w, o / 1e6, n / 1e6, n / o, 'yes' if same else 'NO')
            print(line, flush=True); L.append(line)
finally:
    for label in ('old', 'new'):
        subprocess.run(['git', 'worktree', 'remove', '--force', os.path.join(tmp, label)], cwd=ROOT, capture_output=True)
    subprocess.run(['git', 'worktree', 'prune'], cwd=ROOT, capture_output=True)
    shutil.rmtree(tmp, ignore_errors=True)
