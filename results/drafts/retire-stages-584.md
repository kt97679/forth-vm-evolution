# Retiring the older formats - the owner's condition, the plan, the test (Iteration 584)

The owner (584), on bytehdr, varcall, doesfar, scale and lean: "If this simplification will not result in losing good
designs - go ahead." Their other values build only the hand-made stages s2-s5, so retiring them means keeping those
stages as built artefacts rather than rebuilding them from source (results/drafts/retire-candidates-573.md, 1).

**The condition, checked.** No design on the pooled true front of seeds 77-86 (444) uses bytehdr 0, varcall 0, doesfar 0,
scale 1-3 or lean 0 (results/drafts/retire-report-583.md); none of the 232 final-pick candidates does
(results/drafts/retire-candidates-583.py), so no final-set design can. s6, the reference every speed is measured against,
has the front's values (bytehdr 1, varcall 1, doesfar 1, scale 0, lean 1); s0 and s1 have them dormant - all three as
they are. The values live only in s2 (scale 1), s3 (scale 3), s4 (bytehdr 0, varcall 0, scale 3; sharedcall 0) and s5
(bytehdr 0, doesfar 0, scale 3); lean 0 is in s4 only - not dormant there: built with lean on, s4's image changes (589). Frozen, s2-s5 are kept, not lost: what goes is
building them again from source.

**The test, mechanical** (results/drafts/build-hash-584.py): every pooled-front design, every candidate and the seven
stages built by evolve.py's own build() - at 8-byte cells, and at 4 as eval32 builds them - their engine and image
hashed, each in a fixed directory. Deterministic (four designs built twice: the same bytes); about 1.2 s a design here,
so about 15 minutes a width. On master at 584: results/drafts/build-hash-584-8.jsonl and -4.jsonl. Each patch below
passes only when every design but s2-s5 hashes the same on the patched tree - the same engine bytes and image bytes, so
the same design, measured or not. The hashes are this sandbox's compilers': a new chat checks a few against its own
build before relying on them, or reruns master.

**What goes** (grep counts, not an audit): the engine's VARCALL paths (17 lines naming it, vm-lab.c and spn-cv8.c),
SCALE (32, jit.c's 2 among them), DOESFAR (10), SHAREDCALL (7); layout.py's scaled call targets (--cpt) and full headers
(--bytehdr's other side); each gene FROZEN at the front's value, as tail and kstack (the ids unchanged).

**What uses s2-s5 by name** (12): tools/build-stages.sh, run-tests.sh, test-ext-loops.sh, arm-cross-check.py,
clockfit.py, collect-results.sh, compare-commits.py, layout-noise.sh, show-word.sh, spn-bench.py; lab/evolve/design.py
and evolve.py (HUMAN; --validate's 7 of 7). The remote hosts run build-stages.sh before each check: dream at both widths,
the Tegra natively - no x86 artefact runs there.

**The sequence** - one patch each, queued in results/queued-consolidation/ after fsys45, each passing the build hashes
at both widths, run-tests, validate and batch-check:
1. **freeze**: s2-s5's engines and images, 8- and 4-byte cells, tracked with their hashes; build-stages.sh copies them
   instead of building; --validate rebuilds s0, s1 and s6 and checks s2-s5's hashes; the twelve read them where they are;
   the remote hosts skip s2-s5 (each tool's need checked first); the owner's rage-check.sh after.
2. **scale** 1-3 -> 0: the engine's SCALE paths, layout.py's scaling, eval32's cap.
3. **varcall** 0 -> 1, sharedcall with it (dormant wherever varcall is on).
4. **doesfar** 0 -> 1.
5. **bytehdr** 0 -> 1: the full-header formats.
6. **lean** 0 -> 1: --drop-x8 and --drop-dumptool unconditional for cv8.

**When**: applied at consolidation, after chain B's final pick, with fsys45. Built in fresh chats - the freeze first,
the largest; then a gene a patch - each starting from this file and the baseline hashes.

## In practice (Iteration 588)

**Step 1, the freeze, queued**: freeze-after-seed86.patch (results/pending/ORDER.md). Each next patch, one a
chat: as root `PENDING=results/queued-consolidation SCRATCH=/tmp/x sh tools/setup-sandbox.sh` (master and the queue
applied, built); the patch committed in /tmp/x, its subject's first word the gene (`scale: ...`); `PENDING=
results/queued-consolidation sh tools/batch-make.sh 86 N /tmp/x` and its ORDER.md paragraph committed; then
`setsid nohup sh results/drafts/retire-test-588.sh /tmp/x &` - a fresh clone of /tmp/x built, --validate, build-hash-584.py
at both widths compared with the 584 hashes by build-hash-cmp-588.py, then batch-check of the queue (RECORD=1), polled to
DONE in /tmp/vh/status: about an hour here, so start it early in the turn. --validate comes before the hashes: it makes
the dictionary dumps the 8-byte build reads - a tree built but not validated kills designs (FileNotFoundError), not a
patch's fault. A gene patch leaves s2-s5 to stages/frozen: --validate checks their hashes and never builds their HUMAN
genomes; the tools that build those genomes or their formats move with the patch that retires the value - test-ext-loops.sh
and layout-noise.sh (scale 3), arm-cross-check.py (HUMAN, each patch), design.py's bases (s4-cv8).

Two lessons from the freeze (588). evolve.py's `FROZEN` is the genes' dict (tail, kstack, tailpn - frozen genes); the
stage tuple first took that name, was shadowed by it, and --validate silently rebuilt s2-s5 still 7 of 7 - caught,
renamed FROZEN_STAGES, the branch run by hand (four hashes IDENTICAL, each alive): grep a module name before adding one.
And hv.load keys records by their recorded id, so a canon() change - a gene frozen, fsys45's 4-5 read as 3 - re-identifies
only designs built after it; the pooled fronts stand.

**Step 2, lean, queued (589)**: lean-after-seed86.patch - FROZEN's 'lean': 1 (in LATE and EXPRESSED still, so the ids
stand), the row's two drops for every CV8 design, layout.py's lean-off switches gone. Build-hash 667 of 667 the same at both widths, batch-check PASS on the 3 patches (run-tests PASS, validate 7 of 7 IDENTICAL, the jail PASS). The
frozen stages' own line is the patch's control: s4, the one stage with lean 0, built from source changes its image (its
engine the same); s2, s3, s5 the same. Next: scale, varcall with sharedcall, doesfar, bytehdr - one a chat.

**Step 3, scale, queued (590)**: scale-after-seed86.patch - scale retired at 0 for CV8 only. 584's "the engine's SCALE
paths go" was wrong: SCALE is not CV8's alone - cpt16 expresses scale (built at max(1, scale)), sod16 builds at SCALE 1,
and s1-sod16 is rebuilt from source; vm-lab.c's `cbase + (t << SCALE)` and layout.py's --cpt serve them, so they stay,
and so do eval32's cap and canon()'s bytehdr guard (cpt16's). What goes: the CV8 gene (FROZEN, and mutate()'s pool now
excludes FROZEN for CV8 alone, as require() applies it - only scale, of the FROZEN genes, is expressed outside CV8) and
the JIT's two shifts (dead: JITVAR needs TAG2, which #errors unless SCALE 0). The far-DOES> line keeps `- SCALE` (right
at any scale). s4 and s5 still build from source (a hand-made genome bypasses require()), so the tools that build them
need no move. Tested by retire-test-588.sh: build-hash 667 of 667 the same at both widths (s2, s3, s5 from source the
same; s4 lean's change), batch-check PASS on the 4 patches. No design lost: seeds 77-86's results files hold 2681 designs, all CV8, 2 at scale 1 or 3, neither on the
front; the 232 candidates, the final 14 and the shortlist 40 all at scale 0. Removing SCALE itself would mean retiring
the cpt16 and sod16 families - none recorded since seed 77, but not in the owner's go-ahead (584's five genes) - asked; the owner (590): "let's not retire them now" - they stay.

**Step 4, varcall with sharedcall, queued (592)**: varcall-after-seed86.patch - FROZEN's 'varcall': 1, 'sharedcall': 1 (sharedcall already dormant under varcall: express() drops it, build() forced it on). Unlike scale, nothing outside CV8 used either: SHAREDCALL appears only as `ENC == 3 && SHAREDCALL`, and VARCALL defaulted to 1 in both engines, read only in CV8's code - so the engines' fixed 15-bit call (NEXT's per-handler call, do_call's and DODOES's 15-bit decode, the HOTCALLS #error) went, in vm-lab.c and spn-cv8.c alike, with layout.py's --no-varcall and sod16.py's VARCALL and every -DVARCALL/-DSHAREDCALL. s4 can no longer be built from source: build() refuses varcall 0 by name, design.py's example base and test-ext-loops.sh's s4 line went with it (the tools of 588's list that build its format). The image's compiler variable CV8-VARCALL-V stays, written -1 (its bytes are in every image). Tested by retire-test-588.sh: build-hash 667 of 667 the same at both widths (s2, s3, s5 from source the same; s4 now refused by build() - varcall 0), validate 7 of 7 IDENTICAL on the patched tree, batch-check PASS on the 5 patches (run-tests PASS, validate 7 of 7 IDENTICAL, the jail PASS); the 8-byte hashes resumed after a turn's end, the 150 missing by --only. Next: doesfar, then bytehdr - one a chat.

**Step 5, doesfar, queued (593)**: doesfar-after-seed86.patch - FROZEN's 'doesfar': 1. The engines' DOESFAR switch went (vm-lab.c, spn-cv8.c, gen-tos.py's DOVAR: CREATE reserves three bytes, a far DOES> call counts cells) and layout.py's --does-far (the far form and its compiler variables for every CV8 design); build() refuses doesfar 0. s5's engine is no longer built from source, so layout-noise.sh moved to s6; test-ext-loops.sh keeps s5's line (layout.py writes s5's image as before - no DOES> tail at 16K cells - run on the frozen engine). Kept: cv8.4's CV8-DOES-FAR? branch (image bytes) and DODOES's near form (tails under 16 KB). The engines preprocessed the same at 22 settings (doesfar-pp-593.sh); s6's images the same with --does-far. Tested by retire-test-588.sh: build-hash 667 of 667 the same at 8-byte cells and 667 of 667 at 4 (s5 now refused by build() - doesfar 0), validate 7 of 7 IDENTICAL on the patched tree, batch-check PASS on the 6 patches (run-tests PASS, validate 7 of 7 IDENTICAL, the jail PASS); the run cut off by a turn's end and resumed (RESUME=1). retire-test-588.sh resumes now: RESUME=1 keeps the clone, build and validate and each width's hashes (build-hash-584.py --resume). Next: bytehdr - the last.

**Step 6, bytehdr, queued (594) - the last**: bytehdr-after-seed86.patch - FROZEN's 'bytehdr': 1. The engines had no switch (F_BYTEHDR in every CV8 engine's features), so what went is CV8's full-header format: layout.py refuses --v8 without --bytehdr, which already wanted --cpt 0, so every CV8 image's calls are unscaled - v8val, v8pfa, v8loc and the far DOES> call lose their shifts and CV8-SHIFT-V is written 0; the full-header side stays for cpt16 (kept, 590), and canon()'s cpt16 guard with it. The -self dumps (cv8.4 without cv8b.4) went: setup()'s 63, build-stages.sh's k64/k32-self and d64/d32-self (the last read by s5's image line until the freeze), and the remote hosts' copy of k32-self.txt. build() refuses bytehdr 0; test-ext-loops.sh lost s5's line (layout.py no longer writes its format). The Forth side as it was: cv8.4's full-header words are in every image, cv8b.4 overriding them. Tested by retire-test-588.sh: build-hash 667 of 667 the same at both widths (s2, s3 from source the same; s4 and s5 refused by build()), validate 7 of 7 IDENTICAL on the patched tree, batch-check PASS on the 7 patches (run-tests PASS, validate 7 of 7 IDENTICAL, the jail PASS); cut off by a turn's end at the 4-byte hashes and resumed (RESUME=1). All six steps queued: they apply at consolidation with fsys45 (retire-plan-583.md), after chains C and D's processing.

The next patches' footprints (588, grep counts, not an audit). **lean**, the smallest: its gene row (`gene('lean',
convert=...)`: the two drops when on), LATE, EXPRESSED, HUMAN's s5 and s6; layout.py's measuring switches (_NO_LEAN,
SOD16_NO_DROPX8, SOD16_NO_DROPTOOL). **scale**, the largest: SCALE in vm-lab.c 16 times, spn-cv8.c 14, jit.c 2; in
evolve.py the CV8 base (scale=3), HUMAN, EXPRESSED, BLOCKS, the bytehdr guard, eval32's cap, -DSCALE, --cpt,
reach_lethal and the mutation values; the images' own compiler takes the design's scale (--set-compiler-vars), so the
Forth side stays as it is - its bytes are in every image; test-ext-loops.sh and layout-noise.sh build scale-3 formats.
