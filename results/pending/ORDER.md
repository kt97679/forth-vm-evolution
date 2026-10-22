# The pending batch - the gene votes' first freeze, before seed 66 (Iteration 450)

The owner (449-450): "yes, please prepare that freeze and continue" - the gene rule's next step for its first
candidates (results/seed63-rules.md, "The gene votes"): frozen off for one run, the code kept, removed only if that run
shows no loss.

| # | patch | what it does |
|---|---|---|
| 1 | freeze-before-seed66.patch | **sharedcall, tail, kstack and tailpn frozen off** (FROZEN, evolve.py) - each 12 of 12 removal votes over seeds 63-65 and on no front design, so the dependence test had nothing to rebuild. And **review-checks.py votes counts only the front's own encoding's genes**: skippad and fold, the other two candidates, are genes of sod16 and cpt16 (the old 16-bit encodings), not of CV8 - voted on CV8 fronts they cannot reach. Freezing them in CV8 would do nothing; whether those encoding families should go is a separate question, put to the owner. |

    git apply results/pending/freeze-before-seed66.patch

## How it was tested

batch-check (below). The freeze, as patch 10's (Iteration 409), applies to the designs the search makes (require(), at
get()); hand-made designs keep their own values, so s6 and the stages are unchanged and validate stays IDENTICAL.
