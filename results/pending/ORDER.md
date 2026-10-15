# The after-seed-51 batch - apply in this order (against master after Iteration 298)

| # | patch | what it does |
|---|---|---|
| 1 | alignhot-after-seed51.patch | The gene alignhot (late; off, 32:11, 32, 64; Iteration 298): GCC's -falign-jumps, -falign-labels and -falign-functions - a computed goto's target, or a tail engine's function, on a fetch window's start; 32:11 aligns only where it costs at most 10 bytes. The laptop's counters put the evolved interpreted designs' front end at half their cycles on compute work (results/counters-amd-ryzen-7-pro-8840hs.md), and align1 and alignfn only take alignment away. GCC only; not with align1 or alignfn - on seed 50's front clang 28, align1 116, alignfn 124 (GCC-built: 159), either 139: 20 of 187 could take it. The engine: s6 +1,280 bytes at 32:11, +5,216 at 32, +12,192 at 64; 658ed9b9f8 +1,216, +4,448, +10,976. |

    git apply results/pending/alignhot-after-seed51.patch

Patch 1, tested on master at Iteration 298 in a scratch tree: the build; engines-check PASS, 52
paths - five more: aligned to 32:11, 32, 64, 64 with the cached top off, 64 with tail calls;
run-tests PASS; gene-equiv.py against HEAD - every recorded design's id and expression the same
(3,235), every made genome different (a new gene's key); the gate with alignhot at 64 on seed
50's front: 20 of 20 alive, the other 167 unable to express it. It applies on a fresh clone of
master after Iteration 298 and reproduces the tested files.
