# The answers to the noise prompt, checked - and our own noise measured (Iteration 513)

Five answers to results/drafts/ask-noise-511.md (the owner, 513). Checked against seed 70's own records, the
measurement code, two literature searches and the order statistics - and against two errors in the prompt itself.

## Two premises of the prompt were wrong - mine

- **The noise is about 1%, not 2-3%.** Seed 70's 1,130 gated designs were each read twice, in different batches among
  other co-runners: ln(second/first) has a standard deviation of 1.36%, so one reading's is **0.96%**.
- **The reference is already paired.** The prompt said s6 is measured once per run; in fact `measure()` runs the design
  and s6 back to back in every round, alternating which goes first, and divides (since the evolver's first iterations).
  The answers' main fix for load - a time-local, interleaved reference (all five) - has been in place all along.

## What the data says about the 7-10%

- **Winner's curse at the reading level: none to speak of.** The gate picks designs on a fast first reading; their
  second reading comes out slower by **0.07%** on average (median 0.03%; slower in 51.5% of them) - regression to the
  mean that small means a single reading's luck cannot make 7-10%.
- **What differs is the context.** In the run: 3 rounds, three other workers measuring at the same time. The re-measure
  (`--remeasure`): 6 rounds, alone. The pair with s6 cancels load that slows both alike; it cannot cancel load that slows
  them differently - **a design-specific response to contention** (answer 9 names exactly this limit). The fastest
  designs (JIT, compact code) and s6 (an interpreter) plausibly use the shared cache, memory bandwidth and the clock
  differently, so under co-runners the ratio shifts. This container has one CPU and cannot show it (co-runners only
  time-share it: the ratio moved -3.5% to +1.5% for four of seed 70's front, no pattern).
- **So more readings, racing, OCBA or shrinkage would not touch it** - they reduce a noise that is small here.

## What holds in the answers

- **The order statistic**: for two independent normal readings, E[max] = mu + sigma/sqrt(pi) - answers 9 and 10 (answer 7's
  "0.2-0.4%" is arithmetic wrong). At our sigma, **the slower of two is 0.54% pessimistic** - pointless against a
  context offset, and a small discontinuity at the gate (all five).
- **The geometric mean on a log scale** is the right estimator for repeated readings (answer 9's derivation) - what the
  gate already does.
- **Elite accumulative resampling** (Fieldsend, EMO 2015, LNCS 9019, 172-186 - found): the paper itself finds that at low
  noise a low fixed resample rate is usually sufficient - our gate's two readings already are one.
- References that check out: Fieldsend 2015; Hughes 2001 (EMO, LNCS 1993, 329-343); Teich 2001 (EMO, "Pareto-front
  exploration with uncertain objectives"); irace (Operations Research Perspectives, 2016); Jamieson and Talwalkar
  (AISTATS 2016). Garbled or invented: answer 10's "Hughes, IEEE TEC 2005" and "Teich, IEEE TEC 2001" (both EMO 2001,
  other titles), "D. M. T. et al., SIGMETRICS workshops"; answer 6's "Non-stochastic Negative Successive Halving".

## The answers, ranked

9 the best: careful statistics on the log scale, the limit of pairing named, real references, honest uncertainty. 7 well
organised (elite resampling first) but its bias arithmetic wrong. 8 sensible and the most sceptical of OCBA for our costs.
10 right on the order statistic but with invented figures ("in my experience", "39 h") and several invented references.
6 thin, an overstated "severe" discontinuity, a garbled reference. All five were led by the prompt's two wrong premises.

## Done, and proposed

- **Withdrawn**: the slower-of-two patch (fastgate-slower-after-seed71, now results/drafts/fastgate-slower-withdrawn-513.patch)
  - 0.54% of pessimism against a 7-10% that is not noise; the gate keeps the geometric mean. Its prediction (503)
  withdrawn. The other four pending patches apply without it.
- **Proposed - an experiment that names the cause**: re-measure the front's fastest tenth (a) alone, as now, and (b)
  with three workers running ordinary measurements beside it - on the laptop. If (b) matches the in-run speeds and (a)
  is the 7-10% slower, the offset is contention; then the question is which speed the search should optimise - with
  co-runners (as now: cheap, four at a time) or alone (the speed a user sees) - and rule 3 compares like with like.

**The owner (514)**: the experiment added - lab/evolve/contention.py, the last step of seed 72's chain (NEXT-RUN's note,
the seed 71 checklist): the 16 fastest of the front, each measured as the run measures it, alone and beside three
co-runners on other cores (looping s6 and front designs over the selection workloads), alone-loaded-loaded-alone.
