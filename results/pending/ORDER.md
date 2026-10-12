# The after-seed-42 batch, in this order

Each made on a fresh copy of master (Iteration 198, the after-seed-41 batch
applied) with the ones before it, and verified to apply in order.

| # | patch | what |
|---|---|---|
| 1 | shortbranch-after-seed42.patch | short branches the tag-2 encoding finds out of range kept long on a second conversion - seed 41's 37 converter deaths alive, living designs byte-identical (199) |
| 2 | screen-after-seed42.patch | the surrogate screen: children predicted beaten by 30%/5% not measured, one in ten audited - pure Python (200) |
| 3 | fsys-after-seed42.patch | the gene fsys: six file words and RESIZE in Forth over SYSCALL, their handlers out of the engine; -fsys dumps - engine and forth: rebuild (202) |
| 4 | threads-after-seed42.patch | the gene threads: the dictionary in 16, 32, 64 or 128 chains - corpus -28% dispatches at 64 for ~240 bytes (204) |
| 5 | fsys2-after-seed42.patch | fsys 2, the single-SYSCALL family's stage A: OPEN-, CLOSE-, WRITE-FILE, ALLOCATE, FREE in Forth, the kernel's uses rebound - the smallest 628 bytes smaller (205) - engine: rebuild |
| 6 | fsys3-after-seed42.patch | fsys 3, stage B: WRITE (unbuffered), READ, READ-LINE (no read-ahead from what cannot seek), BYE in Forth - the smallest 1,217 bytes smaller, the I/O workloads slower (206) - engine: rebuild |
| 7 | fsys4-after-seed42.patch | fsys 4: fsys 3 with the output buffered off a terminal (Gforth's rule), flushed at the native engine's points; lab/evolve/outbuf-check.py (207) - engine: rebuild |

To apply, on a fresh clone of master:

    for f in shortbranch screen fsys threads fsys2 fsys3 fsys4; do git apply results/pending/$f-after-seed42.patch || break; done

Then the checks as for every batch (results/applied-after-seed41/ORDER.md): the
reseed only if forth/kernel.4 changed, the stage build, run-tests (bash),
--validate, the front designs alive, ans-check on the front.
