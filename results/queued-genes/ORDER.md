# The reopened search's genes - after the new roles ship, before the next series (Iteration 710)

The owner (708): the search reopens after the roles, chainorder and mechanism 9's V1' built as genes first. Made on
top of the after-seed-96 batch, so applied after it: that batch went in at chain A's processing (Iteration 713,
results/applied-after-seed96); this queue after the roles ship (designs/, the package), before the reopened search's
first seed. Check it on master as it stands: `env PENDING=results/queued-genes RECORD=1 sh tools/batch-check.sh` (no
BASE since 713). Then, from the repository's top:

    git apply results/queued-genes/jitdead-after-seed96.patch
    git apply results/queued-genes/fixenv-after-seed96.patch

batch-check (713, on ec09a65 - 2 patches): PASS - run-tests PASS (the generators: 113 paths), validate 7 of 7 IDENTICAL,
the jail PASS.

**jitdead-after-seed96.patch** (engine/jit.c, engine/vm-lab.c, forth/cv8t-jitd.4, lab/evolve/GENES.md,
lab/evolve/engines-check.py, lab/evolve/evolve.py, lab/evolve/export-genes.py, tools/layout.py, tools/sod16.py) - the
gene jitdead, mechanism 9's V1' (results/drafts/triz-706.md): the JIT's header [JIT] alone, not [JIT][four bytes]. The
translator finds the body's end by the converter's rule (an image word's, --jitimg, from jit_wends); translated, the
trigger becomes JITN - a code of its own, pinned, the same handler (vm-lab.c) - and the body's first four bytes the
native offset, what native code reads there at run time (inline strings, (ABORT")'s resume point) copied first; left
bytecode, the trigger a NOOP. Bodies padded with NOOPs to four bytes (forth/cv8t-jitd.4's `;8`, the converter's
jitimg words). A late gene, 0/1, with the JIT; a dump of its own (-jitd); engines-check.py's four variants. Not yet in
the self-hosting compiler: export-genes.py puts --jit-dead in G-NOT-YET, so cross-cv8.4 refuses such a design. Why: the
header was 875 of the five programs' code bytes on every JIT design (706's price, -700). Tested (results/drafts/
jitdead-710.md): ten JIT designs, the gene off and on, at both widths - the five programs' code -693 to -741 bytes, the
image -24 to -80, the engine -592 to +640, the total -0.3 to -2.9 %; all 40 builds alive, fib and apps as s6;
fuzz-designs.py 800 runs, 0 differ; instructions (callgrind) the same or fewer on every workload of four designs (up to
-5.9 % on the corpus).

**fixenv-after-seed96.patch** (lab/evolve/evolve.py; Iteration 713 - the owner: "if you think it will help us find
better designs - let's do it") - every engine run with one environment: PATH=/usr/bin:/bin, cputime's CPUTIME_JAIL,
and EVOLVE_PAD filling the environment's and the arguments' strings (the exec's file name counted) to 1,024 bytes of
the initial stack (evolve.run_env, called by sh() for an engine or cputime; EVOLVE_KEEP_ENV=1 keeps the caller's). Why
(results/drafts/early-games-713.md): memory is the pages a run faults, the stack's among them, and the measuring
process's environment and paths moved it between machines and sessions - the sandbox's 17 KB environment +3 pages; the
environment's size biases timings too (Mytkowicz et al., ASPLOS 2009 - with ASLR on, as the search runs, noise). With
the reopened search's series so its runs compare with each other, not with the earlier series' records (about a page
apart on the laptop). Tested (results/drafts/fixenv-713.md): fb0d57c8a2 medians of 15 - start-up 15 pages and the
kernel workload 27 with the parent's environment as it is or 20 KB larger (before: 19 and 31, 24 and 36); the outputs
alike; 27 the laptop's record. All of the search's measuring goes through sh() (measure-ids.py, loadtest.py, xcheck.py:
E.measure); lucky.py and run-spread.py, studies of the run's spread, keep their own.
