#!/usr/bin/env python3
"""results/drafts/seed73-front-544.py DB REPORT - seed 73's true front (dominates(), as review-checks.py votes --db)
against the results file's shortcut front; the JIT genes' shares (prediction 518: jitexec), the extremes, the 32-bit
failures by encoding (Iteration 544)."""
import json, sys, os, re, bisect
dbp, rep = sys.argv[1], sys.argv[2]
sys.argv = ['x']; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../lab/evolve'))
import evolve as E
Rd = {}
for l in open(dbp, errors='replace'):
    if l.startswith('{'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id'): Rd[r['id']] = r
ok = [i for i, r in Rd.items() if r.get('status') == 'ok' and r.get('speed') and E.ov(r, 'total') and r.get('rss')]
E.TWO_WIDTHS[0] = sum(1 for i in ok if Rd[i].get('speed32')) * 2 > len(ok)
if E.TWO_WIDTHS[0]: ok = [i for i in ok if Rd[i].get('speed32')]
arch = []
for i in sorted(ok, key=lambda i: (E.ov(Rd[i], 'total'), Rd[i]['speed'])):
    if any(E.dominates(Rd[a], Rd[i]) for a in arch): continue
    arch = [a for a in arch if not E.dominates(Rd[i], Rd[a])]; arch.append(i)
by_t = sorted(ok, key=lambda i: E.ov(Rd[i], 'total')); tots = [E.ov(Rd[i], 'total') for i in by_t]
ids = [b for b in arch if not any(a != b and E.dominates(Rd[a], Rd[b]) for a in by_t[:bisect.bisect_right(tots, E.ov(Rd[b], 'total'))])]
short = set(m.group(1) for m in (re.match(r'\| ([0-9a-f]{10}) \|', l) for l in open(rep, errors='replace')) if m)
n = len(ids); k = max(1, n // 10)
print('true front %d designs (two widths: %s); the results file\'s shortcut front %d; in both %d' % (n, E.TWO_WIDTHS[0], len(short), len(short & set(ids))))
sp = {i: Rd[i]['speed'] for i in ids}; by = {i: E.ov(Rd[i], 'total') for i in ids}; mem = {i: Rd[i]['rss'] for i in ids}
f = min(ids, key=sp.get); s = min(ids, key=by.get); m = min(ids, key=mem.get)
print('fastest %s %.4f (%s bytes, 32-bit %.4f); smallest %s %s bytes (speed %.3f); least memory %s %s KB; most memory %s KB' % (
    f, sp[f], '{:,}'.format(by[f]), Rd[f].get('speed32') or 0, s, '{:,}'.format(by[s]), sp[s], m, mem[m], max(mem.values())))
ex = {i: E.express(E.canon(Rd[i]['genome'])) for i in ids}
jit = [i for i in ids if E.jit_on(E.canon(Rd[i]['genome']))]
fast = sorted(ids, key=sp.get)[:k]; fjit = [i for i in fast if i in jit]
print('JIT designs: %d of %d; in the fastest tenth (%d): %d' % (len(jit), n, k, len(fjit)))
for g in ('jitx', 'jitexec', 'jitfuse', 'jitmul', 'jitdoes', 'jitcfa', 'jitrp', 'jitret', 'jitvar', 'jitos', 'jitimg'):
    a = sum(1 for i in jit if ex[i].get(g)); b = sum(1 for i in fjit if ex[i].get(g))
    print('  %-8s on %3d of the %d JIT designs (%4.1f%%); %2d of the fastest tenth\'s %d' % (g, a, len(jit), 100.0 * a / max(1, len(jit)), b, len(fjit)))
for g in ('rtimm', 'rtfuse', 'tail'):
    print('  %-8s on %3d of %d front designs' % (g, sum(1 for i in ids if ex[i].get(g)), n))
f32 = [r for r in Rd.values() if r.get("why32")]
enc = {}
for r in f32: kk = (r["genome"].get("enc"), str(r.get("why32"))[:40], r.get("status")); enc[kk] = enc.get(kk, 0) + 1
print("32-bit failures, by encoding, cause and 64-bit status: %s" % enc)
