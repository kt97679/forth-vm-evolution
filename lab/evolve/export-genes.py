#!/usr/bin/env python3
"""lab/evolve/export-genes.py [NAME ...] - each design's genes as Forth, for forth/cross-cv8.4 (Iteration 669;
results/drafts/selfhost-plan-666.md, phase 2): designs/NAME/genes.4, and stages/s6-genes.4 for the ladder's s6-cv8b.
The values are the ones the evolver hands the translator: evolve.py's own build() runs for the design with every
command recorded, and the translator's options (tools/layout.py) and the overlays of the dump it reads are written
out as words the cross compiler includes; the engine's flags come from the design's Makefile. As the build user, in a
built tree, from the repository's top. With no NAME, every design in designs/ and s6."""
import json, os, re, shutil, sys
NAMES = sys.argv[1:]
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
LOG = []; _sh = E.sh
def sh(cmd, *a, **k):
    LOG.append([str(c) for c in cmd]); return _sh(cmd, *a, **k)
E.sh = sh
E.setup()

OVERLAY_ORDER = ['cv8.4', 'cv8b.4', 'cv8b-kfast.4', 'cv8b-kinput.4', 'cv8b-klookup.4', 'cv8b-knumber.4']
def overlays(dump):
    """The files the dump's boot loaded, in evolve.py setup()'s order (tag-2 dumps aside: phase 3)."""
    n = os.path.basename(dump)
    assert n.startswith('k64-b') or n.startswith('k32-b'), n
    assert not n[5:].startswith('t'), 'a tag-2 dump: phase 3'
    fs = ['cv8.4', 'cv8b.4'] + [f for f, k in (('cv8b-kfast.4', '-kfast'), ('cv8b-kinput.4', '-kinput'),
                                               ('cv8b-klookup.4', '-klookup'), ('cv8b-knumber.4', '-knumber')) if k in n]
    fs += ['cv8-fuse.4'] if '-fuse' in n else []
    fs += ['cv8-fuse-imm.4'] if '-imm' in n else []
    fs += ['cv8-fuse-loopall.4'] if '-loopall' in n else []
    fs += ['cv8-fuse-iplus.4'] if '-iplus' in n else []
    fs += ['file-sysc.4'] if '-fsys' in n else []
    fs += ['file-sysc2.4'] if ('-fsys2' in n or '-fsys3' in n) else []
    fs += ['file-sysc3.4'] if '-fsys3' in n else []
    return fs

def opt(args, k, default=None):
    return args[args.index(k) + 1] if k in args else default

def flags(makefile):
    d = dict(re.findall(r'-D([A-Z0-9_]+)=?(\d*)', open(makefile).read()))
    return {k: int(v) if v else 1 for k, v in d.items()}

def genes(name, args, eflags, out):
    dump = args[0]
    ov = overlays(dump)
    spec = set((opt(args, '--spec') or '').split(',')) - {''}
    bits = sum(b for s, b in (('small', 1), ('imm', 2), ('var', 4), ('tiny', 8), ('loc', 16)) if s in spec)
    folds = (opt(args, '--fold-set') or '').split(',') if '--fold' in args else []
    sup = json.load(open(opt(args, '--supers-file'))) if '--supers-file' in args else []
    o10 = json.load(open(opt(args, '--ops10-file'))) if '--ops10-file' in args else []
    espec, ehot, etag2 = eflags.get('SPEC', 0), eflags.get('HOTCALLS', 0), eflags.get('TAG2', 0)
    feat = 1 | (2 if eflags.get('VARSLOT', 1) else 0) | (4 if espec else 0) | 8 | 16 | (32 if ehot else 0) | (64 if etag2 else 0)
    def lst(nm, toks, what):
        # A list: G-LIST: NAME, then its text a line at a time - REFILL reads 256 characters a line at most.
        out, cur = ['G-LIST: %s  \\ %s' % (nm, what)], ''
        for t in toks:
            if cur and len(cur) + len(t) + 1 > 100: out.append('S" %s" G+' % cur); cur = ''
            cur += t + ' '
        if cur: out.append('S" %s" G+' % cur)
        return out
    L = ['\\ %s - %s\'s genes for forth/cross-cv8.4, written by lab/evolve/export-genes.py from the' % (os.path.relpath(out), name),
         '\\ options the evolver hands the translator (tools/layout.py) and the engine\'s flags. Include it before',
         '\\ cross-cv8.4: S" extend.4" INCLUDED  S" genes.4" INCLUDED  S" cross-cv8.4" INCLUDED',
         '\\ A list is a word giving its text ( --- c-addr u ), names and numbers each followed by one space.',
         'VARIABLE G-AT',
         ': G-LIST: ( "name" --- ) CREATE HERE G-AT ! 0 , DOES> DUP CELL+ SWAP @ ;',
         ': G+ ( c-addr u --- ) DUP G-AT @ +! HERE SWAP DUP ALLOT CMOVE ;']
    L += lst('G-OVERLAYS', ov, 'after kernel.4, in this order')
    L += lst('G-FOLDS', folds, 'the fold set: FOLD-BASE + place')
    L += ['%d CONSTANT G-SPEC          \\ the specialisations: 1 small, 2 imm, 4 var, 8 tiny, 16 loc' % bits]
    L += lst('G-SUPERS', ['%s %s %d' % (a, b, n) for a, b, n in sup], 'fused pairs: first second opcode')
    L += lst('G-OPS10', ['%s %d' % (a, n) for a, n in o10], 'format-10 operations: name opcode')
    L += [
          '%d CONSTANT G-HOTCALLS      \\ one-byte calls, at most' % (int(opt(args, '--hotcalls', 0)) if ehot else 0),
         '%d CONSTANT G-OP-BODIES     \\ the format-10 words\' bodies their opcode' % (-1 if '--op-bodies' in args else 0),
         '%d CONSTANT G-OP-INLINE     \\ ...placed among the primitives' % (-1 if '--op-inline' in args else 0),
         '%d CONSTANT G-BSS           \\ TIB, POCKET, INCLUDE-BUFFER past the image\'s end' % (-1 if '--bss' in args else 0),
         '%d CONSTANT G-THIN-HEADER   \\ one empty thread head in the file' % (-1 if '--thin-header' in args else 0),
         '%d CONSTANT G-THREADS       \\ the dictionary\'s hash threads' % int(opt(args, '--threads', 32)),
         '%d CONSTANT G-RTFUSE        \\ the run-time fuser\'s tables filled (cv8-fuse.4\'s SUPER-TABLE, IMM-OPS)' % (-1 if '--rtfuse' in args else 0),
          ]
    # --escape: the rarely used primitives behind ESC (0x7D) and a selector, the others closing up
    # (tools/sod16.py's ESC_PRIMS_ALL and cv8_op; the engine's -DESCAPE=1)
    esc = re.search(r'ESC_PRIMS_ALL = set\(\"\"\"(.*?)\"\"\"', open('tools/sod16.py').read(), re.S).group(1).split()
    L += ['%d CONSTANT G-ESCAPE         \\ escaped primitives: two bytes, ESC and a selector' % (-1 if '--escape' in args else 0)]
    L += lst('G-ESC-PRIMS', esc if '--escape' in args else [], 'the escaped primitives')
    L += ['%d CONSTANT G-VARSLOT        \\ slot operands 2 or 3 bytes, high byte first; else 2, low first' % (-1 if eflags.get('VARSLOT', 1) else 0)]
    L += lst('G-REBIND', [t for t in (opt(args, '--rebind') or '').split(',') if t], "the kernel's uses rebound to the overlays' words")
    L += lst('G-HEADERLESS', [t for t in (opt(args, '--headerless') or '').split(',') if t], 'no headers')
    L += ['%d CONSTANT G-ENGINE-SPEC   \\ the engine\'s flags: SPEC (the locals block in the header)' % (1 if espec else 0),
         '%d CONSTANT G-FEATURES      \\ the image\'s feature bits (engine/vm-lab.c\'s IMAGE_MAGIC)' % feat,
         '%d CONSTANT G-MAGIC5' % (76 if espec else 0)]
    # What forth/cross-cv8.4 has no rule for yet: it refuses a design that names one.
    ny = [k for k in ('--escape2', '--tag2', '--hot-inline', '--jit', '--opcall-file', '--guard-abort') if k in args]
    ny += [n for n in ('=I?BRANCH', '=I?BRANCH8', 'DUP?NBRANCH', 'DUP?NBRANCH8') if n in dict(o10)]
    L += lst('G-NOT-YET', ny, "the translator's options the cross compiler does not do yet")
    assert max(len(l) for l in L) < 250, 'a genes line too long for REFILL'
    open(out, 'w').write('\n'.join(L) + '\n')
    print(out, '-', len(ov), 'overlays,', len(folds), 'folds, spec', bits, ',', len(o10), 'ops10,', len(sup), 'pairs')

ROLES = sorted(d for d in os.listdir('designs') if os.path.exists(os.path.join('designs', d, 'record.json')))
for name in NAMES or (['s6'] + ROLES):
    if name == 's6':
        hot = re.search(r"^HOT='([^']*)'", open('tools/build-stages.sh').read(), re.M).group(1)
        args = ['k64-b.txt', '8', '--v8', '--cpt', '0', '--bytehdr', '--dataprims', '--fold', '--fold-set', hot,
                '--spec', 'loc,var,tiny,small,imm', '--cv8-compiler', '--drop-x8', '--drop-dumptool']
        genes('s6-cv8b', args, {'SPEC': 1, 'VARSLOT': 1}, 'stages/s6-genes.4'); continue
    g = json.load(open(os.path.join('designs', name, 'record.json')))['genome']
    b = os.path.join(E.EV, 'genes-%s' % name); shutil.rmtree(b, ignore_errors=True)
    del LOG[:]
    E.build(E.canon(g), b)
    c = [c for c in LOG if any(x.endswith('tools/layout.py') for x in c)][-1]
    args = c[[k for k, x in enumerate(c) if x.endswith('tools/layout.py')][0] + 1:]
    try: genes(name, args, flags(os.path.join('designs', name, 'Makefile')), os.path.join('designs', name, 'genes.4'))
    except AssertionError as e: print(name, '- skipped:', e)
