# Seed 78's processing - the checklist (Iteration 561)

The first processing with process-run.sh; it comes in the after-seed-78 batch (results/applied-after-seed78/ORDER.md), so once:

1. As root: `git clone -q /mnt/user-data/uploads/<bundle> /tmp/s && cd /tmp/s && git apply
   results/applied-after-seed78/process-after-seed78.patch && sh tools/setup-sandbox.sh && cd / && rm -rf /tmp/s`.
2. As claude in /home/claude/forth-vm-evolution: `sh tools/batch-check.sh` detached, PASS; then each patch ORDER.md
   names (all three: the owner said yes to the matched stopping rule, 562) with `git apply --index`, and `git commit -m "Iteration N: the
   after-seed-78 batch applied - K patches (...), batch-check PASS"`.
3. `setsid nohup sh lab/evolve/process-run.sh N > /dev/null 2>&1 &` - early in a turn, and seen to DONE in it: a
   detached job dies when the turn ends (561; cut off: FROM=checks resumes it at the checks). It finds the batch applied; then HANDOFF.md's
   routine: wait-for.sh, summary.md, the judgment, process-finish.sh.

What to judge:
- **The stopping rule** (matched, 562): seed 78 is the series' second run, judged at its last generation against
  seed 77 at that generation - stopping.py prints the bar; at about 120 generations: the hypervolume >= 0.34447, the
  fastest <= 0.1394, the smallest <= 13,910, the memory <= 104 KB, 32-bit <= 0.1668. process-run.sh computes its curve.
- **Prediction 560** is on the whole run's tolerance front (hv.py's line), not the stopping rule's matched numbers: the fastest in
  0.1363-0.1450, the hypervolume in 0.3485-0.3567, the smallest above 14,015.
- **The deaths**: from seed 78 on (the hole fix applied before it ran) a JIT death of the 557 pair is a regression.
- **NEXT-RUN**: seed 79 at the owner's hours.
