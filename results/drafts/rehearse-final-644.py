#!/usr/bin/env python3
"""results/drafts/rehearse-final-644.py SRC OUT_tar.gz - the final check's processing rehearsed at its size (Iteration
644). The tools that process a follow-up (lab/evolve/process-followup.sh: chain-sessions.py, final-pick.py,
followup-roles.py) had seen 282 designs at most; the final check measures 435 (results/followup-seed91-final.md). From a
real chain unpacked at SRC (seed 91's follow-up: its packs, its remote lines) this writes an archive of the same layout
whose every session holds the 435: a design that chain measured keeps its own readings, any other gets the readings of the
measured design nearest it in-run, scaled by their in-run ratio at that width, with 0.6% noise a reading (seeded). The
rejected samples stay as measured. Synthetic numbers - the rehearsal tests the processing, nothing about the designs.
Then: OUT=/tmp/rh DEST=/tmp/rh-dest sh lab/evolve/process-followup.sh 91-final ITER ROLES OUT_tar.gz."""
import glob, json, math, os, random, shutil, sys, tarfile, tempfile

SRC, OUT = sys.argv[1].rstrip('/'), sys.argv[2]
LIST = 'results/followup-seed91-final.md'
L = [json.loads(l) for l in open(LIST) if l.startswith('{')]
ids = [r['id'] for r in L]; LR = {r['id']: r for r in L}
sys.path.insert(0, 'lab/evolve'); sys.argv = ['x']; import evolve as E


def near(d, real, key):
    """the measured design nearest d in-run at this width (key: the record's in-run field)"""
    w = 'speed32' if key in ('inrun32', 'speed32') else 'speed'
    return min(real, key=lambda b: abs(math.log(LR[d][w] / real[b][key])))


def noisy(rnd):
    return math.exp(rnd.gauss(0, 0.006))


def loadtest(path, tag):
    lines = open(path).read().split('\n')
    real = {}
    for l in lines:
        if l.startswith('{"'): r = json.loads(l); real[r['id']] = r
    out, done = [], False
    for l in lines:
        if l.startswith('{"'):
            if done: continue
            done = True
            for d in ids:
                if d in real: out.append(json.dumps(real[d])); continue
                rnd = random.Random('%s %s' % (tag, d))
                b64, b32 = near(d, real, 'inrun'), near(d, real, 'inrun32')
                f64, f32 = LR[d]['speed'] / real[b64]['inrun'], LR[d]['speed32'] / real[b32]['inrun32']
                out.append(json.dumps({'id': d, 'idle': real[b64]['idle'] * f64 * noisy(rnd), 'idle32': real[b32]['idle32'] * f32 * noisy(rnd),
                                       'inrun': LR[d]['speed'], 'inrun32': LR[d]['speed32'],
                                       'loaded': real[b64]['loaded'] * f64 * noisy(rnd), 'loaded32': real[b32]['loaded32'] * f32 * noisy(rnd)}))
        else:
            out.append(l.replace('results/followup-seed91.md', LIST).replace('(38 designs)', '(%d designs)' % len(ids)))
    open(path, 'w').write('\n'.join(out))


def remote(path, tag, w):
    o = json.load(open(path))
    real = {r['id']: r for r in o['designs'] if not r.get('rejected') and r['id'] in LR}
    rej = [r for r in o['designs'] if r.get('rejected')]
    key = 'speed32' if w == 4 else 'speed'
    # the record's own in-run figure is the line's width's: carry it, so near() reads like with like
    for b in real: real[b]['_inrun'] = LR[b][key]
    new = []
    for d in ids:
        if d in real: r = dict(real[d]); r.pop('_inrun'); new.append(r); continue
        rnd = random.Random('%s %s' % (tag, d))
        b = min(real, key=lambda b: abs(math.log(LR[d][key] / real[b]['_inrun'])))
        f = LR[d][key] / real[b]['_inrun']
        r = {k: v for k, v in real[b].items() if k != '_inrun'}
        r.update(id=d, speed=LR[d][key], total=LR[d]['total'], speed_here=real[b]['speed_here'] * f * noisy(rnd),
                 ratios={k: v * f * noisy(rnd) for k, v in real[b]['ratios'].items()})
        new.append(r)
    o['designs'] = new + rej
    json.dump(o, open(path, 'w'))


T = tempfile.mkdtemp(prefix='rehearse-'); C = os.path.join(T, os.path.basename(SRC))
shutil.copytree(SRC, C)
for t in sorted(glob.glob(os.path.join(C, 'packs', '*.tar.gz'))):
    x = tempfile.mkdtemp(dir=T)
    with tarfile.open(t) as z: z.extractall(x)
    for f in glob.glob(os.path.join(x, '**', 'loadtest.md'), recursive=True): loadtest(f, os.path.basename(t))
    with tarfile.open(t, 'w:gz') as z:
        for n in sorted(os.listdir(x)): z.add(os.path.join(x, n), arcname=n)
    shutil.rmtree(x)
for h in sorted(glob.glob(os.path.join(C, 'remote', '*', ''))):
    w = 4 if ('32' in h or 'arm' in h) else 8
    for f in glob.glob(os.path.join(h, 'out*.json')): remote(f, f, w)
    dj = os.path.join(h, 'designs.json')
    if os.path.exists(dj):
        old = json.load(open(dj)); rej = [r for r in old if r.get('rejected')]
        json.dump([{'id': d, 'genome': LR[d]['genome'], 'expressed': E.express(E.canon(LR[d]['genome'])), 'rejected': False,
                    'speed': LR[d]['speed32' if w == 4 else 'speed'], 'total': LR[d]['total']} for d in ids] + rej, open(dj, 'w'))
with tarfile.open(OUT, 'w:gz') as z: z.add(C, arcname=os.path.basename(SRC))
shutil.rmtree(T)
print('%s: %d designs a session, %d packs, %d remote lines' % (OUT, len(ids), len(glob.glob(SRC + '/packs/*.tar.gz')),
                                                              len(glob.glob(SRC + '/remote/*/'))))
