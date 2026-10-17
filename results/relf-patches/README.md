# Patches for relf, from this lab (RELF.md)

Each a patch against vendor/relf/tree (relf master as vendored, vendor/relf/UPSTREAM), applied and
measured by tools/relf-ab.sh: relf's own make test as a regression gate, then its bench-vm.py.

| patch | what | gate | dispatches (realistic) | time |
|---|---|---|---|---|
| `zeq-qbranch.patch` (Iteration 360) | `0= ?BRANCH` as one opcode, 0=?BRANCH (spec 0x60, b16): branches when the flag is not zero; fused by kernel.4's IF (and WHILE) when a 0= was the last operation compiled - as PEEP-VAR does `var @`. opcodes.tab, cv8.c, relfasm64.4, kernel.4 | **passes relf's whole make test** (both engines, both widths, the images reproducing themselves, the shell suites) | **-2.10 %** (18,401,921 to 18,016,020; 0=?BRANCH runs 385,963 times) | this VM: within its noise (ratios 1.00-1.05, the floor +-6 %) - **the laptop's to measure** |
| `var-fetch-plus.patch` (Iteration 361; after zeq-qbranch.patch) | `var @ +` as one opcode, VAR@+ (spec 0x71, slot): the variable added to the top; kernel.4's PEEP-VFPLUS rewrites a just-compiled VAR@'s opcode in place when + follows it (LAST-VF, LAST-VF-END; NO-PEEP forgets it); **and the inliner taught VAR@+ as a slot operation** (INL-OP, INLINE-COPY) | **passes relf's whole make test** (both patches) | **-4.74 % with both** (18,401,921 to 17,529,656): VAR@+ 445,922, 0=?BRANCH 385,963, and 40,428 calls and EXITs fewer - small words with VAR@+ now fit the inliner's 3 instructions and 6 bytes | this VM, both: loop 0.962, **fn 0.933 [0.896-0.969]**, str 0.994, arith 0.987, realistic 0.962, start 1.000 - leaning faster, fn's interval below 1; **the laptop's to confirm** |
| `two-var-fetch.patch` (Iteration 362; after the two above) | `a @ b @` as one opcode, 2VAR@ (spec 0x76, a new operand format slot2: two slots, each from itself): PEEP-VAR rewrites a VAR@ ending right where it rewinds a variable's call; **CALL, keeps LAST-VF across its NO-PEEP** (else the call to b erased the VAR@ before: a first version never fired); the inliner taught 2VAR@ (its length, both slots re-aimed); relf's image-audit.py, superinst.py and opcodes.py taught slot2 | **passes relf's whole make test** (all three) | **-6.41 % with all three** (18,401,921 to 17,221,555): 2VAR@ about 329,440, VAR@+ 408,333 (some `a @ b @ +` now 2VAR@ +, no loss), 0=?BRANCH 385,963, and 56,653 calls and EXITs fewer | this VM, all three: loop 0.969, fn 0.969, str 0.985, **arith 0.947 [0.921-0.971], realistic 0.944 [0.922-0.967]**, start 0.987 - two intervals below 1; **the laptop's to confirm** |

To measure one on the laptop (quiet, as relf's own reports were):

    sh tools/relf-ab.sh -r 30 -s 4 results/relf-patches/zeq-qbranch.patch \
        results/relf-patches/var-fetch-plus.patch results/relf-patches/two-var-fetch.patch

**A lesson (Iteration 361)**: the first VAR@+ passed relf's whole suite and still cost 167,966 calls -
kernel.4's inliner knew the slot opcodes by number (INL-OP, INLINE-COPY: 100, 101) and so would not
copy a small word holding the new one; only the dispatch count showed it. A new slot opcode must be
taught to everything that knows them by number: the peephole, the inliner, relf's image tools.

Within relf's 64 one-byte opcodes (its QUESTIONS.md A15) a fused opcode takes a slot whose operation
then runs escaped; for the measurement it sits at a free number (0x60) - the trade, if adopted, R@'s
slot (0.13 % of dispatches) by tools/relf-pairs.py's budget. UNTIL's backward branch (BACK, with its
8-bit form) is not fused yet; the rest of 0='s runs are there or before other operations.

**A second lesson (Iteration 362)**: the first 2VAR@ passed relf's whole suite and never fired once -
CALL, begins with NO-PEEP, which (since VAR@+) also forgot the last VAR@, so the call to b in `a @ b @`
erased the memory of the first fetch before @ came. Passing tests prove a fusion safe, not that it
happens: each patch is counted too (tools/relf-pairs.py with RELF_TREE on the harness's B).

## Build-only candidates: this lab's cheap genes on relf's shell (Iteration 364)

The C-engine-only class of results/drafts/relf-gene-classes.md, each measured through the whole gate
(`RELF_AB_MAKE_B`, make variables for B alone; the shells measured are the ones built, set aside
before relf's make test - which rebuilds relf64 without them - and checked: B's engine text, or its
use of the pinned register). This VM, 12 rounds at SCALE=2, B's time over relf's:

| candidate | gate | loop | fn | str | arith | realistic | start |
|---|---|---|---|---|---|---|---|
| CC=clang (18, against gcc 13) | passes | 1.054 | 1.044 | **1.044** | 1.036 | 0.995 | 1.003 |
| REGPIN=1 (`regpin.patch` + -DREGPIN=1: ip rbx, rp r12, dsp r13, tos r14) | passes | 1.024 | 1.006 | **1.059** | **0.956** | 1.002 | 0.982 |
| CFLAGS=-Os (engine text 25,574 bytes, from 26,519) | passes | **1.046** | **1.022** | 1.046 | 0.992 | **1.019** | 1.033 |

(bold: the interval excludes 1.) **None of them transfers**: clang and -Os, what every one of this
lab's fastest designs of seeds 55-56 chose, are slower for relf's cv8.c - they belong to those designs'
whole combination of genes, not to engines at large; relf's cv8.c has been tuned with gcc -O2 through
hundreds of its iterations. Two more need no test: relf dispatches through a 256-entry table already
(d256) and guards its stacks with pages already (GUARD 1). What this lab can give relf is at the
level of its instructions, measured on its terms - the three patches above.

