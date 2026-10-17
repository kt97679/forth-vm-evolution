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
