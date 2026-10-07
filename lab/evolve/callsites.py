#!/usr/bin/env python3
"""callsites.py ID [ID ...] [--db FILE ...] - a design's calls in the two-bit
tag (FORMAT-TAG2.md), counted, and what inlining short words and Forth tail
calls would buy: priced before anything is built (lab/evolve/GENES.md,
"Candidates (Iterations 82-86)", 1 and 2).

Iteration 13's tool priced one-byte calls (results/price-hotcalls-seed3-front.md).
Ported to the tag in Iteration 88: the tag has no hot calls, so that price is
gone (git history keeps it); the census and the profile stay, read for two
other questions.

--db: a database, or a run report in results/ - each ends with its front's
genomes as JSON lines (Iteration 87), the other lines are skipped. Repeatable;
by default build/evolve/db.jsonl and every run report in results/.

For each design:

  1. The census. The converter writes the image's code as it lays it out
     (CALLMAP, tools/layout.py): every call site (offset, length, target),
     every operation (its name), every word's body, every branch target, and
     the tag's codes.
  2. The profile. Built with the engine's profiler (VMPROF): each workload's
     dispatches by address, and every call by its return address - the
     image's and those compiled at run time alike - with the byte after the
     call and the callee's first eight bytes, read as the run ends.
  3. Inlining short words: a call whose callee's body is at most two
     operations, each a one-byte code without an operand, then EXIT - or the
     last with its EXIT folded - none touching the return stack. A site saves
     the call's bytes less the operations'; a run, the call's dispatch and
     the callee's EXIT (none where the EXIT was folded).
  4. Forth tail calls: a call followed by EXIT becomes a BRANCH to the callee
     (BRANCH8 where it reaches). A site saves the call and the EXIT - which
     stays where something branches to it - less the branch; a run, the
     caller's EXIT. Callees that read their own return address (R> R@ RDROP
     RP@ RP! in their body) are counted apart.

Bytes are counted, not laid out again: a body that starts on a cell (data,
inline cells) can swallow a byte saved before it. Code compiled at run time
is not in the image: it counts in the dynamic columns only.

Audits - each stops the tool: the image is the size its record says; every
site's bytes decode to its target; every dispatched address in the image
holding a call's first byte is a census site; the profile's dispatches by
address sum to its dispatches by pair, and its calls by return address to
its calls by pair; every call it saw return into the image is a census site,
run as often as that site was dispatched.
"""
import collections, glob, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
args = sys.argv[1:]; dbs = []
while '--db' in args: i = args.index('--db'); dbs.append(args[i + 1]); del args[i:i + 2]
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
dbs = dbs or [os.path.join(ROOT, 'build', 'evolve', 'db.jsonl')] + sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*.md')))
recs = {}
for db in dbs:
    if not os.path.exists(db): continue
    for l in open(db, errors='replace'):
        try: r = json.loads(l)
        except ValueError: continue
        if isinstance(r, dict) and 'genome' in r and 'id' in r: recs[r['id']] = r
if [d for d in args if d not in recs]: sys.exit('no record of %s in %s' % (' '.join(d for d in args if d not in recs), ' '.join(dbs)))
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
WORKS = E.WORK_SEL + E.WORK_HELD
RA_READ = {'R>', 'R@', 'RDROP', '2R>', '2R@', 'RP@', 'RP!'}         # a callee's own return address, read
RSTACK = RA_READ | {'>R', '2>R', 'I', 'J', 'UNLOOP', '(DO)', '(?DO)', '(LOOP)', '(+LOOP)', '(LEAVE)', 'I+', 'EXECUTE'}
OPND = ('LIT', 'BRANCH', 'ADDI', 'EQI', '(LOOP)', '(+LOOP)', '(?DO)', '(LEAVE)', 'SWAP+I', 'JIT', 'DOVAR', 'DODOES')
def parts(name): return (name[:-5] if name.endswith(';EXIT') else name).split(' ')
pct = lambda a, b: '%.1f%%' % (100.0 * a / b) if b else '-'

def census(g, d):
    """Build g in d with the call map and the profiler: (engine, image, the map's lines)."""
    cm = d.rstrip('/') + '.map'
    if os.path.exists(cm): os.remove(cm)
    os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
    g2 = dict(g, tail=0, msc=0)                             # the profiler reads the plain dispatch; the image
    if not E.jit_on(g): g2['jit'] = 0                       # depends on neither - but a JIT gene they kept dormant
    try: eng, img = E.build(g2, d)                          # would wake (e83972af52: 136 bytes more)
    finally: E.PROFILING[0] = False; del os.environ['CALLMAP']
    return eng, img, [l.rstrip('\n').split(' ') for l in open(cm)]

SUMMARY = []
for did in args:
    rec = recs[did]; g = E.canon(rec['genome'])
    if not (g.get('tag2') and g['bytehdr']): sys.exit('%s is not in the two-bit tag: this tool reads the tag only' % did)
    d = os.path.join(E.EV, 'callsites'); shutil.rmtree(d, ignore_errors=True)
    eng, img, M = census(g, d)
    hdr, n, _ = map(int, M[0][1:4]); assert M[0][0] == 'H', 'no header line in the call map'
    im = open(img, 'rb').read()[hdr:]
    assert len(im) == n == rec['size'] - hdr, 'image %d bytes after a %d-byte header, the map says %d, the record %d' % (len(im), hdr, n, rec['size'])
    C = {int(f[1]): dict(len=int(f[2]), t=int(f[3]), forced=int(f[5]), caller=f[6], target=' '.join(f[7:])) for f in M if f[0] == 'C'}
    O = {int(f[1]): ' '.join(f[4:]) for f in M if f[0] == 'O'}
    T = {int(f[1]) for f in M if f[0] == 'T'}
    Wd = {int(f[1]): (int(f[2]), f[3], ' '.join(f[4:])) for f in M if f[0] == 'W'}
    ONE = {' '.join(f[3:]): int(f[2]) for f in M if f[:2] == ['M', '1']}
    SEL = {int(f[2]): ' '.join(f[3:]) for f in M if f[:2] == ['M', '2']}
    ESC = [int(f[2]) for f in M if f[:2] == ['M', 'E']][0]
    BYTE = {c: x for x, c in ONE.items()}
    for a, s in C.items():                                  # every site decodes to its target
        b = im[a]; v = b & 0x3F
        for k in range(1, s['len']): v = v << 8 | im[a + k]
        assert (b >> 6) + 1 == s['len'] and v == s['t'], 'site %d: %d bytes from %#x decode to %d, the map says %d' % (a, s['len'], b, v, s['t'])
    starts = sorted(set(O) | set(C))
    def items(at, end):                                     # (name, bytes, call?) from at to the body's end
        out = [x for x in starts if at <= x < end]
        return [(O.get(x, 'call'), (out[i + 1] if i + 1 < len(out) else end) - x, x in C) for i, x in enumerate(out)]
    def has_opnd(name):                                     # by name: a length would count NOOP padding too
        return any(x in name for x in OPND) or name in ('vf', 'vs', 'LSAVE', 'LRESTORE', 'L!', 'LZERO')
    def short(body):
        """A body's first operations -> (bytes inlined, dispatches a run saves, None) or (None, None, why not)."""
        ops = []
        for name, nb, call in body:
            if call: return None, None, 'a call' if name != 'data' else 'not code'
            if name == 'EXIT': saves = 2; break
            ops.append((name, nb))
            if name.endswith(';EXIT'): saves = 1; break
            if len(ops) > 2: return None, None, 'longer'
        else: return None, None, 'longer'
        if len(ops) > 2: return None, None, 'longer'
        if any(p in RSTACK for nm, _ in ops for p in parts(nm)): return None, None, 'return stack'
        if any(has_opnd(nm) for nm, _ in ops): return None, None, 'an operand'
        if any(ONE.get(nm[:-5] if nm.endswith(';EXIT') else nm) is None for nm, _ in ops): return None, None, 'an escaped code'
        return len(ops), saves, None
    def constant(body):
        """Outside the agreed definition, priced beside it: a body that is one literal
        and EXIT (a CONSTANT) -> (its bytes, the dispatches a run saves) or None."""
        if body and not body[0][2] and 'LIT' in body[0][0]:
            if body[0][0].endswith(';EXIT') or body[0][0] == 'LIT8X': return body[0][1], 1
            if len(body) > 1 and body[1][0] == 'EXIT': return body[0][1], 2
        return None
    def decode(y):                                          # a callee compiled at run time, from its first bytes
        k = 5 if y[0] == ONE.get('JIT') else 0; out = []
        while k < 8:
            b = y[k]
            if b >= 0x40: out.append(('call', (b >> 6) + 1, True)); break
            if b == ESC:
                if k + 1 >= 8: break
                out.append((SEL.get(y[k + 1], '?'), 2, False)); k += 2
            else: out.append((BYTE.get(b, '?'), 1, False)); k += 1
        return out
    def body_of(t, y=None):                                 # y: a run-time callee's first bytes, in its run
        if t in Wd and Wd[t][1] == 'code': return items(t, Wd[t][0])
        if t < n: return [('data', 1, True)]                # a data word or a DOES> tail: not short
        return decode(y)

    # ---- the profile: one fresh file per workload (the profiler appends)
    pw = E.private_work(d); D, CALLS, R = {}, {}, {}
    for w in WORKS:
        pf = os.path.join(d, 'prof-' + w)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=20, env=dict(os.environ, VMPROF=pf))
        ipc, pairs, pcalls, rl = collections.Counter(), 0, 0, {}
        for f in (l.split() for l in open(pf)):
            if f[0] == 'I': ipc[int(f[1])] += int(f[2])
            elif f[0] == 'R': rl[int(f[1])] = (int(f[2]), int(f[3]), int(f[4]), [int(x) for x in f[5:13]])
            elif f[0] != 'C':
                pairs += int(f[2]); pcalls += int(f[2]) if int(f[1]) == 256 else 0
        assert sum(ipc.values()) == pairs, '%s: %d dispatches by address, %d by pair' % (w, sum(ipc.values()), pairs)
        assert sum(x[1] for x in rl.values()) == pcalls, '%s: %d calls by return address, %d by pair' % (w, sum(x[1] for x in rl.values()), pcalls)
        for a, k in ipc.items():
            if a < n and im[a] >= 0x40 and a not in C: sys.exit('%s: a call dispatched at %d is not in the census' % (w, a))
        for r, (t, k, nx, y) in rl.items():
            if r > n: continue
            s = [a for a, c in C.items() if a + c['len'] == r]
            assert s and C[s[0]]['t'] == t and ipc[s[0]] == k, '%s: a call returning to %d is not a census site run %d times' % (w, r, k)
        D[w], CALLS[w], R[w] = pairs, pcalls, rl

    # ---- inlining: the image's sites, then every call the profile saw
    code = {a: s for a, s in C.items() if s['caller'] != '(prologue)'}
    why, inl = collections.Counter(), {}
    cst = {}
    for a, s in code.items():
        k, sv, no = short(body_of(s['t']))
        if no: why[no] += 1
        else: inl[a] = (s['len'] - k, sv)
        c = constant(body_of(s['t']))
        if no and c: cst[a] = s['len'] - c[0]
    byt = collections.defaultdict(lambda: [0, 0, set()])
    for a, (b, sv) in inl.items(): x = byt[code[a]['target']]; x[0] += 1; x[1] += b; x[2].add(' '.join(nm for nm, _, _ in body_of(code[a]['t'])[:3]))
    cache = {}
    def runtime_short(t, y):
        key = t if t < n else (t, tuple(y))
        if key not in cache: cache[key] = short(body_of(t, y))[:2] + (constant(body_of(t, y)),)
        return cache[key]
    dyn = {w: collections.Counter() for w in WORKS}
    tgt_dyn = collections.defaultdict(collections.Counter)
    exitc = ONE['EXIT']
    for w in WORKS:
        for r, (t, k, nx, y) in R[w].items():
            where = 'img' if r <= n else 'rt'
            k_, sv, c = runtime_short(t, y)
            if k_ is None and c: dyn[w]['const_' + where] += k * c[1]
            if k_ is not None:
                dyn[w]['inl_' + where] += k * sv
                tgt_dyn[Wd[t][2] if t in Wd else 'a run-time word: ' + ' '.join(nm for nm, _, _ in body_of(t, y)[:3])][w] += k
            if nx == exitc:
                rd = any(p in RA_READ for nm, _, c in body_of(t) if not c for p in parts(nm)) if t < n else False
                dyn[w][('tail_' if not rd else 'tailx_') + where] += k
    # ---- tail calls: the image's sites
    tail, tailx = {}, collections.Counter()
    b8 = 'BRANCH8' in ONE
    for a, s in code.items():
        e = a + s['len']
        if O.get(e) != 'EXIT' or e in C: continue
        body = body_of(s['t'])
        if s['t'] < n and any(p in RA_READ for nm, _, c in body if not c for p in parts(nm)): tailx[s['target']] += 1; continue
        o = s['t'] - (a + 1)
        br = 2 if b8 and -128 <= o <= 127 else 3
        tail[a] = s['len'] + (0 if e in T else 1) - br, e in T, br == 2
    both = sum(1 for a in tail if a in inl)

    # ---- the report
    lens = collections.Counter(s['len'] for s in code.values())
    print('## %s - image %s bytes, %s total with the engine; speed %.3f\n' % (did, format(rec['size'], ','), format(rec.get('total', 0), ','), rec['speed']))
    print('%d call sites in the image\'s code to %d targets (%s; %d before an inline operand).\n'
          % (len(code), len({s['t'] for s in code.values()}), ', '.join('%d bytes: %d' % (k, lens[k]) for k in sorted(lens)), sum(s['forced'] for s in code.values())))
    print('| workload | dispatches | calls | from the image | from run-time code | inlining saves: image | run-time | tail calls save: image | run-time |')
    print('|---|---|---|---|---|---|---|---|---|')
    for w in WORKS:
        x = dyn[w]; ci = sum(v[1] for r, v in R[w].items() if r <= n)
        print('| %s | %s | %s (%s) | %s | %s | %s | %s | %s | %s |' % (w, format(D[w], ','), format(CALLS[w], ','), pct(CALLS[w], D[w]), pct(ci, CALLS[w]), pct(CALLS[w] - ci, CALLS[w]),
              pct(x['inl_img'], D[w]), pct(x['inl_rt'], D[w]), pct(x['tail_img'], D[w]), pct(x['tail_rt'], D[w])))
    print('\n(Dispatches saved, as a share of the workload\'s. Constants - outside the agreed definition: '
          + ', '.join('%s %s' % (w, pct(dyn[w]['const_img'] + dyn[w]['const_rt'], D[w])) for w in WORKS)
          + '; in the image %d sites, %d bytes. Tail calls whose callee reads its return address are left out: ' % (len(cst), sum(cst.values()))
          + ', '.join('%s %s' % (w, pct(dyn[w]['tailx_img'] + dyn[w]['tailx_rt'], D[w])) for w in WORKS) + '.)\n')
    print('**Inlining, the image**: %d sites to %d short words, %d bytes (%d where the call is longer than the body). Not short: %s.\n'
          % (len(inl), len(byt), sum(b for b, _ in inl.values()), sum(1 for b, _ in inl.values() if b > 0), ', '.join('%s %d' % kv for kv in why.most_common())))
    top = sorted(byt, key=lambda x: (-byt[x][1], -byt[x][0], x))[:12]
    if top:
        print('| short word | body | sites | bytes | ' + ' | '.join('runs: ' + w for w in WORKS) + ' |')
        print('|---|---|---|---|' + '---|' * len(WORKS))
        for x in top: print('| %s | %s | %d | %d | %s |' % (x, ' / '.join(sorted(byt[x][2])), byt[x][0], byt[x][1], ' | '.join(format(tgt_dyn[x][w], ',') for w in WORKS)))
    hot = sorted(tgt_dyn, key=lambda x: -sum(tgt_dyn[x][w] / max(1, D[w]) for w in WORKS))[:10]
    print('\nThe short words most called, everywhere (image and run-time code): ' + '; '.join('%s %s' % (x, '/'.join(pct(tgt_dyn[x][w], CALLS[w]) for w in WORKS)) for x in hot)
          + ' (share of each workload\'s calls, in the order %s).\n' % '/'.join(WORKS))
    print('**Tail calls, the image**: %d sites, %d bytes - the EXIT goes at %d, stays (a branch target) at %d; BRANCH8 reaches at %d. '
          'Callees reading their return address, left out: %d sites (%s). %d sites are inlining\'s too.\n'
          % (len(tail), sum(v[0] for v in tail.values()), sum(1 for v in tail.values() if not v[1]), sum(1 for v in tail.values() if v[1]),
             sum(1 for v in tail.values() if v[2]), sum(tailx.values()), ', '.join('%s %d' % kv for kv in tailx.most_common(6)) or '-', both))
    SUMMARY.append((did, rec, len(inl), sum(b for b, _ in inl.values()), len(tail), sum(v[0] for v in tail.values()),
                    {w: (dyn[w]['inl_img'] + dyn[w]['inl_rt']) / max(1, D[w]) for w in WORKS},
                    {w: (dyn[w]['tail_img'] + dyn[w]['tail_rt']) / max(1, D[w]) for w in WORKS},
                    {w: (dyn[w]['const_img'] + dyn[w]['const_rt']) / max(1, D[w]) for w in WORKS}, len(cst), sum(cst.values())))
    shutil.rmtree(d, ignore_errors=True)

if len(SUMMARY) > 1:
    print('## Summary\n\nPer design: the image\'s sites and bytes, and the dispatches saved on each workload (image and run-time code), %s.\n' % '/'.join(WORKS))
    print('| design | speed | image | inlining: sites | bytes | dispatches saved | tail calls: sites | bytes | dispatches saved | constants: sites | bytes | dispatches saved |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for did, rec, si, bi, st, bt, di, dt, dc, sc, bc in SUMMARY:
        print('| %s | %.3f | %s | %d | %d | %s | %d | %d | %s | %d | %d | %s |' % (did, rec['speed'], format(rec['size'], ','), si, bi, '/'.join('%.1f' % (100 * di[w]) for w in WORKS),
              st, bt, '/'.join('%.1f' % (100 * dt[w]) for w in WORKS), sc, bc, '/'.join('%.1f' % (100 * dc[w]) for w in WORKS)))
