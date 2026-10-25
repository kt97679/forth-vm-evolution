# The answers to the JIT-table review, checked - no bug this time (Iteration 531)

Five answers to results/drafts/ask-jit-table-530.md (the owner, 531; one in the message itself). Every claim checked
against the kernel, the converter, jit.c and the tests that already run.

## The claims

| claim | who | verdict |
|---|---|---|
| 2@ (DUP ADDI FETCH SWAP FETCH) returns the two cells reversed | 59 "high, conditional", 61 "high", 62 "high"; 60 unsure | **wrong** - the kernel's 2@ is `DUP CELL+ @ SWAP @` (forth/kernel.4:452), which is the standard's own stated equivalent (6.1.0350: x2 at a-addr, x1 in the next cell). The row is that sequence exactly. The answers had the standard's order backwards |
| 2! (SWAP OVER STORE ADDI STORE) stores them swapped | 59, 62 | **wrong** - the kernel's 2! is `SWAP OVER ! CELL+ !`, the standard's stated equivalent (6.1.0310); the row is that sequence |
| EXECUTE, CALLX, ABORT" rows read 8 operand bytes at 32 bits (kind 4) | 62 "medium-high" | **wrong** - no image byte maps to those rows: jit_body sets them with the argument already made (an inline cache's address; jit.c 854, 865, 965, 1004); kind 4 only says the argument fills the literal hole whole. engines-check runs jitexec at 32 bits |
| <>?BRANCH inverted | 60, withdrawn by itself | right to withdraw - `<> ?BRANCH` fused |
| ?NBRANCH: branch on nonzero or negative? | 60 "verify" | **correct** - the fusion of `0= ?BRANCH` (sod16.py TESTBR): branch when x is not zero, which LIT 0 EQ 0BRANCH does |
| the extra rows' bound is weaker than its comment (M+4 < 0xFE00), one row left empty | 60 | **true, harmless** - the highest real number is in the hundreds; now asserted |
| jit_op.k is a signed char; a constant over 127 would wrap | 60 | **true, latent** - the largest today is 8; now asserted |
| JIT_DOVAR read raw, would fail if DOVAR had no one-byte code | 60 | true in form; a build would fail loudly, not silently |

**Already shown**: tests/jit/jit-ops.fth runs `11 22 B1 2! B1 2@ . . B1 @ . B1 CELL+ @ .` on every JIT variant at both
widths against the interpreter (engines-check, PASS); the Forth 2012 core tests expect `1ST 2@ -> 2 1` after
`2 1 1ST 2!` and JIT designs pass them (ans-check, 0 of 38 differ at 520); jit-diff.fth's `8 MOD 0= IF` exercises the
?NBRANCH fusion at both widths.

## Hardening taken

The two bounds a reviewer named, asserted in tools/layout.py (the after-seed-73 batch's sixth patch): the extra rows
below T2_JIT, and each row's constant within a signed char. Neither fires today; either would now stop a build with a
message instead of a wrong table.

## The answers, ranked

60 the most useful: it checked its own derivations (withdrew <>?BRANCH), found the two latent bounds, and left 2@/2! as
"verify" rather than claim. 59 careful in form - it qualified its 2@/2! claim as conditional - but on a misremembered
standard. The answer in the message: "all correct", without detail - right. 61 and 62: confident and wrong on 2@, and
62's 32-bit EXECUTE claim misreads how those rows are made. A round with no bug is a result: the table's last three
bugs were found by our tests, and this review found none they missed.
