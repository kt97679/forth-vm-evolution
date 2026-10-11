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
