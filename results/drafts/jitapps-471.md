# What the JIT leaves on the applications - and why (Iteration 471)

The owner (470-471): the coverage study. Applications held out keep a quarter of the fast designs' lead or less
(results/drafts/appbench-468.md); lab/evolve/jitapps.py asks why. As jitleft.py does for the selection's workloads, the
design is built for the profiler twice - the JIT off, and on with -DJITLOG=1 - and each application run in both; the
dispatches the JIT left, then where they sit and why each refused word was refused, a callee's refusal followed to its
root. For it the analysis-only log (engine/jit.c, JITLOG builds only - production code unchanged) now tells "too long"
apart (why 6) and names the operation without stencils by jit_ops[]'s index (a fifth field).

## Seed 68's b9c5b4ae74 - 0.140 on the selection's workloads

| application | dispatches, JIT off | left by the JIT | left |
|---|---|---|---|
| sim16 | 2,573,988,784 | 1,261,076,321 | 49.0% |
| gc16 | 2,004,182,667 | 735,881,896 | 36.7% |
| scan | 1,927,686,824 | 1,789,188,064 | 92.8% |
| evo | 1,687,180,694 | 1,393,457,063 | 82.6% |
| fcp | 2,956,380,783 | 2,124,558,813 | 71.9% |
| brainless | 2,054,044,780 | 1,939,561,897 | 94.4% |
| cd16sim | 4,994,858,845 | 4,321,334,857 | 86.5% |

**On the applications the JIT leaves most of the work to the interpreter** - a third to nine tenths. The lead is lost
there, not in the JIT's code.

Why, by the left dispatches each cause carries (the rest - 22-61% - in words the JIT translated or never reached):

| cause | sim16 | gc16 | scan | evo | fcp | brainless | cd16sim |
|---|---|---|---|---|---|---|---|
| an operation without stencils, op 27 | - | 22.8% | 71.2% | 39.0% | - | 3.1% | - |
| an operation without stencils, op 70 | - | 22.1% | - | - | 25.1% | 30.1% | 28.7% |
| an operation without stencils, op 28 / 119 / 118 | - | - | 2.8% | - | 15.4% | 3.3% | - |
| the return stack's order | 58.9% | - | 1.8% | - | 30.3% | 13.3% | 13.6% |
| too long (JIT_MAXOPS) | - | - | - | - | 1.6% | - | 3.3% |

What the operations are, by a probe (tiny words, one primitive each, on the same logging build): `*`, `MOD`, `/`,
`/MOD`, `*/` and `CELLS` are refused through a callee - in this design they are colon words over primitives without
stencils, ops 27 and 28 at the root: by every sign the double-cell multiply and divide under them. op 70 and op 32 are
not yet named. And the return stack's order is EXECUTE's dispatch (sim16's STEP, cd16sim's DEFER and SJW:, the words
VALUE makes) - EXECUTE itself refused.

**One missing stencil sinks a whole word, and every caller after it** - the JIT is all or nothing per word. RANDOM's
`1103515245 *`, an array's `CELLS` (sim16's tables, gc16's heap, scan's DFA, evo's fitness), a `MOD` - and the hot
loops of real programs stay interpreted. Our six workloads never meet them, so the search was never paid to cover them.

## Proposed (the owner's calls)

1. **Stencils for the multiply and divide** under `*`, `CELLS`, `MOD`, `/` - or `*` and `CELLS` as primitives with
   stencils of their own (CELLS a shift).
2. **EXECUTE in native code**: a call through the token - native when the target is, the interpreter when not.
3. **Name ops 70 and 32** and give them stencils; **JIT_MAXOPS** raised or long words split.
4. Then jitapps.py again - and appbench.py's times - to see how much of the lead comes back.
