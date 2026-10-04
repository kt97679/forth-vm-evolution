# Evolution on the Ryzen 7 PRO 8840HS - seed 4

The fourth run, with what came after seed 3: the body-check fix (Iteration
13 - a format-10 word a design carries is now really in it), the second
escape level (Iteration 11), five more tests fused with their branch
(Iteration 12), and one-byte calls (`hotcalls`, Iteration 14).
`--pop 32 --gens 40 --rounds 3 --seed 4` at eef54661 (Iteration 18), run by
`lab/evolve/next-run.sh` on 2026-10-04 in 37 minutes, then `--remeasure 6`.
1,310 designs, 1,188 alive (database sha256 fc553d0a7ebd5e86...). Speed:
CPU time over hand-made s6's, paired, geometric mean over kernel, fib,
parse, corpus; loop held out. Every figure measured.

## The calibration, first

Hand-made s6 measured against itself, inside the run: **1.038** - fib
1.117. Seed 3's was 0.986 - kernel 0.926. A single run on this laptop
carries several per cent of noise per workload, and selection picks the
designs whose draws were luckiest: the re-measure took 1-24% off the
selected front's figures (seed 3: 0-6%), and four of its eleven designs
were dominated once measured again. Quote the re-measured column.
Differences between seeds of a few per cent are not established by runs
made in different sessions - see the end.

## The Pareto front, as selected

| design | speed | re-measured | size | loop (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| 12d8e18511 | 0.536 | 0.667 | 13360 | 0.897 | nocet=1; ipaclone=1; bytehdr=0; guard=1; 17 pairs: DUP >R, C! R>, R@ ROT, DUP C@, ...; rtfuse=0; ops10=EXECUTE,I,+!,?DUP,<?BRANCH8,UNLOOP,J,(LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,=?BRANCH,=?BRANCH8,U<?BRANCH,<>?BRANCH,<>?BRANCH8,>?BRANCH,0<?BRANCH8,=I?BRANCH8,>?BRANCH8,0<?BRANCH,(?DO),=I?BRANCH; escape=2; msc=1 | crossover; borrowed folds+supers from 05158c8ac9; mutation:  |
| 29ad5ba726 | 0.562 | 0.589 | 13352 | 0.778 | nocet=1; bytehdr=0; guard=1; 17 pairs: DUP >R, C! R>, >R C!, R@ ROT, ...; rtfuse=0; ops10=EXECUTE,I,+!,?DUP,<?BRANCH8,UNLOOP,J,(LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,(DO),=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,0<?BRANCH8,=I?BRANCH8,>?BRANCH8,0<?BRANCH; escape=2; msc=1 | mutation: ipaclone=0 |
| 14f6036a4b | 0.571 | 0.627 | 13217 | 0.883 | nocet=1; noreorder=1; peel=1; bytehdr=0; varslot=0; guard=1; -LSHIFT; 17 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,+!,?DUP,<?BRANCH8,UNLOOP,J,(LOOP),(?DO),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,(DO),=?BRANCH,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=2; msc=1; hotcalls=32 | mutation: bytehdr=0 |
| 1769ca2a48 | 0.589 | 0.603 | 13209 | 0.863 | nocet=1; noreorder=1; bytehdr=0; varslot=0; guard=1; -LIT; 7 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,+!,?DUP,<?BRANCH8,UNLOOP,J,(LOOP),(?DO),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,(DO),=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=1; msc=1; hotcalls=32 | mutation: bytehdr=0 |
| e0cbf09bc2 | 0.594 | 0.666 | 13057 | 0.896 | nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; bytehdr=0; spec=loc,tiny,small,imm; -U<; 8 pairs: DUP >R, C! R>, R@ ROT, DUP C@, ...; rtfuse=0; ops10=EXECUTE,I,+!,?DUP,<?BRANCH8,UNLOOP,J,(LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,(DO),=?BRANCH,U<?BRANCH,<>?BRANCH,<>?BRANCH8,>?BRANCH,0<?BRANCH,0<?BRANCH8,=I?BRANCH,>?BRANCH8,(+LOOP),U<?BRANCH8,=I?BRANCH8; escape=1; msc=1; hotcalls=32 | mutation: -fold U< |
| 90018981c6 | 0.595 | 0.696 | 9678 | 0.922 | align1=1; noreorder=1; guard=1; 6 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,+!,?DUP,<?BRANCH8,UNLOOP,J,(LOOP),(?DO),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,(DO),=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=1; msc=1 | mutation: +op <?BRANCH8 |
| 6463752a82 | 0.630 | 0.669 | 9523 | 0.891 | nocet=1; peel=1; varslot=0; guard=1; -ROT; 18 pairs: DUP >R, C! R>, R@ ROT, DUP C@, ...; rtfuse=0; ops10=EXECUTE,I,?DUP,UNLOOP,J,(LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,(DO),=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,0<?BRANCH8,=I?BRANCH8,>?BRANCH8,0<?BRANCH,(?DO),=I?BRANCH; escape=2; msc=1; hotcalls=16 | mutation: scale=2, noreorder=0 |
| 38d91795a2 | 0.641 | 0.678 | 9474 | 0.884 | nocet=1; noreorder=1; varslot=0; guard=1; -LIT; 7 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,+!,?DUP,<?BRANCH8,UNLOOP,J,(LOOP),(?DO),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,(DO),=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=1; msc=1; hotcalls=32 | mutation: peel=0 |
| 7fe7f039bd | 0.649 | 0.702 | 9450 | 0.826 | nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tracer=1; guard=1; -R@; 8 pairs: DUP >R, DUP C@, OVER C@, C@ =, ...; rtfuse=0; ops10=EXECUTE,I,+!,?DUP,UNLOOP,(LOOP),(?DO),(LEAVE),?BRANCH8,?NBRANCH,?NBRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH,=I?BRANCH,(DO),(+LOOP),<?BRANCH8,BRANCH8,<?BRANCH,0<?BRANCH8,<>?BRANCH8,=?BRANCH,=I?BRANCH8; escape=1; msc=1; hotcalls=32 | crossover; mutation: tracer=1 |
| 672538daf5 | 0.654 | 0.780 | 9351 | 1.000 | opt=O3; nocrossjump=1; noreorder=1; peel=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; 7 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,+!,?DUP,J,U<?BRANCH,(?DO),(+LOOP),(LEAVE),?BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH8,>?BRANCH8,0<?BRANCH,0<?BRANCH8,(DO),UNLOOP,BRANCH8,>?BRANCH,=I?BRANCH,(LOOP),<>?BRANCH8; escape=1; msc=1; hotcalls=32 | crossover; borrowed ops10+supers from 75371dd980; mutation:  |
| 3453246bdf | 0.684 | 0.727 | 9335 | 0.882 | nocrossjump=1; nocet=1; align1=1; peel=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -NEGATE -RSHIFT; 8 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,UNLOOP,J,(?DO),(+LOOP),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8,(LOOP),?DUP; escape=1; msc=1; hotcalls=32 | borrowed folds from 98663b1620; mutation: -fold NEGATE |

### How it came about

- `12d8e18511`: from crossover; mutation: align1=0, then crossover; mutation: noreorder=1 / crossover; borrowed ops10+supers from 5dbd753782; mutation: op <?BRANC / mutation: +op <?BRANCH8 / crossover; mutation: align1=0, scale=3 / crossover; mutation: tail=1 / crossover; mutation: escape=2 / mutation: ipaclone=0 / crossover; borrowed folds+supers from 05158c8ac9; mutation: ipaclone=1
- `29ad5ba726`: from crossover; mutation: align1=1, then crossover; mutation: align1=0 / crossover; mutation: noreorder=1 / crossover; borrowed ops10+supers from 5dbd753782; mutation: op <?BRANC / mutation: +op <?BRANCH8 / crossover; mutation: align1=0, scale=3 / crossover; mutation: tail=1 / crossover; mutation: escape=2 / mutation: ipaclone=0
- `14f6036a4b`: from borrowed msc+tail from 653f59f04b; mutation: +super ROT R>, then mutation: nocrossjump=1 / crossover; borrowed supers from 8004aff064; mutation: d256=1, hotcalls / mutation: peel=0 / crossover; mutation: peel=1 / borrowed ops10 from 90018981c6; mutation: -fold LIT / crossover; mutation: peel=1 / mutation: varslot=0 / mutation: bytehdr=0
- `1769ca2a48`: from crossover; mutation: noreorder=1, then borrowed msc+tail from 653f59f04b; mutation: +super ROT R> / mutation: nocrossjump=1 / crossover; borrowed supers from 8004aff064; mutation: d256=1, hotcalls / mutation: peel=0 / crossover; mutation: peel=1 / borrowed ops10 from 90018981c6; mutation: -fold LIT / mutation: peel=0 / mutation: bytehdr=0
- `e0cbf09bc2`: from crossover; mutation: noreorder=1, then crossover; borrowed ops10+supers from 5dbd753782; mutation: op <?BRANC / mutation: +op <?BRANCH8 / crossover; mutation: align1=0, scale=3 / crossover; mutation: -super OVER R>, ipaclone=1 / crossover; mutation: (none) / mutation: noreorder=1 / crossover; mutation: guard=0 / mutation: -fold U<
- `90018981c6`: from hand-made s5-cv8spec, then crossover; mutation: -op (DO), guard=1 / crossover; mutation: align1=1 / crossover; mutation: align1=0 / crossover; mutation: noreorder=1 / crossover; borrowed ops10+supers from 5dbd753782; mutation: op <?BRANC / mutation: +op <?BRANCH8
- `6463752a82`: from crossover; mutation: noreorder=1, then crossover; borrowed ops10+supers from 5dbd753782; mutation: op <?BRANC / mutation: +op <?BRANCH8 / crossover; mutation: align1=0, scale=3 / crossover; mutation: tail=1 / crossover; mutation: escape=2 / crossover; mutation: hotcalls=16 / crossover; mutation: sharedcall=0 / mutation: scale=2, noreorder=0
- `38d91795a2`: from crossover; mutation: align1=0, then crossover; mutation: noreorder=1 / borrowed msc+tail from 653f59f04b; mutation: +super ROT R> / mutation: nocrossjump=1 / crossover; borrowed supers from 8004aff064; mutation: d256=1, hotcalls / mutation: peel=0 / crossover; mutation: peel=1 / borrowed ops10 from 90018981c6; mutation: -fold LIT / mutation: peel=0
- `7fe7f039bd`: from crossover; mutation: noreorder=1, scale=3, then crossover; borrowed folds+supers from d30e4f1a25; mutation: noreorder= / crossover; mutation: peel=1 / mutation: hotcalls=32 / mutation: peel=0, op 0<?BRANCH8->=?BRANCH8 / crossover / crossover; mutation: super C@ DUP->@ < / crossover / crossover; mutation: tracer=1
- `672538daf5`: from crossover; mutation: d256=1, then mutation: hotcalls=32 / crossover; borrowed tail from 5eadd40f8f; mutation: rtfuse=0 / crossover; mutation: varslot=0 / crossover; mutation: hotcalls=16 / mutation: tail=1, hotcalls=32 / crossover / crossover; mutation: sharedcall=0, tracer=1 / crossover; borrowed ops10+supers from 75371dd980; mutation: tracer=1, 
- `3453246bdf`: from mutation: nocrossjump=1, then crossover; borrowed supers from 8004aff064; mutation: d256=1, hotcalls / mutation: peel=0 / crossover; mutation: peel=1 / borrowed ops10 from 90018981c6; mutation: -fold LIT / crossover; mutation: nocrossjump=1 / mutation: noreorder=0 / crossover; borrowed ops10 from 2f9481e1e9; mutation: d256=0 / borrowed folds from 98663b1620; mutation: -fold NEGATE


## The front, re-measured

Six rounds each. Of the eleven, these seven are not dominated:

| design | re-measured | size | loop (held out) | one-byte calls | escape | headers | pairs | format-10 | of them Iteration 12 tests | restored at 13 |
|---|---|---|---|---|---|---|---|---|---|---|
| 29ad5ba726 | 0.589 | 13,352 | 0.813 | - | 2 | cell | 17 | 26 | 7 | (LOOP) ?DUP (DO) |
| 1769ca2a48 | 0.603 | 13,209 | 0.890 | 32 | 1 | cell | 7 | 28 | 8 | (LOOP) (?DO) ?DUP (DO) |
| e0cbf09bc2 | 0.666 | 13,057 | 0.939 | 32 | 1 | cell | 8 | 27 | 8 | (LOOP) (+LOOP) ?DUP (DO) |
| 6463752a82 | 0.669 | 9,523 | 0.906 | 16 | 2 | byte | 18 | 26 | 8 | (LOOP) (?DO) ?DUP (DO) |
| 38d91795a2 | 0.678 | 9,474 | 0.876 | 32 | 1 | byte | 7 | 28 | 8 | (LOOP) (?DO) ?DUP (DO) |
| 7fe7f039bd | 0.702 | 9,450 | 0.871 | 32 | 1 | byte | 8 | 27 | 8 | (LOOP) (?DO) (+LOOP) ?DUP (DO) |
| 3453246bdf | 0.727 | 9,335 | 0.851 | 32 | 1 | byte | 8 | 28 | 8 | (LOOP) (?DO) (+LOOP) ?DUP (DO) |

The loop column moves with the image's size mod 8 (alignment NOOPs in code
compiled at run time, Iteration 13): compare it only at equal size mod 8.

## Four seeds, re-measured

| | seed 1 | seed 2 | seed 3 | seed 4 (new genes) |
|---|---|---|---|---|
| fastest, about 13.4 KB | 0.609 at 13,480 | 0.619 at 13,472 | 0.595 at 13,464 | **0.589** at 13,352 |
| | | | | 0.603 at 13,209 |
| near 9.5-9.8 KB | 0.649 at 9,801 | 0.667 at 9,761 | **0.622** at 9,785 | 0.669 at 9,523 |
| | 0.705 at 9,761 | 0.725 at 9,769 | 0.683 at 9,761 | 0.678 at 9,474 |
| smallest | | | 0.696 at 9,745 | 0.727 at **9,335** |

**What selection chose.** One-byte calls: six of the seven, five with 32
targets - and 56% of the 1,152 living CV8 designs (32 targets 332, 16 185, 8
130). Every front design has multi-state caching, seven or eight of
Iteration 12's eight test opcodes (95% of the living have one at least),
and the words restored at Iteration 13: `(LOOP)`, `?DUP` and `(DO)` on all
seven, `(?DO)` on five. Format-10 opcodes now take 26-28 slots, so the pairs
fell to 7-8 - except on the two designs with the second escape level,
which hold 17 and 18: Iteration 11 found its nine slots worthless filled
with the next pairs alone, and selection found them worth having all the
same - the fastest design has them, and no one-byte calls.

**What moved.** The fast end: 1% faster, inside the noise, and 112 bytes
smaller - what the body-check fix gives that layout. The small end: 262-410
bytes smaller - one-byte calls - and 7.5% slower than seed 3's best small
design (0.669 against 0.622). That gap is larger than either run's own
calibration error, but the two were measured in different sessions with
calibrations of 0.986 and 1.038, and the kinds of design differ: so it is
open, not found - both fronts measured in one session decide it (GOALS.md).

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.145 | 25144 | no |
| s1-sod16 | 1.491 | 16304 | no |
| s2-cpt16 | 1.133 | 15384 | no |
| s3-cpt16f | 1.141 | 15200 | no |
| s4-cv8 | 1.106 | 14152 | no |
| s5-cv8spec | 0.908 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths, audited

122. 121 declined unrun - two-byte-only forms at scale 0 (`reach_lethal`,
Iteration 10). 1 timed out: 4a1c0107e4, scale 1 with near DOES> calls -
rebuilt on the development VM it times out as recorded, lives with
`doesfar=1` alone and not with tail calls off alone: the scale-1 reach
limit (SCAN.md), nothing new. None died on the body check, fatal since
Iteration 13: every living design has every word it carries.

## The laptop's later benchmark sweep

`next-run.sh` found results/ changed and sent it back: the stage tables and
SPN figures of a sweep at 02:48-02:51 UTC on 2026-09-30, eighteen minutes
after the one recorded (02:30-02:33), same kernel, load 1.09 against 2.76.
It agrees with the recorded sweep within error bars on kernel, corpus and
parse; on fib its bars doubled (+-0.077 against +-0.035). A repeat, not a
change: nothing re-recorded (prompts/09).
