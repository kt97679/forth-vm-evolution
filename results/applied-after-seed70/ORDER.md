# The after-seed-70 batch - applied at seed 70's processing (Iterations 488-490)

Prepared while seed 70 runs; master stays what seed 70's bundle tests. Six patches, in this order:

    git apply results/applied-after-seed70/jit-more-after-seed70.patch
    git apply results/applied-after-seed70/coreext-2r-after-seed70.patch
    git apply results/applied-after-seed70/jit-32bit-after-seed70.patch
    git apply results/applied-after-seed70/jitrp-after-seed70.patch
    git apply results/applied-after-seed70/decisions-after-seed70.patch
    git apply results/applied-after-seed70/nocase-after-seed70.patch

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

**jitrp-after-seed70.patch** (494; engine/spn-stencils.c, engine/vm-lab.c, tools/gen-jitk.py, lab/evolve/evolve.py,
lab/evolve/engines-check.py): the 465 prototype made **the gene jitrp**, staged frozen - the JIT's return-stack pointer
in a register across the stencils (GCC's global register variable; GCC and 64-bit only; r15, or rbx under regpin 2,
r13 under regpin 3 - clear of regpin's). Rebased onto the batch: the native call site reads the register after a
return and after a throw or a resume (JIT_RP_GET), and the nested interpreter (jit_interp, for EXECUTE's interpreted
path) starts from it. Right against the interpreter on s6 with every JIT gene, with jitrp, and with jitrp beside
regpin 2 (nested loops, >R and R@, EXECUTE, DOES>, I and J, ABORT" and division throws through CATCH, LEAVE, ?DO), the
corpus each; engines-check PASS at both widths. Instructions (cachegrind) on seed 68's fastest GCC JIT design,
6c0c4e6886: loop -19.2%, bubble -4.0%, fib 0.0%, ackermann +2.0% - the 465 prototype's figures again; on s6 with the
JIT, whose loops run otherwise, -0.4% at most. Frozen until the owner says.

**decisions-after-seed70.patch** (495; lab/evolve/evolve.py) - **the owner's decisions**: (1) **the applications in the
selection** - `apps`, the seventh selection workload: our own four applications, their source inline (no file needed
wherever it runs), one short pass each - sim16 running fib(15) on its simulated CPU, gc16 200 steps, scan 3 builds,
evo 12 generations - 0.058 s on s6 (0.010 of it compiling the four), 0.016 s on seed 68's fast design with the four
genes, its output s6's; the speed objective's geometric mean now over seven - **a break in the speed column from the
first run with it**; Appbench's programs stay held out (appbench.py). (2) **jitos frozen** (12 of 12 removal votes over
seeds 67-69). (3) **jitrp enabled** (out of FROZEN). Tested in a clone with all five patches: run-tests PASS; one
generation of the evolver, 33 designs, each measured on `apps` too, its report naming seven workloads.

**nocase-after-seed70.patch** (497; forth/cv8b-nocase.4 and forth/cv8bt-nocase.4 new, lab/evolve/evolve.py,
lab/evolve/engines-check.py): **the gene nocase**, staged frozen - names without case (results/drafts/nocase-496.md).
An X8 overlay after kfast's and kinput's: FOLD8 (ASCII a-z only), NAME>BUF8 folding NAMEBUF after the copy (every
search, the C walks included), HEADER8 folding the name it stores - one per header system (cv8bt's links are up to
4 bytes). Needs kfast, not klookup (whose (FIND) copies the key in C). Two kernel dumps per header system more
(-kfast-nocase, -kfast-kinput-nocase). Tested: a lower-case program - definitions, EVALUATE, variables, mixed case,
loops, ' and EXECUTE - right with the gene on s6 with kfast, with kinput, and with tag 2 and the JIT (undefined words
without it), the corpus each; **Appbench's fcp and cd16sim run with no folding of their source** (fcp's results,
cd16sim's own check right); lexex and benchgc stop at a word their own files define (show-set, mark-stack) - not yet
traced; run-tests PASS (an engines-check variant with it), validate 7 of 7. Frozen until the owner says.

**At seed 70's processing**: `sh tools/batch-check.sh` first, then apply both, the routine's chain after it.
