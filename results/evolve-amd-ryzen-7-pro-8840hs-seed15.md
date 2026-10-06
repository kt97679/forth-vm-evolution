# Seed 15 on the AMD Ryzen 7 PRO 8840HS (Iteration 63)

The first run with thinhdr, rtiplus and swapi (Iterations 58-61) to
choose. Commit 6d2696f7, `seed 15` from NEXT-RUN, pop 32 x 40
generations, 3 rounds, by the median, 188 designs carried in from the
fronts of 16 databases: 58 minutes, 1,396 living designs. Measured again
with the newest four runs (session 13, calibration 0.994, the CPUs' ranks
agreeing 1.00): **13 of the 14 designs on the front of all runs are seed
15's own - the smallest yet, 6,654 bytes (0.433); 0.251 at 6,817; 0.239
at 6,940; the fastest yet, 0.230 at 7,958** - and seed 14's 3995ab7bde.

## Against the fastest earlier design no larger

| seed 15 | size | speed | the fastest earlier design no larger | seed 15 / it |
|---|---|---|---|---|
| 58c0a33fbe | 6,654 | 0.433 | none so small | - |
| 29b1a365dc | 6,655 | 0.420 | none so small | - |
| eabd014b0c | 6,673 | 0.400 | none so small | - |
| 1d44bcb8a5 | 6,693 | 0.353 | none so small | - |
| 9c2db9aebe | 6,699 | 0.345 | none so small | - |
| f1c82fbd44 | 6,700 | 0.342 | none so small | - |
| 9f9bfa4f49 | 6,711 | 0.338 | none so small | - |
| eb0033be3d | 6,759 | 0.328 | none so small | - |
| ce2e13ce87 | 6,777 | 0.308 | none so small | - |
| d1b2f540a8 | 6,817 | 0.251 | none so small | - |
| cbbc5291f8 | 6,940 | 0.239 | 3c84b53247 0.375 at 6,939 | 0.637 |
| 8298ca5d59 | 7,310 | 0.234 | 3995ab7bde 0.238 at 7,286 | 0.983 |
| 3a96a12236 | 7,958 | 0.230 | 3995ab7bde 0.238 at 7,286 | 0.966 |

Ten of the thirteen have no earlier design as small; 0.239 at 6,940 is
36% faster than the best earlier design that small. The fastest moved
4.2%, 0.240 -> 0.230, and 362 bytes smaller.

## The new genes

| | living (1,396) | the front (13) |
|---|---|---|
| thinhdr | 70% | 13 |
| rtiplus | 1% | 0 - it needs rtloopall, on 3 of the 13 |
| swapi | 8% | 1 |

All three first in generation 2. thinhdr is free and was taken up
everywhere; the run-time code genes, counted at loop 0.80 (rtiplus) and
fib 0.94 (swapi), did not pay in time against their compile cost and
their opcode slots.

## The run's report

# Evolved VM designs

1482 designs evaluated, 1396 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus, loop,
relative to s6-cv8b; size is the self-hosting image. sieve is held out.

## The Pareto front

| design | speed | re-measured | size | sieve (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| 3a96a12236 | 0.218 | 0.225 | 7958 | 0.476 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; varslot=0; guard=1; -OVER; 6 pairs: + R>, DUP C@, OVER R>, R> SWAP, ...; rtfuse=1; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),<>?BRANCH,CMOVE,0<?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,BRANCH8,<>?BRANCH8,DUP?NBRANCH8,=I?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?BRANCH,SWAP+I,>?BRANCH8,?BRANCH8,OVER?BRANCH8,(DO),?DUP,DUP?BRANCH8; escape=2; msc=1; hotcalls=32; rtimm=1; lean=1; rtloop=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1 | crossover; mutation: ipaclone=0, rtfuse=1 |
| 8298ca5d59 | 0.220 | 0.236 | 7310 | 0.502 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; peel=1; ipaclone=1; varslot=0; guard=1; -+; 4 pairs: DUP @, + R>, DUP C@, >R OVER; rtfuse=0; ops10=(FIND),(>NUMBER),SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,THREAD-FIND,0<?BRANCH,DUP?BRANCH,SWAP+I,>?BRANCH8,?BRANCH8,OVER?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; bss=1; kfast=1; kinput=1; klookup=1; thinhdr=1 | crossover; mutation: peel=1 |
| 773f6d9daf | 0.227 | 0.239 | 6993 | 0.423 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; varslot=0; guard=1; -C@; 5 pairs: DUP @, + R>, DUP C@, >R OVER, ...; rtfuse=0; ops10=I+,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),<>?BRANCH,CMOVE,0<?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,DUP?BRANCH,SWAP+I,>?BRANCH8,?BRANCH8,OVER?BRANCH8,(DO); escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; rtiplus=1 | mutation: rtiplus=1 |
| cbbc5291f8 | 0.228 | 0.246 | 6940 | 0.478 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; varslot=0; guard=1; -OVER; 4 pairs: DUP @, + R>, DUP C@, OVER R>; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),<>?BRANCH,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,EXECUTE,>?BRANCH,DUP?NBRANCH,0<?BRANCH,DUP?BRANCH,SWAP+I,?BRANCH8,OVER?BRANCH8,(DO),?DUP,<?BRANCH,?NBRANCH; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1 | mutation: peel=0 |
| d1b2f540a8 | 0.232 | 0.243 | 6817 | 0.481 | opt=O3; nocet=1; ipaclone=1; spec=tiny,small,imm; varslot=0; guard=1; -AND; 4 pairs: DUP @, + R>, DUP C@, OVER C@; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,(DO),I,(?DO),<?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,0<?BRANCH,DUP?BRANCH,SWAP+I,?DUP,DUP?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1 | mutation: -spec loc, noreorder=0 |
| ce2e13ce87 | 0.298 | 0.311 | 6777 | 0.580 | opt=O3; nocet=1; peel=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -AND; 6 pairs: DUP @, + R>, DUP C@, >R OVER, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,0<?BRANCH,DUP?BRANCH,SWAP+I; escape=2; msc=1; hotcalls=32; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1 | mutation: swapi=0 |
| eb0033be3d | 0.318 | 0.331 | 6759 | 0.682 | opt=O3; nocrossjump=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -OR; 5 pairs: DUP >R, DUP R@, SWAP DUP, DUP @, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,J,?NBRANCH8,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,DUP?BRANCH,<>?BRANCH,UNLOOP,(LOOP),OVER?BRANCH,BRANCH8,DUP?NBRANCH; escape=2; hotcalls=16; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1 | mutation: nocet=0 |
| 9f9bfa4f49 | 0.325 | 0.334 | 6711 | 0.694 | opt=O3; nocrossjump=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -OR; 5 pairs: DUP >R, DUP R@, SWAP DUP, @ >R, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),(?DO),<?BRANCH8,0<?BRANCH,=I?BRANCH8,<?BRANCH,J,?NBRANCH8,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,DUP?BRANCH,<>?BRANCH,UNLOOP,(LOOP),OVER?BRANCH,BRANCH8,DUP?NBRANCH; escape=2; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1 | mutation: sharedcall=0, swapi=1 |
| f1c82fbd44 | 0.331 | 0.336 | 6700 | 0.717 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tos=0; spec=loc,tiny,small,imm; varslot=0; guard=1; -C!; 5 pairs: DUP @, + R>, DUP C@, >R OVER, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,(DO),I,<?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,DUP?BRANCH,SWAP+I,?DUP,DUP?BRANCH8,=I?BRANCH8,>?BRANCH8; escape=2; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1 | mutation: tos=0, nocrossjump=1 |
| 9c2db9aebe | 0.340 | 0.353 | 6699 | 0.769 | opt=O3; align1=1; peel=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -R>; 4 pairs: DUP @, + R>, DUP C@, OVER C@; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8,0<?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1 | mutation: align1=1 |
| 1d44bcb8a5 | 0.353 | 0.358 | 6693 | 0.821 | opt=O3; nogcse=1; align1=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -C!; 5 pairs: @ >R, DUP C@, >R OVER, >R C!, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,(DO),I,<?BRANCH8,<?BRANCH,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,0<?BRANCH,DUP?BRANCH,SWAP+I,?DUP,DUP?BRANCH8,=I?BRANCH8,>?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1 | mutation: align1=1, rtiplus=1 |
| 0df4c46cec | 0.396 | 0.412 | 6680 | 0.744 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -R>; 7 pairs: DUP @, DUP R@, + R>, OVER C@, ...; rtfuse=0; ops10=SWAP+I,THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,(?DO),<?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8,DUP?BRANCH8,(DO),?DUP,<>?BRANCH8,=I?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; swapi=1 | crossover; mutation: swapi=1 |
| eabd014b0c | 0.404 | 0.402 | 6673 | 0.713 | opt=O3; nocet=1; noreorder=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -OVER; 7 pairs: DUP >R, DUP R@, SWAP DUP, DUP @, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LEAVE),?BRANCH8,?NBRANCH,CMOVE,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,0<?BRANCH,SWAP+I,=I?BRANCH8,<?BRANCH,?NBRANCH8,OVER?BRANCH8,DUP?NBRANCH,<>?BRANCH8,EXECUTE,DUP?NBRANCH8,DUP?BRANCH,>?BRANCH,<>?BRANCH,UNLOOP,(LOOP),BRANCH8,(+LOOP),>?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1 | mutation: peel=1, rtiplus=1 |
| 29b1a365dc | 0.407 | 0.415 | 6655 | 0.748 | opt=O3; nocet=1; peel=1; spec=loc,tiny,small,imm; guard=1; -R>; 6 pairs: DUP @, + R>, DUP C@, OVER C@, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,UNLOOP,J,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8,0<?BRANCH; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1 | mutation: rtloopall=0, noreorder=0 |
| 58c0a33fbe | 0.429 | 0.417 | 6654 | 0.795 | opt=O3; nogcse=1; nocrossjump=1; nocet=1; align1=1; noreorder=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -C!; 7 pairs: @ >R, DUP C@, >R OVER, >R C!, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,(DO),I,<?BRANCH8,<?BRANCH,?NBRANCH8,OVER?BRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,0<?BRANCH,DUP?BRANCH,SWAP+I,?DUP,DUP?BRANCH8,=I?BRANCH8,>?BRANCH8; escape=2; msc=1; hotcalls=32; lean=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1 | mutation: nocrossjump=1, nocet=1 |

## How the front came about

- `3a96a12236`: from carried from archived-20261006-024824/db.jsonl: 285b6909d1, then mutation: noreorder=0, thinhdr=1 / crossover; borrowed rtfuse+rtimm from a6beaa6c01; mutation: lean=0 / crossover; borrowed folds+supers from 6a7d472040; mutation: d256=0 / crossover; mutation: tfind=0 / crossover / crossover; mutation: ipaclone=0, rtfuse=1
- `8298ca5d59`: from carried from archived-20261006-024824/db.jsonl: 285b6909d1, then mutation: noreorder=0, thinhdr=1 / crossover; borrowed rtfuse+rtimm from a6beaa6c01; mutation: lean=0 / crossover; borrowed folds+supers from 6a7d472040; mutation: d256=0 / crossover; mutation: tfind=0 / borrowed spec from cbbc5291f8; mutation: rtloopall=0, noreorder=0 / crossover; mutation: peel=1
- `773f6d9daf`: from carried from archived-20261006-024824/db.jsonl: 285b6909d1, then mutation: noreorder=0, thinhdr=1 / crossover; borrowed rtfuse+rtimm from a6beaa6c01; mutation: lean=0 / crossover; borrowed folds+supers from 6a7d472040; mutation: d256=0 / crossover; mutation: tfind=0 / crossover / mutation: rtiplus=1
- `cbbc5291f8`: from carried from archived-20261006-024824/db.jsonl: 285b6909d1, then mutation: noreorder=0, thinhdr=1 / crossover; borrowed rtfuse+rtimm from a6beaa6c01; mutation: lean=0 / crossover; borrowed folds+supers from 6a7d472040; mutation: d256=0 / crossover; mutation: tfind=0 / crossover; mutation: tail=1 / crossover / mutation: nocrossjump=1 / mutation: peel=0
- `d1b2f540a8`: from carried from archived-20261006-024824/db.jsonl: 285b6909d1, then mutation: noreorder=0, thinhdr=1 / crossover; mutation: nocrossjump=0 / crossover; mutation: d256=0 / crossover; mutation: +super @ >R / borrowed folds+supers from 7c7a8189da; mutation: sharedcall=0 / mutation: -spec loc, noreorder=0
- `ce2e13ce87`: from carried from archived-20261006-024824/db.jsonl: 285b6909d1, then mutation: noreorder=0, thinhdr=1 / crossover; mutation: nocrossjump=0 / mutation: rtloop=0 / crossover; mutation: swapi=1 / mutation: swapi=0
- `eb0033be3d`: from carried from archived-20261006-012857/db.jsonl: ccf0eb9891, then crossover; mutation: d256=0, thinhdr=1 / mutation: sharedcall=1, nocet=0 / mutation: noreorder=0 / mutation: msc=0 / mutation: klookup=1 / mutation: varslot=0 / borrowed hotcalls from 29b1a365dc; mutation: nocet=1, hotcalls=16 / mutation: nocet=0
- `9f9bfa4f49`: from carried from archived-20261006-012857/db.jsonl: ccf0eb9891, then crossover; mutation: d256=0, thinhdr=1 / mutation: sharedcall=1, nocet=0 / mutation: noreorder=0 / mutation: msc=0 / mutation: klookup=1 / mutation: varslot=0 / mutation: +super @ >R / mutation: sharedcall=0, swapi=1
- `f1c82fbd44`: from carried from archived-20261006-024824/db.jsonl: 285b6909d1, then mutation: noreorder=0, thinhdr=1 / crossover; mutation: nocrossjump=0 / crossover; mutation: d256=0 / crossover; mutation: +super @ >R / borrowed folds+supers from 7c7a8189da; mutation: sharedcall=0 / crossover; mutation: rtloop=0 / mutation: tos=0, nocrossjump=1
- `9c2db9aebe`: from carried from archived-20261006-012857/db.jsonl: 5347899701, then mutation: thinhdr=1, tail=1 / mutation: d256=0, tfind=0 / crossover; mutation: tail=0 / mutation: varslot=1 / mutation: ipaclone=0 / mutation: rtloopall=0, noreorder=0 / crossover; mutation: nocet=0, rtimm=0 / mutation: align1=1
- `1d44bcb8a5`: from carried from archived-20261006-024824/db.jsonl: 285b6909d1, then mutation: noreorder=0, thinhdr=1 / crossover; mutation: nocrossjump=0 / crossover; mutation: d256=0 / crossover; mutation: +super @ >R / crossover; mutation: nocet=0 / mutation: align1=1, rtiplus=1
- `0df4c46cec`: from carried from archived-20261006-024824/db.jsonl: 3280937f3d, then mutation: thinhdr=1 / crossover; mutation: swapi=1
- `eabd014b0c`: from carried from archived-20261006-024824/db.jsonl: 5e7eed1cba, then crossover / mutation: peel=1, rtiplus=1
- `29b1a365dc`: from carried from archived-20261006-012857/db.jsonl: 5347899701, then mutation: thinhdr=1, tail=1 / mutation: d256=0, tfind=0 / crossover; mutation: tail=0 / mutation: varslot=1 / mutation: ipaclone=0 / mutation: rtloopall=0, noreorder=0
- `58c0a33fbe`: from carried from archived-20261006-024824/db.jsonl: 285b6909d1, then mutation: noreorder=0, thinhdr=1 / crossover; mutation: nocrossjump=0 / crossover; mutation: d256=0 / crossover; mutation: +super @ >R / crossover; mutation: nocet=0 / mutation: align1=1, rtiplus=1 / borrowed rtloopall from 5e25b0d512; mutation: klookup=0 / mutation: nocrossjump=1, nocet=1

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.173 | 25144 | no |
| s1-sod16 | 1.548 | 16304 | no |
| s2-cpt16 | 1.195 | 15384 | no |
| s3-cpt16f | 1.150 | 15200 | no |
| s4-cv8 | 1.156 | 14152 | no |
| s5-cv8spec | 0.952 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 77
- died: image did not convert (AssertionError: LOOPTAB: rtloopall needs all eight loop opcodes): 9

