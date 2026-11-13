#!/usr/bin/env python3
"""results/drafts/rage-pack-654.py CHAIN_TGZ [--md] - the rage check's chain archive read without unpacking (Iteration 654):
the chain's state and the laptop's checks; the laptop's tree against the commit it ran (every tracked file's size, and
`git status --porcelain --ignored` only '!!' lines); the designs export-arm.py took on the Tegra against each one's class
in designs/NAME/Makefile at that commit (GCC without the JIT: taken, as 652's lab_class()); each taken design's result
and its ARMv7 engine's bytes - make's forth-arm, tightened, and build()'s engine. Exit 0 when all agree and the pack's
rage-designs.md says PASS. --md prints that file as it came. Run in the repository, as claude (git reads the commit)."""
import io, re, subprocess, sys, tarfile
A = [a for a in sys.argv[1:] if a != '--md']
if len(A) != 1: sys.exit(__doc__)
outer = tarfile.open(A[0])
def text(t, suffix):
    m = [x for x in t.getmembers() if x.isfile() and x.name.endswith(suffix)]
    if len(m) != 1: sys.exit('rage-pack: %d members ending %s' % (len(m), suffix))
    return t.extractfile(m[0]).read().decode()
pk = [x for x in outer.getmembers() if re.search(r'/packs/[^/]*rage-designs[^/]*\.tar\.gz$', x.name)]
if len(pk) != 1: sys.exit('rage-pack: %d rage-designs packs' % len(pk))
inner = tarfile.open(fileobj=io.BytesIO(outer.extractfile(pk[0]).read()))
md, files = text(inner, '/rage-designs.md'), text(inner, '/repo-files.txt')
if '--md' in sys.argv: print(md.rstrip()); sys.exit(0)
head, status, line, log = [text(outer, '/' + f).strip() for f in ('head', 'status', 'line', 'chain.log')]
git = lambda *a: subprocess.run(['git'] + list(a), capture_output=True, text=True, check=True).stdout
bad = []
def need(ok, what):
    print('  %-3s %s' % ('ok' if ok else 'BAD', what)); bad.extend([] if ok else [what])
print('the chain at %s: %s - %s' % (head, line, status))
need(status == 'done', 'the chain done')
for p in ('PASS - no regressions', '7 of 7 IDENTICAL'): need(p in log, 'the laptop: %s' % p)
need(re.search(r'== [\d:]+ the jail\nPASS', log) is not None, 'the laptop: the jail PASS')
tree = {}                                                # the commit's tracked files and sizes
for l in git('ls-tree', '-r', '-l', head).splitlines():
    meta, path = l.split('\t', 1); f = meta.split()
    if f[1] == 'blob': tree[path] = int(f[3])
lap, status_lines, sect = {}, [], 'tree'                 # repo-files.txt: the tree, the build/ sizes, git status
for l in files.splitlines():
    if l.startswith('# git status'): sect = 'status'; continue
    if l.startswith('#'):
        if 'by entry' in l: sect = 'du'
        continue
    if sect == 'tree':
        f = l.split(' ', 3)
        if len(f) == 4 and f[0] == 'f': lap[f[3][2:] if f[3].startswith('./') else f[3]] = int(f[1])
    elif sect == 'status' and l.strip(): status_lines.append(l)
same = sum(1 for p in tree if lap.get(p) == tree[p])
need(same == len(tree), "the laptop's tree: %d of %d tracked files at the commit's sizes" % (same, len(tree)))
need(bool(status_lines) and all(l.startswith('!! ') for l in status_lines),
     "the laptop's git status: %d lines, all ignored ('!!')" % len(status_lines))
taken = []
for m in re.finditer(r"^(\S+) \((\w{10})\): (clang|GCC), (the JIT|no JIT) - (taken here|not this host's)$", md, re.M):
    name, i, cc, jit, take = m.groups()
    mk = git('show', '%s:designs/%s/Makefile' % (head, name))
    clang = re.search(r'^CC = (\S+)', mk, re.M).group(1) == 'clang'
    j = re.search(r'^SRC = .*\bsrc/jit\.c\b', mk, re.M) is not None
    need((cc == 'clang') == clang and (jit == 'the JIT') == j and (take == 'taken here') == (not clang and not j),
         "%s (%s): %s, %s - %s - as its Makefile at %s" % (name, i, cc, jit, take, head))
    if take == 'taken here': taken.append((name, i))
need(len(taken) == 3, 'the Tegra took %d designs (the GCC three expected)' % len(taken))
rows = []
for name, i in taken:
    n = re.escape(name)
    e = re.search(r'^%s \(%s, GCC\): srcarm (\d+) files, the engine (\d+) bytes$' % (n, i), md, re.M)
    t = re.search(r'/%s/forth-arm\.tight: (\d+) -> (\d+) bytes$' % n, md, re.M)
    r = re.search(r'^  %s forth-arm: (.*)$' % n, md, re.M)
    ok = bool(e and t and r) and t.group(2) == e.group(2) and r.group(1) == "the lab's bytes, runs (7 SQ . -> 49)"
    need(ok, "%s: make's forth-arm the lab's bytes and running" % name)
    if e and t and r: rows.append((name, i, e.group(1), t.group(1), e.group(2), r.group(1)))
need("export-arm: 3 designs, all the lab's bytes and running" in md, "export-arm: 3 designs, all the lab's bytes and running")
need(md.rstrip().endswith('rage-designs: PASS'), 'rage-designs.md: rage-designs: PASS')
print("\n| design | id | srcarm files | make's forth-arm | tightened = build()'s engine | the check |")
print('|---|---|---|---|---|---|')
for r in sorted(rows, key=lambda r: int(r[4])): print('| %s | %s | %s | %s B | %s B | %s |' % r)
print('\nrage-pack: %s' % ('PASS' if not bad else 'FAILED - %d' % len(bad)))
sys.exit(1 if bad else 0)
