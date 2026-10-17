# Patches for relf, from this lab (RELF.md)

Each a patch against vendor/relf/tree (relf master as vendored, vendor/relf/UPSTREAM), applied and
measured by tools/relf-ab.sh: relf's own make test as a regression gate, then its bench-vm.py.

| patch | what | gate | dispatches (realistic) | time |
|---|---|---|---|---|
| `zeq-qbranch.patch` (Iteration 360) | `0= ?BRANCH` as one opcode, 0=?BRANCH (spec 0x60, b16): branches when the flag is not zero; fused by kernel.4's IF (and WHILE) when a 0= was the last operation compiled - as PEEP-VAR does `var @`. opcodes.tab, cv8.c, relfasm64.4, kernel.4 | **passes relf's whole make test** (both engines, both widths, the images reproducing themselves, the shell suites) | **-2.10 %** (18,401,921 to 18,016,020; 0=?BRANCH runs 385,963 times) | this VM: within its noise (ratios 1.00-1.05, the floor +-6 %) - **the laptop's to measure** |

To measure one on the laptop (quiet, as relf's own reports were):

    sh tools/relf-ab.sh -r 30 -s 4 results/relf-patches/zeq-qbranch.patch

Within relf's 64 one-byte opcodes (its QUESTIONS.md A15) a fused opcode takes a slot whose operation
then runs escaped; for the measurement it sits at a free number (0x60) - the trade, if adopted, R@'s
slot (0.13 % of dispatches) by tools/relf-pairs.py's budget. UNTIL's backward branch (BACK, with its
8-bit form) is not fused yet; the rest of 0='s runs are there or before other operations.
