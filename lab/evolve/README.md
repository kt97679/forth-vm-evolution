# Evolving VM designs

`evolve.py` breeds CV8-family designs: engines and images built from a
genome, kept alive only if they pass the CORE corpus byte for byte and
cross-compile the kernel exactly, and selected on two counts at once -
speed, and image size - as a Pareto front. Its docstring has the genome,
the operators and the fitness; this is how to use it and what it found.

    lab/evolve/evolve.py --validate     s4, s5, s6 rebuilt from their genomes
    lab/evolve/evolve.py --pop 32 --gens 40 --rounds 5
    lab/evolve/evolve.py --report       build/evolve/report.md

It needs a finished `tools/build-stages.sh`. Everything it learns goes to
`build/evolve/db.jsonl`, one line per design - genome, parents, how it was
made, how it lived or died - so a run can stop and resume, and no design
is measured twice.

**Trusting it.** `--validate` rebuilds the three hand-made CV8 stages from
their genomes; their images must be byte-identical to the build's, or the
genome means something other than it says. They are.

**Running it for real.** Selection on CPU time in a VM is noise-bound; on
the Ryzen, cycles repeat to 0.3%. With the counters readable, it measures
cycles by itself:

    sudo sysctl kernel.perf_event_paranoid=2
    BENCH_CPU=9 lab/evolve/evolve.py --pop 32 --gens 40 --rounds 5
    sudo sysctl kernel.perf_event_paranoid=4

A design takes a second or two to build and test; 32 x 40 is about an
hour, less what the database already knows.

## Tools - one line each

What each script here does, from its own first line (Iteration 275). What each gene is:
GENES.md; running the evolution on the laptop: RUNNING.md; the rest of this file
is the evolver's development history, phase by phase, then iteration by iteration.

- `draft-results.py` - a returned seed's results file drafted from process-seed.sh's output (Iteration 551): the facts - records, the true front, the hypervolume, the extremes, one round first, the operators, the JIT designs, the fast end re-measured, the experiments, the remote checks.
- `process-run.sh` ITERATION [ARCHIVE] - a returned seed's processing, its mechanical part, one detached job (Iteration 560): process-seed.sh, draft-results.py, the batch checked and applied (git apply --index), process-checks.sh, and the control.
- `process-followup.sh` N ITERATION ROLES [ARCHIVE] - a returned follow-up chain's processing, its mechanical part, one command (Iteration 615): the archive unpacked, the chain's lines, the readings by session, the pooled pick, each role against its holder (followup-roles.py) - rehearsed by results/drafts/followup-rehearsal-615.sh.
- `process-finish.sh` N ITERATION [--dry] - the processing finished (Iteration 560): every check passed, the chain line filled, no TODO, process-records.sh, the chat's records there, then the commit and the bundle; stops naming what is wrong or missing.
- `process-records.sh` - HANDOFF's step 6, its mechanical part, in one command (Iteration 560): the applied batch moved to results/applied-after-seedN/ (only when every patch is applied) with its citations, the progress table, the gene votes and the stopping line appended (each once).
- `carry-check.py` [DB...] [--all] [--sample N] - the confirmation run's founders pre-flighted (Iteration 562): the pool --carry makes (evolve.py's carry_pool - each database's strict front and the named designs), its size and generation 0's hours.
- `restore-archives.sh` [FROM] - carryall's archives (Iteration 572): the databases tools/clean-runs.sh removed, back from their seed packs (seeds FROM on, default 71) as archived-<pack time>; next-run.sh runs it for carryall; tools/test-restore-archives.sh in run-tests.
- `carry-named.txt` - designs named elsewhere (each machine's fastest, the held-out and application bests), carried in where a database has them and no front did (Iteration 562).
- `deaths-check.py` - a returned seed's deaths and wrong outputs rebuilt on this tree, each against s6's output (Iteration 560): the expected causes listed, not rebuilt; exit 1 on one still wrong - an open correctness issue. process-checks.sh runs it after ans-check. A death by a retired value refused here in the run's words is expected (615; --self-test in run-tests).
- `design.py` DESIGN [GENE=VALUE ...] [--db FILE] [--width 4] [--keep DIR] INPUT ... - one design built and run against s6 (Iteration 567): a recorded id or a hand-made stage with genes set, each gene said expressed or not.
- `gene-narrow.py` DB ID WORKLOAD GENE=VALUE... - which genes a design's wrong output needs (Iteration 564): each suspect value put back one at a time (necessary), then each returned alone to the rest put back (sufficient); a build a line.
- `heldout.py` - does the front's speed hold on the held-out workload: the rank correlation, the fastest designs' held-out ranks, the designs the selection flatters (Iteration 305) Iteration 390: the Spearman over the fastest third and tenth, and the regret (the pick against the held-out fastest).
- `footprint-gen.py` - a held-out program whose code footprint grows (N [--calls T] [--defs-only]): N words in levels, run round-robin, a checksum (Iteration 370; results/generalization.md)
- `lifted.py` - the freezes lifted at 556 on a run's true front (Iteration 557): each gene's share at each value, the enrichment of its other values, prediction 556 scored; process-seed.sh runs it.
- `stopping.py` - GOALS.md's stopping rule, mechanical (Iteration 554): a run's hypervolume and four extremes against the best of the method's earlier runs in results/stopping-series.md, criterion by criterion; the count, the earliest stop, the next run's bar.
- `process-checks.sh` - the checks on master after a seed's processing applied its batch (Iteration 551): build, run-tests, validate, the gate, ans-check on its sample, the jail last - started detached, one status file; FROM= resumes after a sandbox restart.
- `stencil-check.py` - the JIT's stencils safe to copy (Iteration 463; the after-seed-68 batch, applied at 487): from objdump's relocations, every stencil's references inside its copied part and no branch past it; engines-check runs it at 64 and 32 bits, and jit.c guards at run time.
- `jitholes-check.py` - a JIT design whose stencil holds a value hole twice computes right (Iteration 557; the after-seed-77 batch, applied at 560): seed 76's d11c9a6300 rebuilt, its corpus against s6's; run-tests runs it.
- `apps/brainless/COPIED.md` - brainless (public domain) copied into apps/brainless/ from Appbench 1.4 (Iteration 492): appbench.py runs it with no zip
- `apps/wordfreq.fth`, `apps/minif.fth` - two more held-out applications from scratch (Iteration 500): words of generated text counted in a hash table of counted strings.
- `appbench.py` - applications held out (Iteration 468): the newest front's designs built and run on Appbench's fcp, brainless and cd16sim (the owner's zip, read in place) against s6, each output checked, ranked against the in-run speed; its folding and prelude in appbench/
- `fold.py` (lab/evolve/appbench/) - appbench.py's folding: an application's source to upper case, keeping strings, comments, file and character names, upper-casing a string EVALUATE takes unless it holds a '/', $hex made decimal (Iteration 467)
- `loadtest.py` - the measuring load (Iteration 455): the newest run's front, its fastest and slowest, each measured against s6 idle and with other cores busy running s6 - does load explain the fast end's optimism (results/drafts/fastgate-review-445.md); --ids FILE (573): the candidates.
- `footprint.py` - does the front's speed hold as the code footprint grows: a sample of the newest run's front on footprint-gen.py's programs, paired with s6, checksums checked; run and compile phases against s6, and the selection's rank agreement at each N (Iteration 371; results/generalization.md)
- `gene-usage.py` - the genes fronts use, an absent gene counted as off: one group, or two side by side by their difference (--vs) - seed 58 against the carried runs, a review's evidence (Iteration 375)
- `missmap.py` - which handlers mispredict: perf record's user-space branch misses on the kernel and corpus workloads, each sample's source line charged to its handler (Iteration 294; the laptop's, between runs)
- `word-cost.py` - the dispatches each workload spends inside chosen words, on chosen designs - what an opcode for them could save at most (Iteration 281)
- `supers-knockout.py` - do superinstruction pairs buy anything: a front's designs that build pairs, each built as it is and with its supers gene emptied - the profiler's dispatches over the selection workloads and binary + image.
- `review-checks.py` - the methodology review's figures, each reproducible: pedigree (a front's share from each generation-0 design), curse (in-run against re-measured speed; held-out agreement at the top), cpus (a session's verdict measures from each CPU alone; front membership across CPUs).
- `process-seed.sh` ARCHIVE [OUT] - a returned chain archive's mechanical part (Iteration 395): unpacked, the pack's checks, the verdict as printed and from both CPUs, seed-facts, heldout, progress, the remote checks' agreement - files under OUT, about a screen in OUT/summary.md
- `ans-check.py` - ans-check.py [--ids A,B,...] [DB ...] - the held-out check (Iteration 119; the
- `c-baseline.py` - c-baseline.py [--runs N] [IDS...] - the Forth designs against the same
- `callsites.py` - callsites.py ID [ID ...] [--db FILE ...] - a design's calls in the two-bit
- `compare-fronts.py` - compare-fronts.py DB [DB ...] [--rounds N] [--cpus A,B] - the fronts of; Iteration 352: --widths 8,4 - and each design's interpreter at 4-byte cells (eval32), a section "At 32 bits": each run's fastest there against the others'
- `counters-test.py` - counters.py leaves kernel.perf_event_paranoid as it found it, however the run ends: eight cases, a stand-in sudo; as root on a scratch machine (Iteration 279)
- `counters.py` - where the cycles go: hardware counters (perf) for the newest front's designs on the selection workloads - the laptop's (Iteration 278)
- `clockcheck.py` - the clock test (Iteration 527, the owner; from Iteration 554 the cost a design and s6 both pay, and the system time): the fast end paired with s6 alone, beside benchmark co-runners and beside compile co-runners, each run's CPU time and cycles and the core's clock.
- `contention.py` - the fastest of a run's front measured as the run measures them (paired with s6), alone and beside co-running workers (Iteration 514): does contention account for the fast end's 7-10% (rule 3)? A chain step from seed 72
- `cpu-noise.py` - cpu-noise.py [--rounds N] [--cpus A,B] [--ids ID,...] [--work W,...] DB [DB ...]
- `engines-check.py` - (Iteration 501: the JIT kept at 32 bits, and tests/jit/jit-diff.fth on every JIT variant against s6 at the same width) engines-check.py - an engine down every generator's path builds, and runs
- `evolve.py` - evolve.py - evolve VM designs: the faster and the smaller survive
- `factor-price.py` - factor-price.py ID [--shares 1e-3,1e-2,2] [--db FILE ...] - what the gene
- `final-set.py` - GOALS.md step 3's selection (Iteration 571): from runs' records pooled, the true front merged within the tolerances, the four strict extremes, then designs by hypervolume gain to K; a knee as a candidate; --candidates (573): the re-measure's.
- `baseline.py` - GOALS.md step 4, the random-search baseline (Iteration 573): the random run beside the series at the same generation and at their ends, as values; random designs on the final front named; --append its ledger line; --self-test.
- `final-pick.py` - GOALS.md step 3 after the re-measures (Iteration 573): the extremes and the set chosen from loadtest.py --ids's re-measures, alone and under load; each host's fastest named, its fast five FLAGGED if out of the set; --self-test.
- `confirm.py` - GOALS.md step 2, the confirmation test (Iteration 573): a carryall run against the series' pooled true front and best extremes, what it added, gains by origin, the genes' four classes (573); process-seed.sh runs it; --self-test.
- `fsys-count.py` - fsys-count.py ID [ID ...] --db FILE [--db FILE] [--levels 4,5] [--works kernel,corpus]
- `gate.py` - gate.py RESULTS COMPARE - step 8 of processing a returned seed (Iteration 256)
- `gene-interactions.py` - gene-interactions.py - how one gene's effect depends on another, read from a
- `genecost.py` - what each gene costs in bytes, switched one at a time on given designs (Iteration 519): the check that would have caught jitexec's 585 KB table (results/drafts/genecost-519.md)
- `hv.py` - the fixed-reference hypervolume of a run's true front (Iteration 539): four objectives in the box hv-bounds.json fixed before seed 74, exact by slicing, pure Python; `--self-test` against Monte Carlo. GOALS.md's stopping rule and confirmation run use it
- `hotsites.py` - hotsites.py ID [--db FILE ...] [--write FILE] - the image's hottest call
- `gene-equiv.py` - the evolver's genes behave as they did at an earlier commit: ids, expressions, seeded mutations, draws and crossovers (Iteration 276)
- `gene-table-test.py` - a new gene is one row: a fictional gene works with no code change (Iteration 276)
- `hotwords.py` - hotwords.py ID [ID ...] [--db FILE ...] [--write FILE] - every word's share
- `jitpairs.py` - the operation pairs a JIT design runs over the selection workloads, named from its JIT table: prices super-stencils (Iteration 506; results/drafts/jit-pairs-506.md)
- `jitapps.py` - what the JIT leaves on the applications (Iteration 471): a design profiled with the JIT off and on (-DJITLOG=1) over appbench.py's applications - the dispatches left, the words they sit in, each refusal followed to its root
- `jitleft.py` - what the JIT leaves to the interpreter (Iteration 339): each JIT design profiled with the JIT off and on - the dispatches left, by workload, and the words that carry them
- `image-ab.py` - image-ab.py ID [ID ...] --env VAR=VALUE [--set GENE=VALUE] [--db FILE] [--rounds N] - a
- `jitstack-inner-sweep.sh` - jitstack-inner-sweep.sh - lab/evolve/jitstack-inner.{c,S} with every loop head
- `jitstack.py` - jitstack.py ID [ID ...] [--db FILE ...] [--works fib,loop,...] - stack state in
- `jitvariants.py` - jitvariants.py [ID] [--k 2,3] [--out FILE] - what stack state in the JIT would
- `loopwords.py` - loopwords.py ID [ID ...] [--db FILE] - the loop words in code compiled at
- `lucky.py` - lucky.py [--step S] [--sweeps K] [--ids ID,...] DB [DB ...] - is the lucky
- `names-check.py` - names-check.py [IDS...] - word names in UTF-8, defined and then compiled
- `chainctl.py` - a chain of runs as one thing (Iteration 313): next-run.sh's status, monitor and stop; the one archive a chain makes, whatever happened; progress lines.
- `next-run.sh` - lab/evolve/next-run.sh [SEED | compare [ROUNDS] | experiment TOOL [ARGS] | none] - the next run on the laptop, in
- `remote-checks.sh` - the previous front measured on other machines alongside a seed chain (Iteration 315): the hosts and modes in lab/evolve/REMOTES; probe at start, start before the evolution, gathered into the chain's archive as remote/HOST.md, stopped with the chain; never costs it.
- `chain-sessions.py` - a returned final-pick chain's readings laid out by session for final-pick.py --also-session; the final-pick line and msc's Tegra verdict printed (Iteration 595).
- `followup-roles.py` - a follow-up chain's roles (Iteration 615; results/drafts/followup-roles-611.py made general, its 611 figures to the byte): completeness, noise, each portable role against its holder by the 2% / 1% / 4 KB rule, a run's predictions.
- `pack-designs.py` - designs packed for another project (Iteration 601, relf): each built at both widths by build(), its engine, image, C source as compiled and build commands, checked against s6 on the nine workloads.
- `portable.py` - the portable run (seed N nojit) beside the portable designs found before it, by the stopping rule's thresholds; its own ledger line (Iteration 602). Iteration 613: every earlier portable run in the pool (the ledger's portable lines); --front OUT writes the pool's front.
- `portable-followup.py` - the portable run's follow-up chain: the run's best on the union's front beside the 282's re-measured set, its list and its NEXT-RUN and REMOTES lines sized from measured rates (Iteration 604).
- `export-designs.py` - designs exported so `make` builds them: each one's real source (the compiler's own -MM), a Makefile, the image shipped; checked byte for byte against the lab's build in a fresh directory (Iteration 608).
- `repeat-fits.sh` - whether one more session of a repeated experiment ends by the chain's deadline - the remote lines' last (Iteration 591, chain D): next-run.sh's then_next asks it; REMOTES' --sessions K is the hosts' side.
- `outbuf-check.py` - outbuf-check.py [ID] - does output buffering break anything? (Iteration 207)
- `price.py` - price.py ID [ID ...] [--db FILE] - what a fusion could save, before building it
- `perf-hold.py` - root's half of counters.py's counters in next-run.sh's chain: sets kernel.perf_event_paranoid 2 only while counters.py measures, then restores it (Iteration 282)
- `perf-hold-start.sh` - next-run.sh's foreground step before its chain detaches: sudo asks once, perf-hold.py is left holding (Iteration 282)
- `progress-table.py` - progress-table.py - every run's extremes, from its results file (Iteration 253)
- `readline-check.py` - readline-check.py [ID ...] - READ-LINE at every single-SYSCALL level against
- `regprice.py` - regprice.py ID|s6 [ID ...] [--db FILE] - the register machine's first
- `run-spread.py` - run-spread.py [--runs N] [--cpus A,B] [--ids ID,...] DB [DB ...] - every
- `scan-bodycheck.py` - scan-bodycheck.py [--db FILE] [--old] - which designs lose a word silently
- `scan.py` - scan.py - every single-gene change of every hand-made design, checked
- `seed-facts.py` - seed-facts.py DB RESULTS - step 3 of processing a returned seed (Iteration 256)
- `stackops.py` - stackops.py ID [ID ...] [--db FILE] - a register machine priced by
- `tag2-rank.py` - tag2-rank.py OUT.json DB ID [ID ...] - the reference ranking
- `test-evolver.py` - the evolver's self-test (Iteration 530; applied at 544 with the after-seed-73 batch): first_front against fronts()[0] over 300 random populations, one round first's decision, the adaptive operators' shares and floor, a gated design's second reading (gate_again) - 14 checks.
- `test-resume.py` - a resumed run replays its first attempt (Iteration 610; seed 87's restart forked at generation 3): a run with a stand-in measurement cut at generation 6, started again - generations 1-6 as the first attempt's; EVOLVE_REPLAY=0 forks, the control. In tools/run-tests.sh.
- `test-jail.py` - test-jail.py - prove that an engine the evolver runs cannot fork
- `truefronts.py` - every run's true front recomputed from its records (Iteration 547; GOALS.md: the article's figures on the true fronts): a chain's experiment step that reads every archived run's database and measures nothing.
- `vm-run.sh` - lab/evolve/vm-run.sh SEED [REQ] - a run on the development VM (Iteration 79)
- `xcheck.py` - the front measured on another machine: --sample picks designs on the laptop, the host's run builds, checks and measures them against s6 there, --report compares the rankings (Iteration 307); --arm, the Tegra's clang designs cross-built (570); --also @FILE (573).
- `NEXT-RUN` - what the laptop runs next, with every past choice as a comment
- `hotsites-v1.json`, `tag2-rank-v1.json`, `hotwords-v1.json` - the reference profiles the converter reads (hotinl, the tag's ranking, factor)

## History

The evolver's development - its phases, and each gene and feature as it came (Iterations 1-376): HISTORY.md, moved
there at Iteration 568. Grep a gene or a word in it; never read it whole.
