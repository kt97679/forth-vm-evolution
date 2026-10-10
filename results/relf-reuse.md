# What RelF upstream gives back: its fixes and tests (Iteration 125)

The owner: check https://github.com/kt97679/relf - it has a lot of RelF fixes
and more tests - and reuse everything applicable; then proceed with the fixes.

## The fork point

This project's baseline kernel.4, extend.4, cross.4 and tests/core/tester.fr
are byte for byte RelF's at commit e8440ed (2026-09-07, RelF's Iteration 125)
- found by comparing the baseline's kernel.4 with every kernel.4 in RelF's
history (822 commits; e8440ed differs by 0 lines). So RelF's changes since are
the complete list of candidates: 63 commits touched kernel.4, most of them
RelF's own way - the shell, its CV8 format, opcodes, the native back end. The
vendored RelF (vendor/relf, 9934f3f, Iteration 602) is the reference every
fault below was checked against.

## The fixes taken - every one a fault on s6, right on RelF

| fault | on s6 before | where it was fixed | RelF |
|---|---|---|---|
| +LOOP exits early where index - limit overflows | 128 iterations of 256 (Haley's tests) | kernel.4 (+LOOP); tools/sod16.py's expected body; the opcode in vm-lab.c, gen-tos.py and gen-msc.py; SPN's st_ploop | Iteration 243, gforth's test |
| PARSE skipped leading delimiters, so S" " ." " ABORT" " and `( )` took the rest of the line | definitions after them lost; ABORT printed " ;" and a word | PARSE standard; the old body kept as PARSE-WORD for WORD and WORD8 (kinput's PARSE8 is PARSE-WORD8); S" ." ABORT" on 34 PARSE STRING,; cross.4's ." and ABORT" likewise; ABORT is WARM | Iteration 245 |
| FILE-POSITION, REPOSITION-FILE, FILE-SIZE in single cells | ( u ior ) where ANS has ( ud ior ) | all six engine sources | cv8.c |
| REPOSITION-FILE's ior was the new position | any position but 0 read as failure | the same handler | cv8.c |
| FILE-SIZE's ior was always 0 | - | the same | cv8.c |
| READ-LINE into a 0-length buffer said end of file | flag 0 | all six engine sources: zero characters are not EOF | Iteration 245 |
| CONVERT began at c-addr1 - 1 | "123" -> 0 | kernel.4 (`1+` for `-1 +`) | Iteration 554 |
| a name over 31 characters accepted, then never found | silent | the three header words (kernel.4, cv8b.4, cv8bt.4): "name too long" | Iteration 556 |
| IF and its kind interpreted wrote branches at HERE | **segfault** | ?COMP in the 15 compile-only words - in all five copies (kernel.4; sod16.4 and cpt16.4's X16; cv8.4 and cv8t.4's X8) and the four fusion overlays, 95 bodies | Iteration 552 |

**PARSE, more cheaply than RelF.** RelF made PARSE standard and put the skip
into WORD; here that would add ~15 dispatches to every token the interpreter
reads, and the fast designs' parse workload is all tokens. So the skipping
body is kept whole under the name PARSE-WORD - what WORD and klookup's WORD8
call, kinput's PARSE8 renamed PARSE-WORD8, its (PARSE) opcode and expected
body unchanged - and PARSE is the standard word, for the string words and
comments. hotinl's three sites in that path follow the body to its new name
(lab/evolve/hotsites-v1.json); `( → PARSE` stays.

**One source relied on the old PARSE**: shell.4 wrote a comment `( ) )` - text
")" - which the skip read as one comment and the standard reads as a comment
and a stray `)`. Now `\ )`. Found by the shell's image failing to build (six
DEFERs unset after the abort).

**Bootstrapped through tools/reseed.sh**: kernel.4 and cross.4 take effect only
through the seed images; the new 8-byte kernel compiles itself to itself
(25,640 bytes, was 25,144), the 4-byte one comes out the same from the old seed
and the new (14,180, was 13,904).

## The tests taken

- **tests/core/coreplus-loop.fth** - RelF's, unchanged: the four +LOOP
  sections of the standard suite's coreplustest.fth (public domain), in the
  `{ -> }` tester's syntax. On the old kernel exactly the seven failures.
- **tests/core/fixes.fth** - new: one test for each fix above that a tester
  case can hold (the empty strings, `( )`, PARSE, CONVERT, the file words).
- **tools/run-tests.sh** runs both on every stage, in one file with the
  sentinel at its end and a copy with one wrong case that must be caught, and
  the refusals on their own (a long name, IF outside a definition: refused,
  and the engine alive). Shown to fail: on Iteration 124's build all 14 stages
  fail both - 8 cases each, and the refusals end in a segfault (exit 139, or
  70 where SPN's handler catches it).
- **And a fault in run-tests.sh itself**: a stage missing where its cell width
  was built counted as SKIP, so a build that stopped half way passed - it did
  once in this iteration. Now FAIL; with s3 hidden the suite fails.

Not taken, and why: RelF's ext/ tests (coreext-std, memorytest, pooltest,
filetest2) need RelF's newer extend.4, which needs its newer kernel (WORDLISTS);
porting extend.4 would also change the kernel workload, which loads it - a
measurement change. ext/filetest.fth passes here as it is. The shell suites
(posix, mrsh, diff, interactive, ...) apply if the shell is part of the job -
an open question. RelF's other fixes are its own: the read-ahead (this project
did it its own way, Iteration 104), every wordlist relocated (one here), the
widening cross-compile (a 32-bit host building 8-byte images, not done here),
and the hashed word list - a fix this project gave RelF.

## What it costs

The 98 designs of Iteration 124's check (the 90 of the front of all runs and 8
with the new genes), rebuilt: none died, every one still says what s6 says on
all 14 files of the standard suite; images +120 to +160 bytes (median 140);
binaries mostly +64 or +96 (the file grows in 32-byte steps; a few smaller);
s6's engine +64. Dispatches, counted exactly on profiling builds:

| design | kernel | fib | parse | corpus | loop | sieve |
|---|---|---|---|---|---|---|
| s6 | +1.79% | 0 | +0.50% | +0.10% | 0 | 0 |
| e5193642ef (fastest) | +2.50% | +1.60% | 0 | +1.45% | +1.57% | +1.40% |
| 585376cf49 (smallest) | +1.84% | 0 | +0.67% | +0.18% | 0 | 0 |
| 19e2e26915 | +2.33% | +1.56% | 0 | +1.45% | +1.53% | +1.39% |

?COMP runs at compile time, so the cost falls where the workloads compile: the
kernel workload loads extend.4 and cross.4. The fast designs' fib, loop and
sieve are native - their few thousand dispatches are compile time too. On the
standard suite s6 now fails 4 tests, the double literals, where it failed 14.

Every image changes, so recorded image sizes no longer reproduce (ids do); the
next comparison session measures every front anew. Seed 37 ran on Iteration
123's code; it is already the first of a new count, so no streak is lost.
