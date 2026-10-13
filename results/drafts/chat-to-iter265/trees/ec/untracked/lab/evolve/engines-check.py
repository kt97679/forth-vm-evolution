#!/usr/bin/env python3
"""engines-check.py - an engine down every generator's path builds, and runs
the corpus right (Iteration 249).

Seed 46 lost every design with the gene tail: an engine change (the dispatch
table as offsets, Iteration 237) broke the engines tools/gen-tail.py makes, and
no check built one - the fronts the gate builds had none. Every variant here is
s6-cv8b with genes set so that one path is taken: the cached top off, multi-
state caching (gen-msc.py), tail-call threading (gen-tail.py), superinstructions
(gen-super.py), op;CALL handlers (gen-opcall.py), format-10 opcodes, the escape
byte (both widths), the two-bit tag (narrow and wide), the JIT with every JIT
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
    ('the JIT, every JIT gene', dict(JIT), ['jit', 'jitx', 'jitloop', 'jitinl', 'jittail']),
    ('the JIT, translator -Os', dict(JIT, jitos=1), ['jit', 'jitos']),
    ('the JIT on the wide tag', dict(JIT, t2wide=1), ['jit', 't2wide']),
] + [('fsys %d' % k, dict(fsys=k), ['fsys']) for k in (1, 2, 3, 4, 5)]

bad = []
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
