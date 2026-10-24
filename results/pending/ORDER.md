# The after-seed-70 batch - applied at seed 70's processing (Iteration 488)

Prepared while seed 70 runs; master stays what seed 70's bundle tests. One patch:

    git apply results/pending/jit-abortq-maxops-after-seed70.patch

**jit-abortq-maxops-after-seed70.patch** (engine/jit.c, engine/spn-stencils.c, engine/vm-lab.c, tools/layout.py):

1. **(ABORT") native** (jitexec with jitmul): the decoder reads a call of (ABORT") (the converter's JIT_W_AQ) as one
   operation, its inline message skipped; the stencil drops a false flag and goes on, and on a true one calls
   jit_resume0 through a new hole (SPN_RS_VALUE), which longjmps to jit_call's return point with the call's own address -
   the interpreter resumes there and runs (ABORT") itself, which never returns (-2 THROW, or the message and ABORT). The
   inline message was decoded as code before (fcp's STR>MV, ?PROMOTEMV, cd16sim's LINE: - "Malformed...", "Illegal..."),
   refusing those words and their callers.
2. **JIT_MAXOPS 256 to 1024**: alone it moved nothing (488) - the long words then failed on other causes - so it rides
   with the rest.

Tested here (488), on master e5c6239's successor with the patch in the working tree: a false flag in a hot loop, a true
one caught by CATCH (-2, depth restored), one uncaught (the message, ABORT) - s6 with the JIT and all four genes, and
seed 68's fast design with and without them, against the interpreter, line for line; the corpus. jitapps.py on the fast
design: brainless's leftover 5.8% to 4.3%, cd16sim's 18.1% to 17.7%, fcp's unchanged 17.5% - what still blocks fcp and
cd16sim is return-address words (2>R, 2R>, (TO)), DOES> code run by interpreted callers, and nested JIT headers.

**At seed 70's processing**: `sh tools/batch-check.sh` first, then apply, the routine's chain after it.
