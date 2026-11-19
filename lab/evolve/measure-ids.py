#!/usr/bin/env python3
"""lab/evolve/measure-ids.py --ids FILE [--rounds R] [DB ...] - designs asked for by id measured as a run measures them
(Iteration 705): each record's genome in FILE (one JSON record a line, as loadtest.py --ids reads) built by evolve.evaluate
at both widths - the binary, the image, the five selection programs' code, the memory and both speeds, R rounds (default
3) - on this machine. For records made under another measure or on another machine: the new roles' holders (649's records
count binary + image only - appsize.one_size refuses to pool them; this sandbox's memory reads 12-16 KB above the
laptop's, results/drafts/holders-705.py), so a chain's first step gives them the laptop's numbers beside the candidates.
The databases a chain's experiment step passes are ignored. stdout: a line a design, then one JSON record a line (the
record as a run's database has it, with FILE's "why"), for the processing to read; a design that dies, its status."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
A = sys.argv[1:]
def opt(name, default=None):
    if name not in A: return default
    i = A.index(name); v = A[i + 1]; del A[i:i + 2]; return v
ids, rounds = opt('--ids'), int(opt('--rounds', '3'))
if not ids: sys.exit(__doc__)
if not os.path.exists(ids): ids = os.path.join(os.path.dirname(os.path.dirname(HERE)), ids)   # a chain names it from the repository
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths()
recs = [json.loads(l) for l in open(ids) if l.startswith('{"') and '"genome": {' in l]
print('# measure-ids.py --ids %s --rounds %d: %d designs, both widths, on %s\n' % (os.path.basename(ids), rounds, len(recs),
      os.uname().nodename), flush=True)
out = []
for r in recs:
    g = E.canon(E.require(dict(r['genome'])))
    try: rec = E.evaluate(g, rounds)
    except Exception as e: rec = {'status': 'died: %s' % str(e)[:120]}
    rec.update(id=E.gid(g), genome=g, gen=0, how='measure-ids.py', why=r.get('why', ''))
    print('- %s %s: total %s (binary %s, image %s, programs %s), memory %s KB, speed %s, at 32 bits %s' % (
        rec['id'], rec['status'], rec.get('total'), rec.get('bin'), rec.get('size'), rec.get('app'), rec.get('rss'),
        rec.get('speed') and '%.4f' % rec['speed'], rec.get('speed32') and '%.4f' % rec['speed32']), flush=True)
    out.append(rec)
print()
for rec in out: print(json.dumps(rec, sort_keys=True))
