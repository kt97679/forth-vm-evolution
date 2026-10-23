#!/usr/bin/env python3
"""engines-check.py - an engine down every generator's path builds, and runs
the corpus right (Iteration 249).

Iteration 456: the tail engines removed (tail frozen off since 450), their paths with them. Seed 46 lost every design with the gene tail: an engine change (the dispatch
table as offsets, Iteration 237) broke the engines tools/gen-tail.py makes, and
no check built one - the fronts the gate builds had none. Every variant here is
s6-cv8b with genes set so that one path is taken: the cached top off, multi-
state caching (gen-msc.py), tail-call threading (gen-tail.py), superinstructions
(gen-super.py), op;CALL handlers (gen-opcall.py), format-10 opcodes, the escape
byte (both widths), the two-bit tag (narrow and wide, and with factored bodies), the JIT with every JIT
gene (and with jitos, and on the wide tag), and the file-system levels (the
libraries the converter binds); the bfind walks at 4-byte cells too (Iteration 399). Values for list genes come from a recorded
design that has them. A variant the evolver will not express (express() drops
a gene the others rule out) is reported and fails the check: a path that can no
longer be taken is news too.

    python3 lab/evolve/engines-check.py        PASS, or FAIL and what died
"""
import contextlib, glob, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E

E.TWO_WIDTHS[0] = True; E.setup_widths(); E.TWO_WIDTHS[0] = False   # Iteration 399: the 4-byte references too
S6 = dict(E.HUMAN['s6-cv8b'])

def donor(gene):
    """A recorded design's value for a list gene - the newest found."""
    val = None
    for f in sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*-seed*.md'))):
        for l in open(f):
            if l.startswith('{"bin"'):
                try: g = json.loads(l)['genome']
                except (ValueError, KeyError): continue
                if g.get(gene): val = g[gene]
    return val

JIT = dict(tag2=1, jit=1, jitx=1, jitloop=1, jitinl=1, jittail=1)   # the JIT and op;CALL live under the tag
VARIANTS = [                                     # (name, genes set on s6, genes that must be expressed)
    ('s6 as it is', {}, []),
    ('cached top off', dict(tos=0), []),
    ('multi-state (gen-msc)', dict(msc=1), ['msc']),
    ('superinstructions (gen-super)', dict(supers=donor('supers')), ['supers']),
    ('op;CALL (gen-opcall)', dict(tag2=1, opcall=donor('opcall')), ['opcall']),
    ('format-10 opcodes', dict(ops10=donor('ops10')), ['ops10']),
    ('escape byte', dict(escape=1), ['escape']),
    ('escape byte, wide', dict(escape=2), ['escape']),
    ('two-bit tag', dict(tag2=1), ['tag2']),
    ('two-bit tag, wide', dict(tag2=1, t2wide=1), ['tag2', 't2wide']),
    ('factored bodies (the tag)', dict(tag2=1, factor=3), ['tag2', 'factor']),        # Iteration 267: the gene factor
    ('the JIT with factored bodies', dict(JIT, factor=3), ['jit', 'factor']),
    ('the JIT, every JIT gene', dict(JIT), ['jit', 'jitx', 'jitloop', 'jitinl', 'jittail']),
    ('the JIT with jitmul', dict(JIT, jitmul=1), ['jit', 'jitmul']),                  # Iteration 472: UM*, UM/MOD, COUNT native
    ('the JIT, jitimg and jitvar', dict(JIT, jitimg=1, jitvar=1), ['jitimg', 'jitvar']),     # Iteration 343
    ('the JIT, jitret', dict(JIT, jitret=1), ['jitret']),                       # Iteration 404: EXIT as pop and jmp
    ('the JIT, jitvar, varslot 0', dict(JIT, jitvar=1, varslot=0), ['jitvar']),
    ('the JIT, jitvar, varslot 1', dict(JIT, jitvar=1, varslot=1), ['jitvar']),
    ('the JIT, translator -Os', dict(JIT, jitos=1), ['jit', 'jitos']),
    ('the JIT on the wide tag', dict(JIT, t2wide=1), ['jit', 't2wide']),
    ('the JIT, a 2-cell stack cache', dict(JIT, jitk=2), ['jit', 'jitk']),      # Iteration 259
    ('the JIT, a 3-cell stack cache', dict(JIT, jitk=3), ['jit', 'jitk']),
    ('link-time optimisation', dict(lto=1), ['lto']),                           # Iteration 260
    ('the JIT with link-time optimisation', dict(JIT, lto=1), ['jit', 'lto']),
    ('goto unfactoring 32', dict(gotodup=1), ['gotodup']),
] + ([                                                                           # Iteration 262: where clang is installed
    ('clang', dict(compiler=1), ['compiler']),
    ('clang, the JIT', dict(JIT, compiler=1), ['compiler', 'jit']),
    ('clang, -Oz', dict(compiler=1, opt='Os'), ['compiler']),
] if E.HAVE_CLANG else []) + [
] + [('fsys %d' % k, dict(fsys=k), ['fsys']) for k in (1, 2, 3, 4, 5)]

bad = []
VARIANTS += [(n + ', 2@ 2! opcodes', dict(g, ops10=list(g.get('ops10') or []) + ['2@', '2!'], opbody=1), need + ['ops10'])   # Iteration 290
             for n, g, need in list(VARIANTS) if n in ('s6 as it is', 'cached top off', 'multi-state (gen-msc)', 'tail calls (gen-tail)', 'the JIT, every JIT gene')]
VARIANTS += [(n.replace('2@ 2! opcodes', '2@ 2! inlined'), dict(g, opinline=1), need + ['opinline'])   # Iteration 292
             for n, g, need in list(VARIANTS) if n.endswith('2@ 2! opcodes')]
KN = dict(kfast=1, kinput=1, klookup=1, knumber=1)   # Iteration 295: NUMBER? as one opcode, on every engine family
VARIANTS += [('klookup, knumber', dict(KN), ['knumber']), ('klookup, knumber, cached top off', dict(KN, tos=0), ['knumber']),
             ('klookup, knumber, multi-state', dict(KN, msc=1), ['knumber', 'msc']),
             ('klookup, knumber, the JIT', dict(KN, **JIT), ['knumber', 'jit'])]
VARIANTS += [('handler entries aligned to 32, padding at most 10', dict(alignhot=1), ['alignhot']),   # Iteration 298
             ('handler entries aligned to 32', dict(alignhot=2), ['alignhot']), ('handler entries aligned to 64', dict(alignhot=3), ['alignhot']),
             ('aligned to 64, cached top off', dict(alignhot=3, tos=0), ['alignhot'])]
VARIANTS += [(n + ', > 0= inlined', dict(g, ops10=['>', '0='] + list(g.get('ops10') or []), opbody=1, opinline=1), need + ['ops10', 'opinline'])   # Iteration 299
             for n, g, need in list(VARIANTS) if n in ('s6 as it is', 'cached top off', 'multi-state (gen-msc)', 'tail calls (gen-tail)', 'the JIT, every JIT gene')]
# Iteration 316: the gene bfind - THREAD-FIND's and (FIND)'s walk branch-light - with each of
# the two words, in each link form (CV8's 1-3 bytes, TAG2's 1-4)
# Iteration 399: tos 0 - a TOS engine's THREAD-FIND and (FIND) are tools/gen-tos.py's own bodies, the plain walk:
# on s6 (tos 1) these four had built no bf_walk at all, at either width.
VARIANTS += [('bfind: THREAD-FIND, CV8', {'kfast': 1, 'tfind': 1, 'bfind': 1, 'tos': 0}, ['bfind']),
             ('bfind: (FIND), CV8', {'kfast': 1, 'kinput': 1, 'klookup': 1, 'bfind': 1, 'tos': 0}, ['bfind']),
             ('bfind: THREAD-FIND, TAG2', {'tag2': 1, 'kfast': 1, 'tfind': 1, 'bfind': 1, 'tos': 0}, ['bfind']),
             ('bfind: (FIND), TAG2', {'tag2': 1, 'kfast': 1, 'kinput': 1, 'klookup': 1, 'bfind': 1, 'tos': 0}, ['bfind'])]
# Iteration 402: and on s6 itself, a TOS design - gen-tos.py's bodies now take the engine's NAME_WALK, so bfind is built
# there too (it had not been, Iteration 399); checked built below, the engine not the same without it.
VARIANTS += [('bfind: THREAD-FIND, CV8, tos', {'kfast': 1, 'tfind': 1, 'bfind': 1}, ['bfind']),
             ('bfind: (FIND), TAG2, tos', {'tag2': 1, 'kfast': 1, 'kinput': 1, 'klookup': 1, 'bfind': 1}, ['bfind'])]
# Iteration 312: designs that once failed (lab/evolve/regressions.json) - each the whole recorded
# genome, built and run on the corpus every time: a fault found once stays a test.
VARIANTS += [('regression %s (seed %s)' % (r['id'], r['seed']), r['genome'], [])
             for r in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'regressions.json')))]
for name, genes, must in VARIANTS:
    g = E.canon(dict(S6, **genes))
    ex = E.express(g)
    lost = [k for k in must if not ex.get(k)]
    if lost:
        bad.append(name); print('  %-32s NOT EXPRESSED: %s' % (name, ', '.join(lost)), flush=True); continue
    d = os.path.join(E.EV, 'engines-check'); shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(g, d)
        E.alive(eng, img, E.private_work(d))
        if name.endswith(', tos') and 'bfind' in must:   # Iteration 402: built, not only expressed
            d0 = d + '-0'; shutil.rmtree(d0, ignore_errors=True); e0, _ = E.build(E.canon(dict(g, bfind=0)), d0)
            if open(e0, 'rb').read() == open(eng, 'rb').read(): raise RuntimeError('bfind inert: the same engine without it')
            shutil.rmtree(d0, ignore_errors=True)
        print('  %-32s ok     engine %6d, image %6d bytes' % (name, os.path.getsize(eng), os.path.getsize(img)), flush=True)
    except Exception as e:
        bad.append(name); print('  %-32s DIED   %s' % (name, str(e)[:110]), flush=True)
# Iteration 399 (HANDOFF open item 0f): the bfind variants at 4-byte cells too, built as eval32 builds a design -
# a 32-bit x86 engine, the JIT off. bf_walk read its 8-byte signature into UNS64, which is the cell - 4 bytes
# there - so a name of 4 to 7 characters matched the newest of its length and first three: 34 of seed 59's
# front (bfind, no tos) died on the corpus at 32 bits, and nothing here built bfind at 4-byte cells.
# Iteration 400: and every tail-call engine - preprocessed for x86-64 and compiled for i386 (__int128), then the i386
# SYSCALL's local label taken for a handler: no tail design had ever built at 4-byte cells (seed 58: 401 of 401).
# Iteration 401: clang's tail engine without preserve_none too - musttail is now on every clang tail engine; without it,
# at 4-byte cells clang made none of its dispatches jumps ('tail calls not jumps', results/fail32-400.md).
V32 = [(name + ', 32 bits', genes, must) for name, genes, must in VARIANTS if 'bfind' in must or 'tail' in must]
for name, genes, must in V32:
    g = E.canon(dict(S6, **dict(genes, jit=0)))
    d = os.path.join(E.EV, 'engines-check'); shutil.rmtree(d, ignore_errors=True)
    try:
        with E.at_width(E.WIDTH4):
            eng, img = E.build(g, d)
            E.alive(eng, img, E.private_work(d))
        print('  %-32s ok     engine %6d, image %6d bytes' % (name, os.path.getsize(eng), os.path.getsize(img)), flush=True)
    except Exception as e:
        bad.append(name); print('  %-32s DIED   %s' % (name, str(e)[:110]), flush=True)
# Iteration 416 (the owner: programs past 4 MB): calls across 4.9 MB of dictionary, links past the three-byte form,
# a DOES> child far from its word and a DOES> word far out - on s6 (plain CV8, where the call reached 2 MB, the link
# 4 MB and DOES> 2 MB), on the two-bit tag, and at 4-byte cells (results/drafts/bigprog-416.py).
BIGFILL = ''.join(': F%02d %d ;  49152 ALLOT\n' % (i, i) for i in range(100))
BIG = [(': A0 1 ;\n: MK CREATE , DOES> @ 1+ ;\nVARIABLE V0  5 V0 !\n' + BIGFILL + ": B1 A0 1+ ;\n: B2 B1 B1 + ;\n7 MK C7\n"
        ": B3 C7 V0 @ + ;\nVARIABLE V1  42 V1 !\n: B4 V1 @ B2 + ;\n' B4 CONSTANT XT4\n: B5 XT4 EXECUTE 1+ ;\n"
        ": B6 B5 B3 + F50 + F99 + ;\nB6 . CR\nBYE\n", '209'),
       (BIGFILL + ': MK2 CREATE , DOES> @ 2 + ;\n3 MK2 D3\nD3 . CR\nBYE\n', '5')]
VBIG = [('past 4 MB, s6', {}, 8), ('past 4 MB, the two-bit tag', {'tag2': 1}, 8), ('past 4 MB, s6 at 4-byte cells', {'jit': 0}, 4)]
for name, genes, w in VBIG:
    d = os.path.join(E.EV, 'engines-check'); shutil.rmtree(d, ignore_errors=True)
    try:
        with (E.at_width(E.WIDTH4) if w == 4 else contextlib.nullcontext()):
            eng, img = E.build(E.canon(dict(S6, **genes)), d); pw = E.private_work(d)
            for prog, want in BIG:
                r = E.sh([eng, img], cwd=pw, inp=prog.encode(), timeout=120, cpu=60)
                got = [l.strip() for l in (r.stdout or b'').decode(errors='replace').replace('\r', '').splitlines() if l.strip() not in ('', 'OK')]
                if want not in got: raise RuntimeError('wanted %s, got %s' % (want, ' / '.join(got[-2:])[:80]))
        print('  %-32s ok     two programs past 4 MB' % name, flush=True)
    except Exception as e:
        bad.append(name); print('  %-32s DIED   %s' % (name, str(e)[:110]), flush=True)
shutil.rmtree(os.path.join(E.EV, 'engines-check'), ignore_errors=True)
print('PASS' if not bad else 'FAIL - %d of %d: %s' % (len(bad), len(VARIANTS) + len(V32) + len(VBIG), '; '.join(bad)))
sys.exit(1 if bad else 0)
