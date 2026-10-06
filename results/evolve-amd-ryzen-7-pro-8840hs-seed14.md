# Seed 14 on the AMD Ryzen 7 PRO 8840HS (Iteration 62)

The first run with the gene `klookup` (Iteration 57): the whole
dictionary lookup ((FIND)) and number conversion ((>NUMBER)) as opcodes,
WORD with one HERE. Commit 4388b682, `seed 14` from NEXT-RUN, pop 32 x 40
generations, 3 rounds, by the median, 173 designs carried in from the
fronts of 15 databases: 54 minutes, 1,356 living designs. Measured again
with every earlier front in one session (session 12, calibration 1.000,
the CPUs' ranks agreeing 1.00): **11 of the 12 designs on the front of all
runs are seed 14's own - the fastest yet, 0.240 at 8,320 bytes, 4.2x
hand-made s6; 0.244 at 7,286; 0.245 at 7,172; 0.264 at 7,089** - and
seed 13's 097ff5bdce (0.411 at 6,913). The small end held: 6,903 bytes.

## Against the fastest earlier design no larger

| seed 14 | size | speed | the fastest earlier design no larger | seed 14 / it |
|---|---|---|---|---|
| 7f7d8e7864 | 6,903 | 0.433 | 5347899701 0.433 at 6,903 | 1.000 |
| b7b4dd1166 | 6,911 | 0.426 | 5347899701 0.433 at 6,903 | 0.984 |
| 3c84b53247 | 6,939 | 0.379 | 097ff5bdce 0.411 at 6,913 | 0.922 |
| 9a9d2cb947 | 6,947 | 0.352 | 097ff5bdce 0.411 at 6,913 | 0.856 |
| 5e7eed1cba | 6,951 | 0.336 | 097ff5bdce 0.411 at 6,913 | 0.818 |
| 7033c6f1ab | 7,017 | 0.326 | 403bda0b3f 0.330 at 7,017 | 0.988 |
| 262f6959cc | 7,057 | 0.265 | 403bda0b3f 0.330 at 7,017 | 0.803 |
| 03fcb0e3e6 | 7,089 | 0.264 | 403bda0b3f 0.330 at 7,017 | 0.800 |
| 285b6909d1 | 7,172 | 0.245 | 76684cada6 0.304 at 7,166 | 0.806 |
| 3995ab7bde | 7,286 | 0.244 | 9c85c7d9f5 0.299 at 7,246 | 0.816 |
| 419cce1726 | 8,320 | 0.240 | ad62971982 0.284 at 7,799 | 0.845 |

15-20% faster from 7.0 to 8.3 KB; 0-18% at the small end.

## klookup, taken up

On 8 of the 11 (all but the three smallest), first in a living design in
generation 2, 41% of the living at the end (kinput 74%). Parse at
0.09-0.12 of s6's time on the front, corpus 0.23-0.26, kernel 0.32-0.42.

## The run's report

# Evolved VM designs

1467 designs evaluated, 1356 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus, loop,
relative to s6-cv8b; size is the self-hosting image. sieve is held out.

## The Pareto front

| design | speed | re-measured | size | sieve (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| 419cce1726 | 0.226 | 0.238 | 8320 | 0.501 | opt=O3; nocrossjump=1; nocet=1; tracer=1; varslot=0; 3 pairs: DUP @, + R>, DUP C@; rtfuse=1; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8; escape=2; msc=1; rtimm=1; lean=1; rtloop=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1 | crossover; mutation: rtfuse=1 |
| 364a0f4617 | 0.227 | 0.249 | 7689 | 0.427 | opt=O3; nocrossjump=1; nocet=1; tracer=1; varslot=0; guard=1; 4 pairs: DUP @, + R>, DUP C@, OVER C@; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),=I?BRANCH,DUP?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8,OVER?BRANCH8,0<?BRANCH; escape=2; msc=1; lean=1; rtloop=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1 | crossover; borrowed tos+guard from 520f651e31; mutation: sha |
| 3995ab7bde | 0.231 | 0.243 | 7286 | 0.553 | opt=O3; nocrossjump=1; nocet=1; tracer=1; varslot=0; 3 pairs: DUP @, + R>, DUP C@; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8; escape=2; msc=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1 | mutation: noreorder=0, tracer=1 |
| 453a46a8e6 | 0.235 | 0.254 | 7188 | 0.491 | opt=O3; nocet=1; noreorder=1; peel=1; varslot=0; guard=1; -@; 4 pairs: + R>, DUP C@, OVER R>, R> SWAP; rtfuse=0; ops10=(FIND),(>NUMBER),SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,THREAD-FIND,0<?BRANCH,DUP?BRANCH,SWAP+I,?DUP; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; kinput=1; klookup=1 | borrowed lean from 003ec9328f; mutation: tfind=0 |
| 285b6909d1 | 0.239 | 0.248 | 7172 | 0.533 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; varslot=0; guard=1; -AND; 4 pairs: DUP @, + R>, DUP C@, >R OVER; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,0<?BRANCH,DUP?BRANCH,SWAP+I; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1 | mutation: ipaclone=0 |
| 03fcb0e3e6 | 0.244 | 0.263 | 7089 | 0.559 | opt=O3; nocet=1; align1=1; noreorder=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -R>; 4 pairs: DUP @, + R>, DUP C@, OVER C@; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,U<?BRANCH,DUP?NBRANCH,>?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1 | mutation: tracer=0 |
| 262f6959cc | 0.253 | 0.259 | 7057 | 0.566 | opt=O3; nocet=1; align1=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -R>; 4 pairs: DUP @, + R>, DUP C@, OVER C@; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1 | crossover; borrowed escape+ops10+supers from 290199b513; mut |
| 828c84dd15 | 0.303 | 0.317 | 7026 | 0.544 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -OVER; 7 pairs: DUP @, DUP R@, + R>, OVER C@, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,BRANCH8,(+LOOP),DUP?BRANCH,EXECUTE,SWAP+I,?NBRANCH,DUP?NBRANCH,>?BRANCH8,0<?BRANCH,DUP?BRANCH8,(DO),?DUP,<>?BRANCH8,=I?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | mutation: tracer=1 |
| 7033c6f1ab | 0.311 | 0.323 | 7017 | 0.593 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -XOR; 6 pairs: DUP @, DUP C@, OVER C@, >R OVER, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1 | mutation: rtloop=1 |
| 5e7eed1cba | 0.319 | 0.333 | 6951 | 0.728 | opt=O3; nocet=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -C!; 5 pairs: DUP >R, DUP R@, SWAP DUP, DUP @, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LEAVE),?BRANCH8,?NBRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,<>?BRANCH8,EXECUTE,DUP?NBRANCH8,DUP?BRANCH,>?BRANCH,<>?BRANCH,UNLOOP,(LOOP),BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1 | mutation: noreorder=0 |
| 9a9d2cb947 | 0.338 | 0.357 | 6947 | 0.769 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; -<; 4 pairs: DUP @, + R>, DUP C@, OVER C@; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,<?BRANCH,UNLOOP,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8,0<?BRANCH,OVER?BRANCH,U<?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1 | mutation: +op U<?BRANCH |
| 3c84b53247 | 0.367 | 0.377 | 6939 | 0.810 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tos=0; spec=loc,tiny,small,imm; -< -=; 6 pairs: DUP @, + R>, DUP C@, OVER C@, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,<?BRANCH,UNLOOP,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8,0<?BRANCH,OVER?BRANCH; escape=2; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1 | crossover; mutation: rtloopall=0 |
| 3280937f3d | 0.402 | 0.416 | 6928 | 0.777 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -<; 7 pairs: DUP @, DUP R@, + R>, OVER C@, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8,0<?BRANCH,DUP?BRANCH8,(DO); escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover; mutation: +super DUP R@ |
| 520f651e31 | 0.408 | 0.411 | 6914 | 0.704 | opt=O3; nocrossjump=1; nocet=1; align1=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -C!; 5 pairs: DUP >R, DUP R@, SWAP DUP, DUP @, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LEAVE),?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,J,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,DUP?BRANCH,>?BRANCH,<>?BRANCH,UNLOOP,(LOOP),BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1 | carried from archived-20261006-012857/db.jsonl: 520f651e31 |
| 097ff5bdce | 0.409 | 0.410 | 6913 | 0.750 | nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -NEGATE; 6 pairs: C@ OR, DUP @, + R>, >R OVER, ...; rtfuse=0; ops10=SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,?DUP,(LOOP),(LEAVE),?BRANCH8,?NBRANCH,<>?BRANCH,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,<?BRANCH,UNLOOP,DUP?NBRANCH,BRANCH8,<>?BRANCH8,DUP?NBRANCH8,THREAD-FIND,EXECUTE,DUP?BRANCH,>?BRANCH,SWAP+I,=I?BRANCH8,=I?BRANCH,0<?BRANCH,J,?NBRANCH8,CMOVE,OVER?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; kinput=1 | carried from archived-20261006-012857/db.jsonl: 097ff5bdce |
| b7b4dd1166 | 0.418 | 0.422 | 6911 | 0.805 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -XOR; 6 pairs: DUP @, DUP C@, OVER C@, >R OVER, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1 | crossover |
| 7f7d8e7864 | 0.422 | 0.435 | 6903 | 0.785 | opt=O3; nocet=1; noreorder=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; -R>; 6 pairs: DUP @, + R>, DUP C@, OVER C@, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8,0<?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1 | mutation: peel=0 |

## How the front came about

- `419cce1726`: from carried from archived-20261006-012857/db.jsonl: 9c85c7d9f5, then mutation: klookup=1 / mutation: noreorder=0, tracer=1 / mutation: rtloopall=0 / crossover; mutation: rtfuse=1
- `364a0f4617`: from carried from archived-20261006-012857/db.jsonl: 9c85c7d9f5, then mutation: klookup=1 / mutation: noreorder=0, tracer=1 / crossover; borrowed tos+guard from 520f651e31; mutation: sharedcall=1
- `3995ab7bde`: from carried from archived-20261006-012857/db.jsonl: 9c85c7d9f5, then mutation: klookup=1 / mutation: noreorder=0, tracer=1
- `453a46a8e6`: from carried from archived-20261006-012857/db.jsonl: ed927db5ce, then crossover; mutation: klookup=1, nocet=0 / mutation: nocet=1, super SWAP R>->R> DROP / crossover; mutation: peel=1 / borrowed lean from 003ec9328f; mutation: tfind=0
- `285b6909d1`: from carried from archived-20261006-012857/db.jsonl: ed927db5ce, then crossover; mutation: klookup=1, nocet=0 / mutation: nocet=1, super SWAP R>->R> DROP / mutation: ipaclone=0
- `03fcb0e3e6`: from carried from archived-20261006-012857/db.jsonl: 5347899701, then crossover; mutation: scale=2 / mutation: -op <?BRANCH8 / crossover; borrowed escape+ops10+supers from 290199b513; mutation: ali / mutation: op ?NBRANCH->U<?BRANCH, peel=1 / mutation: tracer=0
- `262f6959cc`: from carried from archived-20261006-012857/db.jsonl: 5347899701, then crossover; mutation: scale=2 / mutation: -op <?BRANCH8 / crossover; borrowed escape+ops10+supers from 290199b513; mutation: ali
- `828c84dd15`: from carried from archived-20261006-012857/db.jsonl: 5347899701, then mutation: -O2 / crossover; mutation: noreorder=0 / crossover; mutation: +super DUP R@ / crossover; borrowed tail from 097ff5bdce; mutation: ipaclone=1 / mutation: tracer=1
- `7033c6f1ab`: from carried from archived-20261006-012857/db.jsonl: 403bda0b3f, then crossover / mutation: rtloop=1
- `5e7eed1cba`: from carried from archived-20261006-012857/db.jsonl: 520f651e31, then crossover / mutation: noreorder=0
- `9a9d2cb947`: from carried from archived-20261006-012857/db.jsonl: 403bda0b3f, then crossover; mutation: varslot=1 / mutation: peel=1 / mutation: +op U<?BRANCH
- `3c84b53247`: from carried from archived-20261006-012857/db.jsonl: 403bda0b3f, then crossover; mutation: varslot=1 / borrowed varcall+varslot from 7d4606a134; mutation: guard=0 / crossover; mutation: -fold =, varslot=1 / mutation: tos=0 / crossover; mutation: rtloopall=0
- `3280937f3d`: from carried from archived-20261006-012857/db.jsonl: 5347899701, then mutation: -O2 / crossover; mutation: noreorder=0 / crossover; mutation: +super DUP R@
- `520f651e31`: from carried from archived-20261006-012857/db.jsonl: 520f651e31, then (itself)
- `097ff5bdce`: from carried from archived-20261006-012857/db.jsonl: 097ff5bdce, then (itself)
- `b7b4dd1166`: from carried from archived-20261006-012857/db.jsonl: 403bda0b3f, then crossover
- `7f7d8e7864`: from carried from archived-20261006-012857/db.jsonl: 5347899701, then mutation: ipaclone=0 / mutation: peel=0

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.172 | 25144 | no |
| s1-sod16 | 1.556 | 16304 | no |
| s2-cpt16 | 1.185 | 15384 | no |
| s3-cpt16f | 1.161 | 15200 | no |
| s4-cv8 | 1.131 | 14152 | no |
| s5-cv8spec | 0.934 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 99
- died: image did not convert (AssertionError: LOOPTAB: rtloopall needs all eight loop opcodes): 12

