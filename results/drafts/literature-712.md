# More from the literature, checked against what is here (Iteration 712)

The owner (712): "please do a deep dive and see if you can find more articles/blog posts/implementations that can
help with this project". The project has read a lot already, so the first step was the list of what not to
re-propose: the gap check and broad sweep (results/missed-options-2026-10.md, Iterations 258-260), the GP deep dive
(results/gp-deep-dive.md, 197), the JIT and VM survey (results/drafts/jit-vm-survey.md), the scouts (480), the noise,
search and related-work answers (513, 525, 539), originality (605), ideation (707) and Frostbite (711). Already there,
so not repeated below: superinstructions static and dynamic, stack caching, the IP-update work (Ertl and Paysan, ECOOP
2024), Rohou, Swamy and Seznec on branch prediction, copy-and-patch and Deegen, CPython's tail-calling interpreter and
JIT, Ertl and Paysan's code-copying experience report (EuroForth 2025), racing, irace and resampling, adaptive operator
selection, COLE and QuickInterp, MAGPIE and genetic improvement, the echo instruction, Huffman-coded bytecode,
milliForth and sectorforth, Mytkowicz et al. on layout bias.

What is new falls in five places. One of them corrects a premise in the register.

## 1. The stack header: the register's premise is wrong on x86-64 (measured)

GOALS.md's row (Iteration 251, the owner: "captured, left"): without PT_GNU_STACK "the kernel makes the stack - and
with READ_IMPLIES_EXEC every mapping - executable: 56 bytes ... for a weaker process". That was true once. Linux 5.8
(Kees Cook's "x86/elf: Disable automatic READ_IMPLIES_EXEC on 64-bit", April 2020) made a missing header
**exec-none** on x86-64: only mappings asked to be executable are. It stays **exec-all** for ia32 and for 32-bit ARM.
Checked here (results/drafts/literature-712.txt):

| binary | without PT_GNU_STACK |
|---|---|
| x86-64, Linux 6.18 | stack rw-, personality 0 - nothing changes |
| i386 (gcc -m32) | stack rwx, personality 0x400000 (READ_IMPLIES_EXEC) - weaker, as the row says |
| designs/smallest's engine relinked with a one-segment script | 4,912 -> **4,864 bytes** tight (-48: -1.0 % of the engine, -0.35 % of binary + image); stack rw-; runs the same |

Two notes. First, the engines' one segment is RWE already (-Wl,-N), so W^X was never kept. What the header guarded
on x86-64 was only the stack, and the kernel now guards it anyway. Second, the cut is about the same 48 bytes on
every x86-64 engine. No ranking moves; only the reported sizes shrink. The 4-byte (i386) and ARMv7 engines keep
the header. The laptop runs 6.17, and dream's and rage's kernels can be checked in one line (/proc/self/personality
under a header-less binary). **The owner's call, reopened with the corrected premise.**

## 2. For the counters model (countfit, Iteration 711)

**countfit's form is the interval model.** Karkhanis and Smith (ISCA 2004) and Eyerman, Eeckhout, Karkhanis and
Smith (TOCS 2009) split execution time into intervals separated by miss events: mispredictions and cache misses, each
with its own cost. Their model came within 7 % on average of detailed simulation of a 4-wide out-of-order core.
Eyerman, Hoste and Eeckhout (ISPASS 2011) fit such a model to real hardware's counters, to build CPI stacks. Two
things follow for countfit, which fits ns = a·instructions + b·mispredictions + l·misses + c per workload:

- **The penalties belong to the machine, not the workload.** A fit with b and l shared across all workloads and
  designs on one machine has far fewer free numbers than seven independent fits. Its b, times the clock, is cycles per
  misprediction, which can be checked against what the core is known to pay. A fitted penalty that is negative or
  implausible means the model is fitting noise. Proposed: `countfit.py --shared` beside the per-workload fit, on chain
  B's data.
- **The base term is where interpreters differ.** In the interval model the time between misses is set by the
  dependency chains, and for an interpreter that is the IP-update chain Ertl and Paysan measured. So the instructions
  coefficient should differ by regime. 711's held-out table already split the JIT designs from the rest (Spearman 0.70
  against 0.59), and the shared fit should keep that split: a per JIT/not-JIT, b and l shared.

**Zen 4 can report the split directly.** Zen 4 brought pipeline-utilisation events, and perf has carried AMD's
metrics for them since the Zen 4 patch (December 2022). Level 1 is retiring, bad speculation, frontend bound and
backend bound, plus a fifth class for SMT contention. counters.py (Iteration 278) asks exactly
whether an interpreted design is held back by mispredicted dispatch or by the IP chain. It approximates the answer
from stalled-cycle events (295). On the laptop (Ryzen 7 PRO 8840HS, Zen 4), `perf stat -M PipelineL1,PipelineL2`
answers it in slots: bad speculation is the misses; backend bound with few misses is the chain waiting. Proposed:
`counters.py --topdown`, a few lines and the laptop's to run. One caution: AMD counts bad speculation from an earlier
stage than Intel does, so the shares compare within the laptop, not across vendors.

**Instruction counts as the metric: others' experience.** rust-lang's compiler benchmarks default to user-space
instructions retired. Their reason is noise. One measurement of rustc's self-profiler found the instruction counts' worst case about
five orders of magnitude below wall time's 5 %. OCaml's Sandmark reports instructions retired beside time for the same reason, noting that equal
counts can retire at different rates. Laurence Tratt's counter-argument: instructions mislead once the work moves
into memory, branches or parallelism. He keeps them for small code or small changes and wall time for everything
else. That matches countfit's self-test (instructions alone 19 % error, with the miss events 1.5 %). It also gives the
use: an instructions-first screen within a regime (an interpreted design's encoding change), not across regimes (a
JIT design against an interpreter, where branches and memory differ).

## 3. For the measurement: repeat where the variance is (Kalibera and Jones)

Kalibera and Jones, "Rigorous Benchmarking in Reasonable Time" (ISMM 2013), repeat at several levels: iterations,
executions, builds. A dimensioning run finds which level carries the variance, and the repetitions go there, with
results as effect sizes with confidence intervals. The project has already found both of the higher levels.
Iteration 513: one reading's noise is about 1 % and the context the larger term. The article: "a rebuild moved a result
five or ten percent and repeating a run could not see it" (tools/layout-noise.sh, on the stages). What has not been
measured is the build level of the designs the search names. Each role is one build, and rounds cannot see its
layout luck. Proposed, before the roles are named: layout-noise.sh's method on the roles' engines on the laptop (the
same source, flags that move code and nothing else). Where two roles are closer than their spread, the write-up gives
a band, not a winner. The tooling exists; it is the laptop's time.

## 4. For the held-out question (Iteration 711)

Automated program repair has the same problem under another name. Smith, Barr, Le Goues and Brun ("Is the Cure Worse
Than the Disease?", FSE 2015) built patches on one test suite and judged them on a held-out one. By the held-out suite
the repairs made the programs worse, which is why that suite, not the one searched on, is the evaluation. Ahmed et al. (2025) repeated the question for LLM
repair on SWE-bench and still found test overfitting, though less drastic on average. This supports 711's two
proposals - the held-out pair in the roles' write-up as the headline figure, and more held out by group in the reopened
search - without adding a new one.

## 5. For the comparisons: Gforth 1.0

Gforth 1.0 is out: EuroForth 2026's programme describes Ertl's talk on it as the first feature release in 18 years,
and Zeli's report
(October 2026) says its performance is on par with SwiftForth's. The project's comparisons use gforth-fast 0.7.3, from
apt (results/generic-apps-674.md; HANDOFF's application-code paragraph). That is a 2014 release, before the
IP-update optimisations: with them, Ertl and Paysan put Gforth level with the SwiftForth JIT and gcc -O0. A row against
0.7.3 understates today's Gforth, and the article's readers will compare against the current one. Proposed:
genapps.py's Gforth row re-run with Gforth 1.0's gforth-fast, built from source on the laptop (apt still has 0.7.3),
and the version named in every table.

## Checked, little or nothing for us

| find | what it says | for us |
|---|---|---|
| Wasmtime's Pulley interpreter (2025) | the match loop 1.13-1.19x faster than tail calls on two benchmarks, tail calls 1.03-1.04x faster on a third; loading 64 bits of operands with the opcode a universal loss | consistent with `tail` as a gene (no dispatch wins everywhere); nothing to build |
| Identical code folding (GCC -fipa-icf, on by default at -O2) | merges identical functions | our handlers are labels in one computed-goto function, not functions; nothing to fold |
| Header overlays (tmpout.sh; "teensy" ELF) | the program header started at 0x38, inside the ELF header: 112 bytes for both instead of 120; the smaller files (105, 84 bytes) also hide code in header fields; since 2020 the PT_LOAD must ask for execution itself | 8 bytes past section 1's 48, fragile (tools reject such files); not worth it |
| Zen 4's branch targets (Chips and Cheese) | L1 BTB about 1-3 K targets, L2 8 K; a single indirect branch's cost grows past 32 targets without a mispredict spike | our dispatch sites (hundreds, gotodup's copies included) fit; nothing to change |
| EuroForth 2026's programme | Gforth 1.0, control structures, floating-point output, reversible stack machines, type checking, AI and Forth | only Gforth 1.0 bears on us (section 5) |
| Java superoperators (eScholarship) | stack accesses and stack-pointer updates limit an interpreter more than dispatch | what stack caching and the JIT's K genes act on already |

## Proposed (the owner's)

1. **The stack header on the x86-64 engines** (section 1): reopen 251 with the corrected premise. The one-segment link
   script cuts 48 bytes from every 8-byte engine with no weaker process on kernels since 5.8. The i386 and ARMv7 engines
   keep the header. It is a constant, so nothing on the front moves.
2. **countfit --shared** (section 2): the machine's penalties shared, the base per workload and regime, on chain B's
   data beside the per-workload fit. countfit is in the after-seed-96 batch, so this would be a change to the counters
   patch.
3. **counters.py --topdown** on the laptop (section 2): Zen 4's PipelineL1/L2 for the fast end's interpreted designs.
4. **The roles' layout spread** before the roles are named (section 3).
5. **Gforth 1.0** in the comparisons and the article (section 5).

None is built here. Section 1 is measured; 2-5 need the laptop or chain B's data.

## Sources

- Linux: "x86/elf: Disable automatic READ_IMPLIES_EXEC on 64-bit" (9fccc5c0c99f) - lkml.iu.edu/hypermail/linux/kernel/2004.2/06194.html; arm32's table - elixir.bootlin.com/linux/v5.8.1/source/arch/arm/kernel/elf.c; tmpout.sh/2/11.html
- Eyerman, Eeckhout, Karkhanis, Smith, "A mechanistic performance model for superscalar out-of-order processors", TOCS 27, 2009; Karkhanis and Smith, ISCA 2004 - sites.coecis.cornell.edu/isca50retrospective/files/2023/06/KARKHANIS_2004_FIRST.pdf; Eyerman, Hoste, Eeckhout, ISPASS 2011 - researchr.org/publication/EyermanHE11
- perf's Zen 4 metrics - lkml.iu.edu/hypermail/linux/kernel/2212.1/04303.html; chipsandcheese.com/p/hot-chips-2023-characterizing-gaming-workloads-on-zen-4; chipsandcheese.com/p/cpu-zs-inadequate-benchmark
- internals.rust-lang.org/t/what-is-perf-rust-lang-org-measuring-and-why-is-instructions-u-the-default/9815; github.com/asayers/cbdr (instruction_count.md); discuss.ocaml.org/t/sandmark-nightly-service-now-reports-instructions-retired-along-with-time/10475; tratt.net/laurie/blog/2022/what_metric_to_use_when_benchmarking.html
- Kalibera and Jones, ISMM 2013 - kar.kent.ac.uk/id/document/3127886
- Smith, Barr, Le Goues, Brun, FSE 2015 - www.cs.washington.edu/homes/brun/pubs/pubs/Smith15fse.pdf; Ahmed et al. 2025 - arxiv.org/abs/2511.16858
- euro.theforth.net (EuroForth 2026); zeli.app/story/50256952 (Gforth 1.0); Ertl and Paysan, ECOOP 2024 - drops.dagstuhl.de LIPIcs.ECOOP.2024.14
- Pulley - bytecodealliance.github.io/zulip-archive (issue 9995); docs.rs/crate/pulley-interpreter
- Safe ICF (Google, 2010) - research.google/pubs/pub36912; GCC's IPA ICF pass - gcc.gnu.org/legacy-ml/gcc-patches/2014-07/msg00363.html
- Zen 4's frontend - chipsandcheese.com/p/amds-zen-4-part-1-frontend-and-execution-engine
