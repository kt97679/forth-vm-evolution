# What Frostbite's search lends this one (Iteration 711)

The owner (711): "can we reuse anything from this" - 3DNews's report of Architect Labs' Frostbite, then the company's
post (architectlabs.com/blog/frostbite): "Reuse whatever you think is reasonable." Frostbite is a general-purpose
processor on interaction nets (Lafont, 1990), designed by swarms of agents against a formal specification; its numbers
are the company's own, pre-silicon, against an unnamed in-order core. Its architecture lends a stack VM little (below);
three things in how it searched do, and two are taken here.

## What it did, as far as the post says

- **The loop.** Agents proposed revisions in parallel worktrees; each was checked against the formal contracts (ASL,
  translated to Lean), modelled in Arcmodel, built in RTL and measured for power, then kept or dropped - "58 ideas, 37
  kept" over four searches and a final ablation round. The search algorithm and the acceptance rule are not given.
- **A fitted model of the truth.** Arcmodel predicts power and performance from counters the specification defines -
  SRAM reads and writes, operations, flits, credit returns, frame misses - about 200-660 times faster than RTL. It was
  fitted: a pipeline found RTL's power hotspots, traced them to the counters, and an agent wrote "any scalar Python
  function over those counters", iterated until model and RTL agreed within 5 %. Worst-case error went from almost
  250 % (hand-written models 40-130 %) to under 6 %, the median about 1.5 %.
- **Held out by group.** 25 workloads in five groups (parallel, staged, sequential, branching, recursive), each group
  split into a search set (10 in all) and a held-out set (15). Perf/W 6.02x on the search set, 3.83x held out - the
  post headlines the held-out figure; the gap is its evidence that some tuning did not generalise.
- **One source of truth.** The contracts, not the Python models or the PDF (deleted once the model was aligned): the
  authors credit it with stopping "reward-hacking instances" in large swarms.

## Taken: the counters, and a model fitted to them (counters-after-seed96.patch)

Our truth is the CPU time over rounds - 10 rounds and three machines for the shortlist, 21 hours for chain A's screen;
the noise is what makes it slow. The PMU gives counts that one run fixes: instructions exactly, branch mispredictions
and last-level misses nearly so. If a function of them predicts the time as closely as Arcmodel predicted RTL's
power, it is a screen that needs no rounds, and a check on a reading (a measure far from its model is a noisy one, or
a design doing something else). tools/cputime.c read cycles and instructions already (707's ideation, row 18: "INSTR
beside time on the shortlist" - an experiment for chain B, not set up). The patch:

- cputime reads two more counters, branches mispredicted and last-level misses (each on its own, absent where the PMU
  lacks it; four events, no multiplexing on the hosts' cores);
- evolve.py keeps each run's counters (run_metric), their medians per workload and side (measure(): LAST_CNT), and a
  record's "cnt" - [instructions, cycles, mispredictions, misses] per workload - beside its "raw" times;
- loadtest.py's line per design (chain B's) carries "cnt", the first idle measure's, the design's and s6's;
- lab/evolve/countfit.py fits per workload ns = a*instructions + b*mispredictions + l*misses + c (least squares on
  relative error), held out by design (5 folds), and the instructions alone beside it; prints the error by workload
  and over all, and the design's speed predicted against measured (Spearman, error). --self-test on a known model
  with 2 % noise: 1.5 % median error with three counters, 19 % with instructions alone; in run-tests.

Here, in a VM without the PMU, the lines are absent and nothing changes (the parsing tested with a cputime that adds
them). On the laptop, dream and rage, chain B records them for its ~60 designs at 10 rounds: the data to fit and
judge. What would follow, if the model holds within a few percent: a one-run screen for the reopened search, rounds
spent where the model and the reading disagree or two designs are close. If it does not, the record says how far.

## Taken: the held-out check, on the data there is (results/drafts/heldout-711.py, .txt)

Frostbite's 6.02x against 3.83x is the question for our selection: does the search set's speed carry to workloads
never selected on? Every record has the held-out pair, sieve and parse, measured in the same rounds. On the screen's
pool (results/followup-seed96-roles.md, 944 designs, 8-byte cells, ratios to s6):

| | designs | Spearman, search set to held-out | the search set's top 20 %: search, held-out | pool medians | advantage carried (log) |
|---|---:|---:|---|---|---:|
| all | 944 | 0.908 | 0.123, 0.089 | 0.146, 0.102 | - |
| JIT | 530 | 0.701 (parse alone 0.107) | 0.122, 0.088 | 0.140, 0.094 | about half |
| not JIT | 414 | 0.585 | 0.273, 0.233 | 0.305, 0.238 | about a fifth |

The 0.908 over all is the JIT against the interpreters; within each family the ranking carries less, and least at
the interpreted end - its top 20 % by the search set sit at the held-out pair's 40th percentile (the top 1 %, four
designs, at the 43rd). Some of that is the winner's curse (a pool chosen on the search set's readings, noise
included), some is what the pair measures (sieve a loop, parse the outer interpreter); two workloads are a thin
held-out set. Not changed here - the workloads and the roles' rule are the owner's:

- **Proposed: the roles' write-up gives each role's held-out pair beside its speed**, as Frostbite headlines its
  held-out figure.
- **Proposed, for the reopened search: more held out, by group.** The nine workloads in groups - calls and
  recursion (fib, ackermann), loops and arrays (loop, bubble, sieve), the outer interpreter (kernel, corpus, parse),
  programs (apps; the held-out three - wordfreq, minif, brainless - unmeasured for time) - and in each group one held
  out. Today recursion and programs have none; the three programs timed as a held-out "apps2" would give the
  programs one, at a held-out workload's cost per evaluation.

## Not taken

- **The architecture.** "Explicit links between operations" instead of hardware discovering dependencies is what a
  stack VM's code already is, and what the JIT's stack caching would exploit (GOALS.md: priced, deferred, 218-219);
  "each value one owner, used once" is close to Forth's stack, DUP and DROP the explicit copy and erase; tiles,
  work stealing and fine-grained clock gating are hardware a single-threaded VM has no use for.
- **Swarms of agents.** The project's rule: no agents unless the owner asks.
- **The ablation round** we have: knockouts (newgenes.py's pairs) after each series.
- **One source of truth** we have as the gate and the checks: the corpus against the cell engine, the kernel against
  the seed, the output against s6's (516), the fuzzer against s6 (707). Frostbite's "reward hacking" is our 516 - the
  cpt16 designs that stopped early in apps and timed 0.13 of s6.
