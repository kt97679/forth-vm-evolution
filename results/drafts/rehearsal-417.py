# Iteration 417: the final batch rehearsed on plain CV8 - the test programs on s6 at both widths; seed 58's front
# (plain CV8) sampled, each evaluated as a run does at both widths and its image against master's build.
import contextlib, json, os, shutil, sys
tree = sys.argv[1]; os.chdir(tree); sys.argv = ['x']; sys.path.insert(0, os.path.join(tree, 'lab/evolve')); import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths()
P = json.load(open('/tmp/tr/progs.json')); S6 = dict(E.HUMAN['s6-cv8b'])
for name, g, w in [('s6', S6, 8), ('s6 at 4-byte cells', dict(S6, jit=0), 4)]:
    d = os.path.join(E.EV, 'rh'); shutil.rmtree(d, ignore_errors=True); res = []
    with (E.at_width(E.WIDTH4) if w == 4 else contextlib.nullcontext()):
        eng, img = E.build(E.canon(g), d); pw = E.private_work(d)
        for k, (prog, want) in P.items():
            r = E.sh([eng, img], cwd=pw, inp=prog.encode(), timeout=120, cpu=60)
            got = [l.strip() for l in (r.stdout or b'').decode(errors='replace').replace('\r', '').splitlines() if l.strip() not in ('', 'OK')]
            res.append('%s %s' % (k, 'ok' if want in got else 'WRONG ' + ' / '.join(got[-2:])[:40]))
    print('%-20s %s' % (name, '; '.join(res)), flush=True)
F = [json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed58.md') if l.startswith('{"')]
F = [r for r in F if not E.express(E.canon(r['genome'])).get('tag2')]
F.sort(key=lambda r: r.get('total') or 0); pick = F[::max(1, len(F) // 8)][:8]
for r in pick:
    g = E.canon(r['genome'])
    try: rec = E.evaluate(g, 1)
    except Exception as x: rec = {'status': 'EXCEPTION ' + str(x)[:100]}
    print('58 %s total %s: %s speed %s, 32-bit %s%s' % (r['id'], r.get('total'), rec.get('status'), rec.get('speed') and round(rec['speed'], 3),
          rec.get('speed32') and round(rec['speed32'], 3), (' - ' + str(rec['why32'])[:80]) if rec.get('why32') else ''), flush=True)
