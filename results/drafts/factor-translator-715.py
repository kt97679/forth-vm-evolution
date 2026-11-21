# results/drafts/factor-translator-715.py DB ID [4] - the translator's factor lines (tools/layout.py --factor) for a
# record's genome, built by the evolver (lab/evolve/evolve.py build) in a scratch directory under /tmp/fac (Iteration 715).
# The translator's factor lines for a record's genome: python3 tr.py DB ID [4]
import json, os, sys, tempfile
db, i = sys.argv[1], sys.argv[2]; w4 = len(sys.argv) > 3
R = {json.loads(l)['id']: json.loads(l) for l in open(db) if l.startswith('{')}
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
_sh = E.sh
def sh(cmd, *a, **k):
    r = _sh(cmd, *a, **k)
    if any('layout.py' in str(c) for c in cmd):
        print('ARGS:', ' '.join(str(c) for c in cmd[2:]))
        for l in ((getattr(r, 'stdout', b'') or b'').decode() if isinstance(getattr(r, 'stdout', ''), bytes) else (getattr(r, 'stdout', '') or '')).splitlines():
            if 'factor' in l or 'headerless' in l or 'image' in l.lower()[:20]: print('  ', l)
    return r
E.sh = sh
E.setup(); E.TWO_WIDTHS[0] = True; E.setup_widths(); E.TWO_WIDTHS[0] = False
d = tempfile.mkdtemp(prefix='tr-', dir=os.environ.get('TMPDIR', '/tmp'))
ctx = E.at_width(E.WIDTH4) if w4 else __import__('contextlib').nullcontext()
with ctx: print(E.build(E.canon(R[i]['genome']), d))
