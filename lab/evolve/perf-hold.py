#!/usr/bin/env python3
"""perf-hold.py START DONE LOG [CHAIN] [WAIT_START_S WAIT_RUN_S] - root's half of counters.py's
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
# Iteration 314: and CHAIN, next-run.sh's chain directory - then it holds for every measurement of
# the chain, not only the first: after each, the old value back and START and DONE cleared, it
# waits for the next, until the chain has ended (its status final, or its session gone). Its log
# given to whoever owns its directory after every line - root's files left in the clone were a
# fault (Iteration 302).
a = sys.argv[1:]
if len(a) not in (3, 4, 5, 6): sys.exit(__doc__)
START, DONE, LOG = a[:3]
CHAIN = a[3] if len(a) in (4, 6) else ''
WAIT_START, WAIT_RUN = (int(a[-2]), int(a[-1])) if len(a) in (5, 6) else (4 * 3600, 2 * 3600)
ALL_DAY = 48 * 3600                     # a chain's longest: past it, the hold ends whatever the chain says
P, WANT = '/proc/sys/kernel/perf_event_paranoid', 2
try: os.setsid()                        # its own session: closing the terminal next-run.sh was started
except OSError: pass                    # from must not end the hold, any more than it ends the chain (nohup)
_null = os.open(os.devnull, os.O_RDWR)
for _fd in (0, 1, 2): os.dup2(_null, _fd)
def say(m):
    with open(LOG, 'a') as f: f.write('perf-hold %s: %s\n' % (time.strftime('%H:%M:%S'), m))
    try:
        d = os.stat(os.path.dirname(os.path.abspath(LOG))); os.chown(LOG, d.st_uid, d.st_gid)
    except OSError: pass
def chain_over():
    """The chain has ended: its status final, or no process left in its session."""
    try: st = open(os.path.join(CHAIN, 'status')).read().split('\n')[0].strip()
    except OSError: return True
    if st not in ('running', 'stopping'): return True
    try: sid = int(open(os.path.join(CHAIN, 'sid')).read().strip())
    except (OSError, ValueError): return False          # not detached yet
    for d in os.listdir('/proc'):
        if d.isdigit():
            try:
                if int(open('/proc/%s/stat' % d).read().rsplit(')', 1)[1].split()[3]) == sid: return False
            except (OSError, IndexError, ValueError): pass
    return True
def rd(): return int(open(P).read())
def setp(v):
    with open(P, 'w') as f: f.write('%d\n' % v)
OLD, changed = rd(), False
def put_back():
    global changed
    if changed:
        changed = False
        try: setp(OLD)
        except OSError: pass
        now = rd()
        say('kernel.perf_event_paranoid restored to %d' % now if now == OLD else
            'COULD NOT RESTORE kernel.perf_event_paranoid to %d (it is %d) - run: sudo sysctl kernel.perf_event_paranoid=%d' % (OLD, now, OLD))
def restore(*_):
    put_back(); sys.exit(0)
for s_ in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP): signal.signal(s_, restore)
say('waiting for counters.py; kernel.perf_event_paranoid is %d%s' % (OLD, ' - for every measurement of the chain' if CHAIN else ''))
T0 = time.time()
while True:
    t0 = time.time()
    while not os.path.exists(START):
        if (not CHAIN and time.time() - t0 > WAIT_START) or (CHAIN and chain_over()) or time.time() - T0 > ALL_DAY:
            say('the chain has ended - kernel.perf_event_paranoid is %d' % rd() if CHAIN else 'counters.py did not start - nothing changed'); restore()
        time.sleep(2)
    try: pid = int(open(START).read().split()[0])
    except (ValueError, IndexError, OSError): pid = 0
    if pid and os.path.exists('/proc/%d' % pid):
        if OLD > WANT: setp(WANT); changed = True
        say('kernel.perf_event_paranoid %d while a measurement (pid %d) runs' % (rd(), pid))
        t1 = time.time()
        while os.path.exists('/proc/%d' % pid) and not os.path.exists(DONE) and time.time() - t1 < WAIT_RUN: time.sleep(1)
        put_back()
    for f in (START, DONE):
        try: os.remove(f)
        except OSError: pass
    if not CHAIN: restore()
