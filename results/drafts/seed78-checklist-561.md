# Seed 78's processing - the checklist (Iteration 561)

The first processing with process-run.sh; it comes in the after-seed-78 batch (results/pending/ORDER.md), so once:

1. As root: `git clone -q /mnt/user-data/uploads/<bundle> /tmp/s && cd /tmp/s && git apply
   results/pending/process-after-seed78.patch && sh tools/setup-sandbox.sh && cd / && rm -rf /tmp/s`.
2. As claude in /home/claude/forth-vm-evolution: `sh tools/batch-check.sh` detached, PASS; then each patch ORDER.md
   names (the stopping one only if the owner said yes) with `git apply --index`, and `git commit -m "Iteration N: the
   after-seed-78 batch applied - K patches (...), batch-check PASS"`.
3. `setsid nohup sh lab/evolve/process-run.sh N > /dev/null 2>&1 &` - early in a turn, and seen to DONE in it: a
   detached job dies when the turn ends (561; cut off: FROM=checks resumes it at the checks). It finds the batch applied; then HANDOFF.md's
   routine: wait-for.sh, summary.md, the judgment, process-finish.sh.

What to judge:
- **The stopping rule**: with the stopping patch, seed 78 at generation 100 is the series' second run - it gains on
  seed 77 if the hypervolume >= 0.34211, the fastest <= 0.1407, the smallest <= 13,910, the least memory <= 104 KB or the
  fastest at 32 bits <= 0.1668 (stopping.py in summary.md says it). Without it, seed 78 opens the 9-hour series.
- **Prediction 560** is on the whole run's tolerance front (hv.py's line), not at generation 100: the fastest in
  0.1363-0.1450, the hypervolume in 0.3485-0.3567, the smallest above 14,015.
- **The deaths**: from seed 78 on (the hole fix applied before it ran) a JIT death of the 557 pair is a regression.
- **NEXT-RUN**: seed 79 at the owner's hours.
