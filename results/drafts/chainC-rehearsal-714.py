#!/usr/bin/env python3
"""results/drafts/chainC-rehearsal-714.py CHAIN_B_TGZ LIST ARMLIST LISTB WORK OUT_TGZ - a stand-in for chain C's archive,
made from chain B's (Iteration 714, while chain C runs): its laptop and remote readings cut to LIST's designs
(results/followup-seed96-roles-c.md; the Tegra's to ARMLIST's, -c-arm.md), each design chain B did not measure (in LIST,
not in LISTB) given a stand-in's readings under its id - 219878ec89's for a JIT-free one, c6f1c1331b's for a JIT one -,
its five measure-ids packs replaced by chain C's one (every design of LIST, its record's memory as it is), and its
pool-sizes pack by chain C's: --below-jit 36805, one made-up JIT design. For results/drafts/chainC-rehearsal-714.sh:
process-followup.sh 96-roles-c on it, before the real archive comes - the path chain C's processing takes."""
import glob, json, os, shutil, subprocess, sys, tarfile

src, lst, armlst, lstb, work, out = sys.argv[1:7]
ids = [json.loads(l) for l in open(lst) if l.startswith('{"')]
L = {r['id']: r for r in ids}
ARM = {json.loads(l)['id'] for l in open(armlst) if l.startswith('{"')}
B = {json.loads(l)['id'] for l in open(lstb) if l.startswith('{"')}
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve')); sys.argv = ['x']
import evolve as E
STANDIN = {i: ('c6f1c1331b' if E.express(E.canon(L[i]['genome'])).get('jit') else '219878ec89') for i in L if i not in B}
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
            if r.get(key) == old: out.append(json.dumps(dict(r, **{key: new})) + '\n')
    open(path, 'w').write(''.join(out))
P = os.path.join(H, 'packs')
for t in sorted(glob.glob(os.path.join(P, '*.tar.gz'))):
    if '-measure-ids-' in t or '-pool-sizes-' in t: os.remove(t); continue      # chain C's stand-ins below
    if '-loadtest-' not in t: continue
    d = t[:-7]; os.makedirs(d)
    with tarfile.open(t) as x: x.extractall(d, filter='data')
    keep_lines(os.path.join(d, 'pack', 'loadtest.md'))
    with tarfile.open(t, 'w:gz') as x: x.add(os.path.join(d, 'pack'), 'pack')
    shutil.rmtree(d)
for f in glob.glob(os.path.join(H, 'remote', '*', 'out*.json')):
    j = json.load(open(f)); D = []; K = ARM if 'prebuiltarm' in f else set(L)
    for x in j['designs']:
        if x.get('id') in K or x.get('rejected'): D.append(x)
        for new, old in STANDIN.items():
            if x.get('id') == old and new in K: D.append(dict(x, id=new))
    j['designs'] = D; json.dump(j, open(f, 'w'))
def pack(name, files):
    d = os.path.join(work, 'p'); shutil.rmtree(d, ignore_errors=True); os.makedirs(os.path.join(d, 'pack'))
    for n, s in files.items(): open(os.path.join(d, 'pack', n), 'w').write(s)
    with tarfile.open(os.path.join(P, name + '.tar.gz'), 'w:gz') as x: x.add(os.path.join(d, 'pack'), 'pack')
    shutil.rmtree(d)
rec = lambda r, dm: json.dumps(dict(r, status='ok', rss=r['rss'] + dm, mem={k: v + dm for k, v in r.get('mem', {}).items()},
                                    src='measure-ids.py'), sort_keys=True) + '\n'
pack('forth-vm-evolution-measure-ids-rehearse-fury-20261121-150000',
     {'measure-ids.md': '# measure-ids.py (a stand-in)\n\n' + ''.join(rec(r, 0) for r in ids)})
jit1 = [r for r in ids if E.express(E.canon(r['genome'])).get('jit')][0]
fake = dict(jit1, id='0000000000', total=36000, why='pool-sizes.py: 36000 B after the batch, below 36805')
pack('forth-vm-evolution-pool-sizes-rehearse-fury-20261121-153000',
     {'pool-sizes.md': '# pool-sizes.py --list followup-seed96-roles-c.md: a stand-in\n\n- 0000000000 JIT: 36700 -> 36000 B, '
      'below 36805\nJIT-free: 0 of 0 built in the time\nJIT: 300 of 381 built in the time, up to 38900 B before the batch\n'
      'built in 2400 s; 0 failed; 1 below the threshold\n\n' + json.dumps(fake) + '\n'})
subprocess.run(['tar', 'czf', os.path.abspath(out), os.path.basename(H)], cwd=work, check=True)
print('chainC-rehearsal-714: %s - %d designs, %d stand-ins, the Tegra %d, the laptop %d loadtest packs' % (out, len(L),
      len(STANDIN), len(ARM), len(glob.glob(os.path.join(P, '*-loadtest-*')))))
