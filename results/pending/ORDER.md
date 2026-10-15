# The after-seed-52 batch - apply in this order (against master after Iteration 312)

| # | patch | what it does |
|---|---|---|
| 1 | jitscan-after-seed52.patch | The JIT fault seed 52 found (results/drafts/jit-loop-crash.md): jit.c read each stencil at most 64 bytes in a build without jitloop, and a design's (LOOP) stencil was 72 - read to its fall-through, its loop-back missed, copied short: a segmentation fault on `: GD1 DO I LOOP ; 4 1 GD1`. The scan now reads 160 bytes in every build (its end is the last jump to NEXT or JUMP, which only stencils make; the next table function still bounds it), and every branching stencil - 0BRANCH, (LOOP), (+LOOP), (?DO), DUP n > ?BRANCH both exits, BRANCH and LEAVE their jump - must have been read with them, in every build, or is not used: slower, never wrong (Iteration 129 checked (+LOOP) and (?DO) only, and only with jitloop). And lab/evolve/regressions.json: designs that once failed, built and run on the corpus by engines-check every time - the first, seed 52's two. A fix, not a gene: no reseed, no id changes. |

    git apply results/pending/jitscan-after-seed52.patch

Patch 1, tested on master at Iteration 311 in a scratch tree: the build; seed 52's two dead
designs - the micro-program 3 2 1, the corpus right; engines-check PASS, 59 paths - the two
regressions among them; run-tests PASS; the gate, seed 52's front and the joint front: 252
of 252 alive (164 and 130, 42 in both). Speed, three JIT designs of seed 52's front against
s6, master and the fix: no change past the VM's noise - the one that looked slower (92fb0375b9,
loop 0.043 and 0.060 from 2 rounds) measured 0.043 on both, twice, from 5 rounds. It applies on
a fresh clone of master after Iteration 312 and reproduces the tested files.
