#!/usr/bin/env python3
"""results/drafts/article-figures-658.py - the figures the article's section 17 quotes after seed 87, recomputed from the
runs' records (Iteration 658; the freeze's last item - results/drafts/portable-plan-602.md, "Then the freeze": the
article's portable figures recomputed from the runs' records). From the repository only, as the build user: each
follow-up chain's readings (results/chain-followupN/) through lab/evolve/followup-roles.py with the roles that chain ran
with (its document's command); small and fast on ARMv7's six Tegra sessions through results/drafts/smallarm-pool-629.py;
seed 91's whole-pool bridges through results/drafts/gain-bridge-640.py. A chain's size and hours and a run's in-run
figure, which no tool here recomputes, are read from the chain's document and marked (record). The ten roles as relf takes
them: results/handoff-relf-657.md (checked against the records at 657). Each recomputed figure the article quotes is
looked up as written in its chain's document (results/followup-roles-seedN.md); those not found are listed at the end.
Markdown on stdout: results/article-figures-658.md."""
import re, subprocess, sys

R6 = 'fastest=782f3ad7ff,arm=%s,knee=%s,smallarm=%s,memory=fb0d57c8a2,smallest=64a7345393'
X4 = ',fast64=c7c35f9c97,fast32=4ef851fd8e,allround=06b188f45b,smalljit=bac37f35a2'
CHAINS = {   # the chain: the handoff its roles' heading names, the roles it ran with (its document's command)
    '88': ('611', R6 % ('690981ca5b', 'c2ef9488ff', 'a627b954c6')),
    '89': ('611', R6 % ('690981ca5b', 'c2ef9488ff', 'a627b954c6') + X4),
    '90': ('631', R6 % ('3eb59b271d', 'c2ef9488ff', 'ae99617f06')),
    '91': ('636', R6 % ('3eb59b271d', '11a56ff9e4', 'ae99617f06')),
    '91-final': ('636', R6 % ('3eb59b271d', '11a56ff9e4', 'ae99617f06'))}
out, missing, checked = [], [], [0]
p = out.append

def run(*a):
    r = subprocess.run(['python3'] + list(a), capture_output=True, text=True)
    if r.returncode:
        sys.exit('article-figures: %s - exit %d\n%s' % (' '.join(a), r.returncode, (r.stdout + r.stderr)[-1500:]))
    return r.stdout

def roles(n, gain=False):
    h, r = CHAINS[n]
    return run('lab/evolve/followup-roles.py', 'results/followup-seed%s.md' % n, 'results/chain-followup%s' % n,
               '--handoff', 'results/handoff-relf-%s.md' % h, '--roles', r, *(['--gain'] if gain else []))

def doc(n):
    return open('results/followup-roles-seed%s.md' % n).read()

def quote(n, text, pat, *figs):
    """the one line of a tool's output matching pat, printed; figs - the figures in it the article quotes - looked up
    as written in chain n's document"""
    m = [l.strip() for l in text.splitlines() if re.search(pat, l)]
    if len(m) != 1:
        sys.exit('article-figures: %d lines for %r' % (len(m), pat))
    d = doc(n)
    for f in figs:
        if f not in m[0]:
            sys.exit('article-figures: %r is not in its line: %s' % (f, m[0]))
        checked[0] += 1
        if f not in d:
            missing.append('%s - %s (results/followup-roles-seed%s.md)' % (f, m[0][:70], n))
    p('- ' + m[0])
    return m[0]

def record(n, pat):
    m = re.search(pat, doc(n), re.S)
    if not m:
        sys.exit('article-figures: no %r in the seed %s document' % (pat, n))
    return m

def chain(n):
    m = record(n, r'\(fury, [^)]*?([\d.]+) hours[^)]*\):\s+the\s+(\d+)\s+of\s+results/followup-seed')
    return 'the chain: %s designs side by side, %s hours (record)' % (m.group(2), m.group(1))

pct = lambda l: float(re.search(r': ([-+]\d+\.\d+)%', l).group(1))

p("# The article's figures after seed 87, recomputed (Iteration 658; results/drafts/article-figures-658.py)\n")
p("Section 17 of article/article-en-draft.md and article/article-ru-draft.md quotes these. Each line is a tool's output")
p("on a chain's readings in results/, unless marked (record): read from the chain's document.\n")

p('## Seed 88 - the second portable run\n')
m = record('88', r'the fastest at 32 bits \((\w{10})\s+([\d.]+)\s+against\s+([\d.]+),\s+(-[\d.]+%)')
p('- in the run, the fastest at 32 bits: %s %s against %s, %s (record)' % m.groups())
p('- ' + chain('88'))
g = roles('88', True)
quote('88', g, r'^  the laptop alone, 4-byte cells', '+2.06% +/- 0.76%')
quote('88', g, r'^verdict')

p("\n## Seed 89 - a JIT run: its follow-up, and the quick pass over seed 88's rest\n")
p('- ' + chain('89'))
r = roles('89')
quote('89', r, r'3eb59b271d against 690981ca5b', '-2.84% +/- 0.62%')
quote('89', r, r'ee34931cd7 against 4ef851fd8e', '-3.15% +/- 0.42%')
quote('89', r, r'c6f1c1331b 29,306 B')
s = run('results/drafts/smallarm-pool-629.py')
quote('89', s, r'ae99617f06 against a627b954c6', '-2.30% +/- 0.42%')
quote('89', s, r'8164d3858f against a627b954c6', '-1.91% +/- 0.46%')

p("\n## Seed 90 - the other JIT run: the quick pass over seed 89's rest\n")
p('- ' + chain('90'))
r = roles('90')
quote('90', r, r'11a56ff9e4: x86-64', '+1.54%', '-3.59%', '5.45%')

p('\n## Seed 91 - the third portable run\n')
p('- ' + chain('91'))
g = roles('91', True)
quote('91', g, r'^  the laptop alone, 4-byte cells', '-5.38% +/- 0.31%')
quote('91', g, r'^  binary \+ image', '-1.44%')
b = run('results/drafts/gain-bridge-640.py')
quote('91', b, r'chain-followup89: e523a45566 0\.3107', '-0.68%')
quote('91', b, r'binary \+ image \(exact\)', '-0.13%')

p('\n## The final check\n')
p('- ' + chain('91-final'))
g = roles('91-final', True)
L = [quote('91-final', g, pat, f) for pat, f in (
    (r'^  the laptop alone, 8-byte cells', '+2.69% +/- 0.56%'), (r'^  the laptop alone, 4-byte cells', '+1.84% +/- 0.93%'),
    (r'^  x86-64:', '+1.26%'), (r'^  x86-32:', '+0.66%'), (r'^  ARMv7:', '+2.52%'), (r'^  the mean of the three', '+2.83%'))]
p("- so the run's fastest behind the best found before by %.2f%% to %.2f%%" % (min(map(pct, L)), max(map(pct, L))))
quote('91-final', g, r'^  binary \+ image', '13,691 B')
quote('91-final', g, r'^  memory', '+8 KB')
r = roles('91-final')
lines = r.splitlines()
i = [k for k, l in enumerate(lines) if 'smallest - 64a7345393 13,891 B; smaller:' in l]
if len(i) != 1:
    sys.exit("article-figures: the smallest's block")
sm = []
for l in lines[i[0] + 1:]:
    if not re.match(r'\s+[0-9a-f]{10} [\d,]+ B', l):
        break
    sm.append(l.strip())

def trade(l):
    sp = [(float(d), float(e)) for _, d, e in re.findall(r'(x86-64|x86-32|ARMv7) ([-+][\d.]+)% \+/- ([\d.]+)%', l)]
    return len(sp) != 3 or any(d > 2 * e for d, e in sp) or int(re.search(r'memory ([-+]\d+) KB', l).group(1)) > 0

free = [l.split()[0] for l in sm if not trade(l)]
rec = record('91-final', r'(\d+) smaller designs, (\d+) with a trade')
p('- smaller than the smallest holder (64a7345393, 13,891 B): %d designs, %d with a trade (slower on a class by 2 SE, or '
  'more memory); without one: %s' % (len(sm), len(sm) - len(free), ', '.join(free)))
p('- the document: %s smaller, %s with a trade (record)' % rec.groups())
checked[0] += 1
if (len(sm), len(sm) - len(free)) != tuple(map(int, rec.groups())):
    missing.append('the smaller designs: %d, %d with a trade - the document %s, %s' % ((len(sm), len(sm) - len(free)) + rec.groups()))
x32 = [float(re.search(r'x86-32 \+([\d.]+)%', l).group(1)) for l in sm if ' 13,691 B ' in l]
p('- the 13,691 B designs (%d): x86-32 +%.2f%% to +%.2f%%' % (len(x32), min(x32), max(x32)))
quote('91-final', r, r'd180351903 13,883 B', '13,883')

p('\n## The ten roles (results/handoff-relf-657.md, as relf takes them)\n')
rows = [l for l in open('results/handoff-relf-657.md') if re.match(r'\| [^|]+ \| [0-9a-f]{10} \|', l)]
if len(rows) != 10:
    sys.exit('article-figures: %d role rows in the handoff' % len(rows))
p('| role | design | x86-64 | x86-32 | ARMv7 | bytes, 8-byte cells | memory KB | JIT | measured |')
p('|---|---|---|---|---|---|---|---|---|')
for l in rows:
    c = [x.strip() for x in l.strip().strip('|').split('|')]
    p('| %s |' % ' | '.join(c[k] for k in (0, 1, 2, 3, 4, 5, 7, 8, 10)))
p("\n(*) on ARMv7 a JIT design runs without its JIT (the handoff's note).")

p('\n## The check\n')
p("%d figures the article quotes, recomputed; %d of them as written in their chain's document." % (checked[0], checked[0] - len(missing)))
for x in missing:
    p('- not as written: ' + x)
print('\n'.join(out))
