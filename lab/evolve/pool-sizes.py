#!/usr/bin/env python3
"""lab/evolve/pool-sizes.py --list FILE [--free B] [--jit B] [--minutes M] DB ... - the pool's small end built at today's
master, to find a design a size change has moved past the ones a list measures (Iteration 713; the owner: "ensure we are
not losing good designs"). The after-seed-96 batch took 482-2,224 bytes off the engines, not evenly - fbuf=2's engines
16 more than the six at 21,679 B - so 219878ec89 (22,419 B before, 21,673 after) passed them while off chain A's list.
Every alive record of the databases (a chain's experiment step passes every run's here: seed 96's and the archived) not in
FILE (by id) with a total up to --free (JIT-free, default 22,700) or --jit (JIT designs, default 34,300 - wends16 takes up
to 2,224), the smallest first, built by evolve.build at 8-byte cells: the engine, the image, the five programs' code, the
total - for --minutes (default 40; the JIT-free designs 3/4 of it, then the JIT ones; --free 0: the JIT ones all of it).
--below-free B / --below-jit B: report the designs below B instead of FILE's smallest (713 - chain C: --jit 39100
--below-jit 36805, the smallest JIT design's middle; the processing compares their in-run speeds in in-run terms). stdout: a summary, then each design
smaller than FILE's smallest after the change (JIT-free, and JIT apart) as one record a line - its record, "bin" and
"total" master's, "before_batch" the database's - for the processing: a list for the next chain if there are any. FILE's
records carry master's sizes already (results/drafts/sizes-713.py). Never exits non-zero: a build that fails is a line."""
import json, os, shutil, sys, tempfile, time
HERE = os.path.dirname(os.path.abspath(__file__))
A = sys.argv[1:]
def opt(n, d=None):
    if n not in A: return d
    i = A.index(n); v = A[i + 1]; del A[i:i + 2]; return v
lst = opt('--list'); mf, mj = int(opt('--free', '22700')), int(opt('--jit', '34300')); mins = float(opt('--minutes', '40'))
bf, bj = opt('--below-free'), opt('--below-jit')        # 713: report below these, not the list's smallest (chain C: the
                                                        # smallest JIT design's middle - below its holder, 36,805 B)
if not lst: sys.exit(__doc__)
if not os.path.exists(lst): lst = os.path.join(os.path.dirname(os.path.dirname(HERE)), lst)   # a chain names it from the repository
dbs = A
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
L = {r['id']: r for r in (json.loads(l) for l in open(lst) if l.startswith('{"') and '"genome": {' in l)}
isjit = lambda g: bool(E.express(E.canon(g)).get('jit'))
small = {False: min((r['total'] for r in L.values() if not isjit(r['genome'])), default=None),
         True: min((r['total'] for r in L.values() if isjit(r['genome'])), default=None)}
if bf: small[False] = int(bf)
if bj: small[True] = int(bj)
P = {}
for db in dbs:
    try:
        for l in open(db):
            if not l.startswith('{'): continue
            try: r = json.loads(l)
            except ValueError: continue
            if r.get('status') != 'ok' or 'total' not in r or 'genome' not in r or r.get('id') in L or r.get('id') in P: continue
            if r['total'] <= max(mf, mj): P[r['id']] = r
    except OSError as e:
        print('pool-sizes: %s unread (%s)' % (db, e))
J = {i: isjit(r['genome']) for i, r in P.items()}
want = {False: sorted((i for i in P if not J[i] and P[i]['total'] <= mf), key=lambda i: (P[i]['total'], i)),
        True: sorted((i for i in P if J[i] and P[i]['total'] <= mj), key=lambda i: (P[i]['total'], i))}
print('# pool-sizes.py --list %s: %d databases, %d records off the list - %d JIT-free up to %d B, %d JIT up to %d B; the list\'s '
      'smallest or --below: %s (JIT-free) and %s (JIT), master\'s sizes\n' % (os.path.basename(lst), len(dbs), len(P), len(want[False]), mf,
      len(want[True]), mj, small[False], small[True]), flush=True)
t0 = time.time(); done = {False: 0, True: 0}; found = []; died = 0
tmp = tempfile.mkdtemp(prefix='pool-sizes-')
try:
    for j, share in ((False, 0.75), (True, 1.0)):
        for i in want[j]:
            if time.time() - t0 > mins * 60 * share: break
            r = P[i]; g = E.canon(r['genome']); dd = os.path.join(tmp, i)
            try:
                eng, img = E.build(g, dd); pw = E.private_work(dd); E.alive(eng, img, pw, far=True)
                a = E.app_size(eng, img, pw); b = E.bin_size(eng); t = b + os.path.getsize(img) + sum(a)
            except Exception as e:
                died += 1; print('- %s %s: %s' % (i, 'JIT' if j else 'JIT-free', str(e)[:120]), flush=True); continue
            finally:
                shutil.rmtree(dd, ignore_errors=True)
            done[j] += 1
            if small[j] is not None and t < small[j]:
                found.append(dict(r, bin=b, total=t, before_batch=dict(bin=r['bin'], total=r['total']),
                                  why='pool-sizes.py: %d B after the batch, below %d' % (t, small[j])))
                print('- %s %s: %d -> %d B, below %d' % (i, 'JIT' if j else 'JIT-free', r['total'], t, small[j]), flush=True)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
for j in (False, True):
    n = len(want[j]); last = P[want[j][done[j] - 1]]['total'] if done[j] else None
    print('%s: %d of %d built in the time%s' % ('JIT' if j else 'JIT-free', done[j], n,
          ', up to %d B before the batch' % last if last else ''))
print('built in %.0f s; %d failed; %d below the threshold\n' % (time.time() - t0, died, len(found)))
for r in found: print(json.dumps(r, sort_keys=True))
