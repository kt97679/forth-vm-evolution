# results/drafts/price-410.md, "Fixed" - in a scratch clone with the after-seed-62 batch to patch 11, its stages built.
# Iteration 412: 4ac602c8bd with rtiplus on, with the pending batch to patch 11 - built and alive (the corpus, the kernel workload).
import json, os, shutil, sys
os.chdir('/tmp/b65'); sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
r = next(json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed60.md') if l.startswith('{"') and '4ac602c8bd' in l)
for v in (0, 1):
    g = E.canon(dict(r['genome'], rtiplus=v)); d = os.path.join(E.EV, 'ipa%d' % v); shutil.rmtree(d, ignore_errors=True)
    try: eng, img = E.build(g, d); E.alive(eng, img, E.private_work(d)); res = 'alive'
    except Exception as e: res = 'FAILED ' + str(e)[:150]
    print('rtiplus=%d: %s, image %s bytes' % (v, res, os.path.getsize(os.path.join(d, 'image.img')) if os.path.exists(os.path.join(d, 'image.img')) else '?'), flush=True)
