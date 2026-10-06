# Seed 17 on the AMD Ryzen 7 PRO 8840HS (Iteration 76)

The second run in the two-bit tag: `seed 17 tag2`, commit 248cb518 - the
newest four fronts carried in, re-encoded (57 designs); 34 minutes. The
last run under the old rules (speed and image size; engines with the C
library). Measured again with seeds 13-16 (session 15, calibration 0.993).

**The first designs in the tag on the front of all runs:**

| design | size | speed | against |
|---|---|---|---|
| a36dc45e12 | 7,283 | 0.233 | best old design no larger: 0.244 at 7,172 (0.955); old fastest 0.230 at 7,958 |
| 5671742b27 | 7,690 | 0.233 | |

Seed 17's front against seed 16's (both in the tag, this session): the
smallest the same, 7,009 bytes (0.413); the fastest 0.233 at 7,283 against
0.243 at 7,708 - 4.1% faster, 425 bytes smaller. Of the two runs' joint
tag-2 front, 9 of 12 designs are seed 17's. From 7.2 KB up the tag's
price is won back; at 7.0-7.1 KB its designs are 1.28-1.69 of the old
format's small ones, ~350 bytes smaller.

**How**: both front designs leave out multi-state caching (msc=0) -
whose handler copies cost ~20 KB of engine (Iteration 75) - and take up
swapi for the first time in any run, with a 256-entry table; a36dc45e12
also rtloopall (loop opcodes at run time). t2hot the default, 0.02.

## The run's report

# Evolved VM designs

1328 designs evaluated, 1230 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus, loop,
relative to s6-cv8b; size is the self-hosting image. sieve is held out.

## The Pareto front

| design | speed | re-measured | size | engine KB | peak RSS MB | sieve (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|---|---|
| 5671742b27 | 0.224 | 0.234 | 7690 | 17.2 | 1.2 | 0.566 | opt=O3; nocrossjump=1; nocet=1; peel=1; tracer=1; d256=1; guard=1; -RSHIFT; 5 pairs: DUP R@, C@ OR, >R OVER, @ <, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),<?BRANCH8,=I?BRANCH8,J,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,(LOOP),DUP?NBRANCH,I,(+LOOP),>?BRANCH,?NBRANCH8,BRANCH8,UNLOOP,(LEAVE),DUP?BRANCH,<>?BRANCH; escape=2; lean=1; rtloop=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1 | borrowed kfast+tfind+kinput+klookup from 2b7e66e1f3; mutatio |
| a36dc45e12 | 0.231 | 0.235 | 7283 | 17.3 | 1.2 | 0.547 | opt=O3; nocrossjump=1; nocet=1; tracer=1; d256=1; guard=1; -R>; 5 pairs: DUP R@, >R C!, C@ OR, XOR C!, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),(?DO),<?BRANCH8,=I?BRANCH8,J,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,(LOOP),DUP?NBRANCH,THREAD-FIND,I,(+LOOP),?NBRANCH8,BRANCH8,UNLOOP,(LEAVE),DUP?BRANCH,<>?BRANCH; escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1 | crossover; mutation: -super @ < |
| 2b55d23a18 | 0.245 | 0.251 | 7266 | 45.2 | 1.2 | 0.450 | opt=O3; nocet=1; ipaclone=1; guard=1; -OVER; 4 pairs: DUP >R, C@ =, >R OVER, NEGATE NEGATE; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,0<?BRANCH8,(DO),(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,J,OVER?BRANCH8,<>?BRANCH8,EXECUTE,DUP?NBRANCH8,DUP?BRANCH,<>?BRANCH,UNLOOP,(LOOP),DUP?NBRANCH,(LEAVE),I,(+LOOP),?NBRANCH8,BRANCH8,DUP?BRANCH8,U<?BRANCH,>?BRANCH; escape=2; msc=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=2 | mutation: noreorder=0 |
| 38de166d54 | 0.248 | 0.267 | 7234 | 17.1 | 1.2 | 0.530 | opt=O3; nocrossjump=1; nocet=1; peel=1; tracer=1; spec=loc,tiny,small,imm; guard=1; -< -OR; 7 pairs: OVER C@, LSHIFT OVER, R> SWAP, >R C!, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,(LOOP),(LEAVE),?BRANCH8,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,>?BRANCH8,0<?BRANCH,(DO),<>?BRANCH,DUP?NBRANCH; escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=2 | crossover; mutation: +op HASH |
| 2b7e66e1f3 | 0.252 | 0.260 | 7226 | 17.1 | 1.2 | 0.528 | opt=O3; nocrossjump=1; nocet=1; peel=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; guard=1; -AND; 5 pairs: DUP @, + R>, OVER C@, >R OVER, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8; escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=2 | borrowed rtfuse+rtimm from 0826d64cd9; mutation: peel=1 |
| 6583b9f742 | 0.260 | 0.277 | 7218 | 16.7 | 1.2 | 0.535 | opt=O3; nocrossjump=1; nocet=1; tracer=1; spec=tiny,small,imm; varslot=0; guard=1; -= -R@; 7 pairs: DUP @, OVER C@, LSHIFT OVER, R> SWAP, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,>?BRANCH8,0<?BRANCH,(DO); escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=3 | mutation: -fold = |
| ce3a84b4a0 | 0.291 | 0.307 | 7217 | 16.2 | 1.2 | 0.591 | opt=O3; nocet=1; noreorder=1; peel=1; ipaclone=1; spec=tiny,small,imm; varslot=0; guard=1; -C@ -R>; 7 pairs: DUP @, + R>, OVER C@, R> SWAP, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,>?BRANCH8,0<?BRANCH,OVER?BRANCH,(DO); escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=3 | crossover; mutation: noreorder=1 |
| e6a3c1fb8c | 0.303 | 0.318 | 7130 | 17.3 | 1.2 | 0.756 | opt=O3; nocrossjump=1; nocet=1; tracer=1; d256=1; guard=1; -C@; 6 pairs: DUP R@, >R C!, XOR C!, LSHIFT OVER, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),(?DO),<?BRANCH8,=I?BRANCH8,J,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,(LOOP),DUP?NBRANCH,THREAD-FIND,I,(+LOOP),?NBRANCH8,BRANCH8,UNLOOP,(LEAVE),DUP?BRANCH,<>?BRANCH; escape=2; lean=1; bss=1; kfast=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1 | crossover; mutation: bytehdr=0 |
| a1578b537c | 0.320 | 0.334 | 7120 | 17.1 | 1.2 | 0.790 | opt=O3; nocrossjump=1; nocet=1; tracer=1; spec=loc,var,tiny,small; guard=1; -!; 5 pairs: DUP R@, >R C!, C@ OR, >R OVER, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),(?DO),<?BRANCH8,SWAP+I,=I?BRANCH8,J,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,<>?BRANCH,(LOOP),DUP?NBRANCH,I,(+LOOP),>?BRANCH,?NBRANCH8,BRANCH8,UNLOOP,(LEAVE); escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=2 | mutation: -spec imm |
| 323f2ccfb8 | 0.323 | 0.337 | 7105 | 17.1 | 1.2 | 0.750 | opt=O3; nocrossjump=1; nocet=1; tracer=1; guard=1; -!; 5 pairs: DUP R@, >R C!, C@ OR, >R OVER, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),(?DO),<?BRANCH8,SWAP+I,=I?BRANCH8,J,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,<>?BRANCH,(LOOP),DUP?NBRANCH,I,(+LOOP),>?BRANCH,?NBRANCH8,BRANCH8,UNLOOP,(LEAVE); escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=2 | carried from archived-20261006-160616/db.jsonl: 323f2ccfb8 |
| 31e4e22b2e | 0.323 | 0.343 | 7085 | 16.2 | 1.1 | 0.732 | opt=O3; nocet=1; noreorder=1; peel=1; ipaclone=1; tracer=1; spec=var,tiny,small,imm; varslot=0; guard=1; -OVER; 4 pairs: DUP >R, C@ =, C@ OR, >R OVER; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,(DO),(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,J,OVER?BRANCH8,<>?BRANCH8,EXECUTE,DUP?NBRANCH8,DUP?BRANCH,<>?BRANCH,UNLOOP,(LOOP),DUP?NBRANCH,(LEAVE),I,(+LOOP),?NBRANCH8,BRANCH8,DUP?BRANCH8,=I?BRANCH; escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=2 | mutation: tracer=1 |
| 0c5782b28a | 0.326 | 0.343 | 7073 | 16.6 | 1.2 | 0.763 | opt=O3; nocet=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; -LIT; 5 pairs: DUP @, OVER C@, LSHIFT OVER, R> SWAP, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,J,BRANCH8,<>?BRANCH8,(+LOOP),=I?BRANCH,DUP?BRANCH,?NBRANCH,>?BRANCH8,OVER?BRANCH8,?NBRANCH8,>?BRANCH,0<?BRANCH,=I?BRANCH8,UNLOOP,EXECUTE; escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=2 | mutation: t2hot=0.05 |
| 4ba5b2c147 | 0.329 | 0.338 | 7057 | 16.6 | 1.2 | 0.744 | opt=O3; nocet=1; noreorder=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; -LIT; 5 pairs: DUP @, OVER C@, LSHIFT OVER, R> SWAP, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,J,BRANCH8,<>?BRANCH8,(+LOOP),=I?BRANCH,DUP?BRANCH,?NBRANCH,>?BRANCH8,OVER?BRANCH8,?NBRANCH8,>?BRANCH,0<?BRANCH,=I?BRANCH8,UNLOOP,EXECUTE; escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=3 | crossover; mutation: tracer=0, t2hot=100.0 |
| 3405116655 | 0.334 | 0.353 | 7049 | 16.8 | 1.2 | 0.744 | opt=O3; nocrossjump=1; nocet=1; tracer=1; spec=tiny,small,imm; varslot=0; d256=1; guard=1; -OVER; 6 pairs: DUP R@, >R C!, OVER C@, LSHIFT OVER, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),(?DO),<?BRANCH8,SWAP+I,=I?BRANCH8,J,OVER?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,<>?BRANCH,(LOOP),I,(+LOOP),>?BRANCH,?NBRANCH8,BRANCH8,UNLOOP,(LEAVE),DUP?BRANCH; escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=3 | crossover; mutation: d256=1 |
| a1ff4b8022 | 0.391 | 0.388 | 7043 | 16.1 | 1.2 | 0.858 | opt=O3; nocet=1; noreorder=1; tracer=1; spec=tiny,small,imm; varslot=0; guard=1; -C! -XOR; 7 pairs: DUP @, LSHIFT OVER, R> SWAP, SWAP DUP, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,<?BRANCH8,=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,>?BRANCH8,0<?BRANCH,(DO),DUP?NBRANCH; escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=3 | crossover; borrowed ops10 from ea27f86ca3; mutation: rtloop= |
| 3d312e796e | 0.403 | 0.419 | 7009 | 14.5 | 1.2 | 0.729 | opt=O3; nocet=1; noreorder=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -C!; 8 pairs: DUP @, + R>, OVER C@, LSHIFT OVER, ...; rtfuse=0; ops10=SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,<?BRANCH8,=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,>?BRANCH8,THREAD-FIND,0<?BRANCH,(DO),DUP?NBRANCH; escape=2; lean=1; bss=1; kfast=1; kinput=1; thinhdr=1; tag2=1; t2hot=3 | mutation: noreorder=1 |

## How the front came about

- `5671742b27`: from carried from archived-20261006-160616/db.jsonl: 323f2ccfb8, then crossover; borrowed bss+thinhdr from df2ac6c7ab; mutation: d256=1 / crossover; mutation: swapi=0 / mutation: tfind=0, swapi=1 / borrowed kfast+tfind+kinput+klookup from 2b7e66e1f3; mutation: peel=1
- `a36dc45e12`: from carried from archived-20261006-160616/db.jsonl: 323f2ccfb8, then crossover; borrowed bss+thinhdr from df2ac6c7ab; mutation: d256=1 / crossover; mutation: -super @ <
- `2b55d23a18`: from carried from archived-20261006-160616/db.jsonl: 4446c9069e, then borrowed lean from 46d5de3a9c; mutation: -spec loc / crossover; mutation: bytehdr=0 / mutation: noreorder=0
- `38de166d54`: from carried from archived-20261006-160616/db.jsonl: 69270766bd, then mutation: -spec loc / crossover; mutation: varslot=0, swapi=1 / mutation: -fold = / crossover; mutation: +op HASH
- `2b7e66e1f3`: from carried from archived-20261006-160616/db.jsonl: df2ac6c7ab, then crossover; mutation: scale=1 / borrowed rtfuse+rtimm from 0826d64cd9; mutation: peel=1
- `6583b9f742`: from carried from archived-20261006-160616/db.jsonl: 69270766bd, then mutation: -spec loc / crossover; mutation: varslot=0, swapi=1 / mutation: -fold =
- `ce3a84b4a0`: from carried from archived-20261006-160616/db.jsonl: 69270766bd, then mutation: -spec loc / mutation: scale=1, swapi=1 / crossover; mutation: noreorder=1
- `e6a3c1fb8c`: from carried from archived-20261006-160616/db.jsonl: 323f2ccfb8, then crossover; borrowed bss+thinhdr from df2ac6c7ab; mutation: d256=1 / crossover; mutation: -super @ < / crossover; mutation: bytehdr=0
- `a1578b537c`: from carried from archived-20261006-160616/db.jsonl: 323f2ccfb8, then mutation: -spec imm
- `323f2ccfb8`: from carried from archived-20261006-160616/db.jsonl: 323f2ccfb8, then (itself)
- `31e4e22b2e`: from carried from archived-20261006-160616/db.jsonl: 4446c9069e, then borrowed lean from 46d5de3a9c; mutation: -spec loc / mutation: rtloop=0 / mutation: tracer=1
- `0c5782b28a`: from carried from archived-20261006-160616/db.jsonl: bfa7370096, then crossover; mutation: tracer=0, t2hot=100.0 / mutation: noreorder=0 / mutation: t2hot=0.05
- `4ba5b2c147`: from carried from archived-20261006-160616/db.jsonl: bfa7370096, then crossover; mutation: tracer=0, t2hot=100.0
- `3405116655`: from carried from archived-20261006-160616/db.jsonl: 323f2ccfb8, then crossover; mutation: d256=1
- `a1ff4b8022`: from carried from archived-20261006-160616/db.jsonl: 69270766bd, then mutation: -spec loc / crossover; mutation: varslot=0, swapi=1 / mutation: -fold = / crossover; borrowed ops10 from ea27f86ca3; mutation: rtloop=0
- `3d312e796e`: from carried from archived-20261006-160616/db.jsonl: 0826d64cd9, then mutation: noreorder=1

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.128 | 25144 | no |
| s1-sod16 | 1.460 | 16304 | no |
| s2-cpt16 | 1.142 | 15384 | no |
| s3-cpt16f | 1.128 | 15200 | no |
| s4-cv8 | 1.110 | 14152 | no |
| s5-cv8spec | 0.933 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 86
- died: image did not convert (AssertionError: LOOPTAB: rtloopall needs all eight loop opcodes): 12

