import json, collections, sys
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
R = {}
for l in open('/tmp/s46/pack/db.jsonl'):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
nc = [r for r in R.values() if r['status'] == 'died: engine did not compile']
ok = [r for r in R.values() if r['status'] == 'ok']
def ex(r): return E.express(E.canon(r['genome']))
print('tail among compile deaths:', dict(collections.Counter(str(ex(r).get('tail')) for r in nc)), '| among alive:', dict(collections.Counter(str(ex(r).get('tail')) for r in ok)))
ta = [r for r in ok if ex(r).get('tail')]
print('alive with tail: %d; their tos: %s, msc: %s' % (len(ta), dict(collections.Counter(str(ex(r).get('tos')) for r in ta)), dict(collections.Counter(str(ex(r).get('msc')) for r in ta))))
print('deaths: msc %s; tag2 %s' % (dict(collections.Counter(str(ex(r).get('msc')) for r in nc)), dict(collections.Counter(str(ex(r).get('tag2')) for r in nc))))
# in seed 45's db? same failure then?
