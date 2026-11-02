# Consolidation's retirement planned - 578's rule with seed 86, checked against the final pick's candidates (Iteration 583)

The rule (the owner, 578): a gene value or code path is retired only when no design on the pooled true front uses it.
Rerun with seed 86 in the pool (results/drafts/retire-report-583.md; retire-report-579.py): 9 results files, 444 designs
on the pooled true front, 17 values on none of them - against 579: alignhot=0 off the list (a seed 86 front design uses
it), rtloop=2 on (its one front design displaced). But the final set is chosen from the 232 candidates, not the front
alone, so a value is retired only when no candidate - at consolidation, no final-set design - uses it either
(results/drafts/retire-candidates-583.py): jitdoes=1 12 candidates (the fastest, 15ecc6a232, the draft set's #1, among
them), fsys=1 12, rtloop=2 1, the other 14 none.

| value | front | candidates | the code it would remove | class |
|---|---|---|---|---|
| fsys 4, 5 | 0 | 0 | the engine's FSYS >= 4 blocks, file-sysc4.4 and file-sysc5.4, their helpers and dumps (119 lines) | **retired** - the fsys45 batch, queued (results/queued-consolidation/) |
| jitdoes 1 | 0 | 12 | jit.c's `#if JITDOES` block, the flag; the gene FROZEN at 0 | after the final set - retired if no final design uses it |
| rtloop 2 | 0 | 1 | the headerless loop words (layout.py --headerless) | after the final set, as jitdoes |
| msc 1 | 0 | 0 | tools/gen-msc.py and evolve.py's hooks, about 350 lines - the largest | the Tegra first (573): the pairs below in chain B |
| bytehdr 0, doesfar 0, lean 0, scale 1-3, varcall 0 | 0 | 0 | the older formats - they build the hand-made stages s2-s5 | the owner's: freeze s2-s5 as built artefacts, or keep |
| jit 0, jitinl 0, jitos 0; fsys 1; alignhot 1 | 0 | 0-12 | none - the search space only (fsys 1's file-sysc.4 loads at 2-3 too; alignhot 1 a flag string, its removal shifting later values' ids) | kept: nothing simpler |

**msc on the Tegra** (retire-candidates-583.py --msc on seed 86's db.jsonl): its 4 alive msc=1 designs without the JIT, each
with its nearest msc=0 one - on x86 slower and twice the size, never measured on ARMv7, where the JIT cannot win:
6d321be1cc / 9920e9af07 (0.343 / 0.308; 2 genes apart), 01efebca24 / 97a4e37ab4 (0.352 / 0.309; 2), c67e6b5336 /
8bddf3a5e4 (0.356 / 0.322; 2), 629b7e96ec / 75acca89a6 (0.374 / 0.348; 5). For chain B's Tegra list, by id (xcheck.py
--also; the laptop has seed 86's database). msc=1 retired only if each pair's msc=0 design is as fast there or faster.

**At consolidation** (after chain B's final pick): retire-report-579.py and retire-candidates-583.py on the final set;
jitdoes and rtloop 2 drafted if no final design uses them; msc by the Tegra's pairs; the stage genes by the owner's
decision; then results/queued-consolidation/ moved to results/pending/ with the new patches and batch-check run on that
master - the fsys45 patch tested at 583 against master then, not later.
