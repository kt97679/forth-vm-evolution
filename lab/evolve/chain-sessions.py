#!/usr/bin/env python3
"""lab/evolve/chain-sessions.py UNPACKED DEST [CANDIDATES.md] - a returned final-pick chain's readings laid out by session for
final-pick.py --also-session (Iteration 595; HANDOFF.md's processing of chains C and D: "each session a directory").
UNPACKED: process-seed.sh's OUT - the laptop's packs (*-loadtest-*/pack/loadtest.md, one a repeat of the step, in their
order) and chain-*/remote/HOST-HOW/ (out.json the first session, out-sK.json the K-th - remote-checks.sh --sessions, 591;
the reports chain-*/remote/HOST-HOW[-sK].md). One session: DEST flat, as results/chainB-seed86/ (loadtest.md,
HOST-HOW.out.json, HOST-HOW.md) - the form kept in the repository. More: DEST/sK, K from 1 - the K-th laptop pack and each
line's K-th session, whichever there are (a directory without loadtest.md adds hosts only: final-pick.py reads it so).
Prints each source's sessions and the final-pick.py line, with --also-session for every results/chain*-seed86/ kept
beside it when CANDIDATES.md is given; and msc's verdict (retire-plan-583.md): each of the 4 Tegra pairs' msc=0 design
as fast as its msc=1 one or faster on every ARMv7 line, each speed the geometric mean of its sessions."""
import glob, json, math, os, re, shutil, sys
PAIRS = [('6d321be1cc', '9920e9af07'), ('01efebca24', '97a4e37ab4'), ('c67e6b5336', '8bddf3a5e4'), ('629b7e96ec', '75acca89a6')]   # (msc=1, msc=0)


def sessions(h):
    """A remote line's out files in session order."""
    o = [os.path.join(h, 'out.json')] if os.path.exists(os.path.join(h, 'out.json')) else []
    k = sorted(glob.glob(os.path.join(h, 'out-s*.json')), key=lambda f: int(re.search(r'-s(\d+)\.json$', f).group(1)))
    return o + k


def main(a):
    if len(a) < 2: sys.exit(__doc__)
    up, dest = a[0], a[1]; cand = a[2] if len(a) > 2 else None
    packs = sorted(glob.glob(os.path.join(up, '*-loadtest-*', 'pack', 'loadtest.md')))
    ch = sorted(glob.glob(os.path.join(up, 'chain-*')))
    lines = {}
    if ch:
        for h in sorted(glob.glob(os.path.join(ch[0], 'remote', '*', ''))):
            s = sessions(h)
            if s: lines[os.path.basename(h.rstrip('/'))] = s
    n = max([len(packs)] + [len(s) for s in lines.values()]) if packs or lines else 0
    if not n: sys.exit('chain-sessions: no loadtest pack and no remote out file in %s' % up)
    os.makedirs(dest, exist_ok=True)
    dirs = [dest] if n == 1 else [os.path.join(dest, 's%d' % k) for k in range(1, n + 1)]
    for k, d in enumerate(dirs):
        os.makedirs(d, exist_ok=True)
        if k < len(packs): shutil.copy(packs[k], os.path.join(d, 'loadtest.md'))
        for hn, s in lines.items():
            if k < len(s):
                shutil.copy(s[k], os.path.join(d, hn + '.out.json'))
                rep = os.path.join(ch[0], 'remote', hn + ('.md' if k == 0 else '-s%d.md' % (k + 1)))
                if os.path.exists(rep): shutil.copy(rep, os.path.join(d, hn + '.md'))
    print('chain-sessions: %d session(s) -> %s; the laptop %d, %s' % (n, dest, len(packs),
          ', '.join('%s %d' % (hn, len(s)) for hn, s in lines.items()) or 'no remote line'))
    if cand:
        kept = []                                       # 598: a kept chain of several sessions (results/chainD-seed86/sK) - each
        for d in sorted(glob.glob('results/chain*-seed86')):
            if os.path.abspath(d) == os.path.abspath(dest): continue
            kept += sorted(glob.glob(os.path.join(d, 's[0-9]*')), key=lambda p: int(re.search(r's(\d+)$', p).group(1))) or [d]
        first = dirs[0]
        print('final-pick: python3 lab/evolve/final-pick.py %s %s %s%s' % (cand, os.path.join(first, 'loadtest.md'),
              ' '.join(sorted(glob.glob(os.path.join(first, '*.out.json')))),
              ''.join(' --also-session ' + d for d in dirs[1:] + kept)))
    arm = {}
    for hn, s in lines.items():
        for f in s:
            o = json.load(open(f))
            if not str(o.get('env', {}).get('machine', '')).startswith(('arm', 'aarch')): break
            for x in o.get('designs', []):
                if x.get('speed_here'): arm.setdefault(hn, {}).setdefault(x['id'], []).append(x['speed_here'])
    if arm:
        gm = lambda v: math.exp(sum(math.log(t) for t in v) / len(v))
        ok = True
        for hn, d in arm.items():
            for one, zero in PAIRS:
                if one in d and zero in d:
                    a1, a0 = gm(d[one]), gm(d[zero]); ok &= a0 <= a1
                    print('msc %s: %s (msc=1) %.4f, %s (msc=0) %.4f over %d/%d sessions - msc=0 %s' % (
                        hn, one, a1, zero, a0, len(d[one]), len(d[zero]), 'as fast or faster' if a0 <= a1 else '%.1f%% SLOWER' % ((a0 / a1 - 1) * 100)))
                else: ok = False; print('msc %s: the pair %s / %s not both measured - no verdict from it' % (hn, one, zero))
        print('msc verdict (retire-plan-583.md): %s' % ('RETIRE - every pair\'s msc=0 design as fast or faster' if ok else 'KEEP'))


if __name__ == '__main__': main(sys.argv[1:])
