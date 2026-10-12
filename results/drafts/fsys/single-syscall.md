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
