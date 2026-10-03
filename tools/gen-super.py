#!/usr/bin/env python3
"""gen-super.py ENGINE.c SUPERS.json - generate superinstructions: one
opcode for a pair of primitives, executed as the first body, then the
second, with one dispatch instead of two.

SUPERS.json is [[first, second, opcode], ...] by kernel.4 primitive names.
Writes vm-super-table.h (dispatch entries at those opcodes) and
vm-super-bodies.h (the handlers) beside ENGINE.c, which includes them
under SUPER. The bodies are copied from the engine's own handlers, as
gen-fold.py copies them for folds: wherever the first dispatches, it jumps
to the second instead - so a body that dispatches in more than one place
stays correct.
"""
import json, os, re, sys
s = open(sys.argv[1]).read()
pairs = json.load(open(sys.argv[2]))
prims = [l.split()[1] for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'forth', 'kernel.4')) if l.startswith('PRIMITIVE')]
fend = s.index("\n}\n\n/*\n *  Program entry point")
for marker in ('#if FOLD', '#if SUPER'):           # the handlers end where the generated ones begin
    i = s.rfind(marker, 0, fend)
    if i > 0 and '#include "vm-' in s[i:i + 60]: fend = min(fend, i)
sec = s[s.index("L_noop:"):fend]
labs = [(m.start(), m.group(1)) for m in re.finditer(r'^(L_\w+):', sec, re.M)]
tab = s[s.index("static const void *const dispatch[] = {"):]
order = re.findall(r'&&(L_\w+)', tab[:tab.index("};")])
def body(name):
    lab = order[prims.index(name)]
    i = [j for j, (_, l) in enumerate(labs) if l == lab][0]
    pos, nxt = labs[i][0], labs[i + 1][0] if i + 1 < len(labs) else len(sec)
    b = sec[pos:nxt].replace(lab + ':', '', 1)
    return ''.join(l for l in b.splitlines(True) if not l.lstrip().startswith('#'))
table, bodies, esc = [], [], []
for k, (a, b, op) in enumerate(pairs):
    first = body(a).replace('NEXT();', 'goto LSB_%d;' % k)
    bodies.append('LS_%d: /* %s %s */\n%sLSB_%d:\n%s' % (k, a, b, first, k, body(b)))
    if 36 <= op < 68: esc.append('cv8_tab[%d] = &&LS_%d;' % (op, k))   # the band ESCAPE frees
    else: table.append('[%d] = &&LS_%d,' % (op, k))
d = os.path.dirname(os.path.abspath(sys.argv[1]))
open(os.path.join(d, 'vm-super-table.h'), 'w').write('\n'.join(table) + '\n')
open(os.path.join(d, 'vm-super-esc.h'), 'w').write('\n'.join(esc) + '\n')
open(os.path.join(d, 'vm-super-bodies.h'), 'w').write(''.join(bodies))
print(len(pairs), 'superinstructions')
