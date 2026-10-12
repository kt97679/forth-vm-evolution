# The after-seed-44 batch - apply in this order (against master after Iteration 224)

Seed 44 runs at Iteration 216's commit without these. Apply when it is processed:

| # | patch | what |
|---|---|---|
| 1 | writeline-after-seed44.patch | native WRITE-LINE gives back what READ-LINE read ahead before it writes, as WRITE-FILE and the positioning words do - after a READ-LINE on a file opened R/W it wrote past its 4 KB read (found by readline-check.py, Iteration 214); readline-check.py holds native to the right answer now (225) |
| 2 | fbufslots-after-seed44.patch | the native file buffers' slots: their state in one array, their buffers apart - the slot scan touched a page a slot (32 KB at 4 KB buffers); a design with full-size buffers touches 24-36 KB less on every workload, as little as 512-byte buffers did, without their extra reads (225) |
| 3 | fsysread-after-seed44.patch | fsys 3-5's READ asks whether stdin seeks as every file is asked (FS-SEEKS?), its own FS-SEEK0 gone: 40 image bytes fewer at fsys 3; readline-check.py reads the interpreter's input from a stdin that is a file - CR LF, backspace, delete, a long line, KEY, no final newline - against native (226) |

    for f in writeline fbufslots fsysread; do git apply results/pending/$f-after-seed44.patch || break; done

No kernel change: no reseed. The stages rebuild (engine/vm-lab.c changed);
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
