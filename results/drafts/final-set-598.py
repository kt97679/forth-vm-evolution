"""results/drafts/final-set-598.py [OUT] - the final set from chains B, C and D (Iteration 598; the owner's terms at 576 -
lose no good design; HANDOFF's processing of chains C and D: a design in any session's set kept). final-pick.py on chain
C's readings alone (its own set, as process-seed.sh ran it) and on every session pooled (chain D's 40 laid out by
chain-sessions.py, beside chains B and C - its printed line), unioned with chain B's 14 (results/final-set-seed86.md).
Writes OUT (default results/final-set-chainsBCD-seed86.md): one record a line, each with the pooled re-measures (speed,
speed32 the laptop alone, every session's geometric mean; inrun, inrun32 kept), "why" from the pooled pick or
"kept - chain B's set" / "kept - chain C's set", and "sets": which of B, C, pooled hold it. The pooled pick's markdown
goes to /tmp/final-pick-pooled.md. Prints the membership table. As the build user (final-pick imports the evolver)."""
import glob, importlib.util, json, os, re, subprocess, sys, tempfile
OUT = sys.argv[1] if len(sys.argv) > 1 else 'results/final-set-chainsBCD-seed86.md'
SL, FPK = 'results/shortlist-seed86.md', 'lab/evolve/final-pick.py'
_s = importlib.util.spec_from_file_location('fp', FPK); FP = importlib.util.module_from_spec(_s); _s.loader.exec_module(FP)
key = lambda p: int(re.search(r's(\d+)$', p).group(1))
sD = sorted(glob.glob('results/chainD-seed86/s[0-9]*'), key=key)
outs = lambda d: sorted(glob.glob(os.path.join(d, '*.out.json')))


def pick(args, md=None):
    j = tempfile.mktemp(suffix='.json')
    r = subprocess.run(['python3', FPK, SL] + args + ['--json', j], capture_output=True, text=True)
    if r.returncode: sys.exit('final-pick failed: %s' % r.stderr[-400:])
    if md: open(md, 'w').write(r.stdout)
    s = [json.loads(l) for l in open(j)]; os.unlink(j)
    return s


C = pick(['results/chainC-seed86/loadtest.md'] + outs('results/chainC-seed86'))
also = sD[1:] + ['results/chainB-seed86', 'results/chainC-seed86']
A = pick([os.path.join(sD[0], 'loadtest.md')] + outs(sD[0]) + sum((['--also-session', d] for d in also), []), '/tmp/final-pick-pooled.md')
B = [json.loads(l)['id'] for l in open('results/final-set-seed86.md') if l.startswith('{')]
L = FP.merge_sessions([FP.records(os.path.join(d, 'loadtest.md')) for d in [sD[0]] + also if os.path.exists(os.path.join(d, 'loadtest.md'))])
R, left = FP.remeasured(FP.records(SL), L, 'idle', 'idle32')
sets = {}
for n, s in (('B', B), ('C', [r['id'] for r in C]), ('pooled', [r['id'] for r in A])):
    for i in s: sets.setdefault(i, []).append(n)
out = [dict(r, sets=sets[r['id']]) for r in A]
for i in sorted(sets):
    if 'pooled' not in sets[i]:
        out.append(dict(R[i], why='kept - chain %s\'s set' % sets[i][0] if len(sets[i]) == 1 else 'kept - chains B and C\'s sets', adds=0.0, sets=sets[i]))
with open(OUT, 'w') as o:
    o.write('# The final set from chains B, C and D (Iteration 598) - results/drafts/final-set-598.py: the pooled pick over every\n'
            '# session (chain D\'s 40, chains B and C) and the designs only chain B\'s or chain C\'s own set holds (lose no good design),\n'
            '# one record a line, the pooled re-measures in each. Consolidation\'s input (results/final-pick-chainCD-seed86.md).\n\n')
    for r in out: o.write(json.dumps(r, sort_keys=True) + '\n')
print('%d designs -> %s: the pooled %d, chain B %d, chain C %d; chain B\'s kept by the pooled pick %d, by chain C\'s %d' % (
      len(out), OUT, len(A), len(B), len(C), len(set(B) & set(sets) - {i for i in sets if 'pooled' not in sets[i]}),
      sum('C' in sets[i] for i in B)))
print('| design | B | C | pooled | why | speed alone | 32-bit alone | bytes | memory KB |')
print('|---|---|---|---|---|---|---|---|---|')
for r in sorted(out, key=lambda r: r['speed']):
    s = r['sets']
    print('| %s | %s | %s | %s | %s | %.4f | %.4f | %s | %d |' % (r['id'], 'x' if 'B' in s else '', 'x' if 'C' in s else '',
          'x' if 'pooled' in s else '', r['why'], r['speed'], r['speed32'], format(r['total'], ','), r['rss']))
