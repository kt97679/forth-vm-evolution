import re, json, os, sys
T = ['/mnt/transcripts/2026-10-12-18-50-21-forth-vm-evolution-seed43-44.txt', '/mnt/transcripts/2026-10-13-03-42-11-forth-vm-evolution-seed46-work.txt']
TX = [open(t, encoding='utf-8', errors='replace').read() for t in T]
names = sys.argv[1].split(',')
commit = re.compile(r'git commit -q (?:--amend )?-m \\"Iteration (\d+)')
out = {}
for nm in names:
    hit = None
    for ti, tx in enumerate(TX):
        i = tx.find('/tmp/' + nm)
        if i >= 0: hit = (ti, i); break
    if not hit: out[nm] = None; continue
    ti, i = hit; tx = TX[ti]
    m = commit.search(tx, i)
    it = m.group(1) if m else '?'
    # the tool call's description nearest before the first mention
    d = tx.rfind('"description": "', 0, i)
    desc = tx[d + 16:tx.find('"', d + 16)][:170] if d >= 0 and i - d < 20000 else ''
    # the first tool output after the mention
    r = tx.find('"type": "tool_result"', i)
    o = ''
    if r >= 0:
        s = tx.find('"stdout\\":\\"', r)
        if s >= 0 and s - r < 4000: o = tx[s + 12:s + 12 + 220].replace('\\\\n', ' / ').replace('\\n', ' / ')
    out[nm] = dict(tr=ti + 1, it=it, desc=desc, out=o)
json.dump(out, open('/tmp/pk2-attr.json', 'w'), ensure_ascii=False, indent=0)
for nm in names:
    v = out[nm]
    print('%-16s %s' % (nm, 'NOT IN THE TRANSCRIPTS' if not v else 'T%d it %s | %s | %s' % (v['tr'], v['it'], v['desc'][:110], v['out'][:120])))
