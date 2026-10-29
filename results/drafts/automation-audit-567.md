# Where the chat's manual work can become scripts - an audit (Iteration 567)

The owner: audit the project for manual effort on the chat's side that a script can take (prompts/21 item 9, prompts/22).
Read: HANDOFF.md's routine and HANDOFF-REFERENCE.md's processing steps, the tools (tools/, lab/evolve/*.sh and the
evolver's README), the 118 commits of Iterations 500-567 by subject, and this chat's own work (567: a fault found and a
batch made, between runs).

## Already scripted - the baseline

A returned seed is three commands (560): setup-sandbox.sh, process-run.sh (unpack, draft, batch-check and apply, the
checks, the control), process-finish.sh (refuses until every check, TODO and record is there; process-records.sh; the
bundle). Between runs: batch-check.sh, wait-for.sh, make-bundle.sh with handoff-check.py, and since 567 setup-sandbox.sh's
SCRATCH= scratch tree. What stays by hand at a processing is judgment by design: the verdict, the predictions, NEXT-RUN,
the card, the PROGRESS entry. The manual work left is mostly **between runs**, and in **records that restate a fact**.

## The evidence

Of the 118 commits since Iteration 500: 20 "records - ..." fix-ups; 11 recording a batch-check result in ORDER.md by hand
("batch-check PASS on X", a commit each time - the after-seed-78 batch three times); 5 an index line handoff-check asked
for (an xcheck file, a checklist, an ORDER.md - 567's too), 9 touching a per-seed checklist. This
chat: two throwaway scripts to build a genome and run it against s6 (the minimal design on sim16; four designs at both
widths, at two windows), about ten tool calls for a batch's mechanics (patches from the scratch commits, ORDER.md's apply
lines, its index line after handoff-check failed, the PASS line, two commits), a disposable list in the wrong format - and
seed 81's checklist, written at 566, found stale: "nothing waits in results/pending/" while a batch waits.

## The candidates, by what they save

| # | what | recurs | the script | where | size |
|---|---|---|---|---|---|
| 1 | a batch's mechanics | every batch, about one a seed | `tools/batch-make.sh N`: each commit of the scratch tree past master one patch, `NAME-after-seedN.patch` from its subject's first word; ORDER.md's title and `git apply` lines, a TODO for the prose (handoff-check refuses it); results/README.md's pending line; the commit; batch-check detached. `RECORD=1 batch-check.sh` writes its line into ORDER.md and commits. Run again after master moves: the patches regenerated | tools/ - master | ~60 lines sh |
| 2 | a design built and run against s6 | every fault (566, 567: by hand; gene-narrow, deaths-check and jit-sweep-558.py each carry their own) | `lab/evolve/design.py (ID [--db F] \| STAGE GENE=V ...) [--width 4] WORKLOAD\|FILE ...`: right / WRONG / DIES, the first differing lines, `--keep` the build | the batch (lab/evolve) | ~80 lines py |
| 3 | the next run's bars | every hours decision (566: by hand, into the prediction) | `stopping.py --bar GEN`: the gain bars at generation GEN from the ledger's curves - the prediction's numbers | the batch | ~20 lines |
| 4 | a fact restated, then stale | each per-seed checklist; the hours in four files (566's commit) | not a script - the checklist keeps judgment only (what to decide, what to read), never state: a batch waiting, the hours, a bar - process-run's summary and stopping.py print those from their sources | convention | - |
| 5 | predictions scored | every processing | each prediction ends with a fenced block of bars (metric, generation, comparator, value); `predictions.py score N` reads the ledger and the summary and drafts the "Scored" line per bar; the reading stays the chat's | the batch | ~80 lines |
| 6 | the log naming its files | every iteration (the article is written from it) | handoff-check: a file added under results/ since the last bundle and named in no PROGRESS entry fails it | tools/ - master | ~15 lines |
| 7 | the switch's message | every new chat | make-bundle.sh prints HANDOFF-PROMPT.md's second message with the bundle's name in it - the owner pastes it | tools/ - master | ~5 lines |
| 8 | the disposable list | most turn ends | `tools/disposable.sh PATH REASON` appends a line in the format handoff-check reads | tools/ - master | ~5 lines |

1 and 2 save the most: 1 is a turn's dozen mechanical calls and the commonest fix-up commit; 2 is the step every fault
starts with, written afresh each time. 3 and 4 remove a class of stale record. 5 is the largest change for its saving,
and its bars need a format the predictions do not have yet - after 1-4. 6-8 are small.

## What stays judgment

The verdict, what a prediction says, a fault's diagnosis, ORDER.md's prose, the card, the PROGRESS entry's what and why.
A script drafts and checks around them, as draft-results.py's TODO lines do; it does not write them.

## Where they go

tools/ (1, 6, 7, 8) run only here: committed on master, tested as written. lab/evolve/ (2, 3, 5) is the laptop's tree too:
appended to the after-seed-81 batch, batch-check run again, applied at seed 81's processing.

## Done (Iteration 567, the owner's yes to 1-4)

1. tools/batch-make.sh (master); batch-check.sh RECORD=1; handoff-check refuses a TODO in ORDER.md. First use: the two
   patches below - made, indexed and committed in one command, the PASS recorded by the check itself.
2. lab/evolve/design.py (design-after-seed81.patch): the minimal design right at both widths, DIES with the old window.
3. stopping.py --bar (bar-after-seed81.patch): its first use found a bar typed wrong - prediction 566's smallest, 13,849
   where the rule gives 13,910 (results/predictions.md's note).
4. The convention in HANDOFF.md: a checklist holds judgment, not state; seed 81's stale line corrected.

5-8 not done: 5 waits for 1-4 to be used once; 6-8 are small and can go with the next tools change.
