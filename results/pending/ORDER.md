# The after-seed-65 batch - apply in this order (at seed 65's processing)

Prepared at Iteration 446 by the owner's word (445: "yes, please proceed"), after seed 65 so the islands trial is not
mixed with it.

| # | patch | what it does |
|---|---|---|
| 1 | fastgate-defer-after-seed65.patch | The fast gate's second reading deferred (results/drafts/fastgate-review-445.md): a child under the gate is marked, not measured again at once - back to back the two readings shared their moment's luck (seed 64: second / first 1.000, the re-measure after the run about 1.10 slower at the fast end) - and measured again in the next generation's batch, among other co-runners, its speed then the geometric mean of the two (64 bits; its 32-bit reading the first). The same cost; no new threshold. |

    git apply results/pending/fastgate-defer-after-seed65.patch

## How it was tested

In a clone of master (eb306b2), its stages built: a short evolution with the gate on the 4th fastest (16 designs, 4
generations, --fastgate 4) - 12 children measured again in the batch after their own, each its two readings and their
mean logged (results/drafts/fastgate-defer-446.log; e.g. a127d1037a 0.7787 then 0.7242, recorded 0.751), the run to its
end. Rule 3 reads its effect at the first run with it: the fastest tenth's optimism at most 1.05.

**Not prepared: the rtfuse simplification** (rule 9's proposal). Checking it found that `--rtfuse` carries I+'s table
entry too, and that I+ fuses only where the run-time fuser is built: on seed 64's front, a plain design with the fuser
- loop's dispatches -20.0% with rtiplus; one without - +0.0%. 37 of seed 64's 55 front designs with rtiplus have no
fuser (30 of them tag-2 JIT designs, where it hardly matters; 7 plain, where it would). Making rtfuse govern rtimm=2's
fusion would leave more designs so. The owner's call instead: rtiplus to bring the fuser with it (HANDOFF item 4b2).
