#!/usr/bin/env python3
"""results/drafts/esolangs-717.py - two ideas from the esoteric languages priced on the source the workloads interpret
(Iteration 717; results/drafts/esolangs-717.md). Run from the repository's top.

1. FALSE and Brainfuck dispatch on a token's first character; a Forth looks every token up first and tries it as a
   number only after the lookup misses - so every literal walks a whole chain. Counted here: the tokens the text
   interpreter meets in the kernel workload's source (extend.4, cross.4, kernel.4 and what they include), the corpus
   (tests/corpus/core.fth) and the held-out parse workload, and how many are plain decimal literals (-?[0-9]+) - the
   tokens a number-first path would take without a lookup, if no word's name is one (checked: the names defined in
   forth/*.4 that are digits only).
2. Befunge's '#' (skip the next cell) and the skip-next-instruction machines (PDP-8 SKP, PIC BTFSC): a one-byte
   conditional skip for an IF whose body is one word, against the ?BRANCH and its offset. Counted: IF x THEN with x
   one token, in the kernel's and the five programs' source.
A tokenizer by whitespace, comments and strings skipped - an estimate of the token stream, not a trace."""
import collections, glob, os, re

def tokens(path):
    t = open(path, encoding='latin-1').read().split()
    out, i = [], 0
    while i < len(t):
        w = t[i]; u = w.upper()
        if u == '\\':                                   # to the end of the line: re-split by lines instead
            i += 1; continue
        if u in ('(', '.('):
            while i < len(t) and not t[i].endswith(')'): i += 1
            i += 1; continue
        out.append(w)
        if u in ('."', 'S"', 'C"', 'ABORT"', ',"', '."8', 'S"8'):
            i += 1
            while i < len(t) and not t[i].endswith('"'): i += 1
        i += 1
    return out

def lines_tokens(path):                                  # drop \ comments by line first
    keep = []
    for l in open(path, encoding='latin-1'):
        m = re.search(r'(^|\s)\\(\s|$)', l)
        keep.append(l[:m.start()] if m else l)
    tmp = '\n'.join(keep)
    return tokens_from_text(tmp)

def tokens_from_text(s):
    import io, tempfile
    f = tempfile.NamedTemporaryFile('w', delete=False, suffix='.4', encoding='latin-1'); f.write(s); f.close()
    try: return tokens(f.name)
    finally: os.unlink(f.name)

def included(path, seen):
    if path in seen or not os.path.exists(path): return []
    seen.add(path); out = []
    toks = lines_tokens(path)
    for j, w in enumerate(toks):
        out.append(w)
        if w.upper() == 'INCLUDED' and j >= 1:          # S" file" INCLUDED: the file name is the token before
            pass
    for m in re.finditer(r'S"\s+(\S+)"\s+INCLUDED', open(path, encoding='latin-1').read()):
        out += included(os.path.join(os.path.dirname(path), m.group(1)), seen)
    return out

NUM = re.compile(r'^-?[0-9]+$')
def report(name, toks):
    n = len(toks); d = sum(1 for w in toks if NUM.match(w))
    lead = sum(1 for w in toks if w[:1].isdigit() and not NUM.match(w))
    print('  %-34s %7d tokens, %6d plain decimal literals (%4.1f %%), %5d digit-led names (2DUP, 1+ ...)' % (name, n, d, 100.0 * d / max(n, 1), lead))
    return n, d

print('# Two esoteric-language ideas priced on the workloads\' source (results/drafts/esolangs-717.py)')
print('\n## 1. Literals that walk a whole chain before >NUMBER sees them')
seen = set()
k = included('forth/extend.4', seen) + included('forth/cross.4', seen)
report('kernel workload (extend.4, cross.4 ...)', k)
print('    files: ' + ', '.join(sorted(os.path.basename(p) for p in seen)))
report('corpus (tests/corpus/core.fth)', lines_tokens('tests/corpus/core.fth'))
report('parse, held out (bench/parse.fth)', lines_tokens('bench/parse.fth'))
apps = sorted(glob.glob('lab/evolve/apps/*.fth'))
report('the apps (lab/evolve/apps/*.fth)', [w for p in apps for w in lines_tokens(p)])
names = collections.Counter()
for p in glob.glob('forth/*.4'):
    s = open(p, encoding='latin-1').read()
    for m in re.finditer(r'(?:^|\s)(?::|CONSTANT|VARIABLE|VALUE|CREATE|2CONSTANT)\s+(\S+)', s):
        if NUM.match(m.group(1)): names[(os.path.basename(p), m.group(1))] += 1
print('  digit-only names defined in forth/*.4: %s' % (', '.join('%s in %s' % (w, f) for (f, w) in sorted(names)) or 'none'))

print('\n## 2. IF bodies of one word (a one-byte conditional skip instead of ?BRANCH and its offset)')
CTRL = {'IF', 'ELSE', 'THEN', 'BEGIN', 'WHILE', 'REPEAT', 'UNTIL', 'AGAIN', 'DO', '?DO', 'LOOP', '+LOOP', 'EXIT', ';', 'CASE', 'OF', 'ENDOF', 'ENDCASE'}
def ifs(toks):
    u = [w.upper() for w in toks]; one = els = allif = 0
    for j, w in enumerate(u):
        if w == 'IF':
            allif += 1
            if j + 2 < len(u) and u[j + 2] == 'THEN' and u[j + 1] not in CTRL: one += 1
        if w == 'ELSE' and j + 2 < len(u) and u[j + 2] == 'THEN' and u[j + 1] not in CTRL: els += 1
    return allif, one, els
for name, toks in (('kernel.4', lines_tokens('forth/kernel.4')), ('coreext.4', lines_tokens('forth/coreext.4')),
                   ('the five programs (evo gc16 scan sim16 shellmix)', [w for a in ('evo', 'gc16', 'scan', 'sim16', 'shellmix') for w in lines_tokens('lab/evolve/apps/%s.fth' % a)])):
    a, o, e = ifs(toks)
    print('  %-48s IF %4d; IF x THEN %3d (%4.1f %%); ELSE x THEN %3d' % (name, a, o, 100.0 * o / max(a, 1), e))
