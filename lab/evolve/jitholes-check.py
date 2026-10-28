#!/usr/bin/env python3
"""jitholes-check.py - a JIT design whose stencil holds a value hole twice computes right (Iteration 557). Seed 76's
d11c9a6300: -ftracer with -fno-crossjumping leaves st_execute with two copies of EXECUTE's helper hole; jit.c patched one,
and the corpus came out wrong (results/drafts/corpus-deaths-555.md). Builds it, runs the corpus, compares the output
with s6's; exit 1 if it differs. As the build user, in a built tree (run-tests runs it)."""
import os, shutil, sys
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
G = {'tos': 1, 'scale': 0, 'bytehdr': 1, 'spec': ['var', 'tiny', 'small', 'imm'], 'sharedcall': 0, 'doesfar': 1, 'varcall': 1, 'varslot': 1, 'd256': 0, 'guard': 0, 'folds': ['+', '=', '!', '@', 'LSHIFT', 'RSHIFT', 'C@', 'C!', 'AND', 'OR', 'XOR', 'LIT', '<', 'U<', 'OVER', 'DROP', 'DUP', 'SWAP', 'ROT', '>R', 'R>', 'R@', 'NEGATE'], 'skippad': 0, 'fold': 1, 'supers': [['DUP', '>R'], ['C!', 'R>'], ['>R', 'C!'], ['ROT', 'DUP'], ['R@', 'ROT'], ['DUP', 'C@'], ['>R', 'OVER'], ['OVER', 'C@'], ['C@', '='], ['C@', 'DUP'], ['SWAP', 'R>'], ['LSHIFT', 'OVER'], ['OVER', 'R>'], ['ROT', 'ROT'], ['C@', 'SWAP'], ['C@', 'OR'], ['SWAP', 'DUP'], ['R>', 'SWAP'], ['OVER', 'R@'], ['C@', '>R'], ['DUP', '@'], ['+', 'R>'], ['R>', '='], ['C@', 'OVER']], 'rtfuse': 0, 'ops10': ['(DO)', '(LOOP)', '(+LOOP)', '(?DO)', '(LEAVE)', 'I', 'J', 'UNLOOP'], 'escape': 1, 'tail': 0, 'msc': 0, 'opt': 'O2', 'nogcse': 0, 'nocrossjump': 1, 'nocet': 1, 'align1': 0, 'noreorder': 0, 'peel': 0, 'ipaclone': 1, 'tracer': 1, 'enc': 'cv8', 'lean': 1, 'tag2': 1, 'jit': 1, 'jitx': 1, 'jitloop': 1, 'jitinl': 1, 'thinhdr': 1, 'bss': 1, 'kstack': 0, 'tailpn': 0, 'alignhot': 0, 'threads': 0, 'fsys': 2, 'regpin': 3, 'dskew': 0, 'hotcalls': 0, 'rtimm': 2, 'rtloop': 1, 'rtloopall': 1, 'kfast': 1, 'tfind': 0, 'kinput': 1, 'klookup': 1, 'rtiplus': 0, 'swapi': 0, 't2hot': 0, 'hotinl': 20, 'opbody': 0, 't2wide': 0, 'rtempty': 1, 'alignfn': 0, 'noinls': 1, 'fbuf': 0, 'abortif': 1, 'opcall': [], 'sysc': 0, 'jitos': 1, 'jittail': 1, 'jitk': 2, 'lto': 0, 'gotodup': 0, 'compiler': 0, 'jitmul': 1, 'jitdoes': 1, 'jitexec': 1, 'jitcfa': 1, 'jitrp': 1, 'jitfuse': 0, 'opinline': 0, 'knumber': 0, 'jitret': 0, 'jitvar': 0, 'jitimg': 1, 'bfind': 0, 'factor': 3}
E.setup()
d = os.path.join(E.EV, 'jitholes-check'); shutil.rmtree(d, ignore_errors=True)
E.run_metric(*E.REF, 'corpus'); s6 = E.OUT_LAST[0]
eng, img = E.build(E.canon(G), d); E.run_metric(eng, img, E.private_work(d), 'corpus'); got = E.OUT_LAST[0]
shutil.rmtree(d, ignore_errors=True)
print('jitholes-check: d11c9a6300 (tracer with nocrossjump: st_execute holds EXECUTE\'s helper hole twice) - the corpus %s'
      % ('as s6' if got == s6 else 'DIFFERS from s6'))
sys.exit(0 if got == s6 else 1)
