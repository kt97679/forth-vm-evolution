# Retiring the older formats - the owner's condition, the plan, the test (Iteration 584)

The owner (584), on bytehdr, varcall, doesfar, scale and lean: "If this simplification will not result in losing good
designs - go ahead." Their other values build only the hand-made stages s2-s5, so retiring them means keeping those
stages as built artefacts rather than rebuilding them from source (results/drafts/retire-candidates-573.md, 1).

**The condition, checked.** No design on the pooled true front of seeds 77-86 (444) uses bytehdr 0, varcall 0, doesfar 0,
scale 1-3 or lean 0 (results/drafts/retire-report-583.md); none of the 232 final-pick candidates does
(results/drafts/retire-candidates-583.py), so no final-set design can. s6, the reference every speed is measured against,
has the front's values (bytehdr 1, varcall 1, doesfar 1, scale 0, lean 1); s0 and s1 have them dormant - all three as
they are. The values live only in s2 (scale 1), s3 (scale 3), s4 (bytehdr 0, varcall 0, scale 3; sharedcall 0) and s5
(bytehdr 0, doesfar 0, scale 3); lean 0 is dormant in every stage. Frozen, s2-s5 are kept, not lost: what goes is
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

**Step 1, the freeze, queued**: freeze-after-seed86.patch (results/queued-consolidation/ORDER.md). Each next patch, one a
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

The next patches' footprints (588, grep counts, not an audit). **lean**, the smallest: its gene row (`gene('lean',
convert=...)`: the two drops when on), LATE, EXPRESSED, HUMAN's s5 and s6; layout.py's measuring switches (_NO_LEAN,
SOD16_NO_DROPX8, SOD16_NO_DROPTOOL). **scale**, the largest: SCALE in vm-lab.c 16 times, spn-cv8.c 14, jit.c 2; in
evolve.py the CV8 base (scale=3), HUMAN, EXPRESSED, BLOCKS, the bytehdr guard, eval32's cap, -DSCALE, --cpt,
reach_lethal and the mutation values; the images' own compiler takes the design's scale (--set-compiler-vars), so the
Forth side stays as it is - its bytes are in every image; test-ext-loops.sh and layout-noise.sh build scale-3 formats.
