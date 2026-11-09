#!/usr/bin/env python3
"""results/drafts/jit-rehearsal-622.py - the JIT follow-up's tools rehearsed (Iteration 622; results/drafts/jit-run-plan-620.md,
"To prepare while the run goes"), as results/drafts/followup-rehearsal-615.sh rehearsed the portable one. On seed 86's chains
B-D - the readings the relf handoff's x86 roles were picked from (601) - laid out as sessions (chain B s1, chain C s2, chain
D's sK after), the shortlist's 40 the list (each its jit from its genome; the ten 601 holders found before, the rest
stand-ins for a run's): (1) each x86 role's best 601's holder (c7c35f9c97, 4ef851fd8e, 06b188f45b) and the fastest portable
690981ca5b - the portable roles skipping the JIT designs; (2) those figures final-pick.py's
(on the same sessions; 619's audit: 0.1848 and 0.1989) to the 4 digits printed; (3) the control - fast64 held by fb0d57c8a2, c7c35f9c97 a
stand-in: flagged; (4) the JIT verdict; (5) portable-followup.py --jit on seed 86's results file: JIT designs kept, every
record its jit, the ten holders listed; (6) its portable path the pre-622 script's output byte for byte. As the build user."""
import glob, json, os, re, shutil, subprocess, sys, tempfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); os.chdir(ROOT)
sys.path.insert(0, 'lab/evolve'); sys.argv = ['x']; import evolve as E
W = tempfile.mkdtemp(prefix='jitreh-'); S = os.path.join(W, 'sess'); ok = True
def check(c, what):
    global ok; ok &= bool(c); print('  %s  %s' % ('PASS' if c else 'FAIL', what))
F = ('loadtest.md', 'dream.lan-prebuilt64.out.json', 'dream.lan-prebuilt32.out.json', 'rage.lan-prebuiltarm.out.json')
srcs = ['results/chainB-seed86', 'results/chainC-seed86'] + sorted(glob.glob('results/chainD-seed86/s[0-9]*'), key=lambda d: int(d.rsplit('s', 1)[1]))
for k, d in enumerate(srcs, 1):
    os.makedirs(os.path.join(S, 's%d' % k))
    for f in F:
        if os.path.exists(os.path.join(d, f)): os.symlink(os.path.abspath(os.path.join(d, f)), os.path.join(S, 's%d' % k, f))
H = dict(fastest='690981ca5b', arm='690981ca5b', knee='c2ef9488ff', smallarm='22420b3b61', memory='fb0d57c8a2', smallest='cea114f47e',
         fast64='c7c35f9c97', fast32='4ef851fd8e', allround='06b188f45b', smalljit='bac37f35a2')
recs = [json.loads(l) for l in open('results/shortlist-seed86.md') if l.startswith('{')]
J = {r['id']: bool(E.express(E.canon(r['genome'])).get('jit')) for r in recs}
def roles(h, gain=False):
    c = os.path.join(W, 'cand.md')
    with open(c, 'w') as o:
        for r in recs: o.write(json.dumps(dict(r, jit=J[r['id']], why='found before - holder' if r['id'] in h.values() else 'the run - a stand-in'), sort_keys=True) + '\n')
    p = subprocess.run([sys.executable, 'lab/evolve/followup-roles.py', c, S, '--roles', ','.join('%s=%s' % kv for kv in h.items())]
                       + (['--gain'] if gain else []), capture_output=True, text=True)
    return p.stdout + p.stderr
print('jit-rehearsal: %d sessions (chain B, chain C, chain D %d), %d designs, %d with the JIT' % (len(srcs), len(srcs) - 2, len(recs), sum(J.values())))
out = roles(H)
first = lambda name: (re.search(r'^  %s: ([0-9a-f]{10}) ([0-9.]+)' % re.escape(name), out, re.M) or [None, None, None])
fp = re.search(r'fastest portable \(the best mean\): ([0-9a-f]{10}) ([0-9.]+) against', out)
best = {k: first(n) for k, n in (('fast64', 'fastest on x86-64'), ('fast32', 'fastest on x86-32'), ('allround', 'best all-round (the best mean)'))}
check(all(best[k][1] == H[k] for k in best) and fp and fp.group(1) == H['fastest'] and not J[H['fastest']],
      '(1) the x86 roles\' best %s, the fastest portable %s' % (' '.join(str(best[k][1]) for k in best), fp.group(1) if fp else None))
FP = {}                                        # final-pick.py on the same sessions, as process-followup.sh runs it
fpo = subprocess.run([sys.executable, 'lab/evolve/final-pick.py', 'results/shortlist-seed86.md', os.path.join(S, 's1', 'loadtest.md')]
                     + sorted(glob.glob(os.path.join(S, 's1', '*.out.json'))) + sum((['--also-session', d] for d in
                     sorted(glob.glob(os.path.join(S, 's[0-9]*')), key=lambda d: int(d.rsplit('s', 1)[1]))[1:]), []), capture_output=True, text=True).stdout
for l in fpo.split('\n'):
    m = re.match(r'^\| *\d+ \| ([0-9a-f]{10}) \| ([0-9.]+\*?|-) \| ([0-9.]+\*?|-) \| ([0-9.]+\*?|-) \| ([0-9.]+\*?|-) \|', l)
    if m: FP.setdefault(m.group(1), m.groups()[1:])
col = {'fast64': 0, 'fast32': 1, 'allround': 3}
pairs = [(k, best[k][2], FP.get(H[k], ('?',) * 4)[col[k]]) for k in best]
check(all(a == b for k, a, b in pairs), '(2) the figures final-pick.py\'s: %s' % ', '.join('%s %s/%s' % p for p in pairs))
g = roles(dict(H, fast64='fb0d57c8a2'), gain=True)
rl = next((l for l in g.split('\n') if 'beating a holder' in l), '')
check('fastest on x86-64' in rl and 'c7c35f9c97' in rl.split('fastest on x86-64')[1], '(3) the control flags c7c35f9c97 against fb0d57c8a2 on x86-64')
vl = next((l for l in g.split('\n') if l.startswith('verdict:')), '')
check('JIT' in vl, '(4) the JIT verdict: %s' % vl[:110])
fu = os.path.join(W, 'fu86.md')
p = subprocess.run([sys.executable, 'lab/evolve/portable-followup.py', 'results/evolve-amd-ryzen-7-pro-8840hs-seed86.md', '-', fu, '--jit', '--seed', '86',
                    '--holders', 'results/relf-designs-611.md'], capture_output=True, text=True)
rows = [json.loads(l) for l in open(fu) if l.startswith('{')] if p.returncode == 0 else []
hold = [json.loads(l)['id'] for l in open('results/relf-designs-611.md') if l.startswith('{')]
check(rows and all('jit' in r for r in rows) and any(r['jit'] for r in rows) and all(h in {r['id'] for r in rows} for h in hold),
      '(5) portable-followup.py --jit: %d records, %d JIT, the %d holders listed - %s' % (len(rows), sum(r.get('jit', 0) for r in rows), len(hold), (p.stdout.split('\n') or [''])[0][:70]))
old = os.path.join('lab/evolve', '.portable-followup-pre622.py')
try:
    with open(old, 'w') as o: o.write(subprocess.run(['git', 'show', '997d945:lab/evolve/portable-followup.py'], capture_output=True, text=True).stdout)
    a = ['results/evolve-amd-ryzen-7-pro-8840hs-seed88.md', 'results/followup-pick-seed87.json', None, '--before', 'results/portable-front-seed87.md',
         '--holders', 'results/relf-designs-611.md', '--hours', '9', '--rest', None]
    outs = []
    for t, s in (('old', old), ('new', 'lab/evolve/portable-followup.py')):
        x = list(a); x[2] = os.path.join(W, t + '.md'); x[-1] = os.path.join(W, t + '-rest.md')
        q = subprocess.run([sys.executable, s] + x, capture_output=True, text=True)
        outs.append((q.stdout.replace(x[2], 'OUT').replace(x[-1], 'REST'), open(x[2]).read(), open(x[-1]).read()))
    cut = lambda t: t.split('\nthe screen:')[0]      # 631: the screen's sizing lines - seed 90's chain's rates, by design
    check(outs[0][1:] == outs[1][1:] and cut(outs[0][0]) == cut(outs[1][0]) and len(outs[0][1]) > 1000,
          '(6) the portable path the pre-622 script\'s byte for byte (list, screen, printed lines but the screen\'s sizing - 631; %d bytes)' % len(outs[0][1]))
finally:
    os.unlink(old)
shutil.rmtree(W)
print('jit-rehearsal: %s' % ('PASS' if ok else 'FAIL')); sys.exit(0 if ok else 1)
