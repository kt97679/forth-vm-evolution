# Results - every measurement and analysis, indexed

One line each, by topic: the file, then its own title. Each per-run record names the
machine and run it came from. `tools/handoff-check.py` fails when a document here is
missing from this index (README.md, "Documents", indexes everything else).

## The evolution, by subject

Each subject oldest first; a script or patch beside the document it made.

### Each run's records - its report, the comparisons, the ledgers

- `evolve-amd-ryzen-7-pro-8840hs-seed4b.md` - Evolution on the Ryzen 7 PRO 8840HS - seed 4 again: a replicate.
- `compare-fronts-amd-ryzen-7-pro-8840hs.md` - every comparison session: the fronts of all runs measured again together, judged by the five measures.
- `predictions.md` - the predictions written before each run, then scored.
- `progress-by-run.md` - every run's extremes, for the progress charts (lab/evolve/progress-table.py).
- `evolve-amd-ryzen-7-pro-8840hs-seedN.md` - each run, seeds 1-76 (none for seed 48, the owner's choice; Iteration 384 brought this line from 47): the verdict and the facts, then the pack's report with every front design's genome (the gate, ans-check and the other tools read genomes from these).
- `seed63-rules.md` - Seed 63's decisions, the rules written before its results (Iterations 430-431, adopted): ten rules and the gene rule - a gene out only after three runs unused, no front design depending on it, frozen off for a run first.
- `gene-votes.md` - The gene votes, run by run (from Iteration 432): each gene's four removal votes a run - under 10% of the front, in none of its fastest, smallest, best-Q tenths - appended at each processing from seed 63 on; results/seed63-rules.md says how they count.
- `model-usefulness.md` - Which other model helped, one line per answer (Iteration 542): answers pasted one at a time, each assessed on arrival.
- `progress-true-fronts.md` - every run's extremes on its true front, seeds 53-75 (Iteration 553; results/drafts/truefronts-tables-550.py from truefronts-seed75.md): progress-by-run.md's table on the true fronts.
- `truefronts-seed75.md` - every seed pack's true front, seeds 53-75, from each run's records (lab/evolve/truefronts.py in seed 75's chain; Iteration 553): the table and every front's points - the source of the true-front tables and charts.
- `stopping-series.md` - GOALS.md's stopping rule, run by run: each run's fixed-box hypervolume and four extremes, a method line opening each series (lab/evolve/stopping.py appends; Iteration 554, applied at 555).

### Each run's front checked on other machines (xcheck-seedN)

- `xcheck-seed56.md` - The first run checked on four machines (Iteration 354): the Tegra's first native run (ARMv7, Spearman 0.944), dream.lan at 64 bits, at 32, and the same designs at 64 - the skew the width's, not the machine's.
- `xcheck-seed57.md` - The checks of seed 56's front during seed 57 (Iteration 378): dream 64-bit Spearman 0.980; at 32 bits 0.713, the same designs at 64 bits 0.949 - the width's skew again; the Tegra 0.881.
- `xcheck-seed58.md` - The checks of seed 57's front during seed 58, and seed 57's rejected designs (Iteration 384): the Tegra Spearman 0.973, dream 64-bit 0.959, 32-bit 0.875; no rejected design faster on any host than the front's fastest (item 4d); three Tegra link failures (regpin=1 with lto=1).
- `xcheck-seed59.md` - The checks of seed 58's front during seed 59 (Iteration 398): dream 64-bit 0.959/0.963, 32-bit 0.651, the Tegra 0.709 (against the laptop's 64-bit speeds - open item 0g); no rejected design faster; the probes: copies in a second, the Tegra's wait its own build.
- `xcheck-seed60.md` - The checks of seed 59's front during seed 60 (Iteration 406): dream 64-bit 0.941/0.721, 32-bit 0.370; the Tegra's six failures named - the assembler's bad immediate offset, every one alignhot 64 (item 0d).
- `xcheck-seed61.md` - The checks of seed 60's front during seed 61 (Iteration 425): dream 0.863 (default), 0.910 (64-bit), 0.929 (32-bit); the Tegra 0.991, all 16 built - none of seed 60's front carries alignhot above 1.
- `xcheck-seed62.md` - The checks of seed 61's front during seed 62 (Iteration 433): dream 0.943 (default), 0.958 (64-bit), 0.945 (32-bit); the Tegra 0.847, all 16 built; two rejected designs faster than the front's fastest there.
- `xcheck-seed63.md` - The checks of seed 62's front during seed 63 (Iteration 441): dream 0.723 (default), 0.932 (64-bit), 0.834 (32-bit); the Tegra 0.912; the Tegra's rebuild test - all 7 asked for built, item 0d closed.
- `xcheck-seed64.md` - The checks of seed 63's front during seed 64 (Iteration 443): dream 0.707 (default), 0.946 (64-bit), 0.753 (32-bit); the Tegra 0.771; cf524f4c20, rejected by seed 63's selection, faster than the front's median on every host and first across the machine classes (mean 0.409).
- `xcheck-seed65.md` - The checks of seed 64's front during seed 65 (Iteration 449): dream 0.959 (default), 0.937 (64-bit), 0.837 (32-bit); the Tegra 0.857 over 7 - only 3 of seed 64's front are GCC without the JIT, all the Tegra builds as themselves.
- `xcheck-seed66.md` - The checks of seed 65's front during seed 66 (Iteration 454): dream 0.963 (default), 0.977 (64-bit), 0.809 (32-bit); the Tegra 0.818 (16); ad0975a72e, rejected by seed 65's selection, faster than the front's median on every host.
- `xcheck-seed67.md` - The checks of seed 66's front during seed 67 (Iteration 458): dream 0.962 (default), 0.987 (64-bit), 0.833 (32-bit); the Tegra 0.618 (16).
- `xcheck-seed68.md` - The checks of seed 67's front during seed 68 (Iteration 464): dream 0.966 (default), 0.963 (64-bit), 0.946 (32-bit).
- `xcheck-seed69.md` - The checks of seed 68's front during seed 69 (Iteration 487): dream at three builds (0.963 default, 0.862 at 32 bits, 0.863 at 64) and the Tegra (0.965, 16 designs); against the laptop's 32-bit speeds 0.928 and 0.881.
- `xcheck-seed70.md` - The checks of seed 69's front during seed 70 (Iteration 498): dream 0.941 (default), 0.935 (32-bit), 0.959 (64-bit); the Tegra 0.929 (8 designs); against the laptop's 32-bit speeds 0.893 and 0.800.
- `xcheck-seed71.md` - The checks of seed 70's front during seed 71 (Iteration 516): dream 0.804 (default, 24), 0.969 (32-bit), 0.966 (64-bit); the Tegra 0.607 (7).
- `xcheck-seed72.md` - The checks of seed 71's front during seed 72 (Iteration 520): dream at three builds and the Tegra.
- `xcheck-seed73.md` - The checks of seed 72's front during seed 73 (Iteration 544): dream 0.870 (default, 24), 0.931 (32-bit), 0.893 (64-bit); the Tegra 0.882 (16).
- `xcheck-seed74.md` - The checks of seed 73's front during seed 74 (Iteration 549): dream 0.977 (default, 24), 0.974 (32-bit), 0.984 (64-bit); the Tegra 0.856 (16).
- `xcheck-seed75.md` - The checks of seed 74's front during seed 75 (Iteration 553): dream 0.910 (default, 24), 0.906 (32-bit), 0.945 (64-bit); the Tegra 0.762 (8).
- `xcheck-seed76.md` - The checks of seed 75's front during seed 76 (Iteration 555): dream 0.972 (default, 24), 0.952 (32-bit), 0.980 (64-bit); the Tegra 0.832 (16).
- `xcheck-seed77.md` - The checks of seed 76's front during seed 77 (Iteration 560): dream 0.957 (default, 24), 0.951 (32-bit), 0.968 (64-bit); the Tegra 0.921 (16).
- `xcheck-seed78.md` - The checks of seed 77's front during seed 78 (Iteration 563): the Tegra 0.926 (16); no dream report in this chain.
- `xcheck-seed79.md` - The checks of seed 78's front during seed 79 (Iteration 565): dream.lan-prebuilt 24 designs measured on both: Spearman 0.890; dream.lan-prebuilt32 30 designs measured on both: Spearman 0.869; dream.lan-prebuilt64 30 designs measured on both: Spearman 0.931.
- `xcheck-seed80.md` - The checks of seed 79's front during seed 80 (Iteration 566): dream.lan-prebuilt 24 designs measured on both: Spearman 0.877; dream.lan-prebuilt32 30 designs measured on both: Spearman 0.911; dream.lan-prebuilt64 30 designs measured on both: Spearman 0.939.
- `xcheck-seed81.md` - The checks of seed 80's front during seed 81 (Iteration 568): dream.lan-prebuilt 24 designs measured on both: Spearman 0.891; dream.lan-prebuilt32 30 designs measured on both: Spearman 0.919; dream.lan-prebuilt64 30 designs measured on both: Spearman 0.928; rage.lan-native ?.
- `xcheck-seed82.md` - The checks of seed 81's front during seed 82 (Iteration 569): Spearman with the laptop - dream 0.818 (24), 0.864 and 0.892 (30 at 32 and 64 bits); rage 0.143 (8, a narrow band).
- `xcheck-seed83.md` - The checks of seed 82's front during seed 83 (Iteration 572): Spearman with the laptop - dream 0.989 (24), 0.932 and 0.993 (30 at 32 and 64 bits); rage 0.143 (6, a narrow band).
- `xcheck-seed84.md` - The checks of seed 83's front during seed 84 (Iteration 575): Spearman with the laptop 0.969, 0.962 and 0.984 on dream (prebuilt, 32, 64), 0.935 on rage (16, clang-built, the host busy).
- `xcheck-seed85.md` - The checks of seed 84's front during seed 85 (Iteration 576): Spearman with the laptop 0.983, 0.938 and 0.972 on dream (prebuilt, 32, 64), 0.956 on rage (14, clang-built).
- `xcheck-seed86.md` - The checks of seed 85's front during seed 86 (Iteration 582): Spearman with the laptop 0.983, 0.836 and 0.983 on dream (prebuilt, 32, 64), 0.918 on rage (11, clang-built); dream's 41: the bred lead the laptop's.

### The batches of patches applied after the runs

- `applied-after-seedN/ORDER.md` - each batch of patches applied after a run: the order, and how each patch was tested.
- `applied-after-seed68/` - the after-seed-68 batch, applied at seed 69's processing (Iteration 487): the JIT at 32-bit x86 (engine and lab), the stencil check; ORDER.md with how each patch was tested and its rebases (475-486, the engine patch repaired at 486); batch-check PASS on e5c6239.
- `applied-after-seed70/` - the after-seed-70 batch, applied at seed 70's processing (Iteration 498): six patches - more JIT coverage (ABORT", word ends, depth), 2>R in place, the new genes at 32 bits (and CELL+/CELLS by the cell), jitrp.
- `applied-after-seed71/` - the after-seed-71 batch, applied at seed 71's processing (Iteration 516): six patches - nocase retired, jithelp and jitre retired, jitfuse and its enabling, the MARKER fix (jit_k's signature) with its test.
- `applied-after-seed72/` - the after-seed-72 batch, applied at seed 72's processing (Iteration 520): jitexec's JIT table (its rows after the real operations - 585 KB less) and the memory objective without the applications' own data; ORDER.md with how each was tested.
- `applied-after-seed73/` - the after-seed-73 batch, applied at seed 73's processing (Iteration 544): six patches - adaptive operator selection, the evolver's bug-hunt fixes (first_front by dominates(): reports show the true front), one round first.
- `applied-after-seed74/` - the after-seed-74 batch, applied at seed 74's processing (Iteration 549): five patches - fail32 learns cpt16's reach, the clock test takes the chain's perf hold, the progress table's header and front, truefronts.py (every seed pack's true front).
- `applied-after-seed75/` - the after-seed-75 batch, applied at seed 75's processing (Iteration 553): two patches - truefronts.py's reported column; the processing tools, draft-results.py and process-checks.sh.
- `applied-after-seed76/` - the after-seed-76 batch, applied at seed 76's processing (Iteration 555): two patches - the stopping rule mechanical (stopping.py, the ledger stopping-series.md); the clock test's cost a design and s6 both pay (cputime's user and system parts).
- `applied-before-seed77/ORDER.md` - the before-seed-77 batch (its two patches beside it), applied before seed 77 started (Iteration 556): two patches - every freeze that still has code lifted; the stopping rule's extremes from every alive design.
- `applied-after-seed77/` - the after-seed-77 batch, applied at seed 77's processing (Iteration 560): the JIT patches every copy of a value hole (seed 76's corpus deaths); the stencil check reads a design's own flags; lifted.py; how each was tested.
- `applied-after-seed78/` - the after-seed-78 batch, applied at seed 78's processing (Iteration 563): a processing in three commands (process-run.sh, process-finish.sh, setup-sandbox.sh); the stopping rule matched by generation - each run at its last generation against each earlier one there (562).
- `applied-after-seed79/` - the after-seed-79 batch, applied at seed 79's processing (Iteration 565): deaths-check.py names the scale-1 reach limit; gene-narrow.py; the random-search baseline ("random"); lifted.py as built.
- `applied-after-seed81/` - the after-seed-81 batch, applied at seed 81's processing (Iteration 568): jitscan, ccflags, design, bar (ORDER.md says what each does).
- `applied-after-seed83/` - the after-seed-83 batch, applied at seed 83's processing (Iteration 572): armrt, prebuiltarm, ragecheck (ORDER.md says what each does).
- `applied-after-seed84/` - the after-seed-84 batch, applied at once after seed 84's chain failed (Iteration 574): retired (ORDER.md says what it does).
- `queued-consolidation/ORDER.md` - consolidation's retirement batch, queued until after the final pick (Iteration 583): fsys45 - fsys levels 4-5 retired, batch-check PASS; ORDER.md says when and how it is applied.

### The processing checklists

- `drafts/seed71-checklist-505.md` - Seed 71's processing, written before its results (Iteration 505): what compares across the speed break (sizes, memory, within-run measures, appbench's ratios) and what does not (speed, best Q, hypervolume); the predictions it settles; the after-seed-71 batch.
- `drafts/seed73-checklist-532.md` - Seed 73's processing, written before its results (Iteration 532): what compares (memory again the six's), the true front beside the reported, prediction 518 (jitexec's first fair run), the batch, seed 74's line with the clock test.
- `drafts/seed74-checklist-545.md` - Seed 74's processing, the checklist (Iteration 545): the predictions due with their numbers, the hypervolume, the clock test, the votes, the batch, seed 75's line.
- `drafts/seed75-checklist-550.md` - Seed 75's processing, the checklist (Iteration 550).
- `drafts/seed77-checklist-557.md` - Seed 77's processing, the checklist (Iteration 557): the new series' line, prediction 555 on the tolerance front, prediction 556 by lifted.py, the deaths to expect, the clock test's cost both pay.
- `drafts/seed78-checklist-561.md` - Seed 78's processing, the checklist (Iteration 561): the batch by hand once, then process-run.sh; the stopping rule's bar by how far seed 78 goes.
- `drafts/seed79-checklist-563.md` - Seed 79's processing, the checklist (Iteration 563): the stopping rule's third run - the confirmation run's line if it stops.
- `drafts/seed80-checklist-565.md` - Seed 80's processing, the checklist (Iteration 565): the stopping rule's fourth run; seed 79's gain past seed 77's reach; the Tegra.
- `drafts/seed81-checklist-566.md` - Seed 81's processing, the checklist (Iteration 566): the fifth run, a stop if it gains nothing; the confirmation founders; the Tegra's --also test.

### Faults found, and their fixes

- `drafts/jit-loop-crash.md` - A JIT fault seed 52 found (Iteration 310): two designs die in the corpus's loop tests; the trigger narrowed to jit with folds, ops10, rtloop and tag2; the genomes.
- `drafts/convert-align-death.md` - A converter death seed 54 found (Iteration 333): "call target 1390 not 8-aligned", one design of 41,406 - not yet looked into; its genome.
- `bfind32-fault-399.md` - Open item 0f found (Iteration 399): bf_walk's signature in the cell type, three characters compared at 4-byte cells - seed 59's 34 dead at 32 bits live with the fix (pending, after seed 62); engines-check's bfind variants had built no walk; bfind inert in every TOS design.
- `drafts/corpus-deaths-555.md` - Two designs of seed 76 that died on the corpus, reproduced (Iteration 555): a wrong output here, deterministic - an open correctness issue in a JIT combination; their genomes and the steps.
- `drafts/jitexec-alignhot-566.md` - Seed 80's two deaths (Iteration 566; the cause 567): jit_scan's 160-byte window cut st_execute under -falign-*=64; alignhot built where express() drops it - fixed in the after-seed-81 batch.
- `drafts/corpus-deaths-bisect-556.py` - The bisect behind it: the two designs and their parent, one gene at a time (Iteration 556).
- `drafts/seed84-failed-574.md` - Seed 84's chain failed 5 hours in (Iteration 574): seeds 70-71's retired genes (jithelp) broke crossover() after generation 0; generation 0 by database, the remote checks, what the rerun costs.
- `drafts/retired-genes-574.py` - The fix tested on the 3,489 genomes of seeds 70-83's results files (Iteration 574): crossover, mutate and borrow, the ids unchanged, carry_pool and its guard.
- `drafts/body-size-drift-576.md` - Seed 85's 55 "body size drift" deaths (Iteration 576): the scale-0 call reach where varcall and doesfar exempt a design from reach_lethal() - no fault, no change.
- `drafts/body-size-drift-576.py` - The count behind it: the drift deaths, the gene values all of them share, and how every design with those values ended.
- `drafts/fastend-icount-579.md` - Seed 84's fast-end lead counted (Iteration 579): 1.4% fewer instructions than its founders, all on corpus; the rest of the 4.5% idle lead the laptop's time per instruction.
- `drafts/fastend-icount-579.py` - The count behind it: valgrind cachegrind on the seven selection workloads, each design against s6; its output fastend-icount-579.jsonl and .s6.json.
- `drafts/retire-report-579.md` - Consolidation's retirement read under 578's rule (Iteration 579): every gene value against the pooled true front of seeds 77-84 - 17 unused, the thin ones named.
- `drafts/retire-report-579.py` - The report behind it: confirm.py's pool, its true front, each gene value expressed (a live gene's 0 put back); markdown on stdout, nothing changed.
- `drafts/fastend-knockout-581.py` - One gene switched in seed 84's fast designs, counted (Iteration 581): guard gives 8-10% fewer instructions on corpus, jitimg 0.3-0.5%.
- `drafts/fastend-icount-581-32.jsonl` - The 32-bit fast end counted (Iteration 581): seed 84's 3 bred and the pool's 4, under setarch -L; its s6 in fastend-icount-581-32.s6.json.
- `drafts/reach-scale2-581.md` - Why only threads=2 reaches the scale-2 limit (Iteration 581): the near DOES> form's reach, the dictionary grown at run time by 128-chain wordlists.
- `drafts/reach-scale2-581.py` - The rebuilds behind it: seed 85's scale-2 kernel deaths with threads 0-3, then with both far forms, at scale 3 and at scale 1.

### The JIT

- `jitret-404.md` - The gene jitret (Iteration 404, pending patch 8): the JIT's EXIT as pop and jmp, not ret - here ackermann -26%, fib unchanged, bubble and loop +6-9%, the six about 3% faster; the search weighs it from seed 63.
- `drafts/jit-i386-460.md` - The JIT at 32-bit x86, a feasibility study and a working prototype (Iteration 460; the patch beside it): i386's convention as ARM's (one 64-bit state, regparm(2) - eax and edx both ways), 4-byte holes, a variable's alignment bug found.
- `drafts/jitrp-465.md` - jitrp, the JIT's return-stack pointer in a register - a prototype (Iteration 465; the patch beside it): each return-stack stencil three instructions shorter.
- `drafts/jitapps-471.md` - What the JIT leaves on the applications, and why (Iteration 471; lab/evolve/jitapps.py): on seed 68's fast design the JIT leaves 37-94% of the applications' dispatches to the interpreter.
- `drafts/jit-pairs-506.md` - The JIT's operation pairs over the seven selection workloads, pricing super-stencils (Iteration 506): 41% of dispatched pairs in straight-line code, the top 25 a quarter; I +, DUP I, + XOR lead; a few percent to win - a literal-into-operation gene proposed first.
- `drafts/jit-genes-517.md` - Why the search ignored three JIT genes (Iteration 517): jitexec cost 586 KB - its table rows past T2_JIT, a bug (fixed for after seed 72: 2,752 bytes for -13.7% on the applications); jitdoes buys nothing on the selection; jitcfa drifts.
- `drafts/jit-sweep-558.md` - The JIT's stencils across the compiler genes (Iteration 558): 332 flag sets, none unsafe; the only repeated holes st_callx (tracer) and st_execute (tracer with nocrossjump) - both patched by the after-seed-77 batch.
- `drafts/jit-sweep-558.py` - The sweep's script.
- `drafts/jitscan-test-567.py` - the after-seed-81 batch's JIT designs on the corpus, jit-diff and sim16 (Iteration 567): right at 512 at both widths, the first two wrong at 160.
- `drafts/stencil-window-567.py` - jit_scan's window against GCC's stencils over 84 flag sets (Iteration 567): the longest 146 bytes at 32-byte alignment, 242 at 64; 17 sets cut at 160, none at 512.
- `drafts/seed73-front-544.py` - Seed 73's true front against its reported one, the JIT genes' shares (prediction 518), the extremes and the 32-bit failures by encoding (Iteration 544).
- `drafts/jithelp-wip.patch` - Helper calls in progress (Iterations 344-345), against the pending batch: st_callc, h_place, h_parse, COUNT's entry.
- `drafts/jitre-wip.patch` - Interpreter re-entry in progress (Iteration 346), against the pending batch and jithelp-wip.patch: builds; crashes on its first run - to bisect.

### Across machines and widths

- `xcheck-dream-seed53.md` - The first remote check (Iteration 320): seed 52's front on dream.lan (i7-6700), the laptop's binaries - Spearman 0.959, the laptop's six fastest its first six; the JIT designs' lead over s6 smaller there.
- `xcheck-dream-seed54.md` - The second remote check (Iteration 333): seed 53's front on dream.lan - Spearman 0.941, the laptop's six fastest ranked 3 4 2 10 1 5 there.
- `xcheck-dream-seed55.md` - The first check at both widths (Iteration 334): dream.lan 64-bit Spearman 0.940; 32-bit x86 at 4-byte cells 0.694 - the laptop's six fastest interpreted designs 8th-13th there: the skew the owner feared.
- `drafts/two-width-selection.md` - Selecting at both widths, the skew in the evolution itself (Iteration 335, a draft): a design's interpreter measured at 4-byte cells as a second speed objective; the decisions for the owner.
- `drafts/skew-32.md` - Why designs lose at 32 bits (Iteration 352): thirty of seed 55's front at both widths and gene knockouts - tag2 and fsys 3 the causes, compiler's gain 64-bit only; the data in drafts/skew-32-*.jsonl.
- `drafts/cross-machine-weighing.md` - Weighing results across machines (Iteration 376, a proposal for the owner): what the checks show, the blind spot (only the laptop's front is checked elsewhere), and a policy for choosing designs good on every class of machine.
- `fail32-400.md` - Every 32-bit failure of seed 58 classified (Iteration 400): 819: 745 bugs - bfind (418) and the tail engine built for x86-64 and compiled for i386 (327) - and 74 clang tail engines without musttail.
- `xcheck32-402.md` - Item 0g (Iteration 402): xcheck --report --laptop32 - the 32-bit hosts against the laptop's own 32-bit speeds (the Tegra 0.709 to 0.857; dream 0.651 to 0.650, the machine not the width); the Tegra's eight link failures all fsys on.
- `drafts/xcheck-agreement-546.md` - Why the cross-machine checks agreed less on seed 72's front (Iteration 546): mostly the sample; the machines order the fast JIT designs differently; the fast end is a band.
- `drafts/xcheck-agreement-546.py` - The analysis behind it, from a chain's remote measurements and the checked run's records (Iteration 546).
- `drafts/tegra-cross-568.py` - The Tegra's clang designs cross-built on the laptop (Iteration 568): clang for ARMv7 with lld and the armhf C library - corpus, fib and apps identical under qemu-arm; the engine 347,688 bytes with static glibc.
- `drafts/x86-identity-570.py` - The after-seed-83 batch changes nothing on x86 (Iteration 570): s6 and 13 of seed 82's front at 8- and 4-byte cells, engines and images byte-identical in master and the batch.
- `drafts/prebuiltarm-e2e-570.sh` - Rage's prebuiltarm check end to end on one machine (Iteration 570): remote-checks.sh with ssh/scp stand-ins - 10 clang designs cross-built (74 KB), s6 and 2 GCC designs built on the host.

### The search - its method, genes and prices

- `drafts/iploop-plan.md` - The IP-update loop form: three explanations of the evolved designs' lower IPC, and the laptop measurement that decides between them before anything is built (Iteration 295).
- `drafts/runner-protocol.md` - The runner's protocol, the owner's requirements as a specification (Iterations 302-303): one command, one archive with every log, a clean stop, recovery at every start.
- `drafts/next-genes.md` - The search for the genes after seed 54 (Iteration 323): price.py on seed 53's fastest interpreted designs - calls and returns the largest share, their genes in place, pairs diminishing; next, jitleft.py - what the JIT leaves to the interpreter.
- `relf-pairs-realistic.md` - relf's realistic shell script by instruction and by adjacent pair (Iteration 358): VAR@ 15.2 %, VAR@ VAR@ 4.2 %, VAR@ + 3.1 %; relf's 64 one-byte opcodes (A15) as the constraint.
- `relf-patches/README.md` - Patches for relf from this lab (Iteration 360): each with its gate, its dispatch count and its time; the first, 0= ?BRANCH fused.
- `drafts/relf-gene-classes.md` - This lab's genes by what relf would pay to adopt one (Iteration 363): C engine only, opcode set or image format, kernel words, x86-64 JIT.
- `drafts/supers-tag2.md` - The supers gene in tag-2 designs (Iteration 367): its pool misnamed since Iteration 66 (codes read as plain opcodes), the gene inert in ~97% of the fronts (its slots taken by format-10 words); the fix pending after seed 57.
- `drafts/gene-usage-53-56.md` - What the search chose (Iteration 372): every gene on the fronts of seeds 53-56 (722 designs) - never on (msc, scale, tail), rarely on, on everywhere; the evidence for the simplicity review after seed 57.
- `supers-knockout-seed58.md` - Superinstruction pairs knocked out, seed 58's tag-2 designs (Iteration 385; HANDOFF item 1): 0.9% fewer dispatches at the median (to 2.5%), -1,024 to +719 bytes - they buy something, so the gene stays; 2 of 19 carry pairs that never execute.
- `review-methodology-386.md` - A review of the methodology, workflows and logic (Iteration 386): nocarry is not from scratch (two evolved founders, two thirds of seed 58's ancestry); the fast end's in-run speeds ~10% optimistic; the verdict's 2% bars inside the noise.
- `verdict-audit-388.md` - The verdicts audited (Iteration 388): all 16 sessions since the five-measure rule rebuilt and recomputed from each CPU alone - the CPUs agree in 14, the two that differ (seeds 50, 51) decided nothing.
- `convergence-seed58.md` - Is the search stuck in a local minimum? (Iteration 392, the owner's worry): five sources mapped to their tests, and seed 58 from inside - diversity holds and rises, the gains continue to generation 130: no collapse.
- `tools-audit-394.md` - The tools audited after the context-economy changes (Iterations 394-395): nothing downstream broken; batch-check.sh's exit status and kept clone fixed and tested; compare-fronts.py run end to end.
- `drafts/gene-usage-53-59.md` - Seed 59's front against seeds 53-58's (Iteration 403): msc, scale, tail still never on; rtloopall, escape, supers, guard up to 56 points more, tos 39 fewer - a run without the carry ends elsewhere.
- `rehearsal-405.md` - The after-seed-62 batch rehearsed (Iteration 405): 13 of seed 59's front designs with its genes, and a short tag2 run at both widths (330 designs) - every new mechanism alive; one new 32-bit failure, GCC's t2call tail call on the two-bit tag, fixed as patch 9.
- `drafts/gene-usage-53-60.md` - The genes on seeds 53-60's fronts together, 1,431 designs (Iteration 408): eight on in every design, msc, scale and tail in none.
- `drafts/simplicity-proposal-408.md` - The simplicity review, a proposal (Iteration 408): freeze bytehdr, doesfar, thinhdr, varcall, bss and lean; remove msc and scale; tail after seed 63.
- `drafts/price-410.md` - Two levers priced on seed 60's front (Iteration 410): handler replication for calls and returns at most 0.4-1.6% - not built; the register machine's bound, corrected at 411 (stackops.py's opcode names were wrong on the two-bit tag): 7-46% a workload.
- `drafts/preflight-414.md` - The processing tools tried before the runs need them (Iteration 414): spread on seeds 58-60 (466 s; 59 and 60 13.6 points apart in genes, within 6% in speed), curse on seed 60 (1.066, seed 58 1.112), the batch's application dry-run.
- `bigprog-416.md` - Programs past 4 MB (Iteration 416): plain CV8's call (2 MB), link (4 MB) and DOES> (2 MB) reaches extended - FAR,, a fourth link form, cell-counted DOES> calls - pending patch 12; every design runs both test programs; +104 bytes a plain-CV8 image (417's (FAR)).
- `rehearsal-417.md` - The final batch rehearsed on plain CV8 (Iteration 417): the far-call tests and the programs past 4 MB on s6 at both widths, seed 58's front sampled, a short free run; patch 12 at 104 bytes, patch 13 the stage build's overlay check.
- `wip-regmachine/README.md` - The register machine, work in progress (from Iteration 418) - kept apart, nothing there runs: its first pricing on code as it runs (plain CV8 a fifth to a third of most workloads' dispatches taken in as operands; the tag little beyond I+), a first sketch.
- `candidates-generic.md` - Designs kept by id that no front holds (Iteration 430): bf439eb307's record, for xcheck --also - the candidates for the best design across the machine classes.
- `drafts/escape-mechanism-435.md` - An escape mechanism for the fast end, options and costs (Iteration 435): islands, age-layered immigrants, restart on stagnation, replicates; recommended - islands, an evolver option off by default, tried in one run against seeds 63-64.
- `drafts/footprint-gate-435.md` - A footprint gate, priced (Iteration 435): 1,266 fast-end children a run (seed 62), 1-2.5 s a reading; a held-out check about 10 minutes a run, a gate 1-2%, a footprint workload some 30% of the generations; recommended - the held-out check first.
- `audit-genes-designs-439.md` - Are good genes or promising designs being rejected? (Iteration 439): every place the pipeline turns designs away, checked - the screen costs about 9 front-quality designs a run, the 32-bit tail failures fixed and verified.
- `drafts/price-dthread-440.md` - Translation to direct threading at load, priced (Iteration 440): about 3% faster at best by the dispatch lab (the loop slower), about +58 KB in memory - a third of the memory objective - and a new engine path; not worth building now.
- `drafts/fastgate-review-445.md` - The fast gate, reviewed (Iteration 445): seed 64's 1,174 children measured twice agree with themselves (second / first 1.000) but the re-measure after the run finds the fastest about 10% slower - the two back-to-back readings share their moment's luck.
- `drafts/inert-scan-451.md` - Genes switched on but doing nothing (Iterations 451-452): four of seed 65's front designs, each expressed gene turned off, all seven workloads profiled, builds hashed - no gene inert across designs; alignfn, gotodup, fbuf the same build in one design or two.
- `drafts/fern-design-457.md` - **Obsolete (Iteration 510): Fern is its own project, which has these notes.** Fern, a small scripting language compiled into Forth words (Iteration 457): Ruby-style syntax, cells only, locals in a return-stack frame, no runtime of its own.
- `drafts/c4-family-459.md` - c4 and its family (Iterations 459, 462; the second pass: Gforth's code-copying literature, copy-and-patch, CPython's JIT, Deegen - six ideas proposed: a stencil relocatability check, stencils from relocations for ARM, the return-stack pointer in a register, wider.
- `drafts/appbench-466.md` - Real Forth applications as held-out workloads (Iteration 466): Appbench (benchgc, brainless, fcp, cd16sim, CoreMark, lexex) - deep stacks and frequent calls, unlike our kernels (RPyForth, 2026) - not reachable from this machine.
- `drafts/appbench-467.md` - Appbench on our Forth (Iteration 467; its tools in drafts/appbench/: fold.py, prelude.fth, run.py, which read the owner's zip in place): fcp, brainless and cd16sim run on s6 with their own checks PASS (6.8 s, 4.1 s, 6.5 s) - case folding, our own extend.4 and coreext.4.
- `drafts/appbench-468.md` - Applications held out - the tool (lab/evolve/appbench.py) and a first reading (Iteration 468): on three of seed 68's front the order holds but the lead does not - the design at 0.140 on the selection's workloads runs fcp.
- `drafts/apps-selection-491.md` - The applications in the selection, priced (Iteration 491): one short pass of our four applications as a seventh workload - seed 68's fast design at 0.573 of s6 on it, with the four JIT genes 0.193.
- `drafts/nocase-496.md` - The case-insensitive gene planned (Iteration 496): the concern weighed; where it hooks in - fold NAMEBUF after NAME>BUF/NAME>BUF8 (every search, the C ones too), fold the stored name in HEADER; an X8 overlay composing with kfast, klookup, kinput.
- `drafts/process-review-501.md` - What the recent runs say about the workflow, processes and rules (Iteration 501): the 32-bit JIT untested by engines-check (fixed - and a differential JIT test made permanent), conflict markers that apply (batch-check refuses them), rebasing a batch.
- `drafts/genecost-519.md` - Every gene's byte cost on three of seed 71's designs (Iteration 519): only jitexec's 585 KB out of line (fixed after seed 72), the rest as their mechanisms imply.
- `drafts/engine-cache-522.md` - An engine cache priced (Iteration 522): 300 consecutive designs of seed 72, 296 distinct compile inputs - a 1% hit rate (same-size engines differ in flags and tables); not built.
- `drafts/audit-ask-524.md` - An audit by prompt 20 (Iteration 524): every open challenge weighed - three for other models (the search's budget, the CPU state behind the fast end's offset, a fresh reading of the evolver's evaluation and selection), the rest answered by measurement.
- `drafts/front-recheck-528.md` - Seeds 70-72 rechecked by the corrected front (Iteration 528): about a third of each reported front was the true front; rtfuse and rtimm still freeze candidates, jitret not (11 -> 8 votes); jitfuse in 12 of seed 72's fastest 24.
- `drafts/front-recheck-528-votes.py` - The script behind front-recheck-528.md's votes (committed at 542).
- `drafts/frozen-recheck-534.md` - Every freeze rechecked on the true fronts, seeds 59-72 (Iteration 534): alignhot, jithelp, jitre, kstack hold; jitos (495) fails the rule - 11 votes and a keep vote (seed 69's best-Q tenth), and in seeds 59-66 often in the fastest and best-Q tenths.
- `drafts/frozen-recheck-534.py`, `drafts/frozen-recheck-534-raw.py` - The scripts behind frozen-recheck-534.md (committed at 542).
- `drafts/fast-end-offset-550.md` - Where the fast end's offset comes from (Iteration 550): not luck (the gate's two readings agree within 0.9%), not the clock - the JIT designs, under the run's load most likely; the test that would decide.
- `drafts/fast-end-offset-550.py` - The analysis behind it, from a run's records and its remeasure.json (Iteration 550).
- `drafts/fast-end-offset-554.md` - The fast end's offset tested on seed 75's re-measure (Iteration 554): a cost every workload's run pays, a design and s6 alike, outside user space - not the JIT; bubble's about 300 us in every group, kernel's 75.
- `drafts/fast-end-offset-554.py` - The script behind fast-end-offset-554.md: the run's records only, no new timing.
- `drafts/unfreeze-preflight-556.md` - Every lifted freeze checked before seed 77 (Iteration 556): four bases from seed 76's front, one gene at a time, both widths, nine workloads against s6 - no new failure.
- `drafts/unfreeze-preflight-556.py` - The pre-flight's script.
- `drafts/automation-audit-567.md` - Where the chat's manual work can become scripts (Iteration 567): eight candidates by what they save - a batch's mechanics and a design runner first.
- `drafts/ccflags-diff-567.py` - the recorded designs ccflags-after-seed81.patch builds differently (Iteration 567): 9 of seeds 76-80's 1,481, each an unexpressed alignhot.
- `drafts/two-width-scratch-db.jsonl` - The second two-width scratch run's database (Iteration 337): its designs without speed32, to reproduce.
- `drafts/hv-ranges-539.py` - The true fronts' ranges behind lab/evolve/hv-bounds.json (committed at 542).
- `drafts/seed74-front-549.py` - Seed 74's fronts: the true one against the results file's and the old staircase's on the same records (prediction 527), the one-round audits (529), the operators' shares (526), the JIT genes (534), the extremes (Iteration 549).
- `drafts/truefronts-tables-550.py` - truefronts.py's output turned into the progress table on the true fronts and the charts' data (Iteration 550; for seed 75's processing).
- `drafts/truefronts-charts-553.py` - The true fronts' charts drawn into a file from truefronts-tables-550.py's chart data (Iteration 553): each run's fastest, and the size-speed staircases by era.

### The stopping rule, the end of the phase, the article

- `drafts/article-method-548.md` - The article's method section, a first draft (Iteration 548): the design space, the objectives, the search, the three audited shortcuts, the true front, one command a run, the checks, the stopping rule, the baseline, what was not isolated.
- `drafts/confirmation-pool-559.md` - The confirmation run's founders, no good design missed (Iteration 559, the owner): --carry's tolerance front drops chain-hidden designs - the strict front instead, every archived run, the pool pre-flighted.
- `drafts/retire-candidates-573.md` - The nine genes seeds 77-83's fronts never moved off their old values (Iteration 573): what retiring each would remove - little but msc, the old values building the hand-made stages s2-s5; msc's Tegra check first.
- `drafts/retire-report-583.md` - Consolidation's retirement report with seed 86 in the pool (Iteration 583; retire-report-579.py rerun): 17 values on no design of the pooled true front of seeds 77-86.
- `drafts/retire-plan-583.md` - Consolidation's retirement planned (Iteration 583): each value against the 232 final-pick candidates, its code, its class; fsys 4-5 retired, the rest after the final set, the Tegra or the owner.
- `drafts/retire-stages-584.md` - Retiring the older formats (Iteration 584; the owner: if it loses no good design): the condition checked, what goes, what uses s2-s5, the six patches - the freeze first - and their build-hash test.
- `drafts/random-mode-548.patch` - The random-search baseline's mode, drafted and tested for consolidation (Iteration 548; GOALS.md, "When the improvements are done" 4): evolve.py --random - every child a fresh random genome, nothing learned in the loop, the fast gate kept.
- `candidates-final-seed84.md` - The final set's candidates from the pool of seeds 77-83 and seed 84 (Iteration 575, final-set.py --candidates): 242 records, one a line, for loadtest.py --ids and xcheck.py --also.
- `candidates-final-seed86.md` - The final set's candidates from the pool of seeds 77-84 and seed 86 (Iteration 582, final-set.py --candidates): 232 records, one a line, for loadtest.py --ids (the final pick's chain A).
- `final-pick-chainA-seed86.md` - The final pick's chain A (Iteration 585): the 232 re-measured, the set, the additions across machines, and the machines' agreement (the laptop's 64-bit fast-band order its own).
- `shortlist-seed86.md` - The final pick's shortlist (Iteration 585, final-pick.py --shortlist on chain A): 40 records, one a line, for chain B's loadtest.py --ids and dream's --also.
- `tegra-list-seed86.md` - Chain B's list for the Tegra (Iteration 585): the shortlist, retire-plan-583's msc pairs, the rest of the candidates, in xcheck --also's order.
- `final-pick-chainB-seed86.md` - The final pick's chain B (Iteration 587): the shortlist across three machines - the final set of 14, no generic pick within 25%, why the chain took 2.9 hours with nothing cut, the machines' agreement.
- `final-set-seed86.md` - The final set (Iteration 587, chain B): 14 records, one a line - consolidation's input, read again with chain C's second session.
- `chainB-seed86/README.md` - Chain B's readings (Iteration 587): the laptop's loadtest.md and each host's out.json and report, kept so the next session compares (chain A's were not).
- `fastend-remeasure-575.md` - Seed 84's fast-end re-measure (Iteration 575): 41 records - its fast bred designs, its best re-timed founders, the pool's fastest - for loadtest.py --ids; judged by drafts/fastend-judge-575.py.

### Prompts to other models, and their answers

- `drafts/more-projects-478.md` - Another model's list of projects, verified (Iteration 478): nibbleforth, tokthr, zForth, paraforth, astil_forth, romforth, bee, milliForth, sectorforth - what each is.
- `drafts/scout-prompt-479.md` - A prompt for other models to find projects and ideas we can reuse (Iteration 479): the project, the applications finding, seven areas wanted (JIT coverage, cheap transitions, register allocation, 32-bit native, density, workloads, method).
- `drafts/scout-answers-480.md` - Five answers to the scouting prompt, checked and merged (Iteration 480): what exists as described (copapy - MIT, ARM32; Mason's dual threaded and native execution, and his 2026 copy-and-patch JIT for threaded interpreters; Gregg's code-copying JIT; the R.
- `drafts/ask-arm-jit-511.md` - A prompt for other models (Iteration 511): porting the copy-and-patch JIT to 32-bit ARM (Tegra 3, Cortex-A9) - A32 or Thumb-2, copyable stencils without literal pools, the tail jump and branch encodings, movw/movt patching, returning (sp, tos) in registers.
- `drafts/ask-noise-511.md` - A prompt for other models (Iteration 511): selecting under measurement noise - the fast end's 7-10% optimism; the slower-of-two reading weighed; re-evaluation, racing, OCBA, shrinkage, noise-aware dominance; a protocol for our costs; load against luck; verifying a fix.
- `drafts/ask-jit-review-511.md` - A prompt for other models (Iteration 511): a bug hunt in the JIT - jit.c, spn-stencils.c and vm-lab.c's JIT entry and exit attached (as with the after-seed-71 batch); the invariants; each bug with a minimal trigger, to be turned into a test.
- `drafts/ask-arm-jit-answers-512.md` - The five answers to the ARM prompt, checked (Iteration 512) with GCC's ARM cross compiler, QEMU, Linux's cache-v7.S and the assembler: what holds (A32, `b` tails, encodings, uint64_t in r0:r1 - ours already, the cache flush incl. the branch predictor).
- `drafts/ask-noise-answers-513.md` - The five answers to the noise prompt, checked (Iteration 513), and our own noise measured: one reading's is 0.96% (seed 70's 1,130 gated pairs), the gate's regression to the mean 0.07%, the reference already paired.
- `drafts/ask-jit-review-answers-515.md` - The four answers to the bug hunt, checked (Iteration 515): one real bug - a word made after MARKER at an old word's address ran the old word's native code (jit_k keyed by address; reproduced 5 for 7, fixed, tested at both widths).
- `drafts/ask-search-524.md` - A prompt (524): more from a fixed evaluation budget - the surrogate's model and uncertainty, cheaper first looks, adaptive operators, stagnation; our numbers stated.
- `drafts/ask-cpu-state-524.md` - A prompt (524): why a paired ratio shifts ~7% between a loaded run and a quiet re-measure on a Ryzen laptop - what is ruled out, a diagnostic plan asked for.
- `drafts/ask-evolver-review-524.md` - A prompt (524): a bug hunt in the evolver's evaluation and selection - the invariants, the code embedded (359 lines of evolve.py).
- `drafts/ask-search-answers-525.md` - The five answers to the search prompt, checked against seed 72 (Iteration 525): the screen loses nothing (0 audited rejects front-worthy) - room to screen more; single workloads cannot rank the fast end; one round strays up to 7.4%.
- `drafts/ask-cpu-state-answers-526.md` - The five answers to the CPU-state prompt, checked (Iteration 526): the clock first - consistent with our counters (s6 the more compute-bound: 2.41 instructions a cycle against the JIT design's 2.21, a fifth of its branch misses); getrusage claims sorted.
- `drafts/ask-evolver-review-answers-527.md` - The evolver bug hunt's answers, checked (Iteration 527): first_front ignored the 2% speed band and the 32-bit speed - seed 72's front 246 designs, not 185 (every report, the gate, the re-measure); a failed second run kept its first reading.
- `drafts/ask-jit-table-530.md` - A prompt (530, prompt 20): a fresh reading of the converter's JIT table (tools/layout.py's vm-jit-ops.h and the translator's operand decoder, embedded) - the rules a row must keep at both cell widths, and the three bugs found there before.
- `drafts/ask-jit-table-answers-531.md` - The JIT-table review's answers, checked (Iteration 531): no bug - the 2@/2! claims had the standard backwards (the rows are its stated equivalents, the kernel's own definitions), the 32-bit EXECUTE claim misread how those rows are made.
- `drafts/ask-front-stats-537.md` - A prompt (537, prompt 20): comparing Pareto fronts across runs of a stochastic search - indicators and tests with two or three runs per method, the stopping rule's risks, a sound confirmation test, choosing the final set; our real figures stated.
- `drafts/ask-related-work-537.md` - A prompt (537, prompt 20): prior work for the article - automatic design-space exploration of interpreters and VMs, the techniques combined here, size-against-speed optimisation, what would be new, the two venues.
- `drafts/ask-front-stats-answers-538.md` - The front-statistics answers, checked (Iteration 538): a fixed-reference hypervolume, no rank tests with two or three runs (smallest p 0.100 for 3 against 3), at least three runs before stopping, an effect size decided in advance.
- `drafts/ask-related-work-answers-539.md` - The related-work answers, checked (Iteration 539): the prior art verified (Graves and Stigall 1991, Casey et al. 2007, QuickInterp 2020, the EVM superinstruction synthesis 2024 found by search; vmgen, COLE, copy-and-patch known).

## How the search works, and how runs are judged

- `weighing.md` - Weighing the objectives - not to lock out good trade-offs (Iteration 188).
- `run-length.md` - How long should a laptop run be? (Iteration 107).
- `gp-deep-dive.md` - The GP process and its genes: a deep dive (Iteration 195).
- `deep-dive-2.md` - Deep dive 2: more genes, and an instruction set evolution can build (Iteration 115).
- `sample-amd-ryzen-7-pro-8840hs.md` - A uniform sample of the design space - Ryzen 7 PRO 8840HS.
- `run-spread-amd-ryzen-7-pro-8840hs.md` - Every run kept: the best run is luck, the median reproduces - Ryzen 7 PRO 8840HS.
- `lucky-amd-ryzen-7-pro-8840hs.md` - Is the lucky fib run a place? - Ryzen 7 PRO 8840HS.
- `cpu-noise-amd-ryzen-7-pro-8840hs.md` - Does the CPU change a design's ratio? - Ryzen 7 PRO 8840HS.
- `evolve-knockout-amd-ryzen-7-pro-8840hs.md` - What each gene is worth - knockouts on the Ryzen 7 PRO 8840HS.
- `knockouts-seed30.md` - Knockouts of seed 30's front (Iteration 109).
- `gene-interactions-seed46.md` - Which genes interact - read from seed 46's own mutations (Iteration 250).
- `missed-options-2026-10.md` - Options missed so far? A gap check (Iteration 258).
- `stack-placement.md` - The stacks' place - the owner's question (Iteration 183).

## Genes, built and measured

- `bss.md` - Scratch buffers out of the image file: the gene `bss`.
- `dropx8.md` - The compiler's X8 copies, dropped: the gene `dropx8`.
- `lean.md` - Build artifacts left out of the image: the gene `lean`.
- `kfast.md` - The Forth sources: where the dispatches go, and the gene `kfast`.
- `rtimm.md` - n + and SWAP n + in code compiled at run time: the gene `rtimm`.
- `rtloop.md` - Loops compiled at run time with the image's own opcodes: the gene `rtloop`.
- `rtloopall.md` - rtloop for a design with all eight loop opcodes: the gene `rtloopall`.
- `t2wide.md` - The tag without its 3-byte call - the gene t2wide (Iteration 95).
- `jitx.md` - The gene jitx: the JIT reaches further (Iteration 108).
- `hotinl-opbody.md` - Inlining at the hottest call sites, and the bodies opcodes replaced (Iteration 92).
- `opcall.md` - The gene opcall: an operation and the call after it in one opcode (Iteration 121).
- `opcall-deaths.md` - Five wrong answers: the gene opcall (Iteration 173).
- `fused-keep-tests.md` - Tests that keep their value: DUP ?BRANCH and OVER ?BRANCH.
- `flags-gcsections.md` - Dead code out of every engine, and two flag genes (Iteration 113).
- `link-N.md` - The engine's file without page padding (Iteration 110).
- `tracer.md` - The tracer (Iteration 162).
- `far-addresses.md` - Code far from the image base (Iterations 157-158).
- `coverage.md` - Engine coverage - are all execution paths tested? (Iterations 159-161).

## Prices - ideas counted before, or instead of, building

- `price-hotcalls-seed3-front.md` - One-byte calls through a table of hot words - priced on seed 3's front.
- `price-seed3-front.md` - seed 3's front, priced (no heading).
- `price-hybrid.md` - The hybrid stack/register design, priced again (Iteration 172).
- `price-inline-tailcalls.md` - Inlining short words and Forth tail calls, priced (Iteration 89).
- `price-jit-calls.md` - Calls and returns at the fast end - priced (Iteration 245).
- `price-jit-interp.md` - Native code calling byte code, priced again (Iteration 220).
- `price-jit-stack.md` - Stack state in the JIT's translator, priced (Iteration 218).
- `price-keepforms-next.md` - The next keeping forms, priced again (Iteration 222).
- `price-lookup-cache.md` - A name-lookup cache, priced (Iteration 221).
- `price-names.md` - Names in the image, priced (Iteration 222).
- `price-register-machine.md` - A register machine, priced by counting.
- `price-register-stage1.md` - The register machine's first stage, priced by counting.
- `price-runtime-loops.md` - Loop words in code compiled at run time, and the far-call reach - priced by counting.
- `price-stencils-bloom.md` - Three ideas from the outside reviews, priced (Iteration 238).
- `syscall-pricing.md` - One SYSCALL - priced (Iteration 132).
- `jit-kernel-words.md` - Kernel words made native, priced (Iteration 103).
- `c-baseline-x86-64.md` - The Forth designs against the same benchmarks in C (lab/evolve/c-baseline.py) - the VM's, too noisy to keep.
- `c-baseline-amd-ryzen-7-pro-8840hs.md` - The designs against the same benchmarks in C, on the laptop (Iteration 285): the fastest 3.7x C -O2.
- `counters-amd-ryzen-7-pro-8840hs.md` - Hardware counters on the laptop (Iteration 285): dispatch predicted on compute work; the interpreter's work mispredicts on evolved designs, 9-24% of its cycles.
- `generalization.md` - One machine, small programs, the selection's own workloads (Iteration 305): what is measured of each, and the checks to come.
- `missmap-amd-ryzen-7-pro-8840hs.md` - Branch misses by handler on the laptop (Iteration 301): (FIND)'s C 9-13%, calls and returns 15-25%.

## The Forth sources, and other Forths

- `forth-sources.md` - Improving the Forth sources: kstack, ABORT", rewrites, other Forths (Iteration 116).
- `forth-collection.md` - The owner's Forth collection (Iteration 118).
- `forth-collection-catalog.md` - The owner's Forth collection, item by item (Iteration 119).
- `forth-implementations-survey.md` - Other Forths: ideas to borrow (Iteration 196).
- `forth-standard-tests.md` - The Forth 2012 test suite: what it reuses, what it found (Iteration 124).
- `relf-reuse.md` - What RelF upstream gives back: its fixes and tests (Iteration 125).
- `smithforth-review.md` - SmithForth, reviewed for reuse (Iteration 149).
- `docs-reuse.md` - What the collection's doc/ gives this project (Iteration 120).
- `word-audit.md` - Every word, audited - the sources and the weights (Iteration 131).
- `word-audit-plan.md` - Every word, audited against other Forths - the plan, and what is still to build (Iteration 127).
- `source-audit-2.md` - The Forth sources audited again - missed speed and size (Iteration 281): 2@, 2! and DEPTH, hot and reachable by no gene.
- `source-audit-3.md` - Source audit 3 (Iteration 299): where seed 50's fastest designs still dispatch - > and 0= built, ?STACK for later.
- `loop-audit.md` - The loops in the Forth sources - an audit (Iteration 203, the owner).

## The stage ladder, measured on machines

- `amd-ryzen-8840hs.md` - AMD Ryzen 7 PRO 8840HS, 16 cores.
- `amd-ryzen-7-pro-8840hs-x86_64-run1.md` - Results.
- `amd-ryzen-7-pro-8840hs-x86_64-run2.md` - Results.
- `spn-amd-ryzen-7-pro-8840hs-x86_64.md` - SPN measurements: AMD Ryzen 7 PRO 8840HS w/ Radeon 780M Graphics.
- `armv7-tegra.md` - ARMv7 (NVIDIA Tegra), 4 cores, Gentoo.
- `COMPARISON.md` - Two machines, measured the same way.

`RESULTS.md` in the repository root is generated and untracked - it
differs on every machine and would conflict on every pull. Files here
are deliberate snapshots, each naming the machine it came from, so two
runs can be compared without either being mistaken for the canonical
one.

    tools/collect-results.sh run
    tools/collect-results.sh report --save results/<machine>.md

Ratios travel between machines; absolute milliseconds do not. Each file
carries the host block the sweep recorded, so it says for itself what it
ran on.

## The Ryzen 8840HS, in CPU time and in cycles

`amd-ryzen-8840hs.md` is the September snapshot: CPU time, five layout
builds, three builds from a clean tree. `amd-ryzen-7-pro-8840hs-x86_64-run1.md`
and `-run2.md` are the two sweeps of one build at 27cc702, measured in
CPU CYCLES by `tools/bench-laptop.sh` (powersave governor, load 0.63);
`spn-amd-ryzen-7-pro-8840hs-x86_64.md` is the same run's SPN
measurements: start-up, end to end, memory, in CPU time, cycles and
instructions.

The two snapshots agree: for s1-s6 the ratios differ by a median of
1.2%, none by more than about one and a half combined standard errors -
a run in cycles reproduces a run in CPU time.

The same files at bfec34e are the run before the compare-and-branch
fusion (load 1.7), so the pair measures it: fib for s8-spncv8 went from
0.194 to 0.111 of the cell engine, level with s7 (FINDINGS-SPN.md).
Everything the change could not touch agreed between the two runs to a
median of 0.3%. That earlier SPN report's sections on CPU time versus
cycles were rewritten from its raw minima by `tools/clockfit.py`, whose
first explanation had blamed the clock; this one's were written by it.

## Drafts - designs, plans, negative results and archives (`drafts/`)

- `drafts/doc-index-audit-568.md` - How a session finds what the documents hold (Iteration 568): the index narrows a lookup to 2-9 lines where it names the topic; its run-by-run section a flat 170 lines; two reference documents two-thirds history - four proposals.
- `drafts/callrel.md` - The gene callrel - a draft, not in the batch (Iteration 164).
The leftovers of the chats of Iterations 213-265 (drafts/chat-to-iter265/, 3.4 MB as found) left the tree at Iteration 541; they are in the history: `git show cb05abe20:results/drafts/chat-to-iter265/README.md`.
- `drafts/crossfast.md` - The cross-compiler's byte loops - a fast path, proposed (Iteration 255).
- `drafts/factor-plan.md` - The gene factor - repeated code moved into headerless shared bodies (plan, Iteration 264).
- `drafts/fsys/README.md` - fsys - the file and memory words in Forth over SYSCALL (Iteration 202, in progress).
- `drafts/fsys/single-syscall.md` - The single-SYSCALL family - the design agreed with the owner (Iteration 204).
- `drafts/goals-snapshots.md` - GOALS.md as it stood before Iteration 275 - the sections taken out, verbatim.
- `drafts/jit-vm-survey.md` - JITs and VM speed elsewhere - what to borrow (Iteration 217).
- `drafts/locals-plan.md` - Locals ({: (LOCAL) TO) without a kernel hook (Iteration 193).
- `drafts/pgo.md` - The gene pgo - a draft (Iteration 200).
- `drafts/rtloop-cheaper.md` - The cheaper rtloop: rtloop=2 (Iteration 190).
- `drafts/surrogate-offline.md` - A surrogate to screen children - tested offline on seed 40 (Iteration 197).

The drafts also hold scripts and patches - the work behind some of these, kept where it produced a recorded figure.
