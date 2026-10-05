#!/usr/bin/env python3
"""regprice.py ID|s6 [ID ...] [--db FILE] - the register machine's first
stage, priced by counting (Iteration 32).

stackops.py bounded what a register machine could remove: every dispatch
that only moves a value or pushes a lone literal - 38-50%. This prices the
first stage GOALS.md plans - register forms within a block, the stack
synchronised at calls, returns and branches - for one buildable design:

  * a run of data-stack moves (DUP DROP SWAP OVER ROT 2DUP 2DROP, and pairs
    of them) followed, in the same block, by an operation that takes
    operands, is ABSORBED: the operation gets a descriptor naming its
    operand slots and the stack the moves would have left - if the run
    reaches no deeper than the top four items; deeper, it is collapsed;
  * a run ending anywhere else - a call, an exit, a branch, a literal, a
    return-stack read - is COLLAPSED into one shuffle instruction with a
    descriptor: the stack must be real there;
  * a lone literal directly before a two-operand operation becomes an
    immediate operand.

Blocks: the operations of a word body in address order (tools/layout.py's
CALLMAP), split where the executed count changes and after control flow.
Counts: the profiler's executions per address, on every workload - the
same on every machine. A pair is one dispatch: its first part carries it,
so what pairs already save is not counted again. Unknown operation kinds
end a block - the price errs low.

Coverage: code compiled at run time - fib's FIB, the loop's loops - has no
CALLMAP and is not priced; each row says what share of the executed
dispatches the image's own code is.

Size: an absorbed move removes its byte, an absorbing operation gains a
descriptor byte; a collapsed run of n moves becomes 2 bytes; an absorbed
literal saves its opcode byte.
"""
import collections, json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; db = os.path.join(HERE, '..', '..', 'build', 'evolve', 'db.jsonl')
if '--db' in args: i = args.index('--db'); db = args[i + 1]; del args[i:i + 2]
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
recs = {}
if os.path.exists(db):
    for l in open(db):
        try: r = json.loads(l); recs[r['id']] = r
        except ValueError: pass
prims = [l.split()[1] for l in open(os.path.join(E.ROOT, 'forth', 'kernel.4')) if l.startswith('PRIMITIVE')]
src = open(os.path.join(E.ROOT, 'engine', 'vm-lab.c')).read()
band = src[src.index('#if ENC == 3 && SPEC\n        [0x60]'):]; band = band[:band.index('#endif')]
SPECBAND = {0x60 + k: n for k, n in enumerate(re.findall(r'&&L_(\w+)', band))}
FIXED = {68: 'LIT32', 69: 'DOVAR', 70: 'DODOES', 71: 'LIT8', 72: 'LIT8X', 0x7C: 'LIT64', 0x7D: 'ESC'}
MOVE = {'DUP', 'DROP', 'SWAP', 'OVER', 'ROT', '2dup', '2drop'}
LITS = {'LIT', 'LIT8', 'LIT32', 'LIT64', 'lit0', 'lit1', 'litm1'}
BINARY = {'+', 'AND', 'OR', 'XOR', '=', '<', 'U<', 'LSHIFT', 'RSHIFT', '!', 'C!', 'sub', 'ne', 'sgt', '+!', 'UM*', '-', '>'}
USE = BINARY | {'@', 'C@', 'NEGATE', 'zeq', 'zlt', 'onep', 'onem', 'cellp', 'charp', 'cells', 'invert', 'count', 'aligned',
                '>R', 'EXECUTE', '?DUP', 'D+', 'UM/MOD', '0=', '0<', 'INVERT', '1+', '1-', 'CELL+', 'CELLS',
                'addi', 'eqi', '?BRANCH'}            # immediates, and every test-and-branch: it reads the flag or operands
RMOVE = {'>R', 'R>', 'R@', 'I', 'J', 'UNLOOP'}       # return-stack moves: not absorbed in this stage, only counted
TESTBR = {'QBR', 'QBRS', 'NQBR', 'NQBRS', 'LTQBR', 'LTQBRS', 'EQQBR', 'EQQBRS', 'ULTQBR', 'ULTQBRS',
          'NEQBR', 'NEQBRS', 'SGTQBR', 'SGTQBRS', 'ZLTQBR', 'ZLTQBRS'}
USE |= {'?BRANCH:' + k for k in TESTBR}
PRODUCE = {'R>', 'R@', 'I', 'J', 'DOVAR'} | LITS          # push without reading the stack: end a run
WORKS = E.WORK_SEL + E.WORK_HELD

def window(run):            # deepest original slot a run of moves touches (0 = the top)
    st = list(range(8)); deep = 0
    def need(k):
        nonlocal deep
        deep = max(deep, st[k] if k < len(st) else 99)
    for m in run:
        if m == 'DUP': need(0); st.insert(0, st[0])
        elif m == 'DROP': need(0); st.pop(0)
        elif m == 'SWAP': need(0); need(1); st[0], st[1] = st[1], st[0]
        elif m == 'OVER': need(1); st.insert(0, st[1])
        elif m == 'ROT': need(2); st.insert(0, st.pop(2))
        elif m == '2dup': need(1); st[0:0] = st[0:2]
        elif m == '2drop': need(1); del st[0:2]
    return deep

def design(did):
    if did == 's6': return 's6', E.canon(E.HUMAN['s6-cv8b'])
    if did not in recs: sys.exit('no design %s in %s' % (did, db))
    return did, E.canon(recs[did]['genome'])

for did in args:
    did, g = design(did)
    sup = {op: (a, b) for a, b, op in E.supers_in(g)}
    o10 = {op: w for w, op in E.ops10_in(g)}
    folds = g['folds'] if g.get('fold') else []
    def name(op):
        if op in sup: return sup[op]
        if op in o10: return (o10[op],)
        if op >= 128: return ('call',)
        if op in FIXED: return (FIXED[op],)
        if 73 <= op < 73 + len(folds): return (folds[op - 73] + ';EXIT',)
        if g.get('escape') == 2: i = op if op < 27 else None
        elif g.get('escape'): i = op if op < 32 else op + 1 if op < 36 else None
        else: i = op if op < 68 else None
        if i is not None and i < len(prims): return (prims[i],)
        return (SPECBAND.get(op, 'op%d' % op),)
    d = os.path.join(E.EV, 'regprice'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    cm = os.path.join(d, 'callmap'); os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False; del os.environ['CALLMAP']
    ops, kinds = [], collections.Counter()
    for l in open(cm):
        f = l.split()
        if f[0] == 'O':
            k = f[2]; kinds[k] += 1
            if k in ('P', 'LIT', 'SP'): comps = name(int(f[3]))          # SP: a pair, named by its opcode
            elif k in ('ADDI', 'EQI', 'EQIH'): comps = ('addi',) if k == 'ADDI' else ('eqi',)
            elif k == 'VF': comps = ('DOVAR',)            # pushes a variable's value: a producer
            elif k == 'VS': comps = ('!',)                # stores the top: a use
            elif k in TESTBR: comps = ('?BRANCH:' + k,)       # the kind kept: DUP ?BRANCH is not DUP 0= ?BRANCH (Iteration 33)
            else: comps = (k,)                            # BR, PX, LITX, ADDIX, EQIX and anything new: an end
            ops.append((int(f[1]), comps))
        elif f[0] == 'C': ops.append((int(f[1]), ('call',)))
    ops.sort()
    pw = E.private_work(d)
    print('## %s - %s bytes; operation kinds %s\n' % (did, format(recs[did]['size'], ',') if did in recs else 's6',
          ' '.join('%s %d' % kv for kv in sorted(kinds.items()))))
    print('| workload | dispatches in the image\'s code | of all executed | absorbed runs | collapsed runs | literals | saved | runs deeper than 4 | return-stack moves, not absorbed |')
    print('|---|---|---|---|---|---|---|---|---|')
    static_done = False; tops = []
    for w in WORKS:
        pf = os.path.join(d, 'prof-' + w)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=10, env=dict(os.environ, VMPROF=pf))
        ipc = collections.Counter()
        for line in open(pf):
            f = line.split()
            if f[0] == 'I': ipc[int(f[1])] += int(f[2])
        total = sum(ipc[o] for o, _ in ops); everything = sum(ipc.values())
        absorbed = collapsed = lits = deep = 0
        pat = collections.Counter()    # what is absorbed: (moves..., the operation) -> dispatches saved
        rmoves = sum(ipc[o] for o, cs in ops if all(c in RMOVE | MOVE for c in cs) and any(c in RMOVE for c in cs))
        sbytes = 0                      # static: bytes saved (+) or added (-), every operation once
        i = 0
        while i < len(ops):
            o, comps = ops[i]; n = ipc[o]
            # the parts of this operation, each with the dispatch it carries (a pair: the first)
            if all(c in MOVE for c in comps):
                run, j = [], i
                while j < len(ops) and all(c in MOVE for c in ops[j][1]) and ipc[ops[j][0]] == n:
                    run.append(ops[j]); j += 1
                moves = [c for _, cs in run for c in cs]
                disp = len(run)          # dispatches the run costs now
                nxt = ops[j][1] if j < len(ops) and ipc[ops[j][0]] == n else ('end',)
                use = any(c in USE for c in nxt) and not any(c in PRODUCE for c in nxt)
                if use and window(moves) <= 3:
                    absorbed += disp * n; sbytes += (disp - 1) if n else 0
                    pat[' '.join(moves) + ' | ' + ' '.join(nxt)] += disp * n
                else:
                    if window(moves) > 3 and use: deep += disp * n
                    if disp > 1: collapsed += (disp - 1) * n; sbytes += (disp - 2) if n else 0
                i = j; continue
            if comps[0] in LITS and len(comps) == 1 and i + 1 < len(ops) and ipc[ops[i + 1][0]] == n and ops[i + 1][1][0] in BINARY:
                lits += n; sbytes += 1 if n else 0
            i += 1
        s = absorbed + collapsed + lits
        print('| %s | %d | %.0f%% | %.1f%% | %.1f%% | %.1f%% | **%.1f%%** | %.1f%% | %.1f%% |' % (w, total, 100 * total / everything, 100 * absorbed / total, 100 * collapsed / total,
              100 * lits / total, 100 * s / total, 100 * deep / total, 100 * rmoves / total))
        if not static_done: static_bytes = sbytes; static_done = True
        if pat:
            tops.append('%s: %s' % (w, ', '.join('%s %.1f%%' % (pp, 100 * v / total) for pp, v in pat.most_common(5))))
        if w == 'kernel' and pat:
            tot = sum(pat.values()); acc = 0; k80 = 0
            for k, (pp, v) in enumerate(pat.most_common()):
                acc += v
                if acc >= 0.8 * tot: k80 = k + 1; break
            patterns = (len(pat), k80, ', '.join('%s (%.1f%%)' % (pp, 100 * v / total) for pp, v in pat.most_common(8)))
    print('\nthe largest absorbed patterns, as shares of each workload\'s image-code dispatches:\n' + '\n'.join('- ' + t for t in tops))
    print('\nkernel: %d distinct absorbed patterns; %d of them give 80%% of the absorbed saving. The largest: %s' % patterns)
    print('\nstatic: the image\'s code %+d bytes (a run absorbed or collapsed, a literal made immediate, wherever it was executed on the first workload)\n' % -static_bytes)
    shutil.rmtree(d, ignore_errors=True)
