#!/usr/bin/env python3
"""results/drafts/jcc-count-623.py - why GCC builds run slow on dream at 32 bits: the jump-alignment test (Iteration 623;
the question HANDOFF.md carried from 614). dream is an Intel i7-6700 (Skylake), whose microcode for Intel's JCC erratum
keeps a jump that crosses or ends on a 32-byte boundary out of the decoded-instruction cache, and a computed-goto engine
runs a dispatch jump for every primitive. Each of seed 88's follow-up's 46 (results/followup-seed88.md) is built here at
both widths as the laptop builds it (evolve.build; 4-byte cells with evolve.W4_ENV), and its jumps counted from objdump of
engine.full - the same bytes at the same addresses as the engine that runs: the dispatch jumps (indirect jmp), and every
branch unit (a jcc with the macro-fusible op before it as one unit, jmp, call, ret) - affected when it crosses or ends on
a 32-byte boundary. Against each design's dream/laptop time ratio at that width (results/chain-followup88, each source's
geometric mean over its sessions, as followup-roles.py pools): Spearman, and by compiler (gene compiler: 0 GCC, 1 clang).
Static counts, not weighted by how often each jump runs. The builds' check: each 8-byte engine's size against its record's
bin (the laptop's). As the build user; one CPU builds the 92 in about two minutes. --width W OUT: one width's counts (internal).
LIST SESS (optional, both): another list and its sessions - results/candidates-dream32-612.md results/chain-seed88, the dream
32-bit experiment's one-gene variants (612), each design's row printed. Also: the dispatch jumps' count against the ratio
(GCC's engines carry fewer - shared dispatch jumps the candidate)."""
import glob, json, math, os, re, statistics, subprocess, sys, tempfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); os.chdir(ROOT)
pos = [x for x in sys.argv[1:] if not x.startswith('--')]
LIST, SESS = (pos[0], pos[1]) if len(pos) == 2 and '--width' not in sys.argv else ('results/followup-seed88.md', 'results/chain-followup88')
if '--width' in sys.argv: LIST = os.environ.get('JCC_LIST', LIST)
FUSE = ('cmp', 'test', 'add', 'sub', 'and', 'inc', 'dec')

def hit(a, b): return a // 32 != (b - 1) // 32 or b % 32 == 0      # crosses, or ends on, a 32-byte boundary

def count(path):
    out = subprocess.run(['objdump', '-d', '--insn-width=16', path], capture_output=True, text=True).stdout
    ins = []
    for l in out.split('\n'):
        m = re.match(r'^\s*([0-9a-f]+):\t((?:[0-9a-f]{2} )+)\s*\t?(.*)$', l)
        if not m: continue
        op = re.sub(r'^(bnd|notrack|ds|cs|rep[a-z]*|lock|data16|addr32)\s+', '', m.group(3).strip())
        ins.append((int(m.group(1), 16), len(m.group(2).split()), op.split()[0] if op else '', op))
    c = dict(ind=0, ind_hit=0, br=0, br_hit=0)
    for k, (a, n, mn, op) in enumerate(ins):
        if not (mn.startswith('j') or mn.startswith('call') or mn.startswith('ret')): continue
        s = a
        if mn.startswith('j') and not mn.startswith('jmp') and k and ins[k - 1][0] + ins[k - 1][1] == a and ins[k - 1][2].startswith(FUSE):
            s = ins[k - 1][0]                                          # a macro-fused pair: one unit
        c['br'] += 1; c['br_hit'] += hit(s, a + n)
        if mn.startswith('jmp') and '*' in op: c['ind'] += 1; c['ind_hit'] += hit(a, a + n)
    return c

if '--width' in sys.argv:
    w, out = sys.argv[sys.argv.index('--width') + 1], sys.argv[sys.argv.index('--width') + 2]
    sys.path.insert(0, 'lab/evolve'); sys.argv = ['x']; import evolve as E
    W = tempfile.mkdtemp(prefix='jcc%s-' % w); R = {}
    for r in (json.loads(l) for l in open(LIST) if l.startswith('{')):
        d = os.path.join(W, r['id']); os.makedirs(d)
        try:
            eng, _ = E.build(E.canon(r['genome']), d)
            full = eng + '.full' if os.path.exists(eng + '.full') else eng
            R[r['id']] = dict(count(full), size=os.path.getsize(eng), bin=r.get('bin'), compiler=E.express(E.canon(r['genome'])).get('compiler', 0))
        except Exception as e: R[r['id']] = dict(error=str(e)[:100])
        print(w, len(R), r['id'], R[r['id']], file=sys.stderr, flush=True)
    json.dump(R, open(out, 'w')); subprocess.run(['rm', '-rf', W]); sys.exit(0)

sys.path.insert(0, 'lab/evolve')
src = os.path.dirname(os.path.abspath(__file__)); T = tempfile.mkdtemp(prefix='jcc-'); C = {}
for w in ('8', '4'):
    env = dict(os.environ)
    if w == '4':
        sys.argv = ['x']; import evolve as E0; env.update(E0.W4_ENV)
    env['JCC_LIST'] = LIST
    o = os.path.join(T, w + '.json'); subprocess.run([sys.executable, os.path.abspath(__file__), '--width', w, o], env=env, check=True)
    C[w] = json.load(open(o))
gm = lambda v: math.exp(sum(math.log(t) for t in v) / len(v))
S = {s: {} for s in ('laptop64', 'laptop32', 'dream64', 'dream32')}
for d in glob.glob(os.path.join(SESS, 's[0-9]*')):
    if os.path.exists(os.path.join(d, 'loadtest.md')):
        for l in open(os.path.join(d, 'loadtest.md'), errors='replace'):
            if l.startswith('{"'):
                r = json.loads(l)
                for s, k in (('laptop64', 'idle'), ('laptop32', 'idle32')):
                    if r.get(k): S[s].setdefault(r['id'], []).append(r[k])
    for s, f in (('dream64', 'dream.lan-prebuilt64.out.json'), ('dream32', 'dream.lan-prebuilt32.out.json')):
        if os.path.exists(os.path.join(d, f)):
            for x in json.load(open(os.path.join(d, f)))['designs']:
                if x.get('speed_here') and not x.get('rejected'): S[s].setdefault(x['id'], []).append(x['speed_here'])
P = {s: {i: gm(v) for i, v in S[s].items()} for s in S}
print('List: %s; sessions: %s.\n' % (LIST, SESS))
print('# The jump-alignment test - dream (i7-6700, Skylake) against the laptop by the engines\' jumps on 32-byte boundaries (jcc-count-623.py)\n')
ok8 = [i for i, c in C['8'].items() if 'size' in c and c['size'] == c['bin']]
print('Builds: %d of %d at 8-byte cells and %d at 4-byte built here; %d of the 8-byte engines the laptop\'s size exactly (bin).\n'
      % (sum('size' in c for c in C['8'].values()), len(C['8']), sum('size' in c for c in C['4'].values()), len(ok8)))
print('| cells | compiler | designs | dispatch jumps a design | on a boundary | branch units on a boundary | dream/laptop (median) |')
print('|---|---|---|---|---|---|---|')
for w, a, b in (('4', 'dream32', 'laptop32'), ('8', 'dream64', 'laptop64')):
    rows = {i: (c, P[a][i] / P[b][i]) for i, c in C[w].items() if 'ind' in c and i in P[a] and i in P[b] and c['ind']}
    for cc, nm in ((0, 'GCC'), (1, 'clang')):
        g = [rows[i] for i in rows if rows[i][0]['compiler'] == cc]
        if g: print('| %s-byte | %s | %d | %.1f | %.1f%% | %.1f%% | %.3f |' % (w, nm, len(g), statistics.fmean(c['ind'] for c, _ in g),
                    100 * statistics.fmean(c['ind_hit'] / c['ind'] for c, _ in g), 100 * statistics.fmean(c['br_hit'] / c['br'] for c, _ in g),
                    statistics.median(r for _, r in g)))
    x = [rows[i][0]['ind_hit'] / rows[i][0]['ind'] for i in rows]; y = [rows[i][1] for i in rows]
    xb = [rows[i][0]['br_hit'] / rows[i][0]['br'] for i in rows]
    print('| %s-byte | Spearman with dream/laptop | %d | | dispatch %+.2f | branches %+.2f | |' % (w, len(rows), statistics.correlation(x, y, method='ranked'),
          statistics.correlation(xb, y, method='ranked')))
    sp = lambda ids: statistics.correlation([rows[i][0]['ind'] for i in ids], [rows[i][1] for i in ids], method='ranked') if len(ids) > 2 else float('nan')
    print('| %s-byte | Spearman, the dispatch jumps\' count with dream/laptop | all %+.2f | GCC %+.2f | clang %+.2f | | |' % (w, sp(list(rows)),
          sp([i for i in rows if rows[i][0]['compiler'] == 0]), sp([i for i in rows if rows[i][0]['compiler'] == 1])))
    if LIST != 'results/followup-seed88.md':
        for i in sorted(rows, key=lambda i: rows[i][1]):
            c, r = rows[i]; print('|   %s | %s %s | | %d | %.1f%% | %.1f%% | %.3f |' % (w, i, ('GCC', 'clang')[c['compiler']], c['ind'], 100 * c['ind_hit'] / c['ind'], 100 * c['br_hit'] / c['br'], r))
subprocess.run(['rm', '-rf', T])
