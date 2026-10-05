# Evolution on the Ryzen 7 PRO 8840HS - seed 5, selected by the median

The first run selected by the median of its rounds (Iteration 25).
`--pop 32 --gens 40 --rounds 3 --seed 5` at 8d3eb709 (Iteration 27),
2026-10-05, 38 minutes, then `--remeasure 6`. 1,308 designs, 1,162 alive
(database sha256 fd2f99e1adca9750...). Speed: median CPU time over hand-made s6's,
paired, geometric mean over kernel, fib, parse, corpus; loop held out.

**Calibration: s6 against itself 0.989** (fib 0.966). **The re-measure agrees
with selection within 4%** - 0.574 to 0.579, 0.601 to 0.593, 0.734 to
0.731 - where seed 4's first run, selected by the best of N, lost 2-24%.

## The Pareto front, as selected

| design | speed | re-measured | size | loop (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| 2db525ff95 | 0.574 | 0.579 | 14017 | 0.987 | nocrossjump=1; nocet=1; tracer=1; scale=2; bytehdr=0; doesfar=0; varslot=0; guard=1; ->R; 16 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=1; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8,=?BRANCH,<>?BRANCH; escape=2; msc=1; hotcalls=32 | mutation: doesfar=0, scale=2 |
| 22b81e50c4 | 0.580 | 0.605 | 13209 | 0.923 | opt=O3; nocrossjump=1; nocet=1; align1=1; peel=1; tracer=1; scale=1; bytehdr=0; guard=1; 15 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,=?BRANCH8,U<?BRANCH8,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8,=?BRANCH,<>?BRANCH,(LOOP),<?BRANCH8; escape=2; msc=1; hotcalls=32 | mutation: nocrossjump=1 |
| 9e50623ac1 | 0.601 | 0.593 | 13073 | 0.936 | opt=O3; nocet=1; tracer=1; bytehdr=0; spec=loc,tiny,small,imm; guard=1; -XOR; 15 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=2; msc=1; hotcalls=32 | crossover; borrowed hotcalls from 22b81e50c4; mutation: -O3 |
| 5ed1ed8715 | 0.628 | 0.642 | 10018 | 1.010 | opt=O3; nocrossjump=1; nocet=1; noreorder=1; guard=1; 14 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=1; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8,=?BRANCH,<>?BRANCH,(LOOP); escape=2; tail=1; hotcalls=32 | borrowed tail from 22b81e50c4; mutation: peel=0 |
| 52b80007a1 | 0.638 | 0.640 | 10010 | 1.005 | opt=O3; nocrossjump=1; nocet=1; guard=1; 14 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=1; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=2; tail=1; hotcalls=32 | crossover; mutation: msc=0 |
| 8dc0f97f2c | 0.669 | 0.680 | 9458 | 0.938 | nocet=1; align1=1; tracer=1; guard=1; 14 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=2; msc=1; hotcalls=32 | crossover; mutation: nocrossjump=0 |
| f052397620 | 0.690 | 0.685 | 9450 | 0.911 | nocrossjump=1; nocet=1; noreorder=1; peel=1; guard=1; -ROT; 15 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=2; msc=1; hotcalls=32 | mutation: noreorder=1, +spec var |
| 528fc9619a | 0.695 | 0.702 | 9359 | 1.003 | nocet=1; align1=1; tracer=1; spec=loc,tiny,small,imm; guard=1; 14 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=2; msc=1; hotcalls=32 | crossover |
| 4032a5ce71 | 0.708 | 0.698 | 9351 | 0.954 | nocet=1; peel=1; spec=loc,tiny,small,imm; guard=1; -ROT; 15 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=2; msc=1; hotcalls=32 | mutation: nocrossjump=0 |
| 4f010d8ab9 | 0.734 | 0.721 | 9343 | 1.037 | opt=O3; nocet=1; align1=1; spec=loc,tiny,small,imm; varslot=0; 14 pairs: DUP >R, @ +, C! R>, >R C!, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=2; msc=1; hotcalls=32 | mutation: -super OVER C@ |
| 98736f0596 | 0.734 | 0.731 | 9335 | 1.032 | opt=O3; nocrossjump=1; nocet=1; align1=1; spec=loc,tiny,small,imm; varslot=0; 14 pairs: DUP >R, @ +, C! R>, >R C!, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8,?NBRANCH,?NBRANCH8,<?BRANCH,<?BRANCH8,=?BRANCH,=?BRANCH8,U<?BRANCH,U<?BRANCH8,<>?BRANCH,<>?BRANCH8,>?BRANCH,>?BRANCH8,0<?BRANCH,0<?BRANCH8,=I?BRANCH,=I?BRANCH8; escape=2; msc=1; hotcalls=32 | mutation: varslot=0 |

### How it came about

- `2db525ff95`: from mutation: hotcalls=32, tracer=1, then crossover; mutation: varslot=0 / mutation: guard=1 / crossover; borrowed ops10 from c707711b4d; mutation: nocet=1 / mutation: bytehdr=0, rtfuse=1 / crossover; mutation: sharedcall=0, nocet=1 / mutation: nocrossjump=1 / mutation: -fold >R / mutation: doesfar=0, scale=2
- `22b81e50c4`: from crossover; mutation: sharedcall=0, nocet=1, then mutation: nocrossjump=1 / mutation: -fold >R / crossover; mutation: d256=1 / mutation: ipaclone=1, peel=1 / crossover; mutation: sharedcall=0, scale=1 / mutation: varslot=1 / mutation: ipaclone=0 / mutation: nocrossjump=1
- `9e50623ac1`: from mutation: nocet=1, then crossover; mutation: msc=1 / crossover / crossover / mutation: align1=1 / mutation: tracer=1 / mutation: -spec var, sharedcall=0 / crossover / crossover; borrowed hotcalls from 22b81e50c4; mutation: -O3
- `5ed1ed8715`: from crossover; borrowed ops10 from c707711b4d; mutation: nocet=1, then mutation: bytehdr=0, rtfuse=1 / crossover; mutation: sharedcall=0, nocet=1 / mutation: nocrossjump=1 / crossover; mutation: scale=1 / crossover; mutation: d256=1, tail=0 / crossover; mutation: -O3 / mutation: +super OVER >R / borrowed tail from 22b81e50c4; mutation: peel=0
- `52b80007a1`: from mutation: guard=1, then crossover; mutation: ipaclone=0, peel=1 / crossover; mutation: guard=1 / mutation: nocet=1 / crossover; mutation: msc=1 / crossover / crossover / mutation: align1=1 / crossover; mutation: msc=0
- `8dc0f97f2c`: from crossover; mutation: ipaclone=0, peel=1, then crossover; mutation: guard=1 / mutation: nocet=1 / crossover; mutation: msc=1 / crossover / crossover / mutation: align1=1 / mutation: tracer=1 / crossover; mutation: nocrossjump=0
- `f052397620`: from crossover; mutation: ipaclone=1, then crossover; mutation: nocet=1 / borrowed folds from bec714846f; mutation: -O3 / mutation: -spec var, tail=0 / mutation: -fold AND, sharedcall=0 / crossover; mutation: tracer=0, scale=3 / crossover; mutation: -O2 / crossover; borrowed folds from 35153bcaf3; mutation: peel=1 / mutation: noreorder=1, +spec var
- `528fc9619a`: from crossover; mutation: guard=1, then mutation: nocet=1 / crossover; mutation: msc=1 / crossover / crossover / mutation: align1=1 / mutation: tracer=1 / mutation: -spec var, sharedcall=0 / crossover
- `4032a5ce71`: from crossover; mutation: ipaclone=1, then crossover; mutation: nocet=1 / borrowed folds from bec714846f; mutation: -O3 / mutation: -spec var, tail=0 / mutation: -fold AND, sharedcall=0 / crossover; mutation: tracer=0, scale=3 / crossover; mutation: -O2 / crossover; borrowed folds from 35153bcaf3; mutation: peel=1 / mutation: nocrossjump=0
- `4f010d8ab9`: from mutation: nocet=1, then crossover; mutation: msc=1 / crossover / crossover / mutation: align1=1 / crossover; mutation: guard=0, +super @ + / mutation: varslot=0 / mutation: nocrossjump=0 / mutation: -super OVER C@
- `98736f0596`: from crossover; mutation: ipaclone=0, peel=1, then crossover; mutation: guard=1 / mutation: nocet=1 / crossover; mutation: msc=1 / crossover / crossover / mutation: align1=1 / crossover; mutation: guard=0, +super @ + / mutation: varslot=0


## The front, re-measured

| design | re-measured | size | loop (held out) | one-byte calls | escape | headers | scale | pairs | format-10 | run-time fusion |
|---|---|---|---|---|---|---|---|---|---|---|
| 2db525ff95 | 0.579 | 14,017 | 0.981 | 32 | 2 | cell | 2 | 16 | 28 | yes |
| 9e50623ac1 | 0.593 | 13,073 | 0.904 | 32 | 2 | cell | 0 | 15 | 29 | - |
| 52b80007a1 | 0.640 | 10,010 | 1.001 | 32 | 2 | byte | 0 | 14 | 29 | yes |
| 8dc0f97f2c | 0.680 | 9,458 | 0.895 | 32 | 2 | byte | 0 | 14 | 29 | - |
| f052397620 | 0.685 | 9,450 | 0.909 | 32 | 2 | byte | 0 | 15 | 29 | - |
| 4032a5ce71 | 0.698 | 9,351 | 0.944 | 32 | 2 | byte | 0 | 15 | 29 | - |
| 4f010d8ab9 | 0.721 | 9,343 | 1.009 | 32 | 2 | byte | 0 | 14 | 29 | - |
| 98736f0596 | 0.731 | 9,335 | 0.978 | 32 | 2 | byte | 0 | 14 | 29 | - |

**What selection chose**: every design on the front carries 32 one-byte
calls AND the second escape level, holding 14-16 pairs beside 28-29
format-10 opcodes; among the 1,153 living CV8 designs, one-byte calls with
32 targets on 63%, the second escape level on 74%. The fastest design is
new in kind: scale 2, cell headers, run-time fusion (rtfuse), 0.579 at
14,017 bytes. A design near 10 KB (52b80007a1, 0.640 at 10,010) fills the
gap between the 13 KB and 9.4 KB groups.

## Against the earlier runs - across sessions, so provisional

Seed 5's own re-measure against Iteration 26's two-CPU session (all earlier
fronts, by the median); both by the median, but two sessions - the median
has agreed within about 2% between CPUs of one session; between sessions
it is not yet measured, so differences under about 3% are not claimed:

| size | seed 5 (its re-measure) | the best earlier at that size (Iteration 26) |
|---|---|---|
| 14,017 | **0.579** | - (the earlier fastest: 0.588 at 13,201) |
| 13,073 | **0.593** | 0.624 (4cb3fa9172, seed 4) |
| 10,010 | 0.640 | - (nothing between 9.7 and 13 KB) |
| 9,450-9,458 | 0.680, 0.685 | 0.680 (c297551359, seed 4) |
| 9,335 | 0.731 | 0.700 (05dcc81cdc, seed 4) |

At 13,073 bytes 5% faster than anything before; ties at 9.45 KB; slower at
the smallest size. The next laptop session that measures speed measures
seed 5's front with the others in one session (GOALS.md).

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.200 | 25144 | no |
| s1-sod16 | 1.525 | 16304 | no |
| s2-cpt16 | 1.215 | 15384 | no |
| s3-cpt16f | 1.183 | 15200 | no |
| s4-cv8 | 1.151 | 14152 | no |
| s5-cv8spec | 0.903 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths, audited - each rebuilt on the development VM

146. 142 declined unrun (two-byte-only forms at scale 0). Of the four run:

- 3ce3518f60, 477e5eff63 (kernel workload) - scale 1, near DOES> calls:
  live with `doesfar=1` alone. f21df1428a (timed out) - scale 1, neither
  long form: lives with `varcall=1` and `doesfar=1` together, with neither
  alone. The scale-1 reach limits: the kernel workload runs code up to
  about 68 KB (`lab/evolve/loopwords.py`), past near DOES> calls' 32 KB and
  past two-byte calls' 64 KB at scale 1.
- 6a847f127c - the converter's own assertion, "call target 1302 not
  8-aligned": scale 3 with folding off; lives with folding on. Not new:
  Iteration 12's converter fails the same, before any change of this
  session. A rare corner (1 of 1,308), and it fails safe - the design dies
  converting.
