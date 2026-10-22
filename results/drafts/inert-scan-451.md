# Genes switched on but doing nothing - the first scan (Iteration 451)

The owner asked for it after two such genes were found by accident: rtloopall without its eight loop words (Iteration
439) and rtiplus without the run-time fuser (446). results/drafts/inert-scan-451.py on seed 65's front: four designs -
the fastest, the fastest without the JIT, the best by Q, the smallest - and for every gene each expresses (not frozen,
not structural), the design rebuilt with it off. **bytes** is off minus on (binary + image); each workload column the
dispatch counts' change, the profiler's, deterministic (minus: the gene saves dispatches); **inert**: neither bytes nor
any of kernel, loop and fib moved; **no run-time effect**: the bytes moved, no dispatch count did - right for a compiler
flag or a JIT gene (native code, which dispatch counts cannot see), a question for an interpreter mechanism.


## the fastest - d918d61002 (speed 0.115, 42,332 bytes, tag 2; JIT True)

| gene | bytes | kernel | loop | fib | verdict |
|---|---|---|---|---|---|
| tos | -12258 | -77.00% | -253563.05% | -580633.60% | works |
| varslot | -496 | -0.00% | -0.00% | -0.00% | no run-time effect |
| rtfuse | -320 | +0.87% | -1.29% | -0.58% | works |
| escape | -5208 | -373.04% | -1369567.18% | -375.50% | works |
| rtloop | -456 | +2.48% | -1318479.49% | +5.21% | works |
| kfast | -2064 | -192.70% | -220.72% | -231.90% | works |
| tfind | +0 | -0.00% | -0.00% | -0.00% | inert |
| kinput | -1704 | -93.41% | -109.67% | -100.47% | works |
| klookup | -1280 | -47.06% | -49.23% | -45.50% | works |
| swapi | +0 | -0.00% | -0.00% | -0.00% | inert |
| tag2 | -12259 | -93.91% | -253578.30% | -645163.03% | works |
| t2hot | +0 | -0.09% | -0.42% | +0.12% | works |
| jit | -12370 | -77.00% | -253563.05% | -580633.60% | works |
| hotinl | -40 | -5.26% | -6.26% | -6.04% | works |
| opbody | +120 | +5.76% | -0.00% | -0.00% | works |
| t2wide | +944 | -8.76% | -5.86% | -6.12% | works |
| jitx | -1184 | -78.04% | -0.00% | -0.00% | works |
| opcall | -32 | -0.28% | -0.23% | -0.38% | works |
| jitloop | +0 | -0.00% | -0.00% | -0.00% | inert |
| jitinl | -592 | -0.00% | -0.00% | -0.00% | no run-time effect |
| jittail | -1008 | -0.00% | -0.00% | -0.00% | no run-time effect |
| knumber | -520 | -0.58% | -3.55% | -3.40% | works |
| jitk | -3464 | -0.00% | -0.00% | -0.00% | no run-time effect |
| threads | -240 | -0.03% | +6.84% | +6.01% | works |
| dskew | +0 | -0.00% | -0.00% | -0.00% | inert |

## the fastest without the JIT - ab16f60a0c (speed 0.304, 31,887 bytes, plain; JIT False)

| gene | bytes | kernel | loop | fib | verdict |
|---|---|---|---|---|---|
| tos | +0 | -0.00% | -0.00% | -0.00% | inert |
| guard | -160 | -0.00% | -0.00% | -0.00% | no run-time effect |
| rtfuse | -352 | +0.64% | +0.00% | +0.00% | works |
| rtloop | -160 | +1.03% | -399.83% | +0.00% | works |
| rtloopall | +224 | -1.26% | -0.00% | -0.00% | works |
| kfast | -4616 | -187.51% | -0.18% | -0.07% | works |
| kinput | -4616 | -177.36% | -0.17% | -0.06% | works |
| klookup | -2888 | -123.57% | -0.13% | -0.05% | works |
| opbody | +136 | -0.05% | -0.00% | -0.00% | works |
| alignfn | +0 | -0.00% | -0.00% | -0.00% | inert |
| noinls | +2656 | -0.00% | -0.00% | -0.00% | no run-time effect |
| abortif | -80 | -0.37% | -0.00% | -0.00% | works |
| opinline | +0 | -0.04% | -0.00% | -0.00% | inert |
| knumber | -1120 | -0.36% | -0.00% | -0.00% | works |
| lto | +800 | -0.00% | -0.00% | -0.00% | no run-time effect |
| gotodup | +0 | -0.00% | -0.00% | -0.00% | inert |
| threads | +177 | +0.08% | -0.00% | -0.00% | works |
| fsys | +2249 | -0.00% | +0.00% | +0.00% | no run-time effect |
| regpin | +5952 | -0.00% | -0.00% | -0.00% | no run-time effect |

## the best by Q - 8fb19cc40d (speed 0.139, 28,877 bytes, tag 2; JIT True)

| gene | bytes | kernel | loop | fib | verdict |
|---|---|---|---|---|---|
| tos | -8587 | -86.44% | -252954.64% | -715838.82% | works |
| varslot | -352 | -0.00% | -0.00% | -0.00% | no run-time effect |
| guard | +736 | -0.00% | -0.00% | -0.00% | no run-time effect |
| escape | -870 | -153.18% | -1366004.59% | -143.83% | works |
| rtloop | -153 | -3.25% | -1365797.20% | +1.63% | works |
| rtloopall | +309 | -2.70% | -3.15% | -3.99% | works |
| kfast | -1072 | -392.31% | -375.85% | -393.10% | works |
| tfind | +576 | -0.00% | -0.00% | -0.00% | no run-time effect |
| kinput | -840 | -231.55% | -204.03% | -188.69% | works |
| klookup | -456 | -49.90% | -48.38% | -45.04% | works |
| tag2 | -8067 | -98.48% | -252962.83% | -715847.13% | works |
| t2hot | +0 | +0.17% | -0.40% | -0.53% | works |
| jit | -9291 | -86.44% | -252954.64% | -715838.82% | works |
| hotinl | -48 | -5.68% | -7.71% | -7.50% | works |
| opbody | +136 | +3.17% | -0.00% | -0.00% | works |
| t2wide | +79 | -8.25% | -4.48% | -4.97% | works |
| jitx | -880 | -87.39% | -0.00% | -0.00% | works |
| alignfn | +0 | -0.00% | -0.00% | -0.00% | inert |
| noinls | +0 | -0.00% | -0.00% | -0.00% | inert |
| jitloop | +0 | -0.00% | -0.00% | -0.00% | inert |
| jitinl | -456 | -1.91% | -0.00% | -0.00% | works |
| jittail | -160 | -0.00% | -0.00% | -0.00% | no run-time effect |
| opinline | -8 | -0.91% | -0.00% | -0.00% | works |
| bfind | +896 | -0.00% | -0.00% | -0.00% | no run-time effect |
| factor | +53 | +0.14% | +0.48% | +0.46% | works |
| jitk | -2656 | -0.00% | -0.00% | -0.00% | no run-time effect |
| lto | +64 | -0.00% | -0.00% | -0.00% | no run-time effect |
| fsys | +505 | +0.05% | +0.63% | +0.60% | works |

## the smallest - 9403761024 (speed 1.713, 13,959 bytes, plain; JIT False)

| gene | bytes | kernel | loop | fib | verdict |
|---|---|---|---|---|---|
| hotcalls | +319 | +0.04% | -0.00% | -0.00% | no run-time effect |
| fbuf | +0 | -0.00% | -0.00% | -0.00% | inert |
| threads | +144 | +8.43% | +0.01% | +0.01% | works |
| fsys | +1501 | +18.51% | +0.03% | +0.05% | works |


## What it found

1. **jitloop is inert in both JIT designs** - not a byte, not a dispatch. Its engine flag, -DJITLOOP, is read nowhere in
   the engine any more (engine/jit.c and vm-lab.c: no JITLOOP); its converter part (tools/layout.py, --jitloop: SPN's
   (+LOOP) and (?DO) stencils) changed nothing in these images. It rides on every JIT design - 93 of seed 65's front,
   jitx's constant companion - so it gathers keep votes and could never become a candidate. **The gene votes cannot see
   an inert gene that hitchhikes on good designs; this scan can.**
2. **Inert in one design or two**: tfind, swapi and dskew in the fastest; alignfn, gotodup and opinline in the plain
   fastest (GCC); alignfn and noinls in the best by Q (GCC); fbuf in the smallest. A compiler flag that moves no byte
   changed nothing the compiler made there (alignfn: function alignment already where it asks; gotodup's limit not
   reached); dskew and fbuf move data, so a memory or cache effect is not excluded.
3. **tos inert in the plain fastest** (ab16f60a0c) - unexpected: tos chooses the cached engine's source
   (vm-lab-tos.c). To be looked at; in the JIT designs it is the JIT's prerequisite and works.
4. **No run-time effect, as expected**: compiler flags (noinls, lto, regpin), the JIT's own genes (jitinl, jittail, jitk
   - native code), guard, varslot, fsys (the file words, which these workloads do not use), hotcalls (bytes).

## Proposed (the owner's call)

- **jitloop**: confirmed on more JIT designs, then frozen off as the votes' candidates are - reversible, its code kept.
- **tos in plain designs**: a closer look - why the plain fastest builds the same either way.
- **The scan beside the votes**: run on four designs at each seed's processing (about ten minutes); a gene inert in
  every scanned design carrying it, two runs running, joins the votes' candidates - the same reversible freeze.
