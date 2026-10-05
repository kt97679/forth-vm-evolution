# Seed 6 on the AMD Ryzen 7 PRO 8840HS (Iteration 36)

The first run that could choose the tests that keep their value - DUP
?BRANCH, OVER ?BRANCH, DUP 0= ?BRANCH kept - and SWAP n + (Iterations 33-34).
Commit 34f3873c, `seed 6` from NEXT-RUN, pop 32 x 40 generations, 3 rounds,
selected by the median: 37 minutes, 1,309 designs, 1,193 alive. Its front,
measured again in one session with every earlier run's
(`results/compare-fronts-amd-ryzen-7-pro-8840hs.md`, session 4), is the
front of all runs: **0.547 at 14,081 bytes - the fastest yet - down to
0.685 at 9,327, the smallest yet**; 4-7% faster than the fastest earlier
design no larger at most sizes.

## The new opcodes, chosen

Three of the 29 designs of generation 0 had any of them. At the end:

| opcode | living designs with it (of 1,193) | on the front of all runs (of 10) |
|---|---|---|
| DUP?BRANCH | 847 (71%) | 10 |
| DUP?BRANCH8 | 697 (58%) | 8 |
| OVER?BRANCH | 837 (70%) | 9 |
| OVER?BRANCH8 | 735 (62%) | 5 |
| DUP?NBRANCH | 953 (80%) | 10 |
| DUP?NBRANCH8 | 869 (73%) | 9 |
| SWAP+I | 909 (76%) | 10 |

## What they do on seed 6's own front

`lab/evolve/image-ab.py 422d6bcbca c61857fc89 cd943ed219 --env
SOD16_TESTBR_SKIP=DUP,OVER,DUPN,SADDI --rounds 5`, on the development VM:
each design's own engine, its image with the fusions declined (A) and as
built (B). Dispatches are counted, the same on every machine; this VM's
times are noise at this size.

pinned to cpu 0 (it and its sibling 0% busy; BENCH_CPU=N to choose)
| design | size A | size B | B - A | dispatches B / A: kernel, fib, parse, corpus, loop | time B / A: kernel, fib, parse, corpus, loop | selection |
|---|---|---|---|---|---|---|
| 422d6bcbca | 9359 | 9327 | -32 | 0.915, 1.000, 0.911, 0.911, 1.000 | 1.028, 0.998, 0.922, 0.932, 1.006 | 0.969 |
| c61857fc89 | 10066 | 10034 | -32 | 0.905, 1.000, 0.901, 0.900, 1.000 | 0.878, 1.048, 0.942, 0.869, 1.036 | 0.932 |
| cd943ed219 | 14145 | 14081 | -64 | 0.907, 1.000, 0.904, 0.902, 1.000 | 1.069, 1.034, 0.889, 0.954, 1.015 | 0.984 |

**9-10% of the dispatches on kernel, parse and corpus, 32-64 bytes.** fib
and loop do not move: their hot code is compiled at run time, which the
converter's fusions do not reach.

## The run's report

# Evolved VM designs

1309 designs evaluated, 1193 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus,
relative to s6-cv8b; size is the self-hosting image. loop is held out.

## The Pareto front

| design | speed | re-measured | size | loop (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| cd943ed219 | 0.538 | 0.545 | 14081 | 0.782 | nocrossjump=1; nocet=1; ipaclone=1; tracer=1; bytehdr=0; guard=1; 9 pairs: DUP >R, C! R>, >R C!, >R OVER, ...; rtfuse=1; ops10=J,?BRANCH8,=?BRANCH8,SWAP+I,+!,BRANCH8,?NBRANCH,<?BRANCH,DUP?NBRANCH,<>?BRANCH,OVER?BRANCH8,>?BRANCH8,DUP?BRANCH,(LEAVE),?NBRANCH8,0<?BRANCH8,DUP?NBRANCH8,=I?BRANCH,EXECUTE,<?BRANCH8,=?BRANCH,DUP?BRANCH8,<>?BRANCH8,(?DO),OVER?BRANCH; escape=1; msc=1; hotcalls=16 | mutation: rtfuse=1 |
| 15dde12f04 | 0.561 | 0.567 | 13345 | 0.721 | nocrossjump=1; nocet=1; ipaclone=1; tracer=1; bytehdr=0; guard=1; 9 pairs: DUP >R, C! R>, >R C!, >R OVER, ...; rtfuse=0; ops10=J,?BRANCH8,=?BRANCH8,SWAP+I,+!,BRANCH8,?NBRANCH,<?BRANCH,DUP?NBRANCH,<>?BRANCH,OVER?BRANCH8,>?BRANCH8,DUP?BRANCH,(LEAVE),?NBRANCH8,0<?BRANCH8,DUP?NBRANCH8,=I?BRANCH,EXECUTE,<?BRANCH8,=?BRANCH,DUP?BRANCH8,<>?BRANCH8,(?DO),OVER?BRANCH; escape=1; msc=1; hotcalls=16 | crossover |
| dc02ceae31 | 0.565 | 0.560 | 13161 | 0.734 | opt=O3; nocrossjump=1; nocet=1; peel=1; ipaclone=1; scale=1; bytehdr=0; spec=loc,tiny,small,imm; guard=1; 18 pairs: DUP >R, >R OVER, SWAP R>, R> SWAP, ...; rtfuse=0; ops10=EXECUTE,J,(LEAVE),?BRANCH8,SWAP+I,+!,BRANCH8,?NBRANCH,<?BRANCH,=?BRANCH,DUP?BRANCH8,DUP?NBRANCH8,(LOOP),U<?BRANCH,DUP?NBRANCH,<>?BRANCH,<>?BRANCH8,0<?BRANCH,=I?BRANCH,=I?BRANCH8,?NBRANCH8,OVER?BRANCH,OVER?BRANCH8,DUP?BRANCH,0<?BRANCH8; escape=2; msc=1; hotcalls=16 | crossover; mutation: scale=1, tail=1 |
| a74b828e9b | 0.594 | 0.608 | 13073 | 0.936 | nogcse=1; nocet=1; tracer=1; bytehdr=0; spec=loc,tiny,small,imm; guard=1; 17 pairs: DUP >R, C! R>, >R C!, R@ ROT, ...; rtfuse=0; ops10==?BRANCH,>?BRANCH8,=I?BRANCH8,DUP?BRANCH,OVER?BRANCH8,SWAP+I,+!,?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,OVER?BRANCH,DUP?NBRANCH,<?BRANCH8,(LOOP),J,=?BRANCH8,I,<>?BRANCH,?DUP,<>?BRANCH8,<?BRANCH,(LEAVE),=I?BRANCH,DUP?BRANCH8,(?DO); escape=2; tail=1; hotcalls=32 | mutation: nocrossjump=0, nogcse=1 |
| af5e8dc29f | 0.622 | 0.604 | 10254 | 0.867 | nocet=1; peel=1; varslot=0; guard=1; 18 pairs: DUP >R, C! R>, >R C!, DUP C@, ...; rtfuse=1; ops10=>?BRANCH8,=I?BRANCH8,DUP?BRANCH,SWAP+I,+!,?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,OVER?BRANCH,DUP?NBRANCH,>?BRANCH,(?DO),<?BRANCH8,(LOOP),DUP?NBRANCH8,=?BRANCH8,I,<>?BRANCH,0<?BRANCH,EXECUTE,<?BRANCH,DUP?BRANCH8,U<?BRANCH,<>?BRANCH8; escape=2; msc=1 | mutation: +super SWAP ROT |
| b06a4cf784 | 0.636 | 0.615 | 10246 | 0.821 | nocet=1; peel=1; varslot=0; guard=1; 18 pairs: DUP >R, C! R>, >R C!, DUP C@, ...; rtfuse=1; ops10=>?BRANCH8,=I?BRANCH8,DUP?BRANCH,SWAP+I,+!,?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,OVER?BRANCH,DUP?NBRANCH,>?BRANCH,(?DO),<?BRANCH8,(LOOP),DUP?NBRANCH8,=?BRANCH8,I,<>?BRANCH,0<?BRANCH,EXECUTE,<?BRANCH,DUP?BRANCH8,U<?BRANCH,<>?BRANCH8; escape=2; msc=1 | crossover; mutation: peel=1 |
| c61857fc89 | 0.637 | 0.633 | 10034 | 0.723 | align1=1; varslot=0; guard=1; 19 pairs: DUP >R, C! R>, >R C!, >R OVER, ...; rtfuse=1; ops10=EXECUTE,J,(LEAVE),?BRANCH8,=?BRANCH8,SWAP+I,+!,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,DUP?BRANCH8,OVER?BRANCH,DUP?NBRANCH8,(LOOP),U<?BRANCH,DUP?BRANCH,DUP?NBRANCH,I,<>?BRANCH,<>?BRANCH8,(?DO); escape=2; msc=1; hotcalls=32 | mutation: hotcalls=32 |
| ca2ac63866 | 0.641 | 0.634 | 9531 | 0.881 | opt=O3; nocrossjump=1; nocet=1; ipaclone=1; tracer=1; guard=1; 18 pairs: DUP >R, C! R>, >R C!, SWAP R>, ...; rtfuse=0; ops10=J,?BRANCH8,=?BRANCH8,SWAP+I,BRANCH8,?NBRANCH,<?BRANCH,DUP?NBRANCH,<>?BRANCH,>?BRANCH8,DUP?BRANCH,?NBRANCH8,0<?BRANCH8,DUP?NBRANCH8,=I?BRANCH,EXECUTE,<?BRANCH8,DUP?BRANCH8,<>?BRANCH8,(?DO),OVER?BRANCH,(DO),=I?BRANCH8,?DUP,(LOOP); escape=2; msc=1; hotcalls=16 | crossover; mutation: -O3 |
| c40ba92d5b | 0.647 | 0.630 | 9511 | 0.779 | nocrossjump=1; nocet=1; ipaclone=1; tracer=1; spec=tiny,small,imm; guard=1; 18 pairs: DUP >R, C! R>, >R C!, R@ ROT, ...; rtfuse=0; ops10=(DO),=?BRANCH,>?BRANCH8,=I?BRANCH,=I?BRANCH8,DUP?BRANCH,OVER?BRANCH8,SWAP+I,+!,?DUP,?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<>?BRANCH8,0<?BRANCH8,OVER?BRANCH,DUP?NBRANCH,>?BRANCH,(?DO),<?BRANCH8,(LOOP),J,DUP?NBRANCH8; escape=2; msc=1; hotcalls=8 | mutation: hotcalls=8 |
| 6495dcb5dd | 0.649 | 0.662 | 9343 | 0.802 | nocet=1; peel=1; spec=loc,tiny,small,imm; varslot=0; guard=1; 18 pairs: DUP >R, C! R>, >R C!, R@ ROT, ...; rtfuse=0; ops10=(DO),=?BRANCH,>?BRANCH8,=I?BRANCH,=I?BRANCH8,DUP?BRANCH,<>?BRANCH,SWAP+I,+!,?DUP,?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<>?BRANCH8,0<?BRANCH8,OVER?BRANCH,DUP?NBRANCH,>?BRANCH,(?DO),<?BRANCH8,(LOOP),J,DUP?NBRANCH8; escape=2; msc=1; hotcalls=32 | mutation: ipaclone=0 |
| 090672993b | 0.699 | 0.700 | 9335 | 0.853 | nocet=1; noreorder=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; 18 pairs: DUP >R, C! R>, >R C!, R@ ROT, ...; rtfuse=0; ops10=(DO),=?BRANCH,>?BRANCH8,DUP?BRANCH,?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,0<?BRANCH8,OVER?BRANCH,DUP?NBRANCH,<?BRANCH8,(LOOP),DUP?NBRANCH8,U<?BRANCH,=?BRANCH8,I,<>?BRANCH,0<?BRANCH,?DUP,<>?BRANCH8,EXECUTE,<?BRANCH,DUP?BRANCH8,(?DO); escape=2; hotcalls=32 | mutation: scale=1, msc=0 |
| 422d6bcbca | 0.701 | 0.699 | 9327 | 0.942 | nocet=1; align1=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; guard=1; 18 pairs: C! R>, >R C!, SWAP R>, R> SWAP, ...; rtfuse=0; ops10=J,?BRANCH8,=?BRANCH8,SWAP+I,BRANCH8,?NBRANCH,<?BRANCH,DUP?NBRANCH,<>?BRANCH,>?BRANCH8,DUP?BRANCH,?NBRANCH8,DUP?NBRANCH8,=I?BRANCH,EXECUTE,<?BRANCH8,DUP?BRANCH8,<>?BRANCH8,(?DO),=I?BRANCH8,?DUP,(LOOP),=?BRANCH,+!,>?BRANCH; escape=2; msc=1; hotcalls=32 | crossover; mutation: nocrossjump=0 |

## How the front came about

- `cd943ed219`: from crossover; borrowed scale+bytehdr+doesfar from 02e12b6973; mutation: nocet=1, tracer=1, then crossover / crossover; mutation: peel=1 / crossover; mutation: tail=0, tail=1 / crossover; mutation: noreorder=1 / crossover; mutation: d256=1, nocet=0 / mutation: bytehdr=0 / crossover / mutation: rtfuse=1
- `15dde12f04`: from founder: s6-cv8b + escape, all format-10 opcodes, pairs, tests fused at run time, then crossover; borrowed scale+bytehdr+doesfar from 02e12b6973; mutation: n / crossover / crossover; mutation: peel=1 / crossover; mutation: tail=0, tail=1 / crossover; mutation: noreorder=1 / crossover; mutation: d256=1, nocet=0 / mutation: bytehdr=0 / crossover
- `dc02ceae31`: from crossover; mutation: tracer=0, then crossover; borrowed ops10+supers from 7fdf5f6531; mutation: scale=3 / mutation: nocet=0 / borrowed folds+supers from 3fcdd38166; mutation: -O3, hotcalls=8 / mutation: ipaclone=0, peel=1 / mutation: scale=0 / mutation: rtfuse=0 / borrowed folds from 30acef205d; mutation: hotcalls=32, peel=0 / crossover; mutation: scale=1, tail=1
- `a74b828e9b`: from mutation: rtfuse=0, then crossover; borrowed msc from ba8a353700; mutation: -spec var, varslot= / crossover / mutation: peel=1, sharedcall=0 / crossover / crossover; mutation: op (LEAVE)->U<?BRANCH / crossover; mutation: msc=0 / mutation: ipaclone=0 / mutation: nocrossjump=0, nogcse=1
- `af5e8dc29f`: from mutation: nocrossjump=1, msc=1, then crossover; mutation: noreorder=1 / mutation: rtfuse=0 / crossover; borrowed msc from ba8a353700; mutation: -spec var, varslot= / crossover / mutation: peel=1, sharedcall=0 / crossover / crossover; mutation: peel=1 / mutation: +super SWAP ROT
- `b06a4cf784`: from crossover; mutation: peel=1, then mutation: nocrossjump=1, msc=1 / crossover; mutation: noreorder=1 / mutation: rtfuse=0 / crossover; borrowed msc from ba8a353700; mutation: -spec var, varslot= / crossover / mutation: peel=1, sharedcall=0 / crossover / crossover; mutation: peel=1
- `c61857fc89`: from crossover; mutation: noreorder=1, then mutation: rtfuse=0 / crossover; borrowed msc from ba8a353700; mutation: -spec var, varslot= / crossover / crossover; mutation: tos=0, tos=1 / mutation: tracer=1, hotcalls=0 / crossover; borrowed ops10+supers from 93a9092bcd; mutation: align1=1 / mutation: ipaclone=0 / mutation: hotcalls=32
- `ca2ac63866`: from crossover; borrowed scale+bytehdr+doesfar from 02e12b6973; mutation: nocet=1, tracer=1, then crossover / crossover; mutation: peel=1 / crossover; mutation: tail=0, tail=1 / crossover; mutation: noreorder=1 / crossover; mutation: d256=1, nocet=0 / mutation: bytehdr=0 / crossover / crossover; mutation: -O3
- `c40ba92d5b`: from crossover; mutation: tracer=0, then crossover; borrowed ops10+supers from 7fdf5f6531; mutation: scale=3 / mutation: nocet=0 / borrowed msc+tail from 669f644a32; mutation: scale=0 / crossover; mutation: guard=1, varslot=1 / borrowed spec from ba8a353700; mutation: peel=1 / crossover; mutation: -spec loc / borrowed escape+ops10+supers from 4821db509f; mutation: bytehdr=1, pee / mutation: hotcalls=8
- `6495dcb5dd`: from crossover; mutation: peel=1, then mutation: nocrossjump=1, msc=1 / crossover; mutation: noreorder=1 / mutation: rtfuse=0 / crossover; borrowed msc from ba8a353700; mutation: -spec var, varslot= / crossover / mutation: peel=1, sharedcall=0 / mutation: hotcalls=32, op OVER?BRANCH8-><>?BRANCH / mutation: ipaclone=0
- `090672993b`: from crossover; mutation: noreorder=1, then mutation: rtfuse=0 / crossover; borrowed msc from ba8a353700; mutation: -spec var, varslot= / crossover / mutation: peel=1, sharedcall=0 / crossover / crossover; mutation: op (LEAVE)->U<?BRANCH / crossover; mutation: sharedcall=1, noreorder=1 / mutation: scale=1, msc=0
- `422d6bcbca`: from crossover; mutation: peel=1, then crossover; mutation: tail=0, tail=1 / crossover; mutation: noreorder=1 / crossover; mutation: d256=1, nocet=0 / mutation: bytehdr=0 / crossover / crossover; mutation: -O3 / mutation: align1=1 / crossover; mutation: nocrossjump=0

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.195 | 25144 | no |
| s1-sod16 | 1.544 | 16304 | no |
| s2-cpt16 | 1.228 | 15384 | no |
| s3-cpt16f | 1.192 | 15200 | no |
| s4-cv8 | 1.156 | 14152 | no |
| s5-cv8spec | 0.932 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 116

