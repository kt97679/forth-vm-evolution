#!/usr/bin/env python3
"""results/drafts/chainD-725.py [--roles] - chain D's figures beyond process-followup.sh's (Iteration 725). As anyone, from the
top of the tree; reads only.
  1. the smallest JIT design on the laptop alone: dream measured only the 28 fixed at the chain's start (REMOTES' --also),
     so the 30 pool-sizes.py --write finds had "no class in common" in followup-roles.py's pooled classes (the laptop and
     dream). Here lab/evolve/followup-roles.py itself, its classes the laptop's (PARTS replaced in its text), the rule
     unchanged (--roles prints its smallest-JIT block; its later sections need the Tegra and are cut).
  2. dream at 4-byte cells by compiler: dream's speed over the laptop's idle 32-bit reading, per design over the 10 sessions,
     the GCC JIT designs against the clang ones; the same split in every earlier results/chain-followup* directory.
  3. the self-hosting gate's spread (results/selfhost-speed-725.md): each design's 5 alternations, mean +/- SE."""
import glob, json, math, os, re, statistics as st, sys
K = 'results/chain-followup96-jitband'
LIST = 'results/followup-seed96-jitband.md'
if '--roles' in sys.argv:
    path = os.path.abspath('lab/evolve/followup-roles.py'); src = open(path).read()
    old = "PARTS = {'x86-64': ('laptop64', 'dream64'), 'x86-32': ('laptop32', 'dream32'), 'ARMv7': ('rage',)}"
    assert old in src, 'followup-roles.py: PARTS changed'
    src = src.replace(old, "PARTS = {'x86-64': ('laptop64',), 'x86-32': ('laptop32',)}")
    src = src[:src.index("\nif PRED == '610':")]           # the predictions and the dream/Tegra sections need the Tegra
    sys.argv = [path, LIST, K, '--roles', 'smalljit=15eda54ebd', '--handoff', 'results/handoff-relf-657.md']
    sys.path.insert(0, os.path.dirname(path))
    exec(compile(src, path, 'exec'), {'__name__': '__main__', '__file__': path})
    sys.exit(0)

genomes = {}
for f in glob.glob('results/*.md') + glob.glob('results/*/*.md'):
    if os.path.isdir(f): continue
    for l in open(f, errors='replace'):
        if l.startswith('{"') and '"genome"' in l:
            try: r = json.loads(l)
            except ValueError: continue
            if 'id' in r: genomes.setdefault(r['id'], r['genome'])
for l in open(LIST):
    if l.startswith('{"'): r = json.loads(l); genomes[r['id']] = r['genome']
cls = lambda g: ('GCC' if g.get('compiler') == 0 else 'clang') + (' JIT' if g.get('jit') else ' no JIT')

def laptop32(s):
    f = os.path.join(s, 'loadtest.md')
    if not os.path.exists(f): return {}
    j = {r['id']: r['idle32'] for r in (json.loads(l) for l in open(f) if l.startswith('{"'))}
    if j: return j
    out = {}                                                 # older packs: the table's idle 32 column
    for l in open(f):
        c = [x.strip() for x in l.split('|')]
        if len(c) > 10 and re.fullmatch(r'[0-9a-f]{10}', c[1]):
            try: out[c[1]] = float(c[9])
            except ValueError: pass
    return out

def split(d):
    by = {}
    for s in sorted(glob.glob(os.path.join(d, 's*'))):
        f = os.path.join(s, 'dream.lan-prebuilt32.out.json'); L = laptop32(s)
        if not os.path.exists(f) or not L: continue
        for r in json.load(open(f))['designs']:
            i = r['id']
            if i in genomes and i in L and r.get('speed_here'): by.setdefault(i, []).append((r['speed_here'], r['speed_here'] / L[i]))
    return by

print('## 2. dream at 4-byte cells, by compiler (dream / the laptop idle at 32 bits; per design the median over sessions)\n')
by = split(K)
for c in ('GCC JIT', 'clang JIT'):
    v = sorted((st.median(x[1] for x in by[i]), st.median(x[0] for x in by[i]), i) for i in by if cls(genomes[i]) == c)
    if v: print('  chain D %-10s %2d designs: dream/laptop median %.2f (%.2f-%.2f); dream speed %.3f-%.3f'
                % (c, len(v), st.median(x[0] for x in v), v[0][0], v[-1][0], min(x[1] for x in v), max(x[1] for x in v)))
slow = sorted(i for i in by if st.median(x[0] for x in by[i]) > 0.5)
print('  dream speed > 0.5: %d - %s; all GCC JIT: %s' % (len(slow), ' '.join(slow), all(cls(genomes[i]) == 'GCC JIT' for i in slow)))
s1 = [i for i in by if cls(genomes[i]) == 'GCC JIT']
print('  their per-session median, GCC JIT: %s' % ' '.join('%.3f' % st.median(by[i][k][0] for i in s1) for k in range(min(len(by[i]) for i in s1))))
print('\n  every earlier chain (the same reading):')
for d in sorted(glob.glob('results/chain-followup*')):
    if d == K: continue
    b = split(d); row = []
    for c in ('GCC JIT', 'clang JIT', 'GCC no JIT', 'clang no JIT'):
        v = [st.median(x[1] for x in b[i]) for i in b if cls(genomes[i]) == c]
        if v: row.append('%s %d: %.2f (max %.2f)' % (c, len(v), st.median(v), max(v)))
    if row: print('  %-28s %s' % (os.path.basename(d), '; '.join(row)))

print('\n## 3. the self-hosting gate (results/selfhost-speed-725.md): self / translator, the 5 alternations\n')
for l in open('results/selfhost-speed-725.md'):
    if not l.startswith('{"'): continue
    r = json.loads(l)
    for w in ('r8', 'r4'):
        v = r[w]; m = st.fmean(v); se = st.stdev(v) / math.sqrt(len(v))
        print('  %-15s %s %d-byte: mean %.3f +/- %.3f, median %.3f; above 1.02: %d of %d, below 1: %d'
              % (r['name'], r['id'], 8 if w == 'r8' else 4, m, se, st.median(v), sum(x > 1.02 for x in v), len(v), sum(x < 1 for x in v)))
