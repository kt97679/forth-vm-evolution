# The answers to the front-statistics prompt, checked (Iteration 538)

Five answers to results/drafts/ask-front-stats-537.md (the owner, 538). Most of what they say is settled method; what
could be checked is checked - the arithmetic, the code, the references - and where they agree they agree for reasons
our own records already show.

## Where all five agree - and it holds

1. **A hypervolume with a fixed normalisation and a fixed reference point**, the same for every run compared. Our
   spread tool derives its reference per comparison, so its hypervolumes (0.8370, 0.8395, 0.8419; 0.3790, 0.1880) are
   not comparable from one table to the next - true, by construction. Normalise each objective to bounds fixed in
   advance (speed perhaps on a log scale, since relative changes matter: answer 66), the reference a little beyond them.
2. **With two or three runs, no rank test can decide anything** - checked: the smallest two-sided p of Mann-Whitney is
   0.100 for 3 runs against 3, 0.200 for 2 against 3; the Wilcoxon signed-rank test needs 6 pairs to reach 0.031. Report
   the runs' values and their spread; do not test.
3. **Our stopping rule is weak as worded.** "No gain beyond the spread" leans on a range from two or three runs - an
   unstable yardstick - and on extremes alone, blind to the inside of the front. Their remedy: at least three runs on an
   unchanged method before it can fire, a fixed-reference hypervolume as the main statistic, and a practical effect size
   decided in advance (the 2% in speed a natural start), the extremes kept as secondary measures.
4. **"No re-enabled gene in a top tenth" is a screen, not a test**: a gene can matter inside the front without reaching
   a tenth, and the test ignores how often the gene was even tried. Better: the confirmation front's fixed-reference
   hypervolume against the pooled front of the last runs on the same method, with the same effect size; and per gene,
   its share of the front against its share of the children that could carry it, per run (children are not independent
   - answer 66 is right that a Fisher test over them overstates the evidence).
5. **The final set: the extremes, then greedy hypervolume contribution**, after merging designs within the tolerances;
   a knee as a candidate, not an oracle (four objectives have several or none). Finalists re-measured - 1% noise can
   reorder close designs.

## What was wrong

| claim | who | verdict |
|---|---|---|
| false-stop risk "~30-40%", false-continue "~15%" | 63 | **invented** - no basis given; answers 65 and 66 say rightly that no such figure follows from five summary rows |
| a hypergeometric test as written | 63 | its code names a variable it never defines (total_gene_count) - and the children are not independent draws |
| genes_are_worthless(): delta = 0.01 x (hv_with - hv_without) | 67 | **a bug** - it compares the difference with a hundredth of itself: any positive gain reads "worthless" |
| pymoo's KneePointDetector (pymoo.indicators.knee) | 67 | not found in pymoo's package - likely invented |
| While et al. 2012 "A Review of MOEAs" at the DOI of Fonseca's 2006 hypervolume paper | 67 | **mismatched** - the DOI is another paper's |
| Hupkens, Emmerich and Deutz 2014, a statistical stopping test | 67 | **not found** by search |
| "spread on two runs is biased downward, so the rule rarely fires" | 67 | plausible in direction, unquantified |

## References checked

Found as cited: Martí, García, Berlanga, Molina, "A stopping criterion for multi-objective optimization evolutionary
algorithms", Information Sciences 367-368 (2016), 700-718 - MGBM, the mutual domination rate with a Kalman filter (64);
Trautmann, Wagner, Naujoks, Preuss, Mehnen, "Statistical Methods for Convergence Detection of MOEAs", Evolutionary
Computation 17(4) (2009) (64's "Wagner et al."). Known and as cited: Audet et al. 2021 on performance indicators (EJOR);
Ishibuchi et al. 2018 on choosing the reference point (Evolutionary Computation; 64, 66); Branke et al. 2004 on knees
(PPSN); Fonseca et al. on attainment functions; Zitzler and Thiele 1999; Deb and Jain 2014; Blank and Deb's running
performance metric (65).

## The answers, ranked

66 the most careful: the experimental unit is the run, not the design; enrichment per run, with eligibility; log speed;
tolerance-dominance and hypervolume kept apart; honest that no risk figure follows from five rows. 65 clear and decisive,
right on the rank tests and the rule. 64 sound, with real references (MGBM, Trautmann et al.). 67 useful structure but a
code bug, an invented API and two bad references. 63 invented risk figures and broken code.

## Proposed (the owner's)

1. **Revise the stopping rule** in GOALS.md: at least three runs on an unchanged method; the main statistic a
   fixed-reference hypervolume of each run's true front (bounds and reference point fixed in advance, speed on a log
   scale); stop when two consecutive runs gain less than a practical effect size decided now - in hypervolume, and in
   each extreme (2% in speed; a byte and a KB threshold to set) - with no open correctness issue.
2. **Revise the confirmation test**: the confirmation front's hypervolume against the pooled front of the last runs on
   the method, the same effect size; each re-enabled gene's front share against its eligible children's share, per run,
   as the screen; the top-tenth test kept only as a first look.
3. **The final set**: the extremes (re-measured), then greedy hypervolume contribution after merging within tolerances.
4. **A tool**: the fixed-reference hypervolume, pure Python, four objectives, for every run's true front - with the
   bounds written down before the next run, so nothing is fitted after the fact.
