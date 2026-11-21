# The lean end's 4 KB between chains A and B - the after-seed-96 batch's layout, not the environment (Iteration 714)

Chain B's laptop read the lean end 4 KB above chain A's (results/followup-roles-seed96-roles-b.md): fb0d57c8a2 108 ->
112 KB, d180351903 116 -> 120, both by measure-ids.py on the laptop in each chain. Between the chains only the
after-seed-96 batch changed what a design is (7081f96: rtsc, sysstubs, imagemsg, wends16 - every engine 482-2,224
bytes smaller; cputime's counters patch reads the child's rusage as before).

`python3 -I results/drafts/memshift-714.py TREE results/followup-seed96-roles-b.md ID ...`, the same shell, once in a
clone at 3a04c66 (before the batch) and once at master (after): each design built at 8-byte cells, its pages read as
evolve.measure reads them (the faults of the kernel workload - rss - medians of 9; the start-up's, medians of 15), with
the sandbox's environment and with it 4 KB larger. The outputs alike in every run.

| design | engine before -> after | kernel pages, env as is | env +4 KB | start-up, env as is |
|---|---|---|---|---|
| fb0d57c8a2 (least memory) | 8,192 -> 7,574 B | 30 -> 31 | 31 -> 32 | 18 -> 19 |
| 71005d8a0d | 8,192 -> 7,606 B | 30 -> 31 | 31 -> 32 | 19 -> 19 |
| d180351903 (smallest) | 4,912 -> 4,182 B | 33 -> 32 | 33 -> 33 | 20 -> 21 |

The batch moves a design's pages by one, up or down by design - fb0d57c8a2's +1 here is the laptop's +4 KB;
d180351903's -1 here against the laptop's +1 is the environment's page boundary meeting the new layout (the sandbox's
environment is 17 KB, the laptop's near nothing - results/drafts/fixenv-713.md). Layout luck, as
results/drafts/early-games-713.md measured it (1-4 pages by data order alone), not a change in how the laptop measured:
within the roles' 8 KB rule, which takes one page as a design's own noise (708). What follows: a memory record from
before the batch (chain A's, the handoff's, results/relf-designs-649.md) does not compare page for page with one after
it; the chains' rule comparisons stand (each chain measures its own designs at one commit). The queued fixenv takes
the environment's share out; the fixed layout of the engine's writable data (the early-games prototype) would take
the layout's.
