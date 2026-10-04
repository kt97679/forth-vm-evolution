# Evolution on the Ryzen 7 PRO 8840HS - seed 4 again: a replicate

Not planned - `next-run.sh` with no argument meant seed 4, and after
Iteration 21's pull it began a fresh one - but an experiment the project
had not run: the SAME seed and the SAME measured code as seed 4 (the
engine, converter, kernel sources, workloads and evolver are identical
between eef54661 and b9d06884; only documents and scripts changed), with
only the timing noise different. `--pop 32 --gens 40 --rounds 3 --seed 4`
at b9d06884 (Iteration 21), 2026-10-04, 38 minutes, then `--remeasure 6`.
1,310 designs, 1,143 alive (database sha256 9fc3995f149e3017...).

## What a run owes to its seed, and what to its noise

- **The trajectory is chaotic.** The two runs evaluated the same first 35
  designs - the starting population, drawn from the seed before anything is
  timed - and after that only 2 more of their 1,310: the noise picks other
  parents, and the runs never meet again.
- **The noise per design is about 3%.** The 34 designs timed in both: this
  run over the first, median 0.998, 10-90% 0.967-1.025. Sizes identical.
- **The outcome converged anyway.** One-byte calls with 32 targets on every
  design of the re-measured front (the first: six of seven); multi-state
  caching on all; the same smallest size, 9,335 bytes, reached by another
  design. Where the runs drifted apart: the second escape level, on four of
  six front designs here (the first: two of seven) and 54% of the living
  (22%), the slots it frees holding 14-15 pairs; tail calls on 7% of the
  living (39%).
- **This run was calibrated well**: hand-made s6 against itself 1.004, fib
  1.020 (the first: 1.038, fib 1.117) - and the re-measure took 0-7% off the
  selected front (the first: 2-20%). The less noise, the less luck selection
  can pick up.

Its figures cannot be ranked against the first run's: different sessions
(Iteration 21). `next-run.sh compare` ranks them in one.

## The Pareto front, as selected

| design | speed | re-measured | size | loop (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| e99da68667 | 0.547 | 0.581 | 13201 | 1.018 | opt=O3; nocet=1; align1=1; peel=1; ipaclone=1; scale=3; bytehdr=0; spec=var,tiny,small,imm; guard=1; 15 pairs: DUP >R, R@ ROT, DUP C@, >R OVER, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,UNLOOP,J,(LOOP),(?DO),(+LOOP),?BRANCH8,BRANCH8,?NBRANCH,<?BRANCH,<?BRANCH8,=?BRANCH,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,?NBRANCH8,(LEAVE),=I?BRANCH8,=?BRANCH8; escape=2; msc=1; hotcalls=32 | mutation: ipaclone=1, scale=3 |
| 4cb3fa9172 | 0.593 | 0.626 | 13073 | 0.953 | opt=O3; nocet=1; align1=1; noreorder=1; peel=1; bytehdr=0; spec=tiny,small,imm; guard=1; 15 pairs: DUP >R, R@ ROT, DUP C@, >R OVER, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,UNLOOP,J,(LOOP),(?DO),(+LOOP),?BRANCH8,BRANCH8,?NBRANCH,<?BRANCH,<?BRANCH8,=?BRANCH,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,?NBRANCH8,(LEAVE),=I?BRANCH8,=?BRANCH8; escape=2; msc=1; hotcalls=32 | crossover; mutation: sharedcall=0, -spec var |
| 84e302c470 | 0.614 | 0.657 | 13065 | 0.994 | opt=O3; nocet=1; align1=1; peel=1; tracer=1; bytehdr=0; spec=tiny,small,imm; guard=1; 15 pairs: DUP >R, R@ ROT, DUP C@, >R OVER, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,UNLOOP,J,(LOOP),(?DO),(+LOOP),?BRANCH8,BRANCH8,?NBRANCH,<?BRANCH,<?BRANCH8,=?BRANCH,U<?BRANCH,U<?BRANCH8,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,?NBRANCH8,(LEAVE),=I?BRANCH8,=?BRANCH8,?DUP; escape=2; msc=1; hotcalls=32 | crossover; mutation: sharedcall=0 |
| 66eb4a8f15 | 0.626 | 0.641 | 13057 | 0.907 | opt=O3; nocet=1; align1=1; peel=1; bytehdr=0; spec=loc,tiny,small,imm; varslot=0; guard=1; 6 pairs: DUP >R, R@ ROT, DUP C@, >R OVER, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,UNLOOP,J,(LOOP),(?DO),(+LOOP),?BRANCH8,BRANCH8,?NBRANCH,<?BRANCH,<?BRANCH8,=?BRANCH,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH8,=I?BRANCH,?NBRANCH8,(LEAVE),=I?BRANCH8,=?BRANCH8,?DUP; escape=1; msc=1; hotcalls=32 | crossover; mutation: +spec loc |
| e8f1dd3ca2 | 0.646 | 0.678 | 9458 | 0.991 | opt=O3; nocet=1; align1=1; peel=1; spec=var,tiny,small,imm; guard=1; 15 pairs: DUP >R, R@ ROT, DUP C@, >R OVER, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,UNLOOP,J,(LOOP),(?DO),(+LOOP),?BRANCH8,BRANCH8,?NBRANCH,<?BRANCH,<?BRANCH8,=?BRANCH,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,?NBRANCH8,(LEAVE),=I?BRANCH8,=?BRANCH8; escape=2; msc=1; hotcalls=32 | borrowed tail+tos from 1c6561b9ac; mutation: bytehdr=1 |
| c297551359 | 0.667 | 0.682 | 9450 | 0.813 | nocrossjump=1; nocet=1; align1=1; ipaclone=1; tracer=1; spec=var,tiny,small,imm; guard=1; 6 pairs: DUP >R, R@ ROT, DUP C@, >R OVER, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,UNLOOP,J,(LOOP),(?DO),(+LOOP),?BRANCH8,BRANCH8,?NBRANCH,<?BRANCH,<?BRANCH8,=?BRANCH,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,=I?BRANCH,?NBRANCH8,(LEAVE),=I?BRANCH8,=?BRANCH8,?DUP; escape=1; msc=1; hotcalls=32 | crossover; borrowed tail from 5c7ad2f6f1; mutation: ipaclone |
| 05dcc81cdc | 0.686 | 0.688 | 9335 | 0.949 | nocrossjump=1; nocet=1; align1=1; peel=1; ipaclone=1; tracer=1; spec=tiny,small,imm; varslot=0; guard=1; 14 pairs: DUP >R, DUP C@, >R OVER, C! R>, ...; rtfuse=0; ops10=EXECUTE,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),?NBRANCH,<?BRANCH8,=?BRANCH,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,?BRANCH8,?NBRANCH8,(LEAVE),=I?BRANCH8,=?BRANCH8,I,BRANCH8,<?BRANCH; escape=2; msc=1; hotcalls=32 | crossover; mutation: +op ?BRANCH8, ipaclone=1 |

### How it came about

- `e99da68667`: from crossover; mutation: -spec loc, nogcse=0, then mutation: nocet=1, guard=1 / borrowed tail from b3e94c2397; mutation: peel=1 / borrowed tail+tos from 680401e2be; mutation: bytehdr=0 / mutation: tracer=1 / mutation: -O3, align1=1 / crossover; borrowed msc from 2bd2055677 / borrowed skippad+fold from 71840b8c6a; mutation: noreorder=0 / mutation: ipaclone=1, scale=3
- `4cb3fa9172`: from crossover; mutation: hotcalls=16, then crossover; mutation: -spec loc, nogcse=0 / mutation: nocet=1, guard=1 / borrowed tail from b3e94c2397; mutation: peel=1 / borrowed tail+tos from 680401e2be; mutation: bytehdr=0 / mutation: tracer=1 / mutation: -O3, align1=1 / crossover; borrowed msc from 2bd2055677 / crossover; mutation: sharedcall=0, -spec var
- `84e302c470`: from mutation: nocet=1, guard=1, then borrowed tail from b3e94c2397; mutation: peel=1 / borrowed tail+tos from 680401e2be; mutation: bytehdr=0 / mutation: tracer=1 / mutation: -O3, align1=1 / crossover; borrowed msc from 2bd2055677 / borrowed skippad+fold from 71840b8c6a; mutation: noreorder=0 / borrowed tail+tos from 1c6561b9ac; mutation: bytehdr=1 / crossover; mutation: sharedcall=0
- `66eb4a8f15`: from crossover; mutation: -spec loc, nogcse=0, then mutation: nocet=1, guard=1 / borrowed tail from b3e94c2397; mutation: peel=1 / borrowed tail+tos from 680401e2be; mutation: bytehdr=0 / mutation: tracer=1 / mutation: -O3, align1=1 / crossover; borrowed msc from 2bd2055677 / borrowed skippad+fold from 71840b8c6a; mutation: noreorder=0 / crossover; mutation: +spec loc
- `e8f1dd3ca2`: from crossover; mutation: -spec loc, nogcse=0, then mutation: nocet=1, guard=1 / borrowed tail from b3e94c2397; mutation: peel=1 / borrowed tail+tos from 680401e2be; mutation: bytehdr=0 / mutation: tracer=1 / mutation: -O3, align1=1 / crossover; borrowed msc from 2bd2055677 / borrowed skippad+fold from 71840b8c6a; mutation: noreorder=0 / borrowed tail+tos from 1c6561b9ac; mutation: bytehdr=1
- `c297551359`: from mutation: nocet=1, guard=1, then borrowed tail from b3e94c2397; mutation: peel=1 / borrowed tail+tos from 680401e2be; mutation: bytehdr=0 / mutation: tracer=1 / mutation: -O3, align1=1 / crossover; borrowed msc from 2bd2055677 / borrowed skippad+fold from 71840b8c6a; mutation: noreorder=0 / borrowed tail+tos from 1c6561b9ac; mutation: bytehdr=1 / crossover; borrowed tail from 5c7ad2f6f1; mutation: ipaclone=1
- `05dcc81cdc`: from crossover; mutation: msc=1, then crossover; mutation: +super C! R> / crossover; mutation: hotcalls=16 / crossover; mutation: -spec loc, nogcse=0 / crossover; mutation: -op ?BRANCH8 / crossover; mutation: hotcalls=0, guard=1 / crossover; borrowed opt+nogcse+nocrossjump+nocet+align1+noreorder+peel / mutation: nocrossjump=1 / crossover; mutation: +op ?BRANCH8, ipaclone=1


## The front, re-measured

| design | re-measured | size | loop (held out) | one-byte calls | escape | headers | pairs | format-10 |
|---|---|---|---|---|---|---|---|---|
| e99da68667 | 0.581 | 13,201 | 1.044 | 32 | 2 | cell | 15 | 28 |
| 4cb3fa9172 | 0.626 | 13,073 | 0.973 | 32 | 2 | cell | 15 | 28 |
| 66eb4a8f15 | 0.641 | 13,057 | 0.916 | 32 | 1 | cell | 6 | 28 |
| e8f1dd3ca2 | 0.678 | 9,458 | 0.951 | 32 | 2 | byte | 15 | 28 |
| c297551359 | 0.682 | 9,450 | 0.815 | 32 | 1 | byte | 6 | 28 |
| 05dcc81cdc | 0.688 | 9,335 | 0.925 | 32 | 2 | byte | 14 | 29 |

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.199 | 25144 | no |
| s1-sod16 | 1.513 | 16304 | no |
| s2-cpt16 | 1.213 | 15384 | no |
| s3-cpt16f | 1.162 | 15200 | no |
| s4-cv8 | 1.124 | 14152 | no |
| s5-cv8spec | 0.915 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths, audited

129: 128 declined unrun (two-byte-only forms at scale 0); 1 - d40ff02637,
scale 1 with near DOES> calls - timed out on the laptop; rebuilt on the
development VM it gives the kernel workload wrong output instead, and lives
with `doesfar=1` alone: the scale-1 reach limit again, the symptom
whatever the overflowed call lands on.
