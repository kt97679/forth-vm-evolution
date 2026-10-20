# A footprint gate - priced (Iteration 435)

The owner asked for this after seed 62's processing (HANDOFF item 2): footprint.py showed the fast designs about 4x
s6's speed on programs of 100-1,000 words but 1.1-1.5x at 10,000, the selection's order holding only partly
(Spearman 0.783 at 10,000). Should larger programs count in selection? Priced here; nothing built.

## The gate's volume - seed 62's database

A gate measures only designs at the fast end, as the fast gate does: a child whose speed is within 5% of the 20th
fastest so far when it is made. In seed 62's run: **1,266 such children, 4.1% of the 31,071 measured** - 8.1 a
generation on average, most of them early (913, 220 and 133 in the run's three thirds); 658 of them faster than the
20th fastest.

## The cost of one measurement

footprint.py here (results/drafts/footprint-gate-435.out): two designs and s6 at 3,000 and 10,000 words, one round,
the full program and its definitions alone - 139 s with the builds. For a fast design at 10,000 words: compiling
the program takes a fifth of a second to half a second, running it about as much again. A gate reading of 3 rounds,
s6's reference measured once a run, is **about 1-2.5 s a design**.

## The options, priced

| option | what | cost a 10-hour run | effect on selection |
|---|---|---|---|
| 1. A held-out check after each run | footprint.py on the front's fastest tenth, 10,000 words, 3 rounds | about 10 minutes (the current step, 12 designs at four sizes and 5 rounds: 34) | none - a reading each run |
| 2. A footprint gate | the 1,266 fast-end children measured at 10,000 words as they arrive | 20-50 minutes of measuring, about 5-13 minutes of the run's time over 4 workers - 1-2% | needs a rule for how its reading counts; see below |
| 3. A footprint workload in the selection | every design measured on a generated program of a few thousand words | about +1.5 s a design on today's ~3.8 s: some 30% fewer generations | the cleanest - every design judged alike |

**How a gate's reading could count** - the hard part. Its numbers do not mix with the selection's speed (a fast
design: 0.127 on the selection, 0.80 at 10,000 words). Options: rank gated designs by the geometric mean of the two
- they would fall behind ungated designs measured only on small programs, a bias; or a penalty only beyond a bound -
say, a design whose lead over s6 shrinks more than 3-fold from 100 to 10,000 words loses the fast gate's pass - a new
threshold to tune. Both are workable, neither as clean as option 3.

## Recommendation

**Option 1 now, for the data; options 2 or 3 only if it shows the large-program order differing at the very top.**
A check costing about 10 minutes each run (an experiment step after the comparison, or a step of its own) tells,
run by run, whether the fastest designs on small programs are also the fastest at 10,000 words. Seed 62's reading
(Spearman 0.783 over 12 designs from all over the front) does not yet say that for the fastest tenth. If the top
reorders, option 3 is the honest fix - at about 30% of a run's generations - and option 2 a cheaper approximation
with a rule the owner sets.
