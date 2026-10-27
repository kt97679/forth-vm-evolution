#!/usr/bin/env python3
"""lab/evolve/draft-results.py [PROCESS] --iteration N - a returned seed's results file drafted from process-seed.sh's
output (Iteration 551; HANDOFF.md, "Processing a returned seed"): the facts a processing chat gathered by hand - the
run's line and records, the true front against the reported one, the fixed-box hypervolume, the extremes, one round
first, the operators, the JIT designs, the fast end re-measured, the experiments' headlines, the remote checks. Writes
results/evolve-MACHINE-seedN.md (the draft header, ---, report.md), results/xcheck-seedN.md (the chain's remote
checks), and the spread's session appended to results/compare-fronts-MACHINE.md. The verdict, the predictions' scores,
the votes and the rules stay the chat's: TODO lines mark them (summary.md has their facts) - none may be left in what
is committed. PROCESS: /tmp/process."""
import collections, glob, json, os, re, statistics as st, subprocess, sys
a = sys.argv[1:]
it = a[a.index('--iteration') + 1] if '--iteration' in a else 'N'
P = next((x for x in a if not x.startswith('--') and x != it), '/tmp/process')
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
pack = glob.glob(os.path.join(P, 'forth-vm-evolution-seed*-*', 'pack'))[0]
m = re.search(r'seed(\d+)-([0-9a-f]+)-', pack); N, commit = int(m.group(1)), m.group(2)
chain = (glob.glob(os.path.join(P, 'chain-*')) or [''])[0]
rd = lambda f, d='?': open(f).read().strip() if f and os.path.exists(f) else d
line, status = rd(os.path.join(chain, 'line')), rd(os.path.join(chain, 'status')).split('\n')[0]
mach = re.search(r'evolve-(.+)-seed\d+\w*\.md$', sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*-seed*.md')))[-1]).group(1)
db = os.path.join(pack, 'db.jsonl'); R = {}
for l in open(db, errors='replace'):
    if l.startswith('{'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id'): R[r['id']] = r
cnt = collections.Counter(r.get('status') for r in R.values()); gens = max((r.get('gen') or 0) for r in R.values())
hm = re.search(r'\b(\d+)h\b', line); hours = int(hm.group(1)) if hm else None
ok = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and E.ov(r, 'total') and r.get('rss')]
E.TWO_WIDTHS[0] = sum(1 for i in ok if R[i].get('speed32')) * 2 > len(ok)
if E.TWO_WIDTHS[0]: ok = [i for i in ok if R[i].get('speed32')]
T = E.first_front(ok, R); rep = open(os.path.join(pack, 'report.md')).read()
Rf = set(re.findall(r'^\| ([0-9a-f]{10}) \|', rep.split('## How the front came about')[0], re.M))
hv = next((l.strip() for l in subprocess.run([sys.executable, os.path.join(HERE, 'hv.py'), db], capture_output=True, text=True).stdout.split('\n') if 'hypervolume' in l), '?')
so = subprocess.run([sys.executable, os.path.join(HERE, 'stopping.py'), db, '--seed', str(N)], capture_output=True, text=True).stdout   # 554
stop_ = ' '.join(l for l in so.split('\n') if l.startswith(('verdict:', 'the count:', 'the next run gains if:'))) or "TODO: against the method's earlier runs (GOALS.md)."
f = min(T, key=lambda i: R[i]['speed']); s = min(T, key=lambda i: E.ov(R[i], 'total')); mm = min(T, key=lambda i: R[i]['rss'])
w = min((i for i in T if R[i].get('speed32')), key=lambda i: R[i]['speed32'], default=None)
kids = [r for r in R.values() if (r.get('gen') or 0) > 0]; meas = [r for r in kids if r.get('status') != 'screened']
stop = cnt.get('stopped after one round', 0); aud = [i for i, r in R.items() if r.get('stopaudit')]
cls = lambda h: 'crossover' if h.startswith('crossover') else 'borrowed' if ' from ' in h else 'mutation'
def shares(g):
    c = collections.Counter(cls(r.get('how', '')) for r in g); return {k: 100.0 * v / max(1, len(g)) for k, v in c.items()}
top = max((r['gen'] for r in kids), default=0); o_all, o_5 = shares(kids), shares([r for r in kids if r['gen'] > 0.8 * top])
fk = sum(1 for i in T if (R[i].get('gen') or 0) > 0)
ex = {i: E.express(E.canon(R[i]['genome'])) for i in T}; J = [i for i in T if E.jit_on(E.canon(R[i]['genome']))]
k = max(1, len(T) // 10); fj = [i for i in sorted(T, key=lambda i: R[i]['speed'])[:k] if i in J]
genes = ', '.join('%s %d' % (g, sum(1 for i in J if ex[i].get(g))) for g in ('jitmul', 'jitfuse', 'jitexec', 'jitos', 'jitrp'))
rm = json.load(open(os.path.join(pack, 'remeasure.json'))) if os.path.exists(os.path.join(pack, 'remeasure.json')) else {}
ri = sorted((i for i in rm if i in R and R[i].get('speed')), key=lambda i: R[i]['speed']); rr = {i: rm[i]['speed'] / R[i]['speed'] for i in ri}
jr = lambda i: E.jit_on(E.canon(R[i]['genome']))
md = lambda xs: '%.3f' % st.median(xs) if xs else '-'
def exp(tool, pat):
    fs = glob.glob(os.path.join(P, 'forth-vm-evolution-%s-*' % tool, 'pack', tool + '.md')) + glob.glob(os.path.join(chain, 'packs', 'failed-%s-*' % tool, tool + '.md'))
    if not fs: return None
    t = open(fs[0]).read(); return t if pat is None else next((l.strip() for l in t.split('\n') if re.match(pat, l)), '?')
sp = exp('review-checks', None); spread_row = next((l for l in (sp or '').split('\n') if l.startswith('| build/evolve/db.jsonl')), None)
ab, ck = exp('appbench', r'\*\*Spearman'), exp('clockcheck', r'\*\*Medians'); tf = exp('truefronts', None)
remote = sorted(glob.glob(os.path.join(chain, 'remote', '*.md')))
rsp = '; '.join('%s %s' % (os.path.basename(x)[:-3], next((re.sub(r'\s+', ' ', l.replace('*', '').strip()).split(' between')[0][:70] for l in open(x) if 'Spearman' in l), '?')) for x in remote)
P_ = lambda d: ', '.join('%s %.1f%%' % (k, v) for k, v in sorted(d.items()))
head = '\n'.join(x for x in [
 '# Seed %d on the %s - TODO: the run in a phrase (Iteration %s)' % (N, mach.replace('-', ' ').upper().replace('AMD RYZEN', 'AMD Ryzen').replace(' PRO ', ' PRO '), it), '',
 '`%s` at %s. The chain: %s%s. %s designs, generations 0-%d: %s%s.' % (line, commit, status, '' if status == 'done' else ' - TODO: what failed', '{:,}'.format(len(R)), gens,
    ', '.join('%s %s' % ('{:,}'.format(v), k) for k, v in cnt.most_common()), '; %s designs an hour' % '{:,}'.format(len(R) // hours) if hours else ''), '',
 '**The front**: the true one %d designs - the report\'s %d%s.' % (len(T), len(Rf), ', the same' if Rf == set(T) else ' - TODO: why they differ'), '',
 '**The fixed-box hypervolume**: %s. **The stopping rule** (stopping.py, results/stopping-series.md): %s' % (hv.split(': ', 1)[-1], stop_), '',
 '**The extremes**: fastest %s %.4f, smallest %s %s bytes, least memory %s KB%s.' % (f, R[f]['speed'], s, '{:,}'.format(E.ov(R[s], 'total')), R[mm]['rss'],
    ', fastest at 32 bits %s %.4f' % (w, R[w]['speed32']) if w else ''), '',
 '**One round first**: %s children stopped after one round, %.1f%% of those measured; %d audited in full, %d of them on the front.' % (
    '{:,}'.format(stop), 100.0 * stop / max(1, len(meas)), len(aud), len(set(aud) & set(T))), '',
 '**The operators**: %s of the children; the last fifth %s; the front\'s entries per child %.3f%% (%d of %s).' % (P_(o_all), P_(o_5), 100.0 * fk / max(1, len(kids)), fk, '{:,}'.format(len(kids))), '',
 '**The JIT designs**: %d of the front, %d of its fastest tenth\'s %d; %s.' % (len(J), len(fj), k, genes), '',
 '**The fast end re-measured** (remeasure.json, %d designs): the fastest ten %s re-measured / in-run, the JIT designs %s, the rest %s.' % (
    len(ri), md([rr[i] for i in ri[:10]]), md([rr[i] for i in ri if jr(i)]), md([rr[i] for i in ri if not jr(i)])) if ri else None, '',
 '**The experiments**: the spread at generation 102 - %s; appbench - %s; the clock test - %s; truefronts - %s.' % (
    spread_row.strip() if spread_row else 'none', ab or 'none', ck or 'none', '%d runs' % tf.count('{"run"') if tf else 'none'), '',
 '**The remote checks** (results/xcheck-seed%d.md): %s.' % (N, rsp) if remote else None, '',
 'TODO: the verdict (rule 1), the predictions scored (results/predictions.md), the votes and the rules, the held-out check, the curse, progress - summary.md.']
 if x is not None)
out = os.path.join(ROOT, 'results', 'evolve-%s-seed%d.md' % (mach, N))
open(out, 'w').write(head + '\n\n---\n\n' + rep); print('draft-results: %s (%d TODO)' % (out, head.count('TODO')))
if remote:
    x = os.path.join(ROOT, 'results', 'xcheck-seed%d.md' % N)
    open(x, 'w').write("# The checks of seed %d's front during seed %d (Iteration %s)\n\n---\n\n" % (N - 1, N, it) + '\n\n---\n\n'.join(open(r).read().strip('\n') for r in remote) + '\n'); print('draft-results: ' + x)
if sp and '| run |' in sp:
    cf = os.path.join(ROOT, 'results', 'compare-fronts-%s.md' % mach); n = max([int(v) for v in re.findall(r'^## Session (\d+)', open(cf).read(), re.M)] or [0]) + 1
    tab = re.sub(r'/\S*?/runs/', '', sp[sp.index('| run |'):].split('\n\n')[0])
    open(cf, 'a').write('\n## Session %d - Iteration %s: seed %d and the archived runs (the chain\'s spread, at generation 102)\n\nTODO: what compares - the workloads and the memory of each.\n\n%s\n' % (n, it, N, tab.strip('\n')))
    print('draft-results: session %d appended to %s (1 TODO)' % (n, cf))
