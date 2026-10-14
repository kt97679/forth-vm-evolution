#!/usr/bin/env python3
"""counters-test.py - counters.py's PerfAccess leaves kernel.perf_event_paranoid as it found
it, however the measurement ends (Iteration 279; the owner: no global change).

Run as root on a scratch machine - it writes the setting, and puts the machine's own
value back at the end whatever happens. A stand-in sudo, made here in a temporary
directory, runs its command (FAKE_REFUSE_V: it refuses -v; FAKE_REFUSE_RESTORE: it
refuses to write 4; -b runs it in the background). From 4, Ubuntu's default: a normal
end, an error, SIGTERM, SIGHUP, Ctrl-C, the setting already 2 (no sudo at all), sudo
refused at the start (nothing changed), a restore that fails (said, with the command)
- Iteration 279's eight; and next-run.sh's chain (Iteration 282): perf-hold.py with
PerfHold, counters.py killed -9, counters.py never started, perf-hold-start.sh with
the setting already 2, with no terminal, and in a terminal (script(1)); perf without
its kernel's tools (Iteration 283); which perf is found (Iteration 284).

    sudo python3 lab/evolve/counters-test.py
"""
import os, signal, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(os.path.dirname(os.path.dirname(HERE)))
if os.geteuid() != 0: sys.exit('counters-test: run as root, on a scratch machine (it writes kernel.perf_event_paranoid)')
FAKE = tempfile.mkdtemp(prefix='fakesudo-'); LOG = os.path.join(FAKE, 'log')
open(os.path.join(FAKE, 'sudo'), 'w').write('''#!/bin/sh
echo "sudo $*" >> %s
while [ $# -gt 0 ]; do case "$1" in
  -v) [ "${FAKE_REFUSE_V:-}" ] && exit 1; [ $# -eq 1 ] && exit 0; shift;;
  -n) shift;;
  -b) BG=1; shift;;
  *) break;;
esac; done
[ $# -eq 0 ] && exit 0
case "$*" in *=4*) [ "${FAKE_REFUSE_RESTORE:-}" ] && exit 1;; esac
[ -n "${BG:-}" ] && { trap "" HUP; "$@" > /dev/null 2>&1 & exit 0; }   # sudo -b runs it apart from the terminal's foreground group; script(1) closing its pty at once must not hang it up
exec "$@"
''' % LOG); os.chmod(os.path.join(FAKE, 'sudo'), 0o755)
open(os.path.join(FAKE, 'perf'), 'w').write('''#!/bin/sh
[ "${FAKE_PERF_BROKEN:-}" ] && { echo "WARNING: perf not found for kernel 6.8.0-87" >&2; echo "  linux-tools-6.8.0-87-generic" >&2; exit 2; }
echo "perf version 6.8.12"
'''); os.chmod(os.path.join(FAKE, 'perf'), 0o755); os.chmod(FAKE, 0o755)   # Iteration 283: perf-hold-start.sh tries perf first
os.environ['PATH'] = FAKE + ':' + os.environ['PATH']
sys.path.insert(0, HERE); import counters as C
P = C.PARANOID; rd = lambda: int(open(P).read())
def setp(v): subprocess.run(['sysctl', '-q', '-w', 'kernel.perf_event_paranoid=%d' % v], check=True)
ORIG = rd()
try:
    setp(4)
    res = []
    def case(name, ok): res.append((name, ok)); print('  %-58s %s' % (name, 'ok' if ok else 'WRONG'))
    with C.PerfAccess() as a: during = rd()
    case('normal exit: 2 during, 4 after', during == 2 and rd() == 4)
    try:
        with C.PerfAccess(): raise ValueError('a failure mid-measurement')
    except ValueError: pass
    case('an error mid-measurement: 4 after', rd() == 4)
    child = "import sys, time; sys.path.insert(0, 'lab/evolve'); import counters as C\nwith C.PerfAccess(): print('in', flush=True); time.sleep(60)"
    for sig, name in ((signal.SIGTERM, 'SIGTERM'), (signal.SIGHUP, 'SIGHUP'), (signal.SIGINT, 'Ctrl-C (SIGINT)')):
        p = subprocess.Popen([sys.executable, '-c', child], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        p.stdout.readline(); d = rd(); p.send_signal(sig); rc = p.wait(timeout=20)
        case('%s while measuring: 2 during, 4 after, exit %d' % (name, rc), d == 2 and rd() == 4 and rc == 128 + sig)
    setp(2); open(LOG, 'w').close()
    with C.PerfAccess(): pass
    case('already 2: no sudo at all, nothing changed', open(LOG).read() == '' and rd() == 2)
    setp(4); os.environ['FAKE_REFUSE_V'] = '1'
    try:
        with C.PerfAccess(): pass
        case('sudo refused at the start: stops', False)
    except SystemExit as e:
        case('sudo refused at the start: stops, nothing changed', rd() == 4 and 'nothing changed' in str(e))
    del os.environ['FAKE_REFUSE_V']; os.environ['FAKE_REFUSE_RESTORE'] = '1'
    r = subprocess.run([sys.executable, '-c', "import sys; sys.path.insert(0, 'lab/evolve'); import counters as C\nwith C.PerfAccess(): pass"], capture_output=True, text=True)
    case('a restore that fails: says so, with the command', rd() == 2 and 'COULD NOT RESTORE' in r.stderr and 'sudo sysctl kernel.perf_event_paranoid=4' in r.stderr)
    del os.environ['FAKE_REFUSE_RESTORE']; setp(4)
    # Iteration 282: next-run.sh's chain - perf-hold.py as root, counters.py's PerfHold as the user
    import time
    HOLD = os.path.join(HERE, 'perf-hold.py'); W = tempfile.mkdtemp(prefix='hold-'); os.chmod(W, 0o777)
    def files(tag): return os.path.join(W, tag + '.start'), os.path.join(W, tag + '.done'), os.path.join(W, tag + '.log')
    def wait_for(cond, t=15):
        for _ in range(int(t * 10)):
            if cond(): return True
            time.sleep(0.1)
        return False
    holder = "import sys, time; a = sys.argv[1:]; sys.path.insert(0, %r); import counters as C\nwith C.PerfHold(a[0], a[1]): print('in', flush=True); time.sleep(float(a[2]))" % HERE   # counters.py takes sys.argv as it imports
    setp(4); S, D, L = files('a'); h = subprocess.Popen([sys.executable, HOLD, S, D, L, '30', '30'])
    p = subprocess.Popen(['runuser', '-u', 'claude', '--', sys.executable, '-c', holder, S, D, '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p.stdout.readline(); d = rd(); p.wait(timeout=30); h.wait(timeout=30)
    case('the chain: perf-hold.py and PerfHold - 2 during, 4 after', d == 2 and rd() == 4 and 'restored to 4' in open(L).read())
    S, D, L = files('b'); h = subprocess.Popen([sys.executable, HOLD, S, D, L, '30', '30'])
    p = subprocess.Popen(['runuser', '-u', 'claude', '--', sys.executable, '-c', holder, S, D, '60'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    p.stdout.readline(); d = rd(); os.kill(int(open(S).read().split()[0]), signal.SIGKILL); h.wait(timeout=30)   # the pid it announced: no pattern that could match this test's own shell
    case('the chain: counters.py killed -9 - perf-hold.py sees it gone, 4 after', d == 2 and rd() == 4)
    S, D, L = files('c'); h = subprocess.run([sys.executable, HOLD, S, D, L, '3', '30'], timeout=30)
    case('the chain failed before counters.py: perf-hold.py gives up, nothing changed', rd() == 4 and 'did not start - nothing changed' in open(L).read())
    START_SH = os.path.join(HERE, 'perf-hold-start.sh')
    setp(2); open(LOG, 'w').close(); S, D, L = files('d')
    r = subprocess.run(['sh', START_SH, S, D, L], stdin=subprocess.DEVNULL, capture_output=True, text=True)
    case('perf-hold-start.sh, the setting already 2: no sudo, nothing started', r.returncode == 0 and open(LOG).read() == '')
    setp(4); r = subprocess.run(['sh', START_SH, S, D, L], stdin=subprocess.DEVNULL, capture_output=True, text=True)
    case('perf-hold-start.sh with no terminal: refuses, says why', r.returncode == 1 and 'a terminal to ask on' in r.stderr)
    open(LOG, 'w').close(); os.environ['FAKE_PERF_BROKEN'] = '1'
    r = subprocess.run(['sh', START_SH, S, D, L], stdin=subprocess.DEVNULL, capture_output=True, text=True)
    case("perf-hold-start.sh, perf without its kernel's tools: refuses before sudo, with perf's words", r.returncode == 1 and 'not found for kernel' in r.stderr and 'nothing started' in r.stderr and open(LOG).read() == '')
    del os.environ['FAKE_PERF_BROKEN']
    S, D, L = files('e')
    r = subprocess.run(['script', '-qec', 'sh %s %s %s %s' % (START_SH, S, D, L), '/dev/null'], capture_output=True, text=True)
    ok = r.returncode == 0 and wait_for(lambda: os.path.exists(L))
    q = subprocess.Popen(['runuser', '-u', 'claude', '--', sys.executable, '-c', holder, S, D, '1'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    q.stdout.readline(); d = rd(); q.wait(timeout=30)
    case('perf-hold-start.sh in a terminal: sudo once, the helper holds 2, then 4', ok and d == 2 and wait_for(lambda: rd() == 4) and 'restored to 4' in open(L).read())
    # Iteration 284: which perf - find_perf, as next-run.sh asks it (counters.py --find-perf)
    import platform
    TR = tempfile.mkdtemp(prefix='tools-'); os.chmod(TR, 0o755)
    def fakeperf(path, version):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w').write('#!/bin/sh\necho "perf version %s"\n' % version); os.chmod(path, 0o755)
    def find(**env):
        e = dict(os.environ, PERF_TOOLS_ROOT=TR, FAKE_PERF_BROKEN='1'); e.pop('PERF', None); e.update(env)
        return subprocess.run([sys.executable, os.path.join(HERE, 'counters.py'), '--find-perf'], env=e, capture_output=True, text=True)
    r = find()
    case('no perf runs anywhere: --find-perf fails, says what it tried', r.returncode == 1 and 'not found for kernel' in r.stderr and 'linux-tools-$(uname -r)' in r.stderr)
    fakeperf(os.path.join(TR, 'linux-tools', '6.8.0-90-generic', 'perf'), '6.8.12')
    r = find()
    case("the wrapper without the kernel's tools, another kernel's perf installed: that one", r.returncode == 0 and r.stdout.strip().endswith('6.8.0-90-generic/perf') and 'using' in r.stderr)
    fakeperf(os.path.join(TR, 'linux-tools', platform.release(), 'perf'), '6.18.1')
    fakeperf(os.path.join(TR, 'linux-tools', '99.0.0-1-generic', 'perf'), '99.0')
    r = find()
    case("the running kernel's perf before a newer one", r.returncode == 0 and platform.release() in r.stdout)
    fakeperf(os.path.join(TR, 'mine', 'perf'), '7.0')
    r = find(PERF=os.path.join(TR, 'mine', 'perf'))
    case('PERF given and running: used first', r.returncode == 0 and r.stdout.strip() == os.path.join(TR, 'mine', 'perf'))
    subprocess.run(['pkill', '-f', r'^[^ ]*python3[^ ]* [^ ]*/perf-hold\.py '], check=False)   # anchored: a bare pattern matches the shell that runs this
    print('PerfAccess and perf-hold: %d of %d cases right' % (sum(ok for _, ok in res), len(res)))

finally:
    setp(ORIG)
    print('the machine\'s own setting back: %d' % rd())
sys.exit(0 if all(ok for _, ok in res) else 1)
