#!/usr/bin/env python3
"""results/drafts/sizes-713.py LIST OUT.json [--max-free B] [--max-jit B] [--ids a,b,...] - chain A's designs built at
master (the after-seed-96 batch applied, 713) as the search builds them, at 8-byte cells: the engine's bytes, the image's,
the five selection programs' code and the total (the size score's), beside the list's record (chain A's, before the
batch). Which: every JIT-free design of LIST with a total up to --max-free (default 23,600: the smallest role's
contenders - the batch takes 418-1,162 bytes off an x86-64 engine, by compiler), every JIT design up to --max-jit (default
40,000: the smallest JIT design's - wends16 takes ~1.1 KB off a jitx engine), and --ids. Sizes are exact: chain B's
records carry them (shortlist-713.py). Resumable: OUT's designs are kept. About 3 s a design; run detached."""
import json, os, shutil, sys, tempfile
A = sys.argv[1:]
def opt(n, d=None):
    if n not in A: return d
    i = A.index(n); v = A[i + 1]; del A[i:i + 2]; return v
mf, mj, ids = int(opt('--max-free', '23600')), int(opt('--max-jit', '40000')), opt('--ids', '')
lst, out = A[0], A[1]
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve')
sys.path.insert(0, HERE); sys.argv = ['x']
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()     # the kernel references, both widths (setup_widths: 4 only)
C = {r['id']: r for r in (json.loads(l) for l in open(lst) if l.startswith('{"'))}
jit = {i: bool(E.express(E.canon(C[i]['genome'])).get('jit')) for i in C}
want = [i for i in C if (C[i]['total'] <= (mj if jit[i] else mf))] + [i for i in ids.split(',') if i in C]
want = sorted(set(want), key=lambda i: C[i]['total'])
R = json.load(open(out)) if os.path.exists(out) else {}
print('sizes-713: %d designs (%d JIT), %d done before' % (len(want), sum(jit[i] for i in want), sum(i in R for i in want)), flush=True)
tmp = tempfile.mkdtemp(prefix='sizes-713-')
try:
    for i in want:
        if i in R: continue
        g = E.canon(C[i]['genome']); dd = os.path.join(tmp, i)
        try:
            eng, img = E.build(g, dd); pw = E.private_work(dd); E.alive(eng, img, pw, far=True)
            a = E.app_size(eng, img, pw)
            r = dict(bin=E.bin_size(eng), image=os.path.getsize(img), app=sum(a))
            r['total'] = r['bin'] + r['image'] + r['app']
        except Exception as e:
            r = dict(error=str(e)[:200])
        r.update(jit=jit[i], before=dict(bin=C[i]['bin'], image=C[i]['size'], app=C[i]['app'], total=C[i]['total']))
        R[i] = r; shutil.rmtree(dd, ignore_errors=True)
        json.dump(R, open(out, 'w'), indent=0, sort_keys=True)
        print('%s %s %s' % (i, 'JIT ' if jit[i] else 'free', r.get('total', r.get('error'))), flush=True)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
print('sizes-713: DONE %d' % len(R), flush=True)
