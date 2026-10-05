# Seed 7 on the AMD Ryzen 7 PRO 8840HS (Iteration 40)

The first run that could choose `lean` (build artifacts left out of the
image, Iterations 38-39) and `rtimm` (n + and SWAP n + compiled at run time,
Iteration 37). Commit 4f7e06cd, `seed 7` from NEXT-RUN, pop 32 x 40
generations, 3 rounds, by the median: 35 minutes, 1,308 designs, 1,207
alive. Measured again with every earlier front in one session
(`results/compare-fronts-amd-ryzen-7-pro-8840hs.md`, session 5): **seven
of the eight designs on the front of all runs are seed 7's - 0.673 at
8,073 bytes, the smallest yet, to 0.550 at 11,777**; seed 6's cd943ed219
(0.541 at 14,081) is still the fastest.

## The genes

| | generation 0 (28) | living (1,207) | front of all runs (7 of seed 7's) |
|---|---|---|---|
| lean | 0 | 925 (77%) | 7 |
| rtimm, expressed (with run-time fusion) | - | 179 of 557 with run-time fusion (32%) | 1 (4cc12fc1e7, 8,957 bytes) |
| the tests that keep their value, SWAP+I | - | - | 7 |

lean came from nowhere - no design of generation 0 had it - and is on
every front design: free, as measured. rtimm was weighed and mostly left:
three more front designs carry the flag, dormant without run-time fusion;
only in the middle of the front did fib's gain pay for its bytes.

**Beyond lean**: against seed 6's front with lean applied (its sizes as
Iteration 39 measured them, its speeds as recorded), seed 7 is level at
8.07 KB, 4-5% faster around 8.3 KB, 7% around 9 KB and 2.5% at 11.7 KB.

## The run's report

# Evolved VM designs

1308 designs evaluated, 1204 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus,
relative to s6-cv8b; size is the self-hosting image. loop is held out.

## The Pareto front

| design | speed | re-measured | size | loop (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| a214fa731c | 0.534 | 0.557 | 12664 | 0.696 | opt=O3; nocet=1; noreorder=1; peel=1; ipaclone=1; scale=2; bytehdr=0; guard=1; 22 pairs: OVER C@, C@ DUP, OVER R>, ROT ROT, ...; rtfuse=1; ops10=+!,?DUP,BRANCH8,<?BRANCH8,=I?BRANCH,DUP?BRANCH8,(?DO),SWAP+I,DUP?BRANCH,?BRANCH8,=I?BRANCH8,?NBRANCH,<?BRANCH,OVER?BRANCH,OVER?BRANCH8,U<?BRANCH8,EXECUTE,(LEAVE),0<?BRANCH8,>?BRANCH,>?BRANCH8; escape=2; msc=1; rtimm=1; lean=1 | borrowed escape+ops10+supers from 218a9c42de; mutation: rtim |
| 1cf03a8fd4 | 0.539 | 0.545 | 12608 | 0.882 | opt=O3; nocet=1; noreorder=1; ipaclone=1; tracer=1; scale=2; bytehdr=0; spec=var,tiny,small,imm; guard=1; -ROT; 22 pairs: OVER C@, C@ DUP, ROT ROT, C@ >R, ...; rtfuse=1; ops10=?DUP,BRANCH8,DUP?BRANCH8,(?DO),DUP?BRANCH,?BRANCH8,UNLOOP,?NBRANCH,EXECUTE,0<?BRANCH8,>?BRANCH,(DO),(LOOP),DUP?NBRANCH,U<?BRANCH,=I?BRANCH8,>?BRANCH8,=I?BRANCH,<?BRANCH,OVER?BRANCH,(LEAVE); escape=2; msc=1; rtimm=1; lean=1 | mutation: -fold ROT, rtfuse=1 |
| ff39b37bcc | 0.550 | 0.572 | 12584 | 0.966 | nocet=1; peel=1; scale=1; bytehdr=0; guard=1; 10 pairs: OVER C@, C@ DUP, OVER R>, ROT ROT, ...; rtfuse=1; ops10=+!,?DUP,BRANCH8,<?BRANCH8,=I?BRANCH,DUP?BRANCH8,(?DO),SWAP+I,UNLOOP,=?BRANCH8,U<?BRANCH,DUP?BRANCH,DUP?NBRANCH,?BRANCH8,=I?BRANCH8,(DO),?NBRANCH,<?BRANCH,OVER?BRANCH,OVER?BRANCH8,U<?BRANCH8,EXECUTE,<>?BRANCH8,(LOOP); escape=1; msc=1; rtimm=1; lean=1 | mutation: escape=1 |
| 27a35df3fa | 0.553 | 0.570 | 12312 | 0.920 | nocet=1; align1=1; peel=1; tracer=1; bytehdr=0; guard=1; 16 pairs: OVER C@, C@ DUP, OVER R>, ROT ROT, ...; rtfuse=1; ops10=+!,?DUP,BRANCH8,<?BRANCH8,<>?BRANCH8,=I?BRANCH,DUP?BRANCH8,DUP?NBRANCH8,J,(?DO),SWAP+I,UNLOOP,=?BRANCH8,U<?BRANCH,DUP?BRANCH,DUP?NBRANCH,?BRANCH8,=I?BRANCH8,(DO),?NBRANCH,<?BRANCH,<>?BRANCH,0<?BRANCH8,OVER?BRANCH,OVER?BRANCH8,U<?BRANCH8,I; escape=2; tail=1; lean=1 | mutation: align1=1, tracer=1 |
| 2b00aa6e97 | 0.558 | 0.568 | 12145 | 0.829 | nocet=1; peel=1; ipaclone=1; bytehdr=0; varslot=0; guard=1; 18 pairs: R@ ROT, C@ DUP, OVER C@, SWAP DUP, ...; rtfuse=1; ops10=?DUP,(LOOP),(LEAVE),?NBRANCH,?NBRANCH8,<>?BRANCH8,0<?BRANCH,DUP?BRANCH,U<?BRANCH,=I?BRANCH8,DUP?NBRANCH,EXECUTE,DUP?BRANCH8,(?DO),=I?BRANCH,OVER?BRANCH,?BRANCH8,I,J,<>?BRANCH,+!,<?BRANCH8,=?BRANCH8,(DO),U<?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1 | crossover; mutation: varslot=0 |
| 3a7c3d6e90 | 0.560 | 0.551 | 11777 | 0.806 | nocet=1; peel=1; ipaclone=1; bytehdr=0; varslot=0; guard=1; 18 pairs: R@ ROT, C@ DUP, OVER C@, SWAP DUP, ...; rtfuse=0; ops10=?DUP,(LOOP),(LEAVE),?NBRANCH,?NBRANCH8,<>?BRANCH8,0<?BRANCH,DUP?BRANCH,U<?BRANCH,=I?BRANCH8,DUP?NBRANCH,EXECUTE,DUP?BRANCH8,(?DO),=I?BRANCH,OVER?BRANCH,?BRANCH8,I,J,<>?BRANCH,+!,<?BRANCH8,=?BRANCH8,(DO),U<?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1 | mutation: rtfuse=0 |
| 4cc12fc1e7 | 0.570 | 0.561 | 8957 | 0.874 | opt=O3; nocet=1; align1=1; peel=1; ipaclone=1; guard=1; 22 pairs: OVER R>, ROT ROT, C@ >R, R@ ROT, ...; rtfuse=1; ops10=+!,<?BRANCH8,=I?BRANCH,DUP?BRANCH8,(?DO),SWAP+I,DUP?BRANCH,?BRANCH8,?NBRANCH,<?BRANCH,OVER?BRANCH8,EXECUTE,(LEAVE),>?BRANCH,U<?BRANCH,DUP?NBRANCH,(LOOP),?DUP,U<?BRANCH8,0<?BRANCH8,(DO); escape=2; msc=1; rtimm=1; lean=1 | crossover; mutation: align1=1, peel=1 |
| 3c2d8a577b | 0.578 | 0.603 | 8306 | 0.836 | nogcse=1; nocet=1; tracer=1; guard=1; 21 pairs: DUP >R, C@ DUP, ROT ROT, C@ SWAP, ...; rtfuse=0; ops10=(DO),(LOOP),?BRANCH8,BRANCH8,?NBRANCH,=I?BRANCH,(?DO),OVER?BRANCH,DUP?BRANCH8,(LEAVE),=?BRANCH8,DUP?NBRANCH,<?BRANCH,0<?BRANCH,0<?BRANCH8,DUP?BRANCH,U<?BRANCH,OVER?BRANCH8,>?BRANCH,DUP?NBRANCH8,>?BRANCH8; escape=2; tail=1; lean=1 | borrowed rtfuse+rtimm from 3f451bae7e; mutation: +super R@ @ |
| a306cc61fb | 0.598 | 0.615 | 8305 | 0.897 | nogcse=1; nocet=1; ipaclone=1; tracer=1; guard=1; 22 pairs: DUP >R, C@ DUP, ROT ROT, C@ SWAP, ...; rtfuse=0; ops10=(DO),(LOOP),?BRANCH8,BRANCH8,?NBRANCH,(?DO),OVER?BRANCH,DUP?BRANCH8,=?BRANCH8,DUP?NBRANCH,<?BRANCH,0<?BRANCH,DUP?BRANCH,OVER?BRANCH8,>?BRANCH,DUP?NBRANCH8,>?BRANCH8,?DUP,<?BRANCH8,SWAP+I,U<?BRANCH8; escape=2; tail=1; lean=1 | crossover; borrowed folds from 2a138c09ba; mutation: rtimm=1 |
| f060a4c31f | 0.626 | 0.637 | 8289 | 0.864 | opt=O3; nocet=1; ipaclone=1; tracer=1; guard=1; 22 pairs: OVER C@, C@ DUP, ROT ROT, C@ >R, ...; rtfuse=0; ops10=?DUP,BRANCH8,<?BRANCH8,DUP?BRANCH8,(?DO),SWAP+I,DUP?BRANCH,?BRANCH8,UNLOOP,?NBRANCH,U<?BRANCH8,EXECUTE,0<?BRANCH8,>?BRANCH,(DO),(LOOP),DUP?NBRANCH,U<?BRANCH,+!,=I?BRANCH8,>?BRANCH8; escape=2; msc=1; lean=1 | crossover; mutation: tracer=1, noreorder=0 |
| 9f5e6d173c | 0.635 | 0.650 | 8074 | 0.932 | nocet=1; peel=1; spec=loc,tiny,small,imm; 18 pairs: R@ ROT, C@ DUP, OVER C@, SWAP DUP, ...; rtfuse=0; ops10=?DUP,(LOOP),(LEAVE),?NBRANCH,?NBRANCH8,<>?BRANCH8,0<?BRANCH,0<?BRANCH8,DUP?BRANCH,BRANCH8,<?BRANCH,U<?BRANCH,=I?BRANCH8,DUP?NBRANCH,>?BRANCH,EXECUTE,DUP?BRANCH8,(?DO),=I?BRANCH,OVER?BRANCH,?BRANCH8,I,J,<>?BRANCH,SWAP+I; escape=2; msc=1; hotcalls=32; lean=1 | mutation: guard=0 |
| 49b0a93f14 | 0.685 | 0.688 | 8073 | 0.703 | nocrossjump=1; nocet=1; align1=1; tracer=1; spec=loc,tiny,small,imm; guard=1; 18 pairs: C@ DUP, C@ >R, R> =, SWAP DUP, ...; rtfuse=0; ops10=(DO),?DUP,(LOOP),?NBRANCH,<>?BRANCH8,DUP?BRANCH,I,BRANCH8,<?BRANCH8,=I?BRANCH,+!,OVER?BRANCH8,>?BRANCH,OVER?BRANCH,?BRANCH8,DUP?BRANCH8,EXECUTE,>?BRANCH8,SWAP+I,<>?BRANCH,U<?BRANCH,?NBRANCH8,=?BRANCH,=I?BRANCH8,J; escape=2; msc=1; hotcalls=32; lean=1 | mutation: nocet=1 |

## How the front came about

- `a214fa731c`: from crossover; mutation: tail=0, -spec var, then crossover / crossover; mutation: scale=2 / mutation: noreorder=1, bytehdr=0 / crossover; mutation: nocet=1 / mutation: sharedcall=1, peel=1 / borrowed msc+tail from fccad20f92; mutation: scale=2, ipaclone=1 / mutation: noreorder=1, -O3 / borrowed escape+ops10+supers from 218a9c42de; mutation: rtimm=1
- `1cf03a8fd4`: from mutation: sharedcall=1, peel=1, then borrowed msc+tail from fccad20f92; mutation: scale=2, ipaclone=1 / mutation: noreorder=1, -O3 / borrowed escape+ops10+supers from 218a9c42de; mutation: rtimm=1 / crossover / mutation: +op UNLOOP / crossover; mutation: tracer=1, noreorder=0 / crossover / mutation: -fold ROT, rtfuse=1
- `ff39b37bcc`: from crossover; mutation: tail=0, -spec var, then crossover / crossover; mutation: scale=2 / mutation: noreorder=1, bytehdr=0 / crossover; mutation: nocet=1 / mutation: sharedcall=1, peel=1 / crossover; mutation: +op <>?BRANCH8 / mutation: rtimm=1, scale=1 / mutation: escape=1
- `27a35df3fa`: from crossover; mutation: escape=2, varslot=1, then mutation: guard=1 / crossover; mutation: tail=0, -spec var / crossover / crossover; mutation: scale=2 / mutation: noreorder=1, bytehdr=0 / crossover; mutation: nocet=1 / mutation: sharedcall=1, peel=1 / mutation: align1=1, tracer=1
- `2b00aa6e97`: from mutation: nocet=1, then crossover; mutation: tail=1 / crossover; mutation: guard=1 / mutation: nocet=1 / mutation: hotcalls=32 / mutation: noreorder=1 / crossover; mutation: rtfuse=0, rtimm=1 / mutation: tail=0, tracer=0 / crossover; mutation: varslot=0
- `3a7c3d6e90`: from crossover; mutation: tail=1, then crossover; mutation: guard=1 / mutation: nocet=1 / mutation: hotcalls=32 / mutation: noreorder=1 / crossover; mutation: rtfuse=0, rtimm=1 / mutation: tail=0, tracer=0 / crossover; mutation: varslot=0 / mutation: rtfuse=0
- `4cc12fc1e7`: from mutation: noreorder=1, bytehdr=0, then crossover; mutation: nocet=1 / mutation: sharedcall=1, peel=1 / borrowed msc+tail from fccad20f92; mutation: scale=2, ipaclone=1 / mutation: noreorder=1, -O3 / borrowed escape+ops10+supers from 218a9c42de; mutation: rtimm=1 / mutation: -spec loc / crossover / crossover; mutation: align1=1, peel=1
- `3c2d8a577b`: from crossover; mutation: tail=0, -spec var, then mutation: +op OVER?BRANCH, nocrossjump=1 / mutation: guard=0, msc=1 / crossover; mutation: peel=1 / crossover; mutation: d256=1 / mutation: rtimm=1 / crossover; mutation: tracer=1 / mutation: nogcse=1 / borrowed rtfuse+rtimm from 3f451bae7e; mutation: +super R@ @
- `a306cc61fb`: from mutation: +op OVER?BRANCH, nocrossjump=1, then mutation: guard=0, msc=1 / crossover; mutation: peel=1 / crossover; mutation: d256=1 / mutation: rtimm=1 / crossover; mutation: tracer=1 / mutation: nogcse=1 / borrowed rtfuse+rtimm from 3f451bae7e; mutation: +super R@ @ / crossover; borrowed folds from 2a138c09ba; mutation: rtimm=1
- `f060a4c31f`: from mutation: noreorder=1, bytehdr=0, then crossover; mutation: nocet=1 / mutation: sharedcall=1, peel=1 / borrowed msc+tail from fccad20f92; mutation: scale=2, ipaclone=1 / mutation: noreorder=1, -O3 / borrowed escape+ops10+supers from 218a9c42de; mutation: rtimm=1 / crossover / mutation: +op UNLOOP / crossover; mutation: tracer=1, noreorder=0
- `9f5e6d173c`: from mutation: nocet=1, then crossover; mutation: tail=1 / crossover; mutation: guard=1 / mutation: nocet=1 / mutation: hotcalls=32 / mutation: noreorder=1 / crossover; mutation: rtfuse=0, rtimm=1 / mutation: tail=0, tracer=0 / mutation: guard=0
- `49b0a93f14`: from mutation: nocrossjump=1, -super OVER C@, then crossover; mutation: (none) / borrowed rtimm from 777c52a532; mutation: nocet=0 / crossover; mutation: tos=0 / mutation: -super ROT DUP, d256=1 / mutation: -super + R> / mutation: +super >R DUP / borrowed tail+tos from f08c0348cf; mutation: msc=1 / mutation: nocet=1

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.190 | 25144 | no |
| s1-sod16 | 1.506 | 16304 | no |
| s2-cpt16 | 1.172 | 15384 | no |
| s3-cpt16f | 1.162 | 15200 | no |
| s4-cv8 | 1.130 | 14152 | no |
| s5-cv8spec | 0.959 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 100
- died: kernel workload: 3
- died: image did not convert (AssertionError: call target 1302 not 8-aligned): 1

