# The after-seed-42 batch, in this order

Each made on a fresh copy of master (Iteration 198, the after-seed-41 batch
applied) with the ones before it, and verified to apply in order.

| # | patch | what |
|---|---|---|
| 1 | shortbranch-after-seed42.patch | short branches the tag-2 encoding finds out of range kept long on a second conversion - seed 41's 37 converter deaths alive, living designs byte-identical (199) |
| 2 | screen-after-seed42.patch | the surrogate screen: children predicted beaten by 30%/5% not measured, one in ten audited - pure Python (200) |

To apply, on a fresh clone of master:

    for f in shortbranch screen; do git apply results/pending/$f-after-seed42.patch || break; done

Then the checks as for every batch (results/applied-after-seed41/ORDER.md): the
reseed only if forth/kernel.4 changed, the stage build, run-tests (bash),
--validate, the front designs alive, ans-check on the front.
