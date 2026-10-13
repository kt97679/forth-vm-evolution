# The scratch trees, sorted (Iteration 276)

For each tree of the chats of Iterations 213-265 (as found, beside this file): the lines its
patches add - uncommitted.patch and commits-past-clone.patch, lines over 8 characters - and the
share of them that master holds today, anywhere. At 90% or more the tree's work reached master;
under 50% it did not - an experiment kept only here, or work rewritten since. A share is a
pointer, not a proof: read the patch before relying on it.

| tree | lines added | in master | untracked files | verdict | its HEAD, as found |
|---|---|---|---|---|---|
| `ansall` | 6 | 0% | 0 | NOT in master - look | 8953d4c Iteration 253: lab/evolve/progress-table.py and results/progre |
| `b44` | 17 | 100% | 0 | in master | 6628c73 Iteration 224: the hidden-names findings captured in GOALS.md' |
| `b44s` | 93 | 98% | 0 | in master | 34814fc scratch: stackheads |
| `b45` | 312 | 54% | 0 | mostly in master, changed since | 57ef97e scratch: patch 5 (dispoff) |
| `b46` | 274 | 87% | 0 | mostly in master, changed since | 0470c07 scratch: primfirst |
| `b46b` | 302 | 97% | 0 | in master | 5bd981a scratch: jittail |
| `b46c` | 298 | 97% | 0 | in master | 85fe50d scratch: nobit7 |
| `base45` | 262 | 38% | 0 | NOT in master - look | ea9f79d scratch: names |
| `batch43` | 433 | 91% | 0 | in master | e845899 scratch: guard-after-seed43.patch applied |
| `cmp43` | 0 | - | 0 | nothing added | 6437350 Iteration 217: a survey of JITs and VM speed elsewhere (result |
| `ec` | 1 | 0% | 1 | NOT in master - look | c0bf29d Iteration 248: seed 46 processed (not small, hypervolume +6.4% |
| `ff` | 10 | 0% | 0 | NOT in master - look | cbc5db9 Iteration 254: the standard suite over all of seed 46's front  |
| `fresh43` | 126 | 98% | 4 | in master | 6b09fab Iteration 213: the handoff - PROGRESS.md's last entry holds th |
| `fresh44` | 17 | 100% | 0 | in master | 6628c73 Iteration 224: the hidden-names findings captured in GOALS.md' |
| `fresh44b` | 41 | 100% | 1 | in master | 68f504f Iteration 225: the after-seed-44 batch begun (results/pending/ |
| `fresh44c` | 46 | 100% | 1 | in master | 188e513 Iteration 227: the owner's guidance on kernel words, helpers a |
| `fresh44d` | 93 | 98% | 1 | in master | a25960f Iteration 228: the fourth after-seed-44 patch - the image load |
| `fresh45` | 20 | 100% | 0 | in master | dbdf4cb Iteration 230: seed 44 processed - small, the first (hypervolu |
| `fresh45b` | 105 | 29% | 2 | NOT in master - look | 3f77217 Iteration 231: the after-seed-45 batch begun - native terminal |
| `fresh45c` | 168 | 20% | 2 | NOT in master - look | 8553601 Iteration 233: packed names captured in GOALS.md's register, d |
| `fresh45d` | 174 | 20% | 2 | NOT in master - look | 8553601 Iteration 233: packed names captured in GOALS.md's register, d |
| `fresh45e` | 232 | 40% | 2 | NOT in master - look | a5e837d Iteration 236: a compressed image and engine captured in the r |
| `fresh45f` | 248 | 43% | 2 | NOT in master - look | 1b62ab4 Iteration 238: unused JIT stencils (50-170 bytes) and a Bloom  |
| `fresh46` | 191 | 97% | 0 | in master | bf966d9 Iteration 241: seed 46 for 10 hours (the owner) - about 8 hour |
| `fresh47` | 247 | 100% | 0 | in master | 96200bb Iteration 243: HANDOFF refreshed - the state (seed 46 running, |
| `fresh48` | 288 | 99% | 0 | in master | 4d07e3e Iteration 245: calls and returns at the fast end priced - the  |
| `fresh49` | 44 | 100% | 0 | in master | c93f65a Iteration 251: the stack header captured (left, the owner); ou |
| `fresh50` | 66 | 100% | 0 | in master | 7aba7fe Iteration 256: the routine's steps 3 and 8 as tracked tools -  |
| `fresh51` | 194 | 97% | 1 | in master | 8e430f4 Iteration 258: a gap check against the literature - LTO found  |
| `fresh52` | 218 | 100% | 1 | in master | 9250cbe Iteration 262: tools/gen-jitk.py out of master - it belongs to |
| `mo` | 312 | 98% | 0 | in master | 4adbdb2 scratch: compiler |
| `p13` | 105 | 29% | 1 | NOT in master - look | 8553601 Iteration 233: packed names captured in GOALS.md's register, d |

In all: 19 in master, 10 NOT in master - look, 2 mostly in master, changed since, 1 nothing added.

## Read (Iteration 277): no lost work

The share above was measured against today's master, which later batches
rewrote - primfirst (after seed 46) reversed the header layout of Iterations
232-234 - so "NOT in master" meant "not in master today", not "never applied".
Measured instead against the batches as applied (results/applied-after-seed4N/),
and read:

| tree | what it is | where it went |
|---|---|---|
| `ansall` | a first draft of cross.4's fast path (@-T and !-T as host cells) | superseded by `ff` |
| `ff` | cross.4's fast path, as proposed in Iteration 255 | results/drafts/crossfast.patch, line for line; not applied - the kernel workload stays a yardstick (the owner, 257) |
| `ec` | Iteration 248's tail fix reversed, beside lab/evolve/engines-check.py being written (249) | engines-check is in master; the reversal is the fault it was written against. No job, log or entry records the run |
| `base45`, `fresh45b`, `p13` | the names patch (UTF-8 names in byte headers), in the making | the after-seed-45 batch, every added line (names-after-seed45.patch the nearest) |
| `fresh45c`, `fresh45d` | the cell headers' UTF-8 fix (cellnames), in the making | the after-seed-45 batch: 96% and 100% of their lines. fresh45c's other seven are a variant (NAME-AREA, PRIOR-NFA) whose own comment names why it was left: a kernel word beside an overlay's X8 copy - HANDOFF.md's lesson |
| `fresh45e`, `fresh45f` | the after-seed-45 batch, further on (Iterations 236-238) | the after-seed-45 batch, every added line |
| `b45`, `b46` ("mostly") | the dispatch offsets; primfirst | the after-seed-45 and after-seed-46 batches (100%, 89%) |

None holds a prototype of an idea in GOALS.md's register, and none holds work
found nowhere else.
