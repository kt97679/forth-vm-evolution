# Seed 9 on the AMD Ryzen 7 PRO 8840HS (Iteration 45)

The first run that could choose `rtloopall` and `bss` (Iterations 43-44).
Commit 807d0d63, `seed 9` from NEXT-RUN, pop 32 x 40 generations, 3 rounds,
by the median: 40 minutes, 1,309 designs, 1,190 alive. Measured again with
every earlier front in one session (session 7, calibration 1.000, the two
CPUs' ranks agreeing 1.00): **the small end is seed 9's - 0.794 at 7,019
bytes, the smallest yet, to 0.515 at 7,725** - eight of the fifteen
designs on the front of all runs, every one smaller than anything before
(seed 8's smallest: 8,034). Seed 8 keeps the rest, 0.508 at 8,614 to the
fastest, 0.442 at 13,073: seed 9's own fastest were 0.493-0.502.

## The genes

| | generation 0 (29) | living (1,190) | seed 9's front (8) |
|---|---|---|---|
| bss | 0 | 945 (79%) | 8 |
| lean | - | 916 (77%) | 8 |
| rtloop | - | 416 (35%) | 3 (the three fastest) |
| rtloopall, expressed | 0 | - | 2 |

## What did not compound

Every seed starts from the same founders, so what one run found the next
must find again. Seed 8's front built with this commit's two free genes -
bss, and rtloopall where all eight loop opcodes are there - their speeds as
session 7 measured them (neither gene moves a selected workload's
dispatches, Iterations 43-44), their sizes built and their life checked
on the development VM:

| seed 8 design | speed (session 7) | recorded | with bss and rtloopall | life |
|---|---|---|---|---|
| 85cac726b5 | 0.508 | 8,614 | 7,178 | alive |
| f85a63f8c7 | 0.502 | 8,647 | 7,220 | alive |
| 1b602bc9bd | 0.500 | 8,671 | 7,212 | alive |
| 72ca2cf497 | 0.487 | 8,990 | 7,532 | alive |
| 959e88b0f5 | 0.469 | 9,140 | 7,714 | alive |
| 577c999e62 | 0.466 | 9,278 | 7,820 | alive |
| 9bb527944a | 0.442 | 13,073 | 11,569 | alive |

**Projected, these dominate every design of seed 9's front from 7,178
bytes up** (seed 9: 0.515-0.546 at 7.5-7.7 KB; 85cac726b5 alone: 0.508 at
7,178) - seed 9 would keep only its five smallest. Not measured on the
laptop: layout moves timings a percent or two.

## The run's report

# Evolved VM designs

1309 designs evaluated, 1190 alive. Speed is the geometric mean of median cpu time / hand-made s6 over kernel, fib, parse, corpus, loop,
relative to s6-cv8b; size is the self-hosting image. sieve is held out.

## The Pareto front

| design | speed | re-measured | size | sieve (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| 9d89f6ba0e | 0.487 | 0.487 | 13065 | 0.677 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; ipaclone=1; tracer=1; bytehdr=0; guard=1; 21 pairs: C! R>, >R C!, >R OVER, OVER R>, ...; rtfuse=0; ops10=<?BRANCH8,=I?BRANCH8,SWAP+I,(LOOP),DUP?BRANCH8,I,?BRANCH8,?NBRANCH,J,0<?BRANCH,<>?BRANCH,>?BRANCH8; escape=1; msc=1; hotcalls=16; rtloop=1; bss=1 | mutation: guard=1 |
| f084674b22 | 0.492 | 0.516 | 9198 | 0.665 | opt=O3; nocet=1; ipaclone=1; tracer=1; 24 pairs: >R OVER, C@ =, OVER R>, R> SWAP, ...; rtfuse=0; ops10=<?BRANCH8,SWAP+I,(LOOP),0<?BRANCH8,I,?BRANCH8,?NBRANCH,EXECUTE,<>?BRANCH,>?BRANCH8,=I?BRANCH,U<?BRANCH8,(?DO); escape=2; msc=1; hotcalls=16; rtloop=1; bss=1 | mutation: lean=0 |
| 45d2ff7e01 | 0.497 | 0.500 | 7725 | 0.645 | opt=O3; nocet=1; peel=1; tracer=1; 24 pairs: >R OVER, C@ =, OVER R>, R> SWAP, ...; rtfuse=0; ops10=<?BRANCH8,SWAP+I,(LOOP),0<?BRANCH8,I,?BRANCH8,?NBRANCH,EXECUTE,<>?BRANCH,>?BRANCH8,=I?BRANCH,U<?BRANCH8,(?DO); escape=2; msc=1; hotcalls=16; lean=1; rtloop=1; bss=1 | mutation: peel=1 |
| fa23f401cd | 0.522 | 0.525 | 7692 | 0.649 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; peel=1; ipaclone=1; tracer=1; 22 pairs: C! R>, >R OVER, OVER R>, R> SWAP, ...; rtfuse=0; ops10=<?BRANCH8,=I?BRANCH8,SWAP+I,(LOOP),I,?BRANCH8,?NBRANCH,J,0<?BRANCH,<>?BRANCH,>?BRANCH8,(DO); escape=1; msc=1; hotcalls=16; lean=1; rtloop=1; bss=1 | mutation: rtimm=1, peel=1 |
| 853cfb9d36 | 0.539 | 0.536 | 7651 | 0.629 | opt=O3; nocet=1; peel=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; 21 pairs: OVER R>, R> SWAP, DUP @, C@ OVER, ...; rtfuse=0; ops10=SWAP+I,(LOOP),I,?BRANCH8,?NBRANCH,EXECUTE,<>?BRANCH,>?BRANCH8,U<?BRANCH8,(?DO),DUP?BRANCH8,BRANCH8,=?BRANCH8; escape=1; msc=1; hotcalls=8; lean=1; rtloop=1; bss=1 | mutation: align1=0 |
| 2367cb920c | 0.541 | 0.538 | 7510 | 0.632 | nocet=1; noreorder=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; 19 pairs: C! R>, DUP C@, >R OVER, C@ =, ...; rtfuse=0; ops10=I,>?BRANCH8,=I?BRANCH,DUP?BRANCH8,SWAP+I,U<?BRANCH8,(?DO),(LOOP),?BRANCH8,0<?BRANCH8,UNLOOP,<>?BRANCH,BRANCH8,EXECUTE,=?BRANCH8; escape=1; msc=1; hotcalls=32; lean=1; rtloop=1; bss=1 | crossover; mutation: sharedcall=0 |
| 88792f1798 | 0.644 | 0.653 | 7220 | 0.848 | opt=O3; nocet=1; tracer=1; 24 pairs: >R OVER, C@ =, OVER R>, R> SWAP, ...; rtfuse=0; ops10=<?BRANCH8,SWAP+I,(LOOP),0<?BRANCH8,I,?BRANCH8,?NBRANCH,EXECUTE,<>?BRANCH,>?BRANCH8,=I?BRANCH,U<?BRANCH8,(?DO); escape=2; msc=1; hotcalls=16; lean=1; bss=1 | borrowed scale+bytehdr+doesfar from 03a197f9bc; mutation: rt |
| ccce4784b8 | 0.670 | 0.681 | 7091 | 0.836 | nocet=1; ipaclone=1; spec=loc,tiny,small,imm; guard=1; 24 pairs: >R OVER, C@ =, OVER R>, DUP @, ...; rtfuse=0; ops10=?BRANCH8,<>?BRANCH,DUP?BRANCH8,SWAP+I,>?BRANCH8,<?BRANCH8,EXECUTE,?NBRANCH,=I?BRANCH,BRANCH8,=I?BRANCH8,I,(DO); escape=2; msc=1; hotcalls=32; lean=1; bss=1 | mutation: hotcalls=32 |
| ee4d8f8a50 | 0.705 | 0.723 | 7027 | 0.872 | nocet=1; noreorder=1; spec=tiny,small,imm; varslot=0; guard=1; -R@; 22 pairs: ROT DUP, DUP C@, >R OVER, OVER C@, ...; rtfuse=0; ops10=I,U<?BRANCH8,=?BRANCH8,(+LOOP),(LOOP),?BRANCH8,DUP?BRANCH8,>?BRANCH8,BRANCH8,=I?BRANCH8,<?BRANCH8,?DUP,?NBRANCH; escape=1; msc=1; hotcalls=32; lean=1; bss=1 | mutation: -fold R@ |
| 57d12a1bb0 | 0.729 | 0.756 | 7020 | 0.814 | nocrossjump=1; nocet=1; align1=1; spec=loc,tiny,small,imm; varslot=0; 20 pairs: C! R>, DUP C@, C@ =, OVER R>, ...; rtfuse=0; ops10=EXECUTE,>?BRANCH8,=I?BRANCH,=I?BRANCH8,DUP?BRANCH8,U<?BRANCH8,<?BRANCH8,(LOOP),?BRANCH8,0<?BRANCH8,BRANCH8,DUP?NBRANCH8,?NBRANCH,UNLOOP; escape=1; msc=1; hotcalls=32; lean=1; bss=1 | crossover; mutation: peel=0 |
| c513ef17b0 | 0.773 | 0.781 | 7019 | 0.882 | nocrossjump=1; nocet=1; align1=1; ipaclone=1; spec=tiny,small,imm; guard=1; -AND; 21 pairs: C! R>, DUP C@, >R OVER, C@ =, ...; rtfuse=0; ops10=EXECUTE,I,=I?BRANCH,DUP?BRANCH8,SWAP+I,(?DO),<?BRANCH8,(LOOP),?BRANCH8,?NBRANCH,=I?BRANCH8,BRANCH8,DUP?NBRANCH8,UNLOOP; escape=1; tail=1; hotcalls=32; lean=1; bss=1 | crossover; mutation: nocrossjump=1, -fold AND |

## How the front came about

- `9d89f6ba0e`: from crossover; mutation: rtloopall=1, then crossover; borrowed bss from 678b1407c3 / crossover; mutation: nocet=1, tracer=1 / mutation: -O3 / borrowed msc from 676468f3c7; mutation: noreorder=1 / crossover; borrowed folds+supers from 5a1da5967f; mutation: -super C@  / mutation: bytehdr=0 / mutation: lean=0 / mutation: guard=1
- `f084674b22`: from mutation: guard=1, align1=1, then crossover; borrowed varcall+varslot from 7808f657b3; mutation: nocet=1 / mutation: +super @ <, guard=1 / crossover; mutation: rtloopall=1 / crossover; borrowed bss from 678b1407c3 / crossover; mutation: nocet=1, tracer=1 / mutation: -O3 / crossover; mutation: +super R> SWAP / mutation: lean=0
- `45d2ff7e01`: from crossover; borrowed varcall+varslot from 7808f657b3; mutation: nocet=1, then mutation: +super @ <, guard=1 / crossover; mutation: rtloopall=1 / crossover; borrowed bss from 678b1407c3 / crossover; mutation: nocet=1, tracer=1 / mutation: -O3 / crossover; mutation: +super R> SWAP / mutation: ipaclone=0 / mutation: peel=1
- `fa23f401cd`: from mutation: +super @ <, guard=1, then crossover; mutation: rtloopall=1 / crossover; borrowed bss from 678b1407c3 / crossover; mutation: nocet=1, tracer=1 / mutation: -O3 / borrowed msc from 676468f3c7; mutation: noreorder=1 / crossover; borrowed folds+supers from 5a1da5967f; mutation: -super C@  / crossover; mutation: d256=1 / mutation: rtimm=1, peel=1
- `853cfb9d36`: from crossover; borrowed varcall+varslot from 7808f657b3; mutation: nocet=1, then mutation: +super @ <, guard=1 / crossover; mutation: rtloopall=1 / crossover; borrowed bss from 678b1407c3 / crossover; mutation: nocet=1, tracer=1 / mutation: -O3 / crossover; mutation: +super R> SWAP / crossover; mutation: escape=1 / mutation: align1=0
- `2367cb920c`: from mutation: bytehdr=0, then mutation: bss=1 / crossover; mutation: varslot=1 / crossover; mutation: rtloop=1 / crossover / crossover / crossover; mutation: nogcse=1, d256=1 / mutation: noreorder=1 / crossover; mutation: sharedcall=0
- `88792f1798`: from crossover; borrowed varcall+varslot from 7808f657b3; mutation: nocet=1, then mutation: +super @ <, guard=1 / crossover; mutation: rtloopall=1 / crossover; borrowed bss from 678b1407c3 / crossover; mutation: nocet=1, tracer=1 / mutation: -O3 / crossover; mutation: +super R> SWAP / mutation: ipaclone=0 / borrowed scale+bytehdr+doesfar from 03a197f9bc; mutation: rtloop=0
- `ccce4784b8`: from crossover; mutation: rtloopall=1, hotcalls=16, then mutation: guard=1, align1=1 / crossover; borrowed varcall+varslot from 7808f657b3; mutation: nocet=1 / mutation: +super @ <, guard=1 / crossover; mutation: d256=1 / crossover; mutation: op DUP?NBRANCH8->?DUP / crossover; mutation: -spec var / crossover; mutation: escape=2 / mutation: hotcalls=32
- `ee4d8f8a50`: from crossover; mutation: nocrossjump=1, then crossover; mutation: escape=2 / mutation: guard=1 / crossover; mutation: varslot=0 / crossover / crossover / crossover; borrowed tail+tos from a344a1e36b; mutation: nocet=1, tail= / mutation: ipaclone=0 / mutation: -fold R@
- `57d12a1bb0`: from mutation: ipaclone=0, then mutation: nocet=1, ipaclone=1 / crossover; mutation: align1=1, nocet=1 / mutation: peel=1 / mutation: rtloopall=0, nocrossjump=1 / crossover; mutation: rtimm=0 / borrowed lean from 5a1da5967f; mutation: scale=3, noreorder=1 / borrowed rtloop from d04bbdda91; mutation: ipaclone=0 / crossover; mutation: peel=0
- `c513ef17b0`: from crossover; mutation: rtloop=1, then crossover / mutation: ipaclone=0 / mutation: nocet=1, ipaclone=1 / crossover; mutation: align1=1, nocet=1 / crossover; mutation: -super LSHIFT OVER / crossover; mutation: msc=0 / mutation: guard=1 / crossover; mutation: nocrossjump=1, -fold AND

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.126 | 25144 | no |
| s1-sod16 | 1.516 | 16304 | no |
| s2-cpt16 | 1.179 | 15384 | no |
| s3-cpt16f | 1.119 | 15200 | no |
| s4-cv8 | 1.100 | 14152 | no |
| s5-cv8spec | 0.949 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths

- died: reach limit at scale 0 - not run: 119

