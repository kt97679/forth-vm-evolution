# The freeze's retirements, read and prepared while the final check runs (Iteration 641)

**The values (results/drafts/retire-report-639.md, 12 on no pooled-front design).** Four stay: bss=0 (s6, s0 and s1
build with it), fsys=0 (690981ca5b, a winner), jitdoes=1 (3ee67e7d34 and be42bd8ea4, winners), msc=1 (the owner, 626).
The other eight remove no code - the search space only, kept by 583's reading ("kept: nothing simpler",
results/drafts/retire-plan-583.md): alignhot=1 (a flag string in ALIGNV - removing it shifts later values' ids), hotcalls=8
(a number layout.py takes as it is), jit=0, jitinl=0, jitos=0, jitrp=0 (a late gene's 0: the gene fixed on where live,
the plain path still every other design's), opbody=0 (layout.py adds OPBODY's words to _OPB, nothing of its own) and
rtloopall=0 - which alone goes, with the code path below.

**The code paths (results/drafts/freeze-audit-641.py).** A path several genes choose together is no value, so the report
does not see it. The run-time overlay each build loads, over the pooled true front of seeds 77-91:

| overlay | front | alive | list + winners |
|---|---|---|---|
| (none) | 64 | 854 | 65 |
| -fuse-imm-loop | 0 | 2 | 1 |
| -fuse-imm-loopall | 9 | 30 | 0 |
| -fuse-imm-loopall-iplus | 27 | 174 | 34 |
| -fuse-imm-loopall-iplus-empty | 2 | 18 | 2 |
| -fuse-loopall | 0 | 12 | 0 |
| -fuse-loopall-empty | 0 | 3 | 0 |
| -fuse-loopall-iplus | 115 | 675 | 86 |
| -fuse-loopall-iplus-empty | 0 | 2 | 0 |
| -lit-loopall | 0 | 1 | 0 |
| -loop | 0 | 132 | 0 |
| -loop-empty | 0 | 6 | 0 |
| -loopall | 393 | 2892 | 268 |
| -loopall-empty | 5 | 73 | 0 |
the hand-made stages: s4-cv8 (none), s5-cv8spec (none), s6-cv8b (none)
-loop users in the list and the winners: b35ae710e6
rtimm_lean (forth/cv8-imm.4 alone): front 0, alive 1, list + winners 0

- **The partial run-time loop compiler** (`-loop`: forth/cv8-fuse-loop.4, the -loop dumps, layout.py's LOOP-OPS, X10-XTS
  and X10-OPS tables) - on no front design (0 of 615; 140 of 4,874 alive off it, 135 of them rtloop=2 designs whose ids
  595 changed already), no hand-made stage, no winner. **The batch's one patch**, results/queued-freeze/
  rtloop-after-seed91.patch: rtloopall retired at 1 (FROZEN), rtloop expressed with all eight loop opcodes only - 120 lines
  out, 23 in (forth/cv8-fuse-loop.4's 84, layout.py 30 to 6). In the final check's list one design uses it, b35ae710e6
  (chain-followup87's fastest on the laptop at 4-byte cells, off the front): if it takes a role, the patch is dropped.
- **rtimm_lean** (`-lit`: forth/cv8-imm.4 loaded alone, RTIMM_LEAN_INTERNAL headerless; Iteration 422) - on no front
  design, 1 alive, none listed or winning. **The batch's second patch** (643), results/queued-freeze/
  rtimmlean-after-seed91.patch: forth/cv8-imm.4 (55 lines, its own header calls it work in progress), the -lit dumps, the
  headerless list; canon() reads such a genome's rtimm as 0 - the build it had is gone, so it takes another id rather than
  standing for another build (a genome before 422 built the fuser under the same conditions; neither is on the front).
  66 lines out, 8 in. Ids with both patches: 141 of 4,892 change (the 140 -loop designs, the one lean), no winner; the bytes
  of the 52 designs at both widths with both patches applied: 52 of 52 the same engine and image bytes at 8-byte cells, 0 died; 52 of 52 the same engine and image bytes at 4-byte cells, 0 died.

**The patch's test.** Every recorded design's id before and after (evolve.gid, 4,892 designs: the pool, the list, the
winners): 140 change - the -loop designs, none of the winners, b35ae710e6 the one listed. The bytes: 68 designs - the 28
winners (the final set's 21, the relf handoff's ten) and 40 front designs drawn (seed 641: 30 with -loopall, 10 without) -
built by results/drafts/build-hash-641.py (build-hash-584.py reaching the portable pools and the kept designs) on master and on the patched tree at both widths: 52 of 52 the same engine and image bytes at 8-byte cells, 0 died; 52 of 52 the same engine and image bytes at 4-byte cells, 0 died (the 28 winners and 24 front designs drawn - 16 of the 40 drawn are no file build-hash reads). batch-check PASS (run-tests, validate 7 of 7 IDENTICAL, the jail; results/queued-freeze/ORDER.md).
