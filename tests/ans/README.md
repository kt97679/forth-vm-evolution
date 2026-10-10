# The Forth 2012 test suite (Iteration 124; first added in Iteration 118)

The test suite of the Forth 2012 standard - Gerry Jackson's, now kept by the
Forth Standard committee (UPSTREAM: the commit taken), around John Hayes's
core.fr. The files are copied unchanged: Hayes's core.fr and tester.fr "may be
distributed freely as long as this copyright notice remains"; Jackson's files
are in the public domain - "distributed and/or modified in any way", his notice
retained; prelimtest.fth, utilities.fth and runtests.fth carry no notice of
their own. Left out: fp/ and ttester.fs - there is no floating point here.
Until Iteration 124 this directory held the suite's 2007 snapshot (Jackson's
versions 0.1-0.3); these are 0.11-0.15, with prelimtest, coreplustest,
localstest, facilitytest, blocktest, utilities and errorreport new.

lab/evolve/ans-check.py runs it, each file in its own process. prelude.fth
gives the harness what the kernel lacks - FALSE .( NIP TUCK 2>R 2R> 2R@, in
core words, for tester.fr, utilities.fth, errorreport.fth and coreplustest's
helpers; not words under test. tools/ans-upper.py upper-cases the files for
this case-sensitive Forth, leaving strings, CHAR arguments, character literals,
comments and the text of utilities.fth's $" and $2" alone. An empty line
follows core.fr: its ACCEPT test reads the next line of input. runtests.fth is
the suite's own runner, kept for reference: it loads everything into one
process, which stops at the first word set the kernel lacks.

On hand-made s6 (the first table ans-check.py prints): prelimtest (23) and
memorytest (198) pass whole, core.fr's 638 tests pass; coreplustest stops at
:NONAME after 56 tests, 7 failed - +LOOP at the wrap-around boundaries;
filetest stops at /STRING after 16, 3 failed - FILE-POSITION's stack effect
and READ-LINE into a buffer of length 0; doubletest: double literals read as
singles; stringtest stops at S8 because S7's empty S" " swallowed the line that
defines it; the rest stop at the first word set the kernel lacks. Every stage
of the ladder says the same; the vendored RelF passes the +LOOP and file tests.
results/forth-standard-tests.md.
