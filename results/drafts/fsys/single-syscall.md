# The single-SYSCALL family - the design agreed with the owner (Iteration 204)

The owner: OPEN-FILE and CLOSE-FILE can be built on SYSCALL; keep designs
with one SYSCALL and designs with the I/O primitives in the engine, so
nothing is lost - evolution compares; WRITE's buffer in Forth, on the heap,
not in the dictionary.

**The gene.** fsys 0: every I/O primitive native (as today). fsys 1: the six
file words and RESIZE (the after-seed-42 patch). fsys 2, to build: every I/O
word over SYSCALL - WRITE, READ, READ-LINE, OPEN-FILE, CLOSE-FILE, WRITE-FILE,
BYE, ALLOCATE, FREE too - the engine's OS interface SYSCALL alone.

**Rebinding.** What pinned handlers was the kernel's own compiled uses:
INCLUDED (OPEN-FILE, CLOSE-FILE, READ-LINE), SAVE-SYSTEM (ALLOCATE, FREE).
In an -fsys dump each such word is redefined in Forth after the kernel; the
converter then replaces every compiled use of the primitive (its opcode) with
a call to the redefinition, in every word - nothing refers to the handler,
which goes. The redefinitions use SYSCALL only, never the primitive.

**WRITE's buffer on the heap.** Allocated by SYSCALL (mmap) on first use; the
dictionary holds one cell, its address, and its fill. Flushed when full,
before any read of input (READ, READ-LINE and so KEY, ACCEPT, REFILL), before
a SYSCALL that leaves the process's hands (fork, exec, exit) and at BYE. READ-
LINE's read-ahead moves to Forth the same way, its buffer on the heap too, and
SYSCALL -4 (t_fdrop) retires with the native READ-LINE.

**Checks, as for fsys 1:** byte-identical at 0; the corpus and the whole
standard suite at 2; output and input interleaved exactly as before (the
corpus's ACCEPT, the tester's prompts); the engine's bytes saved and the
image's added, measured; then evolution weighs 0, 1 and 2 on the laptop.

## Stage A built (Iteration 205) - results/pending/fsys2-after-seed42.patch

fsys 2: OPEN-FILE, CLOSE-FILE, WRITE-FILE (forth/file-sysc2.4 - the open(2)
flags read from the engine's own table, so they cannot drift), ALLOCATE and
FREE in Forth; the kernel's compiled uses (INCLUDED, SAVE-SYSTEM) rebound by
the converter to the Forth words (--rebind); the engine's five handlers out,
and the C runtime's allocator with them.

| design | fsys 0 | fsys 1 | fsys 2: engine | image | total |
|---|---|---|---|---|---|
| 0ceb043115, the smallest | 18,146 | -104 | -1,312 | +684 | -628 |
| d99e3d9ed9, the knee | 18,362 | -96 | -1,344 | +700 | -644 |
| d9247d19b0, the fastest | 30,944 | -328 | -1,728 | +689 | -1,039 |

All nine through the evolver's full gate (the kernel workload includes its
sources through the rebound OPEN-FILE and CLOSE-FILE); the standard suite 14
of 14 as s6 at fsys 2 on two designs; 7 of 7 stages identical; run-tests PASS.

**Stage B, next:** WRITE with its buffer on the heap (the owner) - EMIT and
TYPE through it, flushed when full, before input is read, before a SYSCALL
that leaves the process and at BYE; READ and READ-LINE with a read-ahead on
the heap - READ-LINE is the kernel workload's, so its speed is measured
against the native; BYE. Then the engine's I/O is SYSCALL alone.

## Stage B built (Iteration 206) - results/pending/fsys3-after-seed42.patch

The owner: no output buffer; no read-ahead from stdin, pipes or anything that
cannot seek. fsys 3: WRITE one write(2) a call; READ the engine's t_read in
Forth (a seekable stdin a block and the rest given back, else a byte at a
time); READ-LINE into the caller's buffer, seeking back where it can, a byte at
a time where it cannot - no state between calls; BYE exit(2). One fault found:
TYPE is `WRITE ;`, the shape of a primitive stub, and read_ops returns stubs
before rebinding - TYPE called the dropped handler (the engine exits 70 at
L_nosys, silently: found by patching L_nosys to report its address, mapped to
TYPE). The converter now rebinds stub-shaped colon words too.

| design | fsys 2 total | fsys 3 total | speed 2 -> 3 | kernel | corpus | fib, bubble |
|---|---|---|---|---|---|---|
| the smallest | -628 | -1,217 | 1.527 -> 1.675 | 1.37 -> 1.88 | 1.51 -> 1.85 | unchanged |
| the knee | -644 | -1,193 | 1.040 -> 1.206 | 0.77 -> 1.27 | 0.52 -> 0.85 | unchanged |
| the fastest | -1,039 | -1,921 | 0.203 -> 0.258 | 0.35 -> 0.66 | 0.25 -> 0.47 | unchanged |

The standard suite 14 of 14 as s6 at fsys 3; the full gate on all three; 7 of
7 stages identical; run-tests PASS. Where the time goes: the corpus reads its
pipe a byte at a time as the native engine already did - its slowdown is the
unbuffered output, a write(2) for each TYPE and EMIT; the kernel workload pays
three system calls a line in READ-LINE against the native 4 KB read-ahead.
Within the owner's rules the one cheaper read is fewer calls a line (the
seek test remembered per file); the output's cost is the buffer's absence.

## The buffered level (Iteration 207) - results/pending/fsys4-after-seed42.patch

The owner: a buffered-output level beside the unbuffered one, with tests that
buffering breaks nothing; unsure how EMIT should be buffered. What is expected:
the standard leaves buffering open (FLUSH-FILE implies it is allowed); Gforth's
proposal and practice - no buffering of input, none of output to a terminal,
buffering of output to a pipe or file; it gave up terminal buffering after
users complained, and measured anywhere from no gain to a factor of 25 for a
filter (complang.tuwien.ac.at/forth/ansforth-cvs/buffering.html).

fsys 4: WRITE (so EMIT and TYPE) asks once whether stdout is a terminal - there
it writes at once; elsewhere into 4 KB on the heap, the dictionary holding its
[address, fill], registered with the engine (SYSCALL -5): t_flush, the native
engine's own flush, empties it at every native flush point - before each system
call, before a read blocks, at exits and faults (the return-stack fault's path
included). A full buffer: SYSCALL -6.

lab/evolve/outbuf-check.py, against native (fsys 0), unbuffered (3), buffered
(4), seed 40's smallest:
- T1, stdout and stderr on one pipe - ten programs (stderr between outputs,
  9,000 EMITs, a 6,000-byte TYPE, no final newline, the end of input without
  BYE, an ABORT", a file written between outputs, control characters, a
  return-stack fault): byte for byte as native at 3 and 4. One case differs as
  it should: 1 0 / kills every engine (SIGFPE) - native loses the 7 bytes its
  buffer held, 3 and 4 keep them.
- T2, a prompt before a blocking read: shown at 0, 3 and 4.
- T3, a terminal: 'A', then a computation with no system call, then 'B' -
  'A' at once at 3 and 4 (0.00 s, 'B' 0.8 s later); native holds it until the
  end (0.72 s with 'B') - its buffer never asked whether it was a terminal.
- The standard suite 14 of 14 as s6 at fsys 4; run-tests PASS; 7 of 7 stages.

Speed: fsys 4 about fsys 3 - the workloads print little; their I/O cost is
READ-LINE's: counted on the smallest, fsys 4 adds 3.5M dispatches to the corpus
(+10%), 1.9M of them FS-LF, the Forth loop that finds the line's end, and
three system calls a line. The next step for speed is there: SCAN (native
under kinput) for FS-LF, and the seek test remembered per file.

## READ-LINE faster (Iteration 208) - results/pending/readline-after-seed42.patch

Within the owner's rules (no read-ahead from what cannot seek): the line's end
found by SCAN - native under kinput, the kernel's loop otherwise - and whether
a file can seek asked once per descriptor (two cells of bits for 0-63;
OPEN-FILE and CLOSE-FILE, wrapped, forget a descriptor whose number is used
again): two system calls a line, not three. Speed against fsys 2 (VM, two
rounds): the fastest design (kinput) 27% slower -> 16%; the knee 16% -> 13%;
the smallest 7% -> 12% (within noise; without kinput its SCAN is a loop, the
dispatches unchanged: corpus 37.11M). ~150 bytes for the cache and wrappers.
outbuf-check.py PASS; the standard suite 14 of 14 at fsys 3 and 4 (filetest
opens, closes, reopens and repositions); run-tests PASS.

What would close the rest: read-ahead where the file can seek - the owner's
rule allows it there - a heap buffer a descriptor, given back by lseek(2)
before READ-FILE, the positioning words and CLOSE-FILE, as the native engine's
t_fgetc and t_fdrop do in C: one read(2) for many lines, as native.

## fsys 5 and a converter fault (Iteration 211) - results/pending/

fsys 5: READ-LINE reads ahead 4 KB where a file can seek (descriptors 1-63,
never stdin or a pipe), its state on the heap, and every other use of the
file first gives back what was read ahead (lseek), as native t_fgetc and
t_fdrop. Measured (VM, three rounds, noisy): against native, the fastest
design 7% behind (fsys 4: 17%), the smallest 2.4% (fsys 4: 3.7%); ~630 bytes
over fsys 4. Counted: more dispatches than fsys 4 (6.95M against 6.76M, the
kernel workload) - the bookkeeping in Forth - for far fewer system calls.

Two faults found on the way, by measuring rather than trusting the gate:
- file-sysc5.4 did not load: two remarks after stack comments were not in
  comments ("Undefined word read(fid,"), and the gate passed on fsys 3's
  READ-LINE, which the converter bound instead. Found because the profile
  showed fsys 3's FS-BACK and none of fsys 5's words.
- --rebind took the OLDEST redefinition: the dump lists words newest first.
  So since Iteration 207 fsys 4's buffered WRITE was never bound (fsys 4 ran
  as fsys 3; its tests passed testing unbuffered output) and INCLUDED used fsys
  2's OPEN-FILE and CLOSE-FILE. Now the newest, by address. Measured after:
  fsys 4 genuinely buffered - the fastest design's kernel workload at times
  near native's; outbuf-check.py now tests buffering for real: on a SIGFPE
  death fsys 4 and 5 lose what their buffer held, exactly as native, fsys 3
  keeps it; the prompt still shown before a blocking read; a terminal still
  shown at once. The standard suite 14 of 14 at fsys 4 and 5; run-tests PASS.

## fsys 5 tightened (Iteration 214) - results/pending/fsys5fast-after-seed43.patch

What fsys 5 paid for its fewer system calls was bookkeeping in Forth: the seek
test on every call, six variables set and read, the table indexed by
multiplication. Now a line whose LF is already in the buffer, within the
caller's room, is taken at once - one SCAN, one CMOVE, the entry's next moved
past the LF. No seek test there: an entry holding unread bytes belongs to a
file that seeks, because every open, close and other use empties it. The
entry is [next, end, buffer] as addresses (equal: nothing read ahead). The rest
- the buffer empty or the line running past its end, the room filled, the end
of the file, an error - goes the general way, with two variables (the entry,
the room's end) where there were six.

Counted - the profiler's per-address counts summed, system calls by strace -f
-c; the same build but for the level (dispatches):

| design | workload | fsys 4 | fsys 5, Iteration 211 | fsys 5 now | now against fsys 4 |
|---|---|---|---|---|---|
| be1620e346, seed 42's smallest (CMOVE an opcode, SCAN a loop) | kernel | 6,754,946 | 6,947,095 | 6,603,379 | -2.2% |
| | corpus | 36,862,315 | - | 36,727,255 | -0.4% |
| a0c7010722, small, without kinput | kernel | 6,737,806 | 6,927,803 | 6,584,073 | -2.3% |
| | corpus | 36,844,867 | 37,651,483 | 36,701,390 | -0.4% |
| 28677d13b1, seed 42's fastest (both opcodes) | kernel | 1,386,707 | 1,439,025 | 1,212,698 | -12.5% |
| | corpus | 4,975,165 | 5,116,693 | 4,494,762 | -9.7% |
| 9a3de58ebe, the best by Q of all runs (CMOVE the byte loop) | kernel | 1,506,883 | 2,447,468 | 2,182,678 | +44.8% |
| | corpus | 5,982,061 | 7,970,410 | 7,242,827 | +21.1% |

System calls as in Iteration 211: the kernel workload 4,441 at fsys 4 (2,189
reads, 2,137 seeks) against 135; the corpus 12,755 against 439. Images: fsys 5
now 33-53 bytes smaller than Iteration 211's (be1620e346 9,585 -> 9,552,
a0c7010722 9,512 -> 9,464, 9a3de58ebe 10,240 -> 10,202, 28677d13b1 10,486 ->
10,433), +576-598 over fsys 4; the engine as before. The counting harness
(lab/evolve/fsys-count.py, in the patch) first reproduced Iteration 211's
6,754,946 and 6,947,095 exactly; profiled after, the seek test ran 192
dispatches where it ran 40,700 - the new path takes the lines.

**The copy.** On 9a3de58ebe 90% of fsys 5's extra dispatches are CMOVE: the
lines copied out of the buffer by the kernel's byte loop, 11 operations a byte.
Its genome lists CMOVE among its format-10 words, but it realizes 14 of its 31
and CMOVE is not one of them. A copy a cell at a time (FS-MOVE: cells while 8
bytes are left, then CMOVE; 16 operations a cell) priced, NOT built - fsys 5
with it against fsys 5 now:

| design | kernel | corpus | image |
|---|---|---|---|
| be1620e346 (CMOVE an opcode) | +2.2% | +0.8% | +17 |
| 28677d13b1 (CMOVE an opcode) | +11.7% | +6.5% | +24 |
| 9a3de58ebe (CMOVE the loop) | -28.3% | -16.7% | +25 |

FS-MOVE costs every design the same 142,302 dispatches on the kernel workload
and 290,340 on the corpus; it pays only where CMOVE has no opcode, and
evolution can give CMOVE one (the format-10 list's order) - so it would need a
gene of its own, for a gain evolution can already reach. The owner's call.

**A native fault found on the way.** lab/evolve/readline-check.py (in the
patch) judges WRITE-LINE after a READ-LINE on a file opened R/W by the file's
bytes: fsys 3, 4 and 5 write at the file position (first, XX, ond line,
third); native writes after the 4 KB it read ahead (first, second line, third,
XX) - its WRITE-LINE handler never calls t_fdrop, as CLOSE-FILE, READ-FILE,
WRITE-FILE, REPOSITION-FILE, FILE-POSITION and FILE-SIZE do. Not fixed: an
engine change to every fsys 0 design, for the owner to decide (with the other
engine findings - PROGRESS.md, Iteration 213, open item 8).
