# Seed 11 on the AMD Ryzen 7 PRO 8840HS (Iteration 52)

The first run that could choose the Forth sources' batch (Iterations
49-51): kfast, FILL and CMOVE as opcodes, THREAD-FIND as one. Commit
557bd718, `seed 11` from NEXT-RUN, pop 32 x 40 generations, 3 rounds, by
the median, 131 designs carried in from the fronts of 12 databases: 49
minutes, 1,425 designs. Measured again with every earlier front in one
session (session 9, calibration 1.007, the CPUs' ranks agreeing 1.00):
**all 11 designs on the front of all runs are seed 11's own - the fastest
yet, 0.413, at 8,030 bytes (seed 8's 0.436 took 13,073); the smallest
yet, 6,971 bytes; 0.433 at 7,238.**

## Against the fastest earlier design no larger

| seed 11 | size | speed | the fastest earlier design no larger | seed 11 / it |
|---|---|---|---|---|
| 7cb20d14b1 | 6,971 | 0.727 | none so small | - |
| d0d304e240 | 6,977 | 0.691 | 295a6acd98 0.760 at 6,977 | 0.909 |
| 98e6135b93 | 6,978 | 0.677 | 295a6acd98 0.760 at 6,977 | 0.891 |
| 6ba318d95c | 6,989 | 0.605 | 82e7e4dc0d 0.731 at 6,979 | 0.828 |
| 31a3ceea45 | 7,037 | 0.591 | bf413bef91 0.671 at 7,002 | 0.881 |
| 63919635b7 | 7,089 | 0.507 | 5df0608416 0.659 at 7,059 | 0.769 |
| 2c9b948725 | 7,097 | 0.485 | 5df0608416 0.659 at 7,059 | 0.736 |
| cac62ca533 | 7,105 | 0.459 | 5df0608416 0.659 at 7,059 | 0.697 |
| 627568164d | 7,147 | 0.444 | 2ed8b1583e 0.514 at 7,129 | 0.864 |
| 37b502fac7 | 7,238 | 0.433 | 96f2d8bfd7 0.490 at 7,236 | 0.884 |
| ced47e8cfa | 8,030 | 0.413 | 049e0c9c48 0.466 at 7,973 | 0.886 |

9-30% faster at every size. Workload by workload, 37b502fac7 (7,238)
against seed 10's 96f2d8bfd7 (7,236): kernel 0.88, fib 0.92, parse 0.80,
corpus 0.83, loop 0.99, sieve 1.02.

## What it took up, and what it did not

| | generation 0 (145) | living | the front (11) |
|---|---|---|---|
| kfast | 0 | 46% | 7 |
| CMOVE (opcode) | - | 34% | 10 |
| FILL (opcode) | - | 1% | 0 |
| THREAD-FIND (opcode, expressed) | - | 0% | 0 |

FILL: with kfast the fill is gone, and only the held-out sieve still calls
it - nothing selected sees it. **THREAD-FIND, the largest saving of the
three (parse 0.489 counted), was never taken up**: seven of 1,425 designs
drew it from the pool of thirty format-10 names, six of them without
kfast, where it is dormant; the one where it worked (generation 21) was
lost. On seed 11's two best it is still there to have: first in the list,
kernel 0.815-0.821, parse 0.491-0.511, corpus 0.633-0.651, alive, 0-8
bytes. Hence the gene `tfind` (Iteration 52): THREAD-FIND first, a plain
switch where the pool was a needle.

## The run's report

# Evolved VM designs

1425 designs evaluated, 1327 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus, loop,
relative to s6-cv8b; size is the self-hosting image. sieve is held out.

## The Pareto front

| design | speed | re-measured | size | sieve (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| ced47e8cfa | 0.405 | 0.406 | 8030 | 0.549 | nocet=1; ipaclone=1; spec=var,tiny,imm; guard=1; -DROP; 13 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=1; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(DO),(+LOOP),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,>?BRANCH,DUP?NBRANCH,DUP?NBRANCH8,BRANCH8,<>?BRANCH8; escape=2; msc=1; hotcalls=8; rtimm=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1 | crossover; mutation: -spec small |
| 37b502fac7 | 0.415 | 0.433 | 7238 | 0.550 | nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=tiny,small,imm; guard=1; -+ -AND; 15 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),I,(?DO),<?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,>?BRANCH,DUP?NBRANCH; escape=2; msc=1; hotcalls=8; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1 | mutation: hotcalls=8 |
| 627568164d | 0.426 | 0.447 | 7147 | 0.643 | nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=tiny,small,imm; guard=1; -+ -AND; 15 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),I,(?DO),<?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,>?BRANCH,DUP?NBRANCH; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1 | crossover |
| cac62ca533 | 0.442 | 0.450 | 7105 | 0.582 | nocet=1; align1=1; noreorder=1; peel=1; ipaclone=1; spec=tiny,small,imm; guard=1; -C@ -LSHIFT; 15 pairs: DUP >R, C@ OR, SWAP DUP, DUP @, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,?NBRANCH8,>?BRANCH,U<?BRANCH,>?BRANCH8,UNLOOP,J; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1 | mutation: peel=1 |
| 2c9b948725 | 0.481 | 0.481 | 7097 | 0.640 | opt=O3; nocrossjump=1; nocet=1; align1=1; noreorder=1; spec=tiny,small,imm; -C@; 14 pairs: R@ @, DUP >R, C@ OR, SWAP DUP, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(DO),(+LOOP),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,BRANCH8,<>?BRANCH8,=I?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1 | mutation: noreorder=1 |
| 63919635b7 | 0.490 | 0.502 | 7089 | 0.561 | opt=O3; nocet=1; align1=1; noreorder=1; tracer=1; spec=tiny,small,imm; guard=1; -AND; 14 pairs: R@ @, C@ OR, SWAP DUP, DUP @, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(DO),(+LOOP),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,BRANCH8,<>?BRANCH8,>?BRANCH,EXECUTE; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1 | crossover; mutation: scale=3 |
| 3f1d365b3b | 0.571 | 0.590 | 7061 | 0.798 | nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -OR -XOR; 15 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,OVER?BRANCH8,UNLOOP,J,?NBRANCH8; escape=2; msc=1; hotcalls=16; lean=1; bss=1; kfast=1 | mutation: hotcalls=16 |
| 31a3ceea45 | 0.573 | 0.582 | 7037 | 0.818 | nocet=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -OR -SWAP; 15 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,EXECUTE,(+LOOP),I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,>?BRANCH,DUP?NBRANCH,=I?BRANCH8; escape=2; msc=1; hotcalls=16; lean=1; bss=1; kfast=1 | crossover; mutation: rtloopall=1 |
| 7b9675c9ef | 0.591 | 0.604 | 7004 | 0.756 | nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -OR -XOR; 15 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,OVER?BRANCH8,UNLOOP,J,?NBRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1 | mutation: +super R> DROP |
| 6ba318d95c | 0.591 | 0.601 | 6989 | 0.806 | nocet=1; noreorder=1; tracer=1; spec=loc,tiny,small,imm; guard=1; -OR -R@; 15 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),I,(?DO),BRANCH8,<?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,>?BRANCH,DUP?NBRANCH; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1 | crossover; mutation: d256=1 |
| 98e6135b93 | 0.660 | 0.678 | 6978 | 0.772 | nocet=1; noreorder=1; peel=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; guard=1; -AND -RSHIFT; 15 pairs: R@ @, DUP >R, C@ OR, SWAP DUP, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),I,(?DO),BRANCH8,<?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,>?BRANCH,DUP?NBRANCH,DUP?NBRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1 | mutation: peel=1 |
| d0d304e240 | 0.681 | 0.684 | 6977 | 0.811 | nogcse=1; nocet=1; align1=1; peel=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -= -RSHIFT; 15 pairs: ROT DUP, DUP C@, >R OVER, OVER C@, ...; rtfuse=0; ops10=I,(LOOP),?BRANCH8,DUP?BRANCH8,>?BRANCH8,BRANCH8,=I?BRANCH8,?DUP,?NBRANCH,(DO),=I?BRANCH,DUP?BRANCH,SWAP+I,?NBRANCH8,0<?BRANCH8,OVER?BRANCH,DUP?NBRANCH,>?BRANCH,(?DO),J,DUP?NBRANCH8; escape=1; msc=1; hotcalls=32; lean=1; bss=1 | mutation: peel=1 |
| 7cb20d14b1 | 0.708 | 0.718 | 6971 | 0.834 | nocet=1; noreorder=1; spec=loc,tiny,small,imm; guard=1; -DUP -RSHIFT; 7 pairs: ROT DUP, >R OVER, OVER C@, C@ =, ...; rtfuse=0; ops10=I,(LOOP),?BRANCH8,DUP?BRANCH8,>?BRANCH8,BRANCH8,=I?BRANCH8,?NBRANCH,(DO),=I?BRANCH,DUP?BRANCH,SWAP+I,?NBRANCH8,0<?BRANCH8,OVER?BRANCH,DUP?NBRANCH,(?DO),J,DUP?NBRANCH8,+!,(LEAVE),CMOVE,EXECUTE,<?BRANCH8,<>?BRANCH8,0<?BRANCH,<?BRANCH,UNLOOP,OVER?BRANCH8; escape=1; msc=1; hotcalls=32; lean=1; bss=1 | mutation: varslot=1 |

## How the front came about

- `ced47e8cfa`: from carried from archived-20261005-204503/db.jsonl: 9385a8fcbb, then borrowed tos+guard from 5df0608416; mutation: kfast=1 / crossover; mutation: kfast=1, op >?BRANCH->CMOVE / crossover / mutation: hotcalls=8 / crossover; mutation: -spec small
- `37b502fac7`: from carried from archived-20261005-204503/db.jsonl: 9385a8fcbb, then borrowed tos+guard from 5df0608416; mutation: kfast=1 / crossover; mutation: kfast=1, op >?BRANCH->CMOVE / crossover / mutation: hotcalls=8
- `627568164d`: from carried from archived-20261005-204503/db.jsonl: 9385a8fcbb, then borrowed tos+guard from 5df0608416; mutation: kfast=1 / crossover; mutation: kfast=1, op >?BRANCH->CMOVE / crossover
- `cac62ca533`: from carried from archived-20261005-204503/db.jsonl: 9385a8fcbb, then borrowed tos+guard from 5df0608416; mutation: kfast=1 / crossover; mutation: kfast=1, op >?BRANCH->CMOVE / mutation: ipaclone=0 / crossover; mutation: rtloop=0 / crossover; mutation: align1=1 / mutation: peel=1
- `2c9b948725`: from crossover; mutation: kfast=1, op >?BRANCH->CMOVE, then crossover / borrowed msc from f3988ea716; mutation: align1=1, ipaclone=0 / mutation: tracer=0 / crossover / mutation: noreorder=0 / mutation: op U<?BRANCH->=I?BRANCH / mutation: kfast=1, guard=0 / mutation: noreorder=1
- `63919635b7`: from borrowed tos+guard from 5df0608416; mutation: kfast=1, then crossover; mutation: kfast=1, op >?BRANCH->CMOVE / crossover / borrowed msc from f3988ea716; mutation: align1=1, ipaclone=0 / mutation: tracer=0 / crossover / mutation: noreorder=0 / mutation: op U<?BRANCH->=I?BRANCH / crossover; mutation: scale=3
- `3f1d365b3b`: from carried from archived-20261005-204503/db.jsonl: bf413bef91, then mutation: kfast=1 / mutation: hotcalls=16
- `31a3ceea45`: from carried from archived-20261005-204503/db.jsonl: 9385a8fcbb, then borrowed tos+guard from 5df0608416; mutation: kfast=1 / crossover; mutation: kfast=1, op >?BRANCH->CMOVE / mutation: tracer=1 / crossover; mutation: sharedcall=1 / crossover; mutation: rtloopall=1
- `7b9675c9ef`: from carried from archived-20261005-204503/db.jsonl: bf413bef91, then mutation: kfast=1 / mutation: +super R> DROP
- `6ba318d95c`: from carried from archived-20261005-204503/db.jsonl: 9385a8fcbb, then borrowed tos+guard from 5df0608416; mutation: kfast=1 / crossover; mutation: kfast=1, op >?BRANCH->CMOVE / mutation: ipaclone=0 / crossover; mutation: d256=1
- `98e6135b93`: from carried from archived-20261005-204503/db.jsonl: 9385a8fcbb, then borrowed tos+guard from 5df0608416; mutation: kfast=1 / crossover; mutation: kfast=1, op >?BRANCH->CMOVE / mutation: ipaclone=0 / crossover; mutation: d256=1 / crossover / mutation: varslot=1 / mutation: peel=1
- `d0d304e240`: from carried from archived-20261005-204503/db.jsonl: 295a6acd98, then mutation: -op +! / crossover; mutation: nogcse=1 / mutation: peel=1
- `7cb20d14b1`: from carried from archived-20261005-204503/db.jsonl: 295a6acd98, then mutation: -op +! / crossover; mutation: super LSHIFT OVER->C@ DUP / mutation: noreorder=1 / mutation: varslot=1

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.151 | 25144 | no |
| s1-sod16 | 1.508 | 16304 | no |
| s2-cpt16 | 1.141 | 15384 | no |
| s3-cpt16f | 1.126 | 15200 | no |
| s4-cv8 | 1.135 | 14152 | no |
| s5-cv8spec | 0.924 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 91
- died: image did not convert (AssertionError: LOOPTAB: rtloopall needs all eight loop opcodes): 6
- died: kernel workload: 1

