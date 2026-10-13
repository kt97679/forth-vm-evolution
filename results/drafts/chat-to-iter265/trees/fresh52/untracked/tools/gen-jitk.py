#!/usr/bin/env python3
"""gen-jitk.py K OUTDIR - the JIT's stack-cache stencils, for the gene jitk
(Iteration 259; results/price-jit-stack.md for the design, lab/evolve/
jitvariants.py for its first pricing).

Static stack caching in the copied code, as Ertl & Gregg's for interpreters and
CPython 3.15's JIT: the cache state c is how many of the top cells are in
registers, 0..K, always the same registers - the top in the second argument
register, the next in the third, the third in the fourth (sp stays in the
first) - so state 1 is today's (sp, tos), and every stencil without a variant
runs in it. Each hot data operation gets one stencil per input state: it loads
from memory the inputs not cached, computes, keeps at most K cells (the deepest
sent to memory) and continues in the state that leaves. A canonicaliser per
state brings any state back to 1 - before every stencil without a variant
(control, calls, loops, exits) and at branch targets, so every join and every
call sees state 1.

Writes OUTDIR/spn-jitk.inc (the stencils and spn_ktable[], included at the end
of engine/spn-stencils.c) and OUTDIR/jitk-map.h (for engine/jit.c: each base
stencil's variant per state, the state each variant leaves, the
canonicalisers), both under JITK=K.
"""
import os, sys

if len(sys.argv) != 3: sys.exit(__doc__)
K, OUT = int(sys.argv[1]), sys.argv[2]
assert 2 <= K <= 3, 'K is 2 or 3'

# the base stencil, its inputs (top first) and outputs - engine/spn-stencils.c's semantics exactly
OPS = [
    ('S_LIT',    'lit',    0, lambda: ['IMM()']),
    ('S_DUP',    'dup',    1, lambda a: [a, a]),
    ('S_DROP',   'drop',   1, lambda a: []),
    ('S_SWAP',   'swap',   2, lambda a, b: [b, a]),
    ('S_OVER',   'over',   2, lambda a, b: [b, a, b]),
    ('S_PLUS',   'plus',   2, lambda a, b: ['(%s + %s)' % (b, a)]),
    ('S_ADDI',   'addi',   1, lambda a: ['(%s + IMM())' % a]),
    ('S_EQ',     'eq',     2, lambda a, b: ['-(cell)(%s == %s)' % (b, a)]),
    ('S_GT',     'gt',     2, lambda a, b: ['-(cell)(%s > %s)' % (b, a)]),
    ('S_LT',     'lt',     2, lambda a, b: ['-(cell)(%s < %s)' % (b, a)]),
    ('S_AND',    'and',    2, lambda a, b: ['(%s & %s)' % (b, a)]),
    ('S_XOR',    'xor',    2, lambda a, b: ['(%s ^ %s)' % (b, a)]),
    ('S_FETCH',  'fetch',  1, lambda a: ['*(cell *)%s' % a]),
    ('S_STORE',  'store',  2, lambda a, b: ['@*(cell *)%s = %s;' % (a, b)]),
    ('S_CFETCH', 'cfetch', 1, lambda a: ['(cell)*(uint8_t *)%s' % a]),
    ('S_I',      'i',      0, lambda: ['@cell *rr_ = (cell *)*IMM_RP();', 'rr_[0]']),
]
REG = ['t0', 't1', 't2']

def variant(name, n_in, fn, c):
    """The C body of one stencil with c cells cached on entry, and the state it leaves."""
    body, cached = [], REG[:c]
    ins = list(cached[:n_in]); k = 0
    while len(ins) < n_in: body.append('cell m%d = *sp++;' % k); ins.append('m%d' % k); k += 1
    outs = fn(*ins)
    body += [o[1:] for o in outs if o.startswith('@')]
    vals = [o for o in outs if not o.startswith('@')]
    for i, v in enumerate(vals): body.append('cell v%d = %s;' % (i, v))
    new = ['v%d' % i for i in range(len(vals))] + cached[n_in:]
    while len(new) > K: body.append('*--sp = %s;' % new[-1]); new = new[:-1]
    passed = new + REG[len(new):]
    return 'SK(stk_%s_%d) { %s GO4(sp, %s); }' % (name, c, ' '.join(body), ', '.join(passed[:3])), len(new)

inc = ['/* gen-jitk.py %d - the stack-cache stencils (Iteration 259). Generated: do not edit. */' % K,
       'typedef spn_st (*spn_next4_fn)(cell *, cell, cell, cell);',
       '#define SK(name) __attribute__((noinline, used)) spn_st name(cell *sp, cell t0, cell t1, cell t2)',
       '/* the next stencil, the cached cells in the third and fourth argument registers: the JIT',
       '   finds this jump as it finds GO\'s - its target is exactly spn_next */',
       '#define GO4(sp, a, b, c) return ((spn_next4_fn)(void *)spn_next)(sp, a, b, c)']
table, vmap, vout = [], {}, []
for base, name, n_in, fn in OPS:
    for c in range(K + 1):
        src, out = variant(name, n_in, fn, c)
        inc.append(src); vmap[(base, c)] = len(table); table.append('stk_%s_%d' % (name, c)); vout.append(out)
canon = {}
for c in range(K + 1):
    if c == 1: continue
    if c == 0: inc.append('SK(stk_canon_0) { cell t = *sp++; GO4(sp, t, t1, t2); }')
    else: inc.append('SK(stk_canon_%d) { %s GO4(sp, t0, t1, t2); }' % (c, ' '.join('*--sp = %s;' % REG[i] for i in range(c - 1, 0, -1))))
    canon[c] = len(table); table.append('stk_canon_%d' % c); vout.append(1)
inc.append('const void *const spn_ktable[] = {\n    ' + ',\n    '.join('(const void *)%s' % t for t in table) + '\n};')
inc.append('const int spn_ktable_len = %d;' % len(table))
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'spn-jitk.inc'), 'w').write('\n'.join(inc) + '\n')

hdr = ['/* gen-jitk.py %d - the stack-cache map for engine/jit.c (Iteration 259). Generated. */' % K,
       '#define JITK_K %d' % K, '#define JITK_N %d' % len(table),
       'extern const void *const spn_ktable[];', 'extern const int spn_ktable_len;',
       '/* a base stencil\'s variant for each entry state, as index + 1 into spn_ktable (0: none) */',
       'static const unsigned char jitk_v1[S_N][JITK_K + 1] = {']
for base, name, n_in, fn in OPS:
    hdr.append('    [%s] = { %s },' % (base, ', '.join(str(vmap[(base, c)] + 1) for c in range(K + 1))))
hdr.append('};')
hdr.append('/* the state each variant leaves */')
hdr.append('static const unsigned char jitk_vout[JITK_N] = { %s };' % ', '.join(map(str, vout)))
hdr.append('/* the canonicaliser from each state to state 1, as index + 1 (0: none - state 1 itself) */')
hdr.append('static const unsigned char jitk_canon1[JITK_K + 1] = { %s };' % ', '.join(str(canon[c] + 1) if c in canon else '0' for c in range(K + 1)))
open(os.path.join(OUT, 'jitk-map.h'), 'w').write('\n'.join(hdr) + '\n')
print('gen-jitk: K=%d, %d stencils (%d operations x %d states, %d canonicalisers)' % (K, len(table), len(OPS), K + 1, len(canon)))
