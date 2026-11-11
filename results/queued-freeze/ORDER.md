# The after-seed-91 batch - the freeze's retirements of the final pooled front (Iterations 642-643; applied at the freeze, after the final check)

Queued in results/queued-freeze/ (process-run.sh never applies it): applied by hand at the freeze, after the final check is
processed - a patch dropped first if a design the final check gives a role uses what it retires
(results/drafts/freeze-retire-641.md).

    git apply results/queued-freeze/rtloop-after-seed91.patch
    git apply results/queued-freeze/rtimmlean-after-seed91.patch

batch-check (641, on 5be0246 - 1 patches): PASS - run-tests PASS (the generators: 107 paths), validate 7 of 7 IDENTICAL,
the jail PASS.

**rtloop-after-seed91.patch** (forth/cv8-fuse-loop.4, forth/cv8-fuse-loopall.4, lab/evolve/GENES.md, lab/evolve/evolve.py, tools/layout.py) - the freeze's retirement, by 578's rule, of a code path the retire report cannot see (several genes choose it): the partial run-time loop compiler - forth/cv8-fuse-loop.4 (84 lines), the -loop dumps, layout.py's LOOP-OPS, X10-XTS and X10-OPS tables - on no design of the pooled true front of seeds 77-91 (0 of 615; 140 of 4,874 alive off it), no hand-made stage, no winner (results/drafts/freeze-audit-641.py). rtloopall retired at 1 (FROZEN - the report's rtloopall=0), rtloop expressed with all eight loop opcodes only, so every front design's id stands; a genome with rtloop and fewer reads rtloop dormant. 120 lines out, 23 in. Tested: every recorded design's id before and after (4,892 - 140 change, the -loop designs; no winner; b35ae710e6 the one in the final check's list: if it takes a role, drop this patch); the bytes of 68 designs - the winners and 40 front designs drawn - at both widths, master against the patched tree (results/drafts/build-hash-641.py): 52 of 52 the same engine and image bytes at 8-byte cells, 0 died; 52 of 52 the same engine and image bytes at 4-byte cells, 0 died (the 28 winners and 24 front designs drawn - 16 of the 40 drawn are no file build-hash reads); batch-check below.

**rtimmlean-after-seed91.patch** (forth/cv8-imm.4, lab/evolve/evolve.py) - the freeze's second code path no front design uses (results/drafts/freeze-audit-641.py): rtimm_lean - rtimm=2 in a plain-CV8 design with nothing else for the run-time fuser (no pairs, no fused tests, no tag, no I+) built forth/cv8-imm.4 alone (Iteration 422, results/wip-regmachine; its four words headerless, the -lit dumps) - on no design of the pooled true front of seeds 77-91, no stage, no winner, 1 of 4,874 alive. canon() reads such a genome's rtimm as 0: it keeps no build of its own, so its id changes rather than standing for another build. 66 lines out, 8 in. Applies after rtloop-after-seed91.patch. Tested: ids before and after both patches (4,892: 141 change - the 140 -loop designs and the one lean; no winner); the bytes of the same 52 designs at both widths, master against both patches applied: RESULT2; batch-check below.
