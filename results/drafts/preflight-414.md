# The processing tools, tried before the runs need them (Iteration 414)

The owner: review the project for what can be done while seeds 61-62 run. Each step seed 62's processing and seed 63's
will take, run here first on what is in hand.

**review-checks.py spread** - the replicates' comparison, on seeds 58, 59 and 60's databases as stand-ins: it runs, in
466 seconds here for three databases (in the background, then), and reads every run at the earliest last generation:

| run | generation | designs to it | front | fastest | smallest | least memory KB | best Q | hypervolume | fastest at 32 bits |
|---|---|---|---|---|---|---|---|---|---|
| seed58 | 133 | 24831 | 402 | 0.1179 | 14,146 | 112 | 6.4175e+05 | 0.5949 | 0.2997 |
| seed59 | 133 | 25349 | 404 | 0.1173 | 15,915 | 116 | 6.519e+05 | 0.5179 | 0.3250 |
| seed60 | 133 | 25190 | 373 | 0.1111 | 15,938 | 112 | 6.3422e+05 | 0.4961 | 0.3147 |
gene usage on the fronts, how far apart - the mean difference in points over every built gene (two runs of one start; for scale, seeds 55 and 56 differed by up to 17 points in a gene):
  seed58 - seed59: mean 10.3 points; the most: tag2 +60, t2wide +60, factor +48, t2hot +27, hotinl +24
  seed58 - seed60: mean 14.6 points; the most: factor +60, tag2 +60, t2wide +50, dskew +47, rtloopall -35
  seed59 - seed60: mean 13.6 points; the most: rtloopall -51, supers -46, dskew +43, noreorder -42, hotinl -35

Two tag-2 runs of different starts, 59 and 60, sit 13.6 points of gene usage apart on average while their fastest are
within 6% and their smallest within 0.2%: many settings, one performance - the replicates will say how far one start
spreads (Iteration 393's predictions).

**review-checks.py curse** - seed 63's check of the fast end's optimism - on seed 60's report: the fastest tenth's
re-measure over its in-run speed, median 1.066 (range 1.025-1.129); seed 58's was 1.112. So the fast end is already
less lucky without the fast gate: seed 63's figure is read against both.

**The batch applied, dry run** - a scratch clone, the eleven patches applied, `git mv results/pending
results/applied-after-seed62`, the citations' sed of the routine: every patch applied, and handoff-check named one
thing the routine does not do - results/README.md's `pending/ORDER.md` line, left pointing at nothing. The routine
says so now (HANDOFF, step 6). footprint.py was tried at Iteration 403.
