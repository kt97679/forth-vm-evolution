# Seed 12 on the AMD Ryzen 7 PRO 8840HS (Iteration 53)

The first run with the gene `tfind` (Iteration 52): THREAD-FIND, kfast's
thread walk, first among the format-10 names. Commit 011ae717, `seed 12`
from NEXT-RUN, pop 32 x 40 generations, 3 rounds, by the median, 144
designs carried in from the fronts of 13 databases: 47 minutes, 1,334
living designs. Measured again with every earlier front in one session
(session 10, calibration 0.994, the CPUs' ranks agreeing 1.00): **all 12
designs on the front of all runs are seed 12's own - the fastest yet,
0.326 at 9,014 bytes; 0.331 at 7,958; 0.379 at 7,105; the smallest yet,
6,941 bytes.**

## Against the fastest earlier design no larger

| seed 12 | size | speed | the fastest earlier design no larger | seed 12 / it |
|---|---|---|---|---|
| 2816900bac | 6,941 | 0.646 | none so small | - |
| 46fbc9e912 | 6,966 | 0.501 | none so small | - |
| c2d99350f1 | 6,974 | 0.490 | 7cb20d14b1 0.719 at 6,971 | 0.682 |
| 0f90ffc36a | 6,998 | 0.485 | 6ba318d95c 0.599 at 6,989 | 0.810 |
| 988d608671 | 7,014 | 0.485 | 6ba318d95c 0.599 at 6,989 | 0.810 |
| 20b3bde0c3 | 7,097 | 0.397 | 2c9b948725 0.483 at 7,097 | 0.822 |
| 35135bde2f | 7,105 | 0.379 | cac62ca533 0.457 at 7,105 | 0.829 |
| 9a482dbeaf | 7,334 | 0.355 | 37b502fac7 0.435 at 7,238 | 0.816 |
| 040e367ce9 | 7,753 | 0.349 | 37b502fac7 0.435 at 7,238 | 0.802 |
| 1918ae250d | 7,820 | 0.349 | 37b502fac7 0.435 at 7,238 | 0.802 |
| 9102e1dea9 | 7,958 | 0.331 | 37b502fac7 0.435 at 7,238 | 0.761 |
| dcbaf0e29f | 9,014 | 0.326 | ced47e8cfa 0.417 at 8,030 | 0.782 |

17-32% faster at every size. Parse, where THREAD-FIND works: 0.21-0.28
of hand-made s6's time on the front, against 0.40-0.58 on seed 11's.

## THREAD-FIND, taken up

Expressed on 11 of the 12 front designs - all but the smallest, which
has no kfast: 8 by tfind, 3 by the pool from ancestors that had it.
tfind first in a living design in generation 7; at the end kfast on 58%
of the living, tfind on 24%, THREAD-FIND expressed on 37% (seed 11: 0%).

## The run's report

# Evolved VM designs

1438 designs evaluated, 1334 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus, loop,
relative to s6-cv8b; size is the self-hosting image. sieve is held out.

## The Pareto front

| design | speed | re-measured | size | sieve (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| dcbaf0e29f | 0.312 | 0.329 | 9014 | 0.474 | opt=O3; nocet=1; varslot=0; guard=1; -RSHIFT; 12 pairs: DUP >R, C@ OR, SWAP DUP, DUP @, ...; rtfuse=1; ops10=THREAD-FIND,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,OVER?BRANCH,DUP?NBRANCH8,(DO),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,(+LOOP); escape=2; msc=1; rtimm=1; lean=1; rtloop=1; rtloopall=1; kfast=1; tfind=1 | crossover; mutation: noreorder=0, scale=1 |
| c9f3c95232 | 0.314 | 0.330 | 7966 | 0.493 | opt=O3; nocet=1; noreorder=1; ipaclone=1; varslot=0; guard=1; -@; 12 pairs: DUP >R, C@ OR, SWAP DUP, DUP @, ...; rtfuse=1; ops10=THREAD-FIND,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,OVER?BRANCH,(DO),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,(+LOOP),DUP?NBRANCH8; escape=2; msc=1; rtimm=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1 | mutation: -super ROT ROT |
| 9102e1dea9 | 0.325 | 0.316 | 7958 | 0.483 | opt=O3; nocet=1; noreorder=1; varslot=0; guard=1; -RSHIFT; 12 pairs: DUP >R, C@ OR, SWAP DUP, DUP @, ...; rtfuse=1; ops10=THREAD-FIND,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,OVER?BRANCH,(DO),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,(+LOOP),DUP?NBRANCH8; escape=2; msc=1; rtimm=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1 | mutation: bss=1 |
| 1918ae250d | 0.342 | 0.346 | 7820 | 0.530 | opt=O3; nocet=1; noreorder=1; ipaclone=1; tracer=1; varslot=0; guard=1; -ROT; 12 pairs: DUP >R, C@ OR, SWAP DUP, DUP @, ...; rtfuse=1; ops10=THREAD-FIND,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,OVER?BRANCH,(DO),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,(+LOOP),DUP?NBRANCH8; escape=2; msc=1; hotcalls=32; rtimm=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1 | mutation: tracer=1 |
| 040e367ce9 | 0.345 | 0.343 | 7753 | 0.586 | opt=O3; nocet=1; noreorder=1; ipaclone=1; varslot=0; guard=1; -RSHIFT; 13 pairs: DUP >R, C@ OR, SWAP DUP, DUP @, ...; rtfuse=0; ops10=THREAD-FIND,+!,?DUP,(LOOP),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,OVER?BRANCH,(DO),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,(+LOOP),DUP?NBRANCH8; escape=2; msc=1; lean=1; rtloop=1; bss=1; kfast=1; tfind=1 | crossover; borrowed tail+tos from 5062ac5f78; mutation: rtlo |
| 9a482dbeaf | 0.348 | 0.351 | 7334 | 0.551 | opt=O3; nocet=1; noreorder=1; varslot=0; guard=1; -RSHIFT; 12 pairs: DUP >R, C@ OR, SWAP DUP, DUP @, ...; rtfuse=0; ops10=THREAD-FIND,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,OVER?BRANCH,DUP?NBRANCH8,(DO),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,(+LOOP); escape=2; msc=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1 | mutation: ipaclone=0, bss=1 |
| 35135bde2f | 0.355 | 0.371 | 7105 | 0.664 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; peel=1; ipaclone=1; spec=tiny,small,imm; guard=1; -=; 12 pairs: R@ @, >R >R, C@ OR, SWAP DUP, ...; rtfuse=0; ops10=THREAD-FIND,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(DO),(+LOOP),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8; escape=2; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1 | crossover; mutation: msc=0, super DUP >R->>R >R |
| 20b3bde0c3 | 0.375 | 0.385 | 7097 | 0.692 | align1=1; noreorder=1; ipaclone=1; tracer=1; tos=0; spec=loc,tiny,small,imm; guard=1; -NEGATE -ROT; 15 pairs: R@ @, DUP >R, C@ OR, SWAP DUP, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(DO),(+LOOP),I,(?DO),<?BRANCH8,0<?BRANCH,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,=I?BRANCH,THREAD-FIND,>?BRANCH; escape=2; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1 | crossover; mutation: tos=0 |
| 988d608671 | 0.473 | 0.478 | 7014 | 0.846 | nocet=1; align1=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; -LIT -U<; 14 pairs: R@ @, DUP >R, C@ DUP, DUP @, ...; rtfuse=0; ops10=THREAD-FIND,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,I,(?DO),BRANCH8,<?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,UNLOOP,J,OVER?BRANCH8,>?BRANCH,DUP?NBRANCH,<>?BRANCH8,(DO),<?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1 | mutation: ipaclone=1 |
| 0f90ffc36a | 0.477 | 0.474 | 6998 | 0.853 | nocet=1; align1=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; -RSHIFT -U<; 14 pairs: DUP >R, C@ DUP, DUP @, >R C!, ...; rtfuse=0; ops10=THREAD-FIND,+!,?DUP,(LOOP),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,I,(?DO),BRANCH8,<?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,UNLOOP,J,>?BRANCH,DUP?NBRANCH,<>?BRANCH8,(DO),<?BRANCH,(+LOOP),?NBRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1 | crossover; mutation: noreorder=0 |
| c2d99350f1 | 0.481 | 0.481 | 6974 | 0.889 | nocrossjump=1; nocet=1; align1=1; noreorder=1; peel=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; guard=1; -R> -U<; 14 pairs: DUP >R, C@ DUP, C@ OR, DUP @, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,I,=I?BRANCH,(?DO),BRANCH8,<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,J,?NBRANCH8,OVER?BRANCH8,>?BRANCH,DUP?NBRANCH,DUP?NBRANCH8,<>?BRANCH8,THREAD-FIND,(DO),(+LOOP); escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1 | crossover; mutation: +op =I?BRANCH, peel=1 |
| 46fbc9e912 | 0.491 | 0.491 | 6966 | 0.794 | nocrossjump=1; nocet=1; align1=1; noreorder=1; peel=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; guard=1; -R> -U<; 14 pairs: DUP >R, C@ DUP, C@ OR, DUP @, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,I,=I?BRANCH,(?DO),BRANCH8,<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,J,?NBRANCH8,OVER?BRANCH8,>?BRANCH,DUP?NBRANCH,DUP?NBRANCH8,<>?BRANCH8,THREAD-FIND,FILL,(+LOOP); escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1 | mutation: op (DO)->FILL |
| 2816900bac | 0.641 | 0.638 | 6941 | 0.852 | opt=O3; nocet=1; align1=1; spec=loc,tiny,small,imm; guard=1; -NEGATE -RSHIFT; 6 pairs: DUP >R, SWAP DUP, DUP @, + R>, ...; rtfuse=0; ops10=+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,EXECUTE,(DO),I,BRANCH8,<?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,UNLOOP,?NBRANCH8,FILL,DUP?NBRANCH,DUP?NBRANCH8,<>?BRANCH8,OVER?BRANCH8; escape=1; msc=1; hotcalls=32; lean=1; bss=1 | mutation: sharedcall=1, noreorder=0 |

## How the front came about

- `dcbaf0e29f`: from carried from archived-20261005-222307/db.jsonl: 2c9b948725, then crossover; borrowed spec from d113518703; mutation: tfind=1, hotcalls= / crossover / mutation: bss=0, sharedcall=1 / mutation: +op DUP?NBRANCH8 / mutation: ipaclone=0, bss=1 / crossover; mutation: noreorder=0, scale=1
- `c9f3c95232`: from carried from archived-20261005-222307/db.jsonl: 2c9b948725, then crossover; borrowed spec from d113518703; mutation: tfind=1, hotcalls= / crossover / mutation: rtfuse=1 / mutation: nogcse=1, tracer=1 / crossover; mutation: fold @->RSHIFT, noreorder=0 / mutation: noreorder=1 / mutation: -super ROT ROT
- `9102e1dea9`: from carried from archived-20261005-222307/db.jsonl: 2c9b948725, then crossover; borrowed spec from d113518703; mutation: tfind=1, hotcalls= / crossover / mutation: rtfuse=1 / mutation: nogcse=1, tracer=1 / crossover; mutation: fold @->RSHIFT, noreorder=0 / crossover; mutation: bss=0 / mutation: bss=1
- `1918ae250d`: from carried from archived-20261005-222307/db.jsonl: 2c9b948725, then crossover; borrowed spec from d113518703; mutation: tfind=1, hotcalls= / crossover / mutation: rtfuse=1 / crossover; mutation: hotcalls=32 / mutation: tracer=1
- `040e367ce9`: from carried from archived-20261005-222307/db.jsonl: 2c9b948725, then crossover; borrowed spec from d113518703; mutation: tfind=1, hotcalls= / crossover / crossover; borrowed tail+tos from 5062ac5f78; mutation: rtloopall=0, r
- `9a482dbeaf`: from carried from archived-20261005-222307/db.jsonl: 2c9b948725, then crossover; borrowed spec from d113518703; mutation: tfind=1, hotcalls= / crossover / mutation: bss=0, sharedcall=1 / mutation: +op DUP?NBRANCH8 / mutation: ipaclone=0, bss=1
- `35135bde2f`: from carried from archived-20261005-222307/db.jsonl: 2c9b948725, then mutation: noreorder=0 / mutation: peel=1 / mutation: ipaclone=1 / crossover; mutation: msc=0, super DUP >R->>R >R
- `20b3bde0c3`: from carried from archived-20261005-222307/db.jsonl: 6ba318d95c, then crossover; mutation: nocet=1 / mutation: ipaclone=1 / crossover; mutation: +op =I?BRANCH, peel=1 / borrowed tos+guard from d6c6128670; mutation: kfast=0 / crossover; borrowed ops10+supers from fc966fab2e; mutation: nocet=0 / mutation: sharedcall=1, tracer=1 / crossover; mutation: tos=0
- `988d608671`: from carried from archived-20261005-222307/db.jsonl: 6ba318d95c, then crossover; mutation: nocet=1 / crossover; mutation: tail=1 / mutation: tracer=0 / mutation: ipaclone=1
- `0f90ffc36a`: from carried from archived-20261005-222307/db.jsonl: 6ba318d95c, then crossover; mutation: nocet=1 / crossover; mutation: tail=1 / mutation: tracer=0 / mutation: ipaclone=1 / crossover; mutation: noreorder=0
- `c2d99350f1`: from carried from archived-20261005-222307/db.jsonl: 6ba318d95c, then crossover; mutation: nocet=1 / mutation: ipaclone=1 / crossover; mutation: +op =I?BRANCH, peel=1
- `46fbc9e912`: from carried from archived-20261005-222307/db.jsonl: 6ba318d95c, then crossover; mutation: nocet=1 / mutation: ipaclone=1 / crossover; mutation: +op =I?BRANCH, peel=1 / mutation: op (DO)->FILL
- `2816900bac`: from carried from archived-20261005-222307/db.jsonl: 98e6135b93, then crossover; mutation: tfind=1 / crossover; mutation: -O3 / mutation: guard=0, op >?BRANCH->FILL / borrowed skippad+fold from 8e2c95d9b2; mutation: align1=1 / mutation: tfind=0, guard=1 / mutation: sharedcall=1, noreorder=0

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.175 | 25144 | no |
| s1-sod16 | 1.505 | 16304 | no |
| s2-cpt16 | 1.172 | 15384 | no |
| s3-cpt16f | 1.134 | 15200 | no |
| s4-cv8 | 1.108 | 14152 | no |
| s5-cv8spec | 0.944 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 94
- died: image did not convert (AssertionError: LOOPTAB: rtloopall needs all eight loop opcodes): 10

