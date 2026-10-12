#!/usr/bin/env python3
"""jitstack.py ID [ID ...] [--db FILE ...] [--works fib,loop,...] - stack state in
the JIT's translator, priced by counting before anything is built (Iteration
218; results/drafts/jit-vm-survey.md, item 1).

Today every stencil enters and leaves with the stack as (sp, tos): the top in
a register, the rest in memory, so DUP, SWAP, OVER, a literal each still emit
code and touch memory. Proposed: the translator tracks, through straight-line
code, which of the top cells are in registers and which are known constants -
a shuffle a change of state, a literal a constant until something takes it -
with every stencil in variants by state, and the state made canonical (the top
in its register, the rest in memory) at branches, branch targets, loops,
calls and EXIT. What would that remove?

Each design is built with the profiler and JIT_PRICE (engine/vm-lab.c): the
JIT translates every word it would, but the byte code runs, so each operation
of a translated word is counted where it is; the translator's dump lists those
operations, the stencils each becomes, and the branches' targets. The native
code's cost is counted in machine instructions - each stencil's own, read from
the engine with objdump (what the JIT copies: no endbr64, no final jump to the
next) - and simulated with K cached registers: shuffles and literals cost
nothing while their cells are cached (a register may hold several slots, as
Liftoff's does), an operation one instruction, a cell brought from memory one
load, a cell sent there one store, each boundary one stack-pointer update if
the memory part moved. Counted, not timed: instructions are a proxy - the
loads and stores removed are on the dependence chains, which is where the
time goes (FINDINGS-SPN.md: SUMTO 5x C with the top alone cached).

Two bounds: words compiled at run time run native wherever they are called
(their header); kernel words translated under jitx run native only when
native code calls them, so "+kernel" counts all their executions (an upper
bound) and the first column none.
"""
import collections, json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
def opt(name, default=None, many=False):
    vals = []
    while name in args:
        i = args.index(name); vals.append(args[i + 1]); del args[i:i + 2]
    return vals if many else (vals[-1] if vals else default)
dbs = opt('--db', many=True)
works = opt('--works', 'fib,loop,bubble,ackermann,kernel,corpus,sieve,parse').split(',')
KS = [int(k) for k in opt('--regs', '2,3').split(',')]
SHOW = int(opt('--show', '0'))   # the N hottest translated words, operation by operation: the audit
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
recs = {}
for db in dbs or []:
    for l in open(db):
        l = l.strip()
        if l.startswith('{'):
            try: r = json.loads(l); recs[r['id']] = r
            except ValueError: pass

def stencil_names(g):
    """engine/jit.c's enum, as this design compiles it (jitx, jitinl)."""
    src = open(os.path.join(E.ROOT, 'engine', 'jit.c')).read()
    body = src[src.index('enum { J_NEXT'):]; body = body[:body.index('S_N };')]
    names, keep = [], [True]
    for line in body.split('\n'):
        t = line.strip()
        if t.startswith('#if'):
            flag = t.split()[1]
            keep.append(bool(g.get('jitx')) if flag == 'JITX' else bool(E.express(g).get('jitinl')) if flag == 'JITINL' else True)
            continue
        if t.startswith('#endif'): keep.pop(); continue
        if all(keep): names += re.findall(r'\b([JS]_[A-Z0-9_]+)\b', t.split('/*')[0])
    return names

def stencil_cost(eng, names):
    """Each stencil as copied (no endbr64, no final jump to the next):
    (instructions, those there only for the stack in memory, data-stack
    memory accesses). sp is %rdi, the top %rsi (engine/spn-abi.h); an
    instruction is there for the stack if it writes %rdi or moves a cell to or
    from (%rdi) - an operation on a cell in memory keeps its instruction."""
    full = eng + '.full' if os.path.exists(eng + '.full') else eng
    out = subprocess.run(['objdump', '-d', '--no-show-raw-insn', full], stdout=subprocess.PIPE, text=True).stdout
    funcs, cur = {}, None
    for l in out.split('\n'):
        m = re.match(r'^[0-9a-f]+ <(st_\w+)>:', l)
        if m: cur = m.group(1); funcs[cur] = []; continue
        if re.match(r'^[0-9a-f]+ <', l): cur = None; continue
        if cur and re.match(r'^\s+[0-9a-f]+:\s', l):
            ins = l.split(':', 1)[1].strip()
            if ins and not ins.startswith(('nop', 'xchg   %ax,%ax', 'cs nop', 'data16', 'endbr64')): funcs[cur].append(ins)
    cost = {}
    for st in names:
        if not st.startswith('S_'): continue
        f = funcs.get('st_' + st[2:].lower(), [])
        if f and f[-1].startswith('jmp') and 'spn_next' in f[-1]: f = f[:-1]
        mem = sum(1 for i in f if '(%rdi' in i)
        only = sum(1 for i in f if re.search(r',%rdi$', i) or (i.startswith('mov') and '(%rdi' in i))
        cost[st] = (len(f), only, mem)
    return cost

# The stack effect of each stencil: (cells taken, cells left, kind).
# kinds: 'lit' a constant; 'shuf' a permutation; 'alu' one instruction on
# registers or an immediate; 'ld'/'st' memory; 'rs' the return stack; 'ctl' a
# boundary (control flow, call, return) - the state canonical around it.
EFFECT = {'S_LIT': (0, 1, 'lit'), 'S_DUP': (1, 2, 'shuf'), 'S_DROP': (1, 0, 'shuf'), 'S_SWAP': (2, 2, 'shuf'),
          'S_OVER': (2, 3, 'shuf'), 'S_ROT': (3, 3, 'shuf'), 'S_PLUS': (2, 1, 'alu'), 'S_ADDI': (1, 1, 'alu'),
          'S_ADDI32': (1, 1, 'alu'), 'S_EQ': (2, 1, 'alu'), 'S_GT': (2, 1, 'alu'), 'S_LT': (2, 1, 'alu'),
          'S_XOR': (2, 1, 'alu'), 'S_AND': (2, 1, 'alu'), 'S_OR': (2, 1, 'alu'), 'S_ULT': (2, 1, 'alu'),
          'S_LSHIFT': (2, 1, 'alu'), 'S_RSHIFT': (2, 1, 'alu'), 'S_NEGATE': (1, 1, 'alu'),
          'S_FETCH': (1, 1, 'ld'), 'S_CFETCH': (1, 1, 'ld'), 'S_STORE': (2, 0, 'st'), 'S_CSTORE': (2, 0, 'st'),
          'S_TOR': (1, 0, 'rs'), 'S_FROMR': (0, 1, 'rs'), 'S_RFETCH': (0, 1, 'rs'), 'S_I': (0, 1, 'rs'),
          'S_J': (0, 1, 'rs'), 'S_UNLOOP': (0, 0, 'rs'), 'S_DO': (2, 0, 'ctl'), 'S_QDO': (2, 0, 'ctl'),
          'S_LOOP': (0, 0, 'ctl'), 'S_PLOOP': (1, 0, 'ctl'), 'S_LEAVE': (0, 0, 'ctl'), 'S_0BRANCH': (1, 0, 'ctl'),
          'S_BRANCH': (0, 0, 'ctl'), 'S_DUP_GTI_BR': (1, 1, 'ctl'), 'S_CALL': (0, 0, 'ctl'), 'S_EXIT': (0, 0, 'ctl'),
          'S_INTERP': (0, 0, 'ctl'), 'S_PICK': (1, 1, 'pick'), 'S_FILL': (3, 0, 'st'), 'S_DPLUS': (4, 2, 'alu')}

class Cache:
    """The top of the stack as the translator would know it: entries 'R' (a
    register) or 'C' (a constant), the rest in memory; canonical: ['R'].
    Each method returns (instructions, data-stack memory accesses)."""
    def __init__(self, k): self.k = k; self.reset()
    def reset(self): self.top = ['R']; self.moved = False
    def need(self, n):
        """n cells cached at the top: the missing ones loaded from memory."""
        c = 0
        while len(self.top) < n: self.top.insert(0, 'R'); c += 1; self.moved = True
        return c, c
    def room(self):
        """At most k registers: the deepest register cells stored to memory."""
        c = 0
        while sum(1 for e in self.top if e == 'R') > self.k:
            del self.top[self.top.index('R')]; c += 1; self.moved = True
        while len(self.top) > 4 * self.k: del self.top[0]; c += 1; self.moved = True
        return c, c
    def canon(self):
        """Back to (sp, tos): the cells under the top stored, a constant top
        loaded as an immediate, a missing top loaded, sp moved once."""
        below = len(self.top) - 1 if self.top else 0
        ins, mem = below, below
        if self.top and self.top[-1] == 'C': ins += 1
        if not self.top: ins += 1; mem += 1
        if self.moved or len(self.top) != 1: ins += 1
        self.reset()
        return ins, mem
    def op(self, name, cost):
        take, left, kind = EFFECT.get(name, (0, 0, 'ctl'))
        base, only, _ = cost.get(name, (3, 0, 0))
        if kind == 'lit':
            self.top.append('C'); return self.room()
        if kind == 'shuf':
            i1, m1 = self.need(take)
            cells = self.top[len(self.top) - take:]; del self.top[len(self.top) - take:]
            if name == 'S_DUP': cells = cells + cells[-1:]
            elif name == 'S_DROP': cells = []
            elif name == 'S_SWAP': cells = [cells[1], cells[0]]
            elif name == 'S_OVER': cells = cells + cells[:1]
            elif name == 'S_ROT': cells = [cells[1], cells[2], cells[0]]
            self.top += cells
            i2, m2 = self.room(); return i1 + i2, m1 + m2
        if kind == 'pick' and self.top and self.top[-1] == 'C':        # n PICK, n known: a load or a register
            self.top.pop(); self.top.append('R'); i2, m2 = self.room(); return 1 + i2, 1 + m2
        if kind in ('alu', 'ld', 'st', 'rs'):
            i1, m1 = self.need(take)
            ins = self.top[len(self.top) - take:] if take else []
            del self.top[len(self.top) - take:]
            if kind == 'alu' and take and all(e == 'C' for e in ins):
                self.top += ['C'] * left; i2, m2 = self.room(); return i1 + i2, m1 + m2   # folded
            self.top += ['R'] * left
            i2, m2 = self.room()
            return i1 + i2 + max(base - only, 1), m1 + m2               # the operation, its stack moves gone
        # a boundary (and PICK of an unknown n): canonical around it, the stencil less its stack moves
        i1, m1 = self.need(take) if take else (0, 0)
        del self.top[len(self.top) - take:]
        i2, m2 = self.canon()
        return i1 + i2 + max(base - only, 1), m1 + m2 + cost.get(name, (0, 0, 0))[2] * 0

for did in args:
    g0 = recs[did]['genome'] if did in recs else E.recorded_genome(did)
    if g0 is None: sys.exit('no design %s' % did)
    g = E.canon(g0)
    if not E.jit_on(g): print('## %s - no JIT: nothing to price\n' % did); continue
    d = os.path.join(E.EV, 'jitstack'); shutil.rmtree(d, ignore_errors=True)
    os.environ['JIT_PRICE'] = '1'; E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False; del os.environ['JIT_PRICE']
    names = stencil_names(g); cost = stencil_cost(eng, names)
    pw = E.private_work(d)
    print('## %s (speed %s, jitx=%s, jitloop=%s, jitinl=%s)\n' % (did, recs.get(did, {}).get('speed', '?'), g.get('jitx'),
          E.express(g).get('jitloop'), E.express(g).get('jitinl')))
    print('stencils as copied - instructions / of them for the memory stack / data-stack accesses: ' +
          ', '.join('%s %d/%d/%d' % ((st[2:].lower(),) + cost[st]) for st in names if st in cost and st in EFFECT))
    print()
    print('Per workload: all operations dispatched; the share in translated words (run-time words / with kernel words); '
          'in them, native instructions and data-stack memory accesses now, then with K = %s cached registers.\n' % ', '.join(map(str, KS)))
    print('| workload | all ops | translated | instructions now | %s | stack accesses now | %s |' % (
          ' | '.join('K=%d instructions' % k for k in KS), ' | '.join('K=%d accesses' % k for k in KS)))
    print('|---|---|---|---|%s---|%s' % ('---|' * len(KS), '---|' * len(KS)))
    for w in works:
        pf = os.path.join(d, 'prof-' + w)
        if os.path.exists(pf): os.remove(pf)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=900, cpu=120, env=dict(os.environ, VMPROF=pf))
        ipc, recipes, ops = collections.Counter(), {}, []
        for line in open(pf):
            f = line.split()
            if f[0] == 'I': ipc[int(f[1])] += int(f[2])
            elif f[0] == 'L': recipes[int(f[1])] = [names[int(x)] for x in f[5:5 + int(f[4])]]
            elif f[0] == 'O': ops.append((int(f[1]), int(f[2]), int(f[3]), int(f[4])))
        words = collections.defaultdict(list)
        for wd, at, L, t in ops: words[wd].append((at, L, t))
        total = sum(ipc.values())
        Z = lambda: [0, 0, 0] + [0] * (2 * len(KS))      # ops, instructions now, accesses now, then (ins, acc) per K
        res = {'rt': Z(), 'all': Z()}; hot = []
        for wd, lst in words.items():
            lst = sorted(set(lst))
            header = lst[0][0] == wd + 5
            targets = {t for _, _, t in lst if t}
            seq = [(at, ipc.get(at, 0), ['S_LIT'] if L == 0xFFFD else ['S_CALL'] if L >= 0xFFFE else recipes.get(L, ['S_CALL']))
                   for at, L, t in lst]
            vals = [sum(c for _, c, _ in seq),
                    sum(c * sum(cost.get(x, (3, 0, 0))[0] for x in st) for _, c, st in seq),
                    sum(c * sum(cost.get(x, (3, 0, 0))[2] for x in st) for _, c, st in seq)]
            for k in KS:
                cache, ti, tm = Cache(k), 0, 0
                for at, c, st in seq:
                    if at in targets: i, m = cache.canon(); ti += c * i; tm += c * m     # a join: canonical on entry
                    for x in st:
                        i, m = cache.op(x, cost); ti += c * i; tm += c * m
                vals += [ti, tm]
            for key in (['rt', 'all'] if header else ['all']):
                for i, v in enumerate(vals): res[key][i] += v
            hot.append((vals[0], wd, seq, targets))
        for n_ops, wd, seq, targets in sorted(hot, reverse=True)[:SHOW]:
            print('  %s: the word at %d, %s operations run' % (w, wd, format(n_ops, ',')))
            caches = [Cache(k) for k in KS]
            for at, c, st in seq:
                line = []
                for cache in caches:
                    ci = cm = 0
                    if at in targets: i, m = cache.canon(); ci += i; cm += m
                    for x in st: i, m = cache.op(x, cost); ci += i; cm += m
                    line.append('%d/%d %s' % (ci, cm, ''.join(e[0] for e in cache.top)))
                print('    %6d %10s %-28s now %2d/%d   %s' % (at, format(c, ','), ' '.join(x[2:].lower() for x in st) + (' <-' if at in targets else ''),
                      sum(cost.get(x, (3, 0, 0))[0] for x in st), sum(cost.get(x, (3, 0, 0))[2] for x in st), '   '.join(line)))
        a, rt = res['all'], res['rt']
        def pct(x, y): return '%.1f%%' % (100.0 * x / y) if y else '-'
        def both(i): return '%s / %s' % (format(rt[i], ','), format(a[i], ','))
        def red(i, base): return '%s (%s / %s)' % (both(i), pct(rt[i] - rt[base], rt[base]), pct(a[i] - a[base], a[base]))
        print('| %s | %s | %s / %s | %s | %s | %s | %s |' % (w, format(total, ','), pct(rt[0], total), pct(a[0], total), both(1),
              ' | '.join(red(3 + 2 * i, 1) for i in range(len(KS))), both(2), ' | '.join(red(4 + 2 * i, 2) for i in range(len(KS)))))
    print()
    shutil.rmtree(d, ignore_errors=True)
