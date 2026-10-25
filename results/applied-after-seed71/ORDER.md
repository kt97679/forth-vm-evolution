# The after-seed-71 batch - applied at seed 71's processing (Iteration 501)

Prepared while seed 71 runs; master stays what seed 71's bundle tests.

    git apply results/applied-after-seed71/retire-nocase-after-seed71.patch
    git apply results/applied-after-seed71/retire-jithelp-jitre-after-seed71.patch
    git apply results/applied-after-seed71/jitfuse-after-seed71.patch
    git apply results/applied-after-seed71/enable-jitfuse-after-seed71.patch
    git apply results/applied-after-seed71/jit-ksig-after-seed71.patch
    git apply results/applied-after-seed71/outputs-checked-after-seed71.patch

**retire-nocase-after-seed71.patch** (forth/cv8b-nocase.4 and forth/cv8bt-nocase.4 removed, lab/evolve/evolve.py,
lab/evolve/engines-check.py) - **the owner retired nocase** (501): it changes only how names are looked up, so it can
make no design faster; it costs bytes and compile time; no selection workload is in lower case - a gene the search
would never keep. Its overlays, its two extra kernel dumps per header system (built at every setup), the gene and its
engines-check variant go; coreext.4's [ELSE] matching without case stays (499: free, and right for any program). Kept
for a revival: results/drafts/nocase-496.md and results/applied-after-seed70/ (nocase-after-seed70.patch). Tested in a
clone of master (35a2a8c) with it: run-tests PASS (93 engine paths).

**fastgate-slower-after-seed71.patch - withdrawn (513)**: seed 70's own data put one reading's noise at 0.96% and the
gate's regression to the mean at 0.07% - the slower of two would add 0.54% of pessimism against a 7-10% that is
not noise (results/drafts/ask-noise-answers-513.md); kept as results/drafts/fastgate-slower-withdrawn-513.patch.

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

**Rebased at 509** (all five): master gained tests/jit/jit-ops.fth, an engines-check variant with 2@ and 2! as
opcodes, and the 2@/2! width fix itself (moved out of jitfuse's patch onto master); jitfuse's branch targets are now
marked by address, a pass each way. Measured again (instructions, seed 70's fastest with the four genes, jitk 3):
kernel +0.3%, fib -16.3%, corpus +0.7%, loop -5.0%, bubble -10.6%, ackermann +1.5%, apps -1.2% - **the geometric
mean -4.6%** (was -3.8%), 1,136 bytes more. engines-check PASS in a clone with all five (99 paths, the new tests on
every JIT variant at both widths). All five apply in order to master.

**jit-ksig-after-seed71.patch** (515; engine/jit.c, lab/evolve/engines-check.py, tests/jit/jit-marker.fth new) - **a bug
found by the bug hunt**: a word made after MARKER at an old word's address ran the old word's native code (jit_k keyed
by the address alone: a CONSTANT 7 answered 5 on JIT designs without jitinl). Each entry now keeps a hash of the bytes
its translation read; a different word is translated again. And jit_usable refuses a stencil with a 32-bit hole, which
the JIT would not patch (none is used). jit-marker.fth on every JIT variant at both widths, a variant without jitinl
added: engines-check PASS, 101 paths (results/drafts/ask-jit-review-answers-515.md).

**outputs-checked-after-seed71.patch** (516; lab/evolve/evolve.py) - **found at seed 71's processing**: measure() timed
the workloads and never looked at what they printed, so the applications workload rewarded failing it - 791 cpt16
designs stopped early in apps on undefined words and timed 0.13 of s6 there against ~1.07 elsewhere, and one reached
the front (908baebc14, wrong on four of appbench's programs). Now every workload's output is compared with s6's from
the same rounds ('Redefining:' warnings left out - a family's kernel has other words): a wrong output kills the design.
No extra run. Tried on 14 of seed 71's designs across encodings: the failing cpt16 ones refused, cell, cpt16 and cv8
otherwise measured. And jitrp not with lto - six seed 71 designs died: global register variable follows a function
definition. Batch-checked with the chain after it (the other five: batch-check PASS on de80601).

**At seed 71's processing**: `sh tools/batch-check.sh` first, then apply, the routine's chain after it.
