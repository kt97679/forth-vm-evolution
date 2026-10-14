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
