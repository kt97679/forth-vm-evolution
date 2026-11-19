#!/usr/bin/env python3
"""results/drafts/superopt-707.py [--max-len L] [--tests T] - a size superoptimizer's ceiling on the selection's code
(Iteration 707; the ideation survey's item 2 - Iteration 186 found 2-4 shorter stack-word patterns in two images, at most
0.09 % of dispatches; since 678 the size counts the five programs' code, 37 % of the smallest design, so judged again in
bytes). Massalin's method at the source level: every run of consecutive words inside the five programs' colon
definitions (lab/evolve/apps: sim16 gc16 scan evo shellmix) made only of the words modelled here (stack, arithmetic,
logic, comparison, small literals) - the runs of 2 and 3 words with their counts; for each, the shortest sequence of
modelled words, cheaper in bytes, that agrees with it on T random stacks (edge values among them: 0, 1, -1, the sign bit,
the extremes), enumerated by length. Costs: a word 1 byte, a literal 2 (CV8's short literal) - an estimate of the
compiled form; the run-time compiler already folds `n +` and friends on designs with rtimm (684's mechanism 5), so those
rows are marked. Reads only. stdout: the rules found, their instances, the bytes a peephole would save at most."""
import collections, itertools, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APPS = os.path.join(HERE, '..', '..', 'lab', 'evolve', 'apps')
A = sys.argv[1:]
maxlen = int(A[A.index('--max-len') + 1]) if '--max-len' in A else 2
T = int(A[A.index('--tests') + 1]) if '--tests' in A else 3000
M = (1 << 64) - 1; S = 1 << 63
sg = lambda x: x - (1 << 64) if x & S else x
w = lambda x: x & M
F = lambda b: M if b else 0
# a word: (inputs, outputs, function of the inputs -> outputs); cells unsigned 64-bit, flags -1/0
W = {
    'DUP': (1, 2, lambda a: (a, a)), 'DROP': (1, 0, lambda a: ()), 'SWAP': (2, 2, lambda a, b: (b, a)),
    'OVER': (2, 3, lambda a, b: (a, b, a)), 'ROT': (3, 3, lambda a, b, c: (b, c, a)), '-ROT': (3, 3, lambda a, b, c: (c, a, b)),
    'NIP': (2, 1, lambda a, b: (b,)), 'TUCK': (2, 3, lambda a, b: (b, a, b)), '2DUP': (2, 4, lambda a, b: (a, b, a, b)),
    '2DROP': (2, 0, lambda a, b: ()), '+': (2, 1, lambda a, b: (w(a + b),)), '-': (2, 1, lambda a, b: (w(a - b),)),
    '*': (2, 1, lambda a, b: (w(a * b),)), 'AND': (2, 1, lambda a, b: (a & b,)), 'OR': (2, 1, lambda a, b: (a | b,)),
    'XOR': (2, 1, lambda a, b: (a ^ b,)), 'INVERT': (1, 1, lambda a: (a ^ M,)), 'NEGATE': (1, 1, lambda a: (w(-a),)),
    'ABS': (1, 1, lambda a: (w(abs(sg(a))),)), 'MIN': (2, 1, lambda a, b: (a if sg(a) < sg(b) else b,)),
    'MAX': (2, 1, lambda a, b: (a if sg(a) > sg(b) else b,)), '1+': (1, 1, lambda a: (w(a + 1),)), '1-': (1, 1, lambda a: (w(a - 1),)),
    '2*': (1, 1, lambda a: (w(a << 1),)), '2/': (1, 1, lambda a: (w(sg(a) >> 1),)), '=': (2, 1, lambda a, b: (F(a == b),)),
    '<>': (2, 1, lambda a, b: (F(a != b),)), '<': (2, 1, lambda a, b: (F(sg(a) < sg(b)),)), '>': (2, 1, lambda a, b: (F(sg(a) > sg(b)),)),
    'U<': (2, 1, lambda a, b: (F(a < b),)), 'U>': (2, 1, lambda a, b: (F(a > b),)), '0=': (1, 1, lambda a: (F(a == 0),)),
    '0<': (1, 1, lambda a: (F(a & S),)), '0>': (1, 1, lambda a: (F(sg(a) > 0),)), '0<>': (1, 1, lambda a: (F(a != 0),)),
    'CELL+': (1, 1, lambda a: (w(a + 8),)), 'CELLS': (1, 1, lambda a: (w(a * 8),)), 'CHAR+': (1, 1, lambda a: (w(a + 1),)),
    'CHARS': (1, 1, lambda a: (a,)),
}
LITS = ['0', '1', '2', '-1', '3', '4', '8', 'TRUE', 'FALSE']
for n_ in LITS: W[n_] = (0, 1, (lambda v: lambda: (w(v),))({'TRUE': -1, 'FALSE': 0}.get(n_, None) if n_ in ('TRUE', 'FALSE') else int(n_)))
cost = lambda seq: sum(2 if t in LITS and t not in ('TRUE', 'FALSE') else 1 for t in seq)

def run(seq, st):
    st = list(st)
    for t in seq:
        i, o, f = W[t]
        if len(st) < i: return None
        a = st[len(st) - i:] if i else []; del st[len(st) - i:]
        st.extend(f(*a))
    return tuple(st)

def need(seq):   # the stack depth a sequence reads
    d = m = 0
    for t in seq:
        i, o, _ = W[t]; d -= i; m = min(m, d); d += o
    return -m

rng = random.Random(707)
EDGE = [0, 1, M, 2, S, S - 1, S + 1, 255, 256, 7, w(-7), 8]
def stacks(k):
    for _ in range(T): yield tuple(rng.choice(EDGE) if rng.random() < 0.4 else rng.getrandbits(64 if rng.random() < 0.5 else 8) for _ in range(k))

def equal(a, b):
    k = max(need(a), need(b))
    return all(run(a, s) == run(b, s) for s in stacks(k + 1))

# the programs' runs of modelled words
def words(path):
    s = open(path, errors='replace').read()
    s = re.sub(r'\\[^\n]*', ' ', s); s = re.sub(r'\(\s[^)]*\)', ' ', s)
    s = re.sub(r'(\.|S|C|ABORT)"\s[^"]*"', ' "STR" ', s, flags=re.I)
    return s.split()
runs = collections.Counter()
for app in ('sim16', 'gc16', 'scan', 'evo', 'shellmix'):
    toks = [t.upper() for t in words(os.path.join(APPS, app + '.fth'))]
    inside = False
    for i, t in enumerate(toks):
        if t in (':', ':NONAME'): inside = True; continue
        if t == ';': inside = False; continue
        if not inside: continue
        for n in (2, 3):
            g = tuple(toks[i:i + n])
            if len(g) == n and all(x in W for x in g): runs[g] += 1

alpha = [k for k in W if k not in ('TRUE', 'FALSE', 'NIP', 'TUCK', '-ROT', '0<>')]   # 707: not in the kernel (an app's own NIP is a call)   # constants: a call each, not a one-byte word - never cheaper than the literal
found = []
for g, c in runs.most_common():
    if c < 2: break
    best = None
    for L in range(1, min(maxlen, len(g)) + 1):
        for cand in itertools.product(alpha, repeat=L):
            if cost(cand) >= cost(g) or (best and cost(cand) >= cost(best)): continue
            if equal(g, cand): best = cand
        if best: break
    if best: found.append((g, best, c, (cost(g) - cost(best)) * c))
print('the five programs: %d distinct runs of 2-3 modelled words, %d instances; %d occur twice or more'
      % (len(runs), sum(runs.values()), sum(1 for c in runs.values() if c >= 2)))
print('\n| run | shorter, the same on %d stacks | instances | bytes at most | note |\n|---|---|---:|---:|---|' % T)
tot = 0
for g, b, c, s in sorted(found, key=lambda x: -x[3]):
    note = 'rtimm folds it already (684, mechanism 5)' if len(g) == 2 and g[0] in LITS and g[1] in ('+', '-', '=') else ''
    tot += s if not note else 0
    print('| %s | %s | %d | %d | %s |' % (' '.join(g), ' '.join(b), c, s, note))
print('\nat most %d bytes of the five programs\' code (not counting the rows rtimm folds), before a peephole\'s own cost in the overlays' % tot)
