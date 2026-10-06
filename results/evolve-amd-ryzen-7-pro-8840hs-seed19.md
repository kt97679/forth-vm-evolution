# Seed 19 on the AMD Ryzen 7 PRO 8840HS (Iteration 78)

The second run under three objectives, the first with memory within 8 KB
a tie: `seed 19 tag2`, commit 6482259b; the newest four fronts carried in
(73 designs); 1,346 designs, 1,263 alive - no converter deaths; 33
minutes. Session 17 measured it with seeds 15-18 (calibration 1.009,
ranks 1.00).

**The stopping rule (Iteration 78): a small run, the first.**

| objective | seed 19's best | before (seeds 15-18) | improvement | bar |
|---|---|---|---|---|
| fastest | 0.238 (cc0b1e2aeb) | 0.244 (60c95fbea3) | +2.5% | 5% |
| smallest binary + image | 32,299 (f69da4fcc8) | 32,331 (4996bc41b8) | +0.1% | 2% |
| least memory | 208 KB | 204 KB | none | 8 KB |

**The fastest of all runs without a large engine**: cc0b1e2aeb, 0.238 at
42,512 bytes (image 9,064, binary 33,448); seed 18's 60c95fbea3 was 0.244
at 74,548 with a 66 KB multi-state engine.

**The front of all runs: 18 designs, 0 by memory alone** (19 of 40
before the tie) - 12 of seed 19, 6 of seed 18; 32,299-42,512 bytes,
0.601-0.238; engines in three sizes: 25,280, 29,352, 33,448 bytes.

## The run's report

# Evolved VM designs

1346 designs evaluated, 1263 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus, loop,
relative to s6-cv8b; size is the self-hosting image, binary the stripped engine. sieve is held out.
The front is over three objectives, equal (Iteration 75): speed, binary + image, peak memory - memory within 8 KB a tie (Iteration 77).

## The Pareto front

| design | speed | re-measured | image | binary | binary + image | memory KB | sieve (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|---|---|---|
| d60e3aab99 | 0.217 | 0.253 | 9,064 | 37,544 | 46,608 | 216 | 0.549 | opt=O3; nocet=1; peel=1; ipaclone=1; tracer=1; guard=1; -= -DUP; 5 pairs: DUP R@, C@ OR, >R >R, ROT DUP, ...; rtfuse=1; ops10=I+,(FIND),(>NUMBER),SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,<?BRANCH8,=I?BRANCH8,J,OVER?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,(LOOP),THREAD-FIND,I,(+LOOP),?NBRANCH8,BRANCH8,UNLOOP,(LEAVE),<?BRANCH,>?BRANCH,(DO),SWAP+I,(?DO),<>?BRANCH,<>?BRANCH8; escape=2; rtimm=1; lean=1; rtloop=1; rtloopall=1; kfast=1; kinput=1; klookup=1; thinhdr=1; rtiplus=1; tag2=1 | mutation: tracer=1, align1=0 |
| cc0b1e2aeb | 0.238 | 0.241 | 9,064 | 33,448 | 42,512 | 216 | 0.508 | opt=O3; nocet=1; align1=1; peel=1; ipaclone=1; guard=1; -= -DUP; 5 pairs: DUP R@, C@ OR, >R >R, ROT DUP, ...; rtfuse=1; ops10=I+,(FIND),(>NUMBER),SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,<?BRANCH8,=I?BRANCH8,J,OVER?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,(LOOP),THREAD-FIND,I,(+LOOP),?NBRANCH8,BRANCH8,UNLOOP,(LEAVE),<?BRANCH,>?BRANCH,(DO),SWAP+I,(?DO),<>?BRANCH,<>?BRANCH8; escape=2; rtimm=1; lean=1; rtloop=1; rtloopall=1; kfast=1; kinput=1; klookup=1; thinhdr=1; rtiplus=1; tag2=1 | mutation: nocrossjump=0 |
| 1a90a3e004 | 0.253 | 0.257 | 7,712 | 29,352 | 37,064 | 212 | 0.557 | nocrossjump=1; nocet=1; align1=1; ipaclone=1; tracer=1; tos=0; spec=loc,var,tiny,small; d256=1; guard=1; -C@; 5 pairs: OVER C@, >R >R, ROT ROT, OVER R>, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,(LOOP),<>?BRANCH,0<?BRANCH8,I,(?DO),<?BRANCH8,<?BRANCH,BRANCH8,<>?BRANCH8,?NBRANCH,DUP?NBRANCH,DUP?BRANCH,>?BRANCH8,OVER?BRANCH8,(DO),?NBRANCH8,0<?BRANCH,DUP?BRANCH8,+!,?BRANCH8,EXECUTE,U<?BRANCH,=?BRANCH8,>?BRANCH,UNLOOP,(+LOOP),DUP?NBRANCH8,(LEAVE),?DUP; escape=2; lean=1; rtloop=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=2 | crossover; mutation: tracer=1 |
| 7670d35541 | 0.260 | 0.273 | 7,682 | 29,352 | 37,034 | 212 | 0.629 | nocrossjump=1; nocet=1; ipaclone=1; tos=0; spec=loc,var,tiny,small; d256=1; guard=1; -NEGATE; 5 pairs: OVER C@, >R >R, ROT ROT, SWAP DUP, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,(LOOP),<>?BRANCH,CMOVE,0<?BRANCH8,I,(?DO),<?BRANCH8,<?BRANCH,BRANCH8,<>?BRANCH8,=I?BRANCH,?NBRANCH,DUP?NBRANCH,DUP?BRANCH,SWAP+I,>?BRANCH8,OVER?BRANCH8,(DO),?NBRANCH8,0<?BRANCH,DUP?BRANCH8,+!,?BRANCH8,EXECUTE,U<?BRANCH,=I?BRANCH8,=?BRANCH8,>?BRANCH,UNLOOP; escape=2; lean=1; rtloop=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=2 | mutation: t2hot=0.05 |
| 272854107e | 0.270 | 0.275 | 7,290 | 29,352 | 36,642 | 212 | 0.649 | nocrossjump=1; nocet=1; align1=1; tos=0; spec=loc,var,tiny,small; d256=1; guard=1; -< -R>; 5 pairs: OVER C@, >R >R, OVER R>, + SWAP, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,(LOOP),<>?BRANCH,I,(?DO),<?BRANCH8,<?BRANCH,BRANCH8,<>?BRANCH8,?NBRANCH,DUP?NBRANCH,DUP?BRANCH,>?BRANCH8,OVER?BRANCH8,(DO),?NBRANCH8,0<?BRANCH,DUP?BRANCH8,+!,?BRANCH8,EXECUTE,U<?BRANCH,=?BRANCH8,UNLOOP,(+LOOP),DUP?NBRANCH8,(LEAVE),?DUP,CMOVE,J,=I?BRANCH; escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=2 | crossover; mutation: scale=1 |
| c57aebeb3e | 0.276 | 0.277 | 7,282 | 29,352 | 36,634 | 212 | 0.616 | nocrossjump=1; nocet=1; align1=1; tos=0; d256=1; guard=1; -< -R@; 5 pairs: >R C!, XOR C!, LSHIFT OVER, ROT DUP, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(?DO),<?BRANCH8,=I?BRANCH8,J,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,DUP?NBRANCH8,(LOOP),DUP?NBRANCH,I,(+LOOP),BRANCH8,UNLOOP,(LEAVE),DUP?BRANCH,>?BRANCH,U<?BRANCH,(DO),0<?BRANCH,=?BRANCH8; escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=3 | crossover |
| 74ea2d2e27 | 0.294 | 0.304 | 7,274 | 29,352 | 36,626 | 212 | 0.597 | nocet=1; align1=1; peel=1; ipaclone=1; spec=loc,var,tiny,small; d256=1; guard=1; -R> -RSHIFT; 11 pairs: DUP @, LSHIFT OVER, RSHIFT <, C@ OR, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,?DUP,?BRANCH8,UNLOOP,J,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,>?BRANCH8,DUP?NBRANCH,<?BRANCH,OVER?BRANCH8,(?DO),BRANCH8,<>?BRANCH8,(LOOP),=I?BRANCH8,+!,I,=I?BRANCH,(DO),CMOVE,(LEAVE); escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; tag2=1; t2hot=2 | mutation: -O2 |
| 9fac496194 | 0.342 | 0.347 | 7,115 | 29,352 | 36,467 | 212 | 0.943 | nocet=1; align1=1; ipaclone=1; tos=0; d256=1; guard=1; -C!; 5 pairs: SWAP DUP, + SWAP, LSHIFT OVER, C@ OVER, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,(LOOP),(LEAVE),CMOVE,<?BRANCH8,J,BRANCH8,(+LOOP),?NBRANCH,DUP?NBRANCH,DUP?BRANCH,SWAP+I,>?BRANCH8,OVER?BRANCH8,(DO),?NBRANCH8,DUP?BRANCH8,?BRANCH8,EXECUTE,<?BRANCH,?DUP,=?BRANCH8,>?BRANCH,UNLOOP,<>?BRANCH,DUP?NBRANCH8,I,<>?BRANCH8,0<?BRANCH,+!; escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=2 | crossover; borrowed skippad+fold from 37cfbdfba5; mutation:  |
| 570f49c26e | 0.348 | 0.350 | 7,102 | 29,352 | 36,454 | 212 | 0.912 | nocet=1; ipaclone=1; tracer=1; tos=0; spec=loc,var,tiny,small; d256=1; guard=1; -DROP; 7 pairs: DUP @, + R>, DUP C@, OVER R>, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?BRANCH8,0<?BRANCH8,DUP?BRANCH8,J,?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,?NBRANCH,0<?BRANCH,<?BRANCH,OVER?BRANCH8,CMOVE,(?DO),BRANCH8,<>?BRANCH8,(LEAVE),=I?BRANCH8,(LOOP),>?BRANCH8,I,(+LOOP),DUP?NBRANCH,(DO),>?BRANCH; escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=3 | crossover; mutation: tracer=1 |
| 775d8dda6e | 0.349 | 0.357 | 7,091 | 29,352 | 36,443 | 212 | 0.895 | nocet=1; align1=1; ipaclone=1; tos=0; d256=1; guard=1; -C!; 9 pairs: SWAP DUP, + SWAP, LSHIFT OVER, C@ OVER, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?BRANCH8,0<?BRANCH8,DUP?BRANCH8,J,?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,?NBRANCH,0<?BRANCH,<?BRANCH,OVER?BRANCH8,CMOVE,(?DO),<?BRANCH8,BRANCH8,<>?BRANCH8,(LEAVE),=I?BRANCH8,(LOOP),?DUP,UNLOOP,>?BRANCH8; escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=2 | borrowed ops10 from be38873796; mutation: scale=3 |
| 870c24c9cf | 0.414 | 0.440 | 7,632 | 25,280 | 32,912 | 212 | 0.786 | opt=Os; nocet=1; noreorder=1; ipaclone=1; spec=loc,var,tiny,small; d256=1; guard=1; -@; 11 pairs: + R>, DUP C@, OVER R>, >R C!, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?BRANCH8,0<?BRANCH8,DUP?BRANCH8,J,?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,0<?BRANCH,<?BRANCH,OVER?BRANCH8,CMOVE,<?BRANCH8,BRANCH8,<>?BRANCH8,(LEAVE),=I?BRANCH8,(LOOP),?DUP,>?BRANCH8,DUP?NBRANCH8,>?BRANCH,I,(DO); escape=2; lean=1; rtloop=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; tag2=1; t2hot=2 | crossover; mutation: noreorder=1, rtloopall=0 |
| d05d104578 | 0.420 | 0.436 | 7,466 | 25,280 | 32,746 | 216 | 0.793 | opt=Os; nocet=1; align1=1; peel=1; ipaclone=1; spec=loc,var,tiny; d256=1; guard=1; -R> -RSHIFT; 11 pairs: DUP @, LSHIFT OVER, RSHIFT <, C@ OR, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,?DUP,?BRANCH8,UNLOOP,J,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,>?BRANCH8,DUP?NBRANCH,<?BRANCH,OVER?BRANCH8,(?DO),BRANCH8,<>?BRANCH8,(LOOP),=I?BRANCH8,+!,I,=I?BRANCH,(DO),CMOVE,(LEAVE); escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; tag2=1; t2hot=2 | mutation: -spec small |
| ae5d7cdaae | 0.433 | 0.434 | 7,317 | 25,280 | 32,597 | 212 | 0.766 | opt=Os; nocrossjump=1; nocet=1; align1=1; ipaclone=1; tos=0; spec=loc,var,tiny,small; d256=1; guard=1; -DUP -R>; 7 pairs: OVER C@, >R >R, OVER R>, + SWAP, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,(LOOP),<>?BRANCH,I,(?DO),<?BRANCH8,BRANCH8,<>?BRANCH8,?NBRANCH,DUP?NBRANCH,DUP?BRANCH,OVER?BRANCH8,(DO),?NBRANCH8,0<?BRANCH,DUP?BRANCH8,+!,EXECUTE,U<?BRANCH,=?BRANCH8,UNLOOP,(+LOOP),DUP?NBRANCH8,(LEAVE),?DUP,CMOVE,J,=I?BRANCH,SWAP+I,>?BRANCH,=I?BRANCH8; escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; tag2=1 | crossover; mutation: -Os, t2hot=0.02 |
| 8f0973fc8f | 0.436 | 0.438 | 7,274 | 25,280 | 32,554 | 212 | 0.740 | opt=Os; nocet=1; align1=1; peel=1; ipaclone=1; spec=loc,var,tiny,small; d256=1; guard=1; -R> -RSHIFT; 11 pairs: DUP @, LSHIFT OVER, RSHIFT <, C@ OR, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,?DUP,?BRANCH8,UNLOOP,J,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,>?BRANCH8,DUP?NBRANCH,<?BRANCH,OVER?BRANCH8,(?DO),BRANCH8,<>?BRANCH8,(LOOP),=I?BRANCH8,+!,I,=I?BRANCH,(DO),CMOVE,(LEAVE); escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; tag2=1; t2hot=2 | borrowed escape+ops10+supers from e373839dcb; mutation: shar |
| 635a47fd26 | 0.450 | 0.448 | 7,260 | 25,280 | 32,540 | 208 | 0.845 | opt=Os; nocet=1; noreorder=1; peel=1; ipaclone=1; tracer=1; spec=var,tiny,small,imm; varslot=0; d256=1; -RSHIFT; 7 pairs: OVER C@, C@ =, SWAP DUP, C@ >R, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,(LOOP),(LEAVE),<>?BRANCH,CMOVE,0<?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,U<?BRANCH,J,<>?BRANCH8,(+LOOP),=I?BRANCH,?NBRANCH,DUP?NBRANCH,DUP?BRANCH,SWAP+I,>?BRANCH8,(DO),?NBRANCH8,0<?BRANCH,DUP?BRANCH8,+!,?BRANCH8,EXECUTE,UNLOOP,=?BRANCH8,?DUP; escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; tag2=1; t2hot=2 | borrowed ops10+supers from 2f16321733 |
| b00da878bf | 0.452 | 0.469 | 7,210 | 25,280 | 32,490 | 216 | 0.746 | opt=Os; nocet=1; peel=1; ipaclone=1; tracer=1; spec=tiny,small; varslot=0; guard=1; ->R -RSHIFT; 8 pairs: + SWAP, C@ >R, C@ OVER, >R C!, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?BRANCH8,0<?BRANCH8,DUP?BRANCH8,I,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,?NBRANCH,(DO),DUP?NBRANCH,OVER?BRANCH8,<>?BRANCH,CMOVE,(?DO),<?BRANCH8,BRANCH8,<>?BRANCH8,=I?BRANCH8,(LOOP),(LEAVE),?DUP,>?BRANCH8,UNLOOP,J,?NBRANCH8,0<?BRANCH; escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; tag2=1; t2hot=2 | crossover |
| 4542a08fb0 | 0.467 | 0.465 | 7,194 | 25,280 | 32,474 | 212 | 0.809 | opt=Os; nocet=1; noreorder=1; peel=1; ipaclone=1; tracer=1; spec=tiny,small,imm; varslot=0; -RSHIFT; 7 pairs: DUP @, LSHIFT OVER, R> SWAP, @ >R, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,?BRANCH8,0<?BRANCH8,UNLOOP,J,?NBRANCH8,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,>?BRANCH8,DUP?NBRANCH,<?BRANCH,OVER?BRANCH8,(?DO),<?BRANCH8,BRANCH8,<>?BRANCH8,(LOOP),=I?BRANCH8,+!,I,=I?BRANCH,0<?BRANCH,(DO),CMOVE,(LEAVE); escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; tag2=1; t2hot=2 | carried from archived-20261006-175959/db.jsonl: 4542a08fb0 |
| 2f4c1d82ec | 0.545 | 0.541 | 7,056 | 25,280 | 32,336 | 204 | 1.135 | opt=Os; nocet=1; tos=0; spec=var,tiny,small,imm; d256=1; -XOR; 11 pairs: DUP @, + R>, DUP C@, OVER R>, ...; rtfuse=0; ops10=SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?BRANCH8,0<?BRANCH8,DUP?BRANCH8,J,?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,?NBRANCH,0<?BRANCH,<?BRANCH,OVER?BRANCH8,CMOVE,(?DO),<?BRANCH8,BRANCH8,<>?BRANCH8,(LEAVE),=I?BRANCH8,THREAD-FIND,(LOOP),?DUP,UNLOOP,>?BRANCH8; escape=2; lean=1; bss=1; kfast=1; kinput=1; thinhdr=1; tag2=1; t2hot=2 | mutation: -spec loc |
| 263788ab64 | 0.553 | 0.561 | 7,032 | 25,280 | 32,312 | 208 | 1.249 | opt=Os; nocet=1; tos=0; d256=1; -XOR; 11 pairs: DUP @, + R>, DUP C@, OVER R>, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?BRANCH8,0<?BRANCH8,DUP?BRANCH8,J,?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,?NBRANCH,0<?BRANCH,<?BRANCH,OVER?BRANCH8,CMOVE,(?DO),<?BRANCH8,BRANCH8,<>?BRANCH8,(LEAVE),=I?BRANCH8,(LOOP),?DUP,UNLOOP,>?BRANCH8; escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; tag2=1; t2hot=3 | crossover; mutation: rtimm=0 |
| f69da4fcc8 | 0.595 | 0.605 | 7,019 | 25,280 | 32,299 | 208 | 1.199 | opt=Os; nocet=1; tracer=1; spec=tiny,small,imm; varslot=0; -XOR; 8 pairs: DUP @, LSHIFT OVER, R> SWAP, @ >R, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,?BRANCH8,0<?BRANCH8,UNLOOP,J,?NBRANCH8,DUP?NBRANCH8,DUP?BRANCH,SWAP+I,>?BRANCH,?NBRANCH,>?BRANCH8,DUP?NBRANCH,<?BRANCH,OVER?BRANCH8,(?DO),<?BRANCH8,BRANCH8,(LOOP),=I?BRANCH8,+!,I,=I?BRANCH,0<?BRANCH,(DO),CMOVE,(LEAVE),DUP?BRANCH8,?DUP; escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; tag2=1; t2hot=2 | crossover; mutation: noreorder=0 |

## How the front came about

- `d60e3aab99`: from carried from archived-20261006-175959/db.jsonl: 60c95fbea3, then crossover; mutation: lean=0 / crossover; mutation: lean=0, bss=0 / borrowed rtloop from 1d29263cc0; mutation: rtiplus=1 / mutation: lean=1 / mutation: nocrossjump=0 / mutation: tracer=1, align1=0
- `cc0b1e2aeb`: from carried from archived-20261006-175959/db.jsonl: 60c95fbea3, then crossover; mutation: lean=0 / crossover; mutation: lean=0, bss=0 / borrowed rtloop from 1d29263cc0; mutation: rtiplus=1 / mutation: lean=1 / mutation: nocrossjump=0
- `1a90a3e004`: from carried from archived-20261006-175959/db.jsonl: 76ab789fed, then crossover; mutation: tail=1 / crossover; mutation: tracer=1
- `7670d35541`: from carried from archived-20261006-175959/db.jsonl: 76ab789fed, then crossover; mutation: tail=1 / mutation: t2hot=0.05
- `272854107e`: from carried from archived-20261006-175959/db.jsonl: 76ab789fed, then crossover; mutation: tail=1 / crossover; mutation: tracer=1 / crossover; mutation: scale=1
- `c57aebeb3e`: from carried from archived-20261006-175959/db.jsonl: 60c95fbea3, then crossover
- `74ea2d2e27`: from carried from archived-20261006-175959/db.jsonl: 301a268219, then crossover; mutation: noreorder=0, super + R>->DUP = / borrowed escape+ops10+supers from e373839dcb; mutation: sharedcall=1 / mutation: -O2
- `9fac496194`: from carried from archived-20261006-175959/db.jsonl: 51a8931db2, then crossover; mutation: sharedcall=1 / mutation: -fold U< / crossover; mutation: align1=0 / mutation: rtloop=1 / crossover; mutation: tfind=0, align1=1 / crossover; borrowed skippad+fold from 37cfbdfba5; mutation: nocrossjum
- `570f49c26e`: from carried from archived-20261006-175959/db.jsonl: 776c86e476, then mutation: escape=2 / mutation: varslot=1 / crossover; mutation: msc=1, -super SWAP R> / crossover; mutation: rtimm=0 / mutation: ipaclone=1 / crossover; mutation: tracer=1
- `775d8dda6e`: from carried from archived-20261006-175959/db.jsonl: 51a8931db2, then crossover; mutation: sharedcall=1 / mutation: -fold U< / crossover; mutation: align1=0 / mutation: rtloop=1 / crossover; mutation: tfind=0, align1=1 / crossover; borrowed skippad+fold from 37cfbdfba5; mutation: nocrossjum / borrowed ops10 from be38873796; mutation: scale=3
- `870c24c9cf`: from carried from archived-20261006-175959/db.jsonl: 776c86e476, then mutation: escape=2 / mutation: varslot=1 / crossover; mutation: noreorder=1, rtloopall=0
- `d05d104578`: from carried from archived-20261006-175959/db.jsonl: 301a268219, then crossover; mutation: noreorder=0, super + R>->DUP = / borrowed escape+ops10+supers from e373839dcb; mutation: sharedcall=1 / mutation: -spec small
- `ae5d7cdaae`: from carried from archived-20261006-175959/db.jsonl: 76ab789fed, then crossover; mutation: tail=1 / crossover; mutation: tracer=1 / crossover; mutation: scale=1 / crossover; mutation: -Os, t2hot=0.02
- `8f0973fc8f`: from carried from archived-20261006-175959/db.jsonl: 301a268219, then crossover; mutation: noreorder=0, super + R>->DUP = / borrowed escape+ops10+supers from e373839dcb; mutation: sharedcall=1
- `635a47fd26`: from carried from archived-20261006-175959/db.jsonl: 2a2c2b4256, then borrowed ops10+supers from 2f16321733
- `b00da878bf`: from carried from archived-20261006-175959/db.jsonl: 301a268219, then crossover; mutation: noreorder=0, super + R>->DUP = / crossover
- `4542a08fb0`: from carried from archived-20261006-175959/db.jsonl: 4542a08fb0, then (itself)
- `2f4c1d82ec`: from carried from archived-20261006-175959/db.jsonl: 776c86e476, then mutation: escape=2 / mutation: varslot=1 / mutation: tfind=0 / mutation: -spec loc
- `263788ab64`: from carried from archived-20261006-175959/db.jsonl: 776c86e476, then mutation: escape=2 / mutation: varslot=1 / crossover; mutation: msc=1, -super SWAP R> / crossover; mutation: rtimm=0
- `f69da4fcc8`: from carried from archived-20261006-175959/db.jsonl: 4542a08fb0, then crossover; mutation: noreorder=0

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.147 | 25144 | no |
| s1-sod16 | 1.510 | 16304 | no |
| s2-cpt16 | 1.219 | 15384 | no |
| s3-cpt16f | 1.130 | 15200 | no |
| s4-cv8 | 1.147 | 14152 | no |
| s5-cv8spec | 0.951 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 83

