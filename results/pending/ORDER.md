# The after-seed-71 batch - applied at seed 71's processing (Iteration 501)

Prepared while seed 71 runs; master stays what seed 71's bundle tests.

    git apply results/pending/retire-nocase-after-seed71.patch
    git apply results/pending/fastgate-slower-after-seed71.patch
    git apply results/pending/retire-jithelp-jitre-after-seed71.patch
    git apply results/pending/jitfuse-after-seed71.patch
    git apply results/pending/enable-jitfuse-after-seed71.patch

**retire-nocase-after-seed71.patch** (forth/cv8b-nocase.4 and forth/cv8bt-nocase.4 removed, lab/evolve/evolve.py,
lab/evolve/engines-check.py) - **the owner retired nocase** (501): it changes only how names are looked up, so it can
make no design faster; it costs bytes and compile time; no selection workload is in lower case - a gene the search
would never keep. Its overlays, its two extra kernel dumps per header system (built at every setup), the gene and its
engines-check variant go; coreext.4's [ELSE] matching without case stays (499: free, and right for any program). Kept
for a revival: results/drafts/nocase-496.md and results/applied-after-seed70/ (nocase-after-seed70.patch). Tested in a
clone of master (35a2a8c) with it: run-tests PASS (93 engine paths).

**fastgate-slower-after-seed71.patch** (lab/evolve/evolve.py, 503; the owner agreed to proposal 6 of
results/drafts/process-review-501.md): a gated design - faster than the fast gate, measured a second time in the next
generation's batch - takes the slower of its two readings, each workload's, not their geometric mean. Free: no reading
more - the whole slower reading: a first version took each workload's slower time, which compounded (0.70 and 0.70
made 0.74, slower than either). Tested: applies after the retirement; three generations of the evolver with both and
the gate at the third fastest - gated designs measured again, the slower reading kept (0.9512 then 0.9771: 0.9771).

**retire-jithelp-jitre-after-seed71.patch** (504; engine/jit.c, engine/spn-stencils.c, engine/vm-lab.c, tools/layout.py,
lab/evolve/evolve.py, lab/evolve/review-checks.py, results/seed63-rules.md): **jithelp and jitre retired** - frozen since
455, 12 of 12 removal votes, on no front since; the owner's word for them at 432-455: out again if useless. Every
jithelp-only and jitre-only block of the engine removed (the C helpers called from native code, st_callc and the
function hole, the rows' function field; the interpreted call, S_INTERP); jit_interp, its sentinel and its trampoline
kept - jitexec's interpreted path - under JITEXEC alone; the genes, their flags and converter options gone; rule 2
watches jitret alone. Tested in a clone with all three patches: run-tests PASS (93 engine paths, the differential JIT
test on every JIT variant at both widths), validate 7 of 7.

**jitfuse-after-seed71.patch** (507; engine/jit.c, engine/spn-stencils.c, tools/layout.py, lab/evolve/evolve.py,
lab/evolve/engines-check.py, tests/jit/jit-diff.fth): **the gene jitfuse, staged frozen** - a literal into +, <, >, =,
XOR, AND or OR, and I into + or 2@, copied as one stencil (results/drafts/jit-pairs-506.md); never where the second
operation is a branch target. Seven stencils (LIT + is st_addi's). Found while testing: the pairs were first marked before
the callees were translated - a callee's translation overwrote them (the far test crashed); now marked just before the
sizes, as jitk_tg is. And 2@ and 2! in the converter's JIT map took eight-byte cells at either width - by the cell now,
as CELL+ at 493. jit-diff.fth gains the pairs, a branch into one, 2@ and 2!. engines-check PASS (two variants more, with
and without jitk, both widths). **Measured** (instructions, seed 70's fastest with the four JIT genes, jitk 3): fib
-16.3%, bubble -9.3%, loop -4.8%, apps -0.9%, kernel +1.2%, corpus +2.4%, ackermann +2.7% - the geometric mean of the
seven -3.8%, for 912 bytes more (+2.4%).

**enable-jitfuse-after-seed71.patch** (508; lab/evolve/evolve.py) - **the owner enabled jitfuse**: out of FROZEN, for
the search to weigh its speed (-3.8% of instructions over the seven workloads) against its bytes (+2.4%). Rule 11: the
selection sees both - every workload runs JIT code on a JIT design. Rule 12: its votes count from seed 73
(review-checks.py's GRACE). Predicted (results/predictions.md).

**At seed 71's processing**: `sh tools/batch-check.sh` first, then apply, the routine's chain after it.
