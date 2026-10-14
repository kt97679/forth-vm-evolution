# Results - every measurement and analysis, indexed

One line each, by topic: the file, then its own title. Each per-run record names the
machine and run it came from. `tools/handoff-check.py` fails when a document here is
missing from this index (README.md, "Documents", indexes everything else).

## The evolution, run by run

- `evolve-amd-ryzen-7-pro-8840hs-seedN.md` - each run, seeds 1-47: the verdict and the facts, then the pack's report with every front design's genome (the gate, ans-check and the other tools read genomes from these).
- `evolve-amd-ryzen-7-pro-8840hs-seed4b.md` - Evolution on the Ryzen 7 PRO 8840HS - seed 4 again: a replicate.
- `compare-fronts-amd-ryzen-7-pro-8840hs.md` - every comparison session: the fronts of all runs measured again together, judged by the five measures.
- `predictions.md` - the predictions written before each run, then scored.
- `progress-by-run.md` - every run's extremes, for the progress charts (lab/evolve/progress-table.py).
- `applied-after-seedN/ORDER.md` - each batch of patches applied after a run: the order, and how each patch was tested.
- `drafts/iploop-plan.md` - The IP-update loop form: three explanations of the evolved designs' lower IPC, and the laptop measurement that decides between them before anything is built (Iteration 295).
- `pending/ORDER.md` - the batch waiting to be applied after the run now on the laptop, while there is one: the order, and how each patch was tested (results/pending/ moves to applied-after-seedN/ when applied).

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
