#!/usr/bin/env python3
"""outbuf-check.py [ID] - does output buffering break anything? (Iteration 207)

The owner: a buffered-output level for evolution (fsys 4), with tests that
buffering breaks nothing. The standard leaves buffering open; Gforth's
practice (and its proposal, complang.tuwien.ac.at/forth/ansforth-cvs/
buffering.html): never buffer input, never buffer output to a terminal,
buffer it to a pipe or a file. One design (default seed 40's smallest) built
three ways - native I/O (fsys 0, the reference: its flush points are what every
test so far accepted), unbuffered single-SYSCALL (3) and buffered (4) - then:

T1  stdout and stderr on ONE pipe, so their order shows: output larger than
    the buffer, no final newline, the end of input without BYE, errors
    (THROW, ABORT"), a file written between outputs, control characters, a
    return-stack fault the engine itself reports - every level byte for byte
    as native, exit status too.
T2  a prompt before a blocking read: the line is sent, then the prompt must
    appear BEFORE any more input is given - or the engine would wait unseen.
T3  a terminal: output must show at once - "A", a long computation with no
    system call, then "B": "A" must arrive before "B" is written.
"""
import os, sys, pty, time, select, shutil, subprocess, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; sys.argv = ['evolve.py']
spec = importlib.util.spec_from_file_location('E', os.path.join(HERE, 'evolve.py')); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
E.setup()
did = args[0] if args else '0ceb043115'
LEVELS = (0, 3, 4, 5)   # Iteration 211: 5 - read-ahead where a file can seek
builds = {}
for v in LEVELS:
    g = dict(E.recorded_genome(did)); g.pop('fsys', None)
    if v: g['fsys'] = v
    d = os.path.join(E.EV, 'outbuf-%d' % v); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(E.canon(g), d); builds[v] = (eng, img, E.private_work(d))

T1 = {                       # S" ... TYPE, words defined first: ." ABORT" DO LOOP are compile-only
    'stderr between':   'S" A" TYPE S" err" 2 WRITE-FILE DROP S" B" TYPE CR BYE',
    'over the buffer':  ': T 9000 0 DO 42 EMIT LOOP ; T CR S" done" TYPE CR BYE',
    'long TYPE':        'CREATE S 6000 ALLOT  S 6000 66 FILL  S 6000 TYPE CR BYE',
    'no newline, BYE':  'S" tail" TYPE BYE',
    'end of input':     'S" eof-tail" TYPE',
    'THROW':            ': D S" before " TYPE 1 0 / S" after" TYPE CR ; D',
    'ABORT"':           ': X S" x" TYPE 1 ABORT" boom" S" never" TYPE CR ; X S" next" TYPE CR BYE',
    'file between':     'S" A" TYPE S" outbuf.tmp" W/O CREATE-FILE DROP DUP S" data" ROT WRITE-FILE DROP CLOSE-FILE DROP S" B" TYPE CR BYE',
    'control chars':    '7 EMIT 8 EMIT 13 EMIT 9 EMIT S" z" TYPE CR BYE',
    'engine fault':     ': R R ; S" pre " TYPE R',
    # Iteration 229: a zero divisor is -10 THROW in every division word, caught or not
    'DIVZERO':          ": T1 1 0 / ; ' T1 CATCH . : T2 7 0 MOD ; ' T2 CATCH . : T3 7 0 /MOD ; ' T3 CATCH . "
                        ": T4 1 2 0 */ ; ' T4 CATCH . : T5 1 2 0 */MOD ; ' T5 CATCH . : T6 7 0 0 FM/MOD ; ' T6 CATCH . "
                        ": T7 7 0 0 SM/REM ; ' T7 CATCH . : T8 7 0 0 UM/MOD ; ' T8 CATCH . CR\n1 0 / S\" lost\" TYPE\nS\" after\" TYPE CR BYE",
}
def run(v, prog):
    eng, img, pw = builds[v]
    r = subprocess.run([eng, img], cwd=pw, input=(prog + '\n').encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    return r.returncode, r.stdout
fails = 0
print('## T1 - stdout and stderr on one pipe, against native\n')
for name, prog in T1.items():
    ref = run(0, prog)
    res = {v: run(v, prog) for v in LEVELS[1:]}
    ok = all(res[v] == ref for v in res)
    # Iteration 229: every division word throws -10 for a zero divisor, at every
    # level as native: eight -10s, the message for the one not caught, and on.
    if name == 'DIVZERO':
        fails += not (ref[1].count(b'-10 ') == 8 and b'Division by zero' in ref[1] and b'after' in ref[1] and b'lost' not in ref[1])
    # Killed by a signal (the engine fault: a return stack run over), native loses
    # what its C buffer held - the levels keep it: native's output a prefix of
    # theirs, theirs alike, the same signal. Better than native, not worse.
    kept = (not ok and ref[0] < 0 and all(r == ref or (r[0] == ref[0] and r[1].startswith(ref[1])) for r in res.values()))   # each level: native's, or more of it
    fails += not (ok or kept)
    print('- %-16s %s (status %d, %d bytes)%s' % (name, 'same at fsys %s' % ', '.join(map(str, LEVELS[1:])) if ok else
          'killed by signal %d - native loses what its buffer held; %s' % (-ref[0], ', '.join('fsys %d %s' % (v, 'as native' if res[v] == ref else 'keeps %d bytes more' % (len(res[v][1]) - len(ref[1]))) for v in res)) if kept else 'DIFFERS', ref[0], len(ref[1]),
          '' if ok or kept else ' - ' + '; '.join('fsys %d: status %d, %r' % (v, res[v][0], res[v][1][-80:]) for v in res if res[v] != ref)))

def prompt_first(v):
    eng, img, pw = builds[v]
    p = subprocess.Popen([eng, img], cwd=pw, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.stdin.write(b'S" PROMPT>" TYPE KEY EMIT CR BYE\n'); p.stdin.flush()
    got, t0 = b'', time.time()
    while b'PROMPT>' not in got and time.time() - t0 < 5:
        r, _, _ = select.select([p.stdout], [], [], 0.2)
        if r: got += os.read(p.stdout.fileno(), 4096)
    seen = b'PROMPT>' in got
    p.stdin.write(b'x\n'); p.stdin.close()
    rest = p.stdout.read(); p.wait(timeout=10)
    return seen, got + rest
print('\n## T2 - the prompt before a blocking read (a pipe)\n')
for v in LEVELS:
    seen, out = prompt_first(v)
    ok = seen and b'PROMPT>x' in out
    fails += not ok
    print('- fsys %d: %s' % (v, 'the prompt shown while the engine waited, then the key echoed' if ok else 'FAILED - %r' % out[-60:]))

def terminal_first(v):
    eng, img, pw = builds[v]
    m, s = pty.openpty()
    p = subprocess.Popen([eng, img], cwd=pw, stdin=subprocess.PIPE, stdout=s, stderr=s)
    os.close(s)
    p.stdin.write(b': W 40000000 0 DO LOOP ; S" A" TYPE W S" B" TYPE CR BYE\n'); p.stdin.close()
    events, t0 = [], time.time()
    while time.time() - t0 < 30:
        r, _, _ = select.select([m], [], [], 0.05)
        if r:
            try: chunk = os.read(m, 4096)
            except OSError: break
            if not chunk: break
            events.append((time.time() - t0, chunk))
        elif p.poll() is not None: break
    p.wait(timeout=10); os.close(m)
    tA = next((t for t, c in events if b'A' in c), None); tB = next((t for t, c in events if b'B' in c), None)
    return tA, tB
print('\n## T3 - a terminal: output at once (no system call between "A" and "B")\n')
for v in LEVELS:
    tA, tB = terminal_first(v)
    early = tA is not None and tB is not None and tB - tA > 0.1
    if v: fails += not early
    print('- fsys %d: "A" at %s s, "B" at %s s - %s' % (v, '%.2f' % tA if tA is not None else '-', '%.2f' % tB if tB is not None else '-',
          ('"A" shown before the computation ended' if early else 'FAILED: "A" held back') if v else
          ('native: shown at once' if early else 'native: held until the next flush - its own buffer does not ask whether it is a terminal')))
print('\n%s' % ('PASS' if not fails else 'FAIL - %d' % fails))
sys.exit(1 if fails else 0)
