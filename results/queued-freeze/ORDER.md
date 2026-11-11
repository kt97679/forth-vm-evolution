# The freeze's batch - the retirements of the final pooled front (Iteration 642; applied at the freeze, after the final check)

Queued in results/queued-freeze/ (process-run.sh never applies it): applied by hand at the freeze, after the final check is
processed - a patch dropped first if a design the final check gives a role uses what it retires
(results/drafts/freeze-retire-641.md).

    git apply results/queued-freeze/rtloop-after-seed91.patch

**rtloop-after-seed91.patch** (forth/cv8-fuse-loop.4, forth/cv8-fuse-loopall.4, lab/evolve/GENES.md, lab/evolve/evolve.py, tools/layout.py) - the freeze's retirement, by 578's rule, of a code path the retire report cannot see (several genes choose it): the partial run-time loop compiler - forth/cv8-fuse-loop.4 (84 lines), the -loop dumps, layout.py's LOOP-OPS, X10-XTS and X10-OPS tables - on no design of the pooled true front of seeds 77-91 (0 of 615; 140 of 4,874 alive off it), no hand-made stage, no winner (results/drafts/freeze-audit-641.py). rtloopall retired at 1 (FROZEN - the report's rtloopall=0), rtloop expressed with all eight loop opcodes only, so every front design's id stands; a genome with rtloop and fewer reads rtloop dormant. 120 lines out, 23 in. Tested: every recorded design's id before and after (4,892 - 140 change, the -loop designs; no winner; b35ae710e6 the one in the final check's list: if it takes a role, drop this patch); the bytes of 68 designs - the winners and 40 front designs drawn - at both widths, master against the patched tree (results/drafts/build-hash-641.py): RESULT; batch-check below.
