# Genes switched on but doing nothing - the first scan (Iteration 451)

The owner asked for it after two such genes were found by accident: rtloopall without its eight loop words (Iteration
439) and rtiplus without the run-time fuser (446). results/drafts/inert-scan-451.py on seed 65's front: four designs -
the fastest, the fastest without the JIT, the best by Q, the smallest - and for every gene each expresses (not frozen,
not structural), the design rebuilt with it off. **bytes** is off minus on (binary + image); each workload column the
dispatch counts' change, the profiler's, deterministic (minus: the gene saves dispatches). **Corrected at Iteration 452**:
the first pass (below its table, superseded) used only kernel, loop and fib, and called a gene inert when the bytes did not
move - two false findings. Now all seven workloads (the six of the selection and sieve), and **inert only when the build
is the same** - engine and image hashed; a gene that builds differently with no dispatch effect is a compiler flag's or a
data layout's, for timing to judge.

## The corrected scan (Iteration 452)


## the fastest - d918d61002 (speed 0.115, 42,332 bytes, tag 2; JIT True)

| gene | bytes | kernel | fib | corpus | loop | bubble | ackermann | sieve | verdict |
|---|---|---|---|---|---|---|---|---|---|
| tos | -12258 | -77.00% | -580633.60% | -0.54% | -253563.05% | -5679.91% | -81345.88% | -95526.04% | works |
| varslot | -496 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| rtfuse | -320 | +0.87% | -0.58% | -0.36% | -1.29% | +0.02% | +0.65% | +4.03% | works |
| escape | -5208 | -373.04% | -375.50% | -645.66% | -1369567.18% | -23627.61% | -303.21% | -207200.46% | works |
| rtloop | -456 | +2.48% | +5.21% | -14.80% | -1318479.49% | -20993.37% | +4.10% | -147710.75% | works |
| kfast | -2064 | -192.70% | -231.90% | -466.28% | -220.72% | -46.01% | -172.36% | -214.61% | works |
| tfind | +0 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| kinput | -1704 | -93.41% | -100.47% | -159.73% | -109.67% | -17.55% | -82.85% | -93.17% | works |
| klookup | -1280 | -47.06% | -45.50% | -93.49% | -49.23% | -8.08% | -34.67% | -45.76% | works |
| swapi | +0 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| tag2 | -12259 | -93.91% | -645163.03% | -17.00% | -253578.30% | -7051.08% | -91109.40% | -101893.17% | works |
| t2hot | +0 | -0.09% | +0.12% | -1.09% | -0.42% | -2.31% | +0.27% | +1.10% | works |
| jit | -12370 | -77.00% | -580633.60% | -0.54% | -253563.05% | -5679.91% | -81345.88% | -95526.04% | works |
| hotinl | -40 | -5.26% | -6.04% | -7.17% | -6.26% | -1.09% | -5.01% | -5.27% | works |
| opbody | +120 | +5.76% | -0.00% | +0.31% | -0.00% | -7.85% | -0.00% | -0.00% | works |
| t2wide | +944 | -8.76% | -6.12% | -7.62% | -5.86% | -14.82% | -8.36% | -5.62% | works |
| jitx | -1184 | -78.04% | -0.00% | -1.32% | -0.00% | -5672.61% | -81347.10% | -95527.34% | works |
| opcall | -32 | -0.28% | -0.38% | -0.23% | -0.23% | -0.14% | -0.32% | -0.66% | works |
| jitloop | +0 | -0.00% | -0.00% | -1.03% | -0.00% | -5672.58% | -0.00% | -0.00% | works |
| jitinl | -592 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -81347.10% | -0.00% | works |
| jittail | -1008 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| knumber | -520 | -0.58% | -3.40% | -15.69% | -3.55% | -0.32% | -1.49% | -3.65% | works |
| jitk | -3464 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| threads | -240 | -0.03% | +6.01% | +0.09% | +6.84% | +0.49% | +3.60% | +4.06% | works |
| dskew | +0 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |

## the fastest without the JIT - ab16f60a0c (speed 0.304, 31,887 bytes, plain; JIT False)

| gene | bytes | kernel | fib | corpus | loop | bubble | ackermann | sieve | verdict |
|---|---|---|---|---|---|---|---|---|---|
| tos | +0 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| guard | -160 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| rtfuse | -352 | +0.64% | +0.00% | +0.95% | +0.00% | +0.01% | -3.35% | +0.01% | works |
| rtloop | -160 | +1.03% | +0.00% | -9.98% | -399.83% | -363.59% | +0.00% | -63.48% | works |
| rtloopall | +224 | -1.26% | -0.00% | -1.79% | -0.00% | -0.04% | -0.00% | -0.01% | works |
| kfast | -4616 | -187.51% | -0.07% | -768.19% | -0.18% | -1.79% | -0.38% | -23.44% | works |
| kinput | -4616 | -177.36% | -0.06% | -735.70% | -0.17% | -1.72% | -0.36% | -23.42% | works |
| klookup | -2888 | -123.57% | -0.05% | -658.66% | -0.13% | -1.38% | -0.27% | -0.35% | works |
| opbody | +136 | -0.05% | -0.00% | -0.02% | -0.00% | -107.69% | -0.00% | -0.00% | works |
| alignfn | +0 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | **inert - the same build** |
| noinls | +2656 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| abortif | -80 | -0.37% | -0.00% | -4.35% | -0.00% | -0.01% | -0.00% | -0.00% | works |
| opinline | +0 | -0.04% | -0.00% | -0.02% | -0.00% | -30.77% | -0.00% | -0.00% | works |
| knumber | -1120 | -0.36% | -0.00% | -15.04% | -0.00% | -0.01% | -0.00% | -0.01% | works |
| lto | +800 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| gotodup | +0 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | **inert - the same build** |
| threads | +177 | +0.08% | -0.00% | -0.08% | -0.00% | -0.01% | -0.00% | -0.00% | works |
| fsys | +2249 | -0.00% | +0.00% | +0.01% | +0.00% | +0.00% | +0.00% | +0.00% | built differently, no dispatch effect |
| regpin | +5952 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |

## the best by Q - 8fb19cc40d (speed 0.139, 28,877 bytes, tag 2; JIT True)

| gene | bytes | kernel | fib | corpus | loop | bubble | ackermann | sieve | verdict |
|---|---|---|---|---|---|---|---|---|---|
| tos | -8587 | -86.44% | -715838.82% | -1.58% | -252954.64% | -6467.06% | -80598.38% | -116739.23% | works |
| varslot | -352 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| guard | +736 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| escape | -870 | -153.18% | -143.83% | -136.26% | -1366004.59% | -20359.32% | -126.42% | -221581.97% | works |
| rtloop | -153 | -3.25% | +1.63% | -16.06% | -1365797.20% | -20331.21% | -0.54% | -173370.84% | works |
| rtloopall | +309 | -2.70% | -3.99% | -2.13% | -3.15% | -1.35% | -3.41% | -8.19% | works |
| kfast | -1072 | -392.31% | -393.10% | -752.67% | -375.85% | -65.77% | -315.51% | -430.10% | works |
| tfind | +576 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| kinput | -840 | -231.55% | -188.69% | -223.42% | -204.03% | -30.68% | -172.39% | -192.54% | works |
| klookup | -456 | -49.90% | -45.04% | -71.92% | -48.38% | -7.23% | -36.70% | -48.88% | works |
| tag2 | -8067 | -98.48% | -715847.13% | -11.88% | -252962.83% | -7655.77% | -87376.26% | -116749.41% | works |
| t2hot | +0 | +0.17% | -0.53% | -1.44% | -0.40% | -2.53% | -2.18% | -1.24% | works |
| jit | -9291 | -86.44% | -715838.82% | -1.58% | -252954.64% | -6467.06% | -80598.38% | -116739.23% | works |
| hotinl | -48 | -5.68% | -7.50% | -7.79% | -7.71% | -1.11% | -6.37% | -6.85% | works |
| opbody | +136 | +3.17% | -0.00% | +0.20% | -0.00% | -0.00% | -0.00% | -0.00% | works |
| t2wide | +79 | -8.25% | -4.97% | -6.53% | -4.48% | -6.12% | -9.64% | -6.69% | works |
| jitx | -880 | -87.39% | -0.00% | -1.29% | -0.00% | -6460.50% | -80599.09% | -116740.03% | works |
| alignfn | +0 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | **inert - the same build** |
| noinls | +0 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| jitloop | +0 | -0.00% | -0.00% | -1.05% | -0.00% | -6460.47% | -0.00% | -0.00% | works |
| jitinl | -456 | -1.91% | -0.00% | -0.00% | -0.00% | -0.00% | -80599.09% | -0.00% | works |
| jittail | -160 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| opinline | -8 | -0.91% | -0.00% | -0.07% | -0.00% | -0.00% | -0.00% | -0.15% | works |
| bfind | +896 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| factor | +53 | +0.14% | +0.46% | +0.22% | +0.48% | +0.09% | +0.32% | +0.51% | works |
| jitk | -2656 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| lto | +64 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | built differently, no dispatch effect |
| fsys | +505 | +0.05% | +0.60% | +0.02% | +0.63% | +0.05% | +0.52% | +0.61% | works |

## the smallest - 9403761024 (speed 1.713, 13,959 bytes, plain; JIT False)

| gene | bytes | kernel | fib | corpus | loop | bubble | ackermann | sieve | verdict |
|---|---|---|---|---|---|---|---|---|---|
| hotcalls | +319 | +0.04% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | +0.00% | built differently, no dispatch effect |
| fbuf | +0 | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | -0.00% | **inert - the same build** |
| threads | +144 | +8.43% | +0.01% | +25.19% | +0.01% | +0.07% | +0.07% | +0.06% | works |
| fsys | +1501 | +18.51% | +0.05% | +7.78% | +0.03% | +0.15% | +0.27% | +0.12% | works |


## What it found (Iteration 452)

1. **No gene inert across designs.** Inert - the same build with it off - only in one design or two: **alignfn** (the plain
   fastest and the best by Q: function alignment already where it asks), **gotodup** (the plain fastest: GCC's limit not
   reached), **fbuf** (the smallest: its buffer size not compiled in there). Harmless hitchhikers, each working elsewhere
   or not, but costing nothing.
2. **jitloop works** - the first pass's headline was wrong: with it off, bubble's dispatches rise 57 to 65 times in both JIT
   designs, corpus's about 1% - it gives the JIT (+LOOP) and (?DO), which kernel, loop and fib do not use. Its
   engine flag (-DJITLOOP) is indeed read nowhere; its converter stencils are the gene.
3. **tos works in the plain fastest** - built differently (another engine, 22,600 bytes either way: equal sizes, not an
   unchanged build), no dispatch effect: TOS caching changes how each operation runs, not how many run - timing's.
4. Built differently with no dispatch effect, for timing to judge: varslot, tfind, swapi, dskew, guard, noinls, lto,
   regpin, fsys, hotcalls, and the JIT's own jitinl, jittail, jitk (native code).

## Proposed (the owner's call)

- **Nothing to freeze** from this scan: jitloop's proposal withdrawn.
- **The scan beside the votes**, in its corrected form, at each seed's processing (four designs, about twenty minutes): a
  gene the same build with it off in every scanned design carrying it, two runs running, joins the votes' candidates.
- The dead flag: -DJITLOOP, set by the build and read by no code - a line to remove in the next cleanup.

## The first pass (Iteration 451), superseded

Its finding - jitloop inert in both JIT designs, tos inert in the plain fastest - came from three workloads that use
neither (+LOOP) nor (?DO), and from equal sizes taken for an unchanged build.
