#!/usr/bin/env python3
"""results/drafts/branch-census-713.py REPO - the branch-compiling words in kernel.4 and the five selection programs, a word count (Iteration 713, early-games-713.md)."""
import re, sys, os
ROOT = sys.argv[1]
def strip(t):
    t = re.sub(r'\\ [^\n]*', ' ', t)                  # \ comments
    t = re.sub(r'(?<!\S)\( [^)]*\)', ' ', t)           # ( comments )
    return t
words = {'IF': '0br', 'ELSE': 'br', 'WHILE': '0br', 'UNTIL': '0br', 'REPEAT': 'br', 'AGAIN': 'br', 'AHEAD': 'br'}
def census(files):
    c = {}
    for f in files:
        t = strip(open(f, errors='replace').read()).upper().split()
        for w in t:
            if w in words: c[w] = c.get(w, 0) + 1
    return c
apps = [os.path.join(ROOT, 'lab/evolve/apps', f) for f in ('sim16.fth', 'gc16.fth', 'scan.fth', 'evo.fth', 'shellmix.fth')]
kern = [os.path.join(ROOT, 'forth/kernel.4')]
for name, fs in (('kernel.4', kern), ('the five programs', apps)):
    c = census(fs); print('%-18s %4d branches: %s' % (name, sum(c.values()), ', '.join('%s %d' % kv for kv in sorted(c.items()))))
