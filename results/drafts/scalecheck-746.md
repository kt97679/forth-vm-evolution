# The scale between runs, and what moved it at the series boundary (Iteration 746)

**In short.** A new check, `lab/evolve/scalecheck.py`, compares two runs' generation-0 readings of the designs carried
into both (unselected both times, both the run's own parallel measure). On one code it reads 0.998 (seeds 95 -> 96); at
the series boundary (seeds 96 -> 97) the JIT designs 0.984 and the rest 1.061. The rest's step is **code placement**: the
after-seed-96 batch shrank every engine (482-2,224 B), which moved each design's interpreter within its cache line;
instruction counts are unchanged, laptop times not. It now runs in every processing (summary.md, beside stopping.py).
This replaces Iteration 744's "the new series reads 3-7 % faster against s6" and 745's "a step on the laptop around
2026-11-19": both rested on chain A's readings, which are not on the runs' scale.

## The check, validated

`python3 -I -B lab/evolve/scalecheck.py OLD NEW` - OLD and NEW a run's db.jsonl or an extract
(`--extract DB OUT.jsonl.gz`: generation 0's records, about 1 MB). Outputs (GENES=1 adds the breakdowns):
results/drafts/scalecheck-95-96.txt, results/drafts/scalecheck-96-97.txt.

| | in both | JIT | not JIT | every time (s6's and the designs') |
|---|---|---|---|---|
| seeds 95 -> 96 (one code: 19 lines of evolve.py's records between) | 6,658 | 0.998 (0.997-0.998) | 0.998 (0.998-0.999) | 2-3 % faster, alike |
| seeds 96 -> 97 (the batch, fixenv, the layout, the new genes off) | 7,117 | 0.984 (0.983-0.985) | 1.061 (1.057-1.063) | s6 0-10 % slower, the designs 2-19 %, unalike |

So the machine drifts uniformly from run to run (2.4 % between seeds 95 and 96) and the ratio to s6 takes it out - what
s6 is for. Within one series the code is one, so the stopping rule's comparisons stand on one scale; the check confirms
it each run (process-seed.sh: the newest earlier results/gen0/seed*.jsonl.gz against the run's database, then the run's
own extract into results/gen0/ - process-finish commits it). Rehearsed on seed 97's archive with seed 96's extract in
place: the section as above, seed 97's extract rewritten byte-identical (mtime 0).

## What moved at the boundary - the code's place, not its instructions

The not-JIT step by compiler and -O (scalecheck-96-97.txt; the loop workload's own time new / old, its median):

| | n | speed | loop | the same on one code (95 -> 96) |
|---|---|---|---|---|
| clang -Os (-Oz) | 1,821 | 1.088 | 1.256 | 0.998, 0.975 |
| gcc -O2 | 1,586 | 1.024 | 1.104 | 0.998, 0.972 |
| clang -O2 | 157 | 0.981 | 1.026 | 0.996, 0.974 |
| JIT, every kind | 3,538 | 0.976-0.990 | 1.018-1.029 | - |

Five of these designs built at seed 96's tree (67767161) and at the batch's (7081f965), the loop workload under
cachegrind (results/drafts/placement-746.py, .txt):

| design | kind | instructions on loop | engine | virtual_machine's offset in its line |
|---|---|---|---|---|
| f0ab9ee997 | clang -Os | -325 of 53.3 M | 6,696 -> 5,952 B | 0 -> 34 |
| c15ec6a706 | clang -Os | -298 of 25.0 M | 11,112 -> 10,416 | 43 -> 17 (its first 5,492 bytes identical) |
| e2b7c31a92 | clang -Os | -297 of 27.4 M | 10,184 -> 9,504 | 43 -> 17 (the first 4,985 identical) |
| d9c6d1587f | gcc -O2 | +5,107 of 33.8 M | 8,520 -> 7,910 | 42 -> 49 |
| 08e3517f54 | gcc -O2 | +0 of 36.3 M | 17,820 -> 17,286 | 32 -> 0 |

The same instructions, the same body shifted: the time moved by where the hot code sits (clang's -Oz aligns nothing,
so it moves most). A design's own ratio is not proof - on one code a design's loop ranges 0.46-1.84 between runs (3
rounds) - but the medians are: clang -Os' loop 1.256 against 0.975 on one code. And they move one way because the
carried designs are fronts, chosen for their in-run speed: their placements were luckier than most, and a new place
regresses them - the winner's curse, on placement. (sysstubs moved clang's engines most; imagemsg and the rest moved
gcc's.)

## What it means

- **The stopping rule**: unaffected within a series (one code, one placement per genome); checked every run now.
- **The endgame's step 2** (results/queued-layout2, then results/queued-jitguard; applied on master here, not committed -
  results/drafts/placement-step2-746.txt): the five interpreted designs tried (c15ec6a706, 08e3517f54, 48a012411a the knee,
  219878ec89 the smallest, d727605472 portable-fastest) keep virtual_machine where it was, the same size, the same
  instructions on loop, at most one instruction different (an address - the layout moves data). The JIT holder
  (9b15ba26f7) grows 112 B and its function moves one line, at offset 0 both times. So the series' in-run readings carry to
  the roles' screen as far as the code's place goes; what the data's new place does to time, the roles' chains measure.
- **A lesson for any later change to engine code**: it re-rolls the interpreted designs' placement, and the search's
  in-run speeds of those designs carry placement luck that does not survive it. A build elsewhere (another compiler
  version, other flags - relf's own build of the C engines) is such a change; a self-built engine is not.
- **An option, not proposed now**: pin virtual_machine's start (aligned to 64, at most 63 bytes an engine), so a change
  outside the function cannot move it. It changes every design's placement - a method change, a new series - and the
  endgame moves no code, so it would buy nothing before the roles.

## Corrections

- Iteration 744 (results/drafts/series-shift-744.txt, section 0): "the new series reads 3-7 % faster against s6" compared
  seed 97 with chain A's `measure-ids.py` readings. Those read the portable designs about 8 % slower than seed 96's own
  in-run and re-measure on the same builds (chain A at 705's tree: the same placement as seed 96). On the runs' own
  measure the new series reads the JIT designs 1.6 % faster and the rest 6.1 % slower. Why chain A's measure differs for
  the portable designs is open (sequential, pinned; the runs' workers parallel) - the roles' chains compare within their
  own sessions, so nothing rests on it.
- Iteration 745 (results/drafts/early-look-745.md, its second part): "a step on the laptop around 2026-11-19" - no. Every
  pack from 2026-11-12 to 2026-11-23 ran Linux 6.17.0-1033-oem (the owner's listing, 2026-11-23), lscpu the same in seeds
  96 and 97, and the machine's run-to-run drift is uniform and cancels. The step is the code's place at the boundary.
