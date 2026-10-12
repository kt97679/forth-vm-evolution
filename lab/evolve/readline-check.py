#!/usr/bin/env python3
"""readline-check.py [ID ...] - READ-LINE at every single-SYSCALL level against
native (Iteration 214).

fsys 3 and 4 read a line into the caller's buffer and seek back; fsys 5
reads 4 KB ahead where a file can seek and copies lines out of its own
buffer, giving back what it read ahead before any other use of the file.
Each design (default: seed 42's smallest, whose CMOVE is native and SCAN a
loop, and its best by Q, the other way round) is built at fsys 0 (native
I/O: the reference), 3, 4 and 5, and one program run on each - every
result printed: u2, flag, ior and the line between bars. Byte for byte as
native, or the check fails. The program reads:

  lines of every kind - empty, CR LF, a lone CR, no LF at the end - with
    room for them and with room for 10 characters (a line cut, the rest
    next time; an LF just past the room);
  a 10 KB file whose lines cross the 4 KB read-ahead (a CR at its last
    byte, the LF at the next block's first) and a line longer than it;
  FILE-POSITION, REPOSITION-FILE, READ-FILE and FILE-SIZE between lines -
    each must see the position of the lines read, not of the read-ahead;
  WRITE-LINE after a line on a file opened R/W - it must land right after
    the line: judged by the file's bytes, at every level, native included
    (native's WRITE-LINE gave back nothing it had read ahead until Iteration
    225, and wrote past its 4 KB read);
  two files read in turn; a descriptor closed and its number used again
    by another file; u1 = 0; the end of a file met again and again;
  INCLUDED nested two deep;
  a pipe opened as a file (/dev/stdin: the program's own input) - a line
    taken from it must leave the next one to the interpreter: no
    read-ahead where a file cannot seek (the owner's rule).

And READ, the interpreter's own input, from a stdin that is a file (Iteration
226): fsys 3-5's READ reads a block there and gives back what follows the
first editing character - CR LF lines, a backspace and a delete inside a line,
a line longer than ACCEPT's room, KEY, and no newline at the end - every
level byte for byte as native, which reads a block and gives back too.
"""
import os, sys, shutil, subprocess, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; sys.argv = ['evolve.py']
spec = importlib.util.spec_from_file_location('E', os.path.join(HERE, 'evolve.py')); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
E.setup()
IDS = args or ['be1620e346', '9a3de58ebe']
LEVELS = (0, 3, 4, 5)

def files(pw):
    """The test files, written into the work directory (it holds links to
    the shared ones: replace, never write through)."""
    def put(name, data):
        p = os.path.join(pw, name)
        if os.path.lexists(p): os.remove(p)
        open(p, 'wb').write(data)
    put('rl1.txt', b'alpha\n\nbeta\r\n\r\nlone\rcr\n'
                   b'a line that is longer than the small room\n'
                   b'exactly10!\nx\nno newline at the end')
    big, n = bytearray(), 0
    while len(big) < 10000:                      # lines of 0 to 96 characters
        k = n * 37 % 97; big += bytes(48 + (n + i) % 75 for i in range(k)) + b'\n'; n += 1
        if 4060 < len(big) < 4096: big += b'y' * (4095 - len(big)) + b'\r\n'   # a CR at 4095, the LF at 4096
    put('rl2.txt', bytes(big))
    put('rl3.txt', b'short\n' + b'L' * 5000 + b'\nafter the long one\n')
    put('rl4.txt', b'first\nsecond line\nthird\n')
    put('rl-inc1.fth', b'S" in1-a" TYPE CR\nS" rl-inc2.fth" INCLUDED\nS" in1-b" TYPE CR\n')
    put('rl-inc2.fth', b'S" in2" TYPE CR\n')

PROG = r'''
CREATE BUF 8200 ALLOT  VARIABLE F  VARIABLE G  CREATE P 2 CELLS ALLOT
: SHOW ( u2 flag ior -- )  . . DUP . 124 EMIT BUF SWAP TYPE 124 EMIT CR ;
: RL ( u1 fid -- )  BUF ROT ROT READ-LINE SHOW ;
: ALL ( u1 fid -- )  BEGIN 2DUP BUF ROT ROT READ-LINE DUP >R OVER >R SHOW R> R> 0= AND 0= UNTIL 2DROP ;
S" rl1.txt" R/O OPEN-FILE . F !  200 F @ ALL  F @ CLOSE-FILE . CR
S" rl1.txt" R/O OPEN-FILE . F !  10 F @ ALL  F @ CLOSE-FILE . CR
S" rl2.txt" R/O OPEN-FILE . F !  200 F @ ALL  F @ CLOSE-FILE . CR
S" rl2.txt" R/O OPEN-FILE . F !  200 F @ RL 200 F @ RL 200 F @ RL
F @ FILE-POSITION . P 2!  P 2@ D. CR  200 F @ RL
P 2@ F @ REPOSITION-FILE . CR  200 F @ RL
BUF 10 F @ READ-FILE . DUP . 124 EMIT BUF SWAP TYPE 124 EMIT CR  200 F @ RL
F @ FILE-SIZE . D. CR  200 F @ RL  F @ FILE-POSITION . D. CR  F @ CLOSE-FILE . CR
S" rl1.txt" R/O OPEN-FILE . F !  S" rl2.txt" R/O OPEN-FILE . G !
200 F @ RL 200 G @ RL 200 F @ RL 200 G @ RL 200 F @ RL 200 G @ RL  F @ CLOSE-FILE . G @ CLOSE-FILE . CR
S" rl1.txt" R/O OPEN-FILE . F !  200 F @ RL  F @ CLOSE-FILE .
S" rl4.txt" R/O OPEN-FILE . F !  200 F @ RL  200 F @ RL  F @ CLOSE-FILE . CR
S" rl1.txt" R/O OPEN-FILE . F !  0 F @ RL  200 F @ RL  0 F @ RL
200 F @ ALL  200 F @ RL  200 F @ RL  F @ CLOSE-FILE . CR
S" rl3.txt" R/O OPEN-FILE . F !  6000 F @ RL  4096 F @ RL  200 F @ RL  6000 F @ ALL  F @ CLOSE-FILE . CR
S" rl-inc1.fth" INCLUDED
S" /dev/stdin" R/O OPEN-FILE . G !  200 G @ RL
this line is data, taken through /dev/stdin
S" back" TYPE CR  200 G @ RL
a second line of data
G @ CLOSE-FILE . CR  S" end" TYPE CR
BYE
'''

WPROG = r'''
CREATE BUF 200 ALLOT  VARIABLE F
S" rl4.txt" R/W OPEN-FILE . F !  BUF 200 F @ READ-LINE . . .  S" XX" F @ WRITE-LINE .  F @ CLOSE-FILE .
BYE
'''
WANT = b'first\nXX\nond line\nthird\n'          # "XX" and its LF over "sec": right after the first line
STDIN = (b'S" crlf" TYPE CR\r\n1 2 + . CR\r\n'
         b'S" bacX\x08k" TYPE CR\n'
         b'S" delY\x7fete" TYPE CR\n'
         b': L 0 ; ' + b'S" ' + b'x' * 300 + b'" 2DROP S" long" TYPE CR\n'
         b'KEY EMIT Q CR\n'
         b'S" end" TYPE')                                # no newline at the end

fails = 0
for did in IDS:
    g0 = E.recorded_genome(did)
    if g0 is None: sys.exit('no design %s in results/' % did)
    out, wrote, fromfile = {}, {}, {}
    for v in LEVELS:
        g = dict(g0); g.pop('fsys', None)
        if v: g['fsys'] = v
        d = os.path.join(E.EV, 'readline-%d' % v); shutil.rmtree(d, ignore_errors=True)
        eng, img = E.build(E.canon(g), d); pw = E.private_work(d); files(pw)
        r = subprocess.run([eng, img], cwd=pw, input=PROG.encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        out[v] = (r.returncode, r.stdout)
        open(os.path.join(E.EV, 'readline-%s-%d.out' % (did, v)), 'wb').write(r.stdout)   # kept, to look at
        files(pw)
        subprocess.run([eng, img], cwd=pw, input=WPROG.encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
        wrote[v] = open(os.path.join(pw, 'rl4.txt'), 'rb').read()
        sf = os.path.join(pw, 'rl-stdin.txt'); open(sf, 'wb').write(STDIN)
        with open(sf, 'rb') as fin:                      # a stdin that seeks
            r = subprocess.run([eng, img], cwd=pw, stdin=fin, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
        fromfile[v] = (r.returncode, r.stdout)
        shutil.rmtree(d, ignore_errors=True)
    ref = out[0]
    lines = ref[1].count(b'\n')
    sane = ref[0] == 0 and b'\nend' in ref[1] and b'this line is data' in ref[1] and b'in2' in ref[1] and lines > 250
    fails += not sane
    print('## %s - native: status %d, %d bytes, %d lines%s' % (did, ref[0], len(ref[1]), lines, '' if sane else ' - NOT AS EXPECTED: the program did not run through'))
    for v in LEVELS[1:]:
        same = out[v] == ref
        fails += not same
        if same: print('- fsys %d: as native' % v)
        else:
            a, b = ref[1].split(b'\n'), out[v][1].split(b'\n')
            i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
            print('- fsys %d: DIFFERS (status %d) - line %d: native %r, fsys %d %r' % (v, out[v][0], i + 1,
                  a[i][:100] if i < len(a) else b'<none>', v, b[i][:100] if i < len(b) else b'<none>'))
    for v in LEVELS:
        fails += wrote[v] != WANT
    same = [v for v in LEVELS[1:] if fromfile[v] == fromfile[0]]
    fails += len(same) != len(LEVELS) - 1
    print('- READ from a stdin that is a file (%d bytes out, status %d): %s' % (len(fromfile[0][1]), fromfile[0][0],
          'fsys %s as native' % ', '.join(map(str, same)) if len(same) == len(LEVELS) - 1 else
          'DIFFERS at fsys %s: native %r, %r' % (', '.join(str(v) for v in LEVELS[1:] if v not in same), fromfile[0][1][-120:],
                                                 [fromfile[v][1][-120:] for v in LEVELS[1:] if v not in same][0])))
    print('- WRITE-LINE after a line (R/W): %s; native %s' % (
          'fsys %s right after the line' % ', '.join(str(v) for v in LEVELS[1:] if wrote[v] == WANT) if all(wrote[v] == WANT for v in LEVELS[1:])
          else 'WRONG at fsys %s: %r' % (', '.join(str(v) for v in LEVELS[1:] if wrote[v] != WANT), [wrote[v] for v in LEVELS[1:] if wrote[v] != WANT][0]),
          'right after the line too' if wrote[0] == WANT else 'WRONG - elsewhere (its read-ahead not given back): %r' % wrote[0]))
print('\n%s' % ('PASS' if not fails else 'FAIL - %d' % fails))
sys.exit(1 if fails else 0)
