import re, json, sys
T = ['/mnt/transcripts/2026-10-12-18-50-21-forth-vm-evolution-seed43-44.txt', '/mnt/transcripts/2026-10-13-03-42-11-forth-vm-evolution-seed46-work.txt']
TX = [open(t, encoding='utf-8', errors='replace').read() for t in T]
commit = re.compile(r'git commit -q (?:--amend )?-m \\"Iteration (\d+)')
tu = re.compile(r'"type": "tool_use",')
def blocks(tx):
    """(start, end, description, input text) of each tool_use block"""
    out = []
    for m in tu.finditer(tx):
        e = tx.find('"type": "tool_result"', m.end())
        seg = tx[m.start():e if e > 0 else m.start() + 20000]
        d = re.search(r'"description": "((?:[^"\\]|\\.)*)"', seg)
        out.append((m.start(), e, d.group(1) if d else '', seg))
    return out
B = [blocks(tx) for tx in TX]
def result(tx, e):
    if e < 0: return ''
    s = tx.find('"text": "', e)
    return tx[s + 9:s + 9 + 240].replace('\\n', ' / ') if s > 0 and s - e < 3000 else ''
names = sys.argv[1].split(',')
res = {}
for nm in names:
    pat = re.compile(r'(?<![\w.-])' + re.escape(nm) + r'(?![\w-])')
    found = None
    for ti in range(2):
        for (s, e, d, seg) in B[ti]:
            if pat.search(seg):
                runs = re.search(r'(python3|sh|bash|runuser -u claude -- python3) +(\S*/)?' + re.escape(nm), seg)
                if found is None: found = [ti, s, e, d, seg, None]
                if runs and found[5] is None: found[5] = (s, e, d)
        if found: break
    if not found: res[nm] = None; continue
    ti, s, e, d, seg, run = found
    m = commit.search(TX[ti], s)
    r = run or (s, e, d)
    res[nm] = dict(tr=ti + 1, it=m.group(1) if m else '?', made=d[:150], ran=r[2][:150], out=result(TX[ti], r[1]))
json.dump(res, open('/tmp/pk2-attr2.json', 'w'), ensure_ascii=False, indent=1)
for nm in names:
    v = res[nm]
    print('%-15s %s' % (nm, 'NOT IN THE TRANSCRIPTS' if not v else 'T%d it %s\n    made: %s\n    ran:  %s\n    out:  %s' % (v['tr'], v['it'], v['made'], v['ran'], v['out'][:200])))
