import json, collections, sys
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
R = {}
for l in open('/tmp/s46/pack/db.jsonl'):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
nc = [r for r in R.values() if r['status'] == 'died: engine did not compile']
ok = [r for r in R.values() if r['status'] == 'ok']
def ex(r): return E.express(E.canon(r['genome']))
print('compile deaths:', len(nc))
for gname in ('jitos', 'jit', 'opt', 'jitinl', 'jitx', 'tos', 'lean', 'bss'):
    print('  %-6s died: %s | alive: %s' % (gname, dict(collections.Counter(str(ex(r).get(gname)) for r in nc)), dict(collections.Counter(str(ex(r).get(gname)) for r in ok).most_common(5))))
alive_jitos = [r for r in ok if ex(r).get('jitos')]
print('alive with jitos expressed:', len(alive_jitos))
print('first compile death:', nc[0]['id'] if nc else None, {k: v for k, v in sorted(ex(nc[0]).items()) if k.startswith('jit') or k == 'opt'} if nc else '')
print('first error text:', [k for k in nc[0].keys()][:20] if nc else '')
