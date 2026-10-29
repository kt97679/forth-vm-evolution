# The after-seed-79 batch - to apply first at seed 79's processing (Iteration 564)

process-run.sh checks and applies it.

    git apply results/applied-after-seed79/deaths-reach-after-seed79.patch
    git apply results/applied-after-seed79/random-mode-after-seed79.patch
    git apply results/applied-after-seed79/lifted-express-after-seed79.patch

batch-check (564, on cb07975 - the three patches): PASS - all applied to a fresh clone, run-tests PASS, validate 7 of 7
IDENTICAL, the jail PASS.

**deaths-reach-after-seed79.patch** (lab/evolve/deaths-check.py, gene-narrow.py, README.md) - seed 78's three kernel
deaths classified: the reach limit at scale 1, known since Iteration 10 - reach_lethal does not run cv8 designs with a
two-byte call or DOES> form at scale 0 (2^14 bytes; the kernel workload's dictionary is larger) and runs them, jailed,
at scale 1 (2^15; 13 of 18 lived in seed 2). doesfar frozen at 1 (409-556) hid it; lifted, it is back: seed 78's six
such designs, three screened, the three measured dead. gene-narrow.py (new) found it: doesfar=0 necessary and
sufficient on each of the three (the other five lifted values, fold and skippad innocent); doesfar=0 with varcall=1
lives at scales 2-3 (474). deaths-check.py now names the class expected - on seed 78: 0 to rebuild, 0 open.

**random-mode-after-seed79.patch** (lab/evolve/evolve.py, next-run.sh) - **the random-search baseline, ready** (GOALS.md,
"When the improvements are done"): results/drafts/random-mode-548.patch brought up to date - its next-run.sh half no
longer applied (562's carryall on the same lines), its five additions put on today's; evolve.py's half unchanged.
NEXT-RUN's word "random": every child a fresh random genome, nothing learned in the loop. Smoke-tested (564): --pop 4
--gens 1 --noevolved --random, exit 0 in 170 s - generation 0 as the line makes it, generation 1 four random children.

**lifted-express-after-seed79.patch** (lab/evolve/lifted.py) - **the lifted genes read as built**: express(), not canon -
563's open question closed. On seed 78's true front every lifted gene is at its old frozen value as built (msc 35%
and n/e 65%, sharedcall and alignhot n/e 100% - written values that do nothing drift: 24%, 78%, 16% as written);
the other values' enrichment 0.00 throughout. Prediction 556 holds on seed 78 (lifted.py: HOLDS).

