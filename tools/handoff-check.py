#!/usr/bin/env python3
"""tools/handoff-check.py [--disposable FILE] [--scan DIR ...] - nothing of this
chat is lost when the next one starts (Iteration 272).

A chat's work survives only in the repository and the bundle made from it;
/tmp and the chat's transcript are gone when the owner starts a new chat. It
went wrong: Iteration 263's pricing script lived in /tmp and was lost with its
chat; Iterations 267-268's work sat in a scratch tree when a turn ran out of
tool calls; Iteration 265's handoff still said seed 47 was running after it
had been processed, and the new chat's prompt named that entry by number.
This check fails, naming what would be lost, when:

  1. the working tree has changes that are not committed;
  2. HEAD's subject does not start "Iteration N:" (make-bundle names by it);
  3. HANDOFF.md is behind the state: its "master: Iteration N" line names an
     iteration before the last commit that changed what a new chat starts
     from - NEXT-RUN, results/pending, results/applied-after-*, a seed's
     results file, HANDOFF-PROMPT.md;
  4. HANDOFF-PROMPT.md does not send a new chat to HANDOFF.md;
  5. a git tree outside the repository (a scratch clone) holds changes, or
     commits, that the repository does not;
  6. a file in a scanned directory that could hold work - a script, patch or
     Forth source - matches no tracked file byte for byte;
  7. results/pending exists and its patches and ORDER.md disagree;
  8. NEXT-RUN has no line to run;
  9. a tracked document (.md) is in no index, or an index lists one that is
     not there (Iteration 275) - the indexes: README.md, results/README.md,
     prompts/INDEX.md, lab/evolve/README.md and any README.md an index lists.
     A document is in an index when the index names its path from the root,
     from the index's directory, or - beside the index - its name without .md
     (the prompts' ids); a seed's number matches N (seedN, applied-after-seedN);
  10. a script of the evolver (lab/evolve/*.py, *.sh) is missing from
      lab/evolve/README.md's tools.

5 and 6 pass for anything listed in the disposable list (--disposable FILE,
default /tmp/handoff-disposable.txt): per line a path - a file, or a directory
and everything under it - then a reason: something deliberately left behind.
Scanned by default: /tmp and /home/claude, each one level deep for files, two
for git trees. The tests' own leftovers (/tmp/relf-run-*) are ignored.

    python3 tools/handoff-check.py        PASS, or FAIL and what would be lost
"""
import glob, hashlib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
disp_file = '/tmp/handoff-disposable.txt'
if '--disposable' in args: i = args.index('--disposable'); disp_file = args[i + 1]; del args[i:i + 2]
scan = []
while '--scan' in args: i = args.index('--scan'); scan.append(args[i + 1]); del args[i:i + 2]
if args: sys.exit(__doc__)
scan = scan or ['/tmp', '/home/claude']
WORK_EXT = ('.py', '.sh', '.fth', '.4', '.c', '.h', '.S', '.awk', '.patch', '.diff')
IGNORE = (re.compile(r'^/tmp/relf-run-'),)

def git(*a, cwd=ROOT):
    r = subprocess.run(['git', '-c', 'safe.directory=*'] + list(a), cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return r.returncode, r.stdout

fails = []
def fail(rule, what): fails.append('%d. %s' % (rule, what))

disposable = []
if os.path.exists(disp_file):
    for l in open(disp_file):
        l = l.strip()
        if not l or l.startswith('#'): continue
        p = l.split()[0].rstrip('/')
        if len(l.split()) < 2: fail(5, '%s: listed disposable without a reason' % p)
        disposable.append(os.path.realpath(p))
def is_disposable(p):
    p = os.path.realpath(p)
    return any(p == d or p.startswith(d + '/') for d in disposable)

# 1. uncommitted work
_, st = git('status', '--porcelain')
if st.strip(): fail(1, 'not committed:\n' + ''.join('     ' + l + '\n' for l in st.rstrip('\n').split('\n')).rstrip('\n'))

# 2. HEAD's subject
_, subj = git('log', '-1', '--format=%s')
m = re.match(r'Iteration (\d+):', subj); head_n = int(m.group(1)) if m else None
if head_n is None: fail(2, "HEAD's subject does not start 'Iteration N:': %s" % subj.strip())

# 3. HANDOFF.md current with the state
hf = os.path.join(ROOT, 'HANDOFF.md')
hm = re.search(r'^- master: Iteration (\d+)\.', open(hf).read(), re.M) if os.path.exists(hf) else None
if not hm: fail(3, 'HANDOFF.md missing, or without its "- master: Iteration N." line')
else:
    _, log = git('log', '--name-only', '--format=@@%s', '--', 'lab/evolve/NEXT-RUN', 'results', 'HANDOFF-PROMPT.md')
    state_n = None
    for block in log.split('@@')[1:]:
        lines = block.strip('\n').split('\n'); files = lines[1:]
        if any(f == 'lab/evolve/NEXT-RUN' or f == 'HANDOFF-PROMPT.md' or f.startswith('results/pending/')
               or f.startswith('results/applied-after-') or re.match(r'results/evolve-.*-seed\d+\.md$', f) for f in files):
            m2 = re.match(r'Iteration (\d+):', lines[0]); state_n = int(m2.group(1)) if m2 else None
            break
    if state_n is not None and int(hm.group(1)) < state_n:
        fail(3, 'HANDOFF.md says master is Iteration %s, but Iteration %d changed the state a new chat starts from' % (hm.group(1), state_n))

# 4. the prompt sends a new chat to HANDOFF.md
hp = os.path.join(ROOT, 'HANDOFF-PROMPT.md')
if not (os.path.exists(hp) and 'HANDOFF.md' in open(hp).read()): fail(4, 'HANDOFF-PROMPT.md does not name HANDOFF.md')

# 5. scratch git trees holding what the repository does not
_, mine = git('rev-parse', '--show-toplevel'); mine = os.path.realpath(mine.strip())
for d in scan:
    for gd in glob.glob(os.path.join(d, '.git')) + glob.glob(os.path.join(d, '*', '.git')) + glob.glob(os.path.join(d, '*', '*', '.git')):
        t = os.path.realpath(os.path.dirname(gd))
        if t == mine or is_disposable(t): continue
        _, s2 = git('status', '--porcelain', cwd=t)
        _, h2 = git('rev-parse', 'HEAD', cwd=t)
        rc, _ = git('merge-base', '--is-ancestor', h2.strip(), 'HEAD')
        why = (['changes not committed'] if s2.strip() else []) + (['commits the repository does not hold'] if rc != 0 else [])
        if why: fail(5, '%s: %s' % (t, ' and '.join(why)))

# 6. files that could hold work, tracked nowhere
_, ls = git('ls-files', '-s')
tracked = {l.split()[1] for l in ls.split('\n') if l.strip()}
for d in scan:
    for p in sorted(glob.glob(os.path.join(d, '*'))):
        if not os.path.isfile(p) or not p.endswith(WORK_EXT) or any(r.match(p) for r in IGNORE) or is_disposable(p): continue
        if os.path.realpath(p).startswith(mine + '/'): continue
        blob = hashlib.sha1(b'blob %d\0' % os.path.getsize(p) + open(p, 'rb').read()).hexdigest()
        if blob not in tracked: fail(6, '%s: matches no tracked file - track it, delete it, or list it in %s with a reason' % (p, disp_file))

# 7. the pending batch agrees with its ORDER.md
pd = os.path.join(ROOT, 'results', 'pending')
if os.path.isdir(pd):
    order = open(os.path.join(pd, 'ORDER.md')).read() if os.path.exists(os.path.join(pd, 'ORDER.md')) else ''
    if not order: fail(7, 'results/pending has no ORDER.md')
    have = {os.path.basename(p) for p in glob.glob(os.path.join(pd, '*.patch'))}
    named = set(re.findall(r'results/pending/([^\s`]+\.patch)', order))
    for p in sorted(have - named): fail(7, 'results/pending/%s: not applied by ORDER.md' % p)
    for p in sorted(named - have): fail(7, 'ORDER.md applies results/pending/%s, which is not there' % p)

# 8. NEXT-RUN has a line to run
nr = [l.strip() for l in open(os.path.join(ROOT, 'lab', 'evolve', 'NEXT-RUN')) if l.strip() and not l.startswith('#')]
if not nr: fail(8, 'lab/evolve/NEXT-RUN has no line to run')

# 9. every document indexed; every indexed document there
_, mdl = git('ls-files', '*.md')
mds = [m for m in mdl.split('\n') if m and not m.startswith('vendor/relf/tree/')]   # Iteration 356: relf's own documents, indexed by relf's README
idx = ['README.md', 'results/README.md', 'prompts/INDEX.md', 'lab/evolve/README.md']
for _ in range(3):                       # a README.md an index lists is an index too
    text = ''.join(open(os.path.join(ROOT, i)).read() for i in idx if os.path.exists(os.path.join(ROOT, i)))
    idx += [m for m in mds if m.endswith('/README.md') and m not in idx and (m in text or m.split('/', 1)[1] in text)]
itext = {i: open(os.path.join(ROOT, i)).read() for i in idx if os.path.exists(os.path.join(ROOT, i))}
def named(m):
    for i, t in itext.items():
        d = os.path.dirname(i); rel = os.path.relpath(m, d) if d else m
        forms = {m, rel, re.sub(r'seed\d+', 'seedN', m), re.sub(r'seed\d+', 'seedN', rel)}
        if os.path.dirname(m) == d: forms.add(os.path.basename(m)[:-3])
        if any(f in t for f in forms): return True
    return m in idx
for m in mds:
    if not named(m): fail(9, '%s: in no index - add a line for it to the index of its place' % m)
for i, t in itext.items():
    d = os.path.dirname(i)
    for line in t.split('\n'):
        if not line.startswith('- '): continue
        for tok in re.findall(r'`([^`\s]+\.md)`', line):
            if 'N' in re.sub(r'[^N]', '', tok) and re.search(r'seedN|after-seedN', tok): continue
            if not (os.path.exists(os.path.join(ROOT, d, tok)) or os.path.exists(os.path.join(ROOT, tok))):
                fail(9, '%s lists %s, which is not there' % (i, tok))

# 10. every script of the evolver in its README's tools
_, sl = git('ls-files', 'lab/evolve/*.py', 'lab/evolve/*.sh')
lr = open(os.path.join(ROOT, 'lab', 'evolve', 'README.md')).read() if os.path.exists(os.path.join(ROOT, 'lab', 'evolve', 'README.md')) else ''
for sp in [x for x in sl.split('\n') if x]:
    if '`%s`' % os.path.basename(sp) not in lr: fail(10, '%s: not among lab/evolve/README.md\'s tools' % sp)

if fails:
    print('handoff-check: FAIL - a new chat would lose or misread this:')
    for f in fails: print('  ' + f)
    sys.exit(1)
print('handoff-check: PASS - master Iteration %s, HANDOFF.md current, nothing outside the repository, %d documents indexed; NEXT-RUN: %s' % (head_n, len(mds), nr[0]))
