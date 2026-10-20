# results/wip-regmachine/README.md, "Where the bytes go" - seed 58's smallest design as it is, with the immediates
# (rtimm=2) and with the loop compiler (rtloop=1): engine and image bytes, and the image's words from the converter's map
# (CALLMAP's W lines: each word's body; a byte header adds its name's length and 2-3 bytes) - the words a variant adds
# or changes, largest first.
import collections, json, os, shutil, sys
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
r = next(json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed58.md') if l.startswith('{"') and '09de03f091' in l)
g0 = dict(r['genome'])
def words(g):
    d = os.path.join(E.EV, 'rmbytes'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    cm = os.path.join(d, 'callmap'); os.environ['CALLMAP'] = cm
    try: eng, img = E.build(E.canon(g), d)
    finally: os.environ.pop('CALLMAP', None)
    w = collections.defaultdict(list)
    for l in open(cm):
        f = l.split(None, 4)
        if f and f[0] == 'W' and len(f) == 5: w[f[4].strip()].append(int(f[2]) - int(f[1]))
    return os.path.getsize(eng), os.path.getsize(img), w
be, bi, bw = words(g0)
print('as it is: engine %d, image %d bytes; %d words, bodies %d bytes' % (be, bi, sum(len(v) for v in bw.values()), sum(map(sum, bw.values()))))
for name, g in [('rtimm=2', dict(g0, rtimm=2)), ('rtloop=1', dict(g0, rtloop=1))]:
    e, i, w = words(g)
    added = [(n, sum(v), len(v)) for n, v in w.items() if n not in bw]
    changed = [(n, sum(v) - sum(bw[n]), len(v) - len(bw[n])) for n, v in w.items() if n in bw and sum(v) != sum(bw[n])]
    hdr = sum(len(n) + 3 for n, s, k in added for _ in range(k))
    print('\n%s: engine %+d, image %+d bytes; %d words added - bodies %d bytes, headers about %d; %d words changed, %+d bytes' % (
        name, e - be, i - bi, sum(k for n, s, k in added), sum(s for n, s, k in added), hdr, len(changed), sum(s for n, s, k in changed)))
    print('  added, largest: ' + '; '.join('%s %d%s' % (n, s, ' (x%d)' % k if k > 1 else '') for n, s, k in sorted(added, key=lambda x: -x[1])[:16]))
    if changed: print('  changed: ' + '; '.join('%s %+d' % (n, s) for n, s, k in sorted(changed, key=lambda x: -abs(x[1]))[:8]))
