# results/drafts/price-410.md, "The rest of the table" - in a scratch clone with the after-seed-62 batch and
# results/drafts/t2pairs-instrument-413.patch applied (LAYOUT_T2PAIRS: the converter reports its kept and dropped entries).
# Iteration 413: seed 60's front designs built with the after-seed-62 batch; each one's run-time pair table on the
# two-bit tag - how many entries the converter keeps (one-byte codes) and drops (an escaped opcode).
import json, os, shutil, sys
os.chdir('/tmp/b66'); sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
F = [json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed60.md') if l.startswith('{"')]
F.sort(key=lambda r: r['speed']); pick = F[::7][:24]
for r in pick:
    g = E.canon(r['genome']); e = E.express(g); d = os.path.join(E.EV, 't2p'); shutil.rmtree(d, ignore_errors=True)
    rep = '/tmp/t2/%s.txt' % r['id']; os.environ['LAYOUT_T2PAIRS'] = rep
    try: E.build(g, d); txt = open(rep).read().split('\n') if os.path.exists(rep) else ['no table (no rtfuse overlay)']
    except Exception as x: txt = ['build failed: ' + str(x)[:100]]
    print('%s speed %.3f rtfuse %s jit %s supers %d | %s | dropped: %s' % (r['id'], r['speed'], e.get('rtfuse'), e.get('jit'), len(g.get('supers') or []), txt[0], (txt[2][9:] if len(txt) > 2 else '')[:160]), flush=True)
