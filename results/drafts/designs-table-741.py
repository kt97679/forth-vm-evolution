#!/usr/bin/env python3
"""results/drafts/designs-table-741.py RECORDS NAMES SESSIONS[=LABEL] ... - designs/README.md's table rows for any set of roles
(Iteration 741; results/drafts/designs-table-718.py made general - the endgame's step 4, results/drafts/endgame-740.md).
RECORDS: the roles' records (results/relf-designs-NNN.md: master's sizes, the laptop's memory); NAMES: NAME=ID,... in the
table's order (the build-out's NAMES - roles-build-718.sh's, relf-handoff-739.py's); SESSIONS: chains' readings by
session (results/chain-followupNN-*: chain-sessions.py's DEST - sK/loadtest.md and the remote lines' out.json), in order
of preference, each with a LABEL for the row's comment (default the directory's name). Each class the geometric mean
over a chain's sessions, then of its machines (x86-64: the laptop alone and dream at 8-byte cells; x86-32 the same at 4;
ARMv7: the Tegra) - from the first chain that has all three of a design's classes, else the last of those with the most;
a JIT design's ARMv7 figure is its JIT-off build, marked *; bytes and memory the record's. Prints the rows, each with its
chain in a comment; exit 1 if a design is in no chain.
Test (741): with chain B's and chain C's readings and 718's records it prints designs-table-718.py's rows byte for byte,
designs/README.md's table - results/drafts/designs-table-741.sh. Run from the repository's top, as the build user."""
import json, math, os, glob, statistics, sys

A = sys.argv[1:]
if len(A) < 3: sys.exit(__doc__)
RECORDS, NAMES, SES = A[0], [p.split('=', 1) for p in A[1].split(',')], A[2:]
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
LAP = {'lap64': 'idle', 'lap32': 'idle32'}
HOST = {'dream64': 'dream.lan-prebuilt64.out.json', 'dream32': 'dream.lan-prebuilt32.out.json', 'rage': 'rage.lan-prebuiltarm.out.json'}
PARTS = {'x86-64': ('lap64', 'dream64'), 'x86-32': ('lap32', 'dream32'), 'ARMv7': ('rage',)}
def load(ses):
    S = {s: {} for s in list(LAP) + list(HOST)}
    for d in glob.glob(os.path.join(ses, 's[0-9]*')):
        k = int(d.rsplit('s', 1)[1]); p = os.path.join(d, 'loadtest.md')
        if os.path.exists(p):
            for r in (json.loads(l) for l in open(p) if l.startswith('{"')):
                for s, key in LAP.items():
                    if r.get(key): S[s].setdefault(r['id'], {})[k] = r[key]
        for s, f in HOST.items():
            p = os.path.join(d, f)
            if os.path.exists(p):
                for x in json.load(open(p))['designs']:
                    if x.get('speed_here'): S[s].setdefault(x['id'], {})[k] = x['speed_here']
    return S
def cls(S, i):
    c = {}
    for k, ss in PARTS.items():
        if all(S[s].get(i) for s in ss):
            c[k] = math.exp(statistics.fmean(statistics.fmean(math.log(v) for v in S[s][i].values()) for s in ss))
    return c
CH = []
for s in SES:
    d, _, lab = s.partition('=')
    if not os.path.isdir(d): sys.exit('designs-table: no readings at %s' % d)
    CH.append((lab or os.path.basename(d.rstrip('/')), load(d)))
WHAT = {'fastest-x86-64': 'fastest on x86-64', 'fastest-x86-32': 'fastest on x86-32',
        'best-all-round': 'best mean of x86-64, x86-32 and ARMv7', 'small-jit': 'smallest of the JIT designs',
        'portable-fastest': 'fastest without the JIT, by the mean', 'portable-arm': 'fastest on ARMv7',
        'portable-knee': 'fast without the JIT; small', 'portable-small': 'small, fast on ARMv7',
        'least-memory': 'least memory', 'smallest': 'smallest'}
REC = {json.loads(l)['id']: json.loads(l) for l in open(RECORDS) if l.startswith('{"')}
bad = 0
for n, i in NAMES:
    assert n in WHAT, 'no role %s (designs-table-741.py\'s WHAT names the ten)' % n
    assert i in REC, '%s (%s) not in %s' % (i, n, RECORDS)
    r = REC[i]; cs = [(lab, cls(S, i)) for lab, S in CH]
    full = [x for x in cs if len(x[1]) == 3]
    if full: src, c = full[0]
    else:
        most = max(len(x[1]) for x in cs); src, c = [x for x in cs if len(x[1]) == most][-1]
    if not c: print('designs-table: %s (%s) in no chain\'s readings' % (i, n), file=sys.stderr); bad += 1
    jit = bool(E.express(E.canon(r['genome'])).get('jit'))
    f = lambda k: ('%.3f' % c[k] + ('*' if k == 'ARMv7' and jit else '')) if k in c else '-'
    print('| `%s` | %s | %s | %s | %s | %s | {:,} | %s KB | %s |'.format(r['total'])
          % (n, i, WHAT[n], f('x86-64'), f('x86-32'), f('ARMv7'), r.get('rss'), 'yes' if jit else 'no') + '  <!-- chain %s -->' % src)
sys.exit(1 if bad else 0)
