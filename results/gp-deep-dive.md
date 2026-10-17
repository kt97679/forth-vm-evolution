# The GP process and its genes: a deep dive (Iteration 195)

The owner: can we add more genes, or improve the evolutionary process - from
other projects, papers, blog posts, repositories? Two halves: what our own
data says (seed 40's database, 34,983 designs; its re-measured front), and
what the literature offers - each idea weighed against that data.

## 1. What our data says

**Variation operators** (results/drafts/gp-credit.py) - children by how they
were made, and how many reached the run's final front (378 designs):

| variation | children | alive | not dominated by a parent | on the final front | per child |
|---|---|---|---|---|---|
| mutation only | 9,022 | 93.9% | 51.8% | 274 | 3.0% |
| crossover + mutation | 18,032 | 95.2% | 53.9% | 45 | 0.25% |
| borrow + mutation | 1,773 | 94.9% | 52.5% | 38 | 2.1% |
| crossover + borrow + mutation | 3,146 | 95.1% | 49.0% | 5 | 0.16% |
| crossover alone | 1,894 | 99.9% | 59.6% | 9 | 0.48% |

Mutation alone - a front design, one step away - made 73% of the final front
from a quarter of the children; crossover, 60% of all variation by our rates,
is twelve times less productive per child. The search's engine is local
search; crossover mostly spends evaluations.

**Genes**: of 61 genes mutated 150+ times, varcall (0.5% of its mutants not
dominated by their parent) and doesfar (0.2%) never help - ~1,200 evaluations,
3.5% of the run. fbuf is the most productive (75.5%, 37 designs on the final
front) - a buffer size made a gene: a "deep parameter" (2.4). Ten genes never
vary across the final front: bss, bytehdr, doesfar, enc, lean, nocet, scale,
tag2, thinhdr, varcall - converged or dead; their mutations are mostly spent.

**Linkage** (results/drafts/gp-linkage.py) - mutual information between gene
values over the final front, normalised: jit-jitx 0.98, jitx-jitloop 1.00,
jit-jitloop 0.98, jitinl with each 0.67; tos-tail-msc 1.00 each; escape-
rtloopall 0.92; rtfuse-rtimm 0.76. Of these only tos-tail, tail-msc and rtfuse-
rtimm are in the hand-made BLOCKS - the JIT family, tos-msc and escape-
rtloopall are split by crossover today.

**Workloads**: correlations of log speed over the 33,322 living designs -
corpus-parse 0.99, corpus-kernel 0.91, parse-kernel 0.90 (one behaviour, three
votes in the geometric mean); bubble-sieve 0.83, loop-sieve 0.77, bubble-loop
0.74 (the loops); fib-ackermann 0.70 (calls).

**Noise**: seed 40's front designs measured again in another session, same
code: median 1.001, 5-95% 0.986-1.026; 4% moved more than 3%, none more than 5%.

**Cost**: 2.7 s per design (median, build and gate included), 25.3 CPU-hours a
run; died designs cost nothing measurable.

## 2. The process - ranked by evidence over cost

1. **Less crossover, or crossover chosen by its record.** Our data above;
   in genetic improvement of software local search is now common and
   competitive (MAGPIE: one local search, compiler flags, configuration and
   code edits). OpenTuner runs an ensemble of techniques and gives each tests
   by an AUC multi-armed bandit - techniques that do well get more. Change:
   crossover 0.6 -> 0.25 as a first step; then a bandit over the operators
   (crossover, borrow, mutation-only), credit = the child not dominated by its
   parents. Cost: small. Test: seed 42 against seed 41 by the five-measure
   judging.
2. **Linkage learned, not only written** (GOMEA, LTGA: mutual information
   between variables over the population, clustered hierarchically into a
   linkage tree whose clusters are the crossover masks). Change: the three
   groups above into BLOCKS now; later the tree recomputed each generation from
   the population. It may be why crossover does so badly - it splits the JIT
   genes. Cost: small, then medium.
3. **Each gene mutated by its record.** The same bandit, over genes: varcall
   and doesfar retired (or 1/10 the rate), converged genes slowed, productive
   ones (fbuf, kinput, kfast, escape, jit) more often. Cost: small.
4. **Speed within 2% a tie** - as memory within 8 KB is (MEM_TOL): noise is
   +-2.6% at 5-95%, so a smaller speed difference is a coin's decision, and it
   decides dominance today. Cost: small.
5. **A surrogate to screen children** (surrogate-assisted EAs; pre-selection
   by a model before survival; random forests for combinatorial, multi-
   objective problems). We have 35,000 labelled designs a run: a random forest
   on expressed genes predicts size nearly exactly and speed roughly; children
   predicted far from the front skip measurement, a random share measured
   anyway to keep the model honest. Saves whole 2.7 s evaluations - more
   generations a run. Cost: medium.
6. **Age** (Age-Fitness Pareto: a genotype's age as an objective, young
   genetic material protected; ALPS: age layers and fresh random designs
   injected at the bottom - a threefold gain in its paper). Complements the
   attic, which keeps lost genes but not young lineages. Cost: medium.
7. **Racing** (irace: statistical tests discard poor candidates early).
   One round on a workload from each cluster first; a design 10% behind its
   neighbours by size stops there. Saves part of 2.7 s. Cost: medium.
8. **The workloads by cluster** - the owner's to decide, it changes the
   objective: the geometric mean gives corpus/parse/kernel three votes. Equal
   weight per cluster, or epsilon-lexicase over the clusters for parents only
   (lexicase keeps specialists; its own studies warn that redundant, highly
   correlated cases skew it).
9. **Islands with resets** (FunSearch: the weaker half of the islands reset
   from the best of the others; AlphaEvolve/OpenEvolve: islands with migration
   and a MAP-Elites grid). Our seeds with carried fronts already are coarse
   islands; within a run, two or four islands would cost little. Lower: the
   attic and the family rule already keep diversity.
10. **Instruction counts as fitness** (MAGPIE counts instructions with perf,
   not time): noise-free, but blind to what branch prediction and alignment
   genes do - a tie-breaker at most.

## 3. New genes

1. **Deep parameters, found by sweep** (Wu, Weimer, Harman, Jia, Krinke:
   first-order mutants find the sensitive constants, which become parameters
   tuned with the rest - time and memory, bi-objective). fbuf is our proof.
   Method: each numeric constant in the engine, kernel and converter halved
   and doubled on three designs (smallest, knee, fastest); those that move an
   objective by more than noise become genes. Cost: medium, mechanical.
2. **Instruction replication** (Ertl, Gregg, Casey: copies of a VM
   instruction's code improve indirect-branch prediction; with superinstructions
   up to 4.55x over threaded code). Modern predictors weaken it (Rohou, Swamy,
   Seznec: Haswell and ITTAGE predict interpreter dispatch well) - Ertl
   measured on Haswell anyway 1.06-1.81x from replication. Zen 4's predictor
   decides: a gene - the K hottest handlers replicated (K 0/4/8/16), copies
   given out by the converter round-robin over sites; cost one-byte codes and
   engine bytes, evolution weighs them. Cost: medium.
3. **Profile-guided engine** (CPython builds instrumented, runs a training
   workload, builds again; BOLT on top of PGO+LTO up to 15% more on Clang).
   Trained on a workload outside the selection (the build's own boot, or the
   held-out set's sibling) so it does not fit the benchmarks. Doubles a
   design's build. Cost: medium.
4. **Two registers of stack** (Ertl's stack caching: dynamic - an interpreter
   per cache state; static - the compiler tracks the state, instructions in
   versions for several). Our tos is one register; the register stage is worth
   20-26% of the image's dispatches at the small end (results/price-hybrid.md).
   Cost: large - the hybrid's next step.
5. **The next keeping forms** - DUP before ?BRANCH, OVER before C@ (the
   largest absorbable patterns, results/price-hybrid.md). Cost: small each.
6. **Tail-call dispatch** (CPython 3.14: handlers as functions, guaranteed
   tail calls; 9-15% geometric mean, PGO recommended; its first numbers were
   inflated by a compiler bug in the baseline). Needs Clang 19+ on the laptop.
   Cost: large; first check the compiler.

## 4. Not recommended now

LLM-written mutations (AlphaEvolve, FunSearch) - our genes are designed by hand
with the owner, which is that loop at human speed; automating it is a project
of its own. NSGA-III or many-objective selection - three objectives do not
need it. MAP-Elites as the main archive - the families, the attic and the
knee's protection cover what it would add, at much less change.

## 5. A plan

Seed 42 tests the cheap four together against seed 41 (the five-measure
judging): crossover 0.25, the learned BLOCKS, varcall/doesfar slowed, speed
ties within 2%. Then the surrogate (offline first: trained on seeds 39-40,
scored on 41 - how many of 41's front would it have skipped?), and the
deep-parameter sweep. Replication and PGO as genes after that.

## References

- Wu, Weimer, Harman, Jia, Krinke, Deep Parameter Optimisation, GECCO 2015 - human-competitive.org/sites/default/files/wu-weimer-harman-jia-krinke-text.txt
- Blot, Petke, MAGPIE, 2022 - arxiv.org/abs/2208.02811; github.com/bloa/magpie
- Helmuth et al., lexicase and specialists - cs.hamilton.edu/~thelmuth/Pubs/2020-GPEM-lexicase-specialists.pdf; La Cava et al., epsilon-lexicase - arxiv.org/abs/1905.13266; Hernandez et al., redundancy - arxiv.org/abs/2407.15056
- Schmidt, Lipson, Age-Fitness Pareto Optimization, GPTP 2010; Hornby, ALPS, GECCO 2006 - ntrs.nasa.gov/citations/20060015684
- Ansel et al., OpenTuner, PACT 2014 - commit.csail.mit.edu/papers/2014/ansel-pact14-opentuner.pdf
- Bosman, Thierens et al., GOMEA / LTGA - arxiv.org/abs/2109.05259; ics-websites.science.uu.nl/docs/vakken/ea/slides/LTGA_GOMEA.pdf
- OpenEvolve (AlphaEvolve's open implementation: MAP-Elites, islands, cascade evaluation) - github.com/algorithmicsuperintelligence/openevolve
- FunSearch's island resets - llm4ad-doc.readthedocs.io/en/latest/method/funsearch.html; arxiv.org/pdf/2412.20694
- Casey, Ertl, Gregg, Optimizing Indirect Branch Prediction Accuracy in VM Interpreters, TOPLAS 2007 - mural.maynoothuniversity.ie/10188
- Rohou, Swamy, Seznec, Branch Prediction and the Performance of Interpreters, CGO 2015; Ertl's reply with Haswell measurements - compilers.iecc.com/comparch/article/22-10-056
- Ertl, Stack Caching for Interpreters, PLDI 1995
- irace - arxiv.org/pdf/2107.05847 (section 4.2.5)
- CPython PGO and the tail-calling interpreter - lwn.net/Articles/1033373; BOLT - github.com/signalapp/BOLT/blob/master/docs/OptimizingClang.md
- Liou, Forrest, Wu, GEVO (NSGA-II over LLVM-IR edits; epistasis) - arxiv.org/abs/2004.08140, arxiv.org/abs/2208.12350
- Jin, Surrogate-assisted evolutionary computation, 2011; Liu et al., SAEAs for expensive combinatorial optimization, 2024

## Adopted (Iteration 197) - results/applied-after-seed41/gp-process-after-seed41.patch

The four cheap changes, for seed 42 to test against seed 41: crossover 0.25
(EVOLVE_XOVER); LINKS - the JIT's four genes, tos/tail/msc, escape/rtloopall,
rtfuse/rtimm - inherited whole from one parent (crossover had been uniform,
gene by gene; BLOCKS serve borrow only); varcall and doesfar drawn one time in
ten; speed within 2% a tie in the generation's ranking (EVOLVE_SPEED_TOL),
with a guard: a design the relation leaves in no front (tolerances need not be
transitive) goes in a last one, not lost. A scratch run: 28% of 36 children by
crossover, all alive, no varcall or doesfar mutation; run-tests PASS.
