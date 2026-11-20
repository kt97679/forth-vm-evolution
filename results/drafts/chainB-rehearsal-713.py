#!/usr/bin/env python3
"""results/drafts/chainB-rehearsal-713.py CHAIN_A_TGZ LIST LEAN WORK OUT_TGZ - a stand-in for chain B's archive, made from
chain A's (Iteration 713): its laptop and remote readings cut to LIST's designs (results/followup-seed96-roles-b.md; a
design chain A lacks - 219878ec89 - given 21768033b7's readings under its id), its measure-ids pack replaced by chain B's
five (the first every design of LIST, the four more LEAN's, their memory moved -4 / +4 / +8 / 0 KB so the median is
known: the first read + 0), and a pool-sizes pack naming one made-up design. For results/drafts/chainB-rehearsal-713.sh:
process-followup.sh 96-roles-b on it, before the real archive comes - the path chain B's processing takes."""
import glob, json, os, shutil, subprocess, sys, tarfile

src, lst, lean, work, out = sys.argv[1:6]
ids = [json.loads(l) for l in open(lst) if l.startswith('{"')]
L = {r['id']: r for r in ids}
LEAN = [json.loads(l) for l in open(lean) if l.startswith('{"')]
STANDIN = {'219878ec89': '21768033b7'}
shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
with tarfile.open(src) as t: t.extractall(work, filter='data')
H = glob.glob(os.path.join(work, 'chain-*'))[0]
nr = [l for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve', 'NEXT-RUN'))
      if l.strip() and not l.startswith('#')][0]
open(os.path.join(H, 'line'), 'w').write(nr)
def keep_lines(path, key='id'):
    out = []
    for l in open(path):
        if not l.startswith('{"'): out.append(l); continue
        r = json.loads(l)
        if r.get(key) in L: out.append(l)
        for new, old in STANDIN.items():
            if r.get(key) == old and new not in L: pass
            elif r.get(key) == old: out.append(json.dumps(dict(r, **{key: new})) + '\n')
    open(path, 'w').write(''.join(out))
P = os.path.join(H, 'packs')
for t in sorted(glob.glob(os.path.join(P, '*.tar.gz'))):
    if '-measure-ids-' in t: os.remove(t); continue
    d = t[:-7]; os.makedirs(d)
    with tarfile.open(t) as x: x.extractall(d, filter='data')
    keep_lines(os.path.join(d, 'pack', 'loadtest.md'))
    with tarfile.open(t, 'w:gz') as x: x.add(os.path.join(d, 'pack'), 'pack')
    shutil.rmtree(d)
for f in glob.glob(os.path.join(H, 'remote', '*', 'out*.json')):
    j = json.load(open(f)); D = []
    for x in j['designs']:
        if x.get('id') in L or x.get('rejected'): D.append(x)
        for new, old in STANDIN.items():
            if x.get('id') == old and new in L: D.append(dict(x, id=new))
    j['designs'] = D; json.dump(j, open(f, 'w'))
def pack(name, files):
    d = os.path.join(work, 'p'); shutil.rmtree(d, ignore_errors=True); os.makedirs(os.path.join(d, 'pack'))
    for n, s in files.items(): open(os.path.join(d, 'pack', n), 'w').write(s)
    with tarfile.open(os.path.join(P, name + '.tar.gz'), 'w:gz') as x: x.add(os.path.join(d, 'pack'), 'pack')
    shutil.rmtree(d)
rec = lambda r, dm: json.dumps(dict(r, status='ok', rss=r['rss'] + dm, mem={k: v + dm for k, v in r.get('mem', {}).items()},
                                    src='measure-ids.py'), sort_keys=True) + '\n'
pack('forth-vm-evolution-measure-ids-rehearse-fury-20261120-200000',
     {'measure-ids.md': '# measure-ids.py (a stand-in)\n\n' + ''.join(rec(r, 0) for r in ids)})
for k, dm in enumerate((-4, 4, 8, 0)):
    pack('forth-vm-evolution-measure-ids-rehearse-fury-20261120-20%02d00' % (10 + k),
         {'measure-ids.md': '# measure-ids.py (a stand-in, lean)\n\n' + ''.join(rec(r, dm) for r in LEAN)})
fake = dict(ids[0], id='0000000000', total=21600, why='pool-sizes.py: 21600 B after the batch, below the list\'s 21673')
pack('forth-vm-evolution-pool-sizes-rehearse-fury-20261120-203000',
     {'pool-sizes.md': '# pool-sizes.py --list followup-seed96-roles-b.md: a stand-in\n\n- 0000000000 JIT-free: 22300 -> 21600 B, '
      'below the list\'s 21673\nJIT-free: 900 of 1200 built in the time, up to 22650 B before the batch\nJIT: 40 of 40 built in '
      'the time, up to 34290 B before the batch\nbuilt in 2400 s; 0 failed; 1 below the list\'s smallest\n\n' + json.dumps(fake) + '\n'})
subprocess.run(['tar', 'czf', os.path.abspath(out), os.path.basename(H)], cwd=work, check=True)
print('chainB-rehearsal-713: %s - %d designs, %d lean, the laptop %d loadtest packs' % (out, len(L), len(LEAN),
      len(glob.glob(os.path.join(P, '*-loadtest-*')))))
