# The after-seed-77 batch - to apply first at seed 77's processing (Iteration 557)

Prepared while seed 77 runs (the owner, 557); master stays what seed 77's bundle tests.

    git apply results/applied-after-seed77/jit-holes-after-seed77.patch
    git apply results/applied-after-seed77/lifted-after-seed77.patch

batch-check (557): PASS - run-tests (jitholes-check: d11c9a6300's corpus as s6; the stencil check with the pair), validate 7 of 7 IDENTICAL, the jail. Again at 558 - the first patch's comment corrected (st_callx: under -ftracer, not every build), the patch regenerated whole: PASS.

**jit-holes-after-seed77.patch** (engine/jit.c; lab/evolve/stencil-check.py, engines-check.py, jitholes-check.py new;
tools/run-tests.sh) - **the JIT patches every copy of a value hole**: the root of seed 76's corpus deaths
(results/drafts/corpus-deaths-555.md). jit_scan noted one offset for each value hole - the literal, the return stack,
the throw, EXECUTE and resume helpers - and jit_put patched that one; -ftracer duplicates a block and -fno-crossjumping
keeps the copy, so st_execute held EXECUTE's helper hole twice, one copy left at its marker value: a jump to nowhere.
st_callx holds it twice under -ftracer alone (the sweep, 558: 48 of 332 flag sets), on a path the workloads never take. jit_fill patches every copy: a stencil that
holds a hole once gets the bytes it had. stencil-check.py read 0 stencils under a design's own flags (-ffunction-sections
puts each in .text.*; it read .text) - those flags dropped, an empty read now a failure, repeated holes reported;
engines-check runs it with the pair too. jitholes-check.py (in run-tests): d11c9a6300 rebuilt, its corpus against s6's.
Tested: d11c9a6300 and e80800407e right on every workload (the corpus wrong without it); seed 76's fastest, 7f6362b7e5,
right on all nine. A correctness fix - what computes right computes as before: not a method change (the owner agreed, 558). The sweep (results/drafts/jit-sweep-558.md): every stencil safe to copy under all 332 flag sets tried; the repeated holes only these two.

**lifted-after-seed77.patch** (lab/evolve/lifted.py new; process-seed.sh, README.md) - **the lifted freezes on the true
front**: each gene unfrozen at 556, its share at each value, the enrichment of its other values, prediction 556 scored -
in summary.md. Tested on seed 76's records (every gene at its frozen value: the prediction holds trivially). Changes
nothing a run uses.
