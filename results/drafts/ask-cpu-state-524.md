# Why would a paired benchmark ratio shift ~7% between a loaded run and a quiet re-measure on a Ryzen laptop?

I benchmark many variants of a small virtual machine on an AMD Ryzen 7 PRO 8840HS laptop (Zen 4, 8 cores / 16
threads), Linux. Each variant's speed is a **ratio to a fixed reference program**, measured in pairs. The fastest
variants come out ~7% slower (ratio 1.07 higher) when re-measured after the long run than during it - every run. I have
ruled several causes out and would like expert knowledge of the CPU and Linux side, and a diagnostic plan. Please give
checkable answers and say "unsure" where unsure.

## How a measurement is made

- A helper runs the program and reports its CPU time as user + system time of the child, from
  `getrusage(RUSAGE_CHILDREN)`, in nanoseconds; the measuring process is pinned with `taskset` to one core (the one
  that, with its SMT sibling, was least busy over a second when the run began).
- Each round runs the variant and the reference back to back (alternating which goes first); 3 rounds; a workload's
  time ratio is the median variant time over the median reference time; seven workloads, geometric mean.
- **During the run**, four worker processes, each pinned to its own core, do this continuously - and also compile
  each variant with gcc or clang (0.5-2 s each) between measurements. So the machine is under heavy, mixed load
  (compiles and benchmarks) for 9-11 hours.
- **After the run**, the fastest variants are measured again the same way, alone - or, in one experiment, beside three
  co-running processes each running benchmarks (not compiles) on other cores.

## What is known

- **Noise is small**: one reading's noise is ~1%; a variant measured twice during the run, a generation apart, agrees to
  0.07% on average - so it is not selection of a lucky reading.
- **Co-runners that only benchmark change nothing**: alone and beside three such co-runners, after the run, the ratios
  agree to 1.2% (median) - and both are ~7% above the in-run ratios (alone 1.069, loaded 1.080).
- **The binaries are identical**: rebuilt after the run, byte for byte the same as in the run.
- The variants differ in kind from the reference: the fastest are JIT-compiled (copied machine code, a few hundred KB
  of executable memory written at run time), while the reference is a plain bytecode interpreter in C.
- A cycles-based metric (hardware cycle counts via performance counters) is available instead of CPU time but is not
  what the runs use.

## The questions

1. What on Zen 4 / Linux could make a JIT-heavy program and an interpreter respond differently to the machine's state
   - clock frequency and boost under all-core load against light load (and amd_pstate / EPP / platform profiles on a
   laptop), SMT sibling activity, L3 or memory contention from compiles, thermal state after hours, kernel work
   (page faults, TLB, I-cache flushes for the JIT's writes) - so that their **ratio** shifts while each is measured in
   pairs?
2. Does CPU time from getrusage behave differently from cycles under frequency changes in a way that matters here?
3. A diagnostic plan: which counters or tools (perf stat events, turbostat-like readings, /sys/devices/system/cpu
   frequency files, amd_pstate status) to record during the run and after, and which experiment would separate the
   causes - with what result pointing to which cause.
4. Which speed to optimise: under the run's load or alone? Any established practice for benchmarking under load vs
   isolated (e.g. fixing the frequency, disabling boost, isolcpus) and its cost on a laptop.

## The answer I'd like

For each question: the mechanism(s), how likely here, how to test, and references (links) - AMD documentation, kernel
documentation, benchmarking literature. Mark what you are unsure of.
