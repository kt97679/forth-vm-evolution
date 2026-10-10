# The ANS Forth test suite (Iteration 118)

From the owner's Forth collection: Gerry Jackson's ANS test suite 0.3 (2007)
around John Hayes's core.fr (1995). Both may be distributed freely as long as
their copyright notices remain - they are in the files, unchanged.

This Forth is case-sensitive and the files are lowercase: tools/ans-upper.py
upper-cases them, leaving strings, CHAR arguments, character literals and
comments alone. prelude.fth defines what the kernel lacks for the harness to
load (TRUE, FALSE, .( ). core.fr's ACCEPT test reads the next input line, so
an empty line must follow `S" core.fr" INCLUDED` - without it the next file
never runs (results/forth-collection.md).

On hand-made s6 and the fastest design: coreplus (18 cases) and memorytest
(13) pass whole; the rest stop at the first word set the kernel lacks -
:NONAME (core extensions), D- (double), CATCH (exceptions), COMPARE
(strings), ONLY (search order), AHEAD (tools); and double literals (1.) are
read as singles. A held-out check for genetic improvement, and beyond the
gate's corpus: it found the stack-guard gene's silent exit on underflow.
