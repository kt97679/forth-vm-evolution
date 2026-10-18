# The after-seed-59 batch - apply in this order (against master after Iteration 385)

Prepared at Iteration 385, while seed 59 ran: the two faults the free encoding found in seed 58 (HANDOFF
open item 0d). Both change only lab/evolve/evolve.py. Apply after seed 59's processing - seed 59 runs with
the tag-2 requirement, which holds bytehdr on, so the first fault cannot occur in it.

| # | patch | what it does |
|---|---|---|
| 1 | opcall-bytehdr-after-seed59.patch | opcall_on() asks for the tag as the build has it - tag2 with byte headers, as jit_on() and t2wide_on() already do. A genome with tag2=1 and bytehdr=0 was built with OPCALL in an engine without the tag, its CALLNEXT() jumping to the tag's call labels (L_t2call4): all three of seed 58's compile deaths - gcc's two naming the label, clang's "3 errors generated.". |
| 2 | why-after-seed59.patch | why(), a failed tool's words in its died record: the first error, not the last (a link failure's last line is always ld's generic one - all the Tegra's three of seed 57's said only that); where only the generic lines say error, the linker's own line before them; paths cut to their file names, so the words fit 160 characters; a Python traceback keeps its exception line. |

    git apply results/pending/opcall-bytehdr-after-seed59.patch
    git apply results/pending/why-after-seed59.patch

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
