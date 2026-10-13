import json, re, glob, os
rows = []
for f in glob.glob('results/evolve-amd-ryzen-7-pro-8840hs-seed*.md'):
    seed = re.search(r'seed(\w+)\.md$', f).group(1)
    txt = open(f).read()
    head = txt.split('\n', 1)[0]
    it = re.findall(r'Iteration (\d+)', head)
    recs = []
    for l in txt.split('\n'):
        if l.startswith('{') and '"speed"' in l:
            try: r = json.loads(l)
            except ValueError: continue
            if isinstance(r, dict) and 'speed' in r: recs.append(r)
    keys = sorted(recs[0].keys()) if recs else []
    def tot(r):
        img = r.get('size', r.get('img'))
        return (r.get('bin') or 0) + (img or 0) if img is not None else None
    sp = [r['speed'] for r in recs if isinstance(r.get('speed'), (int, float))]
    tt = [tot(r) for r in recs if tot(r)]
    bn = [r['bin'] for r in recs if isinstance(r.get('bin'), (int, float))]
    rows.append((seed, it[0] if it else '?', len(recs), min(sp) if sp else None, min(tt) if tt else None, min(bn) if bn else None, ','.join(keys[:9])))
def sk(r):
    m = re.match(r'(\d+)(\w*)', r[0]); return (int(m.group(1)), m.group(2))
for r in sorted(rows, key=sk): print(r)
