#!/usr/bin/env python3
"""lab/evolve/fuzz-designs.py LIST [--designs N] [--programs P] [--seed S] [--widths 8,4] [--out DIR] [--harsh] [--arm] - differential fuzzing:
random Forth programs run on designs and on the hand-made s6 at the same width, every difference in their output kept
(Iteration 707 - the ideation survey's item 3: the misaligned 2@ of 705 was found only because the Hayes corpus happens to
store a cell at an odd address; a generator finds such classes on purpose). LIST: one record a line (a candidates file,
a results file). N designs spread over LIST by speed, with tos 0 and 1, GCC and clang, the JIT and not among them, each
built by evolve.py as the run builds it (at 4-byte cells as eval32 does). Each program: a few definitions (constants,
variables, short words called from others - what the run-time compilers fuse and inline - loops, branches, a word called
again and again so the JIT translates it) and top-level lines printing the stack after each, over edge values (0, -1,
the cell's extremes, its sign bit), memory at aligned and odd offsets of a buffer, double-cell words. Not generated - the
ambiguous conditions of Forth 2012 whose C is undefined: a shift by the cell's width or more, a division by zero, the
most negative number divided by -1. Output compared as evolve.py compares it ("Redefining:" lines out). DIR: every
program that differed, with both outputs (default /tmp/fuzz). stdout: a line a design and the totals. As the build user."""
import json, os, random, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
A = sys.argv[1:]
def opt(name, default=None):
    if name not in A: return default
    i = A.index(name); v = A[i + 1]; del A[i:i + 2]; return v
ndes, nprog, seed = int(opt('--designs', '12')), int(opt('--programs', '40')), int(opt('--seed', '707'))
widths = [int(w) for w in opt('--widths', '8,4').split(',')]
outd = opt('--out', '/tmp/fuzz')
harsh = '--harsh' in A
if harsh: A.remove('--harsh')
arm = '--arm' in A            # 707: clang's ARMv7 builds under qemu-arm, against s6 at 4-byte cells (x86's)
if arm: A.remove('--arm'); widths = [4]
if len(A) != 1: sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths()
os.makedirs(outd, exist_ok=True)
clean = lambda b: re.sub(rb'(?m)^Redefining:[^\n]*\n', b'', b.replace(b'\r', b''))


class Gen:
    """A stack-safe random program: the depth tracked, every word's effect known."""
    BIN = ['+', '-', '*', 'AND', 'OR', 'XOR', 'MIN', 'MAX', '=', '<>', '<', '>', 'U<', 'U>']
    UN = ['NEGATE', 'INVERT', 'ABS', '1+', '1-', '2*', '2/', '0=', '0<', '0>', 'CELL+', 'CHAR+']   # the kernel's (707: no 0<> NIP TUCK -ROT .R)

    def __init__(self, rng, cell):
        self.r, self.cell, self.bits = rng, cell, cell * 8
        top = (1 << (self.bits - 1))
        self.edges = [0, 1, -1, 2, 3, 7, -7, 127, 128, 255, 256, -256, 65535, 65536, top - 1, -top, top // 2, 1000003, -99]

    def lit(self):
        return str(self.r.choice(self.edges) if self.r.random() < 0.6 else self.r.randint(-1000, 1000))

    def expr(self, depth, n):
        """n words that leave the depth >= 1 and end with depth + 1 on the stack - a straight-line expression."""
        out, d = [], depth
        while len(out) < n or d < depth + 1:
            c = self.r.random()
            if d - depth < 2 or c < 0.3: out.append(self.lit()); d += 1
            elif c < 0.55: out.append(self.r.choice(self.BIN)); d -= 1
            elif c < 0.7: out.append(self.r.choice(self.UN))
            elif c < 0.78: out.append(self.r.choice(['DUP', 'OVER'])); d += 1
            elif c < 0.86: out.append(self.r.choice(['SWAP', 'ROT', 'ROT ROT', '2DUP DROP']) if d - depth >= 3 else 'SWAP'); d += out[-1] == '2DUP DROP'
            elif c < 0.9: out.append(str(self.r.randint(0, self.bits - 1))); out.append(self.r.choice(['LSHIFT', 'RSHIFT']))
            elif c < 0.95: out.append(self.r.choice(['1', '3', '7', '-5', '1000'])); out.append(self.r.choice(['/', 'MOD']))
            else: out.append('DROP'); d -= 1
            if d - depth > 6:
                out.append(self.r.choice(self.BIN)); d -= 1
            if len(out) > 4 * n: break
        while d > depth + 1: out.append(self.r.choice(self.BIN)); d -= 1
        return out

    def program(self):
        r = self.r; L = ['DECIMAL', 'CREATE BUF 64 ALLOT  BUF 64 0 FILL', 'VARIABLE V  0 V !', '%s CONSTANT K' % self.lit(),
                         '%s CONSTANT K2' % self.lit(), ': SQ DUP * ;', ': CUBE DUP SQ * ;', ': K+ K + ;', ': V+! V +! ;']
        words = []
        for i in range(r.randint(2, 5)):
            body = self.expr(1, r.randint(2, 7)) + ['SWAP', 'DROP']      # ( x -- y ): the expression over x, then x dropped
            body = [w if r.random() > 0.15 else r.choice(['SQ', 'K+', 'V @ +', 'K2 XOR']) + ' ' + w if w in self.BIN else w for w in body]
            kind = r.random()
            if kind < 0.25: body = ['DUP', '0<', 'IF', 'NEGATE', 'ELSE', '1+', 'THEN'] + body     # ( x -- x' )
            elif kind < 0.45: body = ['%d' % r.randint(1, 9), '0', 'DO', 'I', '+', 'LOOP'] + body
            elif kind < 0.55: body = ['%d' % r.randint(1, 6), 'BEGIN', '1-', 'DUP', '0=', 'UNTIL', 'DROP'] + body   # ( -- ), bounded
            name = 'F%d' % i; L.append(': %s %s ;' % (name, ' '.join(body))); words.append(name)
        for _ in range(r.randint(6, 14)):
            c = r.random()
            if c < 0.45:
                e = self.expr(0, r.randint(3, 10))
                if words and r.random() < 0.7: e = e + [r.choice(words)]
                L.append(' '.join(e) + ' .')
            elif c < 0.6 and words:
                w = r.choice(words)   # called again and again: the JIT translates it, the counters move
                L.append('0 %d 0 DO I %s + LOOP .' % (r.randint(3, 40), w))
            elif c < 0.8:
                off = r.randint(0, 40)          # aligned and odd offsets of BUF: @ ! C@ C! +! 2@ 2!
                op = r.choice(['! BUF %d + @ .', 'C! BUF %d + C@ .', 'BUF %d + +! BUF %d + @ .', '2!2@'])
                if op == '2!2@': L.append('%s %s BUF %d + 2! BUF %d + 2@ . .' % (self.lit(), self.lit(), off, off))
                elif op.startswith('BUF'): L.append('%s %s' % (self.lit(), op % (off, off)))
                else: L.append('%s BUF %d + %s' % (self.lit(), off, op % off))
            elif c < 0.9:
                a, b = self.lit(), self.lit()
                L.append(r.choice(['%s %s UM* D. ' % (a, b), '%s %s M* D.' % (a, b), '%s %s 2DUP D+ D.' % (a, b),
                                   '%s 0 7 UM/MOD . .' % a, '%s %s 2DUP 2SWAP 2DROP . .' % (a, b), '%s %s 3 */ .' % (a, b)]))
            else:
                L.append('%s V+! V @ .  K . K2 . %s CUBE .' % (self.lit(), self.lit()))
        if self.harsh: L += self.harsh_lines(words)
        L.append('DEPTH .')
        return '\n'.join(L) + '\n'

    harsh = False
    def harsh_lines(self, words):
        """707's second pass: what the run-time compilers and the JIT treat apart - EXIT and LEAVE out of loops,
        RECURSE, the return stack, EXECUTE through a variable whose word changes (the inline cache's hit and miss),
        J, BEGIN WHILE REPEAT, signed and unsigned double division, overlapping CMOVE and MOVE, HEX output."""
        r = self.r; L = []
        L.append(': FACT DUP 2 < IF DROP 1 EXIT THEN DUP 1- RECURSE * ;')
        L.append(': FIND3 ( n -- i ) -1 SWAP 0 DO I 3 = IF DROP I LEAVE THEN LOOP ;')
        L.append(': RSUM ( a b -- a+b ) >R R@ + R> DROP ;')
        L.append(': NEST 0 4 0 DO 3 0 DO I J * + LOOP LOOP + ;')
        L.append(': WH ( n -- m ) 0 SWAP BEGIN DUP 0> WHILE SWAP 1+ SWAP 2/ REPEAT DROP ;')
        L.append('VARIABLE XT')
        L.append(': CALLX ( x -- y ) XT @ EXECUTE ;')
        for _ in range(r.randint(8, 16)):
            c = r.random()
            if c < 0.12: L.append('%d FACT .' % r.randint(0, 20))
            elif c < 0.22: L.append('%d FIND3 .  %s %s RSUM .' % (r.randint(0, 8), self.lit(), self.lit()))
            elif c < 0.3: L.append('%s NEST .  %s WH .' % (self.lit(), str(r.randint(-5, 100000))))
            elif c < 0.45 and words:
                ws = r.sample(words, min(len(words), 2))
                L.append(" ".join("' %s XT !  0 %d 0 DO I CALLX + LOOP ." % (w, r.randint(2, 30)) for w in ws))
            elif c < 0.6:
                a, d = self.lit(), r.choice(['3', '7', '-5', '1000', '-1000'])
                L.append(r.choice(['%s DUP 0< %s FM/MOD . .' % (a, d), '%s DUP 0< %s SM/REM . .' % (a, d),
                                   '%s 0 %s UM/MOD . .' % (a, d.lstrip('-')), '%s %s %s */MOD . .' % (a, self.lit(), d)]))
            elif c < 0.72:
                o1, o2, n = r.randint(0, 20), r.randint(0, 20), r.randint(0, 20)
                L.append('BUF 64 0 FILL  %d 0 DO I 7 * BUF I + C! LOOP  BUF %d + BUF %d + %d %s  BUF %d + C@ . BUF %d + C@ .'
                         % (40, o1, o2, n, r.choice(['CMOVE', 'MOVE', 'CMOVE>']) if False else r.choice(['CMOVE', 'MOVE']), o2, o2 + max(0, n - 1)))
            elif c < 0.82: L.append('HEX %s . %s U. DECIMAL' % (self.lit(), self.lit()))
            elif c < 0.9: L.append('%s %s %s %s 2OVER 2SWAP . . . . . .' % (self.lit(), self.lit(), self.lit(), self.lit()))
            else: L.append('%s %s %s 2 PICK . . . .' % (self.lit(), self.lit(), self.lit()))
        return L


recs = [json.loads(l) for l in open(A[0]) if l.startswith('{"') and '"genome": {' in l]
recs.sort(key=lambda r: r.get('speed') or 9)
pick, seen = [], set()
for r in recs:      # spread: each (tos, compiler, jit) class once first, then by speed
    x = E.express(E.canon(dict(r['genome'])))
    k = (bool(x.get('tos')), bool(x.get('compiler')), bool(x.get('jit')))
    if k not in seen: seen.add(k); pick.append(r)
rest = [r for r in recs if r not in pick]
step = max(1, len(rest) // max(1, ndes - len(pick)))
pick += rest[::step][:max(0, ndes - len(pick))]

tot = dict(runs=0, differ=0)
for cell in widths:
    rng = random.Random(seed * 10 + cell); G = Gen(rng, cell)
    G.harsh = harsh
    progs = [G.program() for _ in range(nprog)]
    ctx = E.at_width(E.WIDTH4) if cell == 4 else __import__('contextlib').nullcontext()
    with ctx:
        s6 = E.canon(dict(E.HUMAN['s6-cv8b'])); d = os.path.join(E.EV, 'fz-s6-%d' % cell)
        se, si = E.build(s6, d); sp = E.private_work(d)
        ref = [clean(E.sh([se, si], cwd=sp, inp=p.encode(), timeout=60, cpu=20).stdout) for p in progs]
        for r in pick[:ndes]:
            g = dict(r['genome'])
            if cell == 4 and (g.get('scale') or 0) > 2: g['scale'] = 2
            g = E.canon(g); dd = os.path.join(E.EV, 'fz-%s-%d' % (r['id'], cell))
            x = E.express(g)
            tag = '%s %d-byte tos=%d %s%s' % (r['id'], cell, bool(x.get('tos')), 'clang' if x.get('compiler') else 'GCC', ' JIT' if x.get('jit') else '')
            if arm and (x.get('jit') or not x.get('compiler') or x.get('enc', 'cv8') != 'cv8'): continue   # the laptop cross-builds clang's
            if arm: os.environ['EVOLVE_TARGET'] = 'armv7'; dd += '-arm'; tag += ' ARMv7'
            try: eng, img = E.build(g, dd); pw = E.private_work(dd)
            except Exception as e: print('%s: did not build - %s' % (tag, str(e)[:80]), flush=True); continue
            finally: os.environ.pop('EVOLVE_TARGET', None)
            bad = []
            for k, p in enumerate(progs):
                try: o = clean(subprocess.run(['qemu-arm', eng, img], cwd=pw, input=p.encode(), capture_output=True, timeout=240).stdout
                               if arm else E.sh([eng, img], cwd=pw, inp=p.encode(), timeout=60, cpu=20).stdout)
                except Exception as e: o = b'(raised: %s)' % str(e)[:60].encode()
                tot['runs'] += 1
                if o != ref[k]:
                    bad.append(k); tot['differ'] += 1
                    f = os.path.join(outd, '%s-%d-p%d' % (r['id'], cell, k))
                    open(f + '.fth', 'w').write(p); open(f + '.got', 'wb').write(o); open(f + '.s6', 'wb').write(ref[k])
            print('%s: %d of %d programs differ%s' % (tag, len(bad), len(progs), (' - p' + ', p'.join(map(str, bad[:8]))) if bad else ''), flush=True)
print('fuzz-designs: %d runs, %d differ from s6; the programs that did in %s' % (tot['runs'], tot['differ'], outd))
