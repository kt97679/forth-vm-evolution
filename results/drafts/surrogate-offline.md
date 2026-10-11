# A surrogate to screen children - tested offline on seed 40 (Iteration 197)

results/gp-deep-dive.md proposed screening children by a model before
measuring them. Tested on seed 40's database (34,983 designs, 137
generations): random forests on the expressed genes (one feature per scalar
value, one per list item; results/drafts/surrogate-train.py) trained on
generations 0-68, scored on the 16,319 living children of 69-136.

**Prediction from genes alone**: speed median error 3.1%, 90% within 10.6%
(a 60-tree forest: 2.5% and 7.8%); binary + image 0.74%, 90% within 2.6%.
Measurement noise between sessions is +-2.6% (5-95%).

**The screen, replayed** (results/drafts/surrogate-replay.py): a child is
skipped when its predicted speed and size are both beaten, by the margins, by
a point of the (speed, size) front of everything measured before its
generation. 163 of those children are on the run's final front:

| margins (speed, size) | skipped | final-front designs lost | random skipping, same rate |
|---|---|---|---|
| 30%, 5% | 34% | 0 | 56 |
| 20%, 2% | 58% | 6 | 95 |
| 10%, 2% | 70% | 19 | 113 |
| 10%, 0% | 87% | 73 | 141 |
| 5%, 0% | 96% | 134 | 156 |

A third of the measurements saved at no loss of the final front; more than
half at 4%. A skipped child costs a prediction (milliseconds) where a measured
one costs 2.7 s, so the saving becomes generations.

Caveats: one model trained on half the run, where a live run would retrain
every few generations; skipping changes which children exist later, which a
replay cannot show; memory is not screened. And scikit-learn is a dependency
the laptop may not have - a pure-Python nearest-neighbour model would avoid it,
to be measured the same way.

**To build** (the owner decides): retrain every 10 generations on the run's
database and the carried runs; skip children beyond 30%/5% at first, recorded
as screened (not measured, not selected); one screened child in ten measured
anyway, to keep the model honest and leave room for surprises.
