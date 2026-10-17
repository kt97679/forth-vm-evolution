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

*Iteration 125: the four kernel faults below are fixed, as RelF had them, with
three more of RelF's - CONVERT, names over 31 characters, IF outside a
definition (a segfault) - and REPOSITION-FILE's ior; s6 now fails only the
double literals (results/relf-reuse.md).*

- **The kernel faults** - +LOOP, the empty strings, FILE-POSITION, READ-LINE.
  Each fix changes every image or every engine: your call. +LOOP: RelF's rule
  is yours to port; the opcode follows the colon word. The empty strings:
  `34 PARSE` for S" and ." (and ABORT"). Once +LOOP is fixed, Haley's tests
  could join the gate - a measurement change, so alone.
- **The kernel's gaps** (the HANDOFF's thread on them), now named file by
  file: :NONAME and 0<> (core extensions), CATCH, AHEAD, ONLY, /STRING,
  BEGIN-STRUCTURE, {:, BLOCK, number prefixes and double literals.

## The extensions under test (Iteration 165)

The owner: add the standard words the suite needs, as an extension.
forth/coreext.4 - 0<> /STRING -TRAILING AHEAD :NONAME ERASE BLANK WITHIN
PARSE-NAME BUFFER: CASE OF ENDOF ENDCASE .R U.R, portable Forth - and the
system's own extend.4 (the search order) load before each file
(ans-check.py). On s6, tests run before -> after, and where each file stops:

| file | before | after | stopped at |
|---|---|---|---|
| coreplustest | 56 | 70 | #-1289 (NUMBER? reads a sign before a prefix, not after) |
| coreexttest | 21 | 183 | UNUSED |
| filetest | 16 | 47 | FLUSH-FILE |
| stringtest | 10 | 18 | SEARCH |
| searchordertest | 0 | 10 | GET-CURRENT |
| toolstest | 0 | 2 | [IF] |

991 tests -> 1,194, no new failure (doubletest's four double literals remain).
Next: UNUSED, FLUSH-FILE, [IF] [ELSE] [THEN], GET-CURRENT SET-CURRENT, SEARCH,
CATCH THROW, the structures, NUMBER?'s "#-", double literals; BLOCK and the
standard's {: are larger.

## Waves two and three, and the kernel's numbers (Iteration 167)

forth/coreext.4 grew: FALSE NIP TUCK 2>R 2R> 2R@ UNUSED FLUSH-FILE GET-CURRENT
SET-CURRENT [IF] [ELSE] [THEN] SEARCH CATCH THROW, the structures
(BEGIN-STRUCTURE END-STRUCTURE +FIELD FIELD: CFIELD:), seventeen double words,
AGAIN, and COMPARE as the standard has it (-1, 0, 1; extend.4's gives
differences and is the kernel workload's, so it stays). The runner loads
extend.4 first. The kernel's NUMBER? takes the standard's sign after a prefix
(#-1289), % for binary and 'c' for a character; INTERPRET keeps a double
literal's two cells (no source of ours wrote a number with a point). Every
design pays ~104 bytes of image for the numbers (s6 8,761 -> 8,865) - the
owner: respect the standard, tolerate the size. results/pending/numbers-after-
seed39.patch, the batch's fourteenth; coreext's, regenerated.

On s6: 1,599 tests (991 before the extension), 6 failed - all filetest's, one
bug: CREATE-FILE could not make a file to read and write.

## Waves four to six (Iteration 170) - results/applied-after-seed40/coreext-after-seed40.patch

coreext.4: CS-PICK CS-ROLL SLITERAL M*/ RESIZE-FILE MARKER, FORTH-WORDLIST and
SET-ORDER in the root wordlist (ONLY's minimum order must hold them), VALUE
2VALUE TO [DEFINED] [UNDEFINED] RENAME-FILE C" ORDER N>R NR> UNESCAPE
FILE-STATUS. Found on the way: extend.4's SET-ORDER with 0 ran its loop from -1
down through memory (searchordertest crashed); M*/ must floor, as this
system's / does (doubletest's ?FLOORED); .( is missing; RECURSE in :NONAME
called LAST's word - its fix crashes under the runner only, held back
(results/drafts/recurse-noname.md). SLITERAL and C" keep their strings on the
heap, not inline in code.

On s6: 1,817 tests, 4 failed (RECURSE in :NONAME). Whole files now:
doubletest (247) and searchordertest (41), with prelimtest, core, coreplus,
facility, memory. Stopping: coreexttest at SAVE-INPUT, filetest at REQUIRED,
toolstest at SYNONYM, stringtest at SUBSTITUTE, exceptiontest at ABORT (the
kernel's abort does not THROW), localstest at {:, blocktest at BLOCK.

**Not ready - a draft, not the batch's.** The held-out check over seed 39's
186 front designs with these waves: all 186 differ from s6 somewhere -
searchordertest on every one, coreexttest on some (before the waves: 0 of 186,
searchordertest stopping at its seventh line on all alike). Either the waves'
search-order words assume s6's wordlists, or the deeper tests reach a real
difference in the designs' - next: one design's searchordertest output beside
s6's. results/drafts/coreext-after-seed40-draft.patch, the check's table
beside it (-front-check.txt).

## Iteration 171: ready - and the kernel's exceptions

**Why all 186 differed:** the runner compares each design's whole output with
s6's, and ORDER printed wordlist ids - addresses, different on every design;
it prints names now (the standard leaves ORDER's format to the system). And
:NONAME's xt was HERE alone: a tag-2 design's COMPILE, tells a colon xt by
what its own : writes, so coreexttest's COMPILE, test failed on every one.
:NONAME is now the design's own : under a fresh name, (NONAMEn) - which also
mends RECURSE in :NONAME (LAST is the definition) and retires the held-back
fix. Its first form failed ;'s depth check (: took the depth before the xt).
With these: s6 1,817 tests, 0 failed; seed 39's 186 front designs, 0 differ -
results/applied-after-seed40/coreext-after-seed40.patch (the check's table beside it).

**The exception wordset in the kernel** - results/pending/exceptions-after-
seed40.patch, after the coreext patch: HANDLER, CATCH and THROW (the
standard's reference design, and the frame keeps the input source - THROW
restores the one CATCH began with, which exceptiontest's -13 in three nested
EVALUATEs needs); ABORT is -1 THROW, ABORT" -2 THROW (its message only when
nothing catches it), an undefined word -13 THROW under a CATCH; QUIT clears
HANDLER; extend.4's preliminary THROW out. With no CATCH every message is as
before. exceptiontest whole; s6 1,821 tests, 0 failed; reseeded (the 8-byte
kernel 26,904 bytes), run-tests, 7 of 7 IDENTICAL, the jail; 186 alive and 0
of 186 differ from s6.

## The seventh wave (Iteration 181) - results/applied-after-seed41/coreext-w7-after-seed41.patch

SYNONYM (immediacy carried), INCLUDE REQUIRED REQUIRE (INCLUDED wrapped to note
each file it loads), SAVE-INPUT RESTORE-INPUT (the same source; otherwise true,
as the standard allows), and PARSE-NAME rewritten to return its name inside the
input buffer. Two faults of the conversion, not of the system, in
tools/ans-upper.py: a file name after INCLUDE or REQUIRE was upper-cased (no
such file - filetest stopped at "Can't open include file"), and so was
PARSE-NAME's token, compared there with a lower-case S" string (two "failures"
in coreexttest - first taken, wrongly, for PARSE-NAME's fault). Both now keep
their case, like CHAR's. On s6: 1,862 tests, 0 failed. Stopping at: DEFER
(coreexttest), S\" (filetest), TRAVERSE-WORDLIST (toolstest), SUBSTITUTE
(stringtest), BLOCK, {:.

## The eighth wave (Iteration 182) - results/applied-after-seed41/coreext-w8-after-seed41.patch

DEFER DEFER@ DEFER! IS ACTION-OF; S\" with the standard's escapes; REPLACES
and SUBSTITUTE; HOLDS; and S" interpreted into two transient buffers in turn,
as the file word set asks (11.6.1.2165) - its test reads two strings at once.
A fault of mine on the way: CHAR-AT kept its character with >R and read it
with R@ inside a ?DO loop, where R@ is the loop's own - 23 of stringtest's
tests wrong, until the character stayed on the data stack. On s6: 1,988
tests, 1 failed - RESTORE-INPUT across lines of a file, which the standard
lets fail and the test expects to work (a file's read-ahead buffer makes the
position unreliable: left). Whole files now nine of fourteen, stringtest
among them. Stopping at: X32X32 (coreexttest's own word - something before it),
SI_INC (filetest, after that RESTORE-INPUT), TRAVERSE-WORDLIST (walks headers,
whose layout differs by design - held back), BLOCK, {:.

## coreexttest whole (Iteration 183) - results/applied-after-seed41/ansupper-sq-after-seed41.patch

Its stop at "X32X32" was a word made of string text: line 767 nests an escaped
string in an escaped string, and tools/ans-upper.py ended an S\" string at its
first quote - an escaped one - and upper-cased the rest, \x32 into \X32, no
escape at all. The conversion now steps over an escaped character inside S\".
coreexttest: 383 tests, 0 failed, the whole file. On s6: 1,989 tests, 1 failed
(RESTORE-INPUT across a file's lines, left as before); ten of fourteen files
whole. Held out with the ten pending patches: 0 of seed 40's 218 front designs
differ from s6.

## Blocks and TRAVERSE-WORDLIST (Iteration 186) - results/applied-after-seed41/coreext-w9-after-seed41.patch

The block word set over blocks.fb in the working directory (1024 bytes a
block, opened R/W or created - CREATE-FILE R/W since Iteration 168): two
buffers, a new block taking the one not current and writing it back first if
updated (blocktest asks for two at once); BLOCK BUFFER UPDATE SAVE-BUFFERS
EMPTY-BUFFERS FLUSH LOAD THRU LIST, BLK and SCR, and \ in a block skipping to
its 64-character line's end. blocktest: 65 tests, 0 failed, whole - REFILL
past a block's end and a nested LOAD's eviction were the expected gaps; its
tests did not reach them.

TRAVERSE-WORDLIST, NAME>STRING, NAME>INTERPRET, NAME>COMPILE: a name token is
the nfa, and NEXT-NFA8 - the byte headers' own link walk, findable in s6 and
the evolved designs, lean ones too - gives the one before it; the walk's state
in variables, since the word called may reach below its nt. Guarded by
[DEFINED] NEXT-NFA8. toolstest: 63 tests, 0 failed, whole.

On s6: 2,068 tests, 1 failed (RESTORE-INPUT across a file's lines). Whole
files: twelve of fourteen - left filetest (that test, then SI_INC after it)
and localstest ({:, locals).

## RESTORE-INPUT across a file's lines; filetest whole (Iteration 192) - results/applied-after-seed41/coreext-w10-after-seed41.patch

filetest's stop at SI_INC was the harness, not the system: SI_INC, SI1 and S$
are coreexttest's, and upstream's runtests.fth includes coreexttest first in
the same session, where ans-check.py gives every file its own. The three are
defined before filetest now, as coreexttest has them.

Then the system: RESTORE-INPUT refused a file's earlier line (the one failure
since Iteration 181). SAVE-INPUT on a file now also records where the current
line starts - the position READ-LINE left, less the line and its end: an LF, a
CR LF or none (the last line, or one longer than the buffer), each tried by
reading the line again and comparing, the position put back. RESTORE-INPUT
repositions there, reads the line again, and restores >IN. In coreext.4 - no
kernel change, no image changes.

filetest: 96 tests, 0 failed, whole - the nested SAVE-INPUT, REFILL, EVALUATE
and RESTORE-INPUT of a file included. On s6: 2,069 tests, 0 failed; thirteen
of fourteen files whole - left localstest ({:, locals: the kernel's name lookup
needs a hook - the owner's decision). Held out: 0 of 12 of seed 40's front
designs (one in eighteen) differ from s6, 14 of 14 files each.

## Locals; the suite whole (Iteration 194) - results/applied-after-seed41/coreext-w11-after-seed41.patch

The locals word set in coreext.4, with no kernel change (results/drafts/
locals-plan.md): the kernel's FIND walks the search order, so the names of the
definition being compiled live in a wordlist of their own, first in the order
while it compiles; each name is an immediate word made in a scratch area
(HERE, LAST and CURRENT saved and restored - the definition's code
uninterrupted, RECURSE still finding it), compiling its index and (L@). The
values live on a stack of their own: DO loops keep the return stack as they
find it, and a local named I or J is the local (localstest's LT29). {: with |
and --, (LOCAL) (the first declared from the top, as LOCALS| has it - {: the
last), TO a local first, ; and DOES> ending the scope (the frame dropped, the
names gone), EXIT immediate while locals are active, ENVIRONMENT? answering
#LOCALS (64). And .S - localstest's last line; the system had none.

localstest: 50 tests, 0 failed, whole - local names over global names and
numbers (DUP, BEAD in HEX), :NONAME and DOES>, recursion, 16 locals, (LOCAL),
and over wordlists pushed after them. On s6: **2,119 tests, 0 failed; all
fourteen files whole.** Held out: 0 of 12 of seed 40's front designs (one in
eighteen) differ from s6, 14 of 14 files each.

Not covered by the suite, left as they are: a THROW out of a definition with
locals leaves their frame on the locals stack (CATCH restores the data and
return stacks, not this one), and a definition abandoned mid-compilation by an
error leaves its names in the search order until the next ; - both harmless to
the tests, and the standard leaves the first unspecified.
