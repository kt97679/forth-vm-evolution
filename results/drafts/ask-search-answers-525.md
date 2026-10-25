# The answers to the search prompt, checked against our own data (Iteration 525)

Five answers to results/drafts/ask-search-524.md (the owner, 525). Most of what they recommend is method; what can be
checked are the premises each leans on - checked here against seed 72's records, a measurement, and the references.

## What our data says about their premises

| premise | who leans on it | checked | verdict |
|---|---|---|---|
| the fixed-margin screen wrongly rejects front-worthy children | 2 (recover 800-2,000 evaluations, 1-3% HV), 1, 3 | seed 72: 4,655 screened, 502 audited (measured anyway), 499 alive - **none on the final front; 0 of 200 checked non-dominated by what was measured before their generation** | **wrong for us**: the screen is conservative - it loses nothing measurable. The room is the other way: **screen more** (answers 3 and 5 expected 25-40% skipped, not 19%) |
| the surrogate trains on survivors only (selection bias) | 1 | evolve.py: every alive measured design of the earlier generations | does not apply |
| a single workload can screen for the seven | 4, 5 | Spearman with the seven's mean over 21,557 alive designs: 0.70-0.91 (apps 0.908, kernel 0.888) - **within the fastest tenth 0.41-0.65** | **rejected**: no single workload ranks the fast end, where it matters |
| one round tracks three well enough to abort early | 1, 2, 3 | here (one CPU), 12 of seed 72's designs, three single rounds each: off the three's median by **1.0% on average, sd 1.9%, at most 7.4%** | **holds with a wide margin**: an abort must allow ~10%; answer 2's "a 5-8% margin is safe" is not, at the tail. A clearly dominated child saves about a third of its measurement |
| a size predictor before compiling would help | 5 | the screen already predicts log size (1.2% offline) | already there |
| scikit-learn is "pure Python, no heavy dependencies" | 5 (and 3) | it is compiled extensions; the owner set the screen to pure Python (Iteration 200) | **wrong**; plain-Python options only |

**Operator yield, from seed 72's own counts** (the AOS question every answer raised): children by operator - mutation
13,591, crossover 9,547, borrowing 2,962; the final front by how made - 151, 13, 21. Per child that reached the front:
**mutation 1.11%, borrowing 0.71%, crossover 0.14%** - crossover, a third of all children, yields eight times less than
mutation. Adaptive operator selection has a real difference to act on.

## References

Checked: Thierens 2005 is "An adaptive pursuit strategy for allocating operator probabilities" (GECCO 2005, 1539-1546)
- answer 5 gave it the title of De Jong's 1975 thesis; answer 5's FRRMAB credited to "Gong, Li, Kwong 2015" is, to my
knowledge, Li, Fialho, Kwong and Zhang (IEEE TEVC 2014) - not searched; answer 4 dates Thierens and Bosman's optimal
mixing 2013 (GECCO 2011). Rendle 2010 (factorization machines), Deb 2002 (NSGA-II), Mouret and Clune 2015 (MAP-Elites),
Daulton et al. 2021 (NEHVI), Li et al. 2018 (Hyperband), Hutter et al. 2011 (SMAC) are as cited. Answer 1's "Li and Li
2026 survey" not verified.

## The answers, ranked

1 the most careful: chronological holdouts, the false-screen rate as the measure that matters, sequential rounds, no
invented gains. 2 concrete and plain-Python (a bootstrap ensemble of the additive model), but built on the screen losing
designs, which our audits contradict, and its numbers invented. 3 reasonable, but scikit-learn. 5 wrong references,
scikit-learn as "pure Python", a size predictor we have. 4 thin, and its single-workload screen fails at the fast end.

## Proposed (the owner's to decide)

1. **Adaptive operator selection** - smallest and best evidenced: probability by recent front yield per child, a floor
   for each operator (crossover's 0.14% against mutation's 1.11%). Pure Python, a few dozen lines.
2. **A bolder screen that knows its uncertainty** - a bootstrap ensemble of the additive model (refits cost seconds
   every 10 generations), screening on the probability of being dominated rather than fixed 30%/5% margins, the one-in-ten
   audit kept as its check: more children skipped while audited rejects stay off the front.
3. **One round first** for children the first round already shows ~10% beyond the measured staircase; the rest measured
   in full. To be priced on the laptop: how many measured children are that far out.
4. Deferred: other model classes (factorization machines, trees), NSGA-III, MAP-Elites, linkage learning - none
   answers a problem our data shows yet.
