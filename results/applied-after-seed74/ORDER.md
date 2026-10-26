# The after-seed-74 batch - to apply at seed 74's processing (Iteration 545)

Prepared while seed 74 runs; master stays what seed 74's bundle tests.

    git apply results/applied-after-seed74/fail32-cpt16-after-seed74.patch
    git apply results/applied-after-seed74/clock-hold-after-seed74.patch
    git apply results/applied-after-seed74/progress-header-after-seed74.patch
    git apply results/applied-after-seed74/truefronts-after-seed74.patch
    git apply results/applied-after-seed74/chain-logs-after-seed74.patch

batch-check (545): PASS - the first three applied to a fresh clone, run-tests (the clock test's self-test among them),
validate 7 of 7 IDENTICAL, the jail. Again with all four (547): PASS. At seed 74's processing (549) patches 3 and 4
revised and 5 added - batch-check again: PROGRESS.md.

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
(results/drafts/fastgate-slower-withdrawn-513.patch) and every row since reads "mean". And (549) the front counted by
the report's front table, not by its genomes: from seed 74 the genomes list the re-measured designs off the front too -
seed 74's row read 261 for a front of 238.

**truefronts-after-seed74.patch** (lab/evolve/truefronts.py new, lab/evolve/README.md) - **every run's true front from
its records** (the owner, Iteration 547; GOALS.md: the article's figures on the true fronts). The runs' records are on
the laptop alone, so it is a chain's experiment step - seed 75's last: `then experiment truefronts.py`. It reads every
archived run's database ($RUNS, else runs/, and lab/evolve/runs/; next-run.sh passes only the newest four), measures
nothing, and names each run by its seed - the results file whose reported front the run's own children made (generation
1 on: a carried design is a founder, generation 0, in the runs after), else the chain's line for this clone's run. Out,
in truefronts.md: a row a run - records, alive, the true front against the reported one, the fastest in the run and at
32 bits, the smallest, the least memory, what its speed is over - and every true front's designs as JSON lines, for the
progress table and the charts. Tested on seed 73's records: seed 73 named at 100%, the true front 222 (votes --db's),
the reported 174, the extremes as its results file's; the same records under other ids named by the chain's line (seed
99 in the test); a run with no speed or size in its records listed as such. About 20 s a database here, 81 MB each. Revised at 549:
tools/clean-runs.sh keeps the newest four archived runs only, so it reads every seed pack first - $RUNS and its chains'
packs/, the db.jsonl inside, the seed from the pack's name, the newest pack of a seed - and a database besides only for a
seed no pack gave. Tested on seed 74's pack: 238, the extremes as seed74-front-549.py's.

**chain-logs-after-seed74.patch** (tools/clean-runs.sh, lab/evolve/next-run.sh, tools/test-clean-runs.sh) - **seed 74's
experiments failed at their packing**. clean-runs.sh, run before every step of a chain, removed a run directory once its
pack was in a chain's packs/ (541) - also while that chain ran: the seed step's directory went before the experiments,
with the tests', validation's and jail's logs a later step copies (`2>/dev/null || true`), and each experiment then
failed at `cp .../tests.log`, its report whole. Now: such a directory goes only once its chain has finished; the first
step's logs are kept in the chain's directory too (checked/), where the later steps copy them from; and an experiment's
pack takes the logs that are there. Tested: test-clean-runs.sh, 13 checks - the new one, a running chain's first step
keeps its directory; next-run.sh's syntax; the first chain at seed 75 runs the rest.
