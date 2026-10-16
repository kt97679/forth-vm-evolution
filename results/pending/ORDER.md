# The after-seed-52 batch - apply in this order (against master after Iteration 312)

| # | patch | what it does |
|---|---|---|
| 1 | jitscan-after-seed52.patch | The JIT fault seed 52 found (results/drafts/jit-loop-crash.md): jit.c read each stencil at most 64 bytes in a build without jitloop, and a design's (LOOP) stencil was 72 - read to its fall-through, its loop-back missed, copied short: a segmentation fault on `: GD1 DO I LOOP ; 4 1 GD1`. The scan now reads 160 bytes in every build (its end is the last jump to NEXT or JUMP, which only stencils make; the next table function still bounds it), and every branching stencil - 0BRANCH, (LOOP), (+LOOP), (?DO), DUP n > ?BRANCH both exits, BRANCH and LEAVE their jump - must have been read with them, in every build, or is not used: slower, never wrong (Iteration 129 checked (+LOOP) and (?DO) only, and only with jitloop). And lab/evolve/regressions.json: designs that once failed, built and run on the corpus by engines-check every time - the first, seed 52's two. A fix, not a gene: no reseed, no id changes. |
| 2 | bfind-after-seed52.patch | The gene bfind (Iteration 316): THREAD-FIND's and (FIND)'s walk with fewer branches to mispredict - (FIND) was 9-13% of the interpreter-heavy runs' mispredictions on the laptop (results/missmap-amd-ryzen-7-pro-8840hs.md). A candidate's count byte and first seven characters as one masked 64-bit compare - almost always unequal, so predicted - the rest of a longer name only on a match; a link read without a branch on its form (TAG2's 1-4 bytes, CV8's 1-3). Exactly the walk it replaces: the same word found, or none (a name over 31 never found, as there). Expressed when (FIND) or THREAD-FIND is a format-10 opcode of the design (klookup's (FIND), tfind's THREAD-FIND - never both; on seed 52's front 61 and 67 designs). One label a handler, the condition inside the body around the walk only: with the gene off the handlers are token for token what they were. Four engines-check paths: each word, each link form. A new gene: no reseed; ids unchanged. |

    git apply results/pending/jitscan-after-seed52.patch
    git apply results/pending/bfind-after-seed52.patch

Patch 1, tested on master at Iteration 311 in a scratch tree: the build; seed 52's two dead
designs - the micro-program 3 2 1, the corpus right; engines-check PASS, 59 paths - the two
regressions among them; run-tests PASS; the gate, seed 52's front and the joint front: 252
of 252 alive (164 and 130, 42 in both). Speed, three JIT designs of seed 52's front against
s6, master and the fix: no change past the VM's noise - the one that looked slower (92fb0375b9,
loop 0.043 and 0.060 from 2 rounds) measured 0.043 on both, twice, from 5 rounds. It applies on
a fresh clone of master after Iteration 312 and reproduces the tested files.

Patch 2, tested on master at Iteration 316 with patch 1 applied beneath it, in a scratch tree:
the four cases - a seed 52 klookup and a tfind design (TAG2), s6 with kfast and tfind and s6
with kfast, kinput and klookup (CV8) - built with bfind and right on the corpus; gene-equiv.py
against patch 1: all 3,561 recorded genomes' ids and expressions the same - its FAIL is the 5,000
operator draws, which differ for any new gene (the search can draw bfind), as after-seed-51's
alignhot; run-tests PASS, 63 engine paths - the four bfind paths and the two regressions among
them; validate 7 of 7 IDENTICAL; forced, 32 designs of seed 52's front (16 with (FIND), 16 with
THREAD-FIND, across it) built with bfind - 32 alive, the corpus right. A first form duplicated
each handler's label under #if/#else: the multi-state generator (gen-msc) failed on it - 5 of 63
paths - and would have failed every msc design, the gene off too; engines-check caught it.

Speed on the VM, without/with bfind, A-B-B-A, 3 rounds each: the (FIND) design kernel 0.951,
corpus 0.993, parse 0.984; the THREAD-FIND design 1.005, 0.990, 1.009 - nothing past the VM's
noise, the kernel's -5% for the (FIND) design perhaps a small cost. The gene is for the laptop's
predictor; a single-core Xeon guest cannot say. An option, not a change: the evolution keeps it
where it pays, and missmap on the laptop can count its mispredictions directly.

Both patches apply on a fresh clone of master after Iteration 317, in this order, and reproduce
the tested files.
