#!/usr/bin/env python3
"""lab/evolve/mech-census.py [--out FILE] - the constructs relf's run-time compiler mechanisms act on, counted in the
source of genapps.py's seven programs (Iteration 684: step 2 of results/drafts/search-reopen-plan-677.md - each
mechanism priced on the selection's four, the held-out three beside).

Inside colon definitions (and :NONAME), outside [ ... ], comments and strings, each word reference is classified by
how its word was defined - in the program, or in the lab's kernel.4, extend.4 and coreext.4 (brainless's prelude):
  const      a CONSTANT (its value's literal size kept: 1, 2 or 4+ bytes of operand)      - mechanism 1 (rtlit)
  var        a VARIABLE or CREATEd word; var@ / var! the ones followed by @ C@ 2@ / ! C! +! 2!   - mechanism 2
  value      a VALUE (a fetch), to: TO / IS                                               - VALUE (680), 8
  does@      a child of a defining word whose DOES> part is `@` alone; does the other children   - mechanism 3, 9
  small4/8   a call to a colon word of at most 4 / 8 words with no control flow, string or return-stack word - 4
  imm        a number followed by + - or =                                                - mechanism 5
  tick       ['] (an address literal; with to and LITERAL, mechanism 8's 9-byte form at 8-byte cells)
  defs       colon definitions and :NONAMEs (the JIT's 5-byte header each)                 - mechanism 9
Static: what is compiled, not what runs (lab/evolve/genapps-dispatch.py's counts are that). The programs are read as
genapps.py loads them: brainless from benchmark.fs, following INCLUDE, REQUIRE, S" ..." INCLUDED and its
load-part, each file once, case folded."""
import json, os, re, sys
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
A = os.path.join(HERE_, 'apps')
PROGS = [('sim16', 'sim16.fth'), ('gc16', 'gc16.fth'), ('scan', 'scan.fth'), ('evo', 'evo.fth'),
         ('wordfreq', 'wordfreq.fth'), ('minif', 'minif.fth'), ('brainless', 'brainless/benchmark.fs'),
         ('shellmix', 'shellmix.fth')]   # 685: relf 953's - relfsh's mix
CONTROL = set('IF ELSE THEN BEGIN WHILE REPEAT UNTIL AGAIN DO ?DO LOOP +LOOP EXIT RECURSE >R R> R@ I J LEAVE UNLOOP '
              'DOES> ." S" C" ABORT" [\'] \' POSTPONE TO IS CASE OF ENDOF ENDCASE [CHAR] CHAR LITERAL ['.split())
STRWORDS = {'."': '"', 'S"': '"', 'C"': '"', 'ABORT"': '"', '.(': ')'}
NAMEWORDS = {"'", "[']", 'POSTPONE', 'TO', 'IS', '[COMPILE]', 'CHAR', '[CHAR]'}
FETCH, STORE = {'@', 'C@', '2@'}, {'!', 'C!', '+!', '2!'}
def num(t):
    try: return int(t[1:], 16) if t.startswith('$') else int(t)
    except ValueError: return None
def tokens(path, seen):
    """(token, raw rest of line) in order, comments and strings dropped; INCLUDE / REQUIRE followed, each file once."""
    if path in seen or not os.path.exists(path): return
    seen.add(path); last = ''
    for line in open(path, errors='replace'):
        i = 0; s = line.rstrip('\n')
        while i < len(s):
            while i < len(s) and s[i] in ' \t': i += 1
            if i >= len(s): break
            j = i
            while j < len(s) and s[j] not in ' \t': j += 1
            t = s[i:j].upper(); i = j
            if t == '\\': break
            if t == '(': k = s.find(')', i); i = len(s) if k < 0 else k + 1; continue
            if t in STRWORDS:
                k = s.find(STRWORDS[t], i + 1); last = s[i + 1:k] if k > 0 else ''; i = len(s) if k < 0 else k + 1
                yield t, ''; continue
            if t in ('INCLUDE', 'REQUIRE', 'LOAD-PART'):    # LOAD-PART: brainless.fs's own loader, NAME.fs
                k = s[i:].split(); i = (s.index(k[0], i) + len(k[0])) if k else len(s)
                if k: yield from tokens(os.path.join(os.path.dirname(path), k[0] + ('.fs' if t == 'LOAD-PART' else '')), seen)
                continue
            if t == 'INCLUDED' and last:
                yield from tokens(os.path.join(os.path.dirname(path), last), seen); last = ''; continue
            yield t, s[i:]
def kernel_kinds():
    K = {}
    for f in ('kernel.4', 'extend.4', 'coreext.4'):
        for m in re.finditer(r'(?im)^(?:(\S+)\s+)?(CONSTANT|VARIABLE|CREATE|VALUE|2VARIABLE)\s+(\S+)', open(os.path.join(ROOT, 'forth', f), errors='replace').read()):
            K.setdefault(m.group(3).upper(), ('const', num(m.group(1) or '')) if m.group(2).upper() == 'CONSTANT' else
                         ('value', None) if m.group(2).upper() == 'VALUE' else ('var', None))
    return K
def census(path):
    T = [t for t, _ in tokens(path, set())]
    kinds = dict(KK); defs = {}; C = dict.fromkeys(('const', 'const1', 'const2', 'const4', 'var', 'var@', 'var!', 'value', 'to',
                                                      'does@', 'does', 'small4', 'small8', 'imm', 'tick', 'literal', 'defs', 'calls'), 0)
    i, n = 0, len(T)
    while i < n:                     # pass 1: what each name is
        t = T[i]
        if t == ':' and i + 1 < n:
            name = T[i + 1]; j = i + 2; body = []
            while j < n and T[j] != ';': body.append(T[j]); j += 1
            defs[name] = body
            if 'DOES>' in body and 'CREATE' in body:
                kinds[name] = ('definer', body[body.index('DOES>') + 1:])
            else:
                kinds[name] = ('colon', body)
            i = j + 1; continue
        if t in ('CONSTANT', '2CONSTANT') and i + 1 < n: kinds[T[i + 1]] = ('const', num(T[i - 1]) if i else None); i += 2; continue
        if t in ('VARIABLE', '2VARIABLE', 'CREATE') and i + 1 < n: kinds[T[i + 1]] = ('var', None); i += 2; continue
        if t in ('VALUE', '2VALUE', 'DEFER') and i + 1 < n: kinds[T[i + 1]] = ('value', None); i += 2; continue
        if t in kinds and kinds[t][0] == 'definer' and i + 1 < n:
            kinds[T[i + 1]] = ('does@' if kinds[t][1] == ['@'] else 'does', None); i += 2; continue
        i += 1
    i, inside, interp = 0, False, False; NM = {}     # per name: kind, references, references followed by @ or !
    while i < n:                     # pass 2: the references inside definitions
        t = T[i]; nx = T[i + 1] if i + 1 < n else ''
        if not inside:
            if t == ':': inside = True; C['defs'] += 1; i += 2; continue
            if t == ':NONAME': inside = True; C['defs'] += 1
            i += 1; continue
        if t == ';': inside = False; i += 1; continue
        if t == '[': interp = True; i += 1; continue
        if t == ']': interp = False; i += 1; continue
        if interp: i += 1; continue
        if t in NAMEWORDS:
            if t == "[']": C['tick'] += 1
            if t in ('TO', 'IS'): C['to'] += 1
            i += 2; continue
        if t == 'LITERAL': C['literal'] += 1; i += 1; continue
        v = num(t)
        if v is not None:
            if nx in ('+', '-', '='): C['imm'] += 1
            i += 1; continue
        k = kinds.get(t)
        if k and t not in KK:
            kk = k[0]
            if kk == 'colon' and t in defs and not (set(defs[t]) & CONTROL):
                kk = 'small4' if len(defs[t]) <= 4 else 'small8' if len(defs[t]) <= 8 else 'colon'
            e = NM.setdefault(t, [kk, 0, 0]); e[1] += 1; e[2] += nx in FETCH or nx in STORE
        if k:
            if k[0] == 'const':
                C['const'] += 1; x = k[1]
                C['const1' if x is not None and -128 <= x < 128 else 'const2' if x is not None and -32768 <= x < 32768 else 'const4'] += 1
            elif k[0] == 'var':
                C['var'] += 1
                if nx in FETCH: C['var@'] += 1
                elif nx in STORE: C['var!'] += 1
            elif k[0] in ('value', 'does@', 'does'): C[k[0]] += 1
            elif k[0] == 'colon' and t in defs:
                C['calls'] += 1; b = defs[t]
                if not (set(b) & CONTROL):
                    if len(b) <= 4: C['small4'] += 1
                    if len(b) <= 8: C['small8'] += 1
        i += 1
    C['names'] = {k: v for k, v in NM.items() if v[0] in ('const', 'var', 'colon', 'small4', 'small8', 'does', 'does@', 'value')}
    return C
KK = kernel_kinds()
R = {p: census(os.path.join(A, f)) for p, f in PROGS}
out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else os.path.join(ROOT, 'build', 'genapps', 'mech-census.json')
os.makedirs(os.path.dirname(out), exist_ok=True); json.dump(R, open(out, 'w'), indent=1)
keys = [k for k in next(iter(R.values())) if k != 'names']
print('| program | ' + ' | '.join(keys) + ' |\n|---|' + '---:|' * len(keys))
for p in R: print('| %s | %s |' % (p, ' | '.join(str(R[p][k]) for k in keys)))
f4 = {k: sum(R[p][k] for p in ('sim16', 'gc16', 'scan', 'evo')) for k in keys}
print('| **the four** | %s |' % ' | '.join(str(f4[k]) for k in keys))
