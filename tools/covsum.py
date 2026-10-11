"""Engine coverage (Iteration 160): gcov over a --coverage build - per binary the
lines run and the handlers (L_ labels, switch cases) no run reached. Usage:
covsum.py BUILD_DIR ROOT. The build: CC with --coverage, ENGINE_RT=libc."""
import os, re, subprocess, glob, json, collections, sys
B = sys.argv[1] if len(sys.argv) > 1 else '/tmp/fa/cov/build'; out = {}
ROOT = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(B.rstrip('/'))
for gcda in sorted(glob.glob(B + '/*.gcda')):
    tmp = '/tmp/fa/gcovtmp'; os.makedirs(tmp, exist_ok=True)
    r = subprocess.run(['gcov', '-t', '-o', os.path.dirname(gcda), gcda], cwd=ROOT, capture_output=True, text=True, errors='replace')
    src, lines, per = None, {}, {}
    for l in r.stdout.split('\n'):
        m = re.match(r'\s*([^:]+):\s*(\d+):(.*)$', l)
        if not m: continue
        c, n, text = m.group(1).strip(), int(m.group(2)), m.group(3)
        if n == 0:
            if text.startswith('Source:'): src = text[7:]; lines = per.setdefault(src, {})
            continue
        lines[n] = (c, text)
    mains = [k for k in per if k.endswith('.c') and not k.endswith('.h')]
    src = max(mains, key=lambda k: len(per[k])) if mains else src; lines = per.get(src, {})
    exe = [v for v in lines.values() if v[0] != '-']; run = [v for v in exe if v[0] not in ('#####', '=====')]
    labels = [(n, re.match(r'\s*(L_\w+):', t).group(1), c) for n, (c, t) in sorted(lines.items()) if re.match(r'\s*L_\w+:', t)]
    labels += [(n, 'case:' + re.match(r'\s*case\s+([\w ]+?)\s*:', t).group(1), c) for n, (c, t) in sorted(lines.items()) if re.match(r'\s*case\s+[\w ]+?\s*:', t)]
    out[os.path.basename(gcda)[:-5]] = {'src': src, 'exe': len(exe), 'run': len(run), 'labels': labels}
json.dump(out, open('/tmp/fa/cov-%s.json' % os.path.basename(os.path.dirname(B.rstrip('/'))), 'w'))
print('%-34s %-10s %6s %8s  %s' % ('binary', 'source', 'lines', 'run', 'handlers never run'))
never = collections.defaultdict(list); have = collections.defaultdict(list)
for k, v in out.items():
    nr = [lab for n, lab, c in v['labels'] if c in ('#####', '=====')]
    for n, lab, c in v['labels']:
        have[lab].append(k)
        if c in ('#####', '====='): never[lab].append(k)
    print('%-34s %-10s %6d %7.1f%%  %d of %d: %s' % (k, os.path.basename(v['src'] or '?'), v['exe'], 100.0 * v['run'] / max(1, v['exe']), len(nr), len(v['labels']), ' '.join(nr)[:150]))
everywhere = sorted(l for l in never if len(never[l]) == len(have[l]))
print('\nhandlers run by NO test in ANY binary that has them (%d): %s' % (len(everywhere), ' '.join(everywhere)))
