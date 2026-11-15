#!/usr/bin/env python3
"""lab/evolve/mech-price.py - relf's run-time compiler mechanisms priced in code bytes on genapps.py's seven programs
(Iteration 684: step 2 of results/drafts/search-reopen-plan-677.md). The counts: lab/evolve/mech-census.py's (its JSON);
the cost of each construct on each system: results/generic-apps-674.md's table at 8-byte cells (genapps-constructs.py).
A mechanism's saving on a system: its instances times (the system's cost less what relf reaches - relf64's, or
relfasm64's for the address literals); for constants, the constant's call less a literal of its value's size, where that is not longer (a large value's
literal is: rtlit's form applies only there). Prints
a table per mechanism: the four, the held-out three, on s6 and four designs. Bytes only - dispatches are the
profiler's (genapps-dispatch.py)."""
import json, os, re
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
C = json.load(open(os.path.join(ROOT, 'build', 'genapps', 'mech-census.json')))
t = open(os.path.join(ROOT, 'results', 'generic-apps-674.md')).read()
tab = t[t.index('| construct | s6'):].split('\n\n')[0].split('\n')
cols = [c.strip() for c in tab[0].strip('|').split('|')][1:]
cost = {r.strip('|').split('|')[0].strip(): dict(zip(cols, (float(x) for x in r.strip('|').split('|')[1:]))) for r in tab[2:]}
SYS = ['s6', 'smallest', 'portable-knee', 'small-jit', 'fastest-x86-64']
FOUR, HELD = ('sim16', 'gc16', 'scan', 'evo'), ('wordfreq', 'minif', 'brainless')
SM = ('shellmix',) if 'shellmix' in C else ()      # 685: relf 953's, relfsh's mix (the selection's fifth since 686)
def n(progs, k): return sum(C[p][k] for p in progs)
def saved(s, progs):
    c = lambda k: cost[k][s]
    lit = {'const1': c('literal 5'), 'const2': c('literal 1000'), 'const4': c('literal 100000')}
    return {
      '1 constants as literals, where not longer': sum(n(progs, b) * max(0.0, c('a constant') - lit[b]) for b in lit),
      '2 a data word\'s @ and ! as one op': n(progs, 'var@') * (c('a variable @') - cost['a variable @']['relf64'])
                                            + n(progs, 'var!') * (c('a variable !') - cost['a variable !']['relf64']),
      '3 DOES> @ as VAR@ (bytes about even: a call for a slot op)': 0.0,
      '5 n + - = as one op': n(progs, 'imm') * (c('5 +') - cost['5 +']['relf64']),
      "8 address literals in 5 bytes ([']; TO)": n(progs, 'tick') * (c("['] DUP") - cost["['] DUP"]['relfasm64'])
                                                 + n(progs, 'to') * (c('TO a VALUE') - cost['TO a VALUE']['relfasm64']),
      '9 no JIT header (5 bytes a definition)': n(progs, 'defs') * 5.0 if s in ('small-jit', 'fastest-x86-64', 'best-all-round', 'fastest-x86-32') else 0.0}
rows = {}
for s in SYS:
    for progs, tag in ((FOUR, 'four'), (HELD, 'held')) + (((SM, 'sm'),) if SM else ()):
        for k, v in saved(s, progs).items(): rows.setdefault(k, {})[(s, tag)] = v
print('| mechanism | ' + ' | '.join('%s: four / held-out%s' % (s, ' / shellmix' if SM else '') for s in SYS) + ' |\n|---|' + '---:|' * len(SYS))
for k, v in rows.items(): print('| %s | %s |' % (k, ' | '.join('%d / %d' % (round(v[(s, 'four')]), round(v[(s, 'held')])) + (' / %d' % round(v[(s, 'sm')]) if SM else '') for s in SYS)))
print('| the instances, the four / held-out | ' + '; '.join('%s %d/%d' % (k, n(FOUR, k), n(HELD, k)) for k in ('const', 'var@', 'var!', 'imm', 'tick', 'to', 'defs', 'small4', 'does')) + ' |')
