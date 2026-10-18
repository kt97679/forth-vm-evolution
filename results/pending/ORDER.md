# The after-seed-59 batch - apply in this order (against master after Iteration 385)

Prepared at Iterations 385 and 387, while seed 59 ran: the two faults the free encoding found in seed 58
(HANDOFF open item 0d), and from the methodology review (results/review-methodology-386.md) the switch for a
clean anchoring test and two fixes to the comparison. Patches 1-2 change lab/evolve/evolve.py; 3 evolve.py
and lab/evolve/next-run.sh; 4 lab/evolve/compare-fronts.py. Apply after seed 59's processing - seed 59 runs with
the tag-2 requirement, which holds bytehdr on, so the first fault cannot occur in it.

| # | patch | what it does |
|---|---|---|
| 1 | opcall-bytehdr-after-seed59.patch | opcall_on() asks for the tag as the build has it - tag2 with byte headers, as jit_on() and t2wide_on() already do. A genome with tag2=1 and bytehdr=0 was built with OPCALL in an engine without the tag, its CALLNEXT() jumping to the tag's call labels (L_t2call4): all three of seed 58's compile deaths - gcc's two naming the label, clang's "3 errors generated.". |
| 2 | why-after-seed59.patch | why(), a failed tool's words in its died record: the first error, not the last (a link failure's last line is always ld's generic one - all the Tegra's three of seed 57's said only that); where only the generic lines say error, the linker's own line before them; paths cut to their file names, so the words fit 160 characters; a Python traceback keeps its exception line. |
| 3 | noevolved-after-seed59.patch | `noevolved` (next-run.sh) and `--noevolved` (evolve.py): nocarry, and no founder drawn from an earlier run's record - seed 37's fastest and seed 40's knee left out, the hand-made designs and the founders built from them kept: the anchoring test as seed 36 ran it, before those founders existed (review, section 1: they are two thirds of seed 58's ancestry). Opt-in: nothing changes without it. |
| 4 | compare-fronts-after-seed59.patch | The verdict's sign labelled in both sections - a positive figure is the run ahead (review 4a: read backwards at 384); and --frontier keeps each run's 32-bit fastest beside its 64-bit bests, as the verdict at both widths reads it (review 4d: latent, a 32-bit specialist dominated at 64 bits could be dropped). |

    git apply results/pending/opcall-bytehdr-after-seed59.patch
    git apply results/pending/why-after-seed59.patch
    git apply results/pending/noevolved-after-seed59.patch
    git apply results/pending/compare-fronts-after-seed59.patch

Tested at Iteration 385, in a scratch clone of master at 31b591c:

The first: seed 58's front design 8259be4f90 (tag2, opcall R>, built by clang), its bytehdr set to 0 -
before, died: engine did not compile (3 errors generated.); after, built (12,360 + 11,753 bytes, opcall not
expressed) and fib exit 0. The design as recorded, the control: 22,308 + 8,235 bytes before and after - its
record's - and fib exit 0. All 1,093 front genomes of seeds 53-58 expressed the same with and without it.

The second: synthetic failures through the old why() and the new. A compile error behind a long path: was
cut off inside the path, now (vm-opcall-bodies.h:1:1: error: label 'L_t2call4' used but not defined). A link
failure: was (collect2: error: ld returned 1 exit status), now the undefined reference. An LTO failure: was
the same collect2 line, now the register error. A Python assertion: (AssertionError: dump incomplete) both -
the first draft gave (assert ok), caught by this test and fixed. A silent crash: (exit 139) both.

Both applied: run-tests.sh PASS - no regressions; evolve.py --validate 7 of 7 IDENTICAL; test-jail.py PASS. On a fresh clone
of master the two apply in this order, and lab/evolve/evolve.py is then byte for byte the tested file.

Tested at Iteration 387, in a scratch clone of master at Iteration 386 with patches 1-2 applied:

The third: next-run.sh's keyword block run alone on its arguments - `seed 60 tag2 12h widths noevolved` (and
noevolved before widths) gives NOEVOLVED=1, NOCARRY=1, WIDTHS=1, `seed 60 tag2 12h` left; nocarry and fromzero
as before; no keyword, nothing set; the environment alone (the detached chain's path) NOEVOLVED=1; the
resume key "seed 60 tag2 noevolved nocarry at ..." - so a noevolved run never resumes a nocarry one. And
evolve.py --pop 8 --gens 0 --rounds 1 --noevolved --require tag2: both evolved founders reported left out,
generation 0 the 7 hand-made designs and the 8 founders built from them (two died at the reach limit, as
without the switch), the best start the s6 + JIT founder at 0.81 - against seed 37's 0.174 under nocarry; exit 0.

The fourth: the thinning block of the old file and the new run on three designs - the 64-bit fastest, the
smallest, and a 32-bit specialist dominated at 64 bits (slower, larger, more memory): the old kept two, the
new all three.

All four applied: run-tests.sh PASS - no regressions; evolve.py --validate 7 of 7 IDENTICAL; test-jail.py PASS. On a fresh clone of
master the four apply in this order, and lab/evolve/evolve.py, next-run.sh and compare-fronts.py are then byte for
byte the tested files.
