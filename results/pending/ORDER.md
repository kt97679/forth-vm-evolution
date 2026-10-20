# The after-seed-63 batch - apply in this order (after the after-seed-62 batch)

Queued at Iteration 424 by the owner's word (423: "queue both for the after-seed-63 batch" - "please proceed"). From the
register-machine work (results/wip-regmachine/README.md): the pricing found the gains a register stage was priced for
largely in place already, gene by gene - and what keeps the small end from them is their bytes. These two make two of
those run-time compilers cheaper without changing what they compile. They wait one run: seed 63 judges the after-seed-62
batch, and these change bytes the search weighs.

| # | patch | what it does |
|---|---|---|
| 1 | rtimm-lean-after-seed63.patch | rtimm=2 in a plain-CV8 design with no built pairs and no fused tests builds forth/cv8-imm.4 alone - the immediates (`n +` as ADDI n, `SWAP n +` as SWAP+I n) over the kernel's own compiler, without cv8-fuse.4's pair lookup and fold-table copy; BEGIN clears LAST-OP; four internal words headerless. Seed 58's smallest: +240 bytes instead of +608 for the same fib -13.6%. Tag-2 designs, and any with pairs or fused tests, keep the full overlay. (results/wip-regmachine/rtimm-lean-422.patch, rebased onto the after-seed-62 batch: one line placed by hand, the same changed lines.) |
| 3 | islands-after-seed63.patch | Added at Iteration 436 (the owner: implement it for the next runs; results/drafts/escape-mechanism-435.md). evolve.py --islands K: the population in K islands, each ranked and bred alone (the same breeding and survival, a share of the population and of the Q keepers each), every 10 generations (EVOLVE_MIGRATE) each sends its two fastest and its best by Q to the next in a ring; the run's front is every island's together, as the report reads the whole database. The generation loop's breeding and survival moved into two helpers, unchanged for one island - the same statements in the same order. next-run.sh: the word "islands" in a seed line - --islands 4. Off unless a line says so. |
| 2 | rtloop-lean-after-seed63.patch | The run-time loop compiler's X10-XTS (forth/cv8-fuse-loop.4) as three 16-bit offsets with no range check, written by tools/layout.py: 56 bytes less a design (rtloop=2 +361 -> +305 on seed 58's smallest), the code it compiles the same. (results/wip-regmachine/rtloop-lean-423.patch, unchanged.) |

    git apply results/pending/rtimm-lean-after-seed63.patch
    git apply results/pending/rtloop-lean-after-seed63.patch
    git apply results/pending/islands-after-seed63.patch

## How each was tested

On master (results/wip-regmachine/README.md, Iterations 422-423): seed 58's smallest design measured with the profiler
(deterministic dispatches) and built at 64 and 32 bits; fifteen run-time compiles - a literal before BEGIN, `n +`,
`SWAP n +`, loops with I, nested J, UNLOOP EXIT, ?DO, LEAVE, +LOOP, branches - the same numbers in every variant; every
seed 58 and 60 front design with rtimm=2 (6) or the loop compiler (301) rebuilt, all alive; run-tests PASS; validate
7 of 7 IDENTICAL.

**Rehearsed with the after-seed-62 batch (Iteration 424, rehearsal-424.out)**: a clone of master with the thirteen
applied, then these two: the stages built; run-tests PASS; validate 7 of 7 IDENTICAL; test-jail PASS; seed 58's smallest
at 64 and 32 bits in five variants, the corpus right and the fifteen compiles the same in each (both on: +551 bytes at
64 bits, +511 at 32); 36 front designs with rtimm=2 or the loop compiler (all six with rtimm=2, every tenth of the rest)
built and alive, one of them lean.

**Patch 3, tested (Iteration 436):** a run of 16 designs, 4 generations with four islands and migration every 2
(EVOLVE_MIGRATE=2): each island ranked and bred alone, migrants at generations 2 and 4 (2-3 an island), the attic fed
from every island's demoted designs (6, 19, 23, 26), the fast gate re-measuring as usual, the report written
(results/drafts/islands-smoke-436.log); and the same with one island, two generations - the generation and attic
lines as before (islands-smoke-436-one.log).

## When

Moved into results/pending/ at seed 62's processing (Iteration 433), once the after-seed-62 batch was applied, and
batch-checked against that master; applied at seed 63's processing, as the routine applies any batch.
