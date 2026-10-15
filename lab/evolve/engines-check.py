#!/usr/bin/env python3
"""engines-check.py - an engine down every generator's path builds, and runs
the corpus right (Iteration 249).

Seed 46 lost every design with the gene tail: an engine change (the dispatch
table as offsets, Iteration 237) broke the engines tools/gen-tail.py makes, and
no check built one - the fronts the gate builds had none. Every variant here is
s6-cv8b with genes set so that one path is taken: the cached top off, multi-
state caching (gen-msc.py), tail-call threading (gen-tail.py), superinstructions
(gen-super.py), op;CALL handlers (gen-opcall.py), format-10 opcodes, the escape
byte (both widths), the two-bit tag (narrow and wide, and with factored bodies), the JIT with every JIT
gene (and with jitos, and on the wide tag), and the file-system levels (the
libraries the converter binds). Values for list genes come from a recorded
design that has them. A variant the evolver will not express (express() drops
a gene the others rule out) is reported and fails the check: a path that can no
longer be taken is news too.

    python3 lab/evolve/engines-check.py        PASS, or FAIL and what died
"""
import glob, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E

E.setup()
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
    ('tail calls (gen-tail)', dict(tail=1), ['tail']),
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
    ('the JIT, translator -Os', dict(JIT, jitos=1), ['jit', 'jitos']),
    ('the JIT on the wide tag', dict(JIT, t2wide=1), ['jit', 't2wide']),
    ('the JIT, a 2-cell stack cache', dict(JIT, jitk=2), ['jit', 'jitk']),      # Iteration 259
    ('the JIT, a 3-cell stack cache', dict(JIT, jitk=3), ['jit', 'jitk']),
    ('link-time optimisation', dict(lto=1), ['lto']),                           # Iteration 260
    ('the JIT with link-time optimisation', dict(JIT, lto=1), ['jit', 'lto']),
    ('tail calls with link-time optimisation', dict(tail=1, lto=1), ['tail', 'lto']),
    ('goto unfactoring 32', dict(gotodup=1), ['gotodup']),
] + ([                                                                           # Iteration 262: where clang is installed
    ('clang', dict(compiler=1), ['compiler']),
    ('clang, the JIT', dict(JIT, compiler=1), ['compiler', 'jit']),
    ('clang, tail calls (gen-tail)', dict(tail=1, compiler=1), ['compiler', 'tail']),
    ('clang, -Oz', dict(compiler=1, opt='Os'), ['compiler']),
] if E.HAVE_CLANG else []) + [
] + [('fsys %d' % k, dict(fsys=k), ['fsys']) for k in (1, 2, 3, 4, 5)]

bad = []
VARIANTS += [(n + ', 2@ 2! opcodes', dict(g, ops10=list(g.get('ops10') or []) + ['2@', '2!'], opbody=1), need + ['ops10'])   # Iteration 290
             for n, g, need in list(VARIANTS) if n in ('s6 as it is', 'cached top off', 'multi-state (gen-msc)', 'tail calls (gen-tail)', 'the JIT, every JIT gene')]
VARIANTS += [(n.replace('2@ 2! opcodes', '2@ 2! inlined'), dict(g, opinline=1), need + ['opinline'])   # Iteration 292
             for n, g, need in list(VARIANTS) if n.endswith('2@ 2! opcodes')]
if E.clang_pn():   # Iteration 293: where a clang 19+ is installed
    VARIANTS += [('clang %s, tail calls with preserve_none' % E.clang_pn(), dict(tail=1, compiler=1, tailpn=1), ['compiler', 'tail', 'tailpn'])]
KN = dict(kfast=1, kinput=1, klookup=1, knumber=1)   # Iteration 295: NUMBER? as one opcode, on every engine family
VARIANTS += [('klookup, knumber', dict(KN), ['knumber']), ('klookup, knumber, cached top off', dict(KN, tos=0), ['knumber']),
             ('klookup, knumber, multi-state', dict(KN, msc=1), ['knumber', 'msc']), ('klookup, knumber, tail calls', dict(KN, tail=1), ['knumber', 'tail']),
             ('klookup, knumber, the JIT', dict(KN, **JIT), ['knumber', 'jit'])]
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
        print('  %-32s ok     engine %6d, image %6d bytes' % (name, os.path.getsize(eng), os.path.getsize(img)), flush=True)
    except Exception as e:
        bad.append(name); print('  %-32s DIED   %s' % (name, str(e)[:110]), flush=True)
shutil.rmtree(os.path.join(E.EV, 'engines-check'), ignore_errors=True)
print('PASS' if not bad else 'FAIL - %d of %d: %s' % (len(bad), len(VARIANTS), '; '.join(bad)))
sys.exit(1 if bad else 0)
