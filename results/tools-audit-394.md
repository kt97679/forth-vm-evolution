# The tools audited after the context-economy changes (Iterations 394-395)

The owner asked for a deep audit: does shorter output break anything? Every code change since this chat began
(Iteration 383: compare-fronts.py, evolve.py, heldout.py, next-run.sh, handoff-check.py, and the new
review-checks.py, supers-knockout.py, batch-check.sh; and the pending fast-gate patch) - for each changed
output, what reads it; then each tool run.

**Nothing downstream breaks.** compare-fronts.py's reworded sentences are parsed by nothing: gate.py reads "The
front of all runs together", next-run.sh the calibration and front lines, review-checks.py the headings and
tables - none changed. A failed build's first-error words: deaths are grouped by the whole message, nothing
reads inside the parentheses. The fast gate's longer evolve log line ("... twice a/b"): chainctl.py's monitor
reads only lines starting "generation ". The `noevolved` in the run's state: next-run.sh compares the string
whole, nothing else parses it. make-bundle.sh reads handoff-check.py's exit status, so rule 11 stops a bundle.

**One tool was broken by its own short output: tools/batch-check.sh** (Iteration 394). It exited 0 when a test
failed, removed the patched clone even after a failure (its comment said it stayed), and printed raw last lines
for the reader to judge. Fixed: PASS only if every check says so in its own words and by its exit status, else
FAIL, exit 1, the clone kept. Tested with stub tools in a scratch repository, five cases: all pass - exit 0, the
clone removed; run-tests failing, validate differing, the jail failing - each FAIL, exit 1, the clone kept; a
patch that does not apply - exit 1, said so. And on the real batch: PASS.

**compare-fronts.py end to end** - its three changes of Iteration 389, first run on the laptop with seed 60:
two small databases from seed 58's front, a 32-bit specialist (d55f05136f) given recorded 64-bit numbers worse
than d79a57826d's, run with --rounds 1 --widths 8,4 --frontier --cpus 0,0 (one CPU here, named twice): exit 0;
the header's sentence and both sign labels there; the thinning active (1e1688dc1b dropped) and the specialist
kept and measured; gate.py's line there; each speed the geometric mean of its two measurements (the same CPU
twice, so the code path, not the arithmetic - a unit test had that).

Not testable here: next-run.sh with `noevolved` end to end (its keyword block is; the laptop's seed 60 is the
first run), and the fast gate over a whole laptop run (seed 63).

**lab/evolve/process-seed.sh** (new at 395, for the chat that processes seeds 59-62): run on seed 58's archive it
reproduced what was found by hand at Iteration 384 - the pack's checks, the verdict as printed (-3.4%, +10.51%, +4
KB, +11.1%, -5.3%; at 32 bits +21.5%), from both CPUs (-0.4% fastest), held out 0.883 / 0.866 / 0.529, the
progress gains, the remote checks' Spearman and rejected-design lines - 79 lines of summary.
