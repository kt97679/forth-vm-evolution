# The after-seed-78 batch - to apply first at seed 78's processing (Iteration 561)

Prepared while seed 78 runs; master stays what seed 78's bundle tests. It brings process-run.sh, so seed 78's processing
applies it by hand this once - results/drafts/seed78-checklist-561.md - and process-run.sh then finds it applied.

    git apply results/pending/process-after-seed78.patch
    git apply results/pending/stopping-gen-after-seed78.patch

**process-after-seed78.patch** (lab/evolve/process-run.sh, process-finish.sh, draft-results.py; tools/setup-sandbox.sh,
wait-for.sh; HANDOFF.md, HANDOFF-PROMPT.md, HANDOFF-REFERENCE.md, README.md, lab/evolve/README.md) - **a processing in three
commands** (the owner, 560-561: every repeatable action a script): setup-sandbox.sh (a new chat's setup, as root);
process-run.sh (detached: process-seed, the drafts, the batch checked and applied with git apply --index, the checks on
master, the control - a death right on master rebuilt on the commit before the batch); process-finish.sh (every check
passed or it stops, the chain line, no TODO, process-records.sh, the chat's records there, the commit, the bundle);
draft-results.py drafts the facts the chat typed (held out, the curse, progress, votes, rules, lifted, 32 bits, the
clock cost, the deaths); wait-for.sh polls. HANDOFF.md's routine three commands, its detail moved to HANDOFF-REFERENCE.md.
Tested: process-finish.sh --dry on seed 77's checks (PASS, and a planted TODO stops it); setup-sandbox.sh fresh and
again; draft-results.py on seed 77's process output; process-run.sh whole - below.

**stopping-gen-after-seed78.patch** (lab/evolve/hv.py, stopping.py; GOALS.md; results/stopping-series.md) - **every run
judged at generation 100 - the owner's yes needed before it is applied.** The owner (561): the hours vary with his
days. GOALS.md counts the hours in the method, so the rule could never stop; at generation 100 (about 8 hours at seed
77's pace: generation 83 at 6 h, 98 at 7, 113 at 8, 127 at 9) every run is judged at one effort - hv.py --gen; a series'
method line "gen": 100; a run short of it recorded with "short": true, not counted. The 9-hour series line goes; the series
from seed 77 at generation 100 has seed 77's line (hypervolume 0.33872, fastest 0.1435, smallest 14,051, 108 KB, 32-bit
0.1702 - against 0.35010, 0.1406, 14,015, 108, 0.1702 at its end): seed 78 its second run, the earliest stop after 79.
stopping.py's self-test 18 checks. If the owner says no: delete its line above - seed 78 opens the 9-hour series.
