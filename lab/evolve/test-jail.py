#!/usr/bin/env python3
"""test-jail.py - prove that an engine the evolver runs cannot fork.

Iteration 10: a run on the owner's laptop forked without bound - a broken
design reaching the FORK primitive in a loop - and froze the machine. The
evolver now jails every engine it runs (lab/evolve/evolve.py, _contain;
tools/cputime.c, CPUTIME_JAIL): no new processes, bounded memory and
files. This checks it, on hand-made s6, in an order that is safe even if
the jail does NOT hold:

  1. one FORK, jailed: it must fail - and if it does not, stop here;
  2. one FORK, not jailed: it must succeed - so step 1 tested something;
  3. only then a fork bomb, jailed, through the evolver's own sh(): run
     directly and under cputime, the engine's processes counted every few
     milliseconds - at most one engine, and the run ends.

As root, RLIMIT_NPROC does not bind, so the engine runs drop to nobody
(uid 65534); as an ordinary user they run as you. Prints PASS or FAIL.
"""
import os, sys, threading, time, subprocess, shutil, signal
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
ENG = os.path.join(E.O, 's6-cv8b-64'); IMG = os.path.join(E.O, 's6-cv8b-s64.img')
for f in (ENG, IMG, E.CPUT):
    if not os.path.exists(f): sys.exit('no %s - run tools/build-stages.sh first' % f)
ROOT_RUN = os.geteuid() == 0
WORK = '/tmp/test-jail-%d' % os.getpid(); os.makedirs(WORK); os.chmod(WORK, 0o777)
if ROOT_RUN:                     # each engine run drops to nobody, after its limits are set
    real = E._contain
    def dropping(cpu, kind=None):
        f = real(cpu, kind)
        # drop first: a set*uid over RLIMIT_NPROC makes the next execve fail
        # (Linux 3.1+), which would refuse the engine rather than its forks
        def g(): os.setgid(65534); os.setuid(65534); f()
        return g
    E._contain = dropping
fails = []
def check(ok, what):
    print('  %-60s %s' % (what, 'ok' if ok else 'FAIL')); ok or fails.append(what)
def run(cmd, inp, cpu=3, jail=True):
    real_kind = E._kind
    if not jail: E._kind = lambda c: None          # step 2 only: the engine as a build tool would run
    try: return E.sh(cmd, cwd=WORK, inp=inp, timeout=30, cpu=cpu)
    finally: E._kind = real_kind
def numbers(r): return [l.strip() for l in r.stdout.decode(errors='replace').replace('\r', '').split('\n') if l.strip().lstrip('-').isdigit()]

ONE = b'FORK . CR BYE\n'
r = run([ENG, IMG], ONE)
n = numbers(r)
check(n == ['-1'] or (len(n) == 1 and int(n[0]) < 0), '1. one FORK, jailed: refused (printed %s)' % n)
if fails: print('FAIL - the jail does not hold here: the fork bomb is NOT run'); shutil.rmtree(WORK, True); sys.exit(1)
r = run([ENG, IMG], ONE, jail=False)
n = numbers(r)
check(len(n) == 2 and '0' in n, '2. one FORK, not jailed: two processes printed (%s)' % n)

BOMB = b': BOMB BEGIN FORK DROP 0 UNTIL ; BOMB\n'   # the kernel has UNTIL; AGAIN comes with extend.4
def engines():
    k = 0
    for p in os.listdir('/proc'):
        if p.isdigit():
            try: k += os.readlink('/proc/%s/exe' % p) == os.path.realpath(ENG)
            except OSError: pass
    return k
for label, cmd in (('3a. fork bomb, jailed, run directly', [ENG, IMG]), ('3b. fork bomb, jailed, under cputime', [E.CPUT, ENG, IMG])):
    peak = [0]; stop = threading.Event()
    def watch():
        while not stop.is_set(): peak[0] = max(peak[0], engines()); time.sleep(0.003)
    t = threading.Thread(target=watch); t.start(); t0 = time.time()
    try:
        r = run(cmd, BOMB, cpu=2)
        # under cputime the CPU limit kills the engine - cputime's child - and
        # cputime exits reporting it: 128 + the signal, as a shell would
        ended = 'stopped at its CPU limit' if r.returncode == 128 + signal.SIGXCPU else 'EXITED %d: %r' % (r.returncode, r.stdout[-60:])
    except subprocess.TimeoutExpired: ended = 'stopped at its CPU limit'
    stop.set(); t.join()
    time.sleep(0.2); left = engines()
    # A bomb that exits did not run (the first version of this test used
    # AGAIN, which the kernel lacks, and passed on an error message): only
    # a loop of refused forks, stopped by its CPU limit, counts.
    check(peak[0] <= 1 and left == 0 and ended.startswith('stopped'),
          '%s: at most %d engine, %s in %.1f s, %d left' % (label, peak[0], ended, time.time() - t0, left))
shutil.rmtree(WORK, True)
print('PASS' if not fails else 'FAIL: %s' % fails)
sys.exit(1 if fails else 0)
