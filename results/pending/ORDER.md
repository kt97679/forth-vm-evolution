# The after-seed-74 batch - to apply at seed 74's processing (Iteration 545)

Prepared while seed 74 runs; master stays what seed 74's bundle tests.

    git apply results/pending/fail32-cpt16-after-seed74.patch
    git apply results/pending/clock-hold-after-seed74.patch
    git apply results/pending/progress-header-after-seed74.patch

**fail32-cpt16-after-seed74.patch** (lab/evolve/review-checks.py) - **cpt16's reach, expected**. cpt16 refuses calls
past its 16-bit reach out loud ("call out of reach", forth/cpt16.4; Iteration 517), and its designs alive at 64 bits -
their applications right - fail the applications at 32 bits, "wrong output: apps": the same refusal at 4-byte cells
(seed 72's processing). Seeds 72 and 73: 67 and 61 such designs, every one cpt16; fail32 called them "not a known
cause - look" and rule 5 read ATTENTION. Now a class of its own beside the known causes (regressions) and the unknown:
expected, no fault - fail32 counts it on a line of its own; rule 5 names it and passes when nothing else failed.
Tested on seed 73's records: fail32 61 expected, 0 unknown, rule 5 PASS; the negative control - one of the 61
re-encoded cv8 - 1 unknown, rule 5 ATTENTION.

**clock-hold-after-seed74.patch** (lab/evolve/next-run.sh, lab/evolve/perf-hold-start.sh, lab/evolve/clockcheck.py,
tools/run-tests.sh) - **the clock test takes the chain's perf hold** (the owner, Iteration 545). Seed 74's clock test
runs with kernel.perf_event_paranoid at Ubuntu's 4 - CPU time and the core's clock, no cycles - unless set by hand,
and set by hand it holds through the evolution as well: tools/cputime.c opens the counters for every run once it may.
Now a chain with clockcheck.py takes the hold counters.py and missmap.py take (282, 314): sudo asks once, at the
start; root's perf-hold.py sets 2 only while the clock test measures. The clock test needs no perf program (cputime.c
reads the counters itself), so perf-hold-start.sh skips that check for it (PERF_HOLD_FOR=clockcheck.py) - a kernel
update without its linux-tools cannot stop the run - and a refused or failed hold stops nothing: the clock test runs on
the time alone, and says so ("none" in PERF_HOLD_START: the chain's later steps do not ask again). clockcheck.py holds
around its measuring (counters.PerfHold). Tested: clockcheck.py --self-test, now in run-tests - the handshake against
a stand-in for perf-hold.py (2 while it measures, 4 after), no holder, none; perf-hold-start.sh with no perf program -
the clock test's passes, counters.py's stops as before; next-run.sh's block in a harness with stand-ins for
perf-hold-start.sh and counters.py - the clock test held, refused (the time alone, said), counters.py held and refused
(stops, as before), no such step, a later step: as intended. Not run here: sudo and root's perf-hold.py (this
sandbox's paranoid is 2) - the first chain with the clock test exercises them, in the foreground, where the counters
steps have since 282.

**progress-header-after-seed74.patch** (lab/evolve/progress-table.py, results/progress-by-run.md) - the table's header
said the fast gate took the slower of two readings from seed 72; that gate was withdrawn at 513
(results/drafts/fastgate-slower-withdrawn-513.patch) and every row since reads "mean". The header only.
