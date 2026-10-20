# The gene votes - each run's votes for taking a gene out (from Iteration 432)

results/seed63-rules.md, "The gene votes" (the owner, Iteration 432): no rule takes a gene out; each run votes. Per
gene and run, four votes for its removal - on under 10% of the front; on no design of its fastest tenth; of its
smallest tenth; of its best-Q tenth (speed x binary + image x memory). Written at each seed's processing from seed 63
on: `python3 lab/evolve/review-checks.py votes results/evolve-<machine>-seedN.md --ledger results/gene-votes.md
--append`, which also prints the tally over the last three runs here. Frozen genes are not voted on.

| seed | gene | share | in the fastest tenth | in the smallest tenth | in the best-Q tenth | removal votes |
|---|---|---|---|---|---|---|
