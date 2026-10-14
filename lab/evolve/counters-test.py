#!/usr/bin/env python3
"""counters-test.py - counters.py's PerfAccess leaves kernel.perf_event_paranoid as it found
it, however the measurement ends (Iteration 279; the owner: no global change).

Run as root on a scratch machine - it writes the setting, and puts the machine's own
value back at the end whatever happens. A stand-in sudo, made here in a temporary
directory, runs its command (FAKE_REFUSE_V: it refuses -v; FAKE_REFUSE_RESTORE: it
refuses to write 4). From 4, Ubuntu's default, eight cases: a normal end, an error,
SIGTERM, SIGHUP, Ctrl-C, the setting already 2 (no sudo at all), sudo refused at the
start (nothing changed), a restore that fails (said, with the command). Iteration
279 on the development VM: 8 of 8.

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
  *) break;;
esac; done
[ $# -eq 0 ] && exit 0
case "$*" in *=4*) [ "${FAKE_REFUSE_RESTORE:-}" ] && exit 1;; esac
exec "$@"
''' % LOG); os.chmod(os.path.join(FAKE, 'sudo'), 0o755)
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
    print('PerfAccess: %d of %d cases right' % (sum(ok for _, ok in res), len(res)))

finally:
    setp(ORIG)
    print('the machine\'s own setting back: %d' % rd())
sys.exit(0 if all(ok for _, ok in res) else 1)
