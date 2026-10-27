# results/drafts/jit-sweep-558.py - the sweep behind jit-sweep-558.md: python3 THIS CHECKER, as the build user in a built tree, CHECKER the
# after-seed-77 batch's stencil-check.py.
# results/drafts/jit-sweep-558.py - the JIT's stencils checked across the compiler genes (Iteration 558). As the build user,
# in a built tree; CHECKER: stencil-check.py with the after-seed-77 batch applied (it reads a design's own flags and
# reports a value hole that repeats). The base: seed 76's d11c9a6300 with every compiler gene at its default - its JIT
# genes, and so the stencils it builds, kept. Every flip of one compiler gene, every pair, 200 random triples (seed 558).
import itertools, json, os, random, re, shutil, subprocess, sys, time
CHECKER = sys.argv[1]; sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
G = next(json.loads(l)['genome'] for l in open('results/drafts/corpus-deaths-555.md') if l.strip().startswith('{') and '"d11c9a6300"' in l)
base = E.canon(dict(G, **E.CC0))
CMDS = []; osh = E.sh
def sh(c, *a, **k):
    if isinstance(c, (list, tuple)) and any('spn-stencils.c' in str(x) for x in c): CMDS.append([str(x) for x in c])
    return osh(c, *a, **k)
E.sh = sh
d = os.path.join(E.EV, 'sweep-base'); shutil.rmtree(d, ignore_errors=True); E.build(base, d)
c = CMDS[-1]; ccv = E.CCV(base); bcc = E.ccflags(base); n0 = len(ccv)
assert c[n0:n0 + len(bcc)] == bcc, (c[:12], bcc)
rest = [x for x in c[n0 + len(bcc):] if x.startswith(('-D', '-U', '-f', '-m')) and x not in ('-ffunction-sections', '-fdata-sections', '-flto')]
alts = []
for k in sorted(set(E.CC0) | set(E.GCC_ONLY)):
    dom = E.GENE_VALUES[k][0] if k in E.GENE_VALUES else [0, 1]
    for v in dom:
        if v == base.get(k, E.CC0.get(k)): continue
        g = E.canon(dict(base, **{k: v}))
        if g.get(k) == v and E.ccflags(g) != bcc: alts.append((k, v))
pairs = [(a, b) for a, b in itertools.combinations(alts, 2) if a[0] != b[0]]
rnd = random.Random(558); triples = set()
while len(triples) < 200:
    t = tuple(sorted(rnd.sample(alts, 3)))
    if len({x[0] for x in t}) == 3: triples.add(t)
combos = [()] + [(a,) for a in alts] + pairs + sorted(triples)
print('base %s %s; %d -D/-f flags kept; the compiler genes that change the flags: %s' % (' '.join(ccv), ' '.join(bcc), len(rest), ' '.join('%s=%s' % a for a in alts)), flush=True)
print('combos: 1 base + %d single + %d pairs + %d triples = %d' % (len(alts), len(pairs), len(triples), len(combos)), flush=True)
unsafe, rep, errs, t0 = [], {}, [], time.time()
for i, combo in enumerate(combos):
    g = E.canon(dict(base, **dict(combo)))
    if any(g.get(k) != v for k, v in combo): continue
    r = subprocess.run([sys.executable, CHECKER, '--cc', ccv[0]] + ccv[1:] + E.ccflags(g) + rest + ['-I', d], capture_output=True, text=True)
    out = r.stdout.strip().split('\n'); name = ' '.join('%s=%s' % a for a in combo) or 'the base'
    if r.returncode:
        (unsafe if 'not safe' in r.stdout else errs).append((name, ' | '.join(out[-3:])[:300])); print('  %s: %s' % (name, ' | '.join(out[-3:])[:300]), flush=True)
    for l in out:
        if 'twice or more' in l:
            for s in l.split(': ', 1)[1].split(', '): rep.setdefault(s.strip(), []).append(name)
    if i % 50 == 0: print('  ... %d of %d (%.0fs)' % (i, len(combos), time.time() - t0), flush=True)
shutil.rmtree(d, ignore_errors=True)
print('SWEEP DONE: %d combos; not safe to copy: %d; did not compile or read no stencil: %d' % (len(combos), len(unsafe), len(errs)), flush=True)
for s, ns in sorted(rep.items()): print('  repeated value hole - %s: under %d of %d combos (e.g. %s)' % (s, len(ns), len(combos), '; '.join(ns[:3])), flush=True)
