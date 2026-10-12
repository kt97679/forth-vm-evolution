# The after-seed-45 batch - apply in this order (against master after Iteration 230)

Seed 45 runs at Iteration 230's commit without these. Apply when it is processed:

| # | patch | what |
|---|---|---|
| 1 | tty-after-seed45.patch | native output to a terminal unbuffered - the owner's standing rule (Gforth's), which native broke: the first WRITE asks isatty(1) (a small isatty in the libc-free runtimes, ioctl TCGETS), a terminal gets every WRITE at once; outbuf-check.py's terminal case now holds native to it (231) |
| 2 | divzero-spn-after-seed45.patch | the SPN engine (s8) throws -10 for a zero divisor too, as vm-lab.c since Iteration 229 - it read THROW's cell and still died of SIGFPE (231) |

    for f in tty divzero-spn; do git apply results/pending/$f-after-seed45.patch || break; done

No kernel change: no reseed. Images unchanged; engines with native output
change (three designs: fsys 3's add5ec8937 the same, d3149e10c6 and cc6d168e0a
+132 bytes - the same check through the generic syscall() measured +100 and
+68, a trim to make before applying if the bytes matter).

Tested together on master and both: outbuf-check PASS (native shows "A" at
once on a terminal, 0.00 s against "B" at 0.88 s); s8-full and s8-spncv8: -10
under CATCH, "Division by zero" uncaught; run-tests PASS (the s8 stages
included); 7 of 7 identical; every design of seed 44's front and the joint
front alive (161 of 161); the standard suite on two designs, 0 differ. Both
apply on a fresh clone and reproduce the tested files.
