# run each build on each workload, keep it waiting for input at the end, and read which pages are present (root: pagemap)
import json, os, re, struct, subprocess, time, collections
B = json.load(open('/tmp/pm/builds.json'))
def syms(eng):
    full = eng + '.full' if os.path.exists(eng + '.full') else eng
    out = []
    for l in subprocess.run(['nm', '-S', '-n', full], stdout=subprocess.PIPE, text=True).stdout.split('\n'):
        f = l.split()
        if len(f) == 4 and f[2] in 'bBdDtTrR': out.append((int(f[0], 16), int(f[1], 16), f[3], f[2]))
    return out
for did, b in B.items():
    S = syms(b['eng'])
    for w, prog in b['progs'].items():
        p = subprocess.Popen([b['eng'], b['img']], cwd=b['pw'], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.stdin.write(prog.encode()); p.stdin.flush()
        pid, last, still = None, -1, 0
        for _ in range(1200):                             # the engine, once its CPU time stops moving and it sleeps on input
            time.sleep(0.05)
            f = open('/proc/%d/stat' % p.pid).read().rsplit(')', 1)[1].split()
            cpu = int(f[11]) + int(f[12])
            still = still + 1 if (cpu == last and f[0] == 'S') else 0; last = cpu
            if still >= 10: pid = str(p.pid); break
        if not pid: print(did, w, 'never waited'); p.kill(); continue
        maps = [l.split() for l in open('/proc/%s/maps' % pid)]
        pm = open('/proc/%s/pagemap' % pid, 'rb')
        regions = collections.Counter(); bysym = collections.Counter(); total = 0
        for m in maps:
            lo, hi = (int(x, 16) for x in m[0].split('-')); name = m[5] if len(m) > 5 else '[anon]'
            for a in range(lo, hi, 4096):
                pm.seek((a // 4096) * 8); raw = pm.read(8)
                if len(raw) < 8: break
                v = struct.unpack('<Q', raw)[0]
                if v >> 63 & 1:
                    total += 1; regions[os.path.basename(name) if name.startswith('/') else name] += 1
                    hit = [s for s in S if s[0] < a + 4096 and s[0] + max(s[1], 1) > a]
                    big = max(hit, key=lambda s: s[1]) if hit else None
                    bysym[big[2] if big and big[1] >= 2048 else ('code' if hit and hit[0][3] in 'tT' else 'small data' if hit else name)] += 1
        p.stdin.close(); p.wait()
        print('%s %s: %d pages present (%d KB) - by mapping %s' % (did, w, total, total * 4, dict(regions)))
        print('   by symbol: %s' % ', '.join('%s %d' % kv for kv in bysym.most_common(12)))
