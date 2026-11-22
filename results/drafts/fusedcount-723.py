#!/usr/bin/env python3
"""results/drafts/fusedcount-723.py [NAME ...] - the fused branches' dispatches, translator-built against self-built
(Iteration 723, after results/drafts/selfhost-variants-723.sh: their sizes alone cannot show it - an operation more in
the ops10 gene moves the tag-2 map, and with it bytes elsewhere). For each variant (default pfv-nq, pfv-short): its
export's engine with -DPROFILE=1 (build/selfhost-ids/out/NAME/Makefile's forth-libc), run on the export's image (the
translator's, T) and on the cross compiler's (build/selfhost/check-NAME/A.img) over the kernel and corpus workloads; the
dispatches of each fused branch the variant has, by its one-byte code (genes.4's G-T2-ONE; VMPROF's pair lines count by
code), and the outputs compared. 8-byte cells. Run from the top as the build user, after selfhost-variants-723.sh."""
import os, re, subprocess, sys
ROOT = os.getcwd(); HERE = os.path.join(ROOT, 'lab', 'evolve')
names = sys.argv[1:] or ['pfv-nq', 'pfv-short']
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E
E.setup()
OPS = ['=I?BRANCH', '=I?BRANCH8', 'DUP?NBRANCH', 'DUP?NBRANCH8', '?NBRANCH']
bad = 0
for n in names:
    X = os.path.join(ROOT, 'build', 'selfhost-ids', 'out', n)
    g = open(os.path.join(X, 'genes.4')).read()
    lst = lambda k: ' '.join(re.findall(r'^S" (.*) " G\+$', g.split('G-LIST: ' + k, 1)[1].split('G-LIST:', 1)[0], re.M)).split()
    t = lst('G-OPS10'); o10 = dict(zip(t[0::2], map(int, t[1::2])))
    t = list(map(int, lst('G-T2-ONE'))); l2c = dict(zip(t[0::2], t[1::2]))
    mk = open(os.path.join(X, 'Makefile')).read()
    cmd = re.search(r'^forth-libc: .*\n\t(.*)$', mk, re.M).group(1)
    cc = re.search(r'^CC\s*=\s*(\S+)', mk, re.M).group(1)
    eng = os.path.join(X, 'forth-prof')
    subprocess.run(cmd.replace('$(CC)', cc).replace('-o forth-libc', '-DPROFILE=1 -o forth-prof'), shell=True, cwd=X, check=True)
    imgs = {'T': os.path.join(X, 'image.img'), 'A': os.path.join(ROOT, 'build', 'selfhost', 'check-' + n, 'A.img')}
    work = E.private_work(os.path.join(ROOT, 'build', 'selfhost-ids', 'work-' + n))
    have = [o for o in OPS if o in o10]
    print('%s - %s' % (n, ', '.join('%s L%d code %s' % (o, o10[o], l2c.get(o10[o], 'escaped')) for o in have)))
    for w in ('kernel', 'corpus'):
        res = {}
        for k, img in imgs.items():
            f = os.path.join(X, 'vmprof.txt')
            if os.path.exists(f): os.remove(f)
            p = subprocess.run([eng, img], cwd=work, input=E.program(w), capture_output=True, timeout=600, env=dict(os.environ, VMPROF=f))
            cnt = {}
            for l in open(f):
                s = l.split()
                if len(s) == 3 and s[0].isdigit(): cnt[int(s[1])] = cnt.get(int(s[1]), 0) + int(s[2])
            res[k] = (p.stdout, {o: cnt.get(l2c.get(o10[o], -1), 0) for o in have}, sum(cnt.values()))
        same = res['T'][0] == res['A'][0]; bad += not same
        print('  %-6s output %s; dispatches T %s A %s' % (w, 'same' if same else 'DIFFERS', '{:,}'.format(res['T'][2]), '{:,}'.format(res['A'][2])))
        for o in have:
            print('    %-13s T %10s   A %10s' % (o, '{:,}'.format(res['T'][1][o]), '{:,}'.format(res['A'][1][o])))
print('fusedcount: %s' % ('FAIL - an output differs' if bad else 'the outputs the same'))
