# The register machine's first stage, priced by counting

Iteration 32, on the development VM - counts are the same on every machine.
`lab/evolve/regprice.py s6 9e50623ac1 8dc0f97f2c 2db525ff95 --db <seed 5's>`.
The stage GOALS.md planned: register forms within a block, the stack
synchronised at calls, returns and branches. Its design, as priced:

- a run of data-stack moves (DUP DROP SWAP OVER ROT 2DUP 2DROP, and pairs
  of them) followed in the same block by an operation that takes operands
  is **absorbed** - the operation carries a descriptor of its operand slots
  and of the stack the moves would have left (every run seen reaches no
  deeper than the top four items);
- a run ending at a call, an exit, a branch or a push is **collapsed** into
  one shuffle instruction;
- a lone literal before a two-operand operation becomes an immediate.

## What it would save

| | kernel | parse | corpus | return-stack moves left alone |
|---|---|---|---|---|
| s6, hand-made | 26.3% | 25.9% | 25.8% | 13-16% |
| seed 5's front, three designs | 19-20% | 19-24% | 19-22% | 13-16% |

Shares of the dispatches in the image's own code: 84-99% of everything
executed on those workloads. fib's FIB and the held-out loop are compiled at
run time and are not priced here - they gain only if the run-time compiler
emits the forms too. Size: 52-101 bytes smaller. Reconciles with
stackops.py's bound (38-50%): this plus the return-stack moves it leaves.

## Where it is - a handful of patterns, out of the pairs' reach

On the front designs 42-53 distinct absorbed patterns; **5-8 of them give
80% of the saving**, the same two leading on every workload:

- `DUP ?BRANCH` - `DUP IF`, `DUP WHILE`: 5.8-6.2% of the dispatches
- `SWAP addi` - n added to the second item: 3.7-5.0%
- then `OVER ?BRANCH`, `2DUP` before a compare-and-branch, `DUP 1-`:
  1-2% together

Evolution never found them: its pairs fuse operand-free primitives, and
every one of these ends in an operation with an operand - a branch target,
an immediate. So the cheap route to most of the prize is not a register
machine but a few **operand-carrying fused opcodes**, built the way the
fused tests are (Iteration 12): branches that test without consuming
(DUP, OVER, 2DUP before a test-and-branch) and an add-immediate to the
second item - about 10-12% of the dispatches, as a gene the evolver can
weigh against the other users of the opcode slots. The register machine
proper - descriptors for the long tail, and the return-stack moves - is
what would remain beyond them.

## The counts

pinned to cpu 0 (it and its sibling 0% busy; BENCH_CPU=N to choose)
## s6 - s6 bytes; operation kinds ADDI 33 ADDIX 6 BR 55 EQI 17 EQIX 1 LIT 215 LITX 26 P 1305 PX 63 QBR 123 VF 121 VS 84

| workload | dispatches in the image's code | of all executed | absorbed runs | collapsed runs | literals | saved | runs deeper than 4 | return-stack moves, not absorbed |
|---|---|---|---|---|---|---|---|---|
| kernel | 8043027 | 88% | 23.7% | 0.5% | 2.1% | **26.3%** | 0.0% | 15.5% |
| fib | 70297 | 0% | 21.5% | 0.5% | 2.8% | **24.9%** | 0.0% | 13.2% |
| parse | 39091294 | 98% | 20.1% | 0.6% | 5.3% | **25.9%** | 0.0% | 12.8% |
| corpus | 6851810 | 98% | 21.7% | 0.6% | 3.5% | **25.8%** | 0.0% | 14.6% |
| loop | 6866286 | 74% | 6.0% | 0.0% | 0.0% | **6.1%** | 0.0% | 40.9% |

the largest absorbed patterns, as shares of each workload's image-code dispatches:
- kernel: ROT DUP | >R 6.4%, SWAP | addi 3.7%, DUP | zeq 3.2%, DUP | C@ 1.3%, DUP | ?BRANCH 1.1%
- fib: ROT DUP | >R 4.6%, SWAP | addi 2.8%, DUP | zeq 2.3%, DUP | C@ 1.9%, 2dup | sub 1.4%
- parse: ROT DUP | >R 5.2%, SWAP | addi 2.9%, DUP | zeq 2.7%, DUP | ?BRANCH 2.1%, DUP | C@ 1.3%
- corpus: ROT DUP | >R 5.5%, SWAP | addi 3.2%, DUP | zeq 2.8%, DUP | ?BRANCH 1.7%, OVER | C@ 1.1%
- loop: DUP | @ 5.8%, ROT DUP | >R 0.0%, SWAP | addi 0.0%, DUP | zeq 0.0%, ROT ROT SWAP | >R 0.0%

kernel: 51 distinct absorbed patterns; 9 of them give 80% of the absorbed saving. The largest: ROT DUP | >R (6.4%), SWAP | addi (3.7%), DUP | zeq (3.2%), DUP | C@ (1.3%), DUP | ?BRANCH (1.1%), OVER | C@ (1.1%), SWAP DUP | >R (1.0%), 2dup | sub (0.9%)

static: the image's code -101 bytes (a run absorbed or collapsed, a literal made immediate, wherever it was executed on the first workload)

## 9e50623ac1 - 13,073 bytes; operation kinds ADDI 32 ADDIX 6 BRS 45 EQI 6 EQIH 10 EQIX 1 EQQBRS 4 LIT 185 LITX 25 LP 7 LTQBRS 5 NEQBRS 4 NQBRS 15 P 1211 PX 85 QBRS 54 SGTQBRS 5 SP 59 ULTQBRS 4 ZLTQBRS 7

| workload | dispatches in the image's code | of all executed | absorbed runs | collapsed runs | literals | saved | runs deeper than 4 | return-stack moves, not absorbed |
|---|---|---|---|---|---|---|---|---|
| kernel | 5759507 | 84% | 18.3% | 0.3% | 1.6% | **20.2%** | 0.0% | 16.1% |
| fib | 49829 | 0% | 17.5% | 0.3% | 1.9% | **19.7%** | 0.0% | 14.0% |
| parse | 26977299 | 96% | 19.6% | 0.3% | 3.5% | **23.4%** | 0.0% | 14.2% |
| corpus | 4849848 | 95% | 18.4% | 0.3% | 2.4% | **21.2%** | 0.0% | 15.7% |
| loop | 6448933 | 70% | 6.3% | 0.0% | 0.0% | **6.3%** | 0.0% | 43.6% |

the largest absorbed patterns, as shares of each workload's image-code dispatches:
- kernel: SWAP | addi 5.2%, DUP | ?BRANCH 5.1%, 2dup | ?BRANCH 1.4%, ROT ROT SWAP | onem 0.8%, OVER | ?BRANCH 0.8%
- fib: SWAP | addi 3.9%, DUP | ?BRANCH 3.9%, 2dup | ?BRANCH 2.0%, DUP ROT ROT | + 1.0%, OVER | ?BRANCH 0.9%
- parse: DUP | ?BRANCH 4.8%, SWAP | addi 4.2%, DUP ROT ROT | + 2.7%, OVER | @ 1.5%, DUP | @ 1.5%
- corpus: DUP | ?BRANCH 4.8%, SWAP | addi 4.5%, DUP ROT ROT | + 1.4%, OVER | @ 1.0%, DUP | @ 0.9%
- loop: DUP | @ 6.2%, SWAP | addi 0.0%, DUP | ?BRANCH 0.0%, 2dup | ?BRANCH 0.0%, ROT ROT SWAP | >R 0.0%

kernel: 47 distinct absorbed patterns; 8 of them give 80% of the absorbed saving. The largest: SWAP | addi (5.2%), DUP | ?BRANCH (5.1%), 2dup | ?BRANCH (1.4%), ROT ROT SWAP | onem (0.8%), OVER | ?BRANCH (0.8%), DUP ROT ROT | + (0.7%), SWAP | DUP >R (0.7%), OVER | @ (0.6%)

static: the image's code -52 bytes (a run absorbed or collapsed, a literal made immediate, wherever it was executed on the first workload)

## 8dc0f97f2c - 9,458 bytes; operation kinds ADDI 33 ADDIX 6 BRS 55 EQI 6 EQIH 11 EQIX 1 EQQBRS 2 LIT 215 LITX 26 LP 7 LTQBRS 5 NEQBRS 4 NQBRS 16 P 1153 PX 63 QBRS 65 SGTQBRS 5 SP 69 ULTQBRS 8 VF 121 VS 84 ZLTQBRS 7

| workload | dispatches in the image's code | of all executed | absorbed runs | collapsed runs | literals | saved | runs deeper than 4 | return-stack moves, not absorbed |
|---|---|---|---|---|---|---|---|---|
| kernel | 6038104 | 85% | 16.8% | 0.4% | 1.9% | **19.1%** | 0.0% | 15.6% |
| fib | 52846 | 0% | 15.4% | 0.5% | 2.6% | **18.4%** | 0.0% | 13.3% |
| parse | 30429924 | 98% | 14.5% | 0.4% | 4.4% | **19.3%** | 0.0% | 12.7% |
| corpus | 5267183 | 97% | 15.5% | 0.5% | 3.1% | **19.0%** | 0.0% | 14.7% |
| loop | 6450833 | 73% | 6.3% | 0.0% | 0.0% | **6.3%** | 0.0% | 43.5% |

the largest absorbed patterns, as shares of each workload's image-code dispatches:
- kernel: DUP | ?BRANCH 5.8%, SWAP | addi 5.0%, 2dup | ?BRANCH 1.3%, ROT ROT SWAP | onem 0.8%, OVER | ?BRANCH 0.7%
- fib: DUP | ?BRANCH 4.8%, SWAP | addi 3.7%, 2dup | ?BRANCH 1.9%, OVER | ?BRANCH 0.8%, ROT ROT SWAP | onem 0.8%
- parse: DUP | ?BRANCH 6.2%, SWAP | addi 3.7%, DUP | onem 1.2%, OVER | ?BRANCH 0.5%, 2dup | ?BRANCH 0.4%
- corpus: DUP | ?BRANCH 5.8%, SWAP | addi 4.1%, DUP | onem 0.7%, OVER | ?BRANCH 0.7%, 2dup | ?BRANCH 0.6%
- loop: DUP | @ 6.2%, DUP | ?BRANCH 0.0%, SWAP | addi 0.0%, 2dup | ?BRANCH 0.0%, ROT ROT SWAP | >R 0.0%

kernel: 42 distinct absorbed patterns; 5 of them give 80% of the absorbed saving. The largest: DUP | ?BRANCH (5.8%), SWAP | addi (5.0%), 2dup | ?BRANCH (1.3%), ROT ROT SWAP | onem (0.8%), OVER | ?BRANCH (0.7%), SWAP | DUP >R (0.7%), ROT DUP | C@ (0.5%), DUP | onem (0.4%)

static: the image's code -80 bytes (a run absorbed or collapsed, a literal made immediate, wherever it was executed on the first workload)

## 2db525ff95 - 14,017 bytes; operation kinds ADDI 33 ADDIX 6 BRS 49 EQI 6 EQIH 11 EQIX 1 EQQBRS 5 LIT 202 LITX 27 LTQBRS 5 NEQBRS 4 NQBRS 15 P 1173 PX 59 QBRS 69 SGTQBRS 5 SP 67 ULTQBRS 4 VF 109 VS 88 ZLTQBRS 7

| workload | dispatches in the image's code | of all executed | absorbed runs | collapsed runs | literals | saved | runs deeper than 4 | return-stack moves, not absorbed |
|---|---|---|---|---|---|---|---|---|
| kernel | 5792999 | 86% | 18.4% | 0.3% | 1.7% | **20.4%** | 0.0% | 16.3% |
| fib | 49841 | 0% | 18.0% | 0.3% | 2.2% | **20.5%** | 0.0% | 14.4% |
| parse | 26589510 | 99% | 20.3% | 0.3% | 3.7% | **24.3%** | 0.0% | 14.4% |
| corpus | 4815484 | 98% | 18.8% | 0.3% | 2.6% | **21.7%** | 0.0% | 16.1% |
| loop | 6850265 | 71% | 11.8% | 0.0% | 0.0% | **11.8%** | 0.0% | 46.9% |

the largest absorbed patterns, as shares of each workload's image-code dispatches:
- kernel: SWAP | addi 5.2%, DUP | ?BRANCH 5.0%, 2dup | ?BRANCH 1.4%, ROT ROT SWAP | onem 0.8%, OVER | ?BRANCH 0.8%
- fib: SWAP | addi 3.9%, DUP | ?BRANCH 3.9%, 2dup | ?BRANCH 2.0%, DUP ROT ROT | + 1.1%, OVER | ?BRANCH 0.9%
- parse: DUP | ?BRANCH 4.8%, SWAP | addi 4.2%, DUP ROT ROT | + 2.9%, OVER | @ 1.6%, DUP | @ 1.5%
- corpus: DUP | ?BRANCH 4.8%, SWAP | addi 4.5%, DUP ROT ROT | + 1.5%, OVER | @ 1.0%, DUP | @ 0.9%
- loop: DUP | @ 5.8%, SWAP | >R 5.8%, SWAP | addi 0.0%, DUP | ?BRANCH 0.0%, 2dup | ?BRANCH 0.0%

kernel: 53 distinct absorbed patterns; 8 of them give 80% of the absorbed saving. The largest: SWAP | addi (5.2%), DUP | ?BRANCH (5.0%), 2dup | ?BRANCH (1.4%), ROT ROT SWAP | onem (0.8%), OVER | ?BRANCH (0.8%), DUP ROT ROT | + (0.7%), SWAP DUP | >R C! (0.7%), OVER | @ (0.6%)

static: the image's code -68 bytes (a run absorbed or collapsed, a literal made immediate, wherever it was executed on the first workload)

