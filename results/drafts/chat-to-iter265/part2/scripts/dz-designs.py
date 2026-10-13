import os, sys, subprocess, re
sys.argv = ['x']; sys.path.insert(0, '/tmp/b44s/lab/evolve'); import evolve as E
E.setup()
PROG = (": T1 1 0 / ; ' T1 CATCH . : T2 7 0 MOD ; ' T2 CATCH . : T3 7 0 /MOD ; ' T3 CATCH . : T4 1 2 0 */ ; ' T4 CATCH . "
        ": T5 1 2 0 */MOD ; ' T5 CATCH . : T6 7 0 0 FM/MOD ; ' T6 CATCH . : T7 7 0 0 SM/REM ; ' T7 CATCH . : T8 7 0 0 UM/MOD ; ' T8 CATCH . CR\n"
        "1 0 / S\" lost\" TYPE\nS\" after\" TYPE CR 7 2 / . 7 2 MOD . -7 2 / . CR BYE\n").encode()
for did, extra in (('f20de05a64', {}), ('4a351e360a', {}), ('cc6d168e0a', {}), ('add5ec8937', {}), ('add5ec8937', {'fsys': 5}), ('fc09f6373d', {})):
    g = E.canon(dict(E.recorded_genome(did), **extra)); d = os.path.join(E.EV, 'dzd'); eng, img = E.build(g, d)
    r = subprocess.run([eng, img], cwd=E.private_work(d), input=PROG, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
    o = r.stdout.decode(errors='replace').replace('\r', '')
    ok = o.count('-10 ') == 8 and 'Division by zero' in o and 'after' in o and 'lost' not in o and '3 1 -4 ' in o
    print('%s%s (msc %s tail %s jit %s tos %s): %s, status %d' % (did, ' fsys 5' if extra else '', g.get('msc', 0), g.get('tail', 0), g.get('jit', 0), g['tos'], 'RIGHT' if ok else 'WRONG: %r' % o[-160:], r.returncode), flush=True)
