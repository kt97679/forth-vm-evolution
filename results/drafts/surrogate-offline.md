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

## Without scikit-learn (Iteration 199)

The laptop may not have it, so two models with no library, the same protocol
(seed 40, trained on generations 0-68, scored on 69-136):

| model | speed error, median / 90% | size error, median | 30%/5% screen: skipped, front lost | 20%/2% |
|---|---|---|---|---|
| random forest (scikit-learn) | 3.1% / 10.6% | 0.74% | 34%, 0 of 163 | 58%, 6 |
| additive, pure Python (one weight per gene value, SGD, 22 s) | 8.2% / 26.7% | 1.23% | 34%, 1 of 163 | 70%, 46 |
| the parents' geometric mean | 25.7% / 57.5% | 5.08% | 1%, 1 | 10%, 3 |
| parents and each mutation's learned effect | 21.6% / 55.3% | 4.82% | 11%, 2 | 32%, 10 |

A child is not like its parents: one gene (jit) moves speed by a factor, and
crossover's children sit between parents unlike each other - the map from
genes to speed has to be learned globally. Additive, it is good enough at the
conservative margins (a third of the measurements saved, one front design in
163 lost - the audit's one in ten measured anyway would catch some), and
overconfident at tighter ones: it cannot see interactions (jit with the rest).
The forest sees them: at 20%/2% it saves 58% for 6 lost.

So: with scikit-learn on the laptop, the forest at 30%/5% first, then 20%/2%;
without it, the additive model at 30%/5% only. Pairwise features for the
linked genes (LINKS) would bring the additive model closer - to measure.
