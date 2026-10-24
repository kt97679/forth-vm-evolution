#!/usr/bin/env python3
"""jitapps.py ID [--zip PATH] [--apps a,b,...] [--db FILE ...] - what the JIT leaves on the applications (Iteration 471)

The applications held out (appbench.py) keep a quarter of the fast designs' lead or less (results/drafts/appbench-468.md).
Why: the JIT translates a word only whole, and a word it refuses runs interpreted. As jitleft.py does for the selection's
workloads, the design is built twice for the profiler - the JIT off (every dispatch the application makes) and the JIT on
with -DJITLOG=1 (each refusal logged with its reason and the operation that stopped it) - and each application run in
both. Per application: the dispatches the JIT left, as a share of all; then where they sit - each left dispatch given to
the word it falls in (the image's words by the call map, the application's own by the JIT's log of every word it
decided on), and each refused word to the root of its refusal, a callee's refusal followed down: an operation without a
mapping (named), too long (JIT_MAXOPS), the return stack's order, a stencil not usable, the JIT's memory full.
"""
import bisect, collections, glob, json, os, re, shutil, sys, tempfile, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
A = sys.argv[1:]
def opt(name, default=None):
    return A[A.index(name) + 1] if name in A else default
zp = opt('--zip', ''); apps = opt('--apps', 'sim16,gc16,scan,evo,fcp,brainless,cd16sim').split(',')
SET = dict(a[6:].split('=', 1) for a in A if a.startswith('--set='))
dbs = [A[i + 1] for i, a in enumerate(A) if a == '--db']
ids = [a for i, a in enumerate(A) if not a.startswith('--') and (i == 0 or A[i - 1] not in ('--zip', '--apps', '--db'))]
if not ids: sys.exit(__doc__)
recs = {}
for db in dbs or sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*.md'))):
    for l in open(db, errors='replace'):
        try: r = json.loads(l)
        except ValueError: continue
        if isinstance(r, dict) and 'genome' in r and 'id' in r: recs[r['id']] = r
sys.path.insert(0, os.path.join(HERE, 'appbench')); from fold import fold
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
OWN = {'sim16': ('sim16.fth', '60 BENCH BYE'), 'gc16': ('gc16.fth', '50000 BENCH BYE'), 'scan': ('scan.fth', '600 BENCH BYE'),
       'evo': ('evo.fth', '3000 BENCH BYE')}
CALLS = {'fcp': 'include fcp-1.31-64.f||!: setup SETUP ;||bench bye', 'brainless': 'include benchmark.fs benchmark bye',
         'cd16sim': ': 3drop 2drop drop ; include bench.f 1000000 benchmark bye'}
WHY = {1: 'an operation without a mapping', 2: "the return stack's order", 3: 'a stencil not usable', 5: "the JIT's memory full",
       6: 'too long (JIT_MAXOPS)'}
def hexfix(t): return re.sub(r'(?<![\w$])\$([0-9A-F]+)\b', lambda m: str(int(m.group(1), 16)), t)
work = tempfile.mkdtemp(prefix='jitapps-'); text = {}
for p in apps:
    d = os.path.join(work, p); os.makedirs(d)
    if p in OWN: f, call = OWN[p]; text[p] = open(os.path.join(HERE, 'apps', f), 'rb').read() + b'\n' + call.encode() + b'\n'; continue
    if not zp: sys.exit('jitapps.py: --zip PATH for ' + p)
    with zipfile.ZipFile(os.path.expanduser(zp)) as z:
        for n in z.namelist():
            m = re.match(r'[^/]+/%s/(.+)' % re.escape(p), n)
            if not m or '/CVS/' in '/' + m.group(1) or n.endswith('/'): continue
            out = os.path.join(d, m.group(1)); os.makedirs(os.path.dirname(out), exist_ok=True); data = z.read(n)
            if re.search(r'\.(fs|f|fth|fb|4th|vhd)$', n, re.I): data = hexfix(fold(data.decode('latin-1'))).encode('latin-1')
            open(out, 'wb').write(data)
    for f in ('extend.4', 'coreext.4'): shutil.copy(os.path.join(ROOT, 'forth', f), d)
    text[p] = (open(os.path.join(HERE, 'appbench', 'prelude.fth')).read() + '\n' + ' '.join(
        s[1:] if s.startswith('!') else hexfix(fold(s)) for s in CALLS[p].split('||')) + '\n').encode('latin-1')

def profile(g, d, why):
    shutil.rmtree(d, ignore_errors=True); cm = d + '.map'; os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
    if why: os.environ['EVOLVE_JITLOG'] = '1'
    try: eng, img = E.build(g, d)
    finally: E.PROFILING[0] = False; del os.environ['CALLMAP']; os.environ.pop('EVOLVE_JITLOG', None)
    lines = [l.rstrip('\n').split(' ') for l in open(cm)]
    W = sorted((int(f[1]), int(f[2]), ' '.join(f[4:])) for f in lines if f[0] == 'W' and f[3] == 'code')
    OPS = {}                                   # jit_ops[]'s index -> its name, from this design's vm-jit-ops.h
    if os.path.exists(os.path.join(d, 'vm-jit-ops.h')):
        for l in open(os.path.join(d, 'vm-jit-ops.h')):
            m = re.match(r'\[(\d+)\] = \{.*/\* *(.+?) *\*/', l)
            if m: OPS[int(m.group(1))] = m.group(2)
            m = re.match(r'/\* \[(\d+)\] (.+?) - no stencils \*/', l)      # 484: the operations without stencils, named (layout.py 472)
            if m: OPS[int(m.group(1))] = m.group(2)
    runs, logs = {}, {}
    for p in apps:
        pf, jl = os.path.join(d, 'p-' + p), os.path.join(d, 'jl-' + p)
        E.sh([eng, img], cwd=os.path.join(work, p), inp=text[p], timeout=1800, cpu=1200,
             env=dict(os.environ, VMPROF=pf, **({'JITLOG': jl} if why else {})))
        c = collections.Counter()
        for f in (l.split() for l in open(pf)):
            if f and f[0] == 'I': c[int(f[1])] += int(f[2])
        runs[p] = c; R, T = {}, {}
        if why and os.path.exists(jl):
            for l in open(jl, errors='replace'):
                f = l.rstrip('\n').split(' ')
                if f[0] == 'R' and len(f) >= 4: R.setdefault(int(f[1]), (int(f[2]), int(f[3]), int(f[4]) if len(f) > 4 else -1))
                elif f[0] == 'T' and len(f) >= 5: T[int(f[1], 16)] = (int(f[3], 16), ' '.join(f[4:])[-16:])
        logs[p] = (R, T)
    shutil.rmtree(d, ignore_errors=True); os.path.exists(cm) and os.remove(cm)
    return W, OPS, runs, logs

def root(R, w, seen=()):
    at, why, op = R[w]
    if why == 4 and at in R and at not in seen: return root(R, at, seen + (w,))
    return why, op, at

for ident in ids:
    g = E.canon(dict(E.canon(recs[ident]['genome']), **{k: int(v) for k, v in SET.items()}))   # 472: --set=gene=value, as jitleft.py
    if not E.express(g).get('jit'): print('%s: no JIT' % ident); continue
    _, _, off, _ = profile(dict(g, jit=0), os.path.join(E.EV, 'jitapps-off'), False)
    W, OPS, on, logs = profile(g, os.path.join(E.EV, 'jitapps-on'), True)
    print('\n## %s\n\n| application | dispatches, JIT off | left by the JIT | left |\n|---|---|---|---|' % ident)
    for p in apps:
        t0, t1 = sum(off[p].values()), sum(on[p].values())
        print('| %s | %s | %s | %.1f%% |' % (p, format(t0, ','), format(t1, ','), 100.0 * t1 / max(1, t0)))
    for p in apps:
        R, T = logs[p]; t1 = sum(on[p].values())
        starts = sorted(set([w[0] for w in W] + list(T)))
        name = {w[0]: w[2] for w in W}; name.update({a: ''.join(ch for ch in T[a][1] if ch not in '.')[-12:] or '?' for a in T if a not in name})
        per = collections.Counter()
        for a, n in on[p].items():
            i = bisect.bisect_right(starts, a) - 1
            per[starts[i] if i >= 0 else -1] += n
        cause = collections.Counter(); top = []
        for w, n in per.most_common():
            if w in R:
                why, op, at = root(R, w)
                k = 'an operation without stencils: %s' % OPS.get(op, 'op %d' % op) if why == 1 else WHY.get(why, 'why %d' % why)
                cause[k] += n
                if len(top) < 6: top.append('%s (%.1f%%: %s)' % (name.get(w, hex(w)), 100.0 * n / max(1, t1), k))
            else: cause['in words the JIT translated or never reached'] += n
        print('\n**%s** - where the %s dispatches left sit:\n' % (p, format(t1, ',')))
        for k, n in cause.most_common(6): print('- %s: %.1f%%' % (k, 100.0 * n / max(1, t1)))
        if top: print('- the refused words carrying most: ' + '; '.join(top))
shutil.rmtree(work, ignore_errors=True)
