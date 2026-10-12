#!/usr/bin/env python3
"""jitvariants.py [ID] [--k 2,3] [--out FILE] - what stack state in the JIT would
cost in engine bytes, priced by building its stencils (Iteration 219;
results/price-jit-stack.md).

The cheapest form (Ertl's static stack caching, as CPython 3.15's JIT): the
state is how many of the top cells are in registers, c = 0..K, always in the
same registers - the top in the second argument register, the next in the
third, the third in the fourth (%rsi, %rdx, %rcx; sp stays %rdi) - so state 1
is today's (sp, tos). Every data operation gets one stencil per input state:
it loads from memory the inputs that are not cached, computes, keeps at most K
cells (the deepest sent to memory) and continues in the state that leaves. A
literal stays a constant in the translator until an operation takes it: the
binary operations get an immediate variant per state. Control, calls and
loops keep today's stencils, in state 1, after a canonicalising stencil
(c -> 1). Shuffles are register moves here, not renames - fixed registers are
what keep the variants few.

Each variant is written in C as the stencils are (engine/spn-stencils.c's
rules: holes, markers, nothing PC-relative), compiled with a reference
design's compiler flags, and measured: bytes (as linked, and as the JIT copies
them), instructions, data-stack memory accesses. Writes the per-variant costs
as JSON for lab/evolve/jitstack.py --variants.
"""
import json, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
def opt(name, default=None):
    if name in args: i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return v
    return default
KS = [int(k) for k in opt('--k', '2,3').split(',')]
OUT = opt('--out', os.path.join(tempfile.gettempdir(), 'jitvariants.json'))
DID = args[0] if args else '28677d13b1'
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()

# top-first inputs a, b, c, d; outputs top first; 'imm' marks the constant-operand forms
OPS = {
    'lit': (0, lambda: ['IMM()']),
    'dup': (1, lambda a: [a, a]), 'drop': (1, lambda a: []), 'swap': (2, lambda a, b: [b, a]),
    'over': (2, lambda a, b: [b, a, b]), 'rot': (3, lambda a, b, c: [c, a, b]),
    'plus': (2, lambda a, b: ['(%s + %s)' % (b, a)]), 'xor': (2, lambda a, b: ['(%s ^ %s)' % (b, a)]),
    'and': (2, lambda a, b: ['(%s & %s)' % (b, a)]), 'or': (2, lambda a, b: ['(%s | %s)' % (b, a)]),
    'eq': (2, lambda a, b: ['-(cell)(%s == %s)' % (b, a)]), 'gt': (2, lambda a, b: ['-(cell)(%s > %s)' % (b, a)]),
    'lt': (2, lambda a, b: ['-(cell)(%s < %s)' % (b, a)]), 'ult': (2, lambda a, b: ['-(cell)((ucell)%s < (ucell)%s)' % (b, a)]),
    'lshift': (2, lambda a, b: ['(cell)((ucell)%s << %s)' % (b, a)]), 'rshift': (2, lambda a, b: ['(cell)((ucell)%s >> %s)' % (b, a)]),
    'negate': (1, lambda a: ['(-%s)' % a]), 'addi': (1, lambda a: ['(%s + IMM())' % a]), 'addi32': (1, lambda a: ['(%s + IMM32)' % a]),
    'fetch': (1, lambda a: ['*(cell *)%s' % a]), 'cfetch': (1, lambda a: ['(cell)*(unsigned char *)%s' % a]),
    'store': (2, lambda a, b: ['@*(cell *)%s = %s;' % (a, b)]), 'cstore': (2, lambda a, b: ['@*(unsigned char *)%s = (unsigned char)%s;' % (a, b)]),
    'tor': (1, lambda a: ['@{ ucell *rv = IMM_RP(); cell *r = (cell *)*rv; *--r = %s; *rv = (ucell)r; }' % a]),
    'fromr': (0, lambda: ['@ucell *rv = IMM_RP(); cell *r = (cell *)*rv; cell x = *r++; *rv = (ucell)r;', 'x']),
    'rfetch': (0, lambda: ['@cell *r = (cell *)*IMM_RP();', '*r']), 'i': (0, lambda: ['@cell *r = (cell *)*IMM_RP();', '*r']),
    'j': (0, lambda: ['@cell *r = (cell *)*IMM_RP();', 'r[2]']),
    'dplus': (4, lambda a, b, c, d: ['@ucell lo = (ucell)%s + (ucell)%s; cell hi = %s + %s + (lo < (ucell)%s);' % (d, b, c, a, d), 'hi', '(cell)lo']),
}
IMMOPS = {'plus_i': lambda b: ['(%s + IMM32)' % b], 'xor_i': lambda b: ['(%s ^ IMM32)' % b], 'and_i': lambda b: ['(%s & IMM32)' % b],
          'or_i': lambda b: ['(%s | IMM32)' % b], 'eq_i': lambda b: ['-(cell)(%s == IMM32)' % b], 'gt_i': lambda b: ['-(cell)(%s > IMM32)' % b],
          'lt_i': lambda b: ['-(cell)(%s < IMM32)' % b], 'ult_i': lambda b: ['-(cell)((ucell)%s < (ucell)IMM32)' % b]}
REG = ['t0', 't1', 't2']

def variant(name, n_in, fn, c, K):
    """The C body of one stencil: c cells cached on entry."""
    body, cached = [], REG[:c]
    ins = list(cached[:n_in]); k = 0
    while len(ins) < n_in: body.append('cell m%d = *sp++;' % k); ins.append('m%d' % k); k += 1
    outs = fn(*ins)
    stmts = [o[1:] for o in outs if o.startswith('@')]; vals = [o for o in outs if not o.startswith('@')]
    body += stmts
    vals = ['v%d' % i for i in range(len(vals))] if vals else []
    for i, v in enumerate([o for o in outs if not o.startswith('@')]): body.append('cell v%d = %s;' % (i, v))
    new = vals + cached[n_in:]
    while len(new) > K: body.append('*--sp = %s;' % new[-1]); new = new[:-1]
    passed = new + REG[len(new):]
    return 'V(st_%s_%d) { %s GO4(sp, %s); }' % (name, c, ' '.join(body), ', '.join(passed)), len(new)

def source(K):
    out = ['#include <stdint.h>', '#include "spn-abi.h"',
           '#define IMM() ({ cell _v; __asm__("movabs %1, %0" : "=r"(_v) : "i"(0x5ea1ed5ea1ed5ea1LL)); _v; })',
           '#define IMM32 0x3c1a5e77L',
           '#define IMM_RP() ({ ucell *_v; __asm__("movabs %1, %0" : "=r"(_v) : "i"(0x7ea1ed5ea1ed5e77LL)); _v; })',
           'extern spn_st spn_next4(cell *sp, cell t0, cell t1, cell t2);',
           '#define V(name) __attribute__((noinline, used)) spn_st name(cell *sp, cell t0, cell t1, cell t2)',
           '#define GO4(sp, a, b, c) return spn_next4(sp, a, b, c)']
    table = {}
    for c in range(K + 1):
        for name, (n_in, fn) in OPS.items():
            s, co = variant(name, n_in, fn, c, K); out.append(s); table['%s_%d' % (name, c)] = co
        for name, fn in IMMOPS.items():
            s, co = variant(name, 1, fn, c, K); out.append(s); table['%s_%d' % (name, c)] = co
    for c in range(K + 1):                                     # back to (sp, tos): state 1
        if c == 1: continue
        if c == 0: out.append('V(st_canon_0) { cell t = *sp++; GO4(sp, t, t1, t2); }')
        else: out.append('V(st_canon_%d) { %s GO4(sp, t0, t1, t2); }' % (c, ' '.join('*--sp = %s;' % REG[i] for i in range(c - 1, 0, -1))))
        table['canon_%d' % c] = 1
    return '\n'.join(out) + '\n', table

g = E.canon(E.recorded_genome(DID))
flags = E.ccflags(g)
d = tempfile.mkdtemp(prefix='jitvar-')
res = {'design': DID, 'flags': flags, 'K': {}}
for K in KS:
    src, table = source(K)
    cf = os.path.join(d, 'v%d.c' % K); of = os.path.join(d, 'v%d.o' % K)
    open(cf, 'w').write(src)
    r = subprocess.run(['cc'] + flags + ['-w', '-c', '-I', os.path.join(E.ROOT, 'engine'), '-o', of, cf], stderr=subprocess.PIPE, text=True)
    if r.returncode: sys.exit('compile failed: ' + r.stderr[-2000:])
    sizes = {}
    for l in subprocess.run(['nm', '-S', of], stdout=subprocess.PIPE, text=True).stdout.split('\n'):
        f = l.split()
        if len(f) == 4 and f[3].startswith('st_'): sizes[f[3]] = int(f[1], 16)
    dis = subprocess.run(['objdump', '-dr', '--no-show-raw-insn', of], stdout=subprocess.PIPE, text=True).stdout
    funcs, cur = {}, None
    for l in dis.split('\n'):
        m = re.match(r'^[0-9a-f]+ <(st_\w+)>:', l)
        if m: cur = m.group(1); funcs[cur] = []; continue
        if cur is None: continue
        if re.match(r'^\s+[0-9a-f]+:\s+R_X86_64', l):
            if funcs[cur] and 'spn_next4' in l: funcs[cur][-1] = funcs[cur][-1] + ' <next>'
            continue
        m = re.match(r'^\s+[0-9a-f]+:\s+(\S.*)$', l)
        if m and not m.group(1).startswith(('nop', 'xchg   %ax,%ax', 'cs nop', 'data16')): funcs[cur].append(m.group(1))
    per = {}
    for name, co in table.items():
        f = [i for i in funcs.get('st_' + name, []) if not i.startswith('endbr64')]
        tail = bool(f) and f[-1].startswith('jmp') and '<next>' in f[-1]
        if tail: f = f[:-1]
        size = sizes.get('st_' + name, 0)
        copied = size - (4 if funcs.get('st_' + name, [''])[0].startswith('endbr64') else 0) - (5 if tail else 0)
        per[name] = {'ins': len(f), 'mem': sum(1 for i in f if '(%rdi' in i), 'out': co, 'bytes': size, 'copied': copied,
                     'calls': sum(1 for i in f if i.startswith('call') or (i.startswith('jmp') and '<next>' not in i))}
    linked = sum(-(-v['bytes'] // 16) * 16 for v in per.values())
    res['K'][K] = {'variants': len(per), 'bytes': sum(v['bytes'] for v in per.values()), 'aligned16': linked,
                   'copied': sum(v['copied'] for v in per.values()), 'per': per}
    print('K=%d: %d stencils, %s bytes (%s aligned to 16), %s as copied' % (K, len(per), format(res['K'][K]['bytes'], ','),
          format(linked, ','), format(res['K'][K]['copied'], ',')))
    bad = [n for n, v in per.items() if v['calls']]
    if bad: print('  not stencil-shaped (a call or a second exit):', ', '.join(sorted(bad)))
    for n in ('dup_1', 'swap_2', 'over_2', 'plus_2', 'plus_1', 'plus_i_1', 'i_2', 'store_2', 'lit_2', 'drop_2', 'canon_2'):
        if n in per: print('  %-9s %d instructions, %d stack accesses, %d bytes copied' % (n, per[n]['ins'], per[n]['mem'], per[n]['copied']))
# today's stencils in the reference design's engine
dd = os.path.join(E.EV, 'jitvar-ref')
eng, img = E.build(g, dd)
full = eng + '.full' if os.path.exists(eng + '.full') else eng
cur = {}
for l in subprocess.run(['nm', '-S', full], stdout=subprocess.PIPE, text=True).stdout.split('\n'):
    f = l.split()
    if len(f) == 4 and f[3].startswith('st_'): cur[f[3]] = int(f[1], 16)
jitc = sum(int(l.split()[1], 16) for l in subprocess.run(['nm', '-S', full], stdout=subprocess.PIPE, text=True).stdout.split('\n')
           if len(l.split()) == 4 and l.split()[2] in 'Tt' and l.split()[3].startswith('jit_'))      # code, not the tables
res['today'] = {'stencils': len(cur), 'bytes': sum(cur.values()), 'aligned16': sum(-(-v // 16) * 16 for v in cur.values()),
                'jit_functions': jitc, 'engine': os.path.getsize(eng)}
print('today, %s: %d stencils, %s bytes (%s aligned to 16); the jit_ functions %s bytes; the engine %s' % (DID, len(cur),
      format(res['today']['bytes'], ','), format(res['today']['aligned16'], ','), format(jitc, ','), format(os.path.getsize(eng), ',')))
json.dump(res, open(OUT, 'w'), indent=1)
print('written', OUT)
