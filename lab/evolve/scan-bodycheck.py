#!/usr/bin/env python3
"""scan-bodycheck.py [--db FILE] [--old] - which designs lose a word silently.

A format-10 or tiny word becomes an opcode only where its compiled body
is exactly the definition the engine implements (tools/sod16.py,
ops10_at and tiny_at). Until Iteration 13 the check read the bodies after
the pairs, short branches and fused tests had rewritten them, so a design
carrying one of those lost the word - the converter printed a line, the
design lived without the opcode, and nothing read the line. Every living
CV8 design in the database is converted (no engine is compiled or run) and
the converter's report read. --old: as the converter was
(SOD16_OLD_BODYCHECK=1). Since Iteration 13 the evolver kills a design the
check fails (build()), so a regression cannot be silent again.
"""
import collections, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; db = os.path.join(HERE, '..', '..', 'build', 'evolve', 'db.jsonl')
if '--db' in args: i = args.index('--db'); db = args[i + 1]; del args[i:i + 2]
old = '--old' in args
if [a for a in args if a != '--old']: sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
real_sh, OUT = E.sh, {}
def sh(cmd, **kw):                      # the converter runs; the engine's generators and compiler do not
    c = [str(x) for x in cmd]
    if len(c) > 1 and c[1].endswith(os.path.join('tools', 'layout.py')):
        r = real_sh(cmd, **kw); OUT['s'] = r.stdout.decode(errors='replace'); return r
    if c[0] == 'cc' or (len(c) > 1 and os.path.basename(c[1]).startswith('gen-')):
        return subprocess.CompletedProcess(c, 0, b'', b'')
    return real_sh(cmd, **kw)
E.sh = sh
if old: os.environ['SOD16_OLD_BODYCHECK'] = '1'
recs = {}
for l in open(db):
    try: r = json.loads(l); recs[r['id']] = r
    except ValueError: pass
alive = [r for r in recs.values() if r['status'] == 'ok' and E.canon(r['genome'])['enc'] == 'cv8']
lost, n = collections.Counter(), 0
for r in alive:
    OUT['s'] = ''
    try: E.build(dict(E.canon(r['genome']), tail=0, msc=0), os.path.join(E.EV, 'scan'))
    except RuntimeError as e:
        if 'no exact body match' not in str(e): print('%s: %s' % (r['id'], e)); continue
        # the death names only the first line; the converter's whole report is in OUT
    miss = [k + ':' + x.strip().strip('\'"') for k, xs in re.findall(r'(ops10|tiny): no exact body match for \[([^]]*)\]', OUT['s'])
            for x in xs.split(',')]
    if miss: n += 1; lost.update(miss); print(r['id'], ' '.join(miss))
print('%d living CV8 designs, %d lost at least one word%s: %s' % (len(alive), n, ' (the old check)' if old else '',
      ', '.join('%s %d' % kv for kv in lost.most_common()) or 'none'))
