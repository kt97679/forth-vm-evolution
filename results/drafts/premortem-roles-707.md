# The new roles' plan - its pre-mortem (prompt 16; Iteration 707)

The plan: results/drafts/new-roles-plan-705.md (chain A, the screen, running since 705; its processing; the shortlist;
chain B; the roles; the export). Prompt 16 should have fired at 705 - a plan of more than a day - and did not; run now,
while chain A runs and every finding is still cheap. One reviewer a domain, each told to find why the plan fails (one
model playing them in turn - not independent; the owner's reading is the independent one).

## 1. The reviewers

| domain | why it fails | finding | the fix |
|---|---|---|---|
| the machines | a stall on the laptop during chain A, as in seed 96's generation 0 (load 27-32, 21:56-22:25) | **real**: the ticker (chainctl.py ticker, 701's machine line) starts only for a seed run (next-run.sh: experiment mode exits before it) - chain A's laptop sessions carry no load record, and a corrupted session would pool unseen. dream and the Tegra keep load.log every 30 s. | for chain B: the ticker beside every experiment step (the batch's third patch, ticker-after-seed96); for chain A: each laptop session's readings of a fixed anchor set (the ten holders) compared session against session - a session off by more than 3 SE on most of them dropped and named |
| measurement | the screen picks a shortlist from 944 noisy readings: the best-looking at 3 rounds are partly the lucky ones (the in-run curse, again, one level down) | the shortlist's rule is final-pick.py's shortlist() - the set, the additions, each width's 5 fastest, then greedy to n | the shortlist by a margin, not a count: every design within 2 paired SE of each role's best on that role's own lines, then shortlist()'s; its size whatever that gives |
| the toolchain | process-followup.sh, final-pick.py and followup-roles.py on 944 candidates, two lists, a measure-ids pack | final-pick.py keeps the candidates' size and memory: the holders' records carry this sandbox's memory (12-16 KB high) until replaced by the measure-ids pack's - the plan says so; followup-roles.py's memory rule is 4 KB, the stopping rule's 8 KB since 702 | the replacement a step of the processing's script, not a hand edit; the memory rule 8 KB (the owner, 708) |
| the user's side (relf) | designs/ ships the self-built images (676); the cross compiler fills neither VAR-OPS nor INL-OPS (697: zeros - the fusions off in self-built images) | **real**: a new role with rtvar, rtconst or rtinline expressed would ship slower than it was measured - silently | **a gate**: a role's design ships only when its self-built image's speed equals the translator-built one's (selfhost-check.sh's speed line), or with the translator's image named as such; self-hosting phase 6 before the export, not after |
| operations | the after-seed-96 batch (arm2at) lands between chain A and chain B | x86 engines byte-identical; tos=1 GCC ARMv7 engines 0-4 bytes different - chain A's Tegra readings of those are of the old engines (their misaligned LDRD fixed up by the kernel, slowly - on the corpus only, not the timed workloads) | chain B re-measures the shortlist on the Tegra with the new engines; the ARM roles read from chain B only |
| the measure | the roles under the new size (the five programs' code counted) are not the roles relf knew | the smallest by total: 22,409 B against d180351903's 22,837 under today's measure, but by binary + image alone the old smallest may stay smaller - two answers to "the smallest" | the handoff states the measure: each role's total and its binary + image, both; relf told which changed by which |

## 2. Ceilings (what the plan can gain at most)

The size: exact - the pool's smallest 22,409 B against d180351903's 22,837 (-1.9 %); the smallest JIT design 32,661 B
against c6f1c1331b's 38,653 (-15.5 %, today's measure, results/roles-holders-705.md). The speeds: no ceiling before the
re-measures - in-run readings are 4-12 % optimistic at the fast end, and the holders' in-run numbers come from older
workloads; a role changes by speed only past 2 % at 2 SE (followup-roles.py). Memory: 108 KB in the pool against
fb0d57c8a2 (120 here - about 104-108 on the laptop): most likely no change.

## 3. "First" and "nobody"

The plan claims none.

## 4. Stopping points

1. After chain A: the x86 roles whose leader beats the next by more than 2 SE on four or more laptop sessions with
   dream agreeing - decided there; the shortlist only for the rest.
2. After chain B: every role.
3. The export: role by role, each through the self-hosting gate above - a role that fails it ships its translator-built
   image, named, rather than holding the others back.

## 5. The boring-result line

Most likely: 6 to 8 of the 10 roles change - the smallest and small-jit by the measure (exact, -1.9 % and -15.5 %), the
fastest roles at both widths and portable-fastest to new designs by 2-5 % re-measured (less than in-run's 11-20 %),
portable-arm and the knee close calls, least-memory unchanged. That is a result: the measure moved the roles more than
the search did.
