# Hardware counters on the AMD Ryzen 7 PRO 8840HS - where the cycles go (Iteration 285)

lab/evolve/counters.py on the laptop (pack forth-vm-evolution-counters-f607d18fb-fury-20261014-051454):
user-space cycles, instructions, branches and branch misses, the median of 5 runs, for hand-made
s6 and the newest front's fastest design with the JIT (e141550b9a), fastest without it
(c9369657e4) and smallest (7535695a36), on the six selection workloads. Counted by perf 6.8.12
(/usr/lib/linux-tools/6.8.0-147-generic/perf) on the running kernel 6.17.0-1032-oem - the
kernel's own tools package has no perf binary where Ubuntu's wrapper looks (Iterations 283-284);
an older perf counts these events on a newer kernel. kernel.perf_event_paranoid was 2 only while
counters.py measured, 4 before and after (perf-hold.py).

| design | workload | cycles (M) | instructions per cycle | branch misses per 1k instructions | misses per branch |
|---|---|---|---|---|---|
| s6 | kernel | 32.3 | 2.41 | 0.68 | 0.31% |
| s6 | fib | 195.6 | 3.86 | 0.43 | 0.20% |
| s6 | corpus | 161.8 | 2.42 | 0.44 | 0.20% |
| s6 | loop | 344.3 | 3.29 | 0.01 | 0.01% |
| s6 | bubble | 145.6 | 2.75 | 0.19 | 0.08% |
| s6 | ackermann | 55.4 | 2.95 | 0.11 | 0.05% |
| e141550b9a | kernel | 9.5 | 2.21 | 3.69 | 2.01% |
| e141550b9a | fib | 43.2 | 4.43 | 0.06 | 0.04% |
| e141550b9a | corpus | 31.7 | 2.14 | 3.51 | 1.80% |
| e141550b9a | loop | 41.3 | 1.95 | 0.11 | 0.11% |
| e141550b9a | bubble | 11.6 | 4.66 | 0.30 | 0.28% |
| e141550b9a | ackermann | 15.7 | 3.38 | 2.51 | 1.50% |
| c9369657e4 | kernel | 16.9 | 1.44 | 9.09 | 5.46% |
| c9369657e4 | fib | 143.2 | 2.37 | 0.54 | 0.36% |
| c9369657e4 | corpus | 37.7 | 1.92 | 3.87 | 2.06% |
| c9369657e4 | loop | 47.4 | 2.87 | 0.06 | 0.03% |
| c9369657e4 | bubble | 46.7 | 2.18 | 0.40 | 0.30% |
| c9369657e4 | ackermann | 58.8 | 1.85 | 0.12 | 0.09% |
| 7535695a36 | kernel | 60.2 | 1.36 | 7.60 | 3.84% |
| 7535695a36 | fib | 194.0 | 2.95 | 0.21 | 0.11% |
| 7535695a36 | corpus | 372.9 | 1.45 | 3.90 | 1.88% |
| 7535695a36 | loop | 386.1 | 2.29 | 0.02 | 0.01% |
| 7535695a36 | bubble | 179.3 | 1.71 | 0.26 | 0.14% |
| 7535695a36 | ackermann | 48.0 | 2.87 | 0.16 | 0.09% |

The interpreter's workloads in absolute terms - instructions are cycles times IPC; a miss's
cost is an assumption (Zen 4's penalty, 12 to 18 cycles), not a count:

| design | workload | instructions | branch misses | at 12-18 cycles a miss |
|---|---|---|---|---|
| s6 | kernel | 77.8M | 53K | 2.0-2.9% of its 32.3M cycles |
| s6 | corpus | 391.6M | 172K | 1.3-1.9% of its 161.8M cycles |
| e141550b9a | kernel | 21.0M | 77K | 9.8-14.7% of its 9.5M cycles |
| e141550b9a | corpus | 67.8M | 238K | 9.0-13.5% of its 31.7M cycles |
| c9369657e4 | kernel | 24.3M | 221K | 15.7-23.6% of its 16.9M cycles |
| c9369657e4 | corpus | 72.4M | 280K | 8.9-13.4% of its 37.7M cycles |
| 7535695a36 | kernel | 81.9M | 622K | 12.4-18.6% of its 60.2M cycles |
| 7535695a36 | corpus | 540.7M | 2109K | 6.8-10.2% of its 372.9M cycles |

## What it says

1. **Dispatch is predicted, not mispredicted, on compute work.** fib, loop, bubble, ackermann:
   every interpreted design at most 0.54 misses per thousand instructions (0.36% of branches) -
   Zen 4's indirect predictor follows threaded dispatch almost perfectly. Mispredicted dispatch,
   the case for replicating it (gotodup), is not what limits these designs here.
2. **Yet the evolved interpreted designs run fewer instructions per cycle than s6 with as few
   misses**: c9369657e4 1.85-2.87 and the smallest 1.71-2.95 on that work, s6 2.75-3.86. So
   something serial limits them - the chain of instruction-pointer updates (Ertl & Paysan; the
   "IP-update loop form" deferred in Iteration 260) or the stack's round trips through memory;
   these four counters cannot tell the two apart. The deferred idea stays open: not refuted.
3. **New: the interpreter's work mispredicts heavily on the evolved designs.** kernel and
   corpus, where parsing, the dictionary lookup and number conversion run: 3.5-9.1 misses per
   thousand instructions against s6's 0.4-0.7 - an estimated 9-24% of their cycles there, s6's
   1-3%. Their likely source: the operations evolution chose for that work, written in C with
   loop exits that depend on the data - the lookup's chain walk, SCAN and SKIP, the name
   compare. Which handlers, exactly, is the next measurement (perf record on branch misses,
   against the unstripped engine).
4. **The JIT on ackermann: 1.50% of branches mispredicted** (2.51 per thousand instructions),
   where the interpreted designs mispredict 0.05-0.09% - deep recursion; most likely returns the
   return-address predictor cannot follow (the JIT's tail calls as jumps, jittail), not looked
   at yet.

## Iteration 294: where to look next

- Which handlers take the interpreter's misses (point 3): lab/evolve/missmap.py, for the
  laptop between runs - perf record's samples, each charged to its handler.
- The JIT's ackermann (point 4), read in jit.c: the JIT's code calls and returns with the
  machine stack's call and ret (an EXIT's stencil ends in ret), and A(3,5) recurses far
  deeper than the return-address predictor holds - returns beyond its depth mispredict;
  the interpreted designs return through an indirect jump the history-based predictor
  follows. No fault: a candidate gene - the JIT's EXIT as pop and jmp - worth perhaps
  ackermann's share of the misses, a sixth of the geometric mean; not built.

## Iteration 297: where the cycles stall

counters.py --extra stalled-cycles-frontend:u,stalled-cycles-backend:u on the laptop
(pack forth-vm-evolution-counters-126cd85c9-fury-20261015-023821), the newest front then
seed 50's: s6, e23b0e4770 (fastest with the JIT), 658ed9b9f8 (fastest without),
4c2b4e4485 (smallest). This CPU and perf 6.8 count front-end stalls - cycles the
dispatch had no operation to take - but not back-end ones (n/a).

| design | workload | cycles (M) | instructions per cycle | branch misses per 1k instructions | misses per branch | stalled-cycles-frontend:u, of cycles | stalled-cycles-backend:u, of cycles |
|---|---|---|---|---|---|---|---|
| s6 | kernel | 31.7 | 2.46 | 0.69 | 0.31% | 42.5% | n/a |
| s6 | fib | 196.5 | 3.84 | 0.43 | 0.20% | 18.0% | n/a |
| s6 | corpus | 158.6 | 2.47 | 0.46 | 0.21% | 42.7% | n/a |
| s6 | loop | 342.8 | 3.31 | 0.01 | 0.00% | 27.1% | n/a |
| s6 | bubble | 145.3 | 2.76 | 0.21 | 0.09% | 36.0% | n/a |
| s6 | ackermann | 58.0 | 2.82 | 0.10 | 0.04% | 33.0% | n/a |
| e23b0e4770 | kernel | 9.8 | 2.27 | 3.62 | 2.22% | 32.7% | n/a |
| e23b0e4770 | fib | 38.5 | 5.11 | 0.05 | 0.05% | 3.4% | n/a |
| e23b0e4770 | corpus | 33.6 | 2.15 | 3.22 | 1.88% | 34.4% | n/a |
| e23b0e4770 | loop | 12.5 | 5.50 | 0.12 | 0.10% | 1.1% | n/a |
| e23b0e4770 | bubble | 11.5 | 4.62 | 0.25 | 0.25% | 6.0% | n/a |
| e23b0e4770 | ackermann | 15.2 | 3.57 | 2.56 | 1.75% | 11.7% | n/a |
| 658ed9b9f8 | kernel | 15.7 | 1.63 | 7.49 | 3.77% | 48.9% | n/a |
| 658ed9b9f8 | fib | 190.5 | 2.30 | 0.16 | 0.08% | 48.9% | n/a |
| 658ed9b9f8 | corpus | 34.8 | 1.71 | 6.99 | 3.54% | 46.1% | n/a |
| 658ed9b9f8 | loop | 46.7 | 3.35 | 0.05 | 0.03% | 0.5% | n/a |
| 658ed9b9f8 | bubble | 62.7 | 1.96 | 0.39 | 0.22% | 56.8% | n/a |
| 658ed9b9f8 | ackermann | 46.8 | 2.81 | 0.10 | 0.06% | 35.8% | n/a |
| 4c2b4e4485 | kernel | 63.5 | 1.35 | 8.33 | 4.26% | 54.4% | n/a |
| 4c2b4e4485 | fib | 191.2 | 2.99 | 0.21 | 0.11% | 28.4% | n/a |
| 4c2b4e4485 | corpus | 382.8 | 1.45 | 4.01 | 1.95% | 55.8% | n/a |
| 4c2b4e4485 | loop | 510.0 | 1.89 | 0.02 | 0.01% | 53.6% | n/a |
| 4c2b4e4485 | bubble | 178.2 | 1.79 | 0.30 | 0.16% | 55.9% | n/a |
| 4c2b4e4485 | ackermann | 66.0 | 2.09 | 0.20 | 0.11% | 48.2% | n/a |

- **The evolved interpreted designs are front-end bound on compute work**: 658ed9b9f8
  stalls in the front end 48.9% of its cycles on fib and 56.8% on bubble, where it
  mispredicts 0.16 and 0.39 branches per thousand instructions - waiting for code, not
  recovering from a wrong guess; the smallest 48-56% nearly everywhere; s6 18-36%. The
  JIT's native code hardly stalls there (1.1-6.0%) and runs 4.6-5.5 instructions a cycle.
- So the IP-update loop form - a back-end chain - is not what bounds them
  (results/drafts/iploop-plan.md, its explanation 3, the front end). Next: which part of
  the front end - Zen 4's own events for the instruction cache, the op cache and the
  instruction TLB, through counters.py --extra - and, as a gene, handler entries aligned
  to 32 or 64 bytes (align1 only takes alignment away).
- loop is the exception: tiny, its loops opcodes - 0.5% and 1.1% front-end stalls.

missmap.py's first laptop run (pack forth-vm-evolution-missmap-126cd85c9-fury-20261015-
023127) attributed nothing: every sample without a source line. evolve.build() strips the
engine it measures and keeps the full one as engine.full; missmap.py ran the stripped one.
It runs engine.full now - the same code at the same addresses, with -g's lines.

## Iteration 301: not the caches

counters.py --extra with Zen 4's instruction-cache and op-cache misses (per 1k instructions;
pack forth-vm-evolution-counters-4282d4e17-fury-20261015-140010), seed 51's front:

| design | workload | cycles (M) | instructions per cycle | branch misses per 1k instructions | misses per branch | stalled-cycles-frontend:u, of cycles | ic_tag_hit_miss.instruction_cache_miss:u, per 1k instructions | op_cache_hit_miss.op_cache_miss:u, per 1k instructions |
|---|---|---|---|---|---|---|---|---|
| s6 | kernel | 33.2 | 2.31 | 0.84 | 0.39% | 43.1% | 0.33 | 0.47 |
| s6 | fib | 215.3 | 3.51 | 0.41 | 0.19% | 22.7% | 0.35 | 0.03 |
| s6 | corpus | 166.2 | 2.34 | 0.50 | 0.23% | 44.7% | 0.15 | 0.43 |
| s6 | loop | 352.3 | 3.23 | 0.01 | 0.01% | 26.6% | 0.02 | 0.03 |
| s6 | bubble | 144.3 | 2.77 | 0.20 | 0.09% | 34.2% | 0.14 | 0.06 |
| s6 | ackermann | 58.8 | 2.80 | 0.11 | 0.05% | 30.5% | 0.06 | 0.07 |
| f7a7740238 | kernel | 10.9 | 1.84 | 4.17 | 1.86% | 31.1% | 0.58 | 1.13 |
| f7a7740238 | fib | 40.9 | 4.75 | 0.06 | 0.06% | 4.1% | 0.01 | 0.02 |
| f7a7740238 | corpus | 38.7 | 2.35 | 2.85 | 1.43% | 32.3% | 0.40 | 0.71 |
| f7a7740238 | loop | 11.9 | 5.23 | 0.14 | 0.11% | 1.1% | 0.04 | 0.04 |
| f7a7740238 | bubble | 8.5 | 5.05 | 0.34 | 0.38% | 5.8% | 0.06 | 0.19 |
| f7a7740238 | ackermann | 17.3 | 2.90 | 2.60 | 1.75% | 10.3% | 0.07 | 0.13 |
| a124348f83 | kernel | 15.0 | 1.43 | 7.25 | 4.26% | 45.4% | 0.36 | 0.53 |
| a124348f83 | fib | 135.6 | 2.50 | 0.55 | 0.37% | 18.0% | 0.04 | 0.01 |
| a124348f83 | corpus | 31.8 | 2.05 | 3.37 | 1.72% | 34.0% | 0.27 | 0.48 |
| a124348f83 | loop | 47.9 | 2.81 | 0.06 | 0.04% | 0.5% | 0.03 | 0.04 |
| a124348f83 | bubble | 56.6 | 1.79 | 0.33 | 0.25% | 51.1% | 0.07 | 0.15 |
| a124348f83 | ackermann | 36.5 | 3.01 | 0.12 | 0.09% | 26.4% | 0.04 | 0.07 |
| 0285b1954f | kernel | 64.7 | 1.29 | 8.31 | 4.14% | 55.9% | 0.81 | 1.82 |
| 0285b1954f | fib | 183.0 | 3.11 | 0.21 | 0.11% | 27.4% | 0.04 | 0.02 |
| 0285b1954f | corpus | 373.1 | 1.48 | 3.99 | 1.93% | 54.1% | 0.61 | 1.31 |
| 0285b1954f | loop | 379.4 | 2.55 | 0.03 | 0.01% | 36.9% | 0.02 | 0.02 |
| 0285b1954f | bubble | 151.7 | 2.09 | 0.33 | 0.18% | 45.9% | 0.15 | 0.06 |
| 0285b1954f | ackermann | 62.5 | 2.19 | 0.21 | 0.11% | 46.4% | 0.04 | 0.08 |

- **On compute work the caches hardly miss**: the fastest design without the JIT (a124348f83)
  stalls in the front end 51.1% of bubble's cycles with 0.07 instruction-cache and 0.15
  op-cache misses per thousand instructions; the smallest 46.4% of ackermann's with 0.04 and
  0.08. Mispredictions there are low too. What is left is the dispatch itself: a taken
  indirect jump every few instructions, each ending a fetch block even when predicted. The
  JIT's native code, without them, stalls 1-6%.
- So the front end's lever is fewer dispatches - superinstructions, more words as opcodes, the
  JIT - and not alignment: alignhot (applied after seed 51) is unlikely to pay, as the
  evolution's taking alignment away from most designs (align1) already said.
- The interpreter's work (kernel, corpus) misses more in both caches (0.27-0.81 and 0.48-1.82
  per thousand) and mispredicts most (results/missmap-amd-ryzen-7-pro-8840hs.md).
