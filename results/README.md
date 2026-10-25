# Results - every measurement and analysis, indexed

One line each, by topic: the file, then its own title. Each per-run record names the
machine and run it came from. `tools/handoff-check.py` fails when a document here is
missing from this index (README.md, "Documents", indexes everything else).

## The evolution, run by run

- `evolve-amd-ryzen-7-pro-8840hs-seedN.md` - each run, seeds 1-60 (none for seed 48, the owner's choice; Iteration 384 brought this line from 47): the verdict and the facts, then the pack's report with every front design's genome (the gate, ans-check and the other tools read genomes from these).
- `evolve-amd-ryzen-7-pro-8840hs-seed4b.md` - Evolution on the Ryzen 7 PRO 8840HS - seed 4 again: a replicate.
- `compare-fronts-amd-ryzen-7-pro-8840hs.md` - every comparison session: the fronts of all runs measured again together, judged by the five measures.
- `predictions.md` - the predictions written before each run, then scored.
- `progress-by-run.md` - every run's extremes, for the progress charts (lab/evolve/progress-table.py).
- `applied-after-seedN/ORDER.md` - each batch of patches applied after a run: the order, and how each patch was tested.
- `audit-genes-designs-439.md` - Are good genes or promising designs being rejected? (Iteration 439): every place the pipeline turns designs away, checked - the screen costs about 9 front-quality designs a run, the 32-bit tail failures fixed and verified; the one real rejection, rtloopall's eight-word prerequisite (92 of 5,819 genomes could express it in seed 62), rtiplus behind it; four recommendations.
- `applied-after-seed71/` - the after-seed-71 batch, applied at seed 71's processing (Iteration 516): six patches - nocase retired, jithelp and jitre retired, jitfuse and its enabling, the MARKER fix (jit_k's signature) with its test, and the outputs checked in measure() (the applications loophole) with jitrp kept from lto; ORDER.md with how each was tested.
- `applied-after-seed70/` - the after-seed-70 batch, applied at seed 70's processing (Iteration 498): six patches - more JIT coverage (ABORT", word ends, depth), 2>R in place, the new genes at 32 bits (and CELL+/CELLS by the cell), jitrp, the owner's decisions (the applications the seventh selection workload, jitos frozen, jitrp enabled), nocase staged; ORDER.md with how each was tested; batch-check PASS on cc6cdcd.
- `applied-after-seed68/` - the after-seed-68 batch, applied at seed 69's processing (Iteration 487): the JIT at 32-bit x86 (engine and lab), the stencil check; ORDER.md with how each patch was tested and its rebases (475-486, the engine patch repaired at 486); batch-check PASS on e5c6239.
- `seed63-rules.md` - Seed 63's decisions, the rules written before its results (Iterations 430-431, adopted): ten rules and the gene rule - a gene out only after three runs unused, no front design depending on it, frozen off for a run first; checked against losing good designs (a one-run rule would have marked jitimg, jitvar, jitos, rtimm and opcall out in turn; the freeze loses nothing).
- `gene-votes.md` - The gene votes, run by run (from Iteration 432): each gene's four removal votes a run - under 10% of the front, in none of its fastest, smallest, best-Q tenths - appended at each processing from seed 63 on; results/seed63-rules.md says how they count.
- `candidates-generic.md` - Designs kept by id that no front holds (Iteration 430): bf439eb307's record, for xcheck --also - the candidates for the best design across the machine classes.
- `drafts/runner-protocol.md` - The runner's protocol, the owner's requirements as a specification (Iterations 302-303): one command, one archive with every log, a clean stop, recovery at every start.
- `relf-patches/README.md` - Patches for relf from this lab (Iteration 360): each with its gate, its dispatch count and its time; the first, 0= ?BRANCH fused.
- `relf-pairs-realistic.md` - relf's realistic shell script by instruction and by adjacent pair (Iteration 358): VAR@ 15.2 %, VAR@ VAR@ 4.2 %, VAR@ + 3.1 %; relf's 64 one-byte opcodes (A15) as the constraint.
- `xcheck-seed56.md` - The first run checked on four machines (Iteration 354): the Tegra's first native run (ARMv7, Spearman 0.944), dream.lan at 64 bits, at 32, and the same designs at 64 - the skew the width's, not the machine's.
- `xcheck-seed57.md` - The checks of seed 56's front during seed 57 (Iteration 378): dream 64-bit Spearman 0.980; at 32 bits 0.713, the same designs at 64 bits 0.949 - the width's skew again; the Tegra 0.881.
- `xcheck-seed58.md` - The checks of seed 57's front during seed 58, and seed 57's rejected designs (Iteration 384): the Tegra Spearman 0.973, dream 64-bit 0.959, 32-bit 0.875; no rejected design faster on any host than the front's fastest (item 4d); three Tegra link failures (regpin=1 with lto=1).
- `xcheck-seed71.md` - The checks of seed 70's front during seed 71 (Iteration 516): dream 0.804 (default, 24), 0.969 (32-bit), 0.966 (64-bit); the Tegra 0.607 (7).
- `xcheck-seed70.md` - The checks of seed 69's front during seed 70 (Iteration 498): dream 0.941 (default), 0.935 (32-bit), 0.959 (64-bit); the Tegra 0.929 (8 designs); against the laptop's 32-bit speeds 0.893 and 0.800.
- `xcheck-seed69.md` - The checks of seed 68's front during seed 69 (Iteration 487): dream at three builds (0.963 default, 0.862 at 32 bits, 0.863 at 64) and the Tegra (0.965, 16 designs); against the laptop's 32-bit speeds 0.928 and 0.881.
- `xcheck-seed68.md` - The checks of seed 67's front during seed 68 (Iteration 464): dream 0.966 (default), 0.963 (64-bit), 0.946 (32-bit).
- `xcheck-seed67.md` - The checks of seed 66's front during seed 67 (Iteration 458): dream 0.962 (default), 0.987 (64-bit), 0.833 (32-bit); the Tegra 0.618 (16).
- `xcheck-seed66.md` - The checks of seed 65's front during seed 66 (Iteration 454): dream 0.963 (default), 0.977 (64-bit), 0.809 (32-bit); the Tegra 0.818 (16); ad0975a72e, rejected by seed 65's selection, faster than the front's median on every host.
- `xcheck-seed65.md` - The checks of seed 64's front during seed 65 (Iteration 449): dream 0.959 (default), 0.937 (64-bit), 0.837 (32-bit); the Tegra 0.857 over 7 - only 3 of seed 64's front are GCC without the JIT, all the Tegra builds as themselves.
- `xcheck-seed64.md` - The checks of seed 63's front during seed 64 (Iteration 443): dream 0.707 (default), 0.946 (64-bit), 0.753 (32-bit); the Tegra 0.771; cf524f4c20, rejected by seed 63's selection, faster than the front's median on every host and first across the machine classes (mean 0.409).
- `xcheck-seed63.md` - The checks of seed 62's front during seed 63 (Iteration 441): dream 0.723 (default), 0.932 (64-bit), 0.834 (32-bit); the Tegra 0.912; the Tegra's rebuild test - all 7 asked for built, item 0d closed; the head to head - seed 62's 5f512a3017 first across the machine classes (mean 0.419).
- `xcheck-seed62.md` - The checks of seed 61's front during seed 62 (Iteration 433): dream 0.943 (default), 0.958 (64-bit), 0.945 (32-bit); the Tegra 0.847, all 16 built; two rejected designs faster than the front's fastest there; on all three classes only 5 small-end designs - the head to head moved to seed 63's chain.
- `xcheck-seed61.md` - The checks of seed 60's front during seed 61 (Iteration 425): dream 0.863 (default), 0.910 (64-bit), 0.929 (32-bit); the Tegra 0.991, all 16 built - none of seed 60's front carries alignhot above 1.
- `xcheck-seed60.md` - The checks of seed 59's front during seed 60 (Iteration 406): dream 64-bit 0.941/0.721, 32-bit 0.370; the Tegra's six failures named - the assembler's bad immediate offset, every one alignhot 64 (item 0d).
- `xcheck-seed59.md` - The checks of seed 58's front during seed 59 (Iteration 398): dream 64-bit 0.959/0.963, 32-bit 0.651, the Tegra 0.709 (against the laptop's 64-bit speeds - open item 0g); no rejected design faster; the probes: copies in a second, the Tegra's wait its own build.
- `xcheck-dream-seed55.md` - The first check at both widths (Iteration 334): dream.lan 64-bit Spearman 0.940; 32-bit x86 at 4-byte cells 0.694 - the laptop's six fastest interpreted designs 8th-13th there: the skew the owner feared.
- `xcheck-dream-seed54.md` - The second remote check (Iteration 333): seed 53's front on dream.lan - Spearman 0.941, the laptop's six fastest ranked 3 4 2 10 1 5 there.
- `drafts/two-width-scratch-db.jsonl` - The second two-width scratch run's database (Iteration 337): its designs without speed32, to reproduce.
- `drafts/cross-machine-weighing.md` - Weighing results across machines (Iteration 376, a proposal for the owner): what the checks show, the blind spot (only the laptop's front is checked elsewhere), and a policy for choosing designs good on every class of machine.
- `drafts/gene-usage-53-56.md` - What the search chose (Iteration 372): every gene on the fronts of seeds 53-56 (722 designs) - never on (msc, scale, tail), rarely on, on everywhere; the evidence for the simplicity review after seed 57.
- `drafts/gene-usage-53-59.md` - Seed 59's front against seeds 53-58's (Iteration 403): msc, scale, tail still never on; rtloopall, escape, supers, guard up to 56 points more, tos 39 fewer - a run without the carry ends elsewhere.
- `drafts/gene-usage-53-60.md` - The genes on seeds 53-60's fronts together, 1,431 designs (Iteration 408): eight on in every design, msc, scale and tail in none.
- `drafts/simplicity-proposal-408.md` - The simplicity review, a proposal (Iteration 408): freeze bytehdr, doesfar, thinhdr, varcall, bss and lean; remove msc and scale; tail after seed 63.
- `drafts/price-410.md` - Two levers priced on seed 60's front (Iteration 410): handler replication for calls and returns at most 0.4-1.6% - not built; the register machine's bound, corrected at 411 (stackops.py's opcode names were wrong on the two-bit tag): 7-46% a workload; its lead I, whose fusion rtiplus never fired on the tag - fixed at 412 (I+ pinned to one byte): loop's dispatches -20%.
- `drafts/preflight-414.md` - The processing tools tried before the runs need them (Iteration 414): spread on seeds 58-60 (466 s; 59 and 60 13.6 points apart in genes, within 6% in speed), curse on seed 60 (1.066, seed 58 1.112), the batch's application dry-run.
- `drafts/escape-mechanism-435.md` - An escape mechanism for the fast end, options and costs (Iteration 435): islands, age-layered immigrants, restart on stagnation, replicates; recommended - islands, an evolver option off by default, tried in one run against seeds 63-64.
- `drafts/footprint-gate-435.md` - A footprint gate, priced (Iteration 435): 1,266 fast-end children a run (seed 62), 1-2.5 s a reading; a held-out check about 10 minutes a run, a gate 1-2%, a footprint workload some 30% of the generations; recommended - the held-out check first.
- `drafts/inert-scan-451.md` - Genes switched on but doing nothing (Iterations 451-452): four of seed 65's front designs, each expressed gene turned off, all seven workloads profiled, builds hashed - no gene inert across designs; alignfn, gotodup, fbuf the same build in one design or two; jitloop works (bubble's dispatches 57-65x without it) and tos works - the first pass's two findings were false.
- `drafts/jitapps-471.md` - What the JIT leaves on the applications, and why (Iteration 471; lab/evolve/jitapps.py): on seed 68's fast design the JIT leaves 37-94% of the applications' dispatches to the interpreter; roots - operations without stencils (the multiply and divide under *, CELLS, MOD, /; op 70) and EXECUTE's dispatch; one missing stencil sinks a word and its callers. Four proposals.
- `drafts/appbench-468.md` - Applications held out - the tool (lab/evolve/appbench.py) and a first reading (Iteration 468): on three of seed 68's front the order holds but the lead does not - the design at 0.140 on the selection's workloads runs fcp, brainless and cd16sim at 1.03 of s6's time (fcp 13% faster, brainless 16% slower); loading is negligible. Three proposals.
- `drafts/appbench-467.md` - Appbench on our Forth (Iteration 467; its tools in drafts/appbench/: fold.py, prelude.fth, run.py, which read the owner's zip in place): fcp, brainless and cd16sim run on s6 with their own checks PASS (6.8 s, 4.1 s, 6.5 s) - case folding, our own extend.4 and coreext.4, a few stubs; lexex and benchgc stop on case-sensitive lookups at run time; the terms of each program; three proposals.
- `drafts/appbench-466.md` - Real Forth applications as held-out workloads (Iteration 466): Appbench (benchgc, brainless, fcp, cd16sim, CoreMark, lexex) - deep stacks and frequent calls, unlike our kernels (RPyForth, 2026) - not reachable from this machine; Gforth's siev, bubble and matrix run on s6 with case folding and a three-line prelude (our kernel lacks NIP and .( ); three proposals.
- `drafts/ask-arm-jit-511.md` - A prompt for other models (Iteration 511): porting the copy-and-patch JIT to 32-bit ARM (Tegra 3, Cortex-A9) - A32 or Thumb-2, copyable stencils without literal pools, the tail jump and branch encodings, movw/movt patching, returning (sp, tos) in registers, cache maintenance, longjmp, prior art.
- `drafts/ask-arm-jit-answers-512.md` - The five answers to the ARM prompt, checked (Iteration 512) with GCC's ARM cross compiler, QEMU, Linux's cache-v7.S and the assembler: what holds (A32, `b` tails, encodings, uint64_t in r0:r1 - ours already, the cache flush incl. the branch predictor), what is wrong (-mword-relocations makes literal pools; -mslow-flash-data is M-profile only; the default stack protector adds literal pools); a copy-and-patch round trip under QEMU (drafts/arm-cp-poc-512.c, 40 2 + = 42); the port's recipe.
- `drafts/ask-noise-511.md` - A prompt for other models (Iteration 511): selecting under measurement noise - the fast end's 7-10% optimism; the slower-of-two reading weighed; re-evaluation, racing, OCBA, shrinkage, noise-aware dominance; a protocol for our costs; load against luck; verifying a fix.
- `drafts/ask-noise-answers-513.md` - The five answers to the noise prompt, checked (Iteration 513), and our own noise measured: one reading's is 0.96% (seed 70's 1,130 gated pairs), the gate's regression to the mean 0.07%, the reference already paired - so the fast end's 7-10% is not luck but context (co-runners shifting the design/s6 ratio); the slower-of-two patch withdrawn; an experiment proposed.
- `drafts/ask-jit-review-511.md` - A prompt for other models (Iteration 511): a bug hunt in the JIT - jit.c, spn-stencils.c and vm-lab.c's JIT entry and exit attached (as with the after-seed-71 batch); the invariants; each bug with a minimal trigger, to be turned into a test.
- `drafts/ask-jit-review-answers-515.md` - The four answers to the bug hunt, checked (Iteration 515): one real bug - a word made after MARKER at an old word's address ran the old word's native code (jit_k keyed by address; reproduced 5 for 7, fixed, tested at both widths); the rest wrong (EXECUTE-shaped words, PICK), correct by design (jitk after a fused pair) or unreachable (imm32 holes - hardened; the ABORT" guards).
- `drafts/jit-pairs-506.md` - The JIT's operation pairs over the seven selection workloads, pricing super-stencils (Iteration 506): 41% of dispatched pairs in straight-line code, the top 25 a quarter; I +, DUP I, + XOR lead; a few percent to win - a literal-into-operation gene proposed first.
- `drafts/seed71-checklist-505.md` - Seed 71's processing, written before its results (Iteration 505): what compares across the speed break (sizes, memory, within-run measures, appbench's ratios) and what does not (speed, best Q, hypervolume); the predictions it settles; the after-seed-71 batch; seed 72's line.
- `drafts/process-review-501.md` - What the recent runs say about the workflow, processes and rules (Iteration 501): the 32-bit JIT untested by engines-check (fixed - and a differential JIT test made permanent), conflict markers that apply (batch-check refuses them), rebasing a batch; proposed - a gene paid for by a workload before it is enabled, a grace period for gene votes, rule 3's band or a re-measure, the footprint experiment dropped.
- `drafts/nocase-496.md` - The case-insensitive gene planned (Iteration 496): the concern weighed; where it hooks in - fold NAMEBUF after NAME>BUF/NAME>BUF8 (every search, the C ones too), fold the stored name in HEADER; an X8 overlay composing with kfast, klookup, kinput; the test - lexex and benchgc unshimmed.
- `drafts/apps-selection-491.md` - The applications in the selection, priced (Iteration 491): one short pass of our four applications as a seventh workload - seed 68's fast design at 0.573 of s6 on it, with the four JIT genes 0.193; a draft patch (apps-selection-491.patch), not applied - the owner's decision.
- `drafts/scout-answers-480.md` - Five answers to the scouting prompt, checked and merged (Iteration 480): what exists as described (copapy - MIT, ARM32; Mason's dual threaded and native execution, and his 2026 copy-and-patch JIT for threaded interpreters; Gregg's code-copying JIT; the R copy-and-patch JIT), what does not hold (four claims), and the order: an inline cache for EXECUTE, native regions with exits back to the interpreter, coverage in what the selection sees; ARM port sources; later register allocation and factoring literature.
- `drafts/scout-prompt-479.md` - A prompt for other models to find projects and ideas we can reuse (Iteration 479): the project, the applications finding, seven areas wanted (JIT coverage, cheap transitions, register allocation, 32-bit native, density, workloads, method), what we have already reviewed, and an answer format with links, licences and confidence.
- `drafts/more-projects-478.md` - Another model's list of projects, verified (Iteration 478): nibbleforth, tokthr, zForth, paraforth, astil_forth, romforth, bee, milliForth, sectorforth - what each is, what we already have (CV8's variable-length literals and calls, frequency-assigned operations, hot calls; SPN and the JIT), and what is new: a factoring pass and single-use inlining (nibbleforth), native code saved with the image (astil_forth).
- `drafts/jitrp-465.md` - jitrp, the JIT's return-stack pointer in a register - a prototype (Iteration 465; the patch beside it): each return-stack stencil three instructions shorter; by cachegrind's exact counts seed 68's fastest GCC JIT design runs loop with 19.9% fewer instructions, bubble 4.5% fewer, ackermann 2.1% more; GCC only, its register clear of regpin's - five steps to a gene.
- `drafts/jit-i386-460.md` - The JIT at 32-bit x86, a feasibility study and a working prototype (Iteration 460; the patch beside it): i386's convention as ARM's (one 64-bit state, regparm(2) - eax and edx both ways), 4-byte holes, a variable's alignment bug found; s6 with the JIT at 32 bits passes the corpus, speed 0.956 to 0.767 (fib 2.3x, ackermann 1.6x); five steps to make it real.
- `drafts/c4-family-459.md` - c4 and its family (Iterations 459, 462; the second pass: Gforth's code-copying literature, copy-and-patch, CPython's JIT, Deegen - six ideas proposed: a stencil relocatability check, stencils from relocations for ARM, the return-stack pointer in a register, wider inlining, a no-vectorise gene, Forth application benchmarks as held-out workloads): c4, EarlGray's i386 JIT, AMaCC and Squint (ARMv7, a peephole optimiser), shecc, write-a-C-interpreter - sizes, licences, techniques; what applies: our JIT already has their lessons (jitk, immediates, fused branches); the gap they point at - no JIT at 32 bits (about 2.6x) - an i386 port proposed; a JIT-redundancy probe; an interpreter-in-Forth workload; c4's frames and structure for Fern.
- `drafts/fern-design-457.md` - **Obsolete (Iteration 510): Fern is its own project, which has these notes.** Fern, a small scripting language compiled into Forth words (Iteration 457): Ruby-style syntax, cells only, locals in a return-stack frame, no runtime of its own - expected within 0-20% of hand-written Forth; a four-step plan; the starting point for its own chat.
- `drafts/fastgate-review-445.md` - The fast gate, reviewed (Iteration 445): seed 64's 1,174 children measured twice agree with themselves (second / first 1.000) but the re-measure after the run finds the fastest about 10% slower - the two back-to-back readings share their moment's luck; proposed: the second measurement deferred to the next generation's batch.
- `drafts/price-dthread-440.md` - Translation to direct threading at load, priced (Iteration 440): about 3% faster at best by the dispatch lab (the loop slower), about +58 KB in memory - a third of the memory objective - and a new engine path; not worth building now.
- `drafts/supers-tag2.md` - The supers gene in tag-2 designs (Iteration 367): its pool misnamed since Iteration 66 (codes read as plain opcodes), the gene inert in ~97% of the fronts (its slots taken by format-10 words); the fix pending after seed 57.
- `supers-knockout-seed58.md` - Superinstruction pairs knocked out, seed 58's tag-2 designs (Iteration 385; HANDOFF item 1): 0.9% fewer dispatches at the median (to 2.5%), -1,024 to +719 bytes - they buy something, so the gene stays; 2 of 19 carry pairs that never execute.
- `review-methodology-386.md` - A review of the methodology, workflows and logic (Iteration 386): nocarry is not from scratch (two evolved founders, two thirds of seed 58's ancestry); the fast end's in-run speeds ~10% optimistic; the verdict's 2% bars inside the noise; front membership 46-65% between CPUs; whole-front Spearman hiding the top end; the surrogate screen cleared; proposals for the owner.
- `verdict-audit-388.md` - The verdicts audited (Iteration 388): all 16 sessions since the five-measure rule rebuilt and recomputed from each CPU alone - the CPUs agree in 14, the two that differ (seeds 50, 51) decided nothing; the verdict reads cpu 2 alone, cpu 8's half of each session unused by it.
- `convergence-seed58.md` - Is the search stuck in a local minimum? (Iteration 392, the owner's worry): five sources mapped to their tests, and seed 58 from inside - diversity holds and rises, the gains continue to generation 130: no collapse.
- `tools-audit-394.md` - The tools audited after the context-economy changes (Iterations 394-395): nothing downstream broken; batch-check.sh's exit status and kept clone fixed and tested; compare-fronts.py run end to end.
- `bfind32-fault-399.md` - Open item 0f found (Iteration 399): bf_walk's signature in the cell type, three characters compared at 4-byte cells - seed 59's 34 dead at 32 bits live with the fix (pending, after seed 62); engines-check's bfind variants had built no walk; bfind inert in every TOS design.
- `wip-regmachine/README.md` - The register machine, work in progress (from Iteration 418) - kept apart, nothing there runs: its first pricing on code as it runs (plain CV8 a fifth to a third of most workloads' dispatches taken in as operands; the tag little beyond I+), a first sketch, the next steps.
- `rehearsal-417.md` - The final batch rehearsed on plain CV8 (Iteration 417): the far-call tests and the programs past 4 MB on s6 at both widths, seed 58's front sampled, a short free run; patch 12 at 104 bytes, patch 13 the stage build's overlay check.
- `bigprog-416.md` - Programs past 4 MB (Iteration 416): plain CV8's call (2 MB), link (4 MB) and DOES> (2 MB) reaches extended - FAR,, a fourth link form, cell-counted DOES> calls - pending patch 12; every design runs both test programs; +104 bytes a plain-CV8 image (417's (FAR)).
- `rehearsal-405.md` - The after-seed-62 batch rehearsed (Iteration 405): 13 of seed 59's front designs with its genes, and a short tag2 run at both widths (330 designs) - every new mechanism alive; one new 32-bit failure, GCC's t2call tail call on the two-bit tag, fixed as patch 9.
- `jitret-404.md` - The gene jitret (Iteration 404, pending patch 8): the JIT's EXIT as pop and jmp, not ret - here ackermann -26%, fib unchanged, bubble and loop +6-9%, the six about 3% faster; the search weighs it from seed 63.
- `xcheck32-402.md` - Item 0g (Iteration 402): xcheck --report --laptop32 - the 32-bit hosts against the laptop's own 32-bit speeds (the Tegra 0.709 to 0.857; dream 0.651 to 0.650, the machine not the width); the Tegra's eight link failures all fsys on.
- `fail32-400.md` - Every 32-bit failure of seed 58 classified (Iteration 400): 819: 745 bugs - bfind (418) and the tail engine built for x86-64 and compiled for i386 (327) - and 74 clang tail engines without musttail; Iteration 401: seed 59 the same classes, and musttail on every clang tail engine (patch 6) - none a design that cannot exist at 32 bits; a proposal: no design dead for a machine class. The Tegra's three link failures.
- `drafts/relf-gene-classes.md` - This lab's genes by what relf would pay to adopt one (Iteration 363): C engine only, opcode set or image format, kernel words, x86-64 JIT.
- `drafts/two-width-selection.md` - Selecting at both widths, the skew in the evolution itself (Iteration 335, a draft): a design's interpreter measured at 4-byte cells as a second speed objective; the decisions for the owner.
- `drafts/convert-align-death.md` - A converter death seed 54 found (Iteration 333): "call target 1390 not 8-aligned", one design of 41,406 - not yet looked into; its genome.
- `xcheck-dream-seed53.md` - The first remote check (Iteration 320): seed 52's front on dream.lan (i7-6700), the laptop's binaries - Spearman 0.959, the laptop's six fastest its first six; the JIT designs' lead over s6 smaller there.
- `drafts/jithelp-wip.patch` - Helper calls in progress (Iterations 344-345), against the pending batch: st_callc, h_place, h_parse, COUNT's entry.
- `drafts/jitre-wip.patch` - Interpreter re-entry in progress (Iteration 346), against the pending batch and jithelp-wip.patch: builds; crashes on its first run - to bisect.
- `drafts/skew-32.md` - Why designs lose at 32 bits (Iteration 352): thirty of seed 55's front at both widths and gene knockouts - tag2 and fsys 3 the causes, compiler's gain 64-bit only; the data in drafts/skew-32-*.jsonl.
- `drafts/next-genes.md` - The search for the genes after seed 54 (Iteration 323): price.py on seed 53's fastest interpreted designs - calls and returns the largest share, their genes in place, pairs diminishing; next, jitleft.py - what the JIT leaves to the interpreter.
- `drafts/jit-loop-crash.md` - A JIT fault seed 52 found (Iteration 310): two designs die in the corpus's loop tests; the trigger narrowed to jit with folds, ops10, rtloop and tag2; the genomes.
- `drafts/iploop-plan.md` - The IP-update loop form: three explanations of the evolved designs' lower IPC, and the laptop measurement that decides between them before anything is built (Iteration 295).

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

- `drafts/callrel.md` - The gene callrel - a draft, not in the batch (Iteration 164).
- `drafts/chat-to-iter265/README.md` - The leftovers of the chats of Iterations 213-265, as found.
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
