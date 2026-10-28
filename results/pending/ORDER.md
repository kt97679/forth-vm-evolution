# The after-seed-78 batch - to apply first at seed 78's processing (Iteration 561)

Prepared while seed 78 runs; master stays what seed 78's bundle tests. It brings process-run.sh, so seed 78's processing
applies it by hand this once - results/drafts/seed78-checklist-561.md - and process-run.sh then finds it applied.

    git apply results/pending/process-after-seed78.patch
    git apply results/pending/stopping-gen-after-seed78.patch

batch-check (561, on c4a42f4 - the patches as they stand): PASS - both applied to a fresh clone, run-tests PASS,
validate 7 of 7 IDENTICAL, the jail PASS.

**process-after-seed78.patch** (lab/evolve/process-run.sh, process-finish.sh, draft-results.py, process-records.sh - refuses a move onto an existing applied-after-seedN/; tools/setup-sandbox.sh,
wait-for.sh; HANDOFF.md, HANDOFF-PROMPT.md, HANDOFF-REFERENCE.md, README.md, lab/evolve/README.md) - **a processing in three
commands** (the owner, 560-561: every repeatable action a script): setup-sandbox.sh (a new chat's setup, as root);
process-run.sh (detached: process-seed, the drafts, the batch checked and applied with git apply --index, the checks on
master, the control - a death right on master rebuilt on the commit before the batch); process-finish.sh (every check
passed or it stops, the chain line, no TODO, process-records.sh, the chat's records there, the commit, the bundle);
draft-results.py drafts the facts the chat typed (held out, the curse, progress, votes, rules, lifted, 32 bits, the
clock cost, the deaths); wait-for.sh polls. HANDOFF.md's routine three commands, its detail moved to HANDOFF-REFERENCE.md.
Tested: process-finish.sh --dry on seed 77's checks (PASS, and a planted TODO stops it); setup-sandbox.sh fresh and
again; draft-results.py on seed 77's process output; and the whole path the checklist gives, on a clone of master with the
batch applied by hand and seed 77's archive (561): process-run.sh exit 0 - the batch found applied, build, run-tests PASS,
validate 7 of 7, the gate 417 of 417, ans-check 0 of 96 differ, deaths-check 1 of 1 right, the jail PASS; the control at
4256111 (before the hole fix) 0 of 1 right - 560's control by hand, reproduced by the script; process-finish.sh --dry
stopped on a TODO left, then (filled) wrote the chain and control lines and stopped at process-records.sh's new guard
(applied-after-seed77/ exists - the archive was seed 77's). The first try was cut off at run-tests: the sandbox suspends
between turns and a detached job dies - so process-run.sh FROM=checks resumes at the checks (and HANDOFF.md says it).

**stopping-gen-after-seed78.patch** (lab/evolve/hv.py, stopping.py; GOALS.md; results/stopping-series.md) - **every run
judged at generation 100 - the owner's yes needed before it is applied.** The owner (561): the hours vary with his
days. GOALS.md counts the hours in the method, so the rule could never stop; at generation 100 (about 8 hours at seed
77's pace: generation 83 at 6 h, 98 at 7, 113 at 8, 127 at 9) every run is judged at one effort - hv.py --gen; a series'
method line "gen": 100; a run short of it recorded with "short": true, not counted. The 9-hour series line goes; the series
from seed 77 at generation 100 has seed 77's line (hypervolume 0.33872, fastest 0.1435, smallest 14,051, 108 KB, 32-bit
0.1702 - against 0.35010, 0.1406, 14,015, 108, 0.1702 at its end): seed 78 its second run, the earliest stop after 79.
stopping.py's self-test 18 checks. If the owner says no: delete its line above - seed 78 opens the 9-hour series.
