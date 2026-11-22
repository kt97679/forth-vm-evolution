# The new genes rehearsed together - jitdead, jitfew, hashk, chainorder, numfirst (Iteration 735)

Before the series' first seed (HANDOFF.md, 727: the reopened search's genes built and rehearsed in the sandbox first;
693's and 696's method). A scratch clone of master at 734 (the fixed data layout applied). The genes: jitdead (710,
mechanism 9's V1'), jitfew (713), hashk (729), chainorder (732), numfirst (733).

## The front, the genes off against on (results/drafts/rehearsal-735.py: evolve.evaluate, 3 rounds, both widths; two interleaved pairs each)

| role | genes on | statuses | speed on / off (64) | (32) | engine | image | the apps' code | total | memory KB (64) |
|---|---|---|---:|---:|---|---|---|---|---|
| best-all-round | jitdead, jitfew, hashk, chainorder, numfirst | ok / ok | 0.996 | 0.977 | 34,216 -> 34,888 | 10,332 -> 10,387 | 10,147 -> 9,458 | 54,695 -> 54,733 | 252 -> 186 |
| fastest-x86-32 | jitdead, jitfew, hashk, chainorder, numfirst | ok / ok | 1.049 | 0.989 | 30,516 -> 31,444 | 9,424 -> 9,527 | 9,985 -> 9,288 | 49,925 -> 50,259 | 226 -> 178 |
| fastest-x86-64 | jitdead, jitfew, hashk, chainorder, numfirst | ok / ok | 0.921 | 1.046 | 33,256 -> 33,944 | 10,152 -> 10,215 | 10,095 -> 9,398 | 53,503 -> 53,557 | 258 -> 186 |
| least-memory | hashk, chainorder, numfirst | ok / ok | 0.973 | 0.998 | 7,574 -> 7,766 | 9,566 -> 9,674 | 8,429 -> 8,424 | 25,569 -> 25,864 | 108 -> 108 |
| portable-arm | hashk, chainorder, numfirst | ok / ok | 1.003 | 0.995 | 26,790 -> 27,238 | 10,055 -> 10,164 | 8,429 -> 8,439 | 45,274 -> 45,841 | 120 -> 118 |
| portable-fastest | hashk, chainorder, numfirst | ok / ok | 0.997 | 0.987 | 16,336 -> 16,560 | 10,256 -> 10,423 | 8,947 -> 8,938 | 35,539 -> 35,921 | 124 -> 126 |
| portable-knee | hashk, chainorder, numfirst | ok / ok | 1.042 | 1.005 | 9,424 -> 9,568 | 9,105 -> 9,249 | 8,428 -> 8,412 | 26,957 -> 27,229 | 120 -> 116 |
| portable-small | hashk, chainorder, numfirst | ok / ok | 1.032 | 0.980 | 8,806 -> 8,966 | 9,135 -> 9,241 | 8,320 -> 8,304 | 26,261 -> 26,511 | 112 -> 112 |
| small-jit | jitdead, jitfew, hashk, chainorder, numfirst | ok / ok | 1.021 | 0.989 | 18,676 -> 19,428 | 8,321 -> 8,449 | 9,347 -> 8,654 | 36,344 -> 36,531 | 194 -> 164 |
| smallest | hashk, chainorder, numfirst | ok / ok | 0.933 | 0.975 | 4,246 -> 4,246 | 9,037 -> 9,191 | 8,390 -> 8,381 | 21,673 -> 21,818 | 104 -> 104 |

Every evaluation ok, on and off. The sandbox's time is noisier than the genes' effect (0.92-1.05, the two widths
disagreeing on one role) - the instructions below are the measure here, the laptop's run the time's. The sizes: the
engines +192 to +928 B (the JIT roles' most: jitdead's and jitfew's code), the images +55 to +167 B; jitdead takes the
JIT's header off every definition, so the JIT roles' application code is about 690 B less and their totals move
+38 to +334 B, the portable ones' +145 to +567 B. Memory: jitfew's arrays - the JIT roles 30-72 KB less (best-all-round
252 -> 186, fastest-x86-64 258 -> 186, small-jit 194 -> 164); the others level.

## Where the score moves - instructions, on / off (results/drafts/rehearsal-instr-735.py: cachegrind, 8-byte cells)

| role | kernel | fib | corpus | loop | bubble | ackermann | apps | sieve | parse | the selection (geomean) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| best-all-round | 1.011 | 1.000 | 0.985 | 1.000 | 1.001 | 1.000 | 0.997 | 1.000 | 0.962 | **0.999** |
| fastest-x86-32 | 1.013 | 1.000 | 0.983 | 1.000 | 1.000 | 1.000 | 0.997 | 1.000 | 0.965 | **0.999** |
| fastest-x86-64 | 1.012 | 1.000 | 0.989 | 1.000 | 1.001 | 1.000 | 0.997 | 1.000 | 0.968 | **1.000** |
| least-memory | 1.005 | 1.000 | 0.972 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.949 | **0.997** |
| portable-arm | 1.008 | 1.000 | 0.993 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.983 | **1.000** |
| portable-fastest | 1.010 | 1.000 | 0.933 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.838 | **0.991** |
| portable-knee | 1.000 | 1.000 | 0.896 | 1.000 | 1.000 | 1.000 | 0.999 | 1.000 | 0.812 | **0.984** |
| portable-small | 1.002 | 1.000 | 0.919 | 1.000 | 1.000 | 1.000 | 0.999 | 1.000 | 0.864 | **0.988** |
| small-jit | 1.038 | 1.000 | 0.969 | 1.000 | 1.001 | 1.001 | 1.020 | 1.000 | 0.891 | **1.004** |
| smallest | 0.969 | 1.000 | 0.710 | 1.000 | 0.998 | 0.999 | 0.976 | 0.999 | 0.457 | **0.944** |

The work done falls where the genes aim: the corpus 0.71-0.99 and parse (held out) 0.46-0.98 - numfirst's literals and
hashk's and chainorder's walks; the smallest, whose lookup is Forth, most (the selection 0.944). The programs (fib,
loop, bubble, ackermann, sieve) do not move - they look nothing up. The kernel workload pays a little: +0.5 to +1.3 %
on most (chainorder's front is the held-out programs' names, not the compiler's), small-jit +3.8 % and its apps +2.0 %
(jitfew: a word longer than 128 operations translated a second time - its memory 30 KB less). Each gene is the
search's to take or leave per design; none costs a design that does not express it a byte (each checked off: 727-733).

## The short run (--pop 8 --gens 2 --seed 735 --widths 8,4; 33 records)

22 alive; the deaths the founders' as at 693 and 696 (s1-sod16's apps, s2-cpt16's application size, s4's and s5's
retired genes - frozen stages), six stopped after one round, and **one new**: 395e2f44e9, a mutation hashk=1 on a design
of no other part - "image did not convert (hashk: --hashk, and no HASH8 in the dump)". The plain design's dump is
tools/build-stages.sh's k64-b.txt (cv8.4 and cv8b.4 alone), which has none of cv8-hashk.4, cv8-chainorder.4 or
cv8-numfirst.4 - every other dump the lab makes has them since 729-733, and every role has a part (so the genes'
checks never built from it). chainorder or numfirst on it would have died the same way. **Fixed** (results/
applied-plain-dump-735/): such a design with any of the three on takes a dump of its own (-bg, made by the lab with
their files); off, the old dump still - the lab's own plain dump was tried first and differs from build-stages' in
INCLUDE-BUFFER's leftover text (the last long line read), so not byte for byte. Checked (results/drafts/
plain-genes-735.py): off, the image and engine the same bytes as before at both widths; each gene and all three on,
the kernel, corpus, parse and apps outputs the same as off at both widths. Mutation reaches each gene about 1 % of the
time (696), so a seed of tens of thousands of designs tries each hundreds of times - this one would have killed them.

Found on the way, a method note: a scratch clone made by `cp -a` keeps build/work's absolute symlinks into the
tree it was copied from, and setup() copies the overlays through them - into master's forth/ (the same bytes here, so
only their times moved and master's build read stale). A copied clone has its stages built before use (which makes
its own links); `git clone` and build, as HANDOFF-REFERENCE.md's lesson 405 says, avoids it.
