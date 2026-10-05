# Seed 10 on the AMD Ryzen 7 PRO 8840HS (Iteration 47)

The first run that starts from the earlier runs' fronts (Iteration 46):
109 designs carried in from the fronts of 11 archived databases, beside
the founders, every one timed again. Commit 5dd1379b, `seed 10` from
NEXT-RUN, pop 32 x 40 generations, 3 rounds, by the median: 47 minutes -
seven more than seed 9, the carried designs' first timing - 1,409
designs. Measured again with every earlier front in one session (session
8, calibration 1.004, the CPUs' ranks agreeing 1.00): **15 of the 16
designs on the front of all runs are seed 10's own** - carried designs
count for the runs that found them - **from 6,977 bytes, the smallest yet,
to 0.438 at 12,145; 0.486 at 7,236.** Seed 8's 9bb527944a (0.436 at
13,073) keeps the fastest place.

## Progress compounded

Every one of the 15 descends from carried designs - three carried
ancestors each, none from a founder alone. Against the fastest earlier
design no larger, in this session:

| seed 10 | size | speed | the fastest earlier design no larger | seed 10 / it |
|---|---|---|---|---|
| 295a6acd98 | 6,977 | 0.760 | none so small | - |
| 82e7e4dc0d | 6,979 | 0.729 | none so small | - |
| 9385a8fcbb | 6,994 | 0.697 | none so small | - |
| bf413bef91 | 7,002 | 0.668 | none so small | - |
| 7380e8bcb1 | 7,050 | 0.661 | ee4d8f8a50 0.725 at 7,027 | 0.912 |
| 5df0608416 | 7,059 | 0.657 | ee4d8f8a50 0.725 at 7,027 | 0.906 |
| d8d62beb78 | 7,106 | 0.555 | ccce4784b8 0.689 at 7,091 | 0.806 |
| f3988ea716 | 7,113 | 0.517 | ccce4784b8 0.689 at 7,091 | 0.750 |
| 2ed8b1583e | 7,129 | 0.509 | ccce4784b8 0.689 at 7,091 | 0.739 |
| 641b85143d | 7,178 | 0.507 | ccce4784b8 0.689 at 7,091 | 0.736 |
| 96f2d8bfd7 | 7,236 | 0.486 | 88792f1798 0.661 at 7,220 | 0.735 |
| 7a8d429413 | 7,714 | 0.486 | fa23f401cd 0.537 at 7,692 | 0.905 |
| 049e0c9c48 | 7,973 | 0.462 | 45d2ff7e01 0.512 at 7,725 | 0.902 |
| 6827e42d47 | 8,352 | 0.455 | 45d2ff7e01 0.512 at 7,725 | 0.889 |
| ff306b06c1 | 12,145 | 0.438 | 577c999e62 0.463 at 9,278 | 0.946 |

5-26% faster at every size; the most - a quarter - at 7.1-7.2 KB, where
seed 9 had 0.661-0.689 and seed 10 has 0.486-0.517. It met the projection
Iteration 45 made from seed 8's front with the free genes (0.508 at 7,178)
and went past it (0.486 at 7,236).

## The genes

bss on all 15, rtloopall on 11; of the 1,297 living designs, bss 65%,
lean 87%, rtloop 56%, rtloopall 33%.

## The run's report

# Evolved VM designs

1403 designs evaluated, 1297 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus, loop,
relative to s6-cv8b; size is the self-hosting image. sieve is held out.

## The Pareto front

| design | speed | re-measured | size | sieve (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| ff3e6b2a34 | 0.419 | 0.438 | 13073 | 0.562 | nocet=1; ipaclone=1; bytehdr=0; guard=1; -DUP; 13 pairs: DUP >R, >R OVER, C@ DUP, C@ OR, ...; rtfuse=1; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,U<?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?NBRANCH8,DUP?BRANCH8,OVER?BRANCH,(+LOOP),<>?BRANCH,OVER?BRANCH8,DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,UNLOOP,=I?BRANCH8,(DO),J; escape=2; msc=1; hotcalls=32; rtimm=1; lean=1; rtloop=1 | mutation: op DUP?BRANCH->DUP?NBRANCH8 |
| 84a09433d4 | 0.432 | 0.435 | 12585 | 0.599 | nocet=1; ipaclone=1; bytehdr=0; guard=1; -DUP; 13 pairs: DUP >R, >R OVER, C@ DUP, C@ OR, ...; rtfuse=1; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,U<?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?NBRANCH8,DUP?BRANCH8,OVER?BRANCH,(+LOOP),<>?BRANCH,OVER?BRANCH8,DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,UNLOOP,=I?BRANCH8,(DO),J; escape=2; msc=1; hotcalls=32; rtimm=1; lean=1; rtloop=1; rtloopall=1 | mutation: rtloopall=1 |
| ff306b06c1 | 0.439 | 0.451 | 12145 | 0.607 | nocet=1; ipaclone=1; bytehdr=0; spec=loc,var,tiny,imm; guard=1; -DUP; 13 pairs: DUP >R, >R OVER, C@ DUP, C@ OR, ...; rtfuse=1; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,U<?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(+LOOP),<>?BRANCH,OVER?BRANCH8,DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,UNLOOP,=I?BRANCH8,DUP?NBRANCH8,J; escape=2; msc=1; hotcalls=32; rtimm=1; lean=1; rtloop=1; bss=1 | mutation: bytehdr=0 |
| 6827e42d47 | 0.441 | 0.451 | 8352 | 0.510 | nocet=1; ipaclone=1; spec=loc,var,tiny,imm; guard=1; -DUP; 13 pairs: DUP >R, >R OVER, C@ DUP, C@ OR, ...; rtfuse=1; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,U<?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(+LOOP),<>?BRANCH,OVER?BRANCH8,DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,UNLOOP,=I?BRANCH8,DUP?NBRANCH8,J; escape=2; msc=1; hotcalls=32; rtimm=1; lean=1; rtloop=1; bss=1 | mutation: op (DO)->DUP?NBRANCH8, bss=1 |
| 049e0c9c48 | 0.464 | 0.457 | 7973 | 0.541 | nocet=1; ipaclone=1; spec=loc,var,tiny,imm; guard=1; -DUP; 13 pairs: DUP >R, >R OVER, C@ DUP, C@ OR, ...; rtfuse=1; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,U<?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(+LOOP),<>?BRANCH,OVER?BRANCH8,DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,UNLOOP,=I?BRANCH8,(DO),J; escape=2; msc=1; hotcalls=32; rtimm=1; lean=1; rtloop=1; rtloopall=1; bss=1 | mutation: bss=1 |
| cda8cad59b | 0.473 | 0.492 | 7949 | 0.594 | nocet=1; ipaclone=1; spec=loc,tiny,imm; guard=1; -LIT; 13 pairs: DUP >R, C@ DUP, C@ OR, SWAP DUP, ...; rtfuse=1; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,U<?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(+LOOP),<>?BRANCH,OVER?BRANCH8,DUP?NBRANCH,I,(?DO),<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,UNLOOP,=I?BRANCH8,(DO),J,EXECUTE; escape=2; msc=1; hotcalls=32; rtimm=1; lean=1; rtloop=1; rtloopall=1; bss=1 | mutation: +super LSHIFT OVER |
| 85a977e3ed | 0.478 | 0.486 | 7804 | 0.585 | opt=O3; nocet=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; -U<; 13 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=1; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,U<?BRANCH; escape=2; msc=1; hotcalls=8; rtimm=1; lean=1; rtloop=1; rtloopall=1; bss=1 | crossover; mutation: hotcalls=8 |
| 7a8d429413 | 0.484 | 0.479 | 7714 | 0.574 | nocet=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -AND; 13 pairs: C@ DUP, C@ OR, SWAP DUP, DUP @, ...; rtfuse=1; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,U<?BRANCH,OVER?BRANCH8; escape=2; msc=1; hotcalls=32; rtimm=1; lean=1; rtloop=1; rtloopall=1; bss=1 | crossover |
| 0e8b212e50 | 0.488 | 0.507 | 7558 | 0.593 | opt=O3; nocet=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; -SWAP; 14 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,OVER?BRANCH8,UNLOOP,J; escape=2; msc=1; hotcalls=16; lean=1; rtloop=1; bss=1 | mutation: bss=1 |
| 55ca1dfdb5 | 0.488 | 0.499 | 7550 | 0.583 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=tiny,small,imm; guard=1; -SWAP; 14 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,OVER?BRANCH8,UNLOOP,J,?NBRANCH8; escape=2; msc=1; hotcalls=16; lean=1; rtloop=1; bss=1 | crossover; mutation: tracer=1 |
| 96f2d8bfd7 | 0.495 | 0.490 | 7236 | 0.562 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; spec=var,tiny,small,imm; guard=1; -SWAP; 14 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,OVER?BRANCH8,UNLOOP,J,?NBRANCH8; escape=2; msc=1; hotcalls=16; lean=1; rtloop=1; rtloopall=1; bss=1 | mutation: d256=1, +spec var |
| 641b85143d | 0.496 | 0.501 | 7178 | 0.605 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; spec=tiny,small,imm; guard=1; -SWAP; 14 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,OVER?BRANCH8,UNLOOP,J,?NBRANCH8; escape=2; msc=1; hotcalls=16; lean=1; rtloop=1; rtloopall=1; bss=1 | crossover |
| 2ed8b1583e | 0.506 | 0.509 | 7129 | 0.588 | nocet=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -DROP -LSHIFT; 14 pairs: C@ DUP, C@ OR, SWAP DUP, DUP @, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,U<?BRANCH,OVER?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1 | crossover; mutation: -O2 |
| f3988ea716 | 0.522 | 0.510 | 7113 | 0.628 | opt=O3; nocet=1; noreorder=1; ipaclone=1; spec=tiny,small,imm; guard=1; 12 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,OVER?BRANCH8,UNLOOP,J,?NBRANCH8,U<?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1 | crossover |
| d8d62beb78 | 0.548 | 0.545 | 7106 | 0.671 | opt=O3; nocet=1; noreorder=1; ipaclone=1; spec=tiny,small,imm; guard=1; 13 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,OVER?BRANCH8,UNLOOP,J,?NBRANCH8,U<?BRANCH,DUP?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1 | crossover; mutation: scale=3, sharedcall=1 |
| 5df0608416 | 0.645 | 0.659 | 7059 | 0.843 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; spec=tiny,small,imm; guard=1; -SWAP; 14 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,OVER?BRANCH8,UNLOOP,J; escape=2; msc=1; hotcalls=16; lean=1; bss=1 | mutation: nocrossjump=1 |
| 7380e8bcb1 | 0.661 | 0.658 | 7050 | 0.787 | opt=O3; nocrossjump=1; nocet=1; peel=1; ipaclone=1; spec=tiny,small,imm; guard=1; -SWAP; 14 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,OVER?BRANCH8,UNLOOP,J,?NBRANCH8,<>?BRANCH; escape=2; msc=1; hotcalls=16; lean=1; bss=1 | crossover; borrowed tos+guard from 1f10b021f8; mutation: pee |
| c25a5e1714 | 0.664 | 0.668 | 7010 | 0.883 | nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -C@ -NEGATE; 15 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<>?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,OVER?BRANCH8,UNLOOP,J,?NBRANCH8,>?BRANCH8,U<?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; bss=1 | crossover; mutation: rtloop=0 |
| bf413bef91 | 0.668 | 0.681 | 7002 | 0.864 | nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -OR -XOR; 15 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,OVER?BRANCH8,UNLOOP,J,?NBRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1 | crossover; mutation: tracer=1 |
| 9385a8fcbb | 0.696 | 0.690 | 6994 | 0.880 | nocet=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; -= -RSHIFT; 15 pairs: R@ @, DUP >R, C@ DUP, C@ OR, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),(+LOOP),DUP?NBRANCH,I,(?DO),BRANCH8,<?BRANCH8,<>?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1 | mutation: varslot=1 |
| 82e7e4dc0d | 0.724 | 0.726 | 6979 | 0.863 | nocet=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -RSHIFT; 12 pairs: ROT DUP, DUP C@, >R OVER, OVER C@, ...; rtfuse=0; ops10=I,(LOOP),?BRANCH8,DUP?BRANCH8,=?BRANCH8,>?BRANCH8,BRANCH8,=I?BRANCH8,?DUP,?NBRANCH,(DO),=I?BRANCH,DUP?BRANCH,SWAP+I,+!,?NBRANCH8,0<?BRANCH8,OVER?BRANCH,DUP?NBRANCH,>?BRANCH,(?DO),J,DUP?NBRANCH8; escape=1; msc=1; hotcalls=32; lean=1; bss=1 | mutation: +super R> R> |
| 295a6acd98 | 0.763 | 0.755 | 6977 | 0.891 | nocet=1; align1=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -= -RSHIFT; 14 pairs: ROT DUP, DUP C@, >R OVER, OVER C@, ...; rtfuse=0; ops10=I,(LOOP),?BRANCH8,DUP?BRANCH8,>?BRANCH8,BRANCH8,=I?BRANCH8,?DUP,?NBRANCH,(DO),=I?BRANCH,DUP?BRANCH,SWAP+I,+!,?NBRANCH8,0<?BRANCH8,OVER?BRANCH,DUP?NBRANCH,>?BRANCH,(?DO),J,DUP?NBRANCH8; escape=1; msc=1; hotcalls=32; lean=1; bss=1 | mutation: ipaclone=0 |

## How the front came about

- `ff3e6b2a34`: from carried from archived-20261005-164554/db.jsonl: 9bb527944a, then mutation: op DUP?BRANCH->DUP?NBRANCH8
- `84a09433d4`: from carried from archived-20261005-164554/db.jsonl: 9bb527944a, then mutation: op DUP?BRANCH->DUP?NBRANCH8 / mutation: rtloopall=1
- `ff306b06c1`: from carried from archived-20261005-164554/db.jsonl: 72ca2cf497, then crossover; mutation: tail=1, rtloopall=1 / borrowed hotcalls from 1bca68d171; mutation: tail=0, -spec small / mutation: op (DO)->DUP?NBRANCH8, bss=1 / mutation: bytehdr=0
- `6827e42d47`: from carried from archived-20261005-164554/db.jsonl: 72ca2cf497, then crossover; mutation: tail=1, rtloopall=1 / borrowed hotcalls from 1bca68d171; mutation: tail=0, -spec small / mutation: op (DO)->DUP?NBRANCH8, bss=1
- `049e0c9c48`: from carried from archived-20261005-164554/db.jsonl: 72ca2cf497, then crossover; mutation: tail=1, rtloopall=1 / borrowed hotcalls from 1bca68d171; mutation: tail=0, -spec small / mutation: bss=1
- `cda8cad59b`: from carried from archived-20261005-164554/db.jsonl: 72ca2cf497, then crossover; mutation: tail=1, rtloopall=1 / borrowed hotcalls from 1bca68d171; mutation: tail=0, -spec small / crossover; mutation: sharedcall=1 / mutation: +super LSHIFT OVER
- `85a977e3ed`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / crossover; mutation: hotcalls=8
- `7a8d429413`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / crossover; mutation: hotcalls=8 / crossover; mutation: -O2 / crossover
- `0e8b212e50`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1
- `55ca1dfdb5`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / borrowed tail+tos from 1636db98cd; mutation: rtloop=0 / mutation: nocrossjump=1 / crossover; mutation: tracer=1
- `96f2d8bfd7`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / mutation: noreorder=0 / crossover / mutation: d256=1, +spec var
- `641b85143d`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / mutation: noreorder=0 / crossover
- `2ed8b1583e`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / crossover; mutation: hotcalls=8 / crossover; mutation: -O2
- `f3988ea716`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / mutation: +fold SWAP / mutation: tracer=1 / mutation: hotcalls=32 / crossover
- `d8d62beb78`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / mutation: +fold SWAP / mutation: tracer=1 / mutation: hotcalls=32 / crossover / crossover; mutation: scale=3, sharedcall=1
- `5df0608416`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / borrowed tail+tos from 1636db98cd; mutation: rtloop=0 / mutation: nocrossjump=1
- `7380e8bcb1`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / borrowed tail+tos from 1636db98cd; mutation: rtloop=0 / mutation: nocrossjump=1 / crossover; borrowed rtfuse+rtimm from 6d6b15bab3; mutation: align1=0 / mutation: peel=1 / crossover; borrowed tos+guard from 1f10b021f8; mutation: peel=1, noreo
- `c25a5e1714`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / crossover; mutation: tracer=1 / crossover; mutation: rtloop=0
- `bf413bef91`: from carried from archived-20261005-164554/db.jsonl: 85cac726b5, then mutation: bss=1 / mutation: rtloopall=1 / mutation: -spec loc / crossover; mutation: tracer=1
- `9385a8fcbb`: from carried from archived-20261005-175214/db.jsonl: ee4d8f8a50, then crossover; mutation: fold RSHIFT->LIT, ipaclone=1 / crossover / mutation: tail=0, -fold = / mutation: align1=0 / borrowed escape+ops10+supers from 423b5d54c6 / mutation: varslot=1
- `82e7e4dc0d`: from carried from archived-20261005-175214/db.jsonl: ee4d8f8a50, then crossover; mutation: fold RSHIFT->LIT, ipaclone=1 / crossover; mutation: ipaclone=0, +op =?BRANCH8 / mutation: +super R> R>
- `295a6acd98`: from carried from archived-20261005-175214/db.jsonl: ee4d8f8a50, then crossover; mutation: fold RSHIFT->LIT, ipaclone=1 / crossover / mutation: tail=0, -fold = / mutation: ipaclone=0

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.170 | 25144 | no |
| s1-sod16 | 1.593 | 16304 | no |
| s2-cpt16 | 1.173 | 15384 | no |
| s3-cpt16f | 1.167 | 15200 | no |
| s4-cv8 | 1.136 | 14152 | no |
| s5-cv8spec | 0.915 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 104
- died: image did not convert (AssertionError: LOOPTAB: rtloopall needs all eight loop opcodes): 2

