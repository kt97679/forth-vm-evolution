# The after-seed-51 batch - apply in this order (against master after Iteration 299)

| # | patch | what it does |
|---|---|---|
| 1 | alignhot-after-seed51.patch | The gene alignhot (late; off, 32:11, 32, 64; Iteration 298): GCC's -falign-jumps, -falign-labels and -falign-functions - a computed goto's target, or a tail engine's function, on a fetch window's start; 32:11 aligns only where it costs at most 10 bytes. The laptop's counters put the evolved interpreted designs' front end at half their cycles on compute work (results/counters-amd-ryzen-7-pro-8840hs.md), and align1 and alignfn only take alignment away. GCC only; not with align1 or alignfn - on seed 50's front clang 28, align1 116, alignfn 124 (GCC-built: 159), either 139: 20 of 187 could take it. The engine: s6 +1,280 bytes at 32:11, +5,216 at 32, +12,192 at 64; 658ed9b9f8 +1,216, +4,448, +10,976. |
| 2 | cmpops-after-seed51.patch | > and 0= as opcodes (Iteration 299): pool words and in opbody's list, so opinline compiles them into code compiled at run time - handlers L_x_gt and L_x_zeq for the plain, cached-top and multi-state engines (the engine's L_gt is <, its name historical); their kernel bodies, SWAP < and 0 =, were in sod16.py's table already; the JIT translates both (GT; LIT and EQ). Found by source audit 3 (results/source-audit-3.md): on seed 50's fastest design without the JIT, > 11.7% of bubble's dispatches, 0= 7.7% of ackermann's. Measured on 658ed9b9f8 with them first, opbody and opinline: bubble -11.7%, ackermann -7.7%; its slots full, the kernel +5.5% and the corpus +8.7% for the words they pushed out - evolution places them. |

    git apply results/pending/alignhot-after-seed51.patch
    git apply results/pending/cmpops-after-seed51.patch

Patch 1, tested on master at Iteration 298 in a scratch tree: the build; engines-check PASS, 52
paths - five more: aligned to 32:11, 32, 64, 64 with the cached top off, 64 with tail calls;
run-tests PASS; gene-equiv.py against HEAD - every recorded design's id and expression the same
(3,235), every made genome different (a new gene's key); the gate with alignhot at 64 on seed
50's front: 20 of 20 alive, the other 167 unable to express it. It applies on a fresh clone of
master after Iteration 298 and reproduces the tested files.

Patch 2, tested on patch 1 in a scratch tree (Iteration 299): the build; engines-check PASS, 57
paths - five more: s6, the cached top off, multi-state, tail calls, the JIT, each with > and
0= first, opbody and opinline; run-tests PASS; gene-equiv.py against patch 1 - every recorded
design's id and expression the same (3,235), and, as a longer pool must, 244 of 1,000 random
genomes and 2 of 3,000 mutations different; word-cost.py as above; the gate with > and 0=
first, opbody and opinline on seed 50's front: 187 of 187 alive, every one expressing them.
Patches 1 and 2 apply in turn on a fresh clone of master after Iteration 299 and reproduce the
tested files.
