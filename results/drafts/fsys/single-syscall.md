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
