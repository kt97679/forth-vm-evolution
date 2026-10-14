#!/usr/bin/env python3
"""perf-hold.py START DONE LOG [WAIT_START_S WAIT_RUN_S] - root's half of counters.py's
perf counters in next-run.sh's chain (Iteration 282).

next-run.sh's chain runs in the background, where sudo cannot ask for a password
(the first try failed so: "unable to read password: Input/output error"). So
perf-hold-start.sh asks in the foreground, once, and starts this as root
(sudo -b). It changes nothing until counters.py writes its pid into START, then
sets kernel.perf_event_paranoid to 2 - user-space counters - and puts the old
value back when counters.py writes DONE or its process is gone (a crash or kill
-9 included), or after WAIT_RUN_S (2 h); if counters.py never starts within
WAIT_START_S (4 h) - the chain failed before it - it exits having changed
nothing. Every step is a line in LOG; a SIGTERM, SIGINT or SIGHUP restores too. It
takes a session of its own: a closed terminal does not end it.
"""
import os, signal, sys, time
if len(sys.argv) not in (4, 6): sys.exit(__doc__)
START, DONE, LOG = sys.argv[1:4]
WAIT_START, WAIT_RUN = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) == 6 else (4 * 3600, 2 * 3600)
P, WANT = '/proc/sys/kernel/perf_event_paranoid', 2
try: os.setsid()                        # its own session: closing the terminal next-run.sh was started
except OSError: pass                    # from must not end the hold, any more than it ends the chain (nohup)
_null = os.open(os.devnull, os.O_RDWR)
for _fd in (0, 1, 2): os.dup2(_null, _fd)
def say(m):
    with open(LOG, 'a') as f: f.write('perf-hold %s: %s\n' % (time.strftime('%H:%M:%S'), m))
def rd(): return int(open(P).read())
def setp(v):
    with open(P, 'w') as f: f.write('%d\n' % v)
OLD, changed = rd(), False
def restore(*_):
    global changed
    if changed:
        changed = False
        try: setp(OLD)
        except OSError: pass
        now = rd()
        say('kernel.perf_event_paranoid restored to %d' % now if now == OLD else
            'COULD NOT RESTORE kernel.perf_event_paranoid to %d (it is %d) - run: sudo sysctl kernel.perf_event_paranoid=%d' % (OLD, now, OLD))
    sys.exit(0)
for s_ in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP): signal.signal(s_, restore)
say('waiting for counters.py; kernel.perf_event_paranoid is %d' % OLD)
t0 = time.time()
while not os.path.exists(START):
    if time.time() - t0 > WAIT_START: say('counters.py did not start - nothing changed'); sys.exit(0)
    time.sleep(2)
try: pid = int(open(START).read().split()[0])
except (ValueError, IndexError): pid = 0
if OLD > WANT: setp(WANT); changed = True
say('kernel.perf_event_paranoid %d while counters.py (pid %d) measures' % (rd(), pid))
t1 = time.time()
while pid and os.path.exists('/proc/%d' % pid) and not os.path.exists(DONE) and time.time() - t1 < WAIT_RUN: time.sleep(1)
restore()
