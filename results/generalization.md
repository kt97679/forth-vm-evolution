# Generalization: one machine, small programs, the selection's own workloads (Iteration 305)

The owner's three concerns, with what this project measures about each and what it
does not.

## 1. Over-fitted to the selection's workloads? Partly - checked by heldout.py

lab/evolve/heldout.py on the last three fronts - selection speed against the held-out
sieve's, both against s6 on the same machine:

| seed | designs | Spearman | the 10 fastest by selection, rank on sieve | sieve / selection speed |
|---|---|---|---|---|
| 49 | 172 | 0.939 | 5 1 7 2 3 6 8 4 23 22 | 0.38 - 2.70 |
| 50 | 187 | 0.942 | 3 9 11 5 12 4 38 1 13 6 | 0.36 - 2.61 |
| 51 | 162 | 0.943 | 3 2 1 4 28 36 10 18 34 8 | 0.37 - 2.64 |

The ranking holds overall and the very fastest hold their places; but a steady group
of designs is 2.5-2.7 times better on the selection than on sieve - flattered by it.
The selection is half the outer interpreter (kernel, corpus) and half compute loops;
a design rich in lookup and parsing operations and poor in loop and memory ones looks
better on it than on sieve. heldout.py now runs in every seed's processing.

## 2. Over-fitted to this CPU? Not measured - every selection measurement is the laptop's

Every speed that has driven a selection came from one AMD Ryzen 7 PRO 8840HS (Zen 4).
What carries to any CPU: fewer dispatches and fewer instructions, the size of image and
engine, memory. What may not: alignment (alignhot, align1, alignfn), GCC's goto
duplication (gotodup), clang or GCC, link-time optimisation, the JIT's native calls and
returns (a 32-entry return-address stack here, 52 on Zen 5; Intel's Golden Cove slow on
deep returns), and which opcodes earn a slot where the indirect predictor is strong. The
check: the joint front measured on a second CPU - an Intel x86, and the planned Tegra
(ARM) session - its ranking against the laptop's, as heldout.py does for workloads.

## 3. Skewed by small programs? Likely - the counters say the hot code fits everywhere

On the compute workloads the instruction cache and the op cache miss under 0.2 times a
thousand instructions (results/counters-amd-ryzen-7-pro-8840hs.md): the hot code fits,
and the predictors see few dispatch contexts. kernel and corpus - the cross-compiler and
the test suite - are the largest programs selected on, and the only ones that miss
(0.3-1.8 a thousand). A program of thousands of words would press the predictors, the
caches, and the dictionary - the fast designs all took 16 hash threads, the fewest - and
a JIT design would pay its translation on code run once. None of that is measured. The
check: a held-out workload whose code footprint grows - generated programs of N words,
N from hundreds to tens of thousands, run hot and run once, and a compile-heavy one -
each front design's time per dispatch against N.

**Iteration 370: the generator** - lab/evolve/footprint-gen.py: N colon definitions in L levels (a word
calls one of the level below, by a test on its argument - chains of at most L, a shallow return stack
at any N), a table of every word's token, and a driver running it round-robin for --calls calls; prints
a checksum. --defs-only stops after the table: the run phase is the full program's time less it.
Checked here: s6 and seed 56's fastest (a0a0277bf2, its JIT on) give the same checksums at N = 100,
1,000, 10,000 and 30,000, both variants. Single runs on the development VM, only for scale: s6 defines
10,000 words in 3.4 s and 30,000 in 41 s (its dictionary searched linearly - quadratic); the fastest,
0.31 s and 3.0 s (hashed, still superlinear). The run phase grows with N too - 200,000 calls: s6 about
0.03 s at N = 100 and 0.14 s at 10,000; the fastest 0.01 s and 0.06 s - the footprint the plan
expected. At 30,000 the definitions swamp a fixed 200,000 calls (the difference within the noise of
two 40-second runs), so the experiment scales --calls with N (at least 40 N): time per call is the
measure, and cycling a footprint past the caches keeps the code cold however often each word runs.

**Iteration 371: the experiment** - lab/evolve/footprint.py, run by the chain as `experiment footprint.py`
over every run's database (the newest run's front taken): K designs sampled from fastest to slowest by
selection speed, each built and passed through alive(); every program, full and definitions-only, timed
in rounds with s6 once per round, size and variant (at 30,000 words s6 costs most of a round), s6 first
in even rounds and last in odd; medians; checksums against s6's, a design that differs reported and not
ranked. Reports s6's time per word and per call, each design's run and compile ratios to s6, and the
Spearman correlation of selection speed with the run ratio at each N. Tried end to end here (2 designs,
N = 100 and 1,000, 2 rounds): s6's run phase 157.5 ns a call at N = 100 and 274.9 at 1,000; seed 56's
sampled fastest 0.280 and 0.234 of s6's - the pipeline, not yet the measurement.

