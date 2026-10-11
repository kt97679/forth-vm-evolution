# The tracer (Iteration 162)

The owner: a profiler in the engine, tracing execution - which paths run, and
why, with the stack as context.

## What it records

vm-lab.c built with -DPROFILE=2 (the evolver's PROFILING[0] = 2;
tools/vmtrace.py builds one for any design):

- **A shadow call stack.** Every call - tag2's, cv8's, the scaled and hot
  calls, the locals helpers, EXECUTE as an opcode - pushes a frame: its
  target, its return address, rp just after the push. A frame whose rp the
  live rp has passed has returned, so returns need no hook, and loop
  parameters or >R data on the return stack cannot confuse the path; RP!
  (QUIT) ends them all.
- **The first time each instruction runs** (a bitmap over the whole memory):
  its offset, the call path (the 24 innermost frames), the top three
  data-stack cells (a TOS engine's register first), and the input line being
  interpreted with >IN - SRC, #SRC and >IN at offsets asked of the design.
- **Dispatches per call path**, folded stacks at the end - flamegraph.pl or
  speedscope read them.

Measured engines are untouched: every hook expands to nothing without
PROFILE, and the 12 stage engines came out byte for byte the same.

## The tool

    tools/vmtrace.py [--design s6-cv8b|ID] [--word NAME]... [--folded FILE] [--uncovered] INPUT...

It builds the trace engine (the JIT off - native code is not traced - and tail
calls and msc off), runs each input, then again with an epilogue naming what
the input compiled: the design walks its own dictionary (NEXT-NFA8, NAME>8 -
byte headers) and names call targets with >NAME (any design). It reports
instructions run, words never entered, partly run words with the instructions
not run, and for --word each instruction's first context. --self-test runs in
run-tests.sh:

    SQ+0 (from TWICE+1) <- EXECUTE+0 (from INTERPRET+30) <- INTERPRET+0 (from QUIT+24)
      | stack 3 0 0, at >IN 8 of: 3 TWICE . CR

## Also fixed

The profiler's per-address tables were masked to 1 MB: code past it - the far
tests, the far benchmark - was counted at other addresses. Now over the whole
memory.

## First use: s6 under the suite's Forth files

1,550 of 2,113 instructions run (73.4%), 63 words never entered, 21 partly run
(inputs on stdin, as run-tests.sh gives them - INCLUDED never runs here):

- ?DO and (?DO): never on s6 - the extensions' loop test runs on s1, s3-s5.
- The cv8 overlay's compiler words under their own names - COMPILE,8,
  HEADER8, ;8, the control words: never, though s6 compiles all the time; its
  compiler runs under the kernel's names. They look like dead copies in the
  yardstick's image - to confirm.
- NUMBER?: the $ and # prefixes and the decimal point never run. Its first
  call: from INTERPRET <- QUIT, on "16" in "CREATE B 16 ALLOT" - the tests'
  numbers are plain decimals.
- The heaviest call path: INTERPRET;FIND;SEARCH-WORDLIST;NEXT-NFA8, 946,621
  dispatches (1,119 paths in all).

## Limits

- vm-lab.c only - stages s1-s6 and the whole front; relf.c, the pack and SPN
  engines have no tracer.
- In a trace build the JIT, tail calls and msc are off. EXECUTE through the
  Forth word (>R ;) is no call: what it runs shows in EXECUTE's frame, named
  by the dictionary walk.
- Run-time words are named by the walk only with byte headers; otherwise call
  targets alone, by >NAME.

## Second use (Iteration 163): s6 under the standard suite too

The standard suite IS run - not by run-tests.sh but by lab/evolve/ans-check.py,
each file in its own process, through prelude.fth (the harness words the
kernel lacks) and tools/ans-upper.py; an earlier note here and in coverage.md
said it never ran, from a probe that bypassed both. On s6: 991 tests, failing
only doubletest's double literals (read as singles); four files of fourteen
run to their end, the rest stop at the first word the kernel lacks -
coreplustest at :NONAME, coreexttest at 0<>, filetest at /STRING, stringtest
at -TRAILING, toolstest at AHEAD, exceptiontest at CATCH, facilitytest at
BEGIN-STRUCTURE, blocktest at BLOCK, and two at words the system has in files
the runner does not load: searchordertest at ONLY (extend.4), localstest at
{: (locals.4).

Traced with its inputs rebuilt as the runner builds them, and run-tests.sh's
Forth files: 1,610 of 2,113 instructions (76.2 percent, from 73.4), 59 words
never entered. ?DO, ABORT" and ABORT still never run: the files that test them
stop first - the missing words hide the tests of words that exist.

The cv8 compiler words never run under their own names on s6 are copies: the
converter's --cv8-compiler writes the overlay's code over the kernel's words
(COMPILE, and COMPILE,8 both 46 bytes, HEADER and HEADER8 both 166, at
different addresses; no address has two names) and leaves the originals in
the image. The overlay copies never run in s6: 26 words, 733 bytes of code (+ their headers); the dump tool: 6 words, 419 bytes; s6 image 10065 bytes. s5 is built the same way; the tag2 front runs the
overlay's words under their own names - nothing copied there.

## The genes the owner asked about (measured on seed 37's smallest, tag2)

Calls by offset, bytes per executed call: from the image base (today)
2.00-2.10 on the eight workloads, 3.00 on far; from the call site 2.00-2.99
(bubble 2.82, sieve 2.99 - their data sits between the code and the kernel),
2.00 on far; either, one tag bit choosing per call, 2.00-2.10 and 2.00 on far.

Stack shuffles (DUP SWAP OVER ROT DROP >R R> R@ ...), share of all dispatches:
loop 46, bubble 43, parse 32, corpus 31, sieve 30, kernel 29, ackermann 27,
fib 23 (percent) - DUP, SWAP, R>, OVER, >R and R@ the heaviest.
