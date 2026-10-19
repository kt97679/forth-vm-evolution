# results/rehearsal-405.md - the after-seed-62 batch's rehearsal (Iteration 405); run in a scratch clone with the batch applied.
# Iteration 405: the after-seed-62 batch rehearsed - seed 59's front designs with the batch's genes on (or as they were,
# where the batch changes their engines), each evaluated as a run does: evolve.evaluate at both widths, one round.
import json, os, sys
tree = sys.argv[1]; os.chdir(tree); sys.argv = ['x']; sys.path.insert(0, os.path.join(tree, 'lab/evolve')); import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths()
F = [json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed59.md') if l.startswith('{"bin"')]
ex = lambda g: E.express(E.canon(g))
jit = [r for r in F if ex(r['genome']).get('jit')][:4]
tosbf = [r for r in F if ex(r['genome']).get('bfind') and ex(r['genome']).get('tos')][:3]
dead32 = [r for r in F if r.get('why32')][:3]
plain = [r for r in F if not ex(r['genome']).get('jit') and ex(r['genome']).get('tos')][:3]
cases = [('JIT +jithelp,jitre,jitret ' + r['id'], dict(r['genome'], jithelp=1, jitre=1, jitret=1), 'jithelp,jitre,jitret') for r in jit]
cases += [('bfind on tos, as is ' + r['id'], r['genome'], 'bfind,tos') for r in tosbf]
cases += [('dead at 32 in 59, as is ' + r['id'], r['genome'], 'bfind') for r in dead32]
cases += [(n + ' ' + r['id'], dict(r['genome'], **gs), k) for r, (n, gs, k) in zip(plain, [('+tail, GCC', dict(tail=1), 'tail'), ('+tail, clang', dict(tail=1, compiler=1), 'tail,compiler'), ('+tail, clang, tailpn', dict(tail=1, compiler=1, tailpn=1), 'tail,tailpn')])]
for name, g, want in cases:
    g = E.canon(g); e = E.express(g); miss = [k for k in want.split(',') if not e.get(k)]
    try: rec = E.evaluate(g, 1)
    except Exception as x: rec = {'status': 'EXCEPTION ' + str(x)[:150]}
    sp, s32 = rec.get('speed'), rec.get('speed32')
    print('%-36s not expressed: %-8s %s speed %s, 32-bit %s%s' % (name, ','.join(miss) or '-', rec.get('status'), sp and round(sp, 3), s32 and round(s32, 3), (' - ' + str(rec['why32'])[:120]) if rec.get('why32') else ''), flush=True)
