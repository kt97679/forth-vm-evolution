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

- `draft-results.py` - a returned seed's results file drafted from process-seed.sh's output (Iteration 551): the facts - records, the true front, the hypervolume, the extremes, one round first, the operators, the JIT designs, the fast end re-measured, the experiments, the remote checks - with TODO lines for the verdict, the predictions, the votes and the rules; also the xcheck file and the spread's session.
- `heldout.py` - does the front's speed hold on the held-out workload: the rank correlation, the fastest designs' held-out ranks, the designs the selection flatters (Iteration 305) Iteration 390: the Spearman over the fastest third and tenth, and the regret (the pick against the held-out fastest).
- `footprint-gen.py` - a held-out program whose code footprint grows (N [--calls T] [--defs-only]): N words in levels, run round-robin, a checksum (Iteration 370; results/generalization.md)
- `lifted.py` - the freezes lifted at 556 on a run's true front (Iteration 557): each gene's share at each value, the enrichment of its other values, prediction 556 scored; process-seed.sh runs it.
- `stopping.py` - GOALS.md's stopping rule, mechanical (Iteration 554): a run's hypervolume and four extremes against the best of the method's earlier runs in results/stopping-series.md, criterion by criterion; the count, the earliest stop, the next run's bar. process-seed.sh and draft-results.py run it; step 6 appends the run (--append).
- `process-checks.sh` - the checks on master after a seed's processing applied its batch (Iteration 551): build, run-tests, validate, the gate, ans-check on its sample, the jail last - started detached, one status file; FROM= resumes after a sandbox restart.
- `stencil-check.py` - the JIT's stencils safe to copy (Iteration 463; the after-seed-68 batch, applied at 487): from objdump's relocations, every stencil's references inside its copied part and no branch past it; engines-check runs it at 64 and 32 bits, and jit.c guards at run time
- `apps/brainless/COPIED.md` - brainless (public domain) copied into apps/brainless/ from Appbench 1.4 (Iteration 492): appbench.py runs it with no zip
- `apps/wordfreq.fth`, `apps/minif.fth` - two more held-out applications from scratch (Iteration 500): words of generated text counted in a hash table of counted strings; a small Forth interpreted in Forth (its own dictionary searched by string compare, colon definitions run through EXECUTE, IF and THEN, an unknown word thrown and caught) - appbench.py's, not the selection's
- `appbench.py` - applications held out (Iteration 468): the newest front's designs built and run on Appbench's fcp, brainless and cd16sim (the owner's zip, read in place) against s6, each output checked, ranked against the in-run speed; its folding and prelude in appbench/
- `fold.py` (lab/evolve/appbench/) - appbench.py's folding: an application's source to upper case, keeping strings, comments, file and character names, upper-casing a string EVALUATE takes unless it holds a '/', $hex made decimal (Iteration 467)
- `loadtest.py` - the measuring load (Iteration 455): the newest run's front, its fastest and slowest, each measured against s6 idle and with other cores busy running s6 - does load explain the fast end's optimism (results/drafts/fastgate-review-445.md)
- `footprint.py` - does the front's speed hold as the code footprint grows: a sample of the newest run's front on footprint-gen.py's programs, paired with s6, checksums checked; run and compile phases against s6, and the selection's rank agreement at each N (Iteration 371; results/generalization.md)
- `gene-usage.py` - the genes fronts use, an absent gene counted as off: one group, or two side by side by their difference (--vs) - seed 58 against the carried runs, a review's evidence (Iteration 375)
- `missmap.py` - which handlers mispredict: perf record's user-space branch misses on the kernel and corpus workloads, each sample's source line charged to its handler (Iteration 294; the laptop's, between runs)
- `word-cost.py` - the dispatches each workload spends inside chosen words, on chosen designs - what an opcode for them could save at most (Iteration 281)
- `supers-knockout.py` - do superinstruction pairs buy anything: a front's designs that build pairs, each built as it is and with its supers gene emptied - the profiler's dispatches over the selection workloads and binary + image, with a control and the sizes checked against the records (Iteration 385; results/supers-knockout-seed58.md)
- `review-checks.py` - the methodology review's figures, each reproducible: pedigree (a front's share from each generation-0 design), curse (in-run against re-measured speed; held-out agreement at the top), cpus (a session's verdict measures from each CPU alone; front membership across CPUs), screen (the surrogate screen's audit), verdicts (every session's verdict rebuilt, then from each CPU alone - Iteration 388) (Iteration 386; results/review-methodology-386.md) And progress (Iteration 392): a run seen from inside - diversity by generation, overall and per encoding family, and its last gains. And spread (Iteration 393): runs of one start compared at one generation - front measures and gene usage.
- `process-seed.sh` ARCHIVE [OUT] - a returned chain archive's mechanical part (Iteration 395): unpacked, the pack's checks, the verdict as printed and from both CPUs, seed-facts, heldout, progress, the remote checks' agreement - files under OUT, about a screen in OUT/summary.md
- `ans-check.py` - ans-check.py [--ids A,B,...] [DB ...] - the held-out check (Iteration 119; the
- `c-baseline.py` - c-baseline.py [--runs N] [IDS...] - the Forth designs against the same
- `callsites.py` - callsites.py ID [ID ...] [--db FILE ...] - a design's calls in the two-bit
- `compare-fronts.py` - compare-fronts.py DB [DB ...] [--rounds N] [--cpus A,B] - the fronts of; Iteration 352: --widths 8,4 - and each design's interpreter at 4-byte cells (eval32), a section "At 32 bits": each run's fastest there against the others'
- `counters-test.py` - counters.py leaves kernel.perf_event_paranoid as it found it, however the run ends: eight cases, a stand-in sudo; as root on a scratch machine (Iteration 279)
- `counters.py` - where the cycles go: hardware counters (perf) for the newest front's designs on the selection workloads - the laptop's (Iteration 278)
- `clockcheck.py` - the clock test (Iteration 527, the owner; from Iteration 554 the cost a design and s6 both pay, and the system time): the fast end paired with s6 alone, beside benchmark co-runners and beside compile co-runners, each run's CPU time and cycles and the core's clock - is the fast end's offset the clock? A chain step from seed 74
- `contention.py` - the fastest of a run's front measured as the run measures them (paired with s6), alone and beside co-running workers (Iteration 514): does contention account for the fast end's 7-10% (rule 3)? A chain step from seed 72
- `cpu-noise.py` - cpu-noise.py [--rounds N] [--cpus A,B] [--ids ID,...] [--work W,...] DB [DB ...]
- `engines-check.py` - (Iteration 501: the JIT kept at 32 bits, and tests/jit/jit-diff.fth on every JIT variant against s6 at the same width) engines-check.py - an engine down every generator's path builds, and runs
- `evolve.py` - evolve.py - evolve VM designs: the faster and the smaller survive
- `factor-price.py` - factor-price.py ID [--shares 1e-3,1e-2,2] [--db FILE ...] - what the gene
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
- `chainctl.py` - a chain of runs as one thing (Iteration 313): next-run.sh's status, monitor and stop; the one archive a chain makes, whatever happened; progress lines; a crashed chain archived at the next start, root's files given back Since Iteration 541 its archive leaves out the copies sent to the remotes (repo.bundle, bins.tar.gz) - about 40% of it, none of it a record.
- `next-run.sh` - lab/evolve/next-run.sh [SEED | compare [ROUNDS] | experiment TOOL [ARGS] | none] - the next run on the laptop, in
- `remote-checks.sh` - the previous front measured on other machines alongside a seed chain (Iteration 315): the hosts in lab/evolve/REMOTES; probe at start, start before the evolution, gathered into the chain's archive as remote/HOST.md, stopped with the chain; never costs it; Iteration 331: several checks a host (run one after another, each deadline from its own start) - prebuilt (the laptop's 64-bit binaries), prebuilt32 (its static 32-bit x86 builds at 4-byte cells and the 4-byte references), native (built there: the Tegra at its own 4-byte cells) Since Iteration 379 the run waits only for the sampling: the copying and starting go to the background (remote/launch.sh) - seed 57 waited 52 minutes for them. Since Iteration 381, probes: each connection and copy timed, the host's load at the start and every 30 s - in each host's report.
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
- `test-evolver.py` - the evolver's self-test (Iteration 530; applied at 544 with the after-seed-73 batch): first_front against fronts()[0] over 300 random populations, one round first's decision, the adaptive operators' shares and floor, a gated design's second reading (gate_again) - 14 checks, run by tools/run-tests.sh.
- `test-jail.py` - test-jail.py - prove that an engine the evolver runs cannot fork
- `truefronts.py` - every run's true front recomputed from its records (Iteration 547; GOALS.md: the article's figures on the true fronts): a chain's experiment step that reads every archived run's database and measures nothing - each run named by its seed (the results file whose front its own children made), its true front against the reported one, the extremes, what its speed is over, then every true front's designs as JSON lines.
- `vm-run.sh` - lab/evolve/vm-run.sh SEED [REQ] - a run on the development VM (Iteration 79)
- `xcheck.py` - the front measured on another machine: --sample picks designs on the laptop, the host's run builds, checks and measures them against s6 there, --report compares the rankings (Iteration 307); Iteration 331: --cell 4 samples a 32-bit check - each design built and alive as a 32-bit x86 engine here before it goes; the host's byte order and cell width recorded Since Iteration 377, --rejected K: designs the selection rejected, measured too.
- `NEXT-RUN` - what the laptop runs next, with every past choice as a comment
- `hotsites-v1.json`, `tag2-rank-v1.json`, `hotwords-v1.json` - the reference profiles the converter reads (hotinl, the tag's ranking, factor)

## Phase 1, development VM, CPU time - a first run, 8 x 3

- **It rediscovered the 256-entry dispatch table.** The best design was s6
  with `d256=1`: the same 9,969-byte image, about 8% faster, and 7% faster
  on the held-out loop - strictly better than the hand-made s6. It got
  there by BORROWING the dispatch block from another lineage.
- **The held-out workload caught overfitting.** The fastest design on the
  four selection workloads (0.849 of s6) was slower than s6 on loop.
- **Most of what mutation tries is lethal**: designs that do not convert,
  fail the corpus, or hang. Each cause is recorded; one, byte headers with
  scaled call targets, is now a constraint rather than a death.
- **The fold gene is small.** Only the 23 hand-picked primitives can be
  folded at all - the other candidates make engines that do not compile -
  so the opcode map's real combinatorial space waits for phase 2.

## Phase 1b: four families and the compiler

The genome now spans the whole ladder - the cell engine, SOD16, CPT16 and
CV8 - with genes a family does not use carried dormant, and the compiler
flags gforth and CPython rely on as genes of their own (`GENES.md`).
`--validate` rebuilds all seven hand-made stages, s0 to s6, with
byte-identical images. Each family keeps its best member, so a family
survives as a species even when CV8 dominates the front.

A first 12 x 3 run in the VM: 48 designs, 37 alive. CV8 took the front;
the other families held their niches. Compiler genes spread on their own
- `-fno-crossjumping` in 9 of the living, `-fcf-protection=none` in 7,
`-fno-gcse` in 6. The fastest design descended from the PLAIN s4 by
crossover, borrowed another lineage's call path and dispatch, and took
`-fno-crossjumping`: 0.83 of s6's time, 0.98 on the held-out loop.

## Phase 2a: superinstructions

`tools/gen-super.py` builds a pair's handler from the two primitives' own
bodies - the first jumps into the second where it would have dispatched -
and the converter fuses the pair wherever no branch lands between them
(`--supers-file`, the same guard as folding). The pairs take the opcodes
nothing else holds: 126 and 127, the fold band past the folds in use, and
the specialisation band when SPEC is off, so folds, specialisations and
pairs compete for slots. The 24 candidates are the primitive pairs the
CV8 interpreter dispatched most over the four selection workloads.

Every pair improves BOTH objectives. Development VM, against the parent:
s6 with the two it has room for, 0.944 of the time and 16 bytes smaller;
s4, which has thirty free slots, with all 24, 0.849 and 96 bytes smaller -
and the held-out loop faster too, 0.983 and 0.892, so it is no artefact
of the selection workloads.

A 12 x 4 run, with two founders carrying pairs: 23 of 44 living designs
had them, and hand-made s6 fell off the front - its founder variant was
smaller and faster. The best design came from that founder, borrowed its
pairs from a third lineage and its call-target block from another, and
reached 0.85 of s6's time.

## Phase 2b: run-time fusion, and a correction about folds

Superinstructions in the image leave out code compiled at run time.
`forth/cv8-fuse.4` is an overlay on the CV8 compiler that fuses as it
compiles: COMPILE,8 rewrites the previous byte when it is a plain
primitive immediately before HERE and the pair is in SUPER-TABLE, which
the converter fills in per design (`--rtfuse`). BEGIN and DO now clear
LAST-OP, since they make HERE a branch target without emitting anything
there. Read back: `: T1 DUP >R C! R> ;` compiles to 126 127 EXIT, while
`DUP BEGIN >R` stays two bytes. Corpus identical, kernel reproduced.

It does not pay on these workloads, so it is a gene (`rtfuse`, with the
overlay only where it is set) and selection rejects it. The overlay costs
560-576 bytes and the designs get slower: s6 with two pairs 0.956 -> 0.970,
s4 with 24 pairs 0.855 -> 0.877. The hot pairs are in the image's code,
already fused; code compiled at run time here holds few of the 24 (FIB
none); and the compiler now scans the pair table for every primitive it
compiles. In a 12 x 4 run, 5 living designs fused at run time, none on
the front.

**A correction to phase 1.** cv8.4's FOLD-OPS, the compiler's fold list,
is fixed in its source. Every CV8 design whose fold list differed from
the default - shorter, or reordered - compiled run-time code with fold
opcodes its engine gives to other primitives, and died on the corpus:
with the converter before this change, s6 without `LIT` and s6 with 12
folds both die. So in every earlier run the fold genes could survive only
in their default form, and nothing said about folds was learned from
selection. The converter now writes each design's list into FOLD-OPS,
padded with 255, which no opcode matches; the default list writes back
the same bytes, so the hand-made stages are unchanged and it costs
nothing. Those designs now live: the reversed list at the same size and
speed, without `LIT` 16 bytes bigger, with 12 folds 40 bytes bigger and
3.5% slower. In the 12 x 4 run, 4 of 5 fold mutants survived, and the best
design has a removed fold and a borrowed fold list in its history.

## Phase 2c: the hang, and two more mapping bugs

The hang was not what it looked like. On s6 the trigger is `bytehdr=0`
ALONE; no caching and `-fno-crossjumping` only changed how it failed (a
stack error instead of a hang). Interpreted, `SOURCE TYPE` worked;
compiled into a definition it failed - so the fault was in code compiled
at RUN time.

cv8.4 and cv8b.4 set the in-image compiler's call shift and DOES> form
as a pair - shift 3, near DOES> calls, 2 bytes reserved; or shift 0, far
calls, 3 bytes - but the genome chooses `scale`, `bytehdr` and `doesfar`
independently. s6 without byte headers got cv8.4's shift 3 with its own
byte-granular calls, so every call compiled at run time went to the
wrong address. The converter now writes all three variables from the
design's own genes (`--set-compiler-vars`, `--does-far`); the hand-made
stages come out unchanged.

The second: variable-length calls are decoded only on the engine's
shared call path (`do_call`), so `varcall` without `sharedcall` misread
every three-byte call - in every earlier run. `sharedcall` is now dormant,
built in, when `varcall` is set; decoding both forms on the unshared path
would reopen that combination.

What dies now is real. A byte-granular design with near DOES> calls, or
without the three-byte call form, reaches 16 KB, and the kernel
workload's dictionary is larger: a DOES> word past 20,000 bytes of padding
hangs with near calls and works with far ones. They die by timing out
because cv8.4's near forms do not check their reach.

The same 12 x 4 run, before and after each fix: alive 45 -> 51 -> 53 of
60; corpus deaths 7 -> 3 -> 0; the remaining 7 deaths all that reach
limit. The fastest design was s6 without byte headers, with d256 and one
pair, at 0.806 of s6 - the combination that used to hang.

All three bugs (with the fold list) are one kind: a setting of the
compiler INSIDE the image that the genome treated as free, but the dump
fixed. So the earlier runs' verdicts on fold lists, on byte headers
against call granularity, and on the shared call path were artefacts.

## Phase 2d: a scan of every single change, and a flawed check

`lab/evolve/scan.py` checks every single-gene change of every hand-made
design for correctness only - 125 changes; `SCAN.md` has the result.

`--sample N` draws designs uniformly from the whole space - the check
that the front is a peak and not a plateau; `SEARCH-SPACE.md` has the
space itself: its axes, what the gene pool leaves out and why, and the
first sample.

It exposed a flaw in the survival check itself. The kernel workload runs
in a directory that starts with a copy of the reference kernel, and the
check compared that file afterwards - so a design that died quietly
before saving passed. Every earlier run has that flaw: designs counted
alive may never have finished the kernel workload, and their kernel
times, cut short, would look fast. The check now removes the file first;
the hand-made stages all still pass.

With the strict check, every death has a real cause. Two-byte-only forms
(calls without `varcall`, near DOES> calls) reach 2^14 units - 16 KB at
scale 0, 32 KB at scale 1 - and the kernel workload's dictionary is
larger; with both far forms the same designs live. And the scan found a
fourth mapping bug: DODOES decodes the far form only under VARCALL, so
`doesfar` is now dormant, built off, without `varcall`.

A broken design executes arbitrary code, and the engine's primitives
include fork and execve. Leftover processes held pipes open past every
timeout, and probably crashed the container once; every engine run now
has a process group of its own, killed whole on timeout, and a CPU cap.

## Phase 3a: relf's format-10 opcodes

`ops10`: seven kernel colon words - `EXECUTE`, `I`, `(DO)`, `+!`, `?DUP`,
`UNLOOP`, `J` - as one-byte opcodes, in the free slots before the pairs
take theirs, so the three compete. The converter substitutes a call only
where the word's compiled body is exactly the definition the engine
implements (the same check as the tiny family; `SOD16_SHOW=NAME,...`
prints how a word reads). As opcodes the return-stack words have no
return address of their own: `I` is the top cell, `J` two below.

Development VM, against the parent: s4 with all seven, 0.964 of the time
and 32 bytes smaller; with 20 pairs as well, 0.843 and 96 smaller; s6 with
the two its free slots hold, `EXECUTE` and `I`, 0.981 and 16 smaller.
Parse and corpus gain most: the outer interpreter runs every word it
interprets through `EXECUTE`. Each word alone passes the strict check in
s4, s5 and s6, and the scan now tries each one.

That check found a hazard in the engine's macros: in the top-of-stack
build, `PUSH(x)` lowers dsp BEFORE it evaluates x, so `PUSH(DS0)` copies
the new, empty slot onto itself. `?DUP` failed in s5 and s6 only; it now
takes the value first.

## Phase 3b: the escape, and the BUF-ALLOC fault

relf's map keeps 26 primitives in one byte and puts 77 behind an escape;
the slots that frees are what pays for its tiny words. The engine lab and
the converter had the escaped band already - primitives 36-67 as 125 and a
selector - but the converter kept it OFF "until the BUF-ALLOC fault is
found". Switched on, s4 passed and s5 and s6 died at start-up of the
kernel workload, a segmentation fault: only the engines that cache the
top of the stack in a register. gen-tos.py wraps any handler not on its
list of ones that never touch the data stack in SPILL / FILL, and L_esc -
which only reads its selector and jumps - was not on it. So every escaped
primitive started with the top of the stack pushed once more. Listed,
the escape passes the strict check in all three.

`escape` puts the freed band in the slot pool, where words and pairs go
in by run-time assignment into the remapped table (the base table still
holds the escaped primitives there). Development VM, against the parent:
the escape alone is about neutral, s6 0.984 and 40 bytes bigger; with the
seven words and all 24 pairs, which the two free slots of s6 could not
hold, s6 0.888 and 72 bytes smaller, s5 0.950 and 96 smaller. The scan
tries the escape on every CV8 design and finds no new death.

## Phase 3c: the loop words with an operand

`(LOOP)`, `(?DO)`, `(+LOOP)` and `(LEAVE)` read an operand cell after
the call through their return address. As opcodes they become BRANCH
kinds: call and operand are two cells, as ?BRANCH is, and the operand's
target is reckoned the same way, so the converter lays them out and emits
them as ?BRANCH - a two-byte offset from the operand - with their own
opcode. A site shrinks from a call, padding and a cell to three bytes.
The handlers follow the kernel's definitions; `(+LOOP)` leaves when
index - limit changes sign, as the kernel's does.

The image code uses LOOP in three places and ?DO, +LOOP and LEAVE in
none, so those three are right but idle here. s4 with all eleven words,
144 bytes smaller; s6 with the escape, eleven words and 24 pairs, 0.871
of the time and 72 bytes smaller (VM; these moved by a few per cent from
run to run). Each word alone passes the strict check in s4, s5 and s6.

One slip caught by that check: the handlers first used BROFF, which only
the generated top-of-stack engine defines - s4, the plain engine, did not
link; they now read `(int16_t)LD16(ip)`, as the plain engine's ?BRANCH
does.

## Phase 3d: short branches, and the format-10 words in the cached engine

`?BRANCH8` and `BRANCH8` take a one-byte offset where it fits. They are
in `ops10` as two pseudo-words, taking slots like the rest; the converter
decides branch by branch (`shorten`), on a layout that counts every
alignment at its widest - so real offsets can only be smaller - going
long where a branch does not fit and redoing the layout until nothing
changes. About 166 branches in the image code: s6 200 bytes smaller, s5
136, s4 192, at the same speed (s6 1.007, within noise) - a size gene.

The format-10 words now have bodies written for the cached top of stack
in gen-tos.py, instead of the generic SPILL / FILL wrapper - `?BRANCH8`
above all, which runs on every IF and loop. s6 with the escape, all
thirteen opcodes and 24 pairs: 0.880 of the time and 256 bytes smaller,
every workload faster, the held-out loop 0.926 (VM). Each opcode alone
passes the strict check in s4, s5 and s6; the scan finds no new death.

@XT, relf's fused @ EXECUTE, is not taken: relf's kernel calls through
vectors, and this one has no `@ EXECUTE` in the image's code at all.

## Phase 4: tail-call threading

`tools/gen-tail.py` takes a design's cached engine preprocessed with the
256-entry dispatch (`cc -E -P`), where every #if and macro is resolved
and every dispatch is one statement, and makes each handler a function of
(ip, dsp, rp, tos, t) - all five in argument registers - ending in a tail
call through a table of functions. The bodies are unchanged; only their
jumps are rewritten, and the label tables become function tables. Each
handler is small, so its registers are allocated for it alone.

GCC 13 has no musttail; the tail calls are -O2's sibling calls, and a
handler that keeps its frame does not get one: five pass a local's
address to the system (fstat's struct, pipe's descriptors, waitpid's
status), and fork returns twice. Their dispatch was a CALL - a frame left
on the C stack each time - so the build reads the machine code for an
indexed indirect call in a handler, splits those handlers (an inner
function runs the body and returns the next function; the outer one
tail-calls it) and checks again: none may be left.

It is a trade-off, not a free gain (VM): s6 with tail calls 0.964 - fib
0.876, loop 0.887, parse 0.938, but kernel 1.045; s5 1.021, slower; s6
with the escape, thirteen opcodes and 24 pairs 0.889, and with tail calls
too 0.871. The kernel workload is slower with tail calls throughout. The
scan tries tail calls on s5 and s6; both live.

A slip on the way: inserting the tail rules between an if and its elif in
express() made doesfar dormant in every design without tail calls - the
scan showed it at once (s6's doesfar=0 death vanished). Restored.

## Phase 5: multi-state stack caching

`tools/gen-msc.py` rewrites a design's cached engine for three states -
nothing, the top, or the top two items in registers (`tos`, `nos`) - with
a dispatch table each. A handler variant knows the state it ends in and
dispatches through that state's table, so the state needs no variable.
Operations with a stack effect the generator knows are generated for each
input state, keeping as much in registers as fits (as gforth's vmgen):
DUP in state 1 ends in state 2 without touching memory. Every other
handler keeps its one-register body, reached from states 0 and 2 through
one normaliser each; NOOP, EXIT, BRANCH and the call path have a copy per
state. The extra tables are filled at start-up by comparing label
addresses, so they follow any opcode assignment.

The first version specified only 25 primitives, and lost: s6 1.049, s5
1.110 (VM). The cost was the normaliser - a second dispatch for every
other operation reached from states 0 and 2, and the folds, the tiny
words, the literals and immediates and the variables are exactly what s5
and s6 run most. With those specified too (72 operations, folds built as
their primitive's effect plus the return, and the format-10 opcodes but
?DUP), s6 0.941, s5 0.956 - fib 0.845, loop 0.815, but kernel 1.025. s6
with the escape, thirteen opcodes and 24 pairs: 0.886 without, 0.882 with:
the pairs were not specified. Composing their effects from their two
halves - a symbolic stack: the second half takes the first's outputs,
then deeper items; what passes between them is a temporary - changed
that: with the same combination and multi-state caching, s6 0.826 (kernel
0.908, fib 0.836, parse 0.736, corpus 0.835, loop 0.831), s5 0.863. The
best design so far, and faster than s6 on every workload.

It excludes tail calls (both are made from the one-register engine).
Every combination tried passes the strict check; the scan tries it on s5
and s6, and both live.

## Phase 5b: each design's own pairs

The pairs gene drew from one fixed pool: the 24 pairs a profile of s6
dispatched most. But a design that already fuses some pairs, or has folds,
specialisations or format-10 words, leaves others hot. `design_pairs`
builds the parent with the engine's profiler (VMPROF), runs the four
selection workloads, and ranks its own primitive pairs (the opcodes map
back through the design's own opcode map, the escape's included; folds,
pairs and words are not primitives and drop out). A mutation adding a pair
draws from that; a design is profiled once, when first used as a parent,
in about 2 s, with tail calls and multi-state caching off - the stream,
not the dispatch, decides the pairs.

The pools differ as they should: s6's is close to the fixed one (3 of 24
new); s6 with DUP >R and C! R> fused no longer offers them, and R@ ROT,
DUP C@ and OVER C@ lead (5 new); s4, whose tiny words are calls, has + SWAP
and + DUP on top (9 new). Mutating s4, every pair added came from its own
pool, 4 of 6 from outside the fixed one. Founders keep the fixed pool.

## Measuring on a machine that is not quiet

The run happens on a laptop with other processes that cannot be stopped,
so the evolver now measures the engine process's own CPU time (user +
system), not cycles, and pairs every timed run of a design with one of
hand-made s6, back to back, alternating order: a design's speed is its
CPU time over s6's, geometric mean over the selection workloads. Drift
over hours cancels; s6 against itself comes out within 1% of 1.0. The
correctness limits are CPU time as well (5 s corpus, 10 s kernel), with a
wall-clock backstop, so a correct design waiting its turn is not killed.
Runs are pinned to the core that, with its hyperthread sibling, was
quietest at start-up, unless BENCH_CPU says otherwise. `RUNNING.md` is
the guide to the run; `tools/bench-laptop.sh` defaults to CPU time too.

## Phase 6: the first run on the Ryzen

`results/evolve-amd-ryzen-7-pro-8840hs-seed1.md`. Measured again, the
front is 38d187239c (0.609 of s6's CPU time, 13,480 bytes), 5b70f3dd64
(0.649, 9,801 - smaller than s6) and 83cb81c383 (0.705, 9,761); the run's
own leader fell from 0.590 to 0.620 and off the front. All have the
escape, multi-state caching, format-10 opcodes and about 22 pairs. The
VM rehearsal's front, selected on another machine and re-measured on the
Ryzen, reached the same level - 0.605 at 13,480 bytes: two searches, one
answer. The run's recorded death reasons exposed the last two evolver
bugs (679e6f3).

## Next

`GENES.md` lists what other VMs could add - load-time translation to
direct threading, indirect threading, SPN's
genes, a register machine - each needing engine work before evolution can
use it.

## Selection since Iteration 188: demote, don't delete

The owner: a small size increase for a big speed gain is a gain, and designs
with potential must not be filtered out. Survival still keeps the best N of
parents and children by front and crowding, and each family's best; and now
the 8 best by Q (binary + image x run time x memory - the knee; EVOLVE_Q_KEEP)
always survive too. What falls out is demoted, not deleted, when it carries a
gene value no survivor has: the attic (EVOLVE_ATTIC, 128) keeps such designs,
the rarest genes first, until the population has those values again. One
parent in ten comes from the attic (EVOLVE_ATTIC_P), and a borrowed gene may
come from there - a stepping stone keeps its chance, at no measuring cost.
Children of attic parents say "via the attic" in how they were made.
EVOLVE_ATTIC=0 turns the attic off.

## rtloop=2 (Iteration 190): the loop compiler's internal words headerless

forth/cv8-fuse-loop.4 defines eight words only its own code calls, or the
converter fills by name in the dump: X10-OP, W@, CHAIN16?, RESOLVE-LEAVE16,
RESOLVE-LEAVES, LOOP-OPS, X10-XTS, X10-OPS. With rtloop=2 the converter
(tools/layout.py --headerless) keeps their code and drops their headers - no
link, no name, on no thread; its chain check expects the rest. Only a name
defined once loses its header: hiding the later of two would hand the name
back to the earlier. 96-108 bytes a design; rtloop costs +460 bytes on seed
40's smallest instead of +568, for -72% loop time. Under rtloopall (its own
overlay) rtloop=2 expresses as 1: the same build, one id.

## Variation since Iteration 197 (results/gp-deep-dive.md)

Seed 40's database: mutation-only children made 73% of the final front from a
quarter of the children; crossover, 60% of variation, was twelve times less
productive per child. Now: crossover 0.25 (EVOLVE_XOVER); genes linked on the
front (mutual information 0.67-1.00: the JIT's four, tos/tail/msc,
escape/rtloopall, rtfuse/rtimm) inherited whole from one parent (LINKS) - the
uniform choice gene by gene split them; varcall and doesfar, whose mutants
were almost never better than their parent, drawn one time in ten
(SLOW_GENES). In the generation's ranking, speed within 2% is a tie as memory
within 8 KB is (EVOLVE_SPEED_TOL; seed 40's front measured again moved +-2.6%
at 5-95%); the reports' and the carry's fronts stay exact.

## regpin (Iteration 197, results/forth-implementations-survey.md)

Gforth tunes its build by pinning the VM registers to machine registers; ours
left them to GCC. regpin 1-3 pins ip, rp and dsp (and tos) to callee-saved
registers in three assignments (engine/vm-lab.c VMREGS, tools/gen-tos.py).
Measured on the development VM: the smallest and the small knee +800-930 bytes
and no faster (the knee 4-7% slower); the fastest JIT design 160-320 bytes
smaller at equal speed - a point of the front. The laptop decides.

## Short branches kept long (Iteration 199)

The converter decides which branches can be short before the tag-2 map
exists, with escaped opcodes counted as one byte and calls as two; a loop
body near 128 bytes could then encode a few bytes past reach - seed 41 lost 37
designs at -131 to -135. Now the encoding records each such branch (its word,
its cell offset) instead of asserting, tools/layout.py writes them to
--long-branches FILE and exits 4, and evolve.py converts again with them kept
long (up to four times; the set only grows). A design that converted before
meets none and is byte for byte as it was.

## The surrogate screen (Iteration 200)

A child whose predicted speed and binary + image are both beaten - by 30% and
5% - by what was measured before its generation is not measured: recorded
`screened` (not a death; the report counts them apart). The model is
additive, one weight per gene value, fitted in pure Python on the earlier
generations' living designs every 10 generations; seed 40 offline: a third of
the children skipped, 1 of 163 final-front designs lost
(results/drafts/surrogate-offline.md). One screened child in ten, chosen by
id, is measured anyway ("screened, audited") - the screen checked as it runs.
Deterministic, so a resumed run decides the same. Settings: EVOLVE_SCREEN (0
off), EVOLVE_SCREEN_MARGINS (0.30,0.05), EVOLVE_SCREEN_AUDIT (10),
EVOLVE_SCREEN_FROM (generation 5), EVOLVE_SCREEN_EVERY (10), EVOLVE_SCREEN_MIN
(1,000 designs).

## fsys (Iteration 202): file words in Forth, their handlers out

27 of the 68 primitives never ran in the eight workloads (s6 profiled); 17
were the shell's, in Forth over SYSCALL since Iteration 147. fsys=1 does the
same for six file words and RESIZE: forth/file-sysc.4 (with ALLOCATE and FREE
in Forth too, for RESIZE's sake - SAVE-SYSTEM keeps the native pair) is
loaded last in a -fsys dump, and the engine (FSYS) points the seven dispatch
entries at L_nosys; SYSCALL -4 drops a file's read-ahead as the handlers did.
Its helpers are headerless. A design without the gene builds from the dumps it
always did: byte for byte as before. Measured: engine -608 bytes and image +504
(the smallest, total -104), the fastest -328 in all; the standard suite whole
on fsys=1 designs (ans-check, ANS_SET=fsys=1).

## threads (Iteration 204): the dictionary's chains

The loop audit (results/loop-audit.md): the name lookup - a walk down one hash
chain - was ~60% of corpus and parse on the smallest design. The converter
now files the dictionary into N chains (--threads; FORTH-WORDLIST's body its
count and N heads; the links sized by the chains they end up on): 0 keeps the
dump's 32, 1-3 give 64, 128 and 16. Every lookup path takes the count from the
word list (HASH, the native FIND and HASH, WORDLIST copying FORTH-WORDLIST's),
so nothing else changes. Counted on the smallest (kernel, corpus, parse):
16 chains +17%, +49%, +53% dispatches for 128 bytes less; 64 chains -9%, -28%,
-27% for ~240 bytes more; 128 chains -14%, -41%, -43% for ~700. The standard
suite whole at 16, 64 and 128; at 32 every image byte for byte as before.

## fsys 2 (Iteration 205): the single-SYSCALL family, stage A

fsys now takes 0 (every I/O primitive native), 1 (six file words and RESIZE
in Forth) and 2: OPEN-FILE, CLOSE-FILE, WRITE-FILE, ALLOCATE and FREE too
(forth/file-sysc2.4, loaded after file-sysc.4 in an -fsys2 dump). The kernel
compiled INCLUDED and SAVE-SYSTEM against those primitives, so the converter
rebinds every compiled use to the Forth word (--rebind: ('P', name) becomes a
call), and the engine (FSYS=2) drops their five handlers - the C runtime's
allocator with them. Measured: the smallest 628 bytes smaller in all, the knee
644, the fastest 1,039; every design through the full gate (the kernel
workload opens its files through the Forth words); the standard suite 14 of 14
as s6. Stage B: WRITE with its buffer on the heap, READ, READ-LINE, BYE.

## fsys 3 (Iteration 206): the single-SYSCALL family, stage B

WRITE, READ, READ-LINE and BYE in Forth over SYSCALL too (forth/file-
sysc3.4), as the owner set them: no output buffer (WRITE one write(2) a call,
EMIT one a character) and no read-ahead from stdin, pipes or anything that
cannot seek. READ is the engine's t_read in Forth; READ-LINE reads into the
caller's own buffer and seeks back after the line where the file can seek, a
byte at a time where it cannot. Their handlers leave the engine; the engine's
I/O is SYSCALL alone. The converter rebinds a stub-shaped colon word too -
TYPE is `WRITE ;`, which read_ops took for a primitive stub and left calling
the handler that was gone. Measured: the smallest 1,217 bytes smaller in all
(fsys 2: 628), the fastest 1,921; the I/O workloads slower - the kernel
workload +37-89%, the corpus +23-88% - fib and bubble not; the standard suite
14 of 14 as s6. Evolution weighs 0 to 3.

## fsys 4 (Iteration 207): the single-SYSCALL family with the output buffered

The owner: a buffered-output level for evolution, with tests that buffering
breaks nothing. The standard leaves buffering open; Gforth's practice and
proposal (complang.tuwien.ac.at/forth/ansforth-cvs/buffering.html): never
buffer input; never buffer output to a terminal; buffer it to a pipe or a
file. fsys 4 is fsys 3 with WRITE so (forth/file-sysc4.4): it asks once
(ioctl TCGETS) - on a terminal it writes at once, elsewhere into 4 KB on the
heap whose [address, fill] the engine knows (SYSCALL -5), so t_flush empties
it wherever the native engine flushed its own: before every system call,
before a read blocks, at every exit and fault. lab/evolve/outbuf-check.py
tests it against native: stdout and stderr on one pipe (ten programs, byte
for byte; a signal death where native loses output the levels keep), the
prompt shown before a blocking read, and a terminal shown at once (native
holds it). The workloads print little: fsys 4 is about fsys 3's speed - their
cost is READ-LINE's scan and system calls a line, not the output.

## fsys 3 and 4, READ-LINE (Iteration 208)

READ-LINE finds the line's end with SCAN (a native opcode under kinput, the
kernel's loop otherwise) and asks whether a file can seek once per
descriptor (0-63; OPEN-FILE and CLOSE-FILE forget it) - a system call a line
fewer. The fastest design (kinput) went from 27% to 16% slower than fsys 2;
designs without kinput keep their SCAN loop. ~150 bytes for it.

## fsys 5 (Iteration 211): READ-LINE reading ahead where a file can seek

fsys 4 with READ-LINE reading 4 KB at a time into a heap buffer on a seekable
descriptor (1-63; never stdin or a pipe - the owner's rule), and every other
use of the file - READ-FILE, the positioning words, WRITE-FILE, WRITE-LINE,
CLOSE-FILE - first giving back what was read ahead by lseek(2), as the native
engine's t_fgetc and t_fdrop did (forth/file-sysc5.4). The state on the heap.
Measured (VM, noisy): between fsys 4 and native - the fastest design 7%
behind native (fsys 4: 17%), the corpus nearly native's - for ~630 bytes over
fsys 4. Also Iteration 211: the converter's --rebind took the OLDEST
redefinition (the dump lists words newest first), so fsys 4's buffered WRITE
was never bound and INCLUDED used fsys 2's OPEN-FILE and CLOSE-FILE, not fsys
3's forgetting wrappers - now the newest, by address.

## The dump guard (Iteration 212, the owner)

A library that does not load whole stops the run at setup, rather than
letting an older definition of the same name stand in and every gate pass -
as file-sysc5.4 once did, at a remark outside a comment, with fsys 3's
READ-LINE answering for fsys 5's. Each dump is checked as it is made: its load
messages hold none of the kernel's load errors (Undefined word, dictionary
full, name too long, Incomplete control structure, compile only, Not found,
Error reading file); every name each loaded file defines is in the dump; and
each such name is there as often as the bare kernel (one extra load) and the
loaded files define it - by count, so a failed REdefinition shows though an
older one of its name stands. Tested: the original remark - stopped, FS-FILL
and FS-TAKE missing; READ-LINE alone broken - stopped, READ-LINE 2 of 3. All
2,666 dumps pass (22 files, 286 names).

## fsys 5 tightened (Iteration 214)

fsys 5's READ-LINE cost more dispatches than fsys 4's (the kernel workload on
seed 42's smallest: 6.95M against 6.76M) - its bookkeeping in Forth: the seek
test on every call, six variables, the table's index arithmetic. Now a line
whose LF is already in the buffer, within the caller's room, is taken at once:
one SCAN, one CMOVE, the entry's next moved past the LF - no seek test (an
entry holding unread bytes belongs to a file that seeks: every open, close and
other use empties it) and no variables; next and end are addresses, equal when
nothing is read ahead. Every other case - the buffer empty or the line running
past it, the room filled, the end of the file - goes the general way, with two
variables where there were six. Counted, fsys 4 -> 5: the kernel workload
-2.2% on the smallest and -12.5% on the fastest (they were +2.8% and +3.8%),
the corpus -0.4% and -9.7%; 33-53 image bytes fewer than before. A design
whose CMOVE is the kernel's byte loop (no opcode slot - seed 42's best by Q)
still pays for copying the lines out: kernel +45%, corpus +21% (+62%, +33%
before). lab/evolve/readline-check.py runs READ-LINE at fsys 3, 4 and 5
against native, byte for byte, and judges WRITE-LINE after a line by the
file's bytes: native's WRITE-LINE does not give back what it read ahead.

Iteration 246: the gene jittail (0/1, JIT designs; in LATE, EXPRESSED and the
JIT's crossover link): the translator turns a call to a native word whose next
operation is EXIT - or a BRANCH chain to one - into a jump, so tail recursion
runs in place. Ackermann 15-18% faster on the VM (two of -ack's three calls are
tail calls), the other selection workloads within noise; +256 engine bytes; off,
the engine is byte-identical (results/price-jit-calls.md).

Iteration 259: the gene jitk (0, 2 or 3 cells; JIT designs; in LATE, EXPRESSED and
the JIT's crossover link): the JIT keeps the top K data-stack cells in fixed
registers across its copied code. tools/gen-jitk.py generates, per build, the
variant stencils (16 hot operations x K+1 states) and canonicalisers, and a map
the translator plans each operation with; anything without a variant, and every
branch target, runs in state 1. Measured on the VM: mixed (loop -9%, fib +16% at
K=2); +2.3-2.8 KB of engine. Built so the laptop's evolution measures it.

Iteration 267: the gene factor (0-3; tag-2 designs; in LATE, EXPRESSED, mutation
and drawing): the converter (tools/layout.py --factor --factor-hot FILE
--factor-share X) moves repeated straight-line code into headerless bodies the
image never names - each use a 2-byte call, then a GAP holding the run's old
cells, so every branch, loop-operand, xt and DOES>-entry offset stays right. A
word takes part when it is below X of the selection workloads' dispatches in
the reference profile (lab/evolve/hotwords.py -> hotwords-v1.json: five of seed
46's front, the JIT off; a word missing from it keeps its code). FACTORV: 0
off, 1e-3, 1e-2, every word. On the smallest design -41, -95 and -127 image
bytes for +0.007%, +0.17% and +1.98% dispatches. Off, every design converts byte
for byte as before (results/drafts/factor-plan.md, PROGRESS.md Iteration 267).

Iteration 276: the gene table (prompts/17-variants-as-data). A gene is one row,
`gene(name, values, show, family, late, needs, convert)`, which LATE, EXPRESSED,
mutate(), random_genome(), express() and the converter's options all read; factor
is the first such row. The older genes with more than two values keep their
rules and build code, their values once in GENE_VALUES. Ids, expressions and
seeded mutations, random draws and crossovers are identical before and after
(GENES.md, "Adding a gene"); gene-table-test.py checks a fictional gene end to
end, with a control.

Iteration 278: 31 older genes moved into rows - rules, values, five converter
flags (GENES.md, "Adding a gene", says which and what stays code, and why).
gene-equiv.py now also judges the 5,000 genomes it makes - mutations, random
genomes, crossovers - by id and expression, reaching combinations no recorded
design has; against the commit before, every id, expression and seeded draw the
same, after it caught rtfuse made late by default (875 ids). counters.py, the
laptop's hardware counters; c-baseline.py and counters.py pick their designs
from the newest front (evolve.newest_front).

Iteration 290: 2@ and 2! join the ops10 pool and opbody's list - the handlers in
vm-lab.c, gen-tos.py and gen-msc.py (gen-tail.py takes them as it finds them; the
JIT, meeting an opcode it does not translate, leaves the word to the interpreter),
their kernel bodies in sod16.py's table as the converter reads them (SOD16_SHOW).
Five engines-check paths carry them: s6, the cached top off, multi-state, tail
calls, the JIT. word-cost.py and gate.py take --set; a list adds its members to a
design's own. The audit that found them: results/source-audit-2.md.

Iteration 292: the gene opinline - the [opcode EXIT] words placed among the
primitives (layout.py --op-inline), so PRIMITIVE?, asking by address, lets every
run-time COMPILE, copy their opcode: code compiled at run time stops calling them.
Five engines-check paths carry it, on the 2@ and 2! ones.

Iteration 293: the gene tailpn - gen-tail.py --preserve-none: clang 19+'s
preserve_none on every handler of the tail-call engine and musttail on every
handler-to-handler call, built with clang_pn(), the newest clang here that takes
them. A versioned clang (clang-19, clang-20) is a build tool now, not jailed as an
engine: the jail's no-new-process rule had kept its driver from the linker.

Iteration 295: the gene knumber - NUMBER? as one opcode, for klookup designs:
forth/cv8b-knumber.4 ((NUMBER?) and NUMBER?8, a stage tag -knumber of its own), the
handler's C in one helper (numberq) for the plain, cached-top and multi-state engines,
its kernel body as the converter reads it in sod16.py's table. Five engines-check paths.

Iteration 298: the gene alignhot - GCC's -falign-jumps/-labels/-functions at 32:11, 32
or 64 bytes, for the front end the laptop's counters found the evolved interpreted
designs stalling in; GCC only, not with align1 or alignfn. Five engines-check paths.

Iteration 299: > and 0= join the ops10 pool and opbody's list (handlers L_x_gt and
L_x_zeq; their kernel bodies were in sod16.py's table already). Five engines-check
paths, with opinline. The audit that found them: results/source-audit-3.md.

Iteration 312: lab/evolve/regressions.json - designs that once failed, each its whole
recorded genome and why; engines-check builds every one and runs it on the corpus, so a
fault found once stays a test. The first two: seed 52's JIT designs whose (LOOP) stencil
was read short (jit.c's scan, 64 bytes without jitloop; now 160 in every build, and every
branching stencil must show both its exits or is not used).

Iteration 338: selecting at both widths (results/drafts/two-width-selection.md). `evolve.py
--widths 8,4` - each design that passes screening is also measured as a 32-bit x86 engine at 4-byte
cells on this machine (gcc -m32; its JIT off - a JIT design judged at 32 bits by the interpreter
under it - and its call scale at most 2, cell-aligned calls being the 32-bit build's), and that
speed32 is a fourth objective on the front beside speed, size and memory; without the flag nothing
changes. NEXT-RUN's word for it: `widths` (seed N tag2 6h widths). The report shows a 32-bit speed
column and seed-facts.py two-width lines whenever the records carry speed32. compare-fronts.py still
judges runs at 64 bits - its five measures, comparable with every earlier session. Since Iteration
375 its 32-bit section adds the verdict at both widths for the run being judged: the five, and its
fastest at 32 bits under 5% against the others' (GOALS.md; the owner confirmed it, Iteration 376).

