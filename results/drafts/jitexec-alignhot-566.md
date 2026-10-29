# Seed 80's two open deaths - the JIT's EXECUTE helper under 64-byte alignment (Iteration 566)

deaths-check on master (3d7ebe2): 2 of seed 80's records died for no expected cause - adc77c3487 (generation 45) and
2d4a69fc8d (generation 125), both "wrong output: apps", both JIT designs. Rebuilt here, each stops on apps at sim16's
`700 RUN` (fib(15) on the simulated CPU - s6 prints `610 18742`): adc77c3487 SIGILL, 2d4a69fc8d exit 70.

**The minimal design** (gene by gene, greedy, each step rebuilt and run on sim16): s6-cv8b with tag2=1, jit=1, jitx=1,
jitexec=1, alignhot=3 - "relf: segmentation fault" (not a stack guard), exit 70. Each alone is right: the same without
jitexec, or with alignhot 1 or 2, or with align1 or alignfn instead; jitmul, jitrp, jitimg, jitinl, jitloop and jittail
are not needed. sim16 is the trigger: STEP and O-ALU end in `@ EXECUTE ;` - EXECUTE of an EXECUTE through jit_exec;
the corpus and jit-diff.fth pass, which is why engines-check (the JIT variants without alignhot, alignhot without the
JIT) never built the pair.

**New with the lifted freezes**: alignhot was frozen at 0 until seed 77 (556); seeds 77-79 had no such death.

**A second fault the search found - alignhot built where it is not expressed**: both designs have align1=1 and
alignfn=1, so express() drops alignhot (its needs) - lifted.py's "n/e" - but ccflags() reads the raw genome, and the
engine is built with -falign-*=64 (appended after align1's =1 flags, so they win). A design's identity and its build
disagree; prediction 556 "as built" (564) read express(), not the build.

**Open** (GOALS.md's stop needs none): the cause in jit.c's EXECUTE path under -falign-*=64 (a stencil, the inline
cache, or jit_interp's setjmp frame); ccflags() to take the expressed genome; then the minimal design into
lab/evolve/regressions.json - not before the fix, or run-tests fails and the laptop's chain stops at its tests.
Reproduce: rebuild either id from seed 80's db.jsonl, or the minimal genome above, and run sim16.fth's line.
