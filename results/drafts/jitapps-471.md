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

## Iteration 472 - the operations named, and the first gene: jitmul

The owner: 1. a gene for the multiply and divide, 2. another for EXECUTE, 3. name and cover the rest, 4. measure again.
layout.py now lists, as comments in vm-jit-ops.h, every operation without stencils; for seed 68's fast design:
op 27 UM*, op 28 UM/MOD, op 32 SP@, op 70 DODOES (the run-time of every DOES> word - VALUE's among them), op 118 COUNT,
op 119 ALIGNED. The four largest causes: UM*, UM/MOD, DODOES and EXECUTE.

jitmul (built, tested, staged frozen off): UM* a stencil of its own - the machine's widening multiply, four
instructions - and COUNT from stencils there are (DUP 1+ SWAP C@). UM/MOD's stencil is written (one divide, the high
cell reduced first - the interpreter's result mod 2^64) but not mapped: the interpreter answers a zero divisor with
-10 THROW (Iteration 229), which a stencil cannot do yet. Found on the way: a first, bit-by-bit UM/MOD ran past the JIT's
160-byte scan window, its second exit not copied, and the corpus died of SIGILL - the hazard the pending stencil-check
reports; and a comment holding the Forth word star-slash closed itself early. s6 with the JIT and jitmul passes the
corpus and matches the interpreter on an arithmetic test (products, quotients, remainders of both signs, UM*, UM/MOD,
M*, star-slash, a division by zero). engines-check has the variant; jitapps.py takes --set=gene=value. jitmul is in
FROZEN (0): the search does not take it until the owner unfreezes it.

## Iteration 473 - jitdoes, and the first measure: scan's work 93% interpreted to 4%

jitdoes (built, tested, staged frozen off): a DOES> child - [DODOES][a 4-byte call of its DOES> code][pad][PFA] - is
translated as a literal of its PFA followed by its DOES> code from after the leading R> to its EXIT, so the return
stack is never touched and the code's own order holds; the converter gives the JIT DODOES's and R>'s one-byte codes
(JIT_DODOES, JIT_FROMR in vm-jit-ops.h). s6 with the JIT and jitdoes, and with jitmul too, passes the corpus and matches
the interpreter on a DOES> test (constants, arrays, values in hot loops). engines-check has the variant.

jitapps.py on seed 68's b9c5b4ae74 with --set=jitmul=1 --set=jitdoes=1 - the dispatches the JIT leaves, before and
after:

| application | before | jitmul and jitdoes |
|---|---|---|
| sim16 | 49.0% | 49.0% |
| gc16 | 36.7% | 32.6% |
| scan | 92.8% | **3.8%** |
| evo | 82.6% | 68.3% |
| fcp | 71.9% | 71.9% |
| brainless | 94.4% | 93.8% |
| cd16sim | 86.5% | 86.5% |

**UM\* native gives scan almost all of its work to the JIT** - its loops index tables with CELLS, and CELLS stood on
UM\*. evo and gc16 move less: their next blocker is UM/MOD (SM/REM, FM/MOD, /MOD under MOD and /) - the throw path. sim16
is EXECUTE's. **jitdoes moved nothing yet in fcp, brainless and cd16sim**: their op-70 refusals remain - the DOES>
children those programs make are reached as callees, not translated as words of their own (a child made by CREATE has
no JIT header, as a variable has none - the JIT handles a variable at its call, JIT_DOVAR), so the next step is the same
there: a DOES> child at its call - a literal of the PFA, then a native call of its DOES> code translated once and kept.

Next, in order of what they free: UM/MOD's throw path (evo, gc16, the Appbench programs' arithmetic), DOES> children at
their call (fcp, brainless, cd16sim), EXECUTE (sim16, cd16sim, fcp's evaluators).

## Iteration 473, later - children at their call; jitmul checked on all seven; jitdoes wrong on real programs

A DOES> child has no JIT header (as a variable has none): the JIT reaches it as a callee and translates it once by
jit_kslot, with the decode starting at the child itself - so jitdoes now takes the child at its own address too. The
dispatches the JIT leaves on seed 68's b9c5b4ae74 with both genes: **fcp 71.9% to 53.9%, brainless 93.8% to 57.2%,
cd16sim 86.5% to 65.9%** (gc16 32.6%, unchanged).

appbench.py now takes --ids (named designs) and --set gene=value, and checks every output. On b9c5b4ae74, one round,
time over s6's:

| genes | sim16 | gc16 | scan | evo | fcp | brainless | cd16sim |
|---|---|---|---|---|---|---|---|
| as it is | 0.642 | 0.485 | 0.687 | 0.589 | 0.953 | 1.013 | 1.062 |
| jitmul | - | - | - | - | 0.805 | 0.965 | 1.190 |
| jitmul and jitdoes | 0.632 | 0.586 | **0.150** | 0.478 | **wrong** | **wrong** | **wrong** |

**jitmul is right on all seven applications** (our four with both genes, Appbench's three with jitmul alone) - and
scan runs at 0.150 of s6, 4.6 times faster than before it. **jitdoes gives fcp, brainless and cd16sim wrong results**,
while the corpus and a DOES> test pass: a fault the small tests do not reach. It stays frozen, marked not to be
unfrozen until found. Suspects to rule out first: a child translated before DOES> patched it (a CREATE'd word used
between CREATE and DOES>, then cached by jit_kslot as a variable or a stale child); children made by DEFER, VALUE and
the programs' own defining words whose DOES> code returns through the return stack; the cache keyed by address when
MARKER or FORGET reuses the space.

## Iteration 474 - jitdoes's fault found and fixed; jitmul enabled; the applications twice s6's speed

**The fault**: a bisection over how many DOES> children jitdoes translates (a knob, since removed) - brainless went
wrong at the first. The JIT's return-stack check (jit_body, JITX) skipped calls by their code 0xFFFF and read the
operation table at every other code - and jitdoes's PFA literal is the first literal ever there at that stage (0xFFFD;
jitx's own literals, a variable's, come later). An out-of-bounds read: harmless garbage on s6, which is why the corpus
and the DOES> test passed there; a segmentation fault on seed 68's fast design, where even `5 KONST FIVE` printed
nothing. The check now skips 0xFFFD and above - calls and literals have no return-stack effect.

On seed 68's b9c5b4ae74, one round, time over s6's, **every output right**:

| genes | sim16 | gc16 | scan | evo | fcp | brainless | cd16sim | geometric mean |
|---|---|---|---|---|---|---|---|---|
| as it is | 0.642 | 0.485 | 0.687 | 0.589 | 0.953 | 1.013 | 1.062 | 0.747 |
| jitmul and jitdoes | 0.611 | 0.501 | **0.189** | 0.511 | **0.632** | **0.636** | **0.729** | **0.508** |

Appbench's three 31-37% faster, scan 3.6 times: on the applications the design goes from 1.3 to 2.0 times s6's speed.
On master: run-tests PASS (71 engine paths - the jitmul and jitdoes variants among them - each corpus right), validate 7
of 7 IDENTICAL, the jail PASS (alone). The pending 32-bit JIT batch still applies on top, all three patches in order.

**The owner: jitmul enabled** - out of FROZEN. **jitdoes stays frozen** until the owner says - now right on every test.

**UM/MOD's throw path, designed**: the interpreter's call into native code made through a small helper holding a
return point (__builtin_setjmp - the engine links no C library, as jit_interp already does); UM/MOD's stencil, on a zero
divisor, calls a helper through a function-address hole that longjmps there with the stack; the interpreter then does
what L_umdiv does - -10 where the divisor was, THROW. Then UM/MOD mapped: MOD and / native - evo's blocker. **jitexec**:
EXECUTE through the token - native when the target is, else the same interpreted call jitre built.
