#!/usr/bin/env python3
"""lab/evolve/export-genes.py [NAME ...] - each design's genes as Forth, for forth/cross-cv8.4 (Iteration 669;
results/drafts/selfhost-plan-666.md, phases 2 and 4): designs/NAME/genes.4 and genes32.4 (8- and 4-byte cells), and
stages/s6-genes.4 for the ladder's s6-cv8b.
The values are the ones the evolver hands the translator: evolve.py's own build() runs for the design with every
command recorded, and the translator's options (tools/layout.py) and the overlays of the dump it reads are written
out as words the cross compiler includes; the engine's flags come from the design's Makefile. As the build user, in a
built tree, from the repository's top. With no NAME, every design in designs/ and s6."""
import contextlib, json, os, re, shutil, sys
NAMES = sys.argv[1:]
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
LOG, OUT = [], []; _sh = E.sh
def sh(cmd, *a, **k):
    LOG.append([str(c) for c in cmd]); r = _sh(cmd, *a, **k)
    OUT.append(r.stdout.decode('latin-1') if r.stdout else ''); return r
E.sh = sh
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.TWO_WIDTHS[0] = False     # the 4-byte references too (WIDTH4)

OVERLAY_ORDER = ['cv8.4', 'cv8b.4', 'cv8b-kfast.4', 'cv8b-kinput.4', 'cv8b-klookup.4', 'cv8b-knumber.4']
def overlays(dump):
    """The files the dump's boot loaded, in evolve.py's order (Iteration 694: its boot_files() - this list had missed
    687's -var and 691's -const)."""
    n = os.path.basename(dump)
    assert n.startswith('k64-b') or n.startswith('k32-b'), n
    return E.boot_files(n)

def opt(args, k, default=None):
    return args[args.index(k) + 1] if k in args else default

def flags(makefile):
    d = dict(re.findall(r'-D([A-Z0-9_]+)=?(\d*)', open(makefile).read()))
    return {k: int(v) if v else 1 for k, v in d.items()}

def t2map(src):
    """The engine's tag-2 map (layout.py writes it, vm-lab.c reads it): (logical op, one-byte code) and (logical
    op, escape selector) pairs - the design's ranking, which the image's bytes must follow."""
    one = [t.strip() for t in open(os.path.join(src, 'vm-tag2-one.h')).read().split(',')]
    esc = [t.strip() for t in open(os.path.join(src, 'vm-tag2-esc.h')).read().split(',')]
    o = [(int(t), i if i < 64 else 0x80 + i - 64) for i, t in enumerate(one) if t.isdigit()]
    e = [(int(t), i) for i, t in enumerate(esc) if t.isdigit()]
    return o, e

def genes(name, args, eflags, out, cell=8, src=None, tout=''):
    dump = args[0]
    ov = overlays(dump)
    spec = set((opt(args, '--spec') or '').split(',')) - {''}
    bits = sum(b for s, b in (('small', 1), ('imm', 2), ('var', 4), ('tiny', 8), ('loc', 16)) if s in spec)
    folds = (opt(args, '--fold-set') or '').split(',') if '--fold' in args else []
    sup = json.load(open(opt(args, '--supers-file'))) if '--supers-file' in args else []
    o10 = json.load(open(opt(args, '--ops10-file'))) if '--ops10-file' in args else []
    espec, ehot, etag2 = eflags.get('SPEC', 0), eflags.get('HOTCALLS', 0), eflags.get('TAG2', 0)
    feat = 1 | (2 if eflags.get('VARSLOT', 1) else 0) | (4 if espec else 0) | 8 | 16 | (32 if ehot else 0) | (64 if etag2 else 0)
    def text(s):
        # A line of a list's text: S" ... " G+, a double quote (as in (ABORT")) appended alone by 34 G-C.
        parts, w = s.split('"'), []
        for i, q in enumerate(parts):
            if q: w.append('S" %s" G+' % q)
            if i < len(parts) - 1: w.append('34 G-C')
        return ' '.join(w)
    def lst(nm, toks, what):
        # A list: G-LIST: NAME, then its text a line at a time - REFILL reads 256 characters a line at most.
        out, cur = ['G-LIST: %s  \\ %s' % (nm, what)], ''
        for t in toks:
            if cur and len(cur) + len(t) + 1 > 100: out.append(text(cur)); cur = ''
            cur += t + ' '
        if cur: out.append(text(cur))
        return out
    L = ['\\ %s - %s\'s genes for forth/cross-cv8.4, written by lab/evolve/export-genes.py from the' % (os.path.relpath(out), name),
         '\\ options the evolver hands the translator (tools/layout.py) and the engine\'s flags. Include it before',
         '\\ cross-cv8.4: S" extend.4" INCLUDED  S" genes.4" INCLUDED  S" cross-cv8.4" INCLUDED',
         '\\ A list is a word giving its text ( --- c-addr u ), names and numbers each followed by one space.',
         'VARIABLE G-AT',
         ': G-LIST: ( "name" --- ) CREATE HERE G-AT ! 0 , DOES> DUP CELL+ SWAP @ ;',
         ': G+ ( c-addr u --- ) DUP G-AT @ +! HERE SWAP DUP ALLOT CMOVE ;',
         ': G-C ( c --- ) HERE C! 1 ALLOT 1 G-AT @ +! ;']
    L += ['%d CONSTANT G-CELL          \\ the target\'s cell, bytes' % cell]
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
    if '--escape2' in args:     # the second level: nine more, as layout.py adds ESC2_PRIMS
        esc += re.search(r"ESC2_PRIMS = set\('([^']*)'", open('tools/sod16.py').read()).group(1).split()
    L += ['%d CONSTANT G-ESCAPE         \\ escaped primitives: two bytes, ESC and a selector' % (-1 if '--escape' in args else 0)]
    L += lst('G-ESC-PRIMS', esc if '--escape' in args else [], 'the escaped primitives')
    L += ['%d CONSTANT G-VARSLOT        \\ slot operands 2 or 3 bytes, high byte first; else 2, low first' % (-1 if eflags.get('VARSLOT', 1) else 0)]
    L += lst('G-REBIND', [t for t in (opt(args, '--rebind') or '').split(',') if t], "the kernel's uses rebound to the overlays' words")
    L += lst('G-HEADERLESS', [t for t in (opt(args, '--headerless') or '').split(',') if t], 'no headers')
    L += ['%d CONSTANT G-ENGINE-SPEC   \\ the engine\'s flags: SPEC (the locals block in the header)' % (1 if espec else 0),
         '%d CONSTANT G-FEATURES      \\ the image\'s feature bits (engine/vm-lab.c\'s IMAGE_MAGIC)' % feat,
         '%d CONSTANT G-MAGIC5' % (76 if espec else 0)]
    # What forth/cross-cv8.4 has no rule for yet: it refuses a design that names one.
    # --tag2: the two-bit tag (FORMAT-TAG2.md) - the engine's map, the wide form; the JIT's image side: its code,
    # the outer words' JIT header (--jitimg); --hot-inline: the sites the translator chose from the profile.
    t2 = '--tag2' in args
    o1, e1 = t2map(src) if t2 else ([], [])
    L += ['%d CONSTANT G-TAG2          \\ the two-bit tag: codes by the engine\'s map, calls 2-4 bytes, links 1-4' % (-1 if t2 else 0),
          '%d CONSTANT G-T2WIDE        \\ ...no 3-byte call: 0x80-0xBF one-byte codes' % (-1 if '--tag2-wide' in args else 0)]
    L += lst('G-T2-ONE', ['%d %d' % p for p in o1], "the engine's map: logical operation, one-byte code")
    L += lst('G-T2-ESC', ['%d %d' % p for p in e1], "...logical operation, escape selector")
    L += ['%d CONSTANT G-JIT           \\ the lazy JIT (engine/jit.c): its opcode a tag-2 code' % (-1 if '--jit' in args else 0),
          '%d CONSTANT G-JITIMG        \\ 1: the outer interpreter\'s words given the JIT header' % int(opt(args, '--jitimg', 0)),
          '%d CONSTANT G-GUARD-ABORT   \\ the gene abortif: ABORT\" guarded by ?BRANCH (sod16.guard_aborts; 714)' % (-1 if '--guard-abort' in args else 0)]
    m = re.search(r'^hot-inline: \d+ sites - (.*)$', tout, re.M)
    assert ('--hot-inline' not in args) or m, 'hot-inline: the translator named no sites'
    # The sites it printed, caller>callee#k - ambiguous where a name holds '>' (?STACK>U>#1): matched against
    # the profile's own entries, in its order.
    said = set(m.group(1).split(', ')) if m and m.group(1) else set()
    prof = json.load(open(opt(args, '--hot-inline'))) if '--hot-inline' in args else []
    hs = [(c_, t_, str(k_)) for c_, t_, k_, _ in prof if '%s>%s#%d' % (c_, t_, k_) in said]
    assert len(hs) == len(said), ('hot-inline: sites not in the profile', len(hs), len(said))
    L += lst('G-HOT-INLINE', ['%s %s %s' % h for h in hs], 'calls inlined: caller callee k (the k-th call), as the translator chose them')
    # 715: the gene factor (layout.py --factor, under the tag and byte headers only, as there): the words it may
    # factor by the reference profile - a word missing from it kept, unless --factor-share is above 1 (every word) -
    # and never the bodies layout.py patches after reading them (T2_CONSTS) or the dump tool (DUMPTOOL).
    fac = '--factor' in args and '--tag2' in args and '--bytehdr' in args
    share = float(opt(args, '--factor-share') or 1e-3)
    hotw = json.load(open(opt(args, '--factor-hot'))) if fac and '--factor-hot' in args else {}
    lsrc = open('tools/layout.py').read()
    never = [n for v in ('T2_CONSTS', 'DUMPTOOL') for n in re.findall(r"'([^']*)'", re.search(v + r' = \(([^)]*)\)', lsrc).group(1))]
    L += ['%d CONSTANT G-FACTOR        \\ the gene factor: repeated cold code in headerless bodies (layout.py --factor; 715)' % (-1 if fac else 0),
          '%d CONSTANT G-FACTOR-ANY    \\ ...every word, the profile aside (--factor-share above 1)' % (-1 if fac and share > 1.0 else 0)]
    L += lst('G-FACTOR-COLD', sorted(n for n, s in hotw.items() if s < share) if fac else [], "...the words below --factor-share of the reference dispatches")
    L += lst('G-FACTOR-NOT', never if fac else [], "...never: what layout.py patches after reading it, the dump tool")
    ny = [k for k in ('--opcall-file',) if k in args]       # 714: --guard-abort done; 715: --factor (G-FACTOR 0 where layout.py ignores it)
    # 722: =I?BRANCH(8) and DUP?NBRANCH(8) done (cross-cv8.4's EQI-PASS and KEEP-PASS)
    L += lst('G-NOT-YET', ny, "the translator's options the cross compiler does not do yet")
    assert max(len(l) for l in L) < 250, 'a genes line too long for REFILL'
    open(out, 'w').write('\n'.join(L) + '\n')
    print(out, '-', len(ov), 'overlays,', len(folds), 'folds, spec', bits, ',', len(o10), 'ops10,', len(sup), 'pairs')

DS = os.environ.get('DESIGNS', 'designs')   # 675: another designs directory (tools/selfhost-ship.sh)
ROLES = sorted(d for d in os.listdir(DS) if os.path.exists(os.path.join(DS, d, 'record.json')))
for name in NAMES or (['s6'] + ROLES):
    if name == 's6':
        hot = re.search(r"^HOT='([^']*)'", open('tools/build-stages.sh').read(), re.M).group(1)
        args = ['k64-b.txt', '8', '--v8', '--cpt', '0', '--bytehdr', '--dataprims', '--fold', '--fold-set', hot,
                '--spec', 'loc,var,tiny,small,imm', '--cv8-compiler', '--drop-x8', '--drop-dumptool']
        genes('s6-cv8b', args, {'SPEC': 1, 'VARSLOT': 1}, 'stages/s6-genes.4'); continue
    g = json.load(open(os.path.join(DS, name, 'record.json')))['genome']
    for cell in (8, 4):
        # As export-designs.py builds image.img and image32.img: the 4-byte build at_width(WIDTH4).
        b = os.path.join(E.EV, 'genes-%s-%d' % (name, cell)); shutil.rmtree(b, ignore_errors=True)
        del LOG[:]; del OUT[:]
        with (E.at_width(E.WIDTH4) if cell == 4 else contextlib.nullcontext()): E.build(E.canon(g), b)
        k = [i for i, c in enumerate(LOG) if any(x.endswith('tools/layout.py') for x in c)][-1]
        c = LOG[k]
        args = c[[k for k, x in enumerate(c) if x.endswith('tools/layout.py')][0] + 1:]
        assert args[1] == str(cell), args[:2]
        out = os.path.join(DS, name, 'genes.4' if cell == 8 else 'genes32.4')
        src = os.path.join(DS, name, 'src' if cell == 8 else 'src32')
        try: genes(name, args, flags(os.path.join(DS, name, 'Makefile')), out, cell, src, OUT[k])
        except AssertionError as e: print(name, cell, '- skipped:', e)
