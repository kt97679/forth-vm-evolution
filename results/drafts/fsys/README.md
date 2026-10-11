# fsys - the file and memory words in Forth over SYSCALL (Iteration 202, in progress)

**Why.** s6 profiled on all eight workloads: 27 of the 68 primitives never
execute, 8 more under 0.01%. Seventeen of the 27 are the shell's words,
already in Forth over the one SYSCALL since Iteration 147 (forth/shell-sysc.4).
The rest are the file and memory words. Pointing their dispatch entries at
L_nosys - the handlers and their C helpers then dropped by GCC and the
linker - measured (corpus still right):

| design | engine | 9 never-run words out | and OPEN-, CLOSE-, WRITE-FILE |
|---|---|---|---|
| 0ceb043115, the smallest | 10,628 | 9,572 (-1,056) | 9,220 (-1,408) |
| d9247d19b0, the fastest | 22,616 | 21,240 (-1,376) | 20,760 (-1,856) |

**Done, and verified at test time.** file-sysc.4: READ-FILE, WRITE-LINE,
REPOSITION-FILE, FILE-POSITION, DELETE-FILE, FILE-SIZE, ALLOCATE, FREE, RESIZE
over SYSCALL, with the handlers' stack effects and results (READ-FILE's and
WRITE-LINE's -200, the positioning words' 200, DELETE-FILE's -errno, 201 and
202 with the block kept). Two things the handlers did that Forth needed: the
output flushed (every SYSCALL does) and a file's read-ahead dropped -
syscall-fdrop.patch: SYSCALL -4 calls t_fdrop (READ-LINE, native, reads
ahead; filetest mixes it with FILE-POSITION and REPOSITION-FILE). Loaded at
test time after coreext.4 (ans-extra.patch: ANS_EXTRA), shadowing the
primitives: filetest 96 tests, memorytest 198, 0 failed; s6 2,119 tests, the
suite whole; the smallest and the fastest as s6. A bug found on the way: a
size whose 16-byte header wraps (-1 ALLOCATE, -1 RESIZE) succeeded - now
fails, 201 and 202, as native (memorytest had silently skipped 28 tests).

**The kernel's own use.** Only SAVE-SYSTEM (forth/cv8-save.4) calls any of
them - ALLOCATE and FREE. So the gene's first form keeps those two native and
moves seven: the six file words and RESIZE.

**Next - the gene.** file-sysc.4 loaded at the end of every CV8 dump (after
every kernel word, so none refers to it); the converter drops its words
without --fsys, so a design without the gene stays byte for byte; with it,
FSYS in the engine points the seven dispatch entries at L_nosys. Then:
images byte-identical at fsys=0, alive and smaller at fsys=1, the standard
suite whole on fsys=1 designs, and the seven's exact saving.

## Built (Iteration 202) - results/pending/fsys-after-seed42.patch

The gene fsys: every dump variant has an -fsys twin with file-sysc.4 loaded
last (before the dump tool); FSYS points seven dispatch entries at L_nosys;
SYSCALL -4 under FSYS only; the library's helpers headerless (one
--headerless list with rtloop=2's). Two faults found on the way: the cell
system that makes the dumps has no NIP or TUCK (the load stopped after
READ-FILE - every other word stayed native, and the suite's file and memory
tests ended in the engine's exit 70); and a check of the kernel's own uses that
skipped every line with a stack comment (redone: none use the seven).

| design | fsys=0 | fsys=1: engine | image | total |
|---|---|---|---|---|
| 0ceb043115, the smallest | identical, engine and image | -608 | +504 | -104 |
| d99e3d9ed9, the knee | identical | -608 | +512 | -96 |
| d9247d19b0, the fastest | identical | -832 | +504 | -328 |

The standard suite on all three with fsys=1: 14 of 14 files as s6
(ans-check, ANS_SET=fsys=1). 7 of 7 hand-made stages identical; run-tests PASS.

Next, to make it pay more: the library is 504 bytes of image against 608 of
engine - shorter Forth (one read/write loop shared, the memory words only if
RESIZE moves) would widen the margin; OPEN-FILE, CLOSE-FILE and WRITE-FILE
(352 engine bytes more) wait on INCLUDED, which the kernel compiles against
OPEN-FILE and CLOSE-FILE.
