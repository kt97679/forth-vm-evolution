# Evolution on the Ryzen 7 PRO 8840HS - seed 3

The third run, with the genes of Iterations 7-9: fused tests before a
branch (`0=`, `<`, `=`, `U<` - eight format-10 opcodes; at run time with
`rtfuse`) and three compiler flags (`peel`, `ipaclone`, `tracer`).
`--pop 32 --gens 40 --rounds 3 --seed 3`; begun at 213b53c, where it froze
the laptop in generation 1 (Iteration 10: a design looping through FORK);
resumed from its database at 3eaa9ec, engines jailed and scale-0 reach
designs declined unrun. Then `--remeasure 6`. 1,310 designs, 1,174 alive.
Speed: CPU time over hand-made s6's, paired, geometric mean over kernel,
fib, parse, corpus; loop held out. Every figure measured.

## The Pareto front

| design | speed | re-measured | size | loop (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| 8dd8a7a146 | 0.596 | 0.595 | 13464 | 0.727 | nocrossjump=1; nocet=1; bytehdr=0; guard=1; 13 pairs: DUP >R, >R DUP, C! R>, >R C!, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8; escape=1; msc=1 | crossover; mutation: bytehdr=0 |
| 60753a0eb0 | 0.606 | 0.622 | 9785 | 0.719 | nocrossjump=1; nocet=1; noreorder=1; guard=1; 13 pairs: DUP >R, >R DUP, C! R>, >R C!, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8; escape=1; msc=1 | mutation: noreorder=1 |
| f4a6dd9a13 | 0.647 | 0.683 | 9761 | 0.752 | nocet=1; spec=loc,tiny,small,imm; guard=1; 13 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,?DUP; escape=1; msc=1 | crossover; borrowed tail+tos from 27fe368264; mutation: trac |
| 550df563ee | 0.678 | 0.696 | 9745 | 0.809 | nocrossjump=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; 13 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,?DUP,J,(LOOP),U<?BRANCH8,UNLOOP,(?DO); escape=1; msc=1 | crossover; mutation: nocrossjump=1 |

## How the front came about

- `8dd8a7a146`: from mutation: msc=1, then mutation: tracer=1 / crossover; mutation: guard=1 / mutation: nocet=1 / mutation: tail=1, +super >R DUP / mutation: nocrossjump=1 / mutation: rtfuse=0, scale=3 / borrowed folds from 8a36a3210f; mutation: d256=1 / crossover; mutation: bytehdr=0
- `60753a0eb0`: from mutation: msc=1, then mutation: tracer=1 / crossover; mutation: guard=1 / mutation: nocet=1 / mutation: tail=1, +super >R DUP / mutation: nocrossjump=1 / mutation: rtfuse=0, scale=3 / borrowed folds from 8a36a3210f; mutation: d256=1 / mutation: noreorder=1
- `f4a6dd9a13`: from founder: s6-cv8b + escape, 7 words, 24 pairs, then crossover; mutation: varslot=0 / mutation: peel=1 / mutation: nocet=1 / mutation: peel=0, guard=1 / crossover; mutation: sharedcall=0 / crossover; mutation: sharedcall=1 / crossover; borrowed tail+tos from 27fe368264; mutation: tracer=0, scal
- `550df563ee`: from crossover; mutation: +fold @, then mutation: nocrossjump=1, tracer=1 / crossover; mutation: (none) / mutation: d256=0 / crossover; mutation: +super DROP DUP, tracer=0 / borrowed tail from 74a2747299; mutation: ipaclone=1 / crossover; mutation: nocet=0 / mutation: tail=1, tracer=1 / crossover; mutation: nocrossjump=1

## Three seeds, re-measured

| | seed 1 | seed 2 | seed 3 (new genes) |
|---|---|---|---|
| fastest, about 13.5 KB | 0.609 at 13,480 | 0.619 at 13,472 | **0.595** at 13,464 |
| near 9.8 KB | 0.649 at 9,801 | 0.667 at 9,761 | **0.622** at 9,785 |
| | 0.705 at 9,761 | 0.725 at 9,769 | **0.683** at 9,761 |
| smallest | | | 0.696 at 9,745 |

**What selection chose.** Every design on the front carries all eight
fused-test opcodes - and they take their slots before the pairs, so the
pairs fell from 21-24 to 13: the tests are worth more per slot than the
marginal pairs. Yet the front moved: 2-4% at the fast end, 4-7% at the
small end, same sizes. The run-time overlay (`rtfuse`) was not chosen -
its 620 bytes for fib's 10% lost. Of the flag genes, `ipaclone` and
`tracer` sit on one design (550df563ee), `peel` on none.

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.240 | 25144 | no |
| s1-sod16 | 1.549 | 16304 | no |
| s2-cpt16 | 1.226 | 15384 | no |
| s3-cpt16f | 1.169 | 15200 | no |
| s4-cv8 | 1.161 | 14152 | no |
| s5-cv8spec | 0.930 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths, audited

136. 129 declined unrun - two-byte-only forms at scale 0 (`reach_lethal`,
Iteration 10). The other 7, all in generation 1, ran before the freeze
under the old code: 6 are that same reach limit - among them 8cfd49f24c,
the fork bomb, recorded as "died: corpus" - and 1 the converter's
alignment refusal (cpt16, scale 3). After the resume, nothing else died.
All 1,310 ids recompute identically.
