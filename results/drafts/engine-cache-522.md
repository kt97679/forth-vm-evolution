# An engine cache - priced, and not worth building (Iteration 522)

The owner asked while seed 73 runs. A design's evaluation is mostly its compiler and its measurement (here, one CPU:
seed 72's fastest c3a18bd60b - build 2.3 s, the compiler 2.05 s of it, measure 1.9 s, the run recorded 4.3 s; the small
6d463f3d0e - build 0.8 s, compiler 0.48 s, measure 5.6 s); the evolver compiles every engine afresh. Seed 72's 22,651
living designs had only 3,206 distinct engine sizes (bytes and text) - which suggested most engines repeat.

**They do not.** 300 consecutive designs from the middle of seed 72 (records 10,000-10,300), each built up to its
compiler call and keyed by everything the compiler reads - its command line (the design's folder abstracted) and every
.c and .h file there: **296 distinct**; a cache would hit 4 (1%). Two designs of the same engine size, diffed: other
flags (REGPIN and X_THREADFIND against GUARD, DSKEW, FBUFSZ, X_DUPNBR, ...), other fold, format-10 and superinstruction
tables - different engines that happen to weigh the same. Siblings differ in the engine as often as in the image.

**Not built.** A smaller idea, unmeasured: the JIT designs' stencils (spn-stencils.c) depend only on the JIT's own
flags, far fewer combinations than whole engines - compiled once per combination and linked, they would take part of
those 2 seconds; worth pricing only if the stencils are a large part of the compile.
