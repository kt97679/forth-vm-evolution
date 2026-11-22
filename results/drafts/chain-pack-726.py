#!/usr/bin/env python3
"""results/drafts/chain-pack-726.py CHAIN_TGZ [--md rage|gate] - the chain of Iteration 725's NEXT-RUN (the rage check
again, then portable-fastest's gate) read without unpacking (Iteration 726; results/drafts/rage-pack-654.py's checks,
for a chain of two experiment steps). The chain's state, steps and timeline; the laptop's checks; each pack's tree
against the commit it ran (every tracked file's size, `git status --porcelain --ignored` only '!!' lines); the Tegra's
choice against each design's Makefile at that commit (GCC without the JIT: taken); each taken design's engine - make's
forth-arm tightened = build()'s engine, running to 49 - and its image32.img self-built when the Makefile has the
selfhost32 rule (725's fix: its identity not asked, forth-arm runs the shipped image); selfhost-speed.md's design, its
two medians at most 1.02 and the gate's word; perf.txt the value the chain started with (4). Exit 0 when all agree.
--md rage|gate prints that step's file as it came. Run in the repository, as claude (git reads the commit)."""
import io, re, subprocess, sys, tarfile
A = [a for a in sys.argv[1:] if not a.startswith('--') and a not in ('rage', 'gate')]
MD = sys.argv[sys.argv.index('--md') + 1] if '--md' in sys.argv else None
if len(A) != 1: sys.exit(__doc__)
outer = tarfile.open(A[0])
def text(t, suffix):
    m = [x for x in t.getmembers() if x.isfile() and x.name.endswith(suffix)]
    if len(m) != 1: sys.exit('chain-pack: %d members ending %s' % (len(m), suffix))
    return t.extractfile(m[0]).read().decode()
def pack(step):
    pk = [x for x in outer.getmembers() if re.search(r'/packs/[^/]*-%s-[^/]*\.tar\.gz$' % step, x.name)]
    if len(pk) != 1: sys.exit('chain-pack: %d %s packs' % (len(pk), step))
    return tarfile.open(fileobj=io.BytesIO(outer.extractfile(pk[0]).read()))
rage, gate = pack('rage-designs'), pack('selfhost-speed')
rmd, gmd = text(rage, '/rage-designs.md'), text(gate, '/selfhost-speed.md')
if MD: print((rmd if MD == 'rage' else gmd).rstrip()); sys.exit(0)
head, status, line, log, steps, perf = [text(outer, '/' + f).strip() for f in ('head', 'status', 'line', 'chain.log', 'steps', 'perf.txt')]
git = lambda *a: subprocess.run(['git'] + list(a), capture_output=True, text=True, check=True).stdout
bad = []
def need(ok, what):
    print('  %-3s %s' % ('ok' if ok else 'BAD', what)); bad.extend([] if ok else [what])
print('the chain at %s: %s - %s' % (head, line, status))
need(status == 'done', 'the chain done')
S = steps.splitlines()
need(len(S) == 2 and all(s.startswith('ok ') for s in S), 'steps: %d, %d ok' % (len(S), sum(s.startswith('ok ') for s in S)))
T = re.findall(r'^== (\d\d):(\d\d):(\d\d) (.*)$', log, re.M)
sec = lambda t: int(t[0]) * 3600 + int(t[1]) * 60 + int(t[2])
for a, b in zip(T, T[1:]):
    print('      %s:%s:%s %-70s %4d s' % (a[0], a[1], a[2], a[3][:70], sec(b) - sec(a)))
print('      the chain: %d s, first step to the last pack' % (sec(T[-1]) - sec(T[0])))
for p in ('PASS - no regressions', '7 of 7 IDENTICAL'): need(p in log, 'the laptop: %s' % p)
need(re.search(r'== [\d:]+ the jail\nPASS', log) is not None, 'the laptop: the jail PASS')
need(perf == 'kernel.perf_event_paranoid at the pack: 4', 'perf.txt: %s' % perf)
tree = {}
for l in git('ls-tree', '-r', '-l', head).splitlines():
    meta, path = l.split('\t', 1); f = meta.split()
    if f[1] == 'blob': tree[path] = int(f[3])
for name, t in (('rage-designs', rage), ('selfhost-speed', gate)):
    lap, st, sect = {}, [], 'tree'
    for l in text(t, '/repo-files.txt').splitlines():
        if l.startswith('# git status'): sect = 'status'; continue
        if l.startswith('#'):
            if 'by entry' in l: sect = 'du'
            continue
        if sect == 'tree':
            f = l.split(' ', 3)
            if len(f) == 4 and f[0] == 'f': lap[f[3][2:] if f[3].startswith('./') else f[3]] = int(f[1])
        elif sect == 'status' and l.strip(): st.append(l)
    same = sum(1 for p in tree if lap.get(p) == tree[p])
    need(same == len(tree), "%s's tree: %d of %d tracked files at the commit's sizes" % (name, same, len(tree)))
    need(bool(st) and all(l.startswith('!! ') for l in st), "%s's git status: %d lines, all ignored" % (name, len(st)))
taken = []
for m in re.finditer(r"^(\S+) \((\w{10})\): (clang|GCC), (the JIT|no JIT) - (taken here|not this host's)$", rmd, re.M):
    name, i, cc, jit, take = m.groups()
    mk = git('show', '%s:designs/%s/Makefile' % (head, name))
    clang = re.search(r'^CC = (\S+)', mk, re.M).group(1) == 'clang'
    j = re.search(r'^SRC = .*\bsrc/jit\.c\b', mk, re.M) is not None
    need((cc == 'clang') == clang and (jit == 'the JIT') == j and (take == 'taken here') == (not clang and not j),
         '%s (%s): %s, %s - %s - as its Makefile' % (name, i, cc, jit, take))
    if take == 'taken here': taken.append((name, i, re.search(r'^selfhost32:', mk, re.M) is not None))
need(len(taken) == 3, 'the Tegra took %d designs (the GCC three expected)' % len(taken))
rows = []
for name, i, s32 in taken:
    n = re.escape(name)
    e = re.search(r'^%s \(%s, GCC\): srcarm (\d+) files, the engine (\d+) bytes(, image32\.img self-built \(its identity not asked\))?$' % (n, i), rmd, re.M)
    t = re.search(r'/%s/forth-arm\.tight: (\d+) -> (\d+) bytes$' % n, rmd, re.M)
    r = re.search(r'^  %s forth-arm: (.*)$' % n, rmd, re.M)
    ok = bool(e and t and r) and t.group(2) == e.group(2) and r.group(1) == "the lab's bytes, runs (7 SQ . -> 49)" \
        and bool(e.group(3)) == s32
    need(ok, "%s: forth-arm the lab's bytes and running; image32.img %s" % (name, 'self-built, as its Makefile' if s32 else "the translator's"))
    if e and t and r: rows.append((name, i, e.group(1), t.group(1), e.group(2), 'self-built' if e.group(3) else "translator's", r.group(1)))
need("export-arm: 3 designs, all the lab's bytes and running" in rmd, "export-arm: 3 designs, all the lab's bytes and running")
need(rmd.rstrip().endswith('rage-designs: PASS'), 'rage-designs.md: rage-designs: PASS')
g = re.findall(r'^\| (\S+) \| (\w{10}) \| ([\d.]+) \(([\d.]+)-([\d.]+)\) \| ([\d.]+) \(([\d.]+)-([\d.]+)\) \| (\w+) \|$', gmd, re.M)
need(len(g) == 1 and g[0][0] == 'portable-fastest' and g[0][1] == 'd727605472', 'selfhost-speed.md: portable-fastest d727605472 alone')
for d in g:
    need(float(d[2]) <= 1.02 and float(d[5]) <= 1.02 and d[8] == 'pass', '%s: self / translator %s (8-byte), %s (4-byte) - %s' % (d[0], d[2], d[5], d[8]))
need(gmd.rstrip().endswith('1 of 1 pass the gate (self-built at most 1.02 of the translator\'s at both widths)'), 'selfhost-speed.md: 1 of 1 pass')
print("\n| design | id | srcarm files | make's forth-arm | tightened = build()'s engine | image32.img | the check |")
print('|---|---|---|---|---|---|---|')
for r in sorted(rows, key=lambda r: int(r[4])): print('| %s | %s | %s | %s B | %s B | %s | %s |' % r)
print('\nchain-pack: %s' % ('PASS' if not bad else 'FAILED - %d' % len(bad)))
sys.exit(1 if bad else 0)
