# results/rehearsal-405.md - the after-seed-62 batch's rehearsal (Iteration 405); run in a scratch clone with the batch applied.
# Iteration 405: patch 9 - seed 59's front designs with tail (GCC) on the two-bit tag, evaluated as a run does at both widths.
import json, os, sys
os.chdir('/tmp/b63'); sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths()
F = [json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed59.md') if l.startswith('{"bin"')]
ex = lambda g: E.express(E.canon(g))
plain = [r for r in F if not ex(r['genome']).get('jit') and ex(r['genome']).get('tos')][:3]
for r in plain:
    g = E.canon(dict(r['genome'], tail=1)); e = E.express(g)
    try: rec = E.evaluate(g, 1)
    except Exception as x: rec = {'status': 'EXCEPTION ' + str(x)[:150]}
    print('+tail, GCC %s (tag2 %s, tail %s): %s speed %s, 32-bit %s%s' % (r['id'], e.get('tag2'), e.get('tail'), rec.get('status'), rec.get('speed') and round(rec['speed'], 3), rec.get('speed32') and round(rec['speed32'], 3), (' - ' + str(rec['why32'])[:100]) if rec.get('why32') else ''), flush=True)
