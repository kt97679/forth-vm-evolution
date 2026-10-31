# The after-seed-84 batch - applied at once, before seed 84 runs again (Iteration 574: seed 84 failed)

No seed to process: batch-check, then applied to master by hand in Iteration 574 (HANDOFF-REFERENCE.md's step 6).

    git apply results/pending/retired-after-seed84.patch

batch-check (573, on f502cba - 1 patches): PASS - run-tests PASS (the generators: 107 paths), validate 7 of 7 IDENTICAL,
the jail PASS.

**retired-after-seed84.patch** (lab/evolve/evolve.py) - Iteration 574: seed 84's failure. Its chain (d00ce78b1) measured
generation 0's 14,219 founders in 5 hours, then breed()'s first crossover stopped on KeyError 'jithelp'. Seeds 70-71 ran
before Iteration 516 deleted jithelp, jitre and nocase; their genomes still hold them, canon() back-filled LATE genes but
kept dead keys, and crossover(a, b) reads b[k] for each key of a - so a seed-71 parent beside any newer one fails. Never
seen before: carryall (562) is the first to carry seed 71, and carry-check (an experiment step) builds and measures the
pool but never breeds it. canon() now keeps only current genes (CV8, CC0, LATE, enc - exactly a hand-made stage's keys);
carry_pool() stops the run at once, naming the design and the genes, on a genome whose keys are not the current ones -
the silent class jithelp was (a dormant gene: generation 0 measured those designs, only breeding read it). Tested
(results/drafts/retired-genes-574.py, on the 3,489 genome records of seeds 70-83's results files): before, 210 of seed
71's carried genomes off the current genes and 7,079 KeyErrors in its crossovers; after, none - crossover, mutate and
borrow both ways against s6 and a seed-83 genome, and every design's id the same as master's; carry_pool on databases of
seeds 71 and 83 - 404 carried, all current; the guard's negative control (a cv8 genome without skippad) stopped.
