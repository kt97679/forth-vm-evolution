# The after-seed-70 batch - applied at seed 70's processing (Iterations 488-490)

Prepared while seed 70 runs; master stays what seed 70's bundle tests. Three patches, in this order:

    git apply results/pending/jit-more-after-seed70.patch
    git apply results/pending/coreext-2r-after-seed70.patch
    git apply results/pending/jit-32bit-after-seed70.patch

**jit-more-after-seed70.patch** (engine/jit.c, engine/spn-stencils.c, engine/vm-lab.c, tools/layout.py):

1. **(ABORT") native** (488; jitexec with jitmul): one operation, its inline message skipped - the message was decoded
   as code before; a false flag dropped, a true one handed back to the interpreter at the call itself (a resume helper
   through a new hole, SPN_RS_VALUE, longjmps to jit_call's return point) - (ABORT") then never returns.
2. **JIT_MAXOPS 256 to 1024** (488).
3. **Every image word's end from the converter** (489; JIT_NWENDS, jit_wends): an image word reached without its header
   was decoded to "the first EXIT no branch passes" - DABS, eight bytes, ran 43 bytes into FM/MOD's header.
4. **Depth** (490): JIT_DEPTH 8 to 16, and a refusal caused only by depth no longer cached below the top - it was, so
   fcp's DABS, first met nine calls below MAKEMOVE, stayed bytecode for good, and SM/REM, FM/MOD, /MOD, /, DIFF>DIR,
   SQATTACKS?, ATTACKS? and MAKEMOVE with it. The refusal log now says so (why 7); before, a depth refusal carried the
   last refusal's stale address and reason - the "return stack's order" that hid this cause in fcp and cd16sim.

**coreext-2r-after-seed70.patch** (forth/coreext.4, 489): 2>R, 2R> and 2R@ compile in place (IMMEDIATE, POSTPONEd
stack operations) - their own bodies moved their return address, which kept every caller from the JIT; their
interpretation semantics are undefined (Forth 2012).

**Tested here (490)**, both patches in the working tree: against the interpreter, line for line, on s6 with the JIT and
all four genes and on seed 68's fast design - (ABORT") false, caught and uncaught; 2>R, 2R>, 2R@ in the Forth 2012
tests' shapes and a loop; signed division, MOD, SM/REM, DABS, /MOD; the corpus; engines-check PASS (64 and 32 bits);
ans-check 0 of 3 of seed 69's front differ, its negative control caught. **The JIT now leaves 0.1% of the dispatches of
fcp, brainless and cd16sim to the interpreter** (17.5%, 5.8% and 18.1% before the batch); seed 68's fast design with all
four genes runs the seven applications at 0.234 of s6 - fcp 0.165, cd16sim 0.300 (0.317 and 0.573 without the batch)
- every output right.

**jit-32bit-after-seed70.patch** (493; engine/jit.c, engine/spn-stencils.c, engine/vm-lab.c, tools/layout.py): the new
genes at 32 bits. The throw, EXECUTE and resume holes in the i386 stencils (they were x86-64 only, so UM/MOD, EXECUTE
and (ABORT") were traps there - never used); the JIT's hole values and widths at 32 bits; an i386 trampoline into
jit_leave (mov ecx; jmp ecx - eax and edx are its arguments) and jit_leave SPN_CC; the stencils' inline-cache hits
calling native code as spn_fn - SPN_CC, which the plain cast was not at 32 bits; the helpers realigning their stack
(force_align_arg_pointer). **And a bug of the 32-bit batch itself**: the converter's JIT map had CELL+ as ADDI 8 and
CELLS as LSHIFT 3 - eight-byte cells - at either width; now by the cell. Tested: s6 at 32 bits interpreted, with the
JIT, and with the JIT and all four genes - EXECUTE, DOES>, division and its throw, (ABORT"), strings, PICK, ALIGNED -
equal line for line, each through the corpus; engines-check PASS at both widths with all three patches.

**At seed 70's processing**: `sh tools/batch-check.sh` first, then apply both, the routine's chain after it.
