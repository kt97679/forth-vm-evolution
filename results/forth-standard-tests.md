# The Forth 2012 test suite: what it reuses, what it found (Iteration 124)

The owner: can we reuse any tests from
https://github.com/Forth-Standard/forth-standard-test-suite? Yes - it is the
suite tests/ans held, eight years newer. Run here, it found five faults in this
project's kernel and engines that no check exercised; one of them, DELETE-FILE,
is fixed in this iteration. And building the harness found that tests/core/
tester.fr had been overwritten since Iteration 118.

## What the suite is, and what was taken

Gerry Jackson's test programs for Forth 2012 and ANS Forth, around John Hayes's
core.fr; since 2026 kept by the Forth Standard committee. Taken: commit 4c87e56
(2026-09-05; tests/ans/UPSTREAM) - every file of src/ but fp/ and ttester.fs
(no floating point here), byte for byte. The terms: Hayes's core.fr and
tester.fr "may be distributed freely as long as this copyright notice
remains"; Jackson's files are public domain, "distributed and/or modified in
any way", his notice retained; prelimtest.fth, utilities.fth and runtests.fth
carry no notice of their own.

tests/ans held the suite's 2007 snapshot: Jackson's versions 0.1-0.3, against
0.11-0.15 now, and seven files new - prelimtest (basic words before the tester
is trusted, reported by its own Pass/Error lines), coreplustest (replacing
coreplus), localstest, facilitytest, blocktest, utilities and errorreport.

## How it runs here

lab/evolve/ans-check.py, rewritten. Every file in its own process, as before -
one process for all of them (the suite's runtests.fth) stops at the first word
set the kernel lacks:

- **prelude.fth** gives the harness the seven words it needs and the kernel
  lacks - FALSE .( NIP TUCK 2>R 2R> 2R@, in core words. Not words under test:
  the kernel lacks 79 of the 116 standard words probed, so most optional word
  sets stop early, and that is not what this check is for.
- **A sentinel inside each file.** An abort inside INCLUDED returns to the
  next line of input, so a sentinel after the INCLUDED prints anyway.
- **Every test counted** (}T redefined after the tester), the tester's own
  #ERRORS read.
- **s6's own result first**, against the suite's expected values: a fault
  every stage shares is invisible to a comparison with s6, and every fault
  below is one.
- **A negative control**: s6 on core.fr with `T{ 1 2 + -> 4 }T` added must
  change its output and fail exactly one test more, or the check is BROKEN.
- **Exit status 1** when a design differs or the control fails (the old
  version always exited 0).

Building the harness took four faults out of it first, each worth knowing for
the next tool that drives this Forth: the old tester closes with `}`, not `}T`;
core.fr's ACCEPT test reads the next line of input (an empty line must follow,
or it swallows whatever comes next); a file included twice doubles its
failures; and core.fr leaves BASE in HEX, so a count printed after it reads
"27E" for 638.

## Coverage, on hand-made s6

Each file's own tests (core.fr's and the helpers' not counted again):

| file | old copy: tests, failed | standard: tests, failed | standard stops at |
|---|---|---|---|
| prelimtest.fth | - | 23, 0 | whole file |
| core.fr | 637, 0 | 638, 0 | whole file |
| coreplus(test).fth | 18, 0 | 56, 7 | :NONAME |
| coreexttest.fth | 2, 0 | 21, 0 | 0<> |
| doubletest.fth | 32, 8 | 5, 4 | #-12346789. (a prefixed literal) |
| filetest.fth | 8, 0 | 16, 3 | /STRING |
| memorytest.fth | 118, 0 | 198, 0 | whole file |
| stringtest.fth | 6, 0 | 6, 0 | S8 (see the empty strings below) |
| exceptiontest, toolstest, searchordertest | 0 | 0 | CATCH, AHEAD, ONLY |
| blocktest, facilitytest, localstest | - | 0 | BLOCK, BEGIN-STRUCTURE, {: |
| **total** | **821, 8** | **963, 14** | |

One loss: doubletest now opens with number prefixes (#, $, %), which the
kernel does not read, and stops before the D+ and DNEGATE tests the old one
reached - 32 tests to 5. It comes back when the kernel reads prefixed numbers.

## Five faults

All of this project's systems fail the same tests - s0 to s5 byte for byte
as s6; the SPN systems s7 and s8 with the same failures, their output not
identical (their images have FALSE and NIP, and s8 more core-extension
words, so its coreexttest runs further). The vendored RelF does not share
them.

| fault | where | found by |
|---|---|---|
| +LOOP exits early at the wrap-around boundaries | forth/kernel.4 `(+LOOP)`, and the opcode designs replace it with | coreplustest, Andrew Haley's 7 tests |
| FILE-POSITION leaves 2 cells: ( fileid -- u ior ), not ( ud ior ) | the engines' primitive | filetest, 2 tests |
| READ-LINE into a buffer of length 0 says end of file (flag 0) | the engines' primitive | filetest, Helmut Eller's test |
| an empty S" " or ." " swallows the rest of the line | forth/kernel.4: S" and ." parse with `34 WORD` | utilities.fth (`: S"" S" " ;`), stringtest (S7) |
| DELETE-FILE segfaults, always | every engine's handler | a reproduction's clean-up line (below) |

**+LOOP.** The kernel exits when the sign of index - limit flips: "exit if
(oldcount - lim < 0) xor (newcount - lim < 0)", SOD32's formula. The standard
exits when the index crosses the boundary between limit-1 and limit: the sign
flips *and* n points at the limit - (d xor (d+n)) < 0 and (d xor n) < 0 for
d = index - limit. They part where d + n overflows. Checked three ways - the
suite, a direct reproduction, a model of both rules - on Haley's eight cases
(counts of iterations; USTEP = 2^56, STEP = 2^56 on 64-bit cells):

| case: limit start step | the kernel's rule | s6 | the standard's rule | RelF | the suite expects |
|---|---|---|---|---|---|
| MAX-UINT 0 USTEP | 128 | 128 | 256 | 256 | 256 |
| 0 MAX-UINT -USTEP | 128 | 128 | 256 | 256 | 256 |
| MAX-INT MIN-INT STEP | 128 | 128 | 256 | 256 | 256 |
| MIN-INT MAX-INT -STEP | 128 | 128 | 256 | 256 | 256 |
| MAX-INT -MAX-INT MAX-INT | 1 | 1 | 2 | 2 | 2 |
| MIN-INT+1 1 MIN-INT | 1 | 1 | 2 | 2 | 2 |
| MAX-INT -1 MAX-INT | 2 | 2 | 2 | 2 | 2 |
| MIN-INT+1 -1 MIN-INT | 1 | 1 | 1 | 1 | 1 |

Upstream SOD32 fails the same 7; RelF, the owner's, passes them - its kernel
has the standard rule (its engine has no +LOOP opcode). Steps that large are
rare in programs; the gate corpus never takes one.

**FILE-POSITION and READ-LINE**, reproduced directly: s6's FILE-POSITION leaves
2 cells where RelF leaves 3; `BUF 0 fid READ-LINE` gives 0 0 0 on s6 (u2,
flag, ior - flag 0, as at the end of the file) and 0 -1 0 on RelF; both read
the line's next 3 characters correctly after it.

**The empty strings.** `: E1 S" " ;` on s6 and s0-cell: WORD skips leading
delimiters, so it skips the closing quote and takes the rest of the line - the
`;` with it - and the definitions after it are lost. RelF: length 0. This is
what stops stringtest at S8 (S7 is `S" "`) and what keeps utilities.fth's $"
from being defined on s6. ABORT" is defined beside them, probably alike; not
tested.

## DELETE-FILE - fixed

```c
L_delfile: { /* c-addr u --- ior */
    t = BYTE(DS1 + DS0);
    BYTE(DS1 + DS0) = 0;
    DS1 = (UNS64)unlink((char*)(uintptr_t)DS1);
    BYTE(DS1 + DS0) = t;          /* DS1 is unlink's result now */
```

The name's byte was restored at result + u: address 12 = 0xc for a failed
unlink of a 13-character name - the address the SPN engines' fault handler
reported. A segfault on every call, success or failure, in all 14 systems -
six copies of the handler (relf.c, pack4.c, pack8.c, vm-lab.c, spn.c,
spn-cv8.c), identical since the baseline commit 59ae3db; OPEN-FILE, just above
it, does the same three steps in the right order. RelF and upstream SOD32 do
not crash. No Forth source calls DELETE-FILE - not the shell - so only a
user's program met it; the suite never did either: filetest stops at /STRING
(and, given /STRING, at line 99, because of the empty strings) before its
DELETE-FILE test at line 174. The clean-up line of a reproduction found it.

Fixed: the result into a local, the byte back, then the result stored. Its
price, the 98 designs below built before and after on the VM: images
identical; binaries the same size on 76, 32 bytes larger on 22 (.text +0 to
+16 bytes - the file grows in 32-byte steps); hand-made s6's engine
unchanged (17,528 bytes, .text 14,861). tools/run-tests.sh checks it now on
every stage - a file made, deleted (ior 0), deleted again (ior not 0), a
clean exit; the binaries from before the fix fail it, 14 of 14 (11
segfaults, 3 stopped by SPN's fault handler), the fixed ones pass, 14 of 14.

## The evolved designs

The 90 designs of the front of all runs (session 31), and 8 with the genes
seed 37 is the first to choose - the fastest and smallest of seeds 32, 33, 35
and 36 with fbuf, kstack, abortif and opcall switched on: **every one says
what s6 says, on all 14 files**, before the fix and after it; no build
failed, no engine exited non-zero. Their (+LOOP) opcodes, where they have
them, behave as the kernel's colon word, Haley's boundaries included. The
record, ans-check.py itself on the 90: 0 of 90 differ, the control caught.

## Found on the way: tests/core/tester.fr overwritten since Iteration 118

The work directories the evolver makes are symlinks into build/work, and
build/work/tester.fr is a symlink to tests/core/tester.fr. ans-check.py copied
the suite's tester.fr into them - through the symlink - from its first run in
Iteration 118, and that commit recorded tests/core/tester.fr changed: 1,022
lines (Hayes's tester and the whole core test set, the corpus's own source)
became the 56-line ANS tester. Only run-tests.sh's locals check reads it, and
it passed either way; so from Iteration 118 to 123 that check ran locals.fth
after the tester alone, not after the core tests under locals.4's redefined
`;` and EXIT. The corpus and the gate never read it. Restored byte for byte
(blob 3359b38); ans-check.py now replaces what is in the work directory
instead of writing through it, and this iteration's runs left it unchanged.

## For the owner

- **The kernel faults** - +LOOP, the empty strings, FILE-POSITION, READ-LINE.
  Each fix changes every image or every engine: your call. +LOOP: RelF's rule
  is yours to port; the opcode follows the colon word. The empty strings:
  `34 PARSE` for S" and ." (and ABORT"). Once +LOOP is fixed, Haley's tests
  could join the gate - a measurement change, so alone.
- **The kernel's gaps** (the HANDOFF's thread on them), now named file by
  file: :NONAME and 0<> (core extensions), CATCH, AHEAD, ONLY, /STRING,
  BEGIN-STRUCTURE, {:, BLOCK, number prefixes and double literals.
