#!/usr/bin/env python3
"""results/drafts/chainorder-use-732.py OUT - the gene chainorder's use file (Iteration 732): each name looked up in the
held-out programs (lab/evolve/apps: wordfreq, minif, brainless - never the selection's), with its count, by
results/drafts/lookup-cache-model.py's tokeniser (the words the outer interpreter looks up, comments and strings out;
numbers left out). tools/layout.py --chainorder orders each chain by it - most looked-up first, the rest newest first as
today - and forth/cross-cv8.4 the same from genes.4. A fixed file, committed (lab/evolve/chainorder-use.txt), so every
build is deterministic; written again only when the held-out programs change. Reads only; python3 -B, as the build user."""
import collections, glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(HERE, 'lookup-cache-model.py')).read()
body = src[src.index('def h(n, T):'):src.index('works = {}')]
ns = {'re': re, 'collections': collections, 'os': os}; exec(body, ns); lookups, strip = ns['lookups'], ns['strip_line_comments']
APPS = os.path.join(ROOT, 'lab', 'evolve', 'apps'); t = ''
for a in ('wordfreq', 'minif', 'brainless'):
    p = os.path.join(APPS, a + '.fth')
    t += open(p, errors='replace').read() if os.path.exists(p) else ''.join(open(f, errors='replace').read() for f in sorted(glob.glob(os.path.join(APPS, a, '*.f*'))))
num = re.compile(r"^[-+]?(\$[0-9A-F]+|#?[0-9]+|%[01]+|'.')\.?$", re.I)
c = collections.Counter(n for k, n in lookups(strip(t)) if k == 'find' and not num.match(n))
with open(sys.argv[1], 'w') as f:
    f.write('# lab/evolve/chainorder-use.txt - the gene chainorder\'s use counts (results/drafts/chainorder-use-732.py):\n'
            '# a name\'s lookups in the held-out programs wordfreq, minif and brainless. COUNT NAME, most first.\n')
    for n, k in sorted(c.items(), key=lambda x: (-x[1], x[0])): f.write('%d %s\n' % (k, n))
print('%d names, %d lookups' % (len(c), sum(c.values())))
