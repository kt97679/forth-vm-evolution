# The fixed data layout, step 1 - applied at Iteration 734 (batch-check PASS on c9a9f6f6)

One patch, `data-layout.patch`: results/drafts/early-games-713.md's proposal, step 1 (GOALS.md's register, 713) - the
engine's writable data in a fixed layout, by an augmenting linker script, engine/data-layout.ld (GNU ld and lld, -T
with INSERT: the default script kept). The engine is built with -fdata-sections, so each variable is a section of its
own; the script places them by name: every small variable in one page-aligned block (.bss.hot), the tables a run
touches after it (.bss.tab: dispatch, the tag's maps, the JIT's per-word marks, then t_obuf and the loader's heads,
buffers used from their start), the other buffers of 4 KB and more after them (.bss.big: the stacks first). No C but
the dictionary's array form (the old families, STACKSEP 0) given a section of its own name. lab/evolve/evolve.py links
every engine of the lab's with it (rt(): x86-64, i386, the ARM builds); lab/evolve/data-layout-check.py lists each
section's members from a link map and faults a big buffer the lists missed - run-tests runs its --self-test (two
roles). Not the stages' engines (tools/build-stages.sh) nor the shipped designs until they are exported again
(export-designs.py copies the script into src/ and writes -Wl,-T,src/data-layout.ld, as it does every file argument).

Checked on a scratch clone (results/drafts/data-layout-734.txt; data-layout-734.py, data-layout-cache-734.py): the ten
roles' engines the same size, every workload's output the same, the instructions the same; the record's memory 8-36 KB
less on nine at 8-byte cells, 12-24 KB on three at 4, least-memory the same (108 KB, 25 runs a workload); start-up 2-8
faults fewer; the L1 and last-level data misses within 1 %; validate, run-tests PASS. Two variants measured and not
taken: the block in the file page's tail (a copy-on-write fault where .data is not written - least-memory +1), and the
written initialized variables made zero at load (no fault fewer, +2-48 B of engine). Then batch-check (run-tests PASS,
validate 7 of 7 IDENTICAL, the jail PASS), `git apply`, the stages rebuilt.

Apply, from the top of the tree:

    git apply results/applied-data-layout-734/data-layout.patch
