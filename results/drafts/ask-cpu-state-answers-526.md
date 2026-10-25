# The answers to the CPU-state prompt, checked (Iteration 526)

Five answers to results/drafts/ask-cpu-state-524.md (the owner, 526): why a design's ratio to s6 is ~7% higher
measured after the run than in it. What can be checked here is checked; the deciding measurements are the laptop's.

## Where they agree, and what our own data adds

All five put **the machine's operating point first** - sustained all-core frequency and package power/thermal limits
under the run's compiles, against a single core boosting alone after it - with **SMT and compiler-specific contention**
second, and a JIT's code-writing costs last. The mechanism that fits the *direction* (the ratio rises when quiet): s6, the
interpreter, is the more compute-bound of the pair, so a higher clock helps it more than a design whose time is partly
stalls that a clock does not shorten. **Our counters study (Iteration 285, results/counters-amd-ryzen-7-pro-8840hs.md)
points the same way**: on the kernel workload s6 ran 2.41 instructions a cycle and 0.68 branch misses per thousand
instructions, the fastest JIT design 2.21 and 3.69 - five times the misses. Consistent with the theory; not proof.

**The decisive measurement is already in our helper**: tools/cputime.c reports CPUNS (getrusage) and - when the
counters are readable (perf_event_paranoid at most 2; lab/evolve/perf-hold.py set that for counters.py) - CYCLES and
INSTR of the same run, user space. All five answers say: compare the time ratio with the cycle ratio across conditions;
if cycles hold while time moves, it is the clock.

## Claims checked

| claim | who | verdict |
|---|---|---|
| getrusage time is scaled through PELT / arch_freq_scale | 49 | **wrong** - load tracking scales by frequency; CPU-time accounting does not |
| getrusage is "wall-clock CPU time" | 51 | muddled - it is time on the CPU, user and system; not wall time |
| getrusage resolution: microseconds, though our helper prints nanoseconds | 53 | **right** - ru_utime is a timeval; the CPUNS figure has microsecond grain (fine for runs of milliseconds) |
| three benchmark-only co-runners leave compile-specific contention and thermal history untested | 50, 53 | **right** - the experiment of 520 had no compiles and ran after the run |
| "SMT off first" | 51 | costly (a reboot or the firmware); a busy sibling under control answers the same (53) |
| "research shows interpreters have better locality" | 52 | its citations are placeholders - unverifiable |

## The answers, ranked

53 the most careful: the ratio written out, a table from (time ratio, cycle ratio) to cause, a four-condition crossover
(quiet; benchmark-only co-runners; compile-only co-runners; compile load after the machine has heated), the
microsecond note. 50 sound, the direction reasoned, consistent with our counters. 52 the clearest on cycles against
time but with empty citations. 51 reasons itself into the direction mid-answer and leads with an expensive test. 49
has getrusage wrong.

## Proposed (the owner's)

**contention.py made the decisive test** - as 53's crossover, on the laptop: the fastest of the front measured paired
with s6 (a) alone, (b) beside three benchmark co-runners, (c) beside three compile co-runners (gcc compiling engines on
other cores, as the run's workers do), recording for every run both CPU time and cycles (the counters held readable for
its duration, as perf-hold.py does), and the cores' reported frequency. If the cycle ratio holds where the time ratio
moves, the offset is the clock: then the owner's choice - select on the speed under load (as now), on cycles (frequency-
free), or measure alone.
