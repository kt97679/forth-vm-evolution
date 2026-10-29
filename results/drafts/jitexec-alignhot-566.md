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

**Open** (566; closed in 567 - the section at the end) (GOALS.md's stop needs none): the cause in jit.c's EXECUTE path under -falign-*=64 (a stencil, the inline
cache, or jit_interp's setjmp frame); ccflags() to take the expressed genome; then the minimal design into
lab/evolve/regressions.json - not before the fix, or run-tests fails and the laptop's chain stops at its tests.
Reproduce: rebuild either id from seed 80's db.jsonl, or the minimal genome above, and run sim16.fth's line.

## The cause and the fix (Iteration 567 - results/pending/, applied at seed 81's processing)

**jit.c's scan window.** jit_scan reads a stencil at most JIT_SCAN_MAX bytes from its start (160 since Iteration 312) and
copies it to its last exit - the last `jmp spn_next`/`spn_jump` inside that window. Under -falign-*=64 GCC pads inside
st_execute: its cache-miss path ends at byte 0x5b, its cache-hit path, behind a 64-aligned label, at 0xa4 - 164, past
the window. The copy ended at the first exit and kept the short `je` to the hit path (rel8: jit_leaves sees only rel32
branches), so the first EXECUTE whose site's cache held a native target jumped 0x25 bytes past the copy - into the next
stencil (SIGILL) or nowhere (segfault). Not the inline cache, not jit_interp's frame: the copy. sim16 was the first
workload whose EXECUTE targets are native; **jit-diff.fth's T2 shows it too** (its second loop alternates 1+, native,
with SQ, not) - the corpus does not, and engines-check never built the pair.

**How far** (results/drafts/stencil-window-567.py, 84 flag sets - x86-64 and i386, alignment 32 and 64, -O2/-O3/-Os,
the flag genes' sets, every JIT define): the longest stencil 146 bytes at 32-byte alignment, 242 at 64 (st_ummod, -Os);
at 160, 17 of 84 sets cut a stencil, all at 64 - st_execute in 16 (every x86-64 -O2 and -O3 set), st_callx in 4,
st_ummod in 1. stencil-check.py passed every one: it read to the last exit, not to the window.

**The fix** (jitscan-after-seed81.patch): JIT_SCAN_MAX 512 - at 512 none of the 84 is cut; no build without 64-byte
alignment copies a byte more (its stencils end by 146). stencil-check.py reads the window from jit.c and so fails a cut
stencil (STENCIL_WINDOW=160: the old); engines-check runs it at -falign-*=64 (x86-64 -O2; i386 -O2 -fno-crossjumping
-ftracer - both failed at 160), builds "the JIT with jitexec, aligned to 64", and runs jit-diff on every regression that
expresses the JIT. The minimal design is regression c578b55046 (lab/evolve/regressions.json). Built after the fix: the
minimal design, the variant and seed 52's two regressions - the corpus, jit-diff and sim16's line right at 8- and
4-byte cells.

**ccflags()** (ccflags-after-seed81.patch): the flags of the genes express() keeps - alignhot under align1, alignfn or
clang builds nothing, as its id says; so do alignfn, noinls, gotodup and alignhot on the families that do not express
them. Of the 1,481 records in seeds 76-80's results files, 9 build differently (seed 78 6, seed 79 3; each an unexpressed alignhot);
seed 80's two dead designs were two of its kind - with this patch alone they would build without the 64. The seed-52
regressions carried alignhot=2 unexpressed and were built with -falign-*=32; they now build as their ids say.
