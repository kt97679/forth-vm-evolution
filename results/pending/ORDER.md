# The after-seed-45 batch - apply in this order (against master after Iteration 230)

Seed 45 runs at Iteration 230's commit without these. Apply when it is processed:

| # | patch | what |
|---|---|---|
| 1 | tty-after-seed45.patch | native output to a terminal unbuffered - the owner's standing rule (Gforth's), which native broke: the first WRITE asks isatty(1) (a small isatty in the libc-free runtimes, ioctl TCGETS), a terminal gets every WRITE at once; outbuf-check.py's terminal case now holds native to it (231) |
| 2 | divzero-spn-after-seed45.patch | the SPN engine (s8) throws -10 for a zero divisor too, as vm-lab.c since Iteration 229 - it read THROW's cell and still died of SIGFPE (231) |
| 3 | names-after-seed45.patch | UTF-8 word names compile right: byte headers carry the count byte AFTER the name, right before the body, so >NAME's scan back for bit 7 stops at it at once - before, a name's own UTF-8 bytes stopped it, and one with bit 5 set read as a primitive (`: суп 5 . ;` ran, `: обед суп суп ;` printed nothing or crashed). The converter, both byte-header overlays (NEXT-NFA8, NAME>8, HEADER8, SEARCH-WORDLIST8, a new REVEAL8), the fast lookup, NAME>STRING, the engine's link readers and lookup opcodes and their gen-tos/gen-msc copies, the converter's THREAD-FIND body check (sod16.py), the tracer's naming (vmtrace.py), SPN's diagnostic; lab/evolve/names-check.py, new (232) |
| 4 | cellnames-after-seed45.patch | the same for the CELL headers - s0 (the build host), s1 SOD16, s2-s3 CPT16, s4-s5, the pack4/pack8 stages, s7: [link cell][zeros][name][count byte], the count byte last, right before the cell-aligned body. kernel.4 (HEADER, SEARCH-WORDLIST - a byte compare now, REVEAL, NAME> as 1+, PRIOR-NFA, NAME=? moved here from the byte overlays), cross.4's target headers, the dictionary dump, the converter's cell path, the SOD16 word table in both engines, sod16.4's own walk gone, the cell SPN translator, REVEAL8 dropped (the kernel's REVEAL does it). **Changes kernel.4: reseed after applying** (233) |

    for f in tty divzero-spn names cellnames; do git apply results/pending/$f-after-seed45.patch || break; done
    sh tools/reseed.sh        # patch 4 changes forth/kernel.4

Patch 4 changes the kernel: reseed after applying (tools/reseed.sh), then build. Images unchanged; engines with native output
change (three designs: fsys 3's add5ec8937 the same, d3149e10c6 and cc6d168e0a
+132 bytes - the same check through the generic syscall() measured +100 and
+68, a trim to make before applying if the bytes matter).

Tested together on master and both: outbuf-check PASS (native shows "A" at
once on a terminal, 0.00 s against "B" at 0.88 s); s8-full and s8-spncv8: -10
under CATCH, "Division by zero" uncaught; run-tests PASS (the s8 stages
included); 7 of 7 identical; every design of seed 44's front and the joint
front alive (161 of 161); the standard suite on two designs, 0 differ. Both
apply on a fresh clone and reproduce the tested files.

Patch 3, on master and patches 1-3: lab/evolve/names-check.py PASS - names
ending in bytes with bit 5 set (суп, café, voilà), a°b, CJK (名前), 31 ASCII
bytes, 15 Cyrillic letters, IMMEDIATE, a redefinition, ' with EXECUTE - on s6,
tag2 with and without kfast/klookup, the multi-state cache, tail calls, the JIT,
fsys 0, 2 and 3; on master the same six crash or print nothing. run-tests PASS
(the SPN stages and the tracer's self-test included); 7 of 7 identical;
outbuf-check and readline-check PASS; all 161 front designs alive; the standard
suite on six designs 14 of 14 each, 0 differ (TRAVERSE-WORDLIST, NAME>STRING).
Cost against patches 1-2: images +16 bytes (add5ec8937, d3149e10c6, dde890d478),
+56 on cc6d168e0a (kfast's THREAD-FIND), engines +0, +0, +32. The three apply in
order on a fresh clone and reproduce the tested files. **Not fixed: the cell
headers** - s0, s4, s5 and the CPT16 stages still carry the count byte before
the name, and the kernel's own COMPILE, asks >NAME: UTF-8 names fail there
(names-check.py --cell showed it) - patch 4 below fixes them (the owner
approved, Iteration 233).

Patch 4, on master and patches 1-4, reseeded (fixed point; the 4-byte kernel
identical from old and new seed): names-check.py PASS on every evolved design
given and on all 14 hand-made stages (s0-s8, p4, p8) - before it, every one of
them failed or crashed; run-tests PASS; 7 of 7 identical; outbuf-check and
readline-check PASS; all 161 front designs alive; the standard suite on six
designs 14 of 14 each, 0 differ. Two faults on the way: the kernel's walk first
named NEXT-NFA - the converter swapped cv8b.4's NEXT-NFA8 into it and
--drop-x8 dropped the name SPN looks up (s8 failed to build); renamed
PRIOR-NFA. And the dump tool's new LINKC kept the converter from dropping the
dump tool (+662 image bytes) until DUMPTOOL listed it. Cost against patches 1-3:
images +32 bytes (add5ec8937, d3149e10c6), 0 on cc6d168e0a; engines the same.
The four apply in order on a fresh clone and, reseeded, reproduce the tested
files, the seeds included.
