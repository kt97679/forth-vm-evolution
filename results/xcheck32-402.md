# The 32-bit hosts against the laptop's 32-bit speeds (Iteration 402, HANDOFF open item 0g)

xcheck.py --report compared every host with the laptop's 64-bit speeds; for a run selected at both widths a 4-byte host
is better compared with the laptop's own 32-bit speeds. `--laptop32 FILE` (a results/evolve-*.md's front lines, or a
db.jsonl) now adds that comparison; without it the report is as before, so nothing a run does changes.

Seed 59's chain's checks of seed 58's front, again:

| host | against the laptop's 64-bit speeds | against its 32-bit speeds |
|---|---|---|
| dream, 32-bit x86 | 0.651 (22 designs) | 0.650 (16 with a 32-bit speed) |
| rage, the Tegra (ARMv7) | 0.709 (11) | 0.857 (8) |

For the Tegra the width was part of the gap; for dream it was not - another x86 machine ranks seed 58's front at 32 bits
about as differently from the laptop's 32-bit ranking as from its 64-bit one: the machine, not the width (item 4d's
question). Small samples: the designs with a 32-bit speed are the front's, not the rejected ones the checks add.

**The Tegra's link failures** (open item 0d). Seed 59's chain: 5 of its 16 designs failed to link there (ce937eca6d,
d55f05136f, 2ad3508c5e, c47b567e8e, fb73c9be4a), all fsys 1, which 1 of the 11 measured has. Seed 58's chain: its 3
(5405c5b1d9, df0c11fd98, ade7c2acb9) all fsys 2, which 4 of its 13 measured have. All eight with the file words in Forth
(fsys on), 5 of the 24 measured (results/drafts/xcheck-fails-402.py). A lead, not the cause: seed 60's chain is the first
to record the linker's first error.
