# The after-seed-91 batch - the freeze's retirements of the final pooled front (Iterations 642-643; applied at the freeze, Iteration 656)

**The freeze** (Iteration 656): queued in results/queued-freeze/ (process-run.sh never applies it) from 642 until the final
check was processed (648-649) and the rage check passed (654); moved here then and applied by hand in this order. A patch
would have been dropped first had a design the final check gave a role used what it retires
(results/drafts/freeze-retire-641.md): none does - b35ae710e6, the final check's one -loop design, took no role (648).

    git apply results/applied-after-seed91/rtloop-after-seed91.patch
    git apply results/applied-after-seed91/rtimmlean-after-seed91.patch

batch-check (642, on 067a360 - 2 patches): PASS - run-tests PASS (the generators: 107 paths), validate 7 of 7 IDENTICAL,
the jail PASS.

**Applied** (656, on master at e8c6e51; no commit after 067a360 touched the six files): run-tests PASS, validate 7 of 7
IDENTICAL, the jail PASS. The bytes, by results/drafts/build-hash-641.py before and after: the 69 designs of
results/drafts/freeze-ids-656.py - the 29 winners (the final set's 21, the relf handoff's roles at 636 and at 649;
d180351903 the one new) and 40 front designs drawn with random.Random(656) (30 whose build loads -loopall, 10 neither it
nor -fuse-imm) - 69 of 69 the same engine and image bytes at 8-byte cells, 0 died; 69 of 69 at 4-byte cells, 0 died. The
build-out (results/drafts/freeze-build-645.sh with results/relf-designs-649.md's ten roles): validate 7 of 7,
export-designs.py's own check, the export the same as designs/ for 10 of 10 (the GCC three's forth-arm by export-arm.py
--gcc with the cross GCC 13.3, gcc-multilib put back after), make, make test 10 ok, make 32, make libc, pack-designs.py 20
of 20 right, the 40 packed engines and images the bytes of results/drafts/designs-sha256-649.txt: no shipped byte changes.

**rtloop-after-seed91.patch** (forth/cv8-fuse-loop.4, forth/cv8-fuse-loopall.4, lab/evolve/GENES.md, lab/evolve/evolve.py, tools/layout.py) - the freeze's retirement, by 578's rule, of a code path the retire report cannot see (several genes choose it): the partial run-time loop compiler - forth/cv8-fuse-loop.4 (84 lines), the -loop dumps, layout.py's LOOP-OPS, X10-XTS and X10-OPS tables - on no design of the pooled true front of seeds 77-91 (0 of 615; 140 of 4,874 alive off it), no hand-made stage, no winner (results/drafts/freeze-audit-641.py). rtloopall retired at 1 (FROZEN - the report's rtloopall=0), rtloop expressed with all eight loop opcodes only, so every front design's id stands; a genome with rtloop and fewer reads rtloop dormant. 120 lines out, 23 in. Tested: every recorded design's id before and after (4,892 - 140 change, the -loop designs; no winner; b35ae710e6 the one in the final check's list: if it takes a role, drop this patch); the bytes of 68 designs - the winners and 40 front designs drawn - at both widths, master against the patched tree (results/drafts/build-hash-641.py): 52 of 52 the same engine and image bytes at 8-byte cells, 0 died; 52 of 52 the same engine and image bytes at 4-byte cells, 0 died (the 28 winners and 24 front designs drawn - 16 of the 40 drawn are no file build-hash reads); batch-check below.

**rtimmlean-after-seed91.patch** (forth/cv8-imm.4, lab/evolve/evolve.py) - the freeze's second code path no front design uses (results/drafts/freeze-audit-641.py): rtimm_lean - rtimm=2 in a plain-CV8 design with nothing else for the run-time fuser (no pairs, no fused tests, no tag, no I+) built forth/cv8-imm.4 alone (Iteration 422, results/wip-regmachine; its four words headerless, the -lit dumps) - on no design of the pooled true front of seeds 77-91, no stage, no winner, 1 of 4,874 alive. canon() reads such a genome's rtimm as 0: it keeps no build of its own, so its id changes rather than standing for another build. 66 lines out, 8 in. Applies after rtloop-after-seed91.patch. Tested: ids before and after both patches (4,892: 141 change - the 140 -loop designs and the one lean; no winner); the bytes of the same 52 designs at both widths, master against both patches applied: 52 of 52 the same engine and image bytes at 8-byte cells, 0 died; 52 of 52 the same engine and image bytes at 4-byte cells, 0 died; batch-check below.
