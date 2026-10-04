# Does the CPU change a design's ratio? - Ryzen 7 PRO 8840HS

Iteration 24. `next-run.sh experiment cpu-noise.py --rounds 20` at 286e1207
(Iteration 23), 2026-10-04: the six designs whose fib moved most between
Iteration 21's and 23's sessions, and hand-made s6, timed on four logical
CPUs - both threads of two cores: (2, 3) and (8, 9) - interleaved, every run
paired with s6 on the same CPU. A ratio is the best design run over the best
s6 run on that CPU.

**kernel, the control, agrees across the four CPUs within 0.8-2.4% for every
design. fib does not: 7-20%, and each design has its own best CPU** -
8dd8a7a146 best on cpu 2 (0.592), worst on cpu 8 (0.711); 29ad5ba726 best
on cpu 9, worst on cpu 8. It is not the core: cpu 2 and cpu 3 are one core,
and 8dd8a7a146 measures 0.592 on one and 0.659 on the other. s6's own fib
moves 3.9% (0.963-1.039), its best time 3% (32.8-33.7 ms).

Both workloads spread wide run to run - a design's median run 11.0% above
its best on fib, 8.5% on kernel - yet only kernel's best runs agree between
CPUs. So kernel's best-of-N finds a floor that is there every time, and
fib's does not: the next suspect is the estimator, not the CPU. If a fib run
depends on where it lands in memory - address randomisation draws anew each
run - the best of 20 is the luckiest placement drawn, which differs every
session. `lab/evolve/run-spread.py` keeps every run and asks.

Correction: Iteration 23 guessed cpu 8 to be cpu 0's sibling; on this laptop
siblings are adjacent - (2, 3), (8, 9) - as the tool read from /sys.

## The tables

## fib

| design | cpu 2 | cpu 3 | cpu 8 | cpu 9 | most / least |
|---|---|---|---|---|---|
| s6-cv8b | 1.023 | 1.039 | 0.963 | 1.022 | 1.079 |
| 8dd8a7a146 | 0.592 | 0.659 | 0.711 | 0.682 | 1.202 |
| 312ad2edaa | 0.676 | 0.748 | 0.709 | 0.677 | 1.106 |
| 550df563ee | 0.740 | 0.825 | 0.689 | 0.774 | 1.197 |
| 29ad5ba726 | 0.748 | 0.680 | 0.769 | 0.655 | 1.176 |
| 6463752a82 | 0.692 | 0.778 | 0.716 | 0.755 | 1.123 |
| 1769ca2a48 | 0.603 | 0.645 | 0.634 | 0.623 | 1.069 |
| s6 best, ms | 33.7 | 32.8 | 33.7 | 33.6 | 1.030 |

Within one CPU, a design's median run is 11.0% above its best (median over designs and CPUs), so a difference between CPUs well above that is the CPU.

## kernel

| design | cpu 2 | cpu 3 | cpu 8 | cpu 9 | most / least |
|---|---|---|---|---|---|
| s6-cv8b | 1.000 | 0.989 | 0.998 | 1.007 | 1.018 |
| 8dd8a7a146 | 0.634 | 0.637 | 0.640 | 0.636 | 1.008 |
| 312ad2edaa | 0.683 | 0.669 | 0.684 | 0.683 | 1.023 |
| 550df563ee | 0.698 | 0.688 | 0.694 | 0.688 | 1.016 |
| 29ad5ba726 | 0.631 | 0.638 | 0.630 | 0.629 | 1.016 |
| 6463752a82 | 0.694 | 0.708 | 0.692 | 0.700 | 1.024 |
| 1769ca2a48 | 0.678 | 0.672 | 0.675 | 0.681 | 1.014 |
| s6 best, ms | 10.8 | 10.9 | 10.8 | 10.8 | 1.007 |

Within one CPU, a design's median run is 8.5% above its best (median over designs and CPUs), so a difference between CPUs well above that is the CPU.

