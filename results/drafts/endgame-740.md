# The endgame - from seed 97 to relf's handoff, in order (Iteration 740)

The owner (727): finish the design evolution, make sure the best designs are found, then one handoff to relf. This is
every step left, in order, with its command, what it needs and what checks it - each one rehearsed on today's tree
(the last column). The owner's decisions are marked **[owner]**; the rest is mechanical. Commands from the repository's
top, as the build user unless marked root. HANDOFF.md stays the card; this is the route.

## 1. The series (seeds 97, 98, ... on the method "from seed 97")

| step | command | checks | rehearsed |
|---|---|---|---|
| a seed's archive arrives | HANDOFF.md, "Processing a returned seed": as root the sandbox from the bundle; `setsid nohup sh lab/evolve/process-run.sh ITERATION ...`, judged at "summary"; `sh lab/evolve/process-finish.sh N ITERATION` | process-checks.sh: run-tests, validate 7 of 7, the gate, ans-check, the jail; process-finish names anything missing | 736: results/drafts/process-rehearsal-736.md - every step PASS on a stand-in |
| the stopping rule | stopping.py (in the summary): a run gains if its hypervolume beats the series' best by 1 % or an extreme by its threshold; stop when, after at least three runs on the method, the last two gain nothing | seed 97 opens the series ("nothing earlier") - so the earliest stop is after seed 99 | 736 |
| the predictions | seed 97's five (results/predictions.md, 735) scored; the next written before the next run | process-finish.sh asks | every seed |
| the next run | NEXT-RUN `seed N widths` - **[owner]** the hours | next-run.sh's own checks before it runs | 735 (seed 97's start) |

The gene votes count runs, not series: seed 97's are read with seeds 95-96's (736's note) - a new gene rare on the front
gathers removal votes early; they stay information until the rule's 11 of 12 over three runs.

## 2. When the series stops - what was held for it

| step | command | checks | rehearsed |
|---|---|---|---|
| the data layout's step 2 | `env PENDING=results/queued-layout2 RECORD=1 sh tools/batch-check.sh`, then `git apply results/queued-layout2/data-layout2-after-series.patch`, `git mv` to results/applied-layout2-ITER, `LAYOUTS=1 bash tools/build-stages.sh`, `python3 lab/evolve/evolve.py --validate` | run-tests, validate 7 of 7, the jail; data-layout-check --self-test | 738: batch-check PASS; results/drafts/data-layout2-738.txt |
| the thumb gene | `env PENDING=results/queued-thumb RECORD=1 sh tools/batch-check.sh`, `git apply results/queued-thumb/thumb-gene-after-series.patch`, `git mv results/queued-thumb/candidates-thumb-742.md results/`, `git mv results/queued-thumb results/applied-thumb-ITER` | run-tests, validate 7 of 7, the jail; every recorded id the same | 742: batch-check PASS; results/drafts/thumb-742.txt |
| the JIT designs' stack guard | `env BASE=results/queued-layout2 PENDING=results/queued-jitguard RECORD=1 sh tools/batch-check.sh`, then `git apply results/queued-jitguard/jit-guard-after-layout2.patch` - after step 2 (the same lines) | run-tests, validate 7 of 7, the jail; the JIT roles' runaways status 70 | 743: results/queued-jitguard/ORDER.md |
| anything else queued then | results/pending/ or another results/queued-*, if present (none besides queued-layout2 at 740) - each by its ORDER.md | its batch-check | - |

Applied before the roles' chains, so the chains measure every candidate's memory on the shipped layout (the records'
rss change by 0-8 KB; the in-run readings the screen uses are only for choosing candidates).

## 3. The roles chosen again (the follow-up chains, as 705-725)

| step | command | checks | rehearsed |
|---|---|---|---|
| the screen's lists | `python3 results/drafts/roles-screen-741.py results/followup-seedN-roles.md results/followup-seedN-roles-arm.md DB_N RESULTS_97 ... RESULTS_N-1 --designs designs --records results/relf-designs-718.md --also results/candidates-guard-740.md --also-arm results/candidates-thumb-742.md --iter ITER --series 'seeds 97-N'` (DB_N: seed N's database from its archive; 741: new-roles-705.py made general) -> LIST (the laptop and dream) and ARMLIST (the Tegra) | its counts; every holder on both lists | 705 (chain A); 741: results/drafts/roles-screen-741.sh - 705's record lines byte for byte |
| the guard challengers | on LIST by the screen's `--also results/candidates-guard-740.md` (not on ARMLIST - JIT designs); keep the file where it is: dream's and the Tegra's lines take genomes for `--also` ids only from results files, results/candidates-*.md and results/relf-designs-*.md | in LIST; measure-ids.py gives their laptop numbers; the remote sample's log says "N of N asked for by id" | 740: results/drafts/guard-challengers-740.sh; 741 |
| the thumb variants | on ARMLIST alone by the screen's `--also-arm results/candidates-thumb-742.md` (the six JIT-free roles with thumb=1: their ARM engines Thumb-2, their x86 builds their parents' bytes); after the chain `python3 results/drafts/thumb-pairs-742.py results/chain-followupNN-... results/candidates-thumb-742.md` - each against its parent on the Tegra, paired by session, the 2 % rule; per role, Thumb-2 ships when the pair shows no loss (743: decided - "Decided" below) | the Tegra line's sample bundles the clang variants' Thumb-2 engines; thumb-pairs-742.py --self-test | 742 |
| chain A (the screen) | NEXT-RUN: `experiment measure-ids.py --ids LIST`, then `loadtest.py --ids LIST --rounds 10` repeated; REMOTES: dream and the Tegra (`--also @FILE` - the ids' genomes from results/evolve-*-seed*.md, results/candidates-*.md and, since 740, results/relf-designs-*.md: a design in none of them is left out) - **[owner]** the hours; the predictions before it | the chain's checks (tests, validate, jail); each remote sample.log's "N of N asked for by id" | 705, 713; 740 (the lookup's two gaps) |
| its processing | `HANDOFF=results/handoff-relf-726.md PRED=ITER sh lab/evolve/process-followup.sh NAME ITERATION ROLES` (ROLES: fast64=..,fast32=..,allround=..,smalljit=.. and the six portable) | followup-roles.py: each role against its holder by the rule - 1 % smaller, no class 2 % slower, memory within 8 KB; a speed role's challenger 2 % faster at 2 SE | 721 (chainD-rehearsal-721.sh), 740 (followup-roles.py on the challengers) |
| chains B, C, D as needed | a shortlist of the undecided (chainC-list-714.py's way), the smallest JIT design's band (pool-sizes.py) | the same | 713-725 |
| the decisions | results/new-roles-ITER.md: each role kept or changed, every near design kept on record; **[owner]** the trades (a design better on one criterion, worse on another) | - | 718 |
| the guard challengers' outcome | fast64 and fast32 by the rule (they must be 2 % faster; the gain is on the interpreted workloads only, so it may not reach it); small-jit's is larger by 0.75 %, so a trade at best - kept on record (743: decided); the gap itself closed for every JIT design by results/queued-jitguard | - | 739, 743 |
| the records | results/relf-designs-ITER.md - the ten, one record a line, master's sizes and the laptop's memory (the chain's measure-ids records) | export-designs.py reads it | 718 |
| the gate and the rage check | a chain carrying `experiment rage-designs.py` (the Tegra: the GCC designs' forth-arm, their self-built images) and lab/evolve/selfhost-speed.py (the laptop: each self-built role against its translator-built image, 5 alternations of 10 rounds, both widths; above 1.02 it ships translator-built) - **[owner]** the hours | rage-designs.md PASS; selfhost-speed.md's ratios | 720-726 |

## 4. The final build (results/drafts/ship-rehearsal-737.sh's order)

| step | command | checks | rehearsed |
|---|---|---|---|
| the packages | root: `CROSS=1 sh tools/setup-sandbox.sh` (lld, qemu-user, the armhf libc and libgcc) - before phase 1 | - | 737: without them lld found no ARM libgcc |
| phase 1 | `sh results/drafts/roles-build-718.sh 1 . results/relf-designs-ITER.md NAMES` - the stages, validate, export-designs.py, export-arm.py (the clang designs) | /tmp/fz/status: build, validate 7 of 7, export, export-arm | 737 |
| the GCC designs' ARM | root: `apt-get install -y gcc-arm-linux-gnueabihf` (gcc-multilib goes); `python3 lab/evolve/export-arm.py /tmp/fz/designs RECORDS NAMES --gcc arm-linux-gnueabihf-gcc`; root: `apt-get install -y gcc-multilib` | the lab's bytes, running under qemu-arm | 737 (the clang step must come first) |
| phase 2 | the gate's verdicts into a file (NAME:REASON lines joined by `|`), then `TRANSLATOR="$(cat FILE)" sh results/drafts/roles-build-718.sh 2 . RECORDS NAMES` - selfhost-ship.sh, the designs' make, test, selfhost, 32, libc, pack-designs.py | test ok, selfhost byte for byte, pack-designs 20 of 20 right | 737 (from a file: the reasons hold quotes) |
| designs/ | the export into designs/ with designs/README.md's table - `python3 results/drafts/designs-table-741.py results/relf-designs-ITER.md NAMES CHAINDIR=LABEL ...` (the chains' readings, results/chain-followupNN-*, in order of preference; 741: designs-table-718.py made general) - and designs/TRANSLATOR-BUILT | designs-table-741.py exits 1 for a design no chain measured; relf-handoff-739.py asserts every row against its record | 718; 741: results/drafts/designs-table-741.sh - today's table byte for byte |
| the package | pack-designs.py's directory tarred: forth-vm-evolution-designs-iterITER.tar.gz; its checksums results/drafts/designs-sha256-ITER.txt | rebuilt byte for byte from the repository | 718, 726 |

## 5. The handoff

| step | command | checks | rehearsed |
|---|---|---|---|
| the notes | results/drafts/handoff-notes-ITER.md - "## Changed" (the series 97-N and its genes, the layout's two steps, the roles' chains), "## For relf" (the JIT stack gap's outcome; anything relf should know), "## History" (one paragraph) - results/drafts/relf-handoff-739-test.md is the form | - | 739 |
| the document | `python3 results/drafts/relf-handoff-739.py --iter ITER --records results/relf-designs-ITER.md --previous results/handoff-relf-726.md --package forth-vm-evolution-designs-iterITER.tar.gz --notes results/drafts/handoff-notes-ITER.md --sha results/drafts/designs-sha256-ITER.txt > results/handoff-relf-ITER.md` | its asserts: every row a record, sizes and memory the record's, the JIT the expression's | 739: 726's table and genes byte for byte; a swapped role found |
| delivered | the bundle, the package and the handoff to the owner, who sends them to relf - **[owner]**; the held iter726 package and results/handoff-relf-726.md superseded (the history) | make-bundle's handoff check | every iteration |

## 6. After

The article (the owner, 636: the last step, once the search has ended, the designs are frozen and relf has them) -
article/article-en-draft.md and article-ru-draft.md, every figure recomputed on the final roles.

## Found by rehearsing this route (740)

- The guard challengers under another file name: dream and the Tegra left all three out (no genome) - hence
  results/candidates-guard-740.md.
- Two holders, 9b15ba26f7 (fastest-x86-64) and 11f956db93 (fastest-x86-32), in no file xcheck.py read - chains A-C found
  them in the laptop's seed 96 database only; after the series the follow-up would have measured neither on dream and
  followup-roles.py refused. Fixed: xcheck.py reads results/relf-designs-*.md (results/applied-xcheck-740).

## Decided (743) - the owner: "for open questions - I don't have strong opinions, please continue as you think is most reasonable"

- **Run hours**: the series' seeds 16 hours each, as seed 97 (the stopping rule judges at matched generations, so the
  length only sets how far each run gets); a chain's hours as its content needs, said before it starts.
- **Trades in the roles' chains**: 718's way (the owner then: "the most reasonable way, not losing any good designs") -
  each role by the chains' rule (1 % smaller, no class 2 % slower, memory within 8 KB; a speed role's challenger 2 %
  faster at 2 SE); a design better on one criterion and worse on another keeps the holder and is kept on record.
- **The JIT stack gap**: no shipped role dies silently - the slim guard for every JIT design without the gene
  (results/queued-jitguard, applied after step 2); the guard gene's variants still compete by the rule (small-jit's can
  only be a trade, larger by 0.75 %, so it stays on record).
- **Thumb-2**: per ARM role, its thumb variant ships when results/drafts/thumb-pairs-742.py shows no loss on the Tegra (2 %
  slower at 2 SE); a loss, or no readings, keeps A32. A shipped variant becomes the role's record (a new id, the same x86
  bytes).
- **s1-sod16's ARM reach**: known (tools/arm-cross-check.py's KNOWN - results/applied-known-743), no design affected.
- **Not this round**: the machine outliner, the tag's tables as const data, a learned bytecode grammar - a later search's.
- **Unchanged**: relf's handoff and the package go once, at the end; the article after it.

## What is not settled yet

- How many seeds: the stopping rule's (at least 97-99).
- Each run's and chain's hours - the owner's.
- Whether any role changes - the chains'; the guard challengers' and the thumb variants' outcomes - the rules above (743).
- The rage check needs the Tegra; the gate needs the laptop; chain A needs dream too.
