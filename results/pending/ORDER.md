# The after-seed-44 batch - apply in this order (against master after Iteration 224)

Seed 44 runs at Iteration 216's commit without these. Apply when it is processed:

| # | patch | what |
|---|---|---|
| 1 | writeline-after-seed44.patch | native WRITE-LINE gives back what READ-LINE read ahead before it writes, as WRITE-FILE and the positioning words do - after a READ-LINE on a file opened R/W it wrote past its 4 KB read (found by readline-check.py, Iteration 214); readline-check.py holds native to the right answer now (225) |
| 2 | fbufslots-after-seed44.patch | the native file buffers' slots: their state in one array, their buffers apart - the slot scan touched a page a slot (32 KB at 4 KB buffers); a design with full-size buffers touches 24-36 KB less on every workload, as little as 512-byte buffers did, without their extra reads (225) |
| 3 | fsysread-after-seed44.patch | fsys 3-5's READ asks whether stdin seeks as every file is asked (FS-SEEKS?), its own FS-SEEK0 gone: 40 image bytes fewer at fsys 3; readline-check.py reads the interpreter's input from a stdin that is a file - CR LF, backspace, delete, a long line, KEY, no final newline - against native (226) |
| 4 | stackheads-after-seed44.patch | the image loader's thread heads static, not a 32 KB local: gcc's default stack-clash protection probed every page of it at each start - 8 pages (32 KB) of every run's memory, every design, for the 16 to 128 heads an image has (228) |
| 5 | divzero-after-seed44.patch | a zero divisor is -10 THROW, not SIGFPE: the converter writes THROW's body into every CV8 image header (after the locals block), the engine's UM/MOD calls it with -10 (a macro, so the handler stays one line for gen-super/gen-tos), SAVE-SYSTEM and the SPN save write the cell, spn-cv8.c reads it; the kernel names an uncaught THROW - "Division by zero" for -10, "Error n" for other codes but -1 and -2. **Changes kernel.4: reseed after applying** (229) |

    for f in writeline fbufslots fsysread stackheads divzero; do git apply results/pending/$f-after-seed44.patch || break; done
    sh tools/reseed.sh        # patch 5 changes forth/kernel.4

Patch 5 changes the kernel: reseed after applying (tools/reseed.sh), then build. The stages rebuild (engine/vm-lab.c changed);
images are unchanged; engines change by a few bytes where a design has the
native WRITE-LINE or file buffers (three designs measured: the same sizes).
Memory changes - every front is measured again in the comparison's session.

Tested together (scratch tree, master and both): readline-check.py PASS on
d3149e10c6 and cc6d168e0a (fsys 3-5 as native, native's WRITE-LINE right);
run-tests PASS; 7 of 7 stages identical; outbuf-check.py PASS; the gate on every
seed 43 front design with native READ-LINE (fsys 0-2): 117 of 117 alive; the
standard suite on d3149e10c6 and cc6d168e0a: 0 differ from s6. Verified: both
apply in order on a fresh clone and reproduce the tested files.

Patch 3, tested on master and patches 1-3: readline-check.py PASS on add5ec8937
and d3149e10c6 (the new stdin case as native at fsys 3-5); shown to fail with
READ's seekable path not stopping at the first editing character (the
backspace and delete reached TYPE raw); outbuf-check.py PASS; run-tests PASS;
7 of 7 identical; the 48 seed 43 front designs with fsys 3 or 4, each at fsys
3, 4 and 5: 144 of 144 alive; the standard suite at fsys 3 on two designs, 0
differ. The three apply in order on a fresh clone and reproduce the tested
files.

Patch 4, on master and patches 1-4: memory by pages touched (cputime's
MINFLT), every selection workload, against master - seed 43's smallest
(add5ec8937, no native file buffers: this patch alone) -28 to -40 KB (fib 112
-> 80, kernel 172 -> 132); d3149e10c6 (full file buffers: patches 2 and 4) -52
to -60 KB (fib 144 -> 88, kernel 196 -> 144); seed 43's fastest (cc6d168e0a) -24
to -44 KB; the Q-best of all runs (fc09f6373d) -16 KB (bubble and ackermann
-4 and 0). run-tests PASS; 7 of 7 identical; all 165 of seed 43's front designs
alive; the standard suite on add5ec8937 and fc09f6373d, 0 differ; engines
+32, +32 and -32 bytes on three designs, images unchanged. The four apply in
order on a fresh clone and reproduce the tested files.

Patch 5, on master and patches 1-5 with the reseed: every division word under
CATCH gives -10 (/ MOD /MOD */ */MOD FM/MOD SM/REM UM/MOD), uncaught prints
"Division by zero" and the line's rest is dropped, ordinary division unchanged
- on designs with the multi-state cache (f20de05a64), tail calls (4a351e360a),
the JIT (cc6d168e0a), the plain cached top (add5ec8937, and at fsys 5), and the
stages s4, s5, s6; run-tests PASS (SAVE-SYSTEM included); 7 of 7 identical;
outbuf-check PASS (its THROW case no longer a signal death; a DIVZERO case, the
same at every level); readline-check PASS; all 165 of seed 43's front designs
alive; the standard suite 14 of 14 on three designs, 0 differ. Cost, three
designs against patches 1-4: engines +192, +96, +96 bytes; images +64 each
(THROW's message and the header cell) - more than the ~20 + ~30 estimated.
The five apply in order on a fresh clone and, reseeded, reproduce the tested
files, the seeds included. Not run: the SPN lab path (mk-spn-cv8-image.sh).
