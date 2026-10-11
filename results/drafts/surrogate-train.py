import json, sys, importlib.util, pickle
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor
sys.argv = ['x']; spec = importlib.util.spec_from_file_location('E', '/tmp/fe/r/lab/evolve/evolve.py'); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
R = []
for l in open('/tmp/s40/run/pack/db.jsonl'):
    try: R.append(json.loads(l))
    except ValueError: pass
ok = [r for r in R if r['status'] == 'ok' and r.get('total') and r.get('speed')]
def feats(g):
    f = {}
    for k, v in E.express(g).items():
        if isinstance(v, (list, tuple)):
            for x in v: f['%s:%s' % (k, json.dumps(x))] = 1
        else: f['%s=%s' % (k, json.dumps(v))] = 1
    return f
CUT = 68
tr = [r for r in ok if r.get('gen', 0) <= CUT]; te = [r for r in ok if r.get('gen', 0) > CUT]
dv = DictVectorizer(); Xtr = dv.fit_transform([feats(r['genome']) for r in tr]); Xte = dv.transform([feats(r['genome']) for r in te])
out = {}
for obj in ('speed', 'total'):
    m = RandomForestRegressor(n_estimators=30, max_features=0.3, min_samples_leaf=3, n_jobs=1, random_state=1).fit(Xtr, np.log([r[obj] for r in tr]))
    p = m.predict(Xte); err = np.abs(np.exp(p - np.log([r[obj] for r in te])) - 1)
    print('%-5s: median error %.2f%%, 90%% within %.1f%%' % (obj, 100 * np.median(err), 100 * np.quantile(err, .9)), flush=True)
    out[obj] = dict(zip([r['id'] for r in te], np.exp(p).tolist()))
RR = {r['id']: r for r in ok}
final = set(E.first_front(list(RR), RR))
pickle.dump({'pred': out, 'final': final}, open('/tmp/fe/sur2.pkl', 'wb'))
print('final front: %d designs; predictions saved' % len(final))
