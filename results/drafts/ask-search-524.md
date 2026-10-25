# Getting more out of a fixed evaluation budget in a multi-objective evolutionary search

I run an evolutionary search over designs of a small virtual machine (a Forth system: a C engine plus a compiled
image). Each run has a fixed wall-clock budget; I'd like to know which established methods would get better results
from the same budget, given my costs. Please give checkable recommendations with references (links), and say "unsure"
where unsure.

## The setting (numbers from the last runs)

- **A design** is a genome of 71 genes for its encoding family (binary, small-valued, and a few list-valued ones such as
  which operation pairs become superinstructions), plus the family itself (4 encodings). 14 genes are frozen.
- **Evaluating one design** (~4-5 s of one core): compile its C engine (0.5-2 s - about half the time for the fast
  designs), convert its image, check correctness (a corpus, far-memory and audit tests; every workload's output compared
  with a reference's), and measure: seven selection workloads, 3 rounds each, each round paired with a fixed reference
  design run back to back. Then the same at 32-bit cells (another compile and measurement).
- **Objectives**: speed (geometric mean of the seven workloads' time ratios to the reference; noise about 1% per
  reading), size (engine + image bytes, exact), memory (peak RSS, near exact), and the 32-bit speed - four, minimised,
  with tolerances in dominance (2% for speed).
- **The search**: 256 children per generation, ~100-155 generations a run (26,000-40,000 designs in 9-11 hours on four
  workers); NSGA-II (non-dominated rank, then crowding); children by mutation (~52%), uniform crossover (~37%) and
  "borrowing" a whole block of genes from an unrelated design (~11%); an archive of up to 128 designs holding gene
  values no survivor has, drawn from with probability 0.1. The front holds ~185-210 designs.
- **A surrogate screen already exists**: an additive model - one weight per gene value - of log speed and log size,
  fitted by SGD every 10 generations from generation 5 on the earlier generations' living designs; a child predicted to
  be beaten by at least 30% in speed and 5% in size by something already measured is not evaluated (one in ten of those
  is evaluated anyway, as a check). It skips ~19% of children; offline it predicted speed within 8.2%, size within 1.2%.
- **Islands** (separate subpopulations) were tried once: no better than the replicates.
- **Where it stalls**: in the last run the best speed improved by 2% or more in 15 generations, the last at generation
  66 of 102; the smallest size gained in 23 generations, the last at 93.

## The questions

1. **The surrogate**: given categorical genes with interactions, which model would predict better for the same cost -
   random forests, gradient boosting, factorization machines, Gaussian processes with categorical kernels, an ensemble?
   And should screening use the model's uncertainty (e.g., probability of improving the front, expected hypervolume
   improvement) instead of a fixed margin?
2. **More children from the same compute**: multi-fidelity evaluation (a cheaper partial measurement first - e.g. one
   round, or a subset of workloads - and the full one only for promising children), or anything else that cuts the cost
   of hopeless children before the compile, which is the dearest step.
3. **Variation**: adaptive operator selection (credit to mutation, crossover, borrowing by how often their children
   enter the front), or operators that learn which genes go together (linkage learning, estimation-of-distribution).
4. **Stagnation**: what helps a multi-objective search that stops improving its extremes two thirds into the run -
   restarts, increasing mutation, quality-diversity archives (MAP-Elites over size bins), reference-point methods
   (NSGA-III) - and how to tell stagnation from having found the optimum.
5. **For my costs**, rank the above by expected gain per unit of implementation effort, with the number you would expect
   (designs saved, hypervolume) where you can.

## The answer I'd like

Ranked recommendations; for each: the mechanism, what to implement, the expected effect and how to measure it, pitfalls,
and references with links. Mark what you are unsure of. Plain-Python implementability matters (no heavy dependencies).
