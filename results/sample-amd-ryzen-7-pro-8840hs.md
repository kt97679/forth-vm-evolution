# A uniform sample of the design space - Ryzen 7 PRO 8840HS

machine: AMD Ryzen 7 PRO 8840HS w/ Radeon 780M Graphics; commit ab7fe76; 128 designs, seed 1, 3 rounds; every figure MEASURED, as the run measures (CPU time over s6's, paired).
Drawn: the family uniformly, then each gene uniformly over its domain (lists: each member in or out with even odds, random order; folds cut to 23; pairs from the founders' pool).

alive: 108 of 128

| died of | designs |
|---|---|
| died: kernel workload | 12 |
| died: timed out | 6 |
| died: corpus | 1 |
| died: engine did not compile (/home/kvt/git/my/forth-vm-evolution/buil | 1 |

speed against s6: fastest 0.860, quartile 1.114, median 1.242, quartile 1.394, slowest 1.729; faster than s6: 10 of 108
size: smallest 10177, median 16304, largest 25144 bytes
the run's database's fastest, 0.595, is faster than 108 of the 108 sampled designs alive

| family | drawn | alive | fastest | median |
|---|---|---|---|---|
| cell | 26 | 26 | 1.075 | 1.245 |
| sod16 | 28 | 28 | 1.381 | 1.544 |
| cpt16 | 31 | 31 | 1.041 | 1.182 |
| cv8 | 43 | 23 | 0.860 | 1.036 |

## What it says

- **The front is a peak, not a plateau.** Of 108 random designs alive, the
  fastest is 0.860 and the median 1.242 - most are slower than s6; 10 beat
  s6. The run's best beats every one, in 31% less time than the best random design.
  The evolver found structure that random choice does not.
- **Deaths, audited** - the draws regenerated here (seeded: 125 of 125
  progress lines matched their design ids), each genome checked: 19 of 20
  are the reach limit of two-byte-only forms at scale 0 or 1, as in the
  run. **The 20th was a generator fault**, now fixed: design 1836554372,
  cached top of stack with format-10 words and no specialisations. Its
  engine did not compile - `tools/gen-tos.py` had dropped the `#endif` and
  `#if ENC == 3 && OPS10` between the specialisations and the format-10
  handlers, so those handlers were compiled only with SPEC. Fixing that
  uncovered a second one: `tools/gen-msc.py` compared the state tables
  with every handler's address unconditionally, so multi-state caching
  without specialisations could not compile either. Neither region was
  reached by either run; the sample reached it in 1 draw of 128.
- Three draws repeated an earlier one (cell has few genes) and were
  evaluated once.
