# The gene callrel - a draft, not in the batch (Iteration 164)

The owner: tag-2 calls by their offset from the image base (today), by their
distance from the call site, or either - a bit saying which - all three as a
gene. results/drafts/callrel-draft.patch, against the eleven pending patches.

## Measured first (seed 37's smallest, 13 and 14 bits)

Executed calls, bytes each: from the base 2.00-2.10 on the eight workloads,
3.00 on far; from the call site 2.00-2.99 (bubble 2.82, sieve 2.99); either
2.00-2.10 and 2.00 on far. The kernel images' own calls (496 and 387 sites):
13 bits from the base cost +0 bytes (the images are under 8 KB), the call site
alone at 13 bits +35 and +41, either +0. A design whose image grows past 8 KB
would pay a byte per call to a word above 8 KB that the site form cannot take.

## Built

- vm-lab.c: CALLREL 0/1/2 - T2TARGET in the three decode labels and DODOES;
  at 0 the engines are byte for byte the same (12 stage engines checked).
- jit.c: the translator, its report and jit_repoint decode and re-encode by
  the mode (repoint keeps the call's own form).
- The converter: --call-rel 2 writes the kernel's calls in the base form with
  the low bit 0 (no positions needed); CV8-CALLREL-V and CV8-T2WIDE-V for the
  run-time compiler. 1 - by distance alone - refused: the converter would have
  to place the kernel's calls by distance.
- cv8t.4: CALL, and !CALL by the mode; T2CALL-REL picks the shortest form,
  never the 3-byte one under t2wide (140 of seed 38's 165 front designs).
- evolve.py: callrel 0/2 in the cv8 family, tag 2 only; off, it stays out of
  the id - every recorded design keeps its id.

## Tested

The smallest (t2wide), the JIT founder (t2wide, JIT) and a design without
t2wide, each with callrel 0 and 2: alive (the corpus, the kernel workload, far,
full), and the whole corpus compiled past a 4 MB ALLOT (the owner's trick: every
test word in long-call reach) gives the same output. run-tests PASS, 7 of 7
IDENTICAL at callrel 0.

## Why not in the batch yet

The run-time encoder lives in cv8t.4, so every tag-2 image carries it - the
smallest's image 6,990 -> 7,390 bytes, ~400 bytes, at callrel 0 too. It must go
to an overlay of its own, loaded for callrel designs only (one more dump
variant), CALL, reaching it through a cell the converter writes. Then the 167
designs swept at 0 and 2, the far benchmark timed at both, and 1 if the
converter learns to place calls by distance.
