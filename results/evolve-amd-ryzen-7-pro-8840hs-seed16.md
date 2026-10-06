# Seed 16 on the AMD Ryzen 7 PRO 8840HS (Iteration 72)

The first run in the two-bit tag (FORMAT-TAG2.md): `seed 16 tag2`, commit
10af4929 - every design entering the run in the tag, the newest four
fronts carried in re-encoded (59 designs), t2hot to choose. 54 minutes.
Measured again with seeds 12-15 (session 14, calibration 1.001).

**Its front is the old front moved ~370 bytes right at about its speed:**

| seed 16 (tag 2) | size | speed | best old-format design no larger | ratio |
|---|---|---|---|---|
| 0826d64cd9 | 7,009 | 0.424 | 773f6d9daf 0.242 at 6,993 | 1.752 |
| 323f2ccfb8 | 7,105 | 0.330 | 773f6d9daf 0.242 at 6,993 | 1.364 |
| 19104ead72 | 7,225 | 0.303 | 285b6909d1 0.240 at 7,172 | 1.262 |
| 4bb0870716 | 7,226 | 0.258 | 285b6909d1 0.240 at 7,172 | 1.075 |
| 4446c9069e | 7,274 | 0.250 | 285b6909d1 0.240 at 7,172 | 1.042 |
| 343d881df1 | 7,708 | 0.243 | 8298ca5d59 0.236 at 7,310 | 1.030 |

From 7.2 KB up within 3-8% of the old front; at the small end the old
front's fastest small designs (0.24 at 6.8-7.0 KB) became ~7.2 KB in the
tag, so the tag's smallest designs are its slower ones. The price of the
format, as Iteration 69 counted it: +5-6% size, +2-3% dispatches.

t2hot on the front: static 4, 0.05 4, 0.02 2, 0 1 - toward size.
Multi-state caching on 4 of 11.

## The run's report

# Evolved VM designs

1327 designs evaluated, 1250 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus, loop,
relative to s6-cv8b; size is the self-hosting image. sieve is held out.

## The Pareto front

| design | speed | re-measured | size | sieve (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| 343d881df1 | 0.232 | 0.242 | 7708 | 0.590 | opt=O3; nocrossjump=1; nocet=1; peel=1; tracer=1; d256=1; guard=1; -C@; 5 pairs: DUP R@, >R C!, C@ OR, >R OVER, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),(?DO),<?BRANCH8,=I?BRANCH8,J,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,DUP?BRANCH,<>?BRANCH,(LOOP),DUP?NBRANCH,I,(+LOOP),>?BRANCH,?NBRANCH8,BRANCH8,UNLOOP; escape=2; lean=1; rtloop=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1 | borrowed rtloop+rtloopall+rtiplus+swapi from 68d7bfa4bf; mut |
| 4446c9069e | 0.234 | 0.239 | 7274 | 0.468 | opt=O3; nocet=1; noreorder=1; peel=1; ipaclone=1; varslot=0; guard=1; -OVER; 4 pairs: DUP >R, C@ =, C@ OR, >R OVER; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,(DO),(?DO),<?BRANCH8,=I?BRANCH8,<?BRANCH,J,OVER?BRANCH8,<>?BRANCH8,EXECUTE,DUP?NBRANCH8,DUP?BRANCH,<>?BRANCH,UNLOOP,(LOOP),DUP?NBRANCH,(LEAVE),I,(+LOOP),?NBRANCH8,BRANCH8,DUP?BRANCH8,=I?BRANCH; escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=2 | crossover; mutation: +super LSHIFT LSHIFT |
| 4bb0870716 | 0.249 | 0.250 | 7226 | 0.528 | opt=O3; nocrossjump=1; nocet=1; tracer=1; spec=loc,tiny,small,imm; guard=1; -AND; 5 pairs: DUP @, + R>, OVER C@, >R OVER, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8; escape=2; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=2 | mutation: varslot=1 |
| 19104ead72 | 0.295 | 0.308 | 7225 | 0.597 | opt=O3; nocrossjump=1; nocet=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; -AND; 5 pairs: DUP @, + R>, OVER C@, OVER R>, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,DUP?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,>?BRANCH8,0<?BRANCH,<?BRANCH,OVER?BRANCH8,CMOVE,<?BRANCH8; escape=2; msc=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=3 | crossover; mutation: tracer=0 |
| bfa7370096 | 0.304 | 0.326 | 7202 | 0.750 | opt=O3; nocet=1; noreorder=1; ipaclone=1; tracer=1; guard=1; -DUP; 4 pairs: DUP @, + R>, OVER C@, LSHIFT OVER; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),U<?BRANCH,?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,<?BRANCH,J,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8,OVER?BRANCH8,?NBRANCH8,>?BRANCH,0<?BRANCH; escape=2; msc=1; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=1 | mutation: varslot=1, tail=1 |
| 2b5e92dd57 | 0.308 | 0.345 | 7186 | 0.602 | opt=O3; nocet=1; peel=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -AND; 7 pairs: DUP @, + R>, OVER C@, >R OVER, ...; rtfuse=0; ops10=THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8; escape=2; msc=1; lean=1; rtloop=1; rtloopall=1; bss=1; kfast=1; tfind=1; kinput=1; thinhdr=1; tag2=1; t2hot=2 | mutation: varslot=0 |
| 7c49a5ffca | 0.322 | 0.324 | 7123 | 0.807 | opt=O3; nocrossjump=1; nocet=1; peel=1; tracer=1; tos=0; d256=1; guard=1; -@; 6 pairs: DUP R@, SWAP DUP, >R C!, SWAP R>, ...; rtfuse=0; ops10=(FIND),(>NUMBER),SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,?BRANCH8,?NBRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),<?BRANCH8,0<?BRANCH,J,?NBRANCH8,EXECUTE,DUP?NBRANCH8,DUP?BRANCH,<>?BRANCH,UNLOOP,(LOOP),OVER?BRANCH,BRANCH8,DUP?NBRANCH,>?BRANCH,(LEAVE),I,(+LOOP),SWAP+I,<?BRANCH,THREAD-FIND,+!,(?DO),<>?BRANCH8; escape=2; lean=1; bss=1; kfast=1; kinput=1; klookup=1; thinhdr=1; tag2=1 | crossover; mutation: tos=0 |
| 323f2ccfb8 | 0.324 | 0.334 | 7105 | 0.733 | opt=O3; nocrossjump=1; nocet=1; tracer=1; guard=1; -!; 5 pairs: DUP R@, >R C!, C@ OR, >R OVER, ...; rtfuse=0; ops10=(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,?BRANCH8,?NBRANCH,CMOVE,>?BRANCH8,0<?BRANCH8,DUP?BRANCH8,(DO),(?DO),<?BRANCH8,SWAP+I,=I?BRANCH8,J,OVER?BRANCH8,<>?BRANCH8,=I?BRANCH,EXECUTE,DUP?NBRANCH8,<>?BRANCH,(LOOP),DUP?NBRANCH,I,(+LOOP),>?BRANCH,?NBRANCH8,BRANCH8,UNLOOP,(LEAVE); escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=2 | crossover; mutation: super R> =->XOR C! |
| df2ac6c7ab | 0.325 | 0.338 | 7050 | 0.763 | opt=O3; nocrossjump=1; nocet=1; ipaclone=1; tracer=1; spec=loc,tiny,small,imm; guard=1; -AND; 5 pairs: DUP @, + R>, OVER C@, >R OVER, ...; rtfuse=0; ops10=SWAP+I,(FIND),(>NUMBER),THREAD-FIND,SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,<>?BRANCH,CMOVE,0<?BRANCH8,DUP?BRANCH8,(DO),I,(?DO),<?BRANCH8,=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,>?BRANCH,?NBRANCH,DUP?NBRANCH,>?BRANCH8; escape=2; lean=1; bss=1; kfast=1; tfind=1; kinput=1; klookup=1; thinhdr=1; swapi=1; tag2=1; t2hot=3 | mutation: t2hot=100.0 |
| 69270766bd | 0.359 | 0.372 | 7049 | 0.769 | opt=O3; nocet=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -NEGATE; 6 pairs: DUP @, + R>, OVER C@, LSHIFT OVER, ...; rtfuse=0; ops10=(FIND),(>NUMBER),SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,(?DO),<?BRANCH8,=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,>?BRANCH8,THREAD-FIND,0<?BRANCH,OVER?BRANCH; escape=2; lean=1; bss=1; kfast=1; kinput=1; klookup=1; thinhdr=1; tag2=1; t2hot=3 | crossover; mutation: sharedcall=0 |
| 0826d64cd9 | 0.406 | 0.420 | 7009 | 0.782 | opt=O3; nocet=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; varslot=0; guard=1; -C!; 8 pairs: DUP @, + R>, OVER C@, LSHIFT OVER, ...; rtfuse=0; ops10=SCAN,SKIP,TABS>BL,FILL,(PARSE),HASH,PLACE,+!,?DUP,(LOOP),(LEAVE),?BRANCH8,CMOVE,0<?BRANCH8,DUP?BRANCH8,I,<?BRANCH8,=I?BRANCH8,UNLOOP,J,?NBRANCH8,BRANCH8,<>?BRANCH8,(+LOOP),DUP?NBRANCH8,=I?BRANCH,DUP?BRANCH,EXECUTE,SWAP+I,>?BRANCH,?NBRANCH,>?BRANCH8,THREAD-FIND,0<?BRANCH,(DO),DUP?NBRANCH; escape=2; lean=1; bss=1; kfast=1; kinput=1; thinhdr=1; tag2=1; t2hot=3 | crossover; mutation: -super >R OVER |

## How the front came about

- `343d881df1`: from tag 2 of archived-20261006-131903/db.jsonl: eb0033be3d, then crossover; mutation: fold RSHIFT->DROP / crossover; mutation: rtloopall=0, d256=1 / crossover; borrowed rtloop from 8904ba7f81; mutation: scale=3, hotcall / borrowed rtloop+rtloopall+rtiplus+swapi from 68d7bfa4bf; mutation: hot
- `4446c9069e`: from tag 2 of archived-20261006-131903/db.jsonl: eb0033be3d, then crossover; mutation: fold RSHIFT->DROP / crossover; borrowed rtimm from 5542092907; mutation: msc=0, msc=1 / borrowed tag2+t2hot from fe4e337835; mutation: super R> =->NEGATE NEGA / mutation: swapi=1, tfind=0 / crossover; mutation: +super LSHIFT LSHIFT
- `4bb0870716`: from tag 2 of archived-20261006-024824/db.jsonl: 3995ab7bde, then crossover; mutation: thinhdr=1 / mutation: tracer=1 / crossover; mutation: msc=0 / mutation: varslot=1
- `19104ead72`: from tag 2 of archived-20261006-024824/db.jsonl: 3995ab7bde, then crossover; mutation: thinhdr=1 / mutation: tracer=1 / crossover; mutation: msc=0 / mutation: varslot=1 / borrowed rtloop+rtloopall+rtiplus+swapi from 76f7932a6f; mutation: hot / mutation: t2hot=0.02, ipaclone=1 / crossover; borrowed lean from 28d7fd0144; mutation: tfind=1 / crossover; mutation: tracer=0
- `bfa7370096`: from tag 2 of archived-20261006-024824/db.jsonl: 3995ab7bde, then crossover; mutation: tos=1, hotcalls=0 / crossover; mutation: rtimm=0 / crossover; mutation: +op U<?BRANCH / mutation: nocet=1, t2hot=0.0 / mutation: varslot=1, tail=1
- `2b5e92dd57`: from tag 2 of archived-20261006-131903/db.jsonl: ce2e13ce87, then borrowed escape+ops10+supers from 7806d89778; mutation: scale=1, varsl / mutation: t2hot=0.05 / mutation: varslot=0
- `7c49a5ffca`: from crossover; mutation: tag2=0, then mutation: rtloopall=0, tfind=0 / crossover; mutation: nocet=1 / borrowed folds from c5d224da5e; mutation: ipaclone=0, align1=1 / mutation: t2hot=100.0, varslot=0 / mutation: fold R@->C!, swapi=0 / mutation: ipaclone=1 / crossover; mutation: hotcalls=8, rtiplus=1 / crossover; mutation: tos=0
- `323f2ccfb8`: from tag 2 of archived-20261006-131903/db.jsonl: eb0033be3d, then crossover; mutation: fold RSHIFT->DROP / crossover; mutation: rtloopall=0, d256=1 / crossover; borrowed rtloop from 8904ba7f81; mutation: scale=3, hotcall / crossover; mutation: super R> =->XOR C!
- `df2ac6c7ab`: from tag 2 of archived-20261006-024824/db.jsonl: 3995ab7bde, then crossover; mutation: thinhdr=1 / mutation: tracer=1 / crossover; mutation: msc=0 / mutation: varslot=1 / borrowed rtloop+rtloopall+rtiplus+swapi from 76f7932a6f; mutation: hot / mutation: t2hot=0.02, ipaclone=1 / mutation: t2hot=100.0
- `69270766bd`: from tag 2 of archived-20261006-131903/db.jsonl: ce2e13ce87, then borrowed escape+ops10+supers from 7806d89778; mutation: scale=1, varsl / mutation: t2hot=0.05 / mutation: varslot=0 / mutation: rtloop=0 / borrowed rtloopall from d40d3f296a; mutation: tracer=0 / borrowed folds+supers from d40d3f296a; mutation: -super DUP R@ / borrowed sharedcall+d256 from 2b5e92dd57; mutation: fold C@->DUP / crossover; mutation: sharedcall=0
- `0826d64cd9`: from borrowed escape+ops10+supers from 7806d89778; mutation: scale=1, varslot=1, then mutation: t2hot=0.05 / mutation: varslot=0 / mutation: rtloop=0 / borrowed rtloopall from d40d3f296a; mutation: tracer=0 / borrowed folds+supers from d40d3f296a; mutation: -super DUP R@ / borrowed sharedcall+d256 from 2b5e92dd57; mutation: fold C@->DUP / crossover; mutation: sharedcall=0 / crossover; mutation: -super >R OVER

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.145 | 25144 | no |
| s1-sod16 | 1.514 | 16304 | no |
| s2-cpt16 | 1.171 | 15384 | no |
| s3-cpt16f | 1.132 | 15200 | no |
| s4-cv8 | 1.121 | 14152 | no |
| s5-cv8spec | 0.941 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 70
- died: image did not convert (AssertionError: LOOPTAB: rtloopall needs all eight loop opcodes): 6
- died: image did not convert (NameError: name 'json' is not defined. Did you forget to import 'json'?): 1

