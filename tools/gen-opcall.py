#!/usr/bin/env python3
"""gen-opcall.py ENGINE.c OPCALL.json - the X;CALL handlers (Iteration 121,
the gene opcall): for each [name, opcode, label], a copy of the handler at
label with its NEXT() made CALLNEXT() - into the call after it, no table
dispatch - written as vm-opcall-table.h and vm-opcall-bodies.h beside
ENGINE.c. A handler must leave by exactly one NEXT() and no goto, or the
copy could leave some other way than into the call: refused, and the build
fails rather than run a wrong opcode."""
import json, os, re, sys
src = open(sys.argv[1]).read()
want = json.load(open(sys.argv[2]))
sec = src[src.index('L_noop:'):]
labs = [(m.start(), m.group(1)) for m in re.finditer(r'^(L_\w+):', sec, re.M)]
at = {lab: i for i, (_, lab) in enumerate(labs)}
table, bodies = [], []
for name, op, lab in want:
    if lab not in at: sys.exit('gen-opcall: no handler %s for %s' % (lab, name))
    i = at[lab]
    body = sec[labs[i][0]:labs[i + 1][0] if i + 1 < len(labs) else len(sec)]
    body = ''.join(l for l in body.splitlines(True) if not l.lstrip().startswith('#'))
    if body.count('NEXT();') != 1 or re.search(r'\bgoto\b|\breturn\b|EXITNEXT|NEXT\(\)\s*;.*NEXT', body, re.S):
        sys.exit('gen-opcall: %s (%s) does not leave by one NEXT()' % (name, lab))
    body = body.replace(lab + ':', 'LC' + lab[1:] + ':', 1).replace('NEXT();', 'CALLNEXT();')
    bodies.append(body.rstrip() + '\n'); table.append('&&LC%s,' % lab[1:])    # in order: logical 0xFE00 + k
d = os.path.dirname(os.path.abspath(sys.argv[1]))
open(os.path.join(d, 'vm-opcall-table.h'), 'w').write('\n'.join(table) + '\n')
open(os.path.join(d, 'vm-opcall-bodies.h'), 'w').write(''.join(bodies))
print(len(bodies), 'op;CALL handlers')
