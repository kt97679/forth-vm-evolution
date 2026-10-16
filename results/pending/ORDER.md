# The after-seed-56 batch - apply in this order (against master after Iteration 338)

| # | patch | what it does |
|---|---|---|
| 1 | two-widths-after-seed56.patch | **Selecting at both widths** (the owner, Iterations 336-338; results/drafts/two-width-selection.md). evolve.py --widths 8,4: setup at 4-byte cells first (setup_widths: its own reference, kernel reference and k32 variants under width-suffixed paths), then as always; each design passing screening also measured as a 32-bit x86 engine at 4-byte cells (eval32: its JIT off, its call scale at most 2, a round fewer, the selection's workloads) - speed32, a fourth objective in dominates() and crowding(); none, with why32, if it does not build or live so. NEXT-RUN's word: widths. The report's 32-bit column and seed-facts' two-width lines from the data. **The converter's call alignment** (tools/layout.py): bodies aligned to max(cell, 2^scale) - the cell at 8-byte cells; SKIPPAD's shortcut only where a scaled call reaches it - seed 54's converter death (a2c8d50d0a) converts and lives. **The cell family's image** by width (and --validate's). No gene; ids unchanged. compare-fronts still judges at 64 bits. |

    git apply results/pending/two-widths-after-seed56.patch

Tested on master at Iteration 338 (results/drafts/two-width-selection.md, "Built so far", "Built"):
- **64 bits unchanged**: six recorded designs of seed 55's front - engines and images byte-identical
  against a clean clone; gene-equiv.py: PASS - 4,096 recorded genomes, every operator draw; run-tests
  PASS; validate 7 of 7 IDENTICAL; the gate: alive: 248 of 248 (the run's front 168, the joint front 133, 53 in both).
- **Two widths**: scratch runs (population 4, one generation, seed 99) - the first 12 of 20 designs
  with speed32; after the alignment fixes, the scale cap and the cell family's image, **20 of 20**
  (results/drafts/two-width-scratch-db.jsonl is the second run's). The report shows the 32-bit
  column from the data alone (no flag); seed-facts' lines: 7 of 7 of the front with speed32,
  Spearman 0.643 between the widths there.
- On a fresh clone of master after Iteration 338 it applies and reproduces the tested files.

To use it: NEXT-RUN "seed N tag2 Hh widths ..." - each design costs about one more build and
measurement, so fewer designs an hour.
