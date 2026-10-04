# Evolution on the Ryzen 7 PRO 8840HS - seed 2

The second run: `evolve.py --pop 32 --gens 40 --rounds 3 --seed 2` at
ab7fe76 (the evolver of the first, with Iteration 4's sampler and option
check), then `--remeasure 6`. 1,308 designs, 1,147 alive. Speed: CPU time
over hand-made s6's, paired run by run, geometric mean over kernel, fib,
parse and corpus, normalised by s6's own figure in the run; loop held out.
Every figure measured. Quote the re-measured column: the run's figure is
the best of noisy measurements, and the re-measurement moved them by -2%
to +10% (57e0e77c09 0.602 -> 0.657; c17103bf95 0.657 -> 0.725).

## The Pareto front

| design | speed | re-measured | size | loop (held out) | genes, where they differ from s6-cv8b | how it was made |
|---|---|---|---|---|---|---|
| 57e0e77c09 | 0.602 | 0.657 | 13480 | 0.661 | opt=O3; nocrossjump=1; nocet=1; bytehdr=0; guard=1; 21 pairs: DUP >R, C! R>, >R C!, DROP DUP, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8; escape=1; msc=1 | mutation: guard=1 |
| 9cd791dd84 | 0.634 | 0.619 | 13472 | 0.849 | opt=O3; nocrossjump=1; nocet=1; scale=2; bytehdr=0; doesfar=0; 21 pairs: DUP >R, C! R>, >R C!, DROP DUP, ...; rtfuse=0; ops10=EXECUTE,I,(DO),+!,?DUP,UNLOOP,J,(LOOP),(?DO),(+LOOP),(LEAVE),?BRANCH8,BRANCH8; escape=1; msc=1 | mutation: +super OVER >R |
| a285fa6ba3 | 0.638 | 0.666 | 13464 | 0.892 | nocrossjump=1; nocet=1; bytehdr=0; spec=loc,tiny,small,imm; guard=1; 22 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,(DO),J,(+LOOP),?BRANCH8,BRANCH8,(LOOP),I,+!,UNLOOP,(LEAVE),?DUP; escape=1; msc=1 | mutation: bytehdr=0, tail=1 |
| c17103bf95 | 0.657 | 0.725 | 9769 | 0.822 | nocet=1; noreorder=1; spec=loc,tiny,small,imm; guard=1; 21 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,(DO),?DUP,J,(?DO),(+LOOP),?BRANCH8,UNLOOP,BRANCH8,(LOOP),I,(LEAVE),+!; escape=1; msc=1 | mutation: +op UNLOOP |
| 0ebf0445e0 | 0.672 | 0.667 | 9761 | 0.923 | nocrossjump=1; nocet=1; spec=loc,tiny,small,imm; guard=1; 22 pairs: DUP >R, C! R>, >R C!, ROT DUP, ...; rtfuse=0; ops10=EXECUTE,(DO),J,(+LOOP),?BRANCH8,BRANCH8,(LOOP),I,+!,UNLOOP,(LEAVE),?DUP; escape=1; msc=1 | crossover; mutation: sharedcall=0 |

## How the front came about

- `57e0e77c09`: from founder: s6-cv8b + escape, 7 words, 24 pairs, then mutation: align1=1 / crossover; mutation: -spec var / mutation: sharedcall=0, guard=1 / crossover; mutation: super ROT DUP->DROP DUP, nocet=1 / mutation: nocrossjump=1 / mutation: guard=1
- `9cd791dd84`: from founder: s6-cv8b + escape, 7 words, 24 pairs, then mutation: align1=1 / crossover; mutation: -spec var / mutation: sharedcall=0, guard=1 / crossover; mutation: super ROT DUP->DROP DUP, nocet=1 / mutation: nocrossjump=1 / mutation: scale=2 / mutation: doesfar=0 / mutation: +super OVER >R
- `a285fa6ba3`: from crossover; mutation: bytehdr=0, sharedcall=0, then crossover; mutation: -spec var / crossover; mutation: -super ROT ROT / crossover; mutation: sharedcall=1 / mutation: noreorder=1 / crossover / crossover; mutation: noreorder=0 / crossover; mutation: sharedcall=0 / mutation: bytehdr=0, tail=1
- `c17103bf95`: from mutation: op (LOOP)->I, then crossover; mutation: bytehdr=0 / crossover; mutation: bytehdr=0, sharedcall=0 / crossover; mutation: -spec var / crossover; mutation: -super ROT ROT / crossover; mutation: sharedcall=1 / mutation: noreorder=1 / mutation: nocet=1 / mutation: +op UNLOOP
- `0ebf0445e0`: from crossover; mutation: bytehdr=0, then crossover; mutation: bytehdr=0, sharedcall=0 / crossover; mutation: -spec var / crossover; mutation: -super ROT ROT / crossover; mutation: sharedcall=1 / mutation: noreorder=1 / crossover / crossover; mutation: noreorder=0 / crossover; mutation: sharedcall=0

## Seed 1 and seed 2, re-measured

| | seed 1 | seed 2 |
|---|---|---|
| fastest, about 13.5 KB | 38d187239c 0.609 at 13,480 | 9cd791dd84 0.619 at 13,472 |
| smallest near 9.8 KB | 5b70f3dd64 0.649 at 9,801 | 0ebf0445e0 0.667 at 9,761 |
| | 83cb81c383 0.705 at 9,761 | c17103bf95 0.725 at 9,769 |

Two independent runs found the same front, to within the measurement's
noise, and the same genes: the escape, multi-state caching, 12-13 of
relf's format-10 words with both short branches, 21-22 pairs, no endbr64,
guard pages, mostly -fno-crossjumping. They differ where the knockouts say
it matters least: scale (seed 2's fastest at scale 2 with near DOES>,
seed 1's at scale 3) and the order of the word and pair lists. The
result does not depend on the seed.

## The hand-made stages

| stage | speed | size | on the front |
|---|---|---|---|
| s0-cell | 1.196 | 25144 | no |
| s1-sod16 | 1.515 | 16304 | no |
| s2-cpt16 | 1.225 | 15384 | no |
| s3-cpt16f | 1.184 | 15200 | no |
| s4-cv8 | 1.138 | 14152 | no |
| s5-cv8spec | 0.924 | 13744 | no |
| s6-cv8b | 1.000 | 10065 | no |

## Deaths, audited

161, every genome checked against its cause - not taken from the label:
160 are the reach limit SCAN.md describes, a two-byte-only call or DOES>
form at scale 0 or 1 (kernel workload 132, timed out 20, corpus 8 - the
corpus ones the silent form found at Iteration 4: wrong output, not an
error); 1 is the converter's alignment refusal (cpt16 at scale 3, a call
target not 8-aligned). None is a generator fault: the region the uniform
sample found broken (`sample-amd-ryzen-7-pro-8840hs.md`) the run never
reached.
