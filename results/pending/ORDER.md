# The after-seed-79 batch - to apply first at seed 79's processing (Iteration 564)

process-run.sh checks and applies it.

    git apply results/pending/deaths-reach-after-seed79.patch

batch-check (564, on d07e175): PASS - applied to a fresh clone, run-tests PASS, validate 7 of 7 IDENTICAL, the jail PASS.

**deaths-reach-after-seed79.patch** (lab/evolve/deaths-check.py, gene-narrow.py, README.md) - seed 78's three kernel
deaths classified: the reach limit at scale 1, known since Iteration 10 - reach_lethal does not run cv8 designs with a
two-byte call or DOES> form at scale 0 (2^14 bytes; the kernel workload's dictionary is larger) and runs them, jailed,
at scale 1 (2^15; 13 of 18 lived in seed 2). doesfar frozen at 1 (409-556) hid it; lifted, it is back: seed 78's six
such designs, three screened, the three measured dead. gene-narrow.py (new) found it: doesfar=0 necessary and
sufficient on each of the three (the other five lifted values, fold and skippad innocent); doesfar=0 with varcall=1
lives at scales 2-3 (474). deaths-check.py now names the class expected - on seed 78: 0 to rebuild, 0 open.
