# The gene votes - each run's votes for taking a gene out (from Iteration 432)

results/seed63-rules.md, "The gene votes" (the owner, Iteration 432): no rule takes a gene out; each run votes. Per
gene and run, four votes for its removal - on under 10% of the front; on no design of its fastest tenth; of its
smallest tenth; of its best-Q tenth (speed x binary + image x memory). Written at each seed's processing from seed 63
on: `python3 lab/evolve/review-checks.py votes results/evolve-<machine>-seedN.md --ledger results/gene-votes.md
--append`, which also prints the tally over the last three runs here. Frozen genes are not voted on. **Seed 63: the JIT's genes not voted** (Iteration 441) - the hand-made founder carrying
the JIT lacked the tag its JIT needs, so none of them was available to the run; their window starts with the next run
that has the JIT.

| seed | gene | share | in the fastest tenth | in the smallest tenth | in the best-Q tenth | removal votes |
|---|---|---|---|---|---|---|
| 63 | skippad | 0% | 0 | 0 | 0 | 4 |
| 63 | fold | 0% | 0 | 0 | 0 | 4 |
| 63 | tos | 79% | 10 | 3 | 9 | 0 |
| 63 | sharedcall | 0% | 0 | 0 | 0 | 4 |
| 63 | varslot | 11% | 2 | 0 | 0 | 2 |
| 63 | d256 | 33% | 0 | 0 | 1 | 2 |
| 63 | guard | 57% | 9 | 0 | 10 | 1 |
| 63 | supers | 3% | 1 | 0 | 0 | 3 |
| 63 | rtfuse | 23% | 5 | 0 | 2 | 1 |
| 63 | escape | 45% | 10 | 0 | 10 | 1 |
| 63 | tail | 0% | 0 | 0 | 0 | 4 |
| 63 | hotcalls | 44% | 0 | 6 | 1 | 1 |
| 63 | rtimm | 17% | 8 | 0 | 3 | 1 |
| 63 | rtloop | 90% | 10 | 2 | 10 | 0 |
| 63 | rtloopall | 0% | 0 | 0 | 0 | 4 |
| 63 | kfast | 88% | 10 | 2 | 10 | 0 |
| 63 | tfind | 58% | 3 | 0 | 1 | 1 |
| 63 | kinput | 57% | 10 | 0 | 10 | 1 |
| 63 | klookup | 42% | 10 | 0 | 10 | 1 |
| 63 | rtiplus | 0% | 0 | 0 | 0 | 4 |
| 63 | swapi | 23% | 8 | 5 | 3 | 0 |
| 63 | tag2 | 10% | 2 | 0 | 0 | 3 |
| 63 | t2hot | 7% | 2 | 0 | 0 | 3 |
| 63 | hotinl | 0% | 0 | 0 | 0 | 4 |
| 63 | opbody | 89% | 10 | 2 | 10 | 0 |
| 63 | t2wide | 7% | 2 | 0 | 0 | 3 |
| 63 | rtempty | 0% | 0 | 0 | 0 | 4 |
| 63 | alignfn | 75% | 3 | 4 | 10 | 0 |
| 63 | noinls | 43% | 10 | 0 | 9 | 1 |
| 63 | fbuf | 19% | 0 | 6 | 3 | 1 |
| 63 | kstack | 0% | 0 | 0 | 0 | 4 |
| 63 | abortif | 17% | 0 | 0 | 0 | 3 |
| 63 | opcall | 0% | 0 | 0 | 0 | 4 |
| 63 | opinline | 83% | 10 | 0 | 10 | 1 |
| 63 | tailpn | 0% | 0 | 0 | 0 | 4 |
| 63 | knumber | 6% | 1 | 0 | 0 | 3 |
| 63 | alignhot | 5% | 5 | 0 | 0 | 3 |
| 63 | bfind | 28% | 3 | 0 | 1 | 1 |
| 63 | factor | 1% | 0 | 0 | 0 | 4 |
| 63 | lto | 41% | 7 | 0 | 9 | 1 |
| 63 | gotodup | 16% | 8 | 0 | 4 | 1 |
| 63 | threads | 63% | 9 | 8 | 4 | 0 |
| 63 | fsys | 99% | 9 | 10 | 10 | 0 |
| 63 | regpin | 41% | 10 | 0 | 9 | 1 |
| 63 | dskew | 55% | 3 | 4 | 5 | 0 |
