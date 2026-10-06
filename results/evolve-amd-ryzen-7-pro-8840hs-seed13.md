# Seed 13 on the AMD Ryzen 7 PRO 8840HS (Iteration 56)

The first run with the gene `kinput` (Iterations 54-55): the input side -
REFILL's tab loop, (PARSE), ?STACK's check, and SCAN, SKIP, TABS>BL, FILL,
(PARSE), HASH, PLACE as opcodes. Commit 5bc9190b, `seed 13` from NEXT-RUN,
pop 32 x 40 generations, 3 rounds, by the median, 157 designs carried in
from the fronts of 14 databases: 49 minutes, 1,350 living designs.
Measured again with every earlier front in one session (session 11,
calibration 0.994, the CPUs' ranks agreeing 1.00): **all 10 designs on the
front of all runs are seed 13's own - the fastest yet, 0.284 at 7,799
bytes, 3.5x hand-made s6; 0.297 at 7,246; 0.329 at 7,017; the smallest
yet, 6,903 bytes at 0.436.** No design above 7,799 bytes is on the front.

## Against the fastest earlier design no larger

| seed 13 | size | speed | the fastest earlier design no larger | seed 13 / it |
|---|---|---|---|---|
| 5347899701 | 6,903 | 0.436 | none so small | - |
| 097ff5bdce | 6,913 | 0.418 | none so small | - |
| 520f651e31 | 6,914 | 0.411 | none so small | - |
| 403bda0b3f | 7,017 | 0.329 | 988d608671 0.482 at 7,014 | 0.683 |
| 1a5dc48b9c | 7,092 | 0.317 | 988d608671 0.482 at 7,014 | 0.658 |
| 76684cada6 | 7,166 | 0.304 | 35135bde2f 0.379 at 7,105 | 0.802 |
| 103cbedc80 | 7,238 | 0.298 | 35135bde2f 0.379 at 7,105 | 0.786 |
| 9c85c7d9f5 | 7,246 | 0.297 | 35135bde2f 0.379 at 7,105 | 0.784 |
| 3218bf9f21 | 7,666 | 0.293 | 9a482dbeaf 0.354 at 7,334 | 0.828 |
| ad62971982 | 7,799 | 0.284 | 040e367ce9 0.353 at 7,753 | 0.805 |

17-34% faster at every size; the three smallest have no earlier design
as small.

## kinput, taken up

On all ten front designs (tfind on nine, kfast on all), first in a living
design in generation 1, on 66% of the living at the end - kfast 78%, tfind
69%. Parse at 0.15-0.18 of s6's time on the front, corpus 0.28-0.33,
kernel 0.36-0.43.

## The run's report

# Evolved VM designs

1451 designs evaluated, 1350 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus, loop,
relative to s6-cv8b; size is the self-hosting image. sieve is held out.

## The Pareto front

| design | speed | re-measured | size | sieve (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| db3dcdb1f8 | 0.266 | 0.272 | 10181 | 0.577 | opt=O3; nocrossjump=1; noreorder=1; peel=1; varslot=0; guard=1; -OR; 6 pairs: C@ OR, SWAP DUP, DUP @, + R>, ...; rtfuse=1; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,OVER?BRANCH,(DO),I,(?DO),<?BRANCH8,<?BRANCH,UNLOOP,DUP?NBRANCH,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,EXECUTE,DUP?BRANCH,>?BRANCH,SWAP+I,=I?BRANCH8,OVER?BRANCH8,=I?BRANCH; escape=2; msc=1; hotcalls=16; rtimm=1; rtloop=1; bss=1; kfast=1; tfind=1; kinput=1 | mutation: lean=0 |
| ad62971982 | 0.271 | 0.268 | 7799 | 0.509 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; varslot=0; guard=1; -OR; 6 pairs: C@ OR, SWAP DUP, DUP @, + R>, ...; rtfuse=1; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,DUP?BRANCH8,OVER?BRANCH,(DO),I,(?DO),<?BRANCH8,<?BRANCH,UNLOOP,DUP?NBRANCH,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,EXECUTE,DUP?BRANCH,>?BRANCH,=I?BRANCH8,OVER?BRANCH8,=I?BRANCH,0<?BRANCH,J,?NBRANCH8; escape=2; msc=1; hotcalls=8; rtimm=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover; mutation: d256=0 |
| cd8075731e | 0.275 | 0.278 | 7773 | 0.525 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; peel=1; varslot=0; guard=1; -DROP; 6 pairs: C@ OR, SWAP DUP, DUP @, + R>, ...; rtfuse=1; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,<?BRANCH,UNLOOP,DUP?NBRANCH,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,EXECUTE,DUP?BRANCH,>?BRANCH,SWAP+I,=I?BRANCH8,=I?BRANCH,0<?BRANCH,J,?NBRANCH8; escape=2; msc=1; hotcalls=32; rtimm=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover; mutation: scale=3 |
| 3218bf9f21 | 0.275 | 0.287 | 7666 | 0.545 | opt=O3; nocet=1; ipaclone=1; tracer=1; varslot=0; guard=1; -+; 7 pairs: C@ OR, SWAP DUP, DUP @, + R>, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),?BRANCH8,?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,EXECUTE,I,BRANCH8,<?BRANCH8,0<?BRANCH,=I?BRANCH,SWAP+I,<?BRANCH,UNLOOP,J,OVER?BRANCH8,DUP?NBRANCH,(+LOOP),=I?BRANCH8,<>?BRANCH8,DUP?NBRANCH8,(LEAVE),OVER?BRANCH; escape=2; msc=1; lean=1; rtloop=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover; borrowed rtloopall from 4fc8aaae98; mutation: rtl |
| 9c85c7d9f5 | 0.276 | 0.280 | 7246 | 0.558 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; varslot=0; 5 pairs: DUP @, + R>, DUP C@, OVER C@, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8; escape=2; msc=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover; mutation: guard=0 |
| 103cbedc80 | 0.277 | 0.290 | 7238 | 0.547 | opt=O3; nocet=1; noreorder=1; tracer=1; varslot=0; -DUP; 6 pairs: DUP @, + R>, DUP C@, OVER C@, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,>?BRANCH8,0<?BRANCH,OVER?BRANCH8; escape=2; msc=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover; mutation: tracer=1 |
| 76684cada6 | 0.284 | 0.303 | 7166 | 0.569 | nocet=1; noreorder=1; tracer=1; -AND -DUP -NEGATE -XOR; 8 pairs: DUP >R, DUP @, >R C!, ROT DUP, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LEAVE),?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),I,<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,<>?BRANCH8,=I?BRANCH,DUP?NBRANCH8,DUP?BRANCH,>?BRANCH,<>?BRANCH,UNLOOP,(LOOP),(+LOOP),(?DO),EXECUTE; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover; mutation: -fold XOR |
| ed927db5ce | 0.290 | 0.304 | 7132 | 0.579 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; peel=1; ipaclone=1; varslot=0; guard=1; -RSHIFT; 6 pairs: DUP @, + R>, DUP C@, >R OVER, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8,0<?BRANCH,DUP?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover; mutation: ipaclone=1 |
| bdb87d827e | 0.299 | 0.304 | 7124 | 0.550 | opt=O3; nocrossjump=1; nocet=1; spec=var,tiny,small,imm; varslot=0; guard=1; -ROT; 6 pairs: R@ @, C@ OR, SWAP DUP, >R C!, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(DO),(+LOOP),I,(?DO),<?BRANCH8,0<?BRANCH,=I?BRANCH8,UNLOOP,J,?NBRANCH8,DUP?NBRANCH,BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,>?BRANCH,?BRANCH8,<?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover; mutation: tail=1, noreorder=0 |
| 1a5dc48b9c | 0.303 | 0.308 | 7092 | 0.549 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; spec=tiny,small,imm; guard=1; -@; 5 pairs: R@ @, C@ OR, SWAP DUP, >R C!, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?NBRANCH,<>?BRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH,DUP?BRANCH8,OVER?BRANCH,(DO),(+LOOP),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,>?BRANCH; escape=2; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | mutation: ipaclone=0 |
| ccf0eb9891 | 0.305 | 0.324 | 7068 | 0.561 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -NEGATE; 6 pairs: DUP >R, DUP R@, SWAP DUP, DUP @, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LEAVE),?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,J,?NBRANCH8,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,>?BRANCH,<>?BRANCH,UNLOOP,(LOOP); escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | mutation: rtloop=1 |
| 403bda0b3f | 0.311 | 0.315 | 7017 | 0.579 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -NEGATE; 6 pairs: DUP @, + R>, DUP C@, OVER C@, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | borrowed ops10+supers from 419616a79f; mutation: rtloop=1, t |
| e973e9ada8 | 0.391 | 0.405 | 6940 | 0.788 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -NEGATE; 7 pairs: DUP >R, DUP R@, SWAP DUP, DUP @, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LEAVE),?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),I,<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,J,?NBRANCH8,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,>?BRANCH,<>?BRANCH,UNLOOP,(LOOP); escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1 | mutation: scale=3, op (?DO)->TABS>BL |
| 520f651e31 | 0.403 | 0.406 | 6914 | 0.767 | opt=O3; nocrossjump=1; nocet=1; align1=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -C!; 5 pairs: DUP >R, DUP R@, SWAP DUP, DUP @, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LEAVE),?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,DUP?BRANCH,>?BRANCH,<>?BRANCH,UNLOOP,(LOOP),BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover |
| 097ff5bdce | 0.403 | 0.406 | 6913 | 0.767 | nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -NEGATE; 6 pairs: C@ OR, DUP @, + R>, >R OVER, ...; rtfuse=0; ops10=SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,<?BRANCH,UNLOOP,DUP?NBRANCH,BRANCH8,<>?BRANCH8,DUP?NBRANCH8,THREAD-FIND,EXECUTE,DUP?BRANCH,>?BRANCH,SWAP+I,=I?BRANCH8,=I?BRANCH,0<?BRANCH,J,?NBRANCH8,CMOVE,OVER?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; kinput=1 | mutation: tfind=0 |
| 5347899701 | 0.411 | 0.431 | 6903 | 0.814 | opt=O3; nocet=1; noreorder=1; peel=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; -R>; 6 pairs: DUP @, + R>, DUP C@, OVER C@, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8,0<?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover |

## How the front came about

- `db3dcdb1f8`: from carried from archived-20261005-235645/db.jsonl: c9f3c95232, then crossover; mutation: tracer=1 / crossover; mutation: -spec var / crossover / crossover; mutation: hotcalls=16 / mutation: peel=1 / mutation: lean=0
- `ad62971982`: from carried from archived-20261005-235645/db.jsonl: c9f3c95232, then crossover; mutation: tracer=1 / crossover; mutation: -spec var / crossover / crossover; mutation: hotcalls=16 / mutation: peel=1 / crossover; mutation: d256=0
- `cd8075731e`: from carried from archived-20261005-235645/db.jsonl: c9f3c95232, then crossover; mutation: tracer=1 / crossover; mutation: -spec var / crossover / crossover; mutation: hotcalls=16 / crossover; mutation: scale=3
- `3218bf9f21`: from carried from archived-20261005-235645/db.jsonl: c9f3c95232, then crossover; mutation: tracer=1 / borrowed rtfuse+rtimm from 6ecdafa95b; mutation: tos=0 / crossover; borrowed ops10 from cad46c5c27; mutation: -op =I?BRANCH8 / crossover; mutation: noreorder=0 / crossover; borrowed rtloopall from 4fc8aaae98; mutation: rtloopall=0
- `9c85c7d9f5`: from carried from archived-20261005-235645/db.jsonl: c9f3c95232, then crossover; mutation: tracer=1 / crossover; mutation: -spec var / crossover; mutation: nogcse=1 / crossover; mutation: +fold SWAP / crossover; borrowed rtloop from ed6ec18ab4; mutation: scale=2 / crossover; mutation: guard=0
- `103cbedc80`: from carried from archived-20261005-235645/db.jsonl: c9f3c95232, then crossover; mutation: tracer=1 / crossover; mutation: -spec var / crossover; mutation: nogcse=1 / crossover; mutation: +fold SWAP / crossover; borrowed rtloop from ed6ec18ab4; mutation: scale=2 / crossover; mutation: guard=0 / crossover; mutation: tracer=1
- `76684cada6`: from crossover; mutation: rtloop=0, then mutation: kinput=1, guard=0 / mutation: super C@ OR->DUP R@ / crossover; mutation: hotcalls=32 / crossover; mutation: -fold LSHIFT / crossover; mutation: peel=0 / mutation: nocet=1 / mutation: align1=1 / crossover; mutation: -fold XOR
- `ed927db5ce`: from crossover; mutation: rtloop=0, then mutation: kinput=1, guard=0 / mutation: super C@ OR->DUP R@ / crossover; mutation: hotcalls=32 / mutation: nocrossjump=1, varslot=0 / mutation: tracer=1 / borrowed ops10+supers from 419616a79f; mutation: rtloop=1, tracer=0 / crossover; mutation: tracer=1 / crossover; mutation: ipaclone=1
- `bdb87d827e`: from carried from archived-20261005-235645/db.jsonl: 35135bde2f, then mutation: -spec small, kinput=1 / crossover; mutation: scale=2 / crossover; mutation: tail=1, noreorder=0
- `1a5dc48b9c`: from carried from archived-20261005-235645/db.jsonl: 35135bde2f, then mutation: -spec small, kinput=1 / crossover; mutation: scale=2 / mutation: ipaclone=0
- `ccf0eb9891`: from carried from archived-20261005-235645/db.jsonl: 9102e1dea9, then crossover; mutation: rtloop=0 / mutation: kinput=1, guard=0 / mutation: super C@ OR->DUP R@ / crossover; mutation: hotcalls=32 / mutation: nocrossjump=1, varslot=0 / borrowed escape+ops10+supers from 2fafc0b1df / mutation: rtloop=1
- `403bda0b3f`: from carried from archived-20261005-235645/db.jsonl: 9102e1dea9, then crossover; mutation: rtloop=0 / mutation: kinput=1, guard=0 / mutation: super C@ OR->DUP R@ / crossover; mutation: hotcalls=32 / mutation: nocrossjump=1, varslot=0 / mutation: tracer=1 / borrowed ops10+supers from 419616a79f; mutation: rtloop=1, tracer=0
- `e973e9ada8`: from carried from archived-20261005-235645/db.jsonl: 9102e1dea9, then crossover; mutation: rtloop=0 / mutation: kinput=1, guard=0 / mutation: super C@ OR->DUP R@ / crossover; mutation: hotcalls=32 / mutation: nocrossjump=1, varslot=0 / borrowed escape+ops10+supers from 2fafc0b1df / mutation: scale=3, op (?DO)->TABS>BL
- `520f651e31`: from carried from archived-20261005-235645/db.jsonl: 9102e1dea9, then crossover; mutation: rtloop=0 / mutation: kinput=1, guard=0 / mutation: super C@ OR->DUP R@ / crossover; mutation: hotcalls=32 / mutation: nocrossjump=1, varslot=0 / crossover
- `097ff5bdce`: from carried from archived-20261005-235645/db.jsonl: c9f3c95232, then crossover; mutation: tracer=1 / crossover; mutation: -spec var / crossover / crossover; mutation: hotcalls=16 / crossover; mutation: scale=3 / crossover; mutation: -super OVER C@, sharedcall=1 / mutation: tfind=0
- `5347899701`: from carried from archived-20261005-235645/db.jsonl: c9f3c95232, then crossover; mutation: tracer=1 / crossover; mutation: -spec var / crossover; mutation: nogcse=1 / crossover; mutation: +fold SWAP / borrowed tos+guard from d113518703; mutation: scale=3 / crossover; mutation: peel=1 / crossover

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.153 | 25144 | no |
| s1-sod16 | 1.551 | 16304 | no |
| s2-cpt16 | 1.134 | 15384 | no |
| s3-cpt16f | 1.128 | 15200 | no |
| s4-cv8 | 1.124 | 14152 | no |
| s5-cv8spec | 0.924 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 90
- died: image did not convert (AssertionError: LOOPTAB: rtloopall needs all eight loop opcodes): 11

