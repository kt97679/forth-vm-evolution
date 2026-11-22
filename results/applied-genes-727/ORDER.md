# The reopened search's first genes - applied at Iteration 727 (results/queued-genes until then)

**Applied at Iteration 727** (the owner: the design evolution finalized before relf's handoff): batch-check PASS on
537f3cc2 (4 patches; run-tests, validate 7 of 7, the jail), `git apply` of the four in this order on master, the stages
rebuilt, and the ten roles' lab build unchanged - pack-designs.py on results/relf-designs-718.md 20 of 20 builds 9 of 9
right, its 40 engine and image checksums results/drafts/designs-sha256-718.txt's.

As it stood before:

# The reopened search's genes - after the new roles ship, before the next series (Iteration 710)

The owner (708): the search reopens after the roles, chainorder and mechanism 9's V1' built as genes first. Made on
top of the after-seed-96 batch, so applied after it: that batch went in at chain A's processing (Iteration 713,
results/applied-after-seed96); this queue after the roles ship (designs/, the package), before the reopened search's
first seed. Check it on master as it stands: `env PENDING=results/applied-genes-727 RECORD=1 sh tools/batch-check.sh` (no
BASE since 713). Then, from the repository's top:

    git apply results/applied-genes-727/jitdead-after-seed96.patch
    git apply results/applied-genes-727/fixenv-after-seed96.patch
    git apply results/applied-genes-727/jitfew-after-seed96.patch
    git apply results/applied-genes-727/jitdead-cross-after-seed96.patch

**Rebased at Iteration 723** (713's three no longer applied to master: export-genes.py had moved, 714-722): made again
on 723's master one commit each - one conflict, G-NOT-YET's line (722 had emptied it; jitdead's --jit-dead kept
there), the rest context; fixenv and jitfew unchanged but their offsets. **jitdead-cross-after-seed96.patch** (new,
last; forth/cross-cv8.4, lab/evolve/export-genes.py): jitdead in the cross compiler - the header the JIT's code
alone, the body padded to four bytes (JD-PAD,), jit_wends' ends before the pad and, without --jitx, the headed words'
rows alone, the header length 1 in the image's table, JITN's code read from the map and written (JITN_CODE);
G-JITDEAD and G-JITX in the genes, read by name so a genes.4 without them still builds (make selfhost: 20 of 20 on
the ten shipped designs' genes); --jit-dead out of G-NOT-YET. Tested: results/drafts/jitdead-cross-723.sh (on the
queue applied) - four JIT records with jitdead, PASS at both widths (results/drafts/jitdead-cross-723.md).

batch-check (724, on af0ef242 - 4 patches): PASS - run-tests PASS (the generators: 118 paths), validate 7 of 7
IDENTICAL, the jail PASS.

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

**jitfew-after-seed96.patch** (engine/jit.c, lab/evolve/GENES.md, lab/evolve/engines-check.py, lab/evolve/evolve.py;
Iteration 713, from the early computers' working sets - results/drafts/early-computers-713.md) - the gene jitfew, 0/1,
with the JIT: jit_body's arrays (at, arg, nat, opl, tl) 128 operations long in its own frame, and 1,024 long
(jit_body_big, cold) only for a word with more operations - its decoding answers JIT_ROOM before anything is emitted or a
callee translated, and the word is translated again from its start. Off, the engine is as before (the old declarations
under #else). Why: the arrays' heads were a page each at every depth of the callees' translation (a 23,752-byte frame,
up to 16 deep) - 10-19 of a JIT design's pages on a workload. Tested on top of jitdead and fixenv (results/drafts/
jitfew-test-713.py, five interleaved rounds): eight JIT designs - memory -5 to -16 pages (-11 to -23 %), apps -7 to -27,
the engine +224 to +544 bytes, the outputs alike on every workload, the time within the rounds' noise; engines-check.py
gains three variants (jitfew; without jitx; with jitdead, jitexec, jitmul, jitcfa).
