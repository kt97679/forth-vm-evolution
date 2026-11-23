"""results/drafts/relf-handoff-739.py --iter N --records RECORDS.md --previous HANDOFF.md --package NAME --notes NOTES.md
[--sha SHA256.txt] [--designs DIR] - the relf handoff for whatever roles designs/ holds, on stdout (Iteration 739; the
owner: one final handoff to relf when the design evolution is done). results/drafts/relf-handoff-726.py wrote 726's
document for that set alone - its ten ids, its three translator-built roles and its prose fixed in the code. Here:

  from designs/ (or DIR): README.md's table (the rows, the speed classes, the bytes, the memory, the JIT) and its "Which
      to use" paragraph (how the speed was measured); TRANSLATOR-BUILT (which images are the converter's, and why);
  from RECORDS (the {"id" lines of the roles' records, results/relf-designs-NNN.md): each row checked - the id, the
      bytes, the memory - and the genome, whose expression off s6-cv8b's by today's evolver gives the genes (with the
      glossary: GENES.md, evolve.py's gene lines, the lines below for the genes neither has);
  from the previous handoff (726's form or 657's): which roles changed and which genes are new since;
  from NOTES (written by hand at the end): "## Changed" - bullets for what changed besides (the series, the roles'
      chains, the measure), "## For relf" - bullets added to that section, "## History" - one paragraph, the newest.

It asserts what must hold: every row a record, its bytes and memory the record's, its JIT the expression's, every
translator-built name a row. 657's and 726's claim - none measured in all three classes within 25 % of the best in
each - is computed and said either way. --sha: the checksums file pack-designs.py's rebuild is checked against. As the
build user, from the repository's top (it imports the evolver):
    runuser -u claude -- python3 results/drafts/relf-handoff-739.py --iter N ... > results/handoff-relf-N.md
Test (739): the 726 roles against 657 with 726's prose as notes (results/drafts/relf-handoff-739-test.md)."""
import argparse, json, os, re, sys, textwrap
ap = argparse.ArgumentParser()
for a in ('--iter', '--records', '--previous', '--package', '--notes'): ap.add_argument(a, required=True)
ap.add_argument('--sha'); ap.add_argument('--designs', default='designs')
A = ap.parse_args()
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E

cells = lambda l: [c.strip() for c in l.strip().strip('|').split('|')]
D = A.designs
README = open(os.path.join(D, 'README.md')).read()
ROWS = []
for l in README.split('\n'):
    c = cells(l) if l.startswith('| `') else None
    if not c or len(c) != 9 or c[1] == 'design': continue
    f = lambda s: None if s == '-' else float(s.rstrip('*'))
    ROWS.append(dict(target=c[0].strip('`'), id=c[1], wins=c[2], x64=f(c[3]), x32=f(c[4]), arm=f(c[5]), arms=c[5],
                     b8=int(c[6].replace(',', '')), mem=int(c[7].split()[0]), jit=c[8] == 'yes'))
dirs = sorted(x for x in os.listdir(D) if os.path.exists(os.path.join(D, x, 'record.json')))
assert sorted(r['target'] for r in ROWS) == dirs, (dirs, [r['target'] for r in ROWS])
m = re.search(r'## Which to use\n\n(.*?)\n\n\|', README, re.S)
METHOD = ' '.join(m.group(1).split()) if m else ''
m = re.search(r'\n\|[^\n]*\|\n\n(\\\*[^\n]*)\n', README)       # the table's footnote (the * and - marks)
FOOT = m.group(1) if m else ''
REC = {json.loads(l)['id']: json.loads(l) for l in open(A.records) if l.startswith('{')}
assert not [r['id'] for r in ROWS if r['id'] not in REC], [r['id'] for r in ROWS if r['id'] not in REC]
TB = {}
for l in open(os.path.join(D, 'TRANSLATOR-BUILT')):
    if l.strip() and not l.startswith('#'): k, _, why = l.strip().partition(' '); TB[k] = why.strip()
assert set(TB) <= set(dirs), TB
for r in ROWS:
    x = REC[r['id']]
    assert (x['total'], x['rss']) == (r['b8'], r['mem']), (r['id'], x['total'], x['rss'], r['b8'], r['mem'])
    assert json.load(open(os.path.join(D, r['target'], 'record.json')))['id'] == r['id'], r['target']
    r['image'] = 'translator-built' if r['target'] in TB else 'self-built'
K = ('x64', 'x32', 'arm'); best = {k: min(r[k] for r in ROWS if r[k] is not None) for k in K}
all3 = [r for r in ROWS if None not in [r[k] for k in K]]
near = [r for r in all3 if all(r[k] <= 1.25 * best[k] for k in K)]

PREV = open(A.previous).read()
OLD = {}
for l in PREV.split('\n'):                               # 726's rows: | `target` | id |; 657's: | ... (`target`) | id |
    mm = re.match(r'\| `([\w-]+)` \| (\w{10}) \|', l) or re.match(r'\| .*\(`([\w-]+)`\) \| (\w{10}) \|', l)
    if mm: OLD[mm.group(1)] = mm.group(2)
assert OLD, 'no roles in ' + A.previous
mp = re.search(r'^# .*\(Iteration (\d+)\)', PREV, re.M) or re.search(r'Iteration (\d+)', PREV)
PREV_IT = mp.group(1) if mp else '?'
changed = [r for r in ROWS if OLD.get(r['target']) not in (None, r['id'])]
new_t = [r for r in ROWS if r['target'] not in OLD]; gone = sorted(set(OLD) - set(dirs))
PREV_GENES = set(re.findall(r'^- `(\w+)` - ', PREV.split('### The genes', 1)[1], re.M)) if '### The genes' in PREV else None

WORD = dict(enumerate('none one two three four five six seven eight nine ten eleven twelve'.split()))
NOTES = {}; cur = None
for l in open(A.notes).read().split('\n'):
    if l.startswith('## '): cur = l[3:].strip(); NOTES[cur] = []
    elif cur: NOTES[cur].append(l)
note = lambda k: [l for l in '\n'.join(NOTES.get(k, [])).strip().split('\n') if l.strip()] if NOTES.get(k) else []

def val(v):
    if v is None: return '-'
    return '%d ops' % len(v) if isinstance(v, list) and len(v) > 3 else ','.join('+'.join(x) if isinstance(x, list) else str(x) for x in v) if isinstance(v, list) else str(v)
s6 = E.express(E.canon(E.HUMAN['s6-cv8b']))
for r in ROWS:
    e = E.express(E.canon(REC[r['id']]['genome']))
    assert bool(e.get('jit')) == r['jit'], r['id']
    r['differs'] = {k: e.get(k) for k in sorted(set(e) | set(s6)) if e.get(k) != s6.get(k)}
    r['tag2'] = bool(e.get('tag2')); r['clang'] = bool(e.get('compiler'))
    r['genes'] = ', '.join('%s=%s' % (k, val(v)) for k, v in sorted(r['differs'].items()))
G = open('lab/evolve/GENES.md').read().split('\n')
GLOSS = {   # 726's (results/drafts/relf-handoff-726.py), for the genes GENES.md has no row for
    'tos': 'the top of the data stack in a register (GENES.md\'s CV8 table; engine/vm-lab-tos.c)',
    'spec': 'specialised opcode families - var, tiny, small, imm, loc: variables, small literals and immediates as their own opcodes (GENES.md\'s CV8 table, "specialisation families")',
    'supers': 'superinstructions - the pairs listed, each one opcode (tools/gen-super.py)',
    'tag2': 'the two-bit tag image format, relf\'s (FORMAT-TAG2.md)',
    'threads': 'the dictionary in 16, 32, 64 or 128 chains (evolve.py, Iteration 204)',
    'fsys': 'the file words over single system calls, by level (results/drafts/fsys/single-syscall.md; levels 4-5 retired at 599)',
    'guard': 'guard pages around the stacks (GENES.md\'s CV8 table)',
    'd256': 'a 256-entry dispatch table (GENES.md\'s CV8 table)',
    'regpin': 'the VM\'s registers pinned to machine registers (RELF.md, Iteration 364)',
    'opt': 'the optimisation level: O2 (absent), O3 or Os (clang: -Oz)',
    'jit': 'the JIT: hot words translated to x86 machine code from compiled stencils (engine/jit.c, engine/spn-stencils.c; x86 only)',
    'jitimg': 'the image\'s own words JIT candidates (evolve.py, Iteration 341)',
    'jitvar': 'variable fetch and store given JIT stencils (evolve.py, Iteration 342)',
    'rtfuse': 'run-time fusion: the compiler the image carries fuses pairs as the converter does',
    'nogcse': '-fno-gcse, GCC only (the compile line in build.txt)', 'nocrossjump': '-fno-crossjumping, GCC only (build.txt)',
    'nocet': '-fcf-protection=none (build.txt)', 'align1': 'the -falign-*=1 flags, GCC only (build.txt)',
    'folds': 'which of the 23 foldable primitives get prim;EXIT opcodes, in what order (GENES.md\'s table)',
    'noreorder': '-fno-reorder-blocks, GCC only (build.txt)',
    't2hot': 'the two-bit tag\'s ranking: its hot threshold - 0.02 by default, 0, 0.05 or static (Iteration 71; with the tag)',
    'varslot': 'slot operands (VAR@ and VAR!, the locals opcodes) of variable length - a 15-bit payload in two bytes, 23 bits in three; at 0 a fixed 16 bits (engine/vm-lab.c, VARSLOT)',
    'peel': '-fpeel-loops, GCC only (build.txt)', 'tracer': '-ftracer, GCC only (build.txt)', 'ipaclone': '-fipa-cp-clone, GCC only (build.txt)',
    'rtvar': 'a data word\'s @ and ! compiled as one operation (vf, vs) at run time - relf\'s VAR@ and VAR!, DOES> @ among them (forth/cv8-fuse-var.4; results/rtvar-688.md, does-at-695.md)',
    'rtconst': 'a constant compiled as its value at run time - relf\'s rule and test (forth/cv8-fuse-const.4; results/rtconst-691.md)',
    'rtinline': 'a body of at most 3 instructions in 6 bytes copied for its call at run time - relf\'s inlining rule (forth/cv8-fuse-inline.4; results/rtinline-694.md)',
    # 739: the reopened search's genes (727-733), from their records
    'hashk': 'the dictionary\'s chain hash with one constant, ((v * 18835) >> 8) & (chains - 1) - after the demoscene\'s crinkler (results/applied-hashk-730/ORDER.md)',
    'chainorder': 'each chain\'s most looked-up names first, the forward links their own form - the converter\'s (results/applied-chainorder-732/ORDER.md)',
    'numfirst': 'a token of digits converted before its lookup while no name has that form - the engine\'s (FIND) or INTERPRET8 (results/applied-numfirst-733/ORDER.md)',
}
def doc(g):
    if g in GLOSS: return GLOSS[g]
    for l in G:
        if re.search(r'\(`%s`[:;)]' % re.escape(g), l) and l.startswith('|'):
            c = l.strip('|').split('|')[0].strip(); return c if len(c) <= 260 else c[:257].rsplit(' ', 1)[0] + ' ...'
    mm = re.search(r"^gene\('%s'.*?#\s*(.*)$" % re.escape(g), open('lab/evolve/evolve.py').read(), re.M)
    return (mm.group(1) if len(mm.group(1)) <= 260 else mm.group(1)[:257].rsplit(' ', 1)[0] + ' ...') + ' (evolve.py\'s gene line)' if mm else None

N, n = A.iter, len(ROWS)
t = lambda rs: ', '.join('`%s`' % r['target'] for r in rs) or 'none'
ids = ','.join(r['id'] for r in ROWS); named = ','.join('%s=%s' % (r['target'], r['id']) for r in ROWS)
used = set()
for r in ROWS: used |= set(r['differs'])
newg = sorted(used - PREV_GENES) if PREV_GENES is not None else []
nojit = [r for r in ROWS if not r['jit']]
L = ['# Forth designs for relf (Iteration %s)' % N, '',
     '(forth-vm-evolution, Iteration %s. It replaces results/handoff-relf-%s.md, which stays as the history. Written by' % (N, PREV_IT),
     'results/drafts/relf-handoff-739.py from designs/, the records (%s) and the notes on what changed.)' % A.records, '',
     '## What changed since the %s handoff' % PREV_IT, '']
L += note('Changed')
L += ['- **The roles**: %s of the %s changed%s%s%s.' % (WORD.get(len(changed), len(changed)), WORD.get(n, n),
          (': ' + ', '.join('`%s` %s (was %s)' % (r['target'], r['id'], OLD[r['target']]) for r in changed)) if changed else '',
          ('; new: ' + t(new_t)) if new_t else '', ('; gone: ' + ', '.join('`%s`' % g for g in gone)) if gone else ''),
      '- **The images**: %s self-built (forth/cross-cv8.4 on the design\'s own engine, `make selfhost` rebuilds them byte for' % WORD.get(n - len(TB), n - len(TB)),
      '  byte), %s' % ('every one' if not TB else '%s translator-built - %s' % (WORD.get(len(TB), len(TB)), '; '.join('`%s`: %s' % (k, TB[k]) for k in sorted(TB)))) +
      ' (designs/TRANSLATOR-BUILT).']
if PREV_GENES is not None:
    L.append('- **Genes new in these designs since %s**: %s.' % (PREV_IT, ', '.join('`%s`' % g for g in newg) if newg else 'none'))
L += ['', '## The designs', '',
      '| `make` target | design | what it wins | x86-64 | x86-32 | ARMv7 | bytes | memory | JIT | image |',
      '|---|---|---|---|---|---|---|---|---|---|']
for r in ROWS:
    L.append('| `%s` | %s | %s | %s | %s | %s | %s | %d KB | %s | %s |' % (r['target'], r['id'], r['wins'],
             '-' if r['x64'] is None else '%.3f' % r['x64'], '-' if r['x32'] is None else '%.3f' % r['x32'], r['arms'],
             format(r['b8'], ','), r['mem'], 'yes' if r['jit'] else 'no', r['image']))
L += ['', (FOOT + ' ' if FOOT else '') + METHOD + ' (designs/README.md, the same table.) Image: what designs/ ships at both widths. ' +
      ('Of the %s measured in all three classes, none comes within 25 %% of the best in each.' % WORD.get(len(all3), len(all3)) if not near else
       'Of the %s measured in all three classes, %s within 25 %% of the best in each.' % (WORD.get(len(all3), len(all3)), t(near))), '',
      '## What each is built from', '',
      'The genes where a design\'s expression differs from s6-cv8b\'s, by today\'s evolver (lab/evolve/evolve.py; long lists as',
      'their length; GENE=- one s6 has and the design does not). tag2: relf\'s two-bit tag format; compiler 1: clang, else GCC;',
      'opt: the optimisation level, -O2 if absent. designs/NAME/genes.4 has the same as Forth (lab/evolve/export-genes.py).', '']
for r in ROWS: L.append('- **%s** (`%s`): %s.' % (r['id'], r['target'], r['genes']))
L += ['', '### The genes', '']
for g in sorted(used):
    d_ = doc(g); L.append('- `%s` - %s' % (g, d_ if d_ else 'see lab/evolve/evolve.py, `grep -n "gene(\'%s\'" lab/evolve/evolve.py`' % g))
L += ['', '## For relf (RELF.md\'s adoption criteria)', '',
      '- **The JIT is x86 only**: %s; the %s without it (%s) are relf\'s candidates as they stand.' % (t([r for r in ROWS if r['jit']]), WORD.get(len(nojit), len(nojit)), t(nojit)),
      '- **The images are built relf\'s way** - by a cross compiler in Forth, from source, on the design\'s own engine: designs/forth/',
      '  and a design\'s genes.4 rebuild its image (`make selfhost`); the genes as Forth name each translator rewrite it uses.',
      '- **The two-bit tag** (relf\'s format, tag2=1): %s; the rest CV8 without the tag.' % t([r for r in ROWS if r['tag2']]),
      '- **Without the C library and on ARMv7**: `make libc`, `make arm` for the %s without the JIT - the clang ones (%s)' % (WORD.get(len(nojit), len(nojit)), t([r for r in nojit if r['clang']])),
      '  cross-built, the lab\'s bytes, under qemu-arm; the GCC ones (%s) built on the Tegra by its own GCC.' % t([r for r in nojit if not r['clang']])]
L += note('For relf')
L += ['- **Not measured here**: relf\'s shell workloads beyond shellmix, AArch64, RISC-V.', '',
      '## The files and how to fetch them', '',
      '- **designs/** in the repository (the bundle the owner hands over) - what to build from: each design\'s engine source,',
      '  its Makefile, its images (the "image" column) and their source; `make`, `make test`, `make selfhost`, `make 32`, `make',
      '  libc`, `make arm` from the top.',
      '- **The package** %s (lab/evolve/pack-designs.py; the owner\'s copy, not the repository): for' % A.package,
      '  each design `ID/record.json` and, at each width, `ID/cell8/`, `ID/cell4/` - `engine`, `image.img` (`./engine image.img',
      '  < program.fth`; names upper case, `BYE` ends it), `src/`, `build.txt` (each command the lab\'s build ran), `check.txt`',
      '  (the nine workloads against s6-cv8b at the same width); `SHA256SUMS`. It is the lab\'s measured build: its images are',
      '  the converter\'s (tools/layout.py), so for the self-built roles designs/\' images differ from it (smaller; the same',
      '  speed by the gate). Rebuilt byte for byte from the repository, in a built tree:',
      '  `python3 lab/evolve/pack-designs.py OUT %s %s`%s' % (A.records, ids, (' - its engines and images the checksums of %s.' % A.sha) if A.sha else '.'),
      '- **The build-out**: `sh results/drafts/roles-build-718.sh 1 . %s NAMES`, the cross GCC\'s export-arm.py --gcc,' % A.records,
      '  then `... 2 . %s NAMES` (the script\'s header; results/drafts/ship-rehearsal-737.sh the order and inputs;' % A.records,
      '  NAMES `%s`); a gate FAIL ships translator-built by `TRANSLATOR=\'NAME:REASON\'` in phase 2. A role' % named,
      '  changed later goes the same way, alone.', '',
      '## The history', '',
      'Each document stays as it was written: results/handoff-relf-%s.md and the ones it names.' % PREV_IT]
L += note('History')
L.append('')
# one logical line a bullet or paragraph (the pieces above and the notes' wrapped lines joined), then wrapped at 120
P = []
for l in '\n'.join(L).split('\n'):
    plain = l.strip() and not l.startswith(('- ', '#', '|', '    '))
    if P and P[-1].strip() and not P[-1].startswith(('#', '|', '    ')) and (l.startswith('  ') and not l.startswith('    ') or
                                                                     plain and not P[-1].startswith('- ')):
        P[-1] = P[-1].rstrip() + ' ' + l.strip()
    else: P.append(l)
W = lambda l: l if l.startswith(('|', '    ')) or len(l) <= 120 else textwrap.fill(l, 120, subsequent_indent='  ' if l.startswith('- ') else '', break_on_hyphens=False, break_long_words=False)
print('\n'.join(W(l) for l in P))
