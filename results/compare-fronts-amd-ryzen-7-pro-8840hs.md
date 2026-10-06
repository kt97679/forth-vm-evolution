# The fronts of all runs, measured in one session - Ryzen 7 PRO 8840HS

Iteration 21. `lab/evolve/next-run.sh compare` at 3be62f44 (Iteration 20),
2026-10-04, on the laptop: every design on the front of seeds 1-4 and of
the VM rehearsal - 34 - rebuilt with that commit (so the older ones carry
Iteration 13's restored words, 99-136 bytes smaller than recorded), passed
through the gate, and timed in one session: 10 rounds, round-robin over the
designs, every run paired with hand-made s6 on the pinned core
(`lab/evolve/compare-fronts.py`). Two minutes.

**Calibration: hand-made s6 against itself 0.991** - kernel 0.989, fib
0.946, parse 1.008, corpus 1.023, loop 1.010. Good enough to rank designs
two per cent apart overall; fib, again the noisiest workload (seed 4's run:
1.117), is not.

## Each run's front, all measured together

| run | its front in this session (speed at size) | the same designs in their own run |
|---|---|---|
| seed 1 | 0.623 at 13,368, 0.698 at 9,694, 0.779 at 9,662 | 0.620, 0.649, 0.705 |
| seed 2 | 0.688 at 13,368, 0.699 at 13,352, 0.725 at 9,662 | 0.619, 0.666, 0.667 |
| rehearsal (VM) | 0.609 at 13,352, 0.632 at 13,344, 0.685 at 9,694, 0.701 at 9,662 | (selected on the VM) |
| seed 3 | 0.600 at 13,352, 0.647 at 9,646 | 0.595, 0.696 |
| seed 4 | **0.591 at 13,352**, 0.613 at 13,209, **0.640 at 9,523**, 0.687 at 9,474, 0.709 at 9,450, 0.716 at 9,335 | 0.589, 0.603, 0.669, 0.678, 0.702, 0.727 |

**The front of all runs together is seed 4's, all seven designs** (seven at
full precision: 14f6036a4b, at 13,217, and 1769ca2a48 both show 0.613). Head to
head: at 13,352 bytes, 29ad5ba726 (seed 4) is 0.985 of 8dd8a7a146 (seed
3) - kernel 0.982, parse 0.937, corpus 0.984, fib 1.035; at the small end
6463752a82 (seed 4) is 0.989 of 550df563ee (seed 3) and 123 bytes smaller;
and seed 4 has three designs smaller than any earlier one (9,335-9,474).
What separates them is seed 4's genes - the two runs' designs were built
by the same converter and engine here, the body-check fix in both.

**The 7.5% that Iteration 20 left open was the sessions, not the designs**:
seed 3's 60753a0eb0, 0.622 in its own run, is 0.647 here; seed 4's
6463752a82, 0.669 in its own, is 0.640.

**One design moves by up to 7% between sessions** - seed 3's designs here
against their own run 0.930-1.040, seed 4's 0.957-1.052 - while the means
agree (1.000, 0.999). A re-measured figure is good within its session
only: designs are ranked here, in one session, or not at all. Seeds 1 and
2 measure 7% slower than in their runs (1.074, 1.073): their sessions, and
the engine changes since (their designs are built with today's), not
separated.

## Every design

loop is held out, and moves with an image's size mod 8 (Iteration 13).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| seed 4 | 3453246bdf | 0.716 | 0.727 | 9,335 | 9,335 | 0.791 | 0.698 | 0.658 | 0.721 | 0.859 | yes |
| seed 4 | 672538daf5 | 0.782 | 0.780 | 9,351 | 9,351 | 0.786 | 0.865 | 0.693 | 0.792 | 1.038 |  |
| seed 4 | 7fe7f039bd | 0.709 | 0.702 | 9,450 | 9,450 | 0.731 | 0.767 | 0.612 | 0.738 | 0.836 | yes |
| seed 4 | 38d91795a2 | 0.687 | 0.678 | 9,474 | 9,474 | 0.739 | 0.693 | 0.599 | 0.724 | 0.815 | yes |
| seed 4 | 6463752a82 | 0.640 | 0.669 | 9,523 | 9,523 | 0.695 | 0.649 | 0.564 | 0.658 | 0.869 | yes |
| seed 4 | 90018981c6 | 0.732 | 0.696 | 9,678 | 9,678 | 0.723 | 0.857 | 0.629 | 0.737 | 1.014 |  |
| seed 4 | e0cbf09bc2 | 0.642 | 0.666 | 13,057 | 13,057 | 0.708 | 0.760 | 0.522 | 0.604 | 0.948 |  |
| seed 4 | 1769ca2a48 | 0.613 | 0.603 | 13,209 | 13,209 | 0.665 | 0.654 | 0.522 | 0.624 | 0.834 | yes |
| seed 4 | 14f6036a4b | 0.613 | 0.627 | 13,217 | 13,217 | 0.647 | 0.810 | 0.473 | 0.568 | 0.893 | yes |
| seed 4 | 29ad5ba726 | 0.591 | 0.589 | 13,352 | 13,352 | 0.638 | 0.701 | 0.477 | 0.571 | 0.753 | yes |
| seed 4 | 12d8e18511 | 0.671 | 0.667 | 13,360 | 13,360 | 0.654 | 0.996 | 0.525 | 0.593 | 0.781 |  |
| rehearsal (VM) | 595fc2b8f4 | 0.701 | 0.784 | 9,662 | 9,761 | 0.741 | 0.713 | 0.646 | 0.707 | 1.072 |  |
| rehearsal (VM) | 6738aed13f | 0.685 | 0.755 | 9,694 | 9,793 | 0.731 | 0.703 | 0.626 | 0.686 | 1.103 |  |
| rehearsal (VM) | 8cbc6dd05c | 0.695 | 0.742 | 9,694 | 9,809 | 0.699 | 0.803 | 0.608 | 0.682 | 0.879 |  |
| rehearsal (VM) | 312ad2edaa | 0.632 | 0.716 | 13,344 | 13,456 | 0.654 | 0.738 | 0.525 | 0.629 | 0.852 |  |
| rehearsal (VM) | 05617039f6 | 0.609 | 0.674 | 13,352 | 13,488 | 0.663 | 0.744 | 0.473 | 0.589 | 0.693 |  |
| rehearsal (VM) | 0b1d16def9 | 0.640 | 0.705 | 13,352 | 13,464 | 0.715 | 0.779 | 0.493 | 0.613 | 0.785 |  |
| rehearsal (VM) | 57a9dcc7cb | 0.660 | 0.680 | 13,368 | 13,480 | 0.686 | 0.840 | 0.529 | 0.623 | 0.952 |  |
| rehearsal (VM) | 32600cab87 | 0.723 | 0.662 | 13,528 | 13,656 | 0.645 | 1.396 | 0.510 | 0.597 | 0.709 |  |
| seed 1 | 83cb81c383 | 0.779 | 0.705 | 9,662 | 9,761 | 0.733 | 0.999 | 0.689 | 0.729 | 1.023 |  |
| seed 1 | 5b70f3dd64 | 0.698 | 0.649 | 9,694 | 9,801 | 0.730 | 0.768 | 0.624 | 0.678 | 0.821 |  |
| seed 1 | a4e82e02e5 | 0.723 | 0.654 | 9,694 | 9,809 | 0.765 | 0.796 | 0.651 | 0.690 | 1.005 |  |
| seed 1 | 53ec9bedde | 0.707 | 0.670 | 13,336 | 13,464 | 0.715 | 0.795 | 0.623 | 0.705 | 0.823 |  |
| seed 1 | 448ef1ef43 | 0.623 | 0.620 | 13,368 | 13,488 | 0.651 | 0.793 | 0.494 | 0.589 | 0.800 |  |
| seed 1 | 38d187239c | 0.670 | 0.609 | 13,368 | 13,480 | 0.731 | 0.813 | 0.549 | 0.619 | 0.771 |  |
| seed 2 | 0ebf0445e0 | 0.725 | 0.667 | 9,662 | 9,761 | 0.781 | 0.699 | 0.693 | 0.732 | 0.987 |  |
| seed 2 | c17103bf95 | 0.753 | 0.725 | 9,662 | 9,769 | 0.794 | 0.763 | 0.712 | 0.744 | 0.904 |  |
| seed 2 | a285fa6ba3 | 0.699 | 0.666 | 13,352 | 13,464 | 0.745 | 0.744 | 0.617 | 0.697 | 0.908 |  |
| seed 2 | 57e0e77c09 | 0.707 | 0.657 | 13,352 | 13,480 | 0.711 | 1.050 | 0.537 | 0.623 | 0.894 |  |
| seed 2 | 9cd791dd84 | 0.688 | 0.619 | 13,368 | 13,472 | 0.704 | 0.869 | 0.574 | 0.638 | 1.008 |  |
| seed 3 | 550df563ee | 0.647 | 0.696 | 9,646 | 9,745 | 0.693 | 0.624 | 0.619 | 0.656 | 0.955 |  |
| seed 3 | f4a6dd9a13 | 0.699 | 0.683 | 9,662 | 9,761 | 0.738 | 0.748 | 0.608 | 0.711 | 0.976 |  |
| seed 3 | 60753a0eb0 | 0.647 | 0.622 | 9,686 | 9,785 | 0.693 | 0.705 | 0.558 | 0.643 | 0.913 |  |
| seed 3 | 8dd8a7a146 | 0.600 | 0.595 | 13,352 | 13,464 | 0.650 | 0.677 | 0.509 | 0.580 | 0.839 |  |

## A second session, and the first one's conclusion withdrawn (Iteration 23)

`next-run.sh compare` again at c1cfa19b, with the seed 4 replicate added:
41 designs, 10 rounds, pinned to cpu 2 (the first session: cpu 8).
**Calibration 0.996** - kernel 1.007, fib 0.981, parse 0.994, corpus 1.002 -
the best yet. And it does not reproduce the first: the front of all runs
together is 8dd8a7a146 (seed 3) 0.564 at 13,352, 312ad2edaa (rehearsal)
0.594 at 13,344, e99da68667 (replicate) 0.601 at 13,201, 84e302c470
(replicate) 0.622 at 13,065, 66eb4a8f15 (replicate) 0.631 at 13,057,
60753a0eb0 (seed 3) 0.636 at 9,686, 6463752a82 (seed 4) 0.661 at 9,523,
c297551359 (replicate) 0.672 at 9,450, 05dcc81cdc (replicate) 0.703 at 9,335.

**"The front of all runs together is seed 4's" is withdrawn**: it was
inside the noise. The same 34 designs, second session over first:

| workload | 10-90% of the designs | extremes |
|---|---|---|
| parse | 0.981-1.033 | 0.964-1.043 |
| kernel | 0.960-1.058 | 0.941-1.065 |
| corpus | 0.965-1.064 | 0.948-1.077 |
| **fib** | **0.784-1.137** | **0.709-1.275** |

The flip at the fast end is fib alone: 8dd8a7a146's kernel, parse and
corpus moved under 2%, its fib 0.677 -> 0.531; 550df563ee's fib 0.624 ->
0.792. s6's own fib calibration was 0.946 and 0.981: fib is not noisy for
s6, it moves each design its own way between sessions. What stands: the
sizes (exact), seed 4's genes reaching 9,335-9,523 bytes where the earlier
seeds stop at 9,646; and a ranking by speed among these fronts that no
session has yet made reproducible. Rank order agreement between the two
sessions: Spearman 0.86. Process address randomisation is ruled out on
the development VM (`lab/evolve/cpu-noise.py`'s docstring); the pinned CPU
is the next suspect (GOALS.md).

### Every design, second session

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 05dcc81cdc | 0.703 | 0.688 | 9,335 | 9,335 | 0.727 | 0.831 | 0.602 | 0.671 | 0.928 | yes |
| this clone: db.jsonl | c297551359 | 0.672 | 0.682 | 9,450 | 9,450 | 0.735 | 0.658 | 0.638 | 0.659 | 0.837 | yes |
| this clone: db.jsonl | e8f1dd3ca2 | 0.685 | 0.678 | 9,458 | 9,458 | 0.693 | 0.811 | 0.585 | 0.671 | 0.954 |  |
| this clone: db.jsonl | 66eb4a8f15 | 0.631 | 0.641 | 13,057 | 13,057 | 0.701 | 0.664 | 0.527 | 0.648 | 0.923 | yes |
| this clone: db.jsonl | 84e302c470 | 0.622 | 0.657 | 13,065 | 13,065 | 0.733 | 0.567 | 0.544 | 0.664 | 0.955 | yes |
| this clone: db.jsonl | 4cb3fa9172 | 0.629 | 0.626 | 13,073 | 13,073 | 0.646 | 0.851 | 0.484 | 0.588 | 0.868 |  |
| this clone: db.jsonl | e99da68667 | 0.601 | 0.581 | 13,201 | 13,201 | 0.606 | 0.839 | 0.455 | 0.563 | 0.970 | yes |
| archived-20261004-200423: db-rehearsal.jsonl | 595fc2b8f4 | 0.696 | 0.784 | 9,662 | 9,761 | 0.739 | 0.722 | 0.629 | 0.699 | 1.042 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 6738aed13f | 0.678 | 0.755 | 9,694 | 9,793 | 0.725 | 0.691 | 0.629 | 0.672 | 1.073 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 8cbc6dd05c | 0.691 | 0.742 | 9,694 | 9,809 | 0.703 | 0.812 | 0.604 | 0.661 | 0.899 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 312ad2edaa | 0.594 | 0.716 | 13,344 | 13,456 | 0.683 | 0.552 | 0.546 | 0.607 | 0.874 | yes |
| archived-20261004-200423: db-rehearsal.jsonl | 05617039f6 | 0.606 | 0.674 | 13,352 | 13,488 | 0.680 | 0.740 | 0.456 | 0.589 | 0.432 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 0b1d16def9 | 0.631 | 0.705 | 13,352 | 13,464 | 0.686 | 0.751 | 0.514 | 0.598 | 0.776 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 57a9dcc7cb | 0.705 | 0.680 | 13,368 | 13,480 | 0.726 | 0.977 | 0.549 | 0.633 | 0.867 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 32600cab87 | 0.670 | 0.662 | 13,528 | 13,656 | 0.664 | 0.990 | 0.510 | 0.602 | 0.713 |  |
| archived-20261004-200423: db-seed1.jsonl | 83cb81c383 | 0.796 | 0.705 | 9,662 | 9,761 | 0.771 | 1.001 | 0.695 | 0.748 | 1.057 |  |
| archived-20261004-200423: db-seed1.jsonl | 5b70f3dd64 | 0.727 | 0.649 | 9,694 | 9,801 | 0.752 | 0.864 | 0.627 | 0.684 | 0.884 |  |
| archived-20261004-200423: db-seed1.jsonl | a4e82e02e5 | 0.749 | 0.654 | 9,694 | 9,809 | 0.798 | 0.825 | 0.657 | 0.728 | 1.007 |  |
| archived-20261004-200423: db-seed1.jsonl | 53ec9bedde | 0.686 | 0.670 | 13,336 | 13,464 | 0.704 | 0.740 | 0.615 | 0.692 | 0.853 |  |
| archived-20261004-200423: db-seed1.jsonl | 38d187239c | 0.658 | 0.609 | 13,368 | 13,480 | 0.710 | 0.786 | 0.550 | 0.610 | 0.790 |  |
| archived-20261004-200423: db-seed1.jsonl | 448ef1ef43 | 0.659 | 0.620 | 13,368 | 13,488 | 0.660 | 1.011 | 0.491 | 0.577 | 0.710 |  |
| archived-20261004-200423: db-seed2.jsonl | 0ebf0445e0 | 0.722 | 0.667 | 9,662 | 9,761 | 0.750 | 0.696 | 0.706 | 0.737 | 0.979 |  |
| archived-20261004-200423: db-seed2.jsonl | c17103bf95 | 0.781 | 0.725 | 9,662 | 9,769 | 0.803 | 0.833 | 0.695 | 0.801 | 0.953 |  |
| archived-20261004-200423: db-seed2.jsonl | a285fa6ba3 | 0.696 | 0.666 | 13,352 | 13,464 | 0.756 | 0.703 | 0.624 | 0.706 | 0.913 |  |
| archived-20261004-200423: db-seed2.jsonl | 57e0e77c09 | 0.716 | 0.657 | 13,352 | 13,480 | 0.725 | 1.049 | 0.543 | 0.635 | 0.916 |  |
| archived-20261004-200423: db-seed2.jsonl | 9cd791dd84 | 0.707 | 0.619 | 13,368 | 13,472 | 0.732 | 0.870 | 0.572 | 0.687 | 1.006 |  |
| archived-20261004-200423: db.jsonl | 550df563ee | 0.695 | 0.696 | 9,646 | 9,745 | 0.680 | 0.792 | 0.620 | 0.698 | 0.976 |  |
| archived-20261004-200423: db.jsonl | f4a6dd9a13 | 0.670 | 0.683 | 9,662 | 9,761 | 0.719 | 0.655 | 0.608 | 0.706 | 1.019 |  |
| archived-20261004-200423: db.jsonl | 60753a0eb0 | 0.636 | 0.622 | 9,686 | 9,785 | 0.652 | 0.659 | 0.564 | 0.677 | 0.902 | yes |
| archived-20261004-200423: db.jsonl | 8dd8a7a146 | 0.564 | 0.595 | 13,352 | 13,464 | 0.653 | 0.531 | 0.511 | 0.570 | 0.883 | yes |
| archived-20261004-214724: db.jsonl | 3453246bdf | 0.709 | 0.727 | 9,335 | 9,335 | 0.751 | 0.667 | 0.680 | 0.739 | 0.881 |  |
| archived-20261004-214724: db.jsonl | 672538daf5 | 0.765 | 0.780 | 9,351 | 9,351 | 0.819 | 0.795 | 0.696 | 0.754 | 0.995 |  |
| archived-20261004-214724: db.jsonl | 7fe7f039bd | 0.682 | 0.702 | 9,450 | 9,450 | 0.770 | 0.650 | 0.613 | 0.704 | 0.853 |  |
| archived-20261004-214724: db.jsonl | 38d91795a2 | 0.678 | 0.678 | 9,474 | 9,474 | 0.732 | 0.653 | 0.618 | 0.716 | 0.865 |  |
| archived-20261004-214724: db.jsonl | 6463752a82 | 0.661 | 0.669 | 9,523 | 9,523 | 0.681 | 0.738 | 0.573 | 0.664 | 0.879 | yes |
| archived-20261004-214724: db.jsonl | 90018981c6 | 0.724 | 0.696 | 9,678 | 9,678 | 0.770 | 0.828 | 0.617 | 0.699 | 1.061 |  |
| archived-20261004-214724: db.jsonl | e0cbf09bc2 | 0.658 | 0.666 | 13,057 | 13,057 | 0.681 | 0.788 | 0.538 | 0.649 | 0.973 |  |
| archived-20261004-214724: db.jsonl | 1769ca2a48 | 0.616 | 0.603 | 13,209 | 13,209 | 0.705 | 0.600 | 0.538 | 0.635 | 0.879 |  |
| archived-20261004-214724: db.jsonl | 14f6036a4b | 0.629 | 0.627 | 13,217 | 13,217 | 0.662 | 0.862 | 0.473 | 0.580 | 0.935 |  |
| archived-20261004-214724: db.jsonl | 29ad5ba726 | 0.604 | 0.589 | 13,352 | 13,352 | 0.635 | 0.754 | 0.476 | 0.585 | 0.760 |  |
| archived-20261004-214724: db.jsonl | 12d8e18511 | 0.638 | 0.667 | 13,360 | 13,360 | 0.693 | 0.779 | 0.528 | 0.580 | 0.910 |  |

## A third session: by the median, on two CPUs (Iteration 26)

`next-run.sh experiment compare-fronts.py --rounds 10 --cpus 2,8` at
c5a4648c (Iteration 25): all 41 designs, every one timed on cpu 2 and cpu 8
of two cores in one session, interleaved, **by the median of the rounds**.
Calibration 0.999 on cpu 2, 0.992 on cpu 8.

**The CPUs agree**: per design, cpu 2 over cpu 8 is 1.002 at the median,
0.988-1.017 for 10-90% of the designs, 0.975-1.028 at the extremes; rank
agreement 0.98 (the two best-of-N sessions: 0.86, fib alone 0.71-1.28). All
seven designs on cpu 2's front are on cpu 8's; cpu 8 adds one.

Each run's front, by the median over both CPUs (20 rounds a design):

| run | its front (speed at size) |
|---|---|
| seed 1 | 0.665 at 13,368, 0.693 at 13,336, 0.733 at 9,694, 0.790 at 9,662 |
| seed 2 | 0.694 at 13,352, 0.722 at 9,662 |
| rehearsal (VM) | 0.622 at 13,352, 0.645 at 13,344, 0.691 at 9,694, 0.699 at 9,662 |
| seed 3 | 0.606 at 13,352, 0.648 at 9,686, 0.671 at 9,662, 0.695 at 9,646 |
| seed 4 (first) | 0.613 at 13,352, 0.616 at 13,209, 0.645 at 13,057, 0.658 at 9,523, 0.675 at 9,474, 0.691 at 9,450, 0.714 at 9,335 |
| seed 4 (replicate) | **0.588 at 13,201**, 0.624 at 13,073, 0.634 at 13,057, 0.680 at 9,450, 0.700 at 9,335 |

**The front of all runs, measured fairly: seven of its eight designs are
seed 4's** - five from the replicate, two from the first run - and one is
seed 3's (60753a0eb0, 0.648 at 9,686). At the fast end the replicate's
e99da68667 is 0.970 of seed 3's best and 151 bytes smaller (and 0.959 of the
first seed 4 run's best - same seed, same code: selection by the best of N
picked worse in the noisier run). At the small end the speeds tie within
the measurement (seed 4's 6463752a82 1.016 of seed 3's 60753a0eb0, 163
bytes smaller; 05dcc81cdc 1.006 of 550df563ee, 311 smaller).

**Iteration 23's reversal was a lucky run**: 8dd8a7a146, there "fastest of
all" at 0.564, is the design whose best fib run was 14.9 ms against a median
of 23.9 (Iteration 25); by the median it is 0.606. Iteration 21's reading -
seed 4 ahead - stands, by the median, with one seed 3 design kept at 9,686.

### The two CPUs, every design

Calibration on cpu 2: 0.999; on cpu 8: 0.992.

Speed on cpu 2 over speed on cpu 8, per design: median 1.002, 10-90% 0.988-1.017, extremes 0.975-1.028; rank agreement (Spearman) 0.98.

The front of all runs on cpu 2: e99da68667 0.594 at 13,201, 4cb3fa9172 0.623 at 13,073, 66eb4a8f15 0.634 at 13,057, 6463752a82 0.656 at 9,523, 38d91795a2 0.671 at 9,474, c297551359 0.676 at 9,450, 05dcc81cdc 0.704 at 9,335

The front of all runs on cpu 8: e99da68667 0.582 at 13,201, 4cb3fa9172 0.625 at 13,073, 66eb4a8f15 0.635 at 13,057, 60753a0eb0 0.639 at 9,686, 6463752a82 0.661 at 9,523, 38d91795a2 0.679 at 9,474, c297551359 0.684 at 9,450, 05dcc81cdc 0.696 at 9,335

On both fronts: 7 of 7 and 8.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| e99da68667 | 0.594 | 0.582 | 1.022 |
| 8dd8a7a146 | 0.611 | 0.601 | 1.016 |
| 29ad5ba726 | 0.612 | 0.614 | 0.998 |
| 1769ca2a48 | 0.617 | 0.615 | 1.003 |
| 05617039f6 | 0.620 | 0.625 | 0.992 |
| 4cb3fa9172 | 0.623 | 0.625 | 0.996 |
| 14f6036a4b | 0.624 | 0.627 | 0.995 |
| 66eb4a8f15 | 0.634 | 0.635 | 0.999 |
| 312ad2edaa | 0.641 | 0.650 | 0.986 |
| e0cbf09bc2 | 0.646 | 0.644 | 1.002 |
| 12d8e18511 | 0.649 | 0.659 | 0.985 |
| 0b1d16def9 | 0.654 | 0.652 | 1.003 |
| 6463752a82 | 0.656 | 0.661 | 0.992 |
| 60753a0eb0 | 0.657 | 0.639 | 1.028 |
| 84e302c470 | 0.658 | 0.675 | 0.975 |
| 38d91795a2 | 0.671 | 0.679 | 0.987 |
| 448ef1ef43 | 0.671 | 0.660 | 1.017 |
| f4a6dd9a13 | 0.672 | 0.671 | 1.001 |
| 38d187239c | 0.672 | 0.666 | 1.010 |
| c297551359 | 0.676 | 0.684 | 0.989 |
| 32600cab87 | 0.679 | 0.669 | 1.014 |
| e8f1dd3ca2 | 0.685 | 0.687 | 0.998 |
| 6738aed13f | 0.693 | 0.689 | 1.005 |
| 7fe7f039bd | 0.693 | 0.690 | 1.004 |
| 57a9dcc7cb | 0.693 | 0.688 | 1.008 |
| 8cbc6dd05c | 0.697 | 0.698 | 0.999 |
| a285fa6ba3 | 0.699 | 0.689 | 1.014 |
| 53ec9bedde | 0.699 | 0.688 | 1.016 |
| 9cd791dd84 | 0.700 | 0.704 | 0.994 |
| 550df563ee | 0.702 | 0.689 | 1.019 |
| 595fc2b8f4 | 0.703 | 0.696 | 1.010 |
| 05dcc81cdc | 0.704 | 0.696 | 1.010 |
| 3453246bdf | 0.710 | 0.719 | 0.988 |
| 57e0e77c09 | 0.715 | 0.706 | 1.013 |
| 0ebf0445e0 | 0.726 | 0.718 | 1.012 |
| 5b70f3dd64 | 0.733 | 0.734 | 0.997 |
| 90018981c6 | 0.737 | 0.725 | 1.017 |
| c17103bf95 | 0.747 | 0.748 | 0.998 |
| a4e82e02e5 | 0.770 | 0.759 | 1.013 |
| 672538daf5 | 0.776 | 0.776 | 1.000 |
| 83cb81c383 | 0.790 | 0.791 | 0.999 |

## Session 4 - Iteration 36: seeds 1-6, after seed 6, on two CPUs

`seed 6 then experiment compare-fronts.py --rounds 10 --cpus 2,8` (Iteration
35's chain), commit 34f3873c: eight databases - the rehearsal, seeds 1-5
archived, seed 6 in the clone - 64 front designs, 10 rounds each by the
median, paired with s6 on cpu 2 and cpu 8. Six and a half minutes.

**Calibration 0.996** (cpu 2: 0.996, cpu 8: 1.011). The CPUs agree: speed
on cpu 2 over cpu 8 per design median 1.001, 10-90% 0.987-1.017; rank
agreement 0.99.

**The front of all runs is seed 6's**: all ten designs, on both CPUs.
Against the fastest earlier design no larger, in this one session:

| seed 6 | size | speed | the fastest earlier design no larger | seed 6 / it |
|---|---|---|---|---|
| 422d6bcbca | 9,327 | 0.685 | none so small | - |
| 6495dcb5dd | 9,343 | 0.660 | 05dcc81cdc (seed 4b) 0.705 at 9,335 | 0.936 |
| c40ba92d5b | 9,511 | 0.631 | e8f1dd3ca2 (seed 4b) 0.667 at 9,458 | 0.946 |
| c61857fc89 | 10,034 | 0.629 | 5ed1ed8715 (seed 5) 0.638 at 10,018 | 0.986 |
| b06a4cf784 | 10,246 | 0.615 | 5ed1ed8715 (seed 5) 0.638 | 0.964 |
| af5e8dc29f | 10,254 | 0.612 | 5ed1ed8715 (seed 5) 0.638 | 0.959 |
| a74b828e9b | 13,073 | 0.607 | 9e50623ac1 (seed 5) 0.610 at 13,073 | 0.995 |
| dc02ceae31 | 13,161 | 0.564 | 9e50623ac1 (seed 5) 0.610 | 0.925 |
| 15dde12f04 | 13,345 | 0.557 | e99da68667 (seed 4b) 0.582 at 13,201 | 0.957 |
| cd943ed219 | 14,081 | 0.547 | e99da68667 (seed 4b) 0.582 | 0.940 |

**Seed 5's provisional claims, settled** (Iteration 28 compared across
sessions): its "new fastest, 0.579 at 14,017" (2db525ff95) measures 0.585
here - slower than seed 4b's e99da68667, 0.582 at 13,201, which dominates
it; its "0.593 at 13,073, 5% faster" (9e50623ac1) measures 0.610. Before
seed 6 the front of all runs was shared - seed 4b five designs (the
fastest, 0.582 at 13,201), seed 5 four (9,359 to 13,073), seed 3 one
(9,686): seed 5 held its place, and set no record.

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 0.996** (kernel 1.010, fib 0.987, parse 1.000, corpus 0.989, loop 0.997).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 422d6bcbca | 0.685 | 0.699 | 9,327 | 9,327 | 0.730 | 0.858 | 0.536 | 0.658 | 0.971 | yes |
| this clone: db.jsonl | 090672993b | 0.704 | 0.700 | 9,335 | 9,335 | 0.691 | 0.859 | 0.623 | 0.664 | 0.878 |  |
| this clone: db.jsonl | 6495dcb5dd | 0.660 | 0.662 | 9,343 | 9,343 | 0.655 | 0.919 | 0.516 | 0.611 | 0.818 | yes |
| this clone: db.jsonl | c40ba92d5b | 0.631 | 0.630 | 9,511 | 9,511 | 0.674 | 0.688 | 0.545 | 0.628 | 0.798 | yes |
| this clone: db.jsonl | ca2ac63866 | 0.639 | 0.634 | 9,531 | 9,531 | 0.656 | 0.721 | 0.557 | 0.636 | 0.921 |  |
| this clone: db.jsonl | c61857fc89 | 0.629 | 0.633 | 10,034 | 10,034 | 0.672 | 0.703 | 0.527 | 0.628 | 0.743 | yes |
| this clone: db.jsonl | b06a4cf784 | 0.615 | 0.615 | 10,246 | 10,246 | 0.642 | 0.702 | 0.524 | 0.606 | 0.870 | yes |
| this clone: db.jsonl | af5e8dc29f | 0.612 | 0.604 | 10,254 | 10,254 | 0.646 | 0.678 | 0.537 | 0.597 | 0.882 | yes |
| this clone: db.jsonl | a74b828e9b | 0.607 | 0.608 | 13,073 | 13,073 | 0.690 | 0.637 | 0.501 | 0.617 | 0.955 | yes |
| this clone: db.jsonl | dc02ceae31 | 0.564 | 0.560 | 13,161 | 13,161 | 0.621 | 0.695 | 0.440 | 0.533 | 0.768 | yes |
| this clone: db.jsonl | 15dde12f04 | 0.557 | 0.567 | 13,345 | 13,345 | 0.611 | 0.747 | 0.399 | 0.529 | 0.764 | yes |
| this clone: db.jsonl | cd943ed219 | 0.547 | 0.545 | 14,081 | 14,081 | 0.615 | 0.680 | 0.402 | 0.532 | 0.802 | yes |
| archived-20261004-200423: db-rehearsal.jsonl | 595fc2b8f4 | 0.696 | 0.784 | 9,662 | 9,761 | 0.746 | 0.731 | 0.608 | 0.710 | 1.040 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 8cbc6dd05c | 0.697 | 0.742 | 9,694 | 9,809 | 0.736 | 0.779 | 0.613 | 0.673 | 0.865 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 6738aed13f | 0.700 | 0.755 | 9,694 | 9,793 | 0.768 | 0.699 | 0.632 | 0.708 | 1.051 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 312ad2edaa | 0.643 | 0.716 | 13,344 | 13,456 | 0.688 | 0.721 | 0.553 | 0.623 | 0.878 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 05617039f6 | 0.622 | 0.674 | 13,352 | 13,488 | 0.678 | 0.787 | 0.463 | 0.606 | 0.701 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 0b1d16def9 | 0.656 | 0.705 | 13,352 | 13,464 | 0.717 | 0.821 | 0.494 | 0.637 | 0.803 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 57a9dcc7cb | 0.675 | 0.680 | 13,368 | 13,480 | 0.715 | 0.878 | 0.524 | 0.631 | 0.960 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 32600cab87 | 0.668 | 0.662 | 13,528 | 13,656 | 0.666 | 0.944 | 0.514 | 0.618 | 0.705 |  |
| archived-20261004-200423: db-seed1.jsonl | 83cb81c383 | 0.787 | 0.705 | 9,662 | 9,761 | 0.774 | 0.981 | 0.689 | 0.734 | 1.069 |  |
| archived-20261004-200423: db-seed1.jsonl | 5b70f3dd64 | 0.737 | 0.649 | 9,694 | 9,801 | 0.735 | 0.949 | 0.612 | 0.690 | 0.862 |  |
| archived-20261004-200423: db-seed1.jsonl | a4e82e02e5 | 0.756 | 0.654 | 9,694 | 9,809 | 0.781 | 0.855 | 0.671 | 0.729 | 1.007 |  |
| archived-20261004-200423: db-seed1.jsonl | 53ec9bedde | 0.693 | 0.670 | 13,336 | 13,464 | 0.720 | 0.779 | 0.605 | 0.678 | 0.870 |  |
| archived-20261004-200423: db-seed1.jsonl | 448ef1ef43 | 0.658 | 0.620 | 13,368 | 13,488 | 0.667 | 0.959 | 0.492 | 0.598 | 0.811 |  |
| archived-20261004-200423: db-seed1.jsonl | 38d187239c | 0.675 | 0.609 | 13,368 | 13,480 | 0.719 | 0.823 | 0.550 | 0.637 | 0.788 |  |
| archived-20261004-200423: db-seed2.jsonl | 0ebf0445e0 | 0.730 | 0.667 | 9,662 | 9,761 | 0.796 | 0.689 | 0.691 | 0.746 | 1.000 |  |
| archived-20261004-200423: db-seed2.jsonl | c17103bf95 | 0.754 | 0.725 | 9,662 | 9,769 | 0.790 | 0.769 | 0.708 | 0.754 | 0.908 |  |
| archived-20261004-200423: db-seed2.jsonl | a285fa6ba3 | 0.687 | 0.666 | 13,352 | 13,464 | 0.754 | 0.690 | 0.625 | 0.686 | 0.927 |  |
| archived-20261004-200423: db-seed2.jsonl | 57e0e77c09 | 0.716 | 0.657 | 13,352 | 13,480 | 0.720 | 1.025 | 0.552 | 0.646 | 0.918 |  |
| archived-20261004-200423: db-seed2.jsonl | 9cd791dd84 | 0.709 | 0.619 | 13,368 | 13,472 | 0.719 | 0.904 | 0.574 | 0.678 | 1.007 |  |
| archived-20261004-200423: db.jsonl | 550df563ee | 0.689 | 0.696 | 9,646 | 9,745 | 0.697 | 0.785 | 0.608 | 0.677 | 0.977 |  |
| archived-20261004-200423: db.jsonl | f4a6dd9a13 | 0.679 | 0.683 | 9,662 | 9,761 | 0.730 | 0.674 | 0.618 | 0.697 | 0.968 |  |
| archived-20261004-200423: db.jsonl | 60753a0eb0 | 0.644 | 0.622 | 9,686 | 9,785 | 0.688 | 0.681 | 0.561 | 0.655 | 0.908 |  |
| archived-20261004-200423: db.jsonl | 8dd8a7a146 | 0.596 | 0.595 | 13,352 | 13,464 | 0.641 | 0.649 | 0.509 | 0.595 | 0.852 |  |
| archived-20261004-214724: db.jsonl | 3453246bdf | 0.716 | 0.727 | 9,335 | 9,335 | 0.754 | 0.696 | 0.685 | 0.732 | 0.887 |  |
| archived-20261004-214724: db.jsonl | 672538daf5 | 0.793 | 0.780 | 9,351 | 9,351 | 0.811 | 0.875 | 0.703 | 0.795 | 1.036 |  |
| archived-20261004-214724: db.jsonl | 7fe7f039bd | 0.694 | 0.702 | 9,450 | 9,450 | 0.765 | 0.692 | 0.629 | 0.698 | 0.831 |  |
| archived-20261004-214724: db.jsonl | 38d91795a2 | 0.676 | 0.678 | 9,474 | 9,474 | 0.758 | 0.646 | 0.603 | 0.706 | 0.854 |  |
| archived-20261004-214724: db.jsonl | 6463752a82 | 0.671 | 0.669 | 9,523 | 9,523 | 0.728 | 0.729 | 0.587 | 0.649 | 0.882 |  |
| archived-20261004-214724: db.jsonl | 90018981c6 | 0.728 | 0.696 | 9,678 | 9,678 | 0.734 | 0.863 | 0.633 | 0.701 | 0.989 |  |
| archived-20261004-214724: db.jsonl | e0cbf09bc2 | 0.654 | 0.666 | 13,057 | 13,057 | 0.687 | 0.775 | 0.526 | 0.652 | 0.945 |  |
| archived-20261004-214724: db.jsonl | 1769ca2a48 | 0.616 | 0.603 | 13,209 | 13,209 | 0.688 | 0.625 | 0.517 | 0.647 | 0.860 |  |
| archived-20261004-214724: db.jsonl | 14f6036a4b | 0.637 | 0.627 | 13,217 | 13,217 | 0.674 | 0.868 | 0.471 | 0.597 | 0.922 |  |
| archived-20261004-214724: db.jsonl | 29ad5ba726 | 0.612 | 0.589 | 13,352 | 13,352 | 0.645 | 0.762 | 0.487 | 0.585 | 0.799 |  |
| archived-20261004-214724: db.jsonl | 12d8e18511 | 0.654 | 0.667 | 13,360 | 13,360 | 0.691 | 0.836 | 0.519 | 0.612 | 0.928 |  |
| archived-20261005-013645: db.jsonl | 05dcc81cdc | 0.705 | 0.688 | 9,335 | 9,335 | 0.733 | 0.794 | 0.605 | 0.702 | 0.917 |  |
| archived-20261005-013645: db.jsonl | c297551359 | 0.679 | 0.682 | 9,450 | 9,450 | 0.738 | 0.658 | 0.634 | 0.690 | 0.804 |  |
| archived-20261005-013645: db.jsonl | e8f1dd3ca2 | 0.667 | 0.678 | 9,458 | 9,458 | 0.674 | 0.811 | 0.572 | 0.634 | 0.948 |  |
| archived-20261005-013645: db.jsonl | 66eb4a8f15 | 0.629 | 0.641 | 13,057 | 13,057 | 0.691 | 0.693 | 0.518 | 0.632 | 0.901 |  |
| archived-20261005-013645: db.jsonl | 84e302c470 | 0.670 | 0.657 | 13,065 | 13,065 | 0.721 | 0.773 | 0.551 | 0.655 | 0.984 |  |
| archived-20261005-013645: db.jsonl | 4cb3fa9172 | 0.618 | 0.626 | 13,073 | 13,073 | 0.661 | 0.798 | 0.482 | 0.572 | 0.949 |  |
| archived-20261005-013645: db.jsonl | e99da68667 | 0.582 | 0.581 | 13,201 | 13,201 | 0.607 | 0.754 | 0.442 | 0.568 | 0.990 |  |
| archived-20261005-042924: db.jsonl | 98736f0596 | 0.725 | 0.731 | 9,335 | 9,335 | 0.777 | 0.731 | 0.667 | 0.730 | 1.017 |  |
| archived-20261005-042924: db.jsonl | 4f010d8ab9 | 0.722 | 0.721 | 9,343 | 9,343 | 0.785 | 0.730 | 0.651 | 0.728 | 1.003 |  |
| archived-20261005-042924: db.jsonl | 4032a5ce71 | 0.705 | 0.698 | 9,351 | 9,351 | 0.766 | 0.799 | 0.577 | 0.702 | 0.978 |  |
| archived-20261005-042924: db.jsonl | 528fc9619a | 0.703 | 0.702 | 9,359 | 9,359 | 0.765 | 0.756 | 0.589 | 0.718 | 0.996 |  |
| archived-20261005-042924: db.jsonl | f052397620 | 0.680 | 0.685 | 9,450 | 9,450 | 0.719 | 0.774 | 0.578 | 0.664 | 0.900 |  |
| archived-20261005-042924: db.jsonl | 8dc0f97f2c | 0.670 | 0.680 | 9,458 | 9,458 | 0.707 | 0.758 | 0.562 | 0.670 | 0.930 |  |
| archived-20261005-042924: db.jsonl | 52b80007a1 | 0.639 | 0.640 | 10,010 | 10,010 | 0.735 | 0.548 | 0.589 | 0.700 | 0.987 |  |
| archived-20261005-042924: db.jsonl | 5ed1ed8715 | 0.638 | 0.642 | 10,018 | 10,018 | 0.724 | 0.534 | 0.619 | 0.692 | 0.988 |  |
| archived-20261005-042924: db.jsonl | 9e50623ac1 | 0.610 | 0.593 | 13,073 | 13,073 | 0.673 | 0.715 | 0.492 | 0.584 | 0.908 |  |
| archived-20261005-042924: db.jsonl | 22b81e50c4 | 0.593 | 0.605 | 13,209 | 13,209 | 0.625 | 0.868 | 0.413 | 0.550 | 0.943 |  |
| archived-20261005-042924: db.jsonl | 2db525ff95 | 0.585 | 0.579 | 14,017 | 14,017 | 0.646 | 0.693 | 0.448 | 0.586 | 0.952 |  |

The front of all runs together, by size: cd943ed219 0.547 at 14,081, 15dde12f04 0.557 at 13,345, dc02ceae31 0.564 at 13,161, a74b828e9b 0.607 at 13,073, af5e8dc29f 0.612 at 10,254, b06a4cf784 0.615 at 10,246, c61857fc89 0.629 at 10,034, c40ba92d5b 0.631 at 9,511, 6495dcb5dd 0.660 at 9,343, 422d6bcbca 0.685 at 9,327

## The same session on two CPUs

Calibration on cpu 2: 0.996; on cpu 8: 1.011.

Speed on cpu 2 over speed on cpu 8, per design: median 1.001, 10-90% 0.987-1.017, extremes 0.980-1.029; rank agreement (Spearman) 0.99.

The front of all runs on cpu 2: cd943ed219 0.547 at 14,081, 15dde12f04 0.557 at 13,345, dc02ceae31 0.564 at 13,161, a74b828e9b 0.607 at 13,073, af5e8dc29f 0.612 at 10,254, b06a4cf784 0.615 at 10,246, c61857fc89 0.629 at 10,034, c40ba92d5b 0.631 at 9,511, 6495dcb5dd 0.660 at 9,343, 422d6bcbca 0.685 at 9,327

The front of all runs on cpu 8: cd943ed219 0.545 at 14,081, 15dde12f04 0.560 at 13,345, dc02ceae31 0.569 at 13,161, a74b828e9b 0.602 at 13,073, b06a4cf784 0.614 at 10,246, c61857fc89 0.625 at 10,034, ca2ac63866 0.628 at 9,531, c40ba92d5b 0.634 at 9,511, 38d91795a2 0.669 at 9,474, 6495dcb5dd 0.670 at 9,343, 422d6bcbca 0.695 at 9,327

On both fronts: 9 of 10 and 11.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| cd943ed219 | 0.547 | 0.545 | 1.005 |
| 15dde12f04 | 0.557 | 0.560 | 0.996 |
| dc02ceae31 | 0.564 | 0.569 | 0.991 |
| e99da68667 | 0.582 | 0.590 | 0.987 |
| 2db525ff95 | 0.585 | 0.587 | 0.997 |
| 22b81e50c4 | 0.593 | 0.598 | 0.991 |
| 8dd8a7a146 | 0.596 | 0.608 | 0.980 |
| a74b828e9b | 0.607 | 0.602 | 1.008 |
| 9e50623ac1 | 0.610 | 0.604 | 1.010 |
| 29ad5ba726 | 0.612 | 0.608 | 1.006 |
| af5e8dc29f | 0.612 | 0.618 | 0.990 |
| b06a4cf784 | 0.615 | 0.614 | 1.002 |
| 1769ca2a48 | 0.616 | 0.609 | 1.011 |
| 4cb3fa9172 | 0.618 | 0.624 | 0.990 |
| 05617039f6 | 0.622 | 0.620 | 1.002 |
| c61857fc89 | 0.629 | 0.625 | 1.006 |
| 66eb4a8f15 | 0.629 | 0.629 | 1.001 |
| c40ba92d5b | 0.631 | 0.634 | 0.996 |
| 14f6036a4b | 0.637 | 0.632 | 1.008 |
| 5ed1ed8715 | 0.638 | 0.640 | 0.998 |
| 52b80007a1 | 0.639 | 0.636 | 1.004 |
| ca2ac63866 | 0.639 | 0.628 | 1.017 |
| 312ad2edaa | 0.643 | 0.641 | 1.003 |
| 60753a0eb0 | 0.644 | 0.639 | 1.008 |
| e0cbf09bc2 | 0.654 | 0.638 | 1.024 |
| 12d8e18511 | 0.654 | 0.648 | 1.010 |
| 0b1d16def9 | 0.656 | 0.657 | 0.998 |
| 448ef1ef43 | 0.658 | 0.670 | 0.982 |
| 6495dcb5dd | 0.660 | 0.670 | 0.985 |
| e8f1dd3ca2 | 0.667 | 0.676 | 0.987 |
| 32600cab87 | 0.668 | 0.673 | 0.994 |
| 84e302c470 | 0.670 | 0.663 | 1.010 |
| 8dc0f97f2c | 0.670 | 0.679 | 0.987 |
| 6463752a82 | 0.671 | 0.668 | 1.005 |
| 38d187239c | 0.675 | 0.659 | 1.025 |
| 57a9dcc7cb | 0.675 | 0.689 | 0.980 |
| 38d91795a2 | 0.676 | 0.669 | 1.010 |
| f4a6dd9a13 | 0.679 | 0.670 | 1.013 |
| c297551359 | 0.679 | 0.679 | 0.999 |
| f052397620 | 0.680 | 0.674 | 1.008 |
| 422d6bcbca | 0.685 | 0.695 | 0.986 |
| a285fa6ba3 | 0.687 | 0.686 | 1.001 |
| 550df563ee | 0.689 | 0.683 | 1.009 |
| 53ec9bedde | 0.693 | 0.699 | 0.990 |
| 7fe7f039bd | 0.694 | 0.686 | 1.013 |
| 595fc2b8f4 | 0.696 | 0.699 | 0.996 |
| 8cbc6dd05c | 0.697 | 0.693 | 1.006 |
| 6738aed13f | 0.700 | 0.702 | 0.997 |
| 528fc9619a | 0.703 | 0.714 | 0.985 |
| 090672993b | 0.704 | 0.709 | 0.993 |
| 05dcc81cdc | 0.705 | 0.709 | 0.994 |
| 4032a5ce71 | 0.705 | 0.709 | 0.996 |
| 9cd791dd84 | 0.709 | 0.703 | 1.009 |
| 57e0e77c09 | 0.716 | 0.715 | 1.001 |
| 3453246bdf | 0.716 | 0.718 | 0.998 |
| 4f010d8ab9 | 0.722 | 0.707 | 1.021 |
| 98736f0596 | 0.725 | 0.726 | 0.998 |
| 90018981c6 | 0.728 | 0.713 | 1.020 |
| 0ebf0445e0 | 0.730 | 0.730 | 0.999 |
| 5b70f3dd64 | 0.737 | 0.737 | 1.000 |
| c17103bf95 | 0.754 | 0.753 | 1.002 |
| a4e82e02e5 | 0.756 | 0.759 | 0.996 |
| 83cb81c383 | 0.787 | 0.773 | 1.018 |
| 672538daf5 | 0.793 | 0.771 | 1.029 |

loop is held out, and moves with an image's size mod 8 (Iteration 13).

## Session 5 - Iteration 40: seeds 1-7, after seed 7, on two CPUs

`seed 7 then experiment compare-fronts.py --rounds 10 --cpus 2,8`, commit
4f7e06cd: nine databases, 76 front designs, 10 rounds each by the median,
paired with s6 on cpu 2 and cpu 8. Eight minutes.

**Calibration 1.008.** The CPUs agree: per design median 1.000, 10-90%
0.988-1.011, ranks 0.99; 7 designs on both CPUs' fronts of 8.

**The front of all runs**: seven designs of seed 7 - 8,073 to 11,777 bytes
- and seed 6's cd943ed219, still the fastest at 0.541. Against the
fastest earlier design no larger, in this session:

| seed 7 | size | speed | the fastest earlier design no larger | seed 7 / it |
|---|---|---|---|---|
| 49b0a93f14 | 8,073 | 0.673 | none so small | - |
| 9f5e6d173c | 8,074 | 0.658 | none so small | - |
| f060a4c31f | 8,289 | 0.637 | none so small | - |
| a306cc61fb | 8,305 | 0.612 | none so small | - |
| 3c2d8a577b | 8,306 | 0.600 | none so small | - |
| 4cc12fc1e7 | 8,957 | 0.570 | none so small | - |
| 3a7c3d6e90 | 11,777 | 0.550 | af5e8dc29f 0.610 at 10,254 | 0.902 |

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 1.008** (kernel 1.017, fib 0.991, parse 1.002, corpus 1.023, loop 0.992).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 49b0a93f14 | 0.673 | 0.688 | 8,073 | 8,073 | 0.671 | 0.890 | 0.544 | 0.632 | 0.709 | yes |
| this clone: db.jsonl | 9f5e6d173c | 0.658 | 0.650 | 8,074 | 8,074 | 0.660 | 0.891 | 0.524 | 0.609 | 0.793 | yes |
| this clone: db.jsonl | f060a4c31f | 0.637 | 0.637 | 8,289 | 8,289 | 0.642 | 0.827 | 0.521 | 0.597 | 0.882 | yes |
| this clone: db.jsonl | a306cc61fb | 0.612 | 0.615 | 8,305 | 8,305 | 0.652 | 0.662 | 0.554 | 0.588 | 0.967 | yes |
| this clone: db.jsonl | 3c2d8a577b | 0.600 | 0.603 | 8,306 | 8,306 | 0.667 | 0.631 | 0.527 | 0.583 | 0.883 | yes |
| this clone: db.jsonl | 4cc12fc1e7 | 0.570 | 0.561 | 8,957 | 8,957 | 0.624 | 0.561 | 0.507 | 0.593 | 0.942 | yes |
| this clone: db.jsonl | 3a7c3d6e90 | 0.550 | 0.551 | 11,777 | 11,777 | 0.593 | 0.824 | 0.360 | 0.520 | 0.846 | yes |
| this clone: db.jsonl | 2b00aa6e97 | 0.555 | 0.568 | 12,145 | 12,145 | 0.616 | 0.819 | 0.361 | 0.520 | 0.820 |  |
| this clone: db.jsonl | 27a35df3fa | 0.558 | 0.570 | 12,312 | 12,312 | 0.620 | 0.581 | 0.489 | 0.552 | 0.924 |  |
| this clone: db.jsonl | ff39b37bcc | 0.563 | 0.572 | 12,584 | 12,584 | 0.632 | 0.630 | 0.457 | 0.552 | 0.973 |  |
| this clone: db.jsonl | 1cf03a8fd4 | 0.550 | 0.545 | 12,608 | 12,608 | 0.587 | 0.689 | 0.408 | 0.553 | 0.876 |  |
| this clone: db.jsonl | a214fa731c | 0.557 | 0.557 | 12,664 | 12,664 | 0.632 | 0.624 | 0.446 | 0.548 | 0.790 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 595fc2b8f4 | 0.702 | 0.784 | 9,662 | 9,761 | 0.758 | 0.726 | 0.649 | 0.682 | 1.051 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 8cbc6dd05c | 0.695 | 0.742 | 9,694 | 9,809 | 0.750 | 0.796 | 0.612 | 0.638 | 0.826 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 6738aed13f | 0.696 | 0.755 | 9,694 | 9,793 | 0.745 | 0.706 | 0.630 | 0.707 | 1.082 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 312ad2edaa | 0.643 | 0.716 | 13,344 | 13,456 | 0.688 | 0.740 | 0.556 | 0.605 | 0.887 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 05617039f6 | 0.619 | 0.674 | 13,352 | 13,488 | 0.657 | 0.798 | 0.472 | 0.594 | 0.695 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 0b1d16def9 | 0.651 | 0.705 | 13,352 | 13,464 | 0.693 | 0.810 | 0.510 | 0.627 | 0.801 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 57a9dcc7cb | 0.682 | 0.680 | 13,368 | 13,480 | 0.721 | 0.880 | 0.546 | 0.626 | 0.960 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 32600cab87 | 0.666 | 0.662 | 13,528 | 13,656 | 0.671 | 0.933 | 0.511 | 0.614 | 0.701 |  |
| archived-20261004-200423: db-seed1.jsonl | 83cb81c383 | 0.794 | 0.705 | 9,662 | 9,761 | 0.771 | 1.010 | 0.698 | 0.731 | 1.068 |  |
| archived-20261004-200423: db-seed1.jsonl | 5b70f3dd64 | 0.736 | 0.649 | 9,694 | 9,801 | 0.740 | 0.919 | 0.626 | 0.689 | 0.882 |  |
| archived-20261004-200423: db-seed1.jsonl | a4e82e02e5 | 0.764 | 0.654 | 9,694 | 9,809 | 0.782 | 0.879 | 0.668 | 0.743 | 0.960 |  |
| archived-20261004-200423: db-seed1.jsonl | 53ec9bedde | 0.704 | 0.670 | 13,336 | 13,464 | 0.732 | 0.818 | 0.614 | 0.669 | 0.855 |  |
| archived-20261004-200423: db-seed1.jsonl | 448ef1ef43 | 0.655 | 0.620 | 13,368 | 13,488 | 0.676 | 0.949 | 0.494 | 0.581 | 0.790 |  |
| archived-20261004-200423: db-seed1.jsonl | 38d187239c | 0.669 | 0.609 | 13,368 | 13,480 | 0.710 | 0.853 | 0.542 | 0.612 | 0.775 |  |
| archived-20261004-200423: db-seed2.jsonl | 0ebf0445e0 | 0.723 | 0.667 | 9,662 | 9,761 | 0.770 | 0.717 | 0.684 | 0.723 | 0.973 |  |
| archived-20261004-200423: db-seed2.jsonl | c17103bf95 | 0.747 | 0.725 | 9,662 | 9,769 | 0.784 | 0.740 | 0.715 | 0.749 | 0.901 |  |
| archived-20261004-200423: db-seed2.jsonl | a285fa6ba3 | 0.693 | 0.666 | 13,352 | 13,464 | 0.752 | 0.697 | 0.633 | 0.696 | 0.934 |  |
| archived-20261004-200423: db-seed2.jsonl | 57e0e77c09 | 0.726 | 0.657 | 13,352 | 13,480 | 0.742 | 1.047 | 0.546 | 0.656 | 0.941 |  |
| archived-20261004-200423: db-seed2.jsonl | 9cd791dd84 | 0.696 | 0.619 | 13,368 | 13,472 | 0.737 | 0.871 | 0.566 | 0.646 | 0.993 |  |
| archived-20261004-200423: db.jsonl | 550df563ee | 0.697 | 0.696 | 9,646 | 9,745 | 0.734 | 0.781 | 0.623 | 0.663 | 0.959 |  |
| archived-20261004-200423: db.jsonl | f4a6dd9a13 | 0.674 | 0.683 | 9,662 | 9,761 | 0.734 | 0.661 | 0.614 | 0.691 | 0.983 |  |
| archived-20261004-200423: db.jsonl | 60753a0eb0 | 0.636 | 0.622 | 9,686 | 9,785 | 0.660 | 0.672 | 0.571 | 0.648 | 0.888 |  |
| archived-20261004-200423: db.jsonl | 8dd8a7a146 | 0.608 | 0.595 | 13,352 | 13,464 | 0.631 | 0.692 | 0.521 | 0.602 | 0.835 |  |
| archived-20261004-214724: db.jsonl | 3453246bdf | 0.715 | 0.727 | 9,335 | 9,335 | 0.748 | 0.702 | 0.679 | 0.733 | 0.919 |  |
| archived-20261004-214724: db.jsonl | 672538daf5 | 0.799 | 0.780 | 9,351 | 9,351 | 0.824 | 0.830 | 0.736 | 0.810 | 0.994 |  |
| archived-20261004-214724: db.jsonl | 7fe7f039bd | 0.687 | 0.702 | 9,450 | 9,450 | 0.738 | 0.712 | 0.621 | 0.682 | 0.853 |  |
| archived-20261004-214724: db.jsonl | 38d91795a2 | 0.671 | 0.678 | 9,474 | 9,474 | 0.730 | 0.639 | 0.624 | 0.697 | 0.842 |  |
| archived-20261004-214724: db.jsonl | 6463752a82 | 0.660 | 0.669 | 9,523 | 9,523 | 0.704 | 0.724 | 0.584 | 0.637 | 0.871 |  |
| archived-20261004-214724: db.jsonl | 90018981c6 | 0.724 | 0.696 | 9,678 | 9,678 | 0.730 | 0.807 | 0.649 | 0.718 | 1.021 |  |
| archived-20261004-214724: db.jsonl | e0cbf09bc2 | 0.647 | 0.666 | 13,057 | 13,057 | 0.679 | 0.776 | 0.519 | 0.641 | 0.958 |  |
| archived-20261004-214724: db.jsonl | 1769ca2a48 | 0.612 | 0.603 | 13,209 | 13,209 | 0.670 | 0.633 | 0.531 | 0.623 | 0.859 |  |
| archived-20261004-214724: db.jsonl | 14f6036a4b | 0.625 | 0.627 | 13,217 | 13,217 | 0.680 | 0.836 | 0.470 | 0.572 | 0.928 |  |
| archived-20261004-214724: db.jsonl | 29ad5ba726 | 0.608 | 0.589 | 13,352 | 13,352 | 0.661 | 0.749 | 0.491 | 0.561 | 0.773 |  |
| archived-20261004-214724: db.jsonl | 12d8e18511 | 0.658 | 0.667 | 13,360 | 13,360 | 0.688 | 0.868 | 0.523 | 0.601 | 0.923 |  |
| archived-20261005-013645: db.jsonl | 05dcc81cdc | 0.705 | 0.688 | 9,335 | 9,335 | 0.719 | 0.815 | 0.614 | 0.688 | 0.919 |  |
| archived-20261005-013645: db.jsonl | c297551359 | 0.666 | 0.682 | 9,450 | 9,450 | 0.710 | 0.662 | 0.628 | 0.667 | 0.812 |  |
| archived-20261005-013645: db.jsonl | e8f1dd3ca2 | 0.670 | 0.678 | 9,458 | 9,458 | 0.690 | 0.813 | 0.574 | 0.627 | 0.971 |  |
| archived-20261005-013645: db.jsonl | 66eb4a8f15 | 0.634 | 0.641 | 13,057 | 13,057 | 0.691 | 0.713 | 0.533 | 0.616 | 0.911 |  |
| archived-20261005-013645: db.jsonl | 84e302c470 | 0.658 | 0.657 | 13,065 | 13,065 | 0.722 | 0.737 | 0.552 | 0.638 | 1.014 |  |
| archived-20261005-013645: db.jsonl | 4cb3fa9172 | 0.625 | 0.626 | 13,073 | 13,073 | 0.647 | 0.811 | 0.487 | 0.595 | 0.951 |  |
| archived-20261005-013645: db.jsonl | e99da68667 | 0.591 | 0.581 | 13,201 | 13,201 | 0.636 | 0.766 | 0.453 | 0.555 | 0.986 |  |
| archived-20261005-042924: db.jsonl | 98736f0596 | 0.736 | 0.731 | 9,335 | 9,335 | 0.793 | 0.769 | 0.660 | 0.730 | 1.023 |  |
| archived-20261005-042924: db.jsonl | 4f010d8ab9 | 0.719 | 0.721 | 9,343 | 9,343 | 0.791 | 0.733 | 0.652 | 0.709 | 0.998 |  |
| archived-20261005-042924: db.jsonl | 4032a5ce71 | 0.719 | 0.698 | 9,351 | 9,351 | 0.781 | 0.811 | 0.604 | 0.696 | 0.964 |  |
| archived-20261005-042924: db.jsonl | 528fc9619a | 0.702 | 0.702 | 9,359 | 9,359 | 0.764 | 0.759 | 0.612 | 0.685 | 0.965 |  |
| archived-20261005-042924: db.jsonl | f052397620 | 0.684 | 0.685 | 9,450 | 9,450 | 0.735 | 0.797 | 0.572 | 0.652 | 0.891 |  |
| archived-20261005-042924: db.jsonl | 8dc0f97f2c | 0.683 | 0.680 | 9,458 | 9,458 | 0.724 | 0.763 | 0.585 | 0.673 | 0.903 |  |
| archived-20261005-042924: db.jsonl | 52b80007a1 | 0.659 | 0.640 | 10,010 | 10,010 | 0.740 | 0.569 | 0.625 | 0.715 | 0.984 |  |
| archived-20261005-042924: db.jsonl | 5ed1ed8715 | 0.647 | 0.642 | 10,018 | 10,018 | 0.735 | 0.580 | 0.618 | 0.665 | 0.996 |  |
| archived-20261005-042924: db.jsonl | 9e50623ac1 | 0.607 | 0.593 | 13,073 | 13,073 | 0.668 | 0.730 | 0.489 | 0.569 | 0.907 |  |
| archived-20261005-042924: db.jsonl | 22b81e50c4 | 0.608 | 0.605 | 13,209 | 13,209 | 0.644 | 0.897 | 0.429 | 0.550 | 0.936 |  |
| archived-20261005-042924: db.jsonl | 2db525ff95 | 0.594 | 0.579 | 14,017 | 14,017 | 0.653 | 0.715 | 0.447 | 0.595 | 0.949 |  |
| archived-20261005-131253: db.jsonl | 422d6bcbca | 0.682 | 0.699 | 9,327 | 9,327 | 0.709 | 0.856 | 0.544 | 0.656 | 0.945 |  |
| archived-20261005-131253: db.jsonl | 090672993b | 0.701 | 0.700 | 9,335 | 9,335 | 0.684 | 0.804 | 0.640 | 0.685 | 0.860 |  |
| archived-20261005-131253: db.jsonl | 6495dcb5dd | 0.671 | 0.662 | 9,343 | 9,343 | 0.681 | 0.906 | 0.529 | 0.621 | 0.787 |  |
| archived-20261005-131253: db.jsonl | c40ba92d5b | 0.635 | 0.630 | 9,511 | 9,511 | 0.657 | 0.688 | 0.569 | 0.631 | 0.792 |  |
| archived-20261005-131253: db.jsonl | ca2ac63866 | 0.637 | 0.634 | 9,531 | 9,531 | 0.658 | 0.730 | 0.565 | 0.606 | 0.886 |  |
| archived-20261005-131253: db.jsonl | c61857fc89 | 0.633 | 0.633 | 10,034 | 10,034 | 0.656 | 0.724 | 0.539 | 0.626 | 0.707 |  |
| archived-20261005-131253: db.jsonl | b06a4cf784 | 0.619 | 0.615 | 10,246 | 10,246 | 0.645 | 0.712 | 0.539 | 0.592 | 0.869 |  |
| archived-20261005-131253: db.jsonl | af5e8dc29f | 0.610 | 0.604 | 10,254 | 10,254 | 0.638 | 0.679 | 0.540 | 0.592 | 0.891 |  |
| archived-20261005-131253: db.jsonl | a74b828e9b | 0.600 | 0.608 | 13,073 | 13,073 | 0.680 | 0.631 | 0.509 | 0.595 | 0.949 |  |
| archived-20261005-131253: db.jsonl | dc02ceae31 | 0.563 | 0.560 | 13,161 | 13,161 | 0.598 | 0.707 | 0.442 | 0.536 | 0.771 |  |
| archived-20261005-131253: db.jsonl | 15dde12f04 | 0.569 | 0.567 | 13,345 | 13,345 | 0.606 | 0.806 | 0.405 | 0.531 | 0.763 |  |
| archived-20261005-131253: db.jsonl | cd943ed219 | 0.541 | 0.545 | 14,081 | 14,081 | 0.586 | 0.692 | 0.404 | 0.524 | 0.789 | yes |

The front of all runs together, by size: cd943ed219 0.541 at 14,081, 3a7c3d6e90 0.550 at 11,777, 4cc12fc1e7 0.570 at 8,957, 3c2d8a577b 0.600 at 8,306, a306cc61fb 0.612 at 8,305, f060a4c31f 0.637 at 8,289, 9f5e6d173c 0.658 at 8,074, 49b0a93f14 0.673 at 8,073

## The same session on two CPUs

Calibration on cpu 2: 1.008; on cpu 8: 1.006.

Speed on cpu 2 over speed on cpu 8, per design: median 1.000, 10-90% 0.988-1.011, extremes 0.978-1.033; rank agreement (Spearman) 0.99.

The front of all runs on cpu 2: cd943ed219 0.541 at 14,081, 3a7c3d6e90 0.550 at 11,777, 4cc12fc1e7 0.570 at 8,957, 3c2d8a577b 0.600 at 8,306, a306cc61fb 0.612 at 8,305, f060a4c31f 0.637 at 8,289, 9f5e6d173c 0.658 at 8,074, 49b0a93f14 0.673 at 8,073

The front of all runs on cpu 8: 1cf03a8fd4 0.535 at 12,608, 3a7c3d6e90 0.554 at 11,777, 4cc12fc1e7 0.570 at 8,957, 3c2d8a577b 0.603 at 8,306, a306cc61fb 0.617 at 8,305, f060a4c31f 0.639 at 8,289, 9f5e6d173c 0.651 at 8,074, 49b0a93f14 0.681 at 8,073

On both fronts: 7 of 8 and 8.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| cd943ed219 | 0.541 | 0.543 | 0.996 |
| 3a7c3d6e90 | 0.550 | 0.554 | 0.993 |
| 1cf03a8fd4 | 0.550 | 0.535 | 1.028 |
| 2b00aa6e97 | 0.555 | 0.554 | 1.002 |
| a214fa731c | 0.557 | 0.561 | 0.994 |
| 27a35df3fa | 0.558 | 0.556 | 1.005 |
| dc02ceae31 | 0.563 | 0.568 | 0.990 |
| ff39b37bcc | 0.563 | 0.560 | 1.006 |
| 15dde12f04 | 0.569 | 0.561 | 1.014 |
| 4cc12fc1e7 | 0.570 | 0.570 | 0.999 |
| e99da68667 | 0.591 | 0.586 | 1.009 |
| 2db525ff95 | 0.594 | 0.589 | 1.008 |
| 3c2d8a577b | 0.600 | 0.603 | 0.995 |
| a74b828e9b | 0.600 | 0.599 | 1.002 |
| 9e50623ac1 | 0.607 | 0.608 | 0.998 |
| 22b81e50c4 | 0.608 | 0.602 | 1.009 |
| 29ad5ba726 | 0.608 | 0.620 | 0.981 |
| 8dd8a7a146 | 0.608 | 0.589 | 1.033 |
| af5e8dc29f | 0.610 | 0.624 | 0.978 |
| 1769ca2a48 | 0.612 | 0.617 | 0.992 |
| a306cc61fb | 0.612 | 0.617 | 0.993 |
| b06a4cf784 | 0.619 | 0.620 | 0.999 |
| 05617039f6 | 0.619 | 0.613 | 1.010 |
| 4cb3fa9172 | 0.625 | 0.625 | 1.000 |
| 14f6036a4b | 0.625 | 0.623 | 1.003 |
| c61857fc89 | 0.633 | 0.621 | 1.020 |
| 66eb4a8f15 | 0.634 | 0.637 | 0.995 |
| c40ba92d5b | 0.635 | 0.638 | 0.994 |
| 60753a0eb0 | 0.636 | 0.641 | 0.992 |
| ca2ac63866 | 0.637 | 0.635 | 1.003 |
| f060a4c31f | 0.637 | 0.639 | 0.997 |
| 312ad2edaa | 0.643 | 0.642 | 1.002 |
| 5ed1ed8715 | 0.647 | 0.643 | 1.005 |
| e0cbf09bc2 | 0.647 | 0.643 | 1.007 |
| 0b1d16def9 | 0.651 | 0.659 | 0.988 |
| 448ef1ef43 | 0.655 | 0.657 | 0.998 |
| 84e302c470 | 0.658 | 0.665 | 0.989 |
| 9f5e6d173c | 0.658 | 0.651 | 1.010 |
| 12d8e18511 | 0.658 | 0.657 | 1.002 |
| 52b80007a1 | 0.659 | 0.647 | 1.018 |
| 6463752a82 | 0.660 | 0.660 | 0.999 |
| 32600cab87 | 0.666 | 0.673 | 0.990 |
| c297551359 | 0.666 | 0.680 | 0.980 |
| 38d187239c | 0.669 | 0.668 | 1.002 |
| e8f1dd3ca2 | 0.670 | 0.682 | 0.983 |
| 6495dcb5dd | 0.671 | 0.668 | 1.004 |
| 38d91795a2 | 0.671 | 0.679 | 0.988 |
| 49b0a93f14 | 0.673 | 0.681 | 0.989 |
| f4a6dd9a13 | 0.674 | 0.677 | 0.995 |
| 422d6bcbca | 0.682 | 0.680 | 1.003 |
| 57a9dcc7cb | 0.682 | 0.686 | 0.994 |
| 8dc0f97f2c | 0.683 | 0.683 | 0.999 |
| f052397620 | 0.684 | 0.690 | 0.991 |
| 7fe7f039bd | 0.687 | 0.690 | 0.996 |
| a285fa6ba3 | 0.693 | 0.687 | 1.009 |
| 8cbc6dd05c | 0.695 | 0.697 | 0.997 |
| 6738aed13f | 0.696 | 0.708 | 0.983 |
| 9cd791dd84 | 0.696 | 0.706 | 0.985 |
| 550df563ee | 0.697 | 0.702 | 0.994 |
| 090672993b | 0.701 | 0.697 | 1.005 |
| 595fc2b8f4 | 0.702 | 0.695 | 1.010 |
| 528fc9619a | 0.702 | 0.700 | 1.004 |
| 53ec9bedde | 0.704 | 0.704 | 1.000 |
| 05dcc81cdc | 0.705 | 0.709 | 0.995 |
| 3453246bdf | 0.715 | 0.713 | 1.003 |
| 4032a5ce71 | 0.719 | 0.720 | 0.999 |
| 4f010d8ab9 | 0.719 | 0.712 | 1.010 |
| 0ebf0445e0 | 0.723 | 0.731 | 0.989 |
| 90018981c6 | 0.724 | 0.723 | 1.001 |
| 57e0e77c09 | 0.726 | 0.718 | 1.011 |
| 5b70f3dd64 | 0.736 | 0.735 | 1.001 |
| 98736f0596 | 0.736 | 0.729 | 1.010 |
| c17103bf95 | 0.747 | 0.749 | 0.997 |
| a4e82e02e5 | 0.764 | 0.754 | 1.014 |
| 83cb81c383 | 0.794 | 0.778 | 1.020 |
| 672538daf5 | 0.799 | 0.798 | 1.002 |

loop is held out, and moves with an image's size mod 8 (Iteration 13).

## Session 6 - Iteration 42: seeds 1-8, after seed 8, over five workloads

`seed 8 then experiment compare-fronts.py --rounds 10 --cpus 2,8`, commit
467dc55f: ten databases, 98 front designs, 10 rounds each by the median,
paired with s6 on cpu 2 and cpu 8. Speed now over kernel, fib, parse,
corpus and loop; sieve held out. Eleven and a half minutes. (The report's
column header still listed the old five workloads - the rows are right,
the last workload column is sieve; compare-fronts.py builds the header
from the lists since.)

**Calibration 1.003** (sieve 1.007). The CPUs agree: per design median
1.004, 10-90% 0.991-1.018, ranks 0.99; 14 designs on both CPUs' fronts.

**The front of all runs**: 14 designs of seed 8, and seed 7's three
smallest (49b0a93f14, 9f5e6d173c, 3c2d8a577b). Against the fastest earlier
design no larger, in this session:

| seed 8 | size | speed | loop | sieve (held out) | the fastest earlier design no larger | seed 8 / it |
|---|---|---|---|---|---|---|
| f41ab1810d | 8,034 | 1.005 | 1.076 | 1.151 | none so small | - |
| 3781c5e756 | 8,041 | 0.757 | 0.833 | 0.851 | none so small | - |
| d4739aac88 | 8,042 | 0.719 | 0.731 | 0.867 | none so small | - |
| 8a2189b3b6 | 8,171 | 0.661 | 0.768 | 0.829 | 9f5e6d173c 0.686 at 8,074 | 0.964 |
| be02a4c0cf | 8,525 | 0.550 | 0.190 | 0.586 | 3c2d8a577b 0.650 at 8,306 | 0.846 |
| caf4358de8 | 8,540 | 0.529 | 0.182 | 0.617 | 3c2d8a577b 0.650 at 8,306 | 0.814 |
| 3d31fd4cc4 | 8,550 | 0.522 | 0.199 | 0.659 | 3c2d8a577b 0.650 at 8,306 | 0.803 |
| 85cac726b5 | 8,614 | 0.505 | 0.184 | 0.597 | 3c2d8a577b 0.650 at 8,306 | 0.777 |
| f85a63f8c7 | 8,647 | 0.503 | 0.189 | 0.612 | 3c2d8a577b 0.650 at 8,306 | 0.774 |
| 1b602bc9bd | 8,671 | 0.490 | 0.185 | 0.586 | 3c2d8a577b 0.650 at 8,306 | 0.754 |
| 72ca2cf497 | 8,990 | 0.480 | 0.197 | 0.542 | 4cc12fc1e7 0.623 at 8,957 | 0.770 |
| 959e88b0f5 | 9,140 | 0.462 | 0.185 | 0.530 | 4cc12fc1e7 0.623 at 8,957 | 0.742 |
| 577c999e62 | 9,278 | 0.454 | 0.179 | 0.512 | 4cc12fc1e7 0.623 at 8,957 | 0.729 |
| 9bb527944a | 13,073 | 0.449 | 0.191 | 0.556 | 3a7c3d6e90 0.599 at 11,777 | 0.750 |

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 1.003** (kernel 1.010, fib 0.997, parse 1.004, corpus 1.008, loop 0.997, sieve 1.007).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | f41ab1810d | 1.005 | 1.008 | 8,034 | 8,034 | 1.002 | 1.258 | 0.808 | 0.934 | 1.076 | 1.151 | yes |
| this clone: db.jsonl | 3781c5e756 | 0.757 | 0.758 | 8,041 | 8,041 | 0.751 | 0.978 | 0.597 | 0.680 | 0.833 | 0.851 | yes |
| this clone: db.jsonl | d4739aac88 | 0.719 | 0.723 | 8,042 | 8,042 | 0.774 | 0.729 | 0.646 | 0.723 | 0.731 | 0.867 | yes |
| this clone: db.jsonl | e05adba602 | 0.695 | 0.687 | 8,082 | 8,082 | 0.710 | 0.778 | 0.552 | 0.653 | 0.812 | 0.791 |  |
| this clone: db.jsonl | bb8a0cb575 | 0.698 | 0.688 | 8,099 | 8,099 | 0.747 | 0.765 | 0.567 | 0.671 | 0.762 | 0.838 |  |
| this clone: db.jsonl | a27aa49d8e | 0.693 | 0.693 | 8,163 | 8,163 | 0.676 | 0.842 | 0.520 | 0.615 | 0.874 | 0.843 |  |
| this clone: db.jsonl | 8a2189b3b6 | 0.661 | 0.646 | 8,171 | 8,171 | 0.672 | 0.761 | 0.525 | 0.611 | 0.768 | 0.829 | yes |
| this clone: db.jsonl | f66d74a27c | 0.690 | 0.682 | 8,210 | 8,210 | 0.693 | 0.882 | 0.517 | 0.626 | 0.789 | 0.827 |  |
| this clone: db.jsonl | be02a4c0cf | 0.550 | 0.533 | 8,525 | 8,525 | 0.763 | 0.774 | 0.613 | 0.729 | 0.190 | 0.586 | yes |
| this clone: db.jsonl | caf4358de8 | 0.529 | 0.514 | 8,540 | 8,540 | 0.750 | 0.756 | 0.585 | 0.690 | 0.182 | 0.617 | yes |
| this clone: db.jsonl | 6578fc6928 | 0.530 | 0.515 | 8,548 | 8,548 | 0.698 | 0.769 | 0.530 | 0.639 | 0.230 | 0.601 |  |
| this clone: db.jsonl | 3d31fd4cc4 | 0.522 | 0.502 | 8,550 | 8,550 | 0.683 | 0.865 | 0.521 | 0.633 | 0.199 | 0.659 | yes |
| this clone: db.jsonl | 85cac726b5 | 0.505 | 0.484 | 8,614 | 8,614 | 0.635 | 0.865 | 0.524 | 0.618 | 0.184 | 0.597 | yes |
| this clone: db.jsonl | f85a63f8c7 | 0.503 | 0.481 | 8,647 | 8,647 | 0.638 | 0.862 | 0.531 | 0.585 | 0.189 | 0.612 | yes |
| this clone: db.jsonl | 51879a71f0 | 0.512 | 0.513 | 8,664 | 8,664 | 0.679 | 0.750 | 0.564 | 0.623 | 0.197 | 0.653 |  |
| this clone: db.jsonl | 1b602bc9bd | 0.490 | 0.478 | 8,671 | 8,671 | 0.670 | 0.792 | 0.495 | 0.584 | 0.185 | 0.586 | yes |
| this clone: db.jsonl | 72ca2cf497 | 0.480 | 0.469 | 8,990 | 8,990 | 0.651 | 0.677 | 0.506 | 0.580 | 0.197 | 0.542 | yes |
| this clone: db.jsonl | 959e88b0f5 | 0.462 | 0.458 | 9,140 | 9,140 | 0.676 | 0.537 | 0.518 | 0.607 | 0.185 | 0.530 | yes |
| this clone: db.jsonl | 577c999e62 | 0.454 | 0.443 | 9,278 | 9,278 | 0.651 | 0.549 | 0.504 | 0.594 | 0.179 | 0.512 | yes |
| this clone: db.jsonl | aba06380d6 | 0.483 | 0.462 | 12,353 | 12,353 | 0.657 | 0.777 | 0.487 | 0.585 | 0.182 | 0.611 |  |
| this clone: db.jsonl | 0212f86508 | 0.468 | 0.453 | 12,377 | 12,377 | 0.637 | 0.795 | 0.443 | 0.553 | 0.180 | 0.623 |  |
| this clone: db.jsonl | 9bb527944a | 0.449 | 0.430 | 13,073 | 13,073 | 0.659 | 0.557 | 0.436 | 0.597 | 0.191 | 0.556 | yes |
| archived-20261004-200423: db-rehearsal.jsonl | 595fc2b8f4 | 0.761 | 0.784 | 9,662 | 9,761 | 0.738 | 0.727 | 0.634 | 0.704 | 1.068 | 0.851 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 8cbc6dd05c | 0.722 | 0.742 | 9,694 | 9,809 | 0.725 | 0.790 | 0.605 | 0.662 | 0.852 | 0.792 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 6738aed13f | 0.756 | 0.755 | 9,694 | 9,793 | 0.765 | 0.690 | 0.629 | 0.698 | 1.062 | 0.847 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 312ad2edaa | 0.685 | 0.716 | 13,344 | 13,456 | 0.677 | 0.722 | 0.559 | 0.618 | 0.894 | 0.851 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 05617039f6 | 0.640 | 0.674 | 13,352 | 13,488 | 0.671 | 0.790 | 0.480 | 0.590 | 0.713 | 0.799 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 0b1d16def9 | 0.678 | 0.705 | 13,352 | 13,464 | 0.700 | 0.815 | 0.505 | 0.616 | 0.805 | 0.837 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 57a9dcc7cb | 0.736 | 0.680 | 13,368 | 13,480 | 0.710 | 0.910 | 0.536 | 0.641 | 0.970 | 0.876 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 32600cab87 | 0.672 | 0.662 | 13,528 | 13,656 | 0.658 | 0.972 | 0.508 | 0.603 | 0.703 | 0.857 |  |
| archived-20261004-200423: db-seed1.jsonl | 83cb81c383 | 0.845 | 0.705 | 9,662 | 9,761 | 0.783 | 0.999 | 0.689 | 0.751 | 1.063 | 0.910 |  |
| archived-20261004-200423: db-seed1.jsonl | 5b70f3dd64 | 0.766 | 0.649 | 9,694 | 9,801 | 0.739 | 0.949 | 0.629 | 0.678 | 0.881 | 0.814 |  |
| archived-20261004-200423: db-seed1.jsonl | a4e82e02e5 | 0.806 | 0.654 | 9,694 | 9,809 | 0.795 | 0.888 | 0.662 | 0.738 | 0.987 | 0.882 |  |
| archived-20261004-200423: db-seed1.jsonl | 53ec9bedde | 0.733 | 0.670 | 13,336 | 13,464 | 0.749 | 0.776 | 0.620 | 0.674 | 0.872 | 0.853 |  |
| archived-20261004-200423: db-seed1.jsonl | 448ef1ef43 | 0.681 | 0.620 | 13,368 | 13,488 | 0.643 | 0.955 | 0.500 | 0.589 | 0.812 | 0.823 |  |
| archived-20261004-200423: db-seed1.jsonl | 38d187239c | 0.694 | 0.609 | 13,368 | 13,480 | 0.717 | 0.836 | 0.544 | 0.627 | 0.789 | 0.809 |  |
| archived-20261004-200423: db-seed2.jsonl | 0ebf0445e0 | 0.773 | 0.667 | 9,662 | 9,761 | 0.774 | 0.704 | 0.690 | 0.764 | 0.964 | 0.863 |  |
| archived-20261004-200423: db-seed2.jsonl | c17103bf95 | 0.777 | 0.725 | 9,662 | 9,769 | 0.794 | 0.759 | 0.704 | 0.738 | 0.907 | 0.840 |  |
| archived-20261004-200423: db-seed2.jsonl | a285fa6ba3 | 0.736 | 0.666 | 13,352 | 13,464 | 0.753 | 0.706 | 0.629 | 0.693 | 0.930 | 0.879 |  |
| archived-20261004-200423: db-seed2.jsonl | 57e0e77c09 | 0.751 | 0.657 | 13,352 | 13,480 | 0.716 | 1.044 | 0.552 | 0.625 | 0.925 | 0.881 |  |
| archived-20261004-200423: db-seed2.jsonl | 9cd791dd84 | 0.756 | 0.619 | 13,368 | 13,472 | 0.737 | 0.892 | 0.573 | 0.653 | 1.002 | 0.883 |  |
| archived-20261004-200423: db.jsonl | 550df563ee | 0.749 | 0.696 | 9,646 | 9,745 | 0.713 | 0.774 | 0.626 | 0.695 | 0.983 | 0.828 |  |
| archived-20261004-200423: db.jsonl | f4a6dd9a13 | 0.723 | 0.683 | 9,662 | 9,761 | 0.721 | 0.669 | 0.616 | 0.678 | 0.982 | 0.765 |  |
| archived-20261004-200423: db.jsonl | 60753a0eb0 | 0.691 | 0.622 | 9,686 | 9,785 | 0.704 | 0.664 | 0.573 | 0.652 | 0.899 | 0.759 |  |
| archived-20261004-200423: db.jsonl | 8dd8a7a146 | 0.638 | 0.595 | 13,352 | 13,464 | 0.636 | 0.658 | 0.505 | 0.586 | 0.853 | 0.807 |  |
| archived-20261004-214724: db.jsonl | 3453246bdf | 0.750 | 0.727 | 9,335 | 9,335 | 0.757 | 0.686 | 0.677 | 0.738 | 0.917 | 0.810 |  |
| archived-20261004-214724: db.jsonl | 672538daf5 | 0.824 | 0.780 | 9,351 | 9,351 | 0.806 | 0.826 | 0.709 | 0.788 | 1.018 | 0.855 |  |
| archived-20261004-214724: db.jsonl | 7fe7f039bd | 0.721 | 0.702 | 9,450 | 9,450 | 0.766 | 0.698 | 0.626 | 0.704 | 0.826 | 0.838 |  |
| archived-20261004-214724: db.jsonl | 38d91795a2 | 0.704 | 0.678 | 9,474 | 9,474 | 0.738 | 0.647 | 0.616 | 0.692 | 0.847 | 0.858 |  |
| archived-20261004-214724: db.jsonl | 6463752a82 | 0.706 | 0.669 | 9,523 | 9,523 | 0.718 | 0.712 | 0.576 | 0.676 | 0.880 | 0.842 |  |
| archived-20261004-214724: db.jsonl | 90018981c6 | 0.775 | 0.696 | 9,678 | 9,678 | 0.730 | 0.797 | 0.667 | 0.720 | 1.001 | 0.896 |  |
| archived-20261004-214724: db.jsonl | e0cbf09bc2 | 0.690 | 0.666 | 13,057 | 13,057 | 0.682 | 0.747 | 0.528 | 0.615 | 0.948 | 0.885 |  |
| archived-20261004-214724: db.jsonl | 1769ca2a48 | 0.660 | 0.603 | 13,209 | 13,209 | 0.707 | 0.623 | 0.524 | 0.633 | 0.858 | 0.846 |  |
| archived-20261004-214724: db.jsonl | 14f6036a4b | 0.683 | 0.627 | 13,217 | 13,217 | 0.679 | 0.829 | 0.479 | 0.584 | 0.943 | 0.893 |  |
| archived-20261004-214724: db.jsonl | 29ad5ba726 | 0.637 | 0.589 | 13,352 | 13,352 | 0.651 | 0.762 | 0.487 | 0.554 | 0.786 | 0.818 |  |
| archived-20261004-214724: db.jsonl | 12d8e18511 | 0.703 | 0.667 | 13,360 | 13,360 | 0.688 | 0.842 | 0.531 | 0.608 | 0.916 | 0.936 |  |
| archived-20261005-013645: db.jsonl | 05dcc81cdc | 0.743 | 0.688 | 9,335 | 9,335 | 0.738 | 0.810 | 0.603 | 0.692 | 0.910 | 0.887 |  |
| archived-20261005-013645: db.jsonl | c297551359 | 0.703 | 0.682 | 9,450 | 9,450 | 0.733 | 0.659 | 0.625 | 0.690 | 0.821 | 0.868 |  |
| archived-20261005-013645: db.jsonl | e8f1dd3ca2 | 0.732 | 0.678 | 9,458 | 9,458 | 0.692 | 0.823 | 0.578 | 0.663 | 0.962 | 0.902 |  |
| archived-20261005-013645: db.jsonl | 66eb4a8f15 | 0.680 | 0.641 | 13,057 | 13,057 | 0.717 | 0.691 | 0.532 | 0.611 | 0.904 | 0.861 |  |
| archived-20261005-013645: db.jsonl | 84e302c470 | 0.723 | 0.657 | 13,065 | 13,065 | 0.726 | 0.761 | 0.551 | 0.644 | 1.005 | 0.883 |  |
| archived-20261005-013645: db.jsonl | 4cb3fa9172 | 0.691 | 0.626 | 13,073 | 13,073 | 0.670 | 0.810 | 0.503 | 0.602 | 0.959 | 0.879 |  |
| archived-20261005-013645: db.jsonl | e99da68667 | 0.649 | 0.581 | 13,201 | 13,201 | 0.600 | 0.766 | 0.453 | 0.554 | 0.996 | 0.863 |  |
| archived-20261005-042924: db.jsonl | 98736f0596 | 0.779 | 0.731 | 9,335 | 9,335 | 0.789 | 0.736 | 0.675 | 0.732 | 1.002 | 0.938 |  |
| archived-20261005-042924: db.jsonl | 4f010d8ab9 | 0.763 | 0.721 | 9,343 | 9,343 | 0.779 | 0.734 | 0.646 | 0.691 | 1.012 | 0.849 |  |
| archived-20261005-042924: db.jsonl | 4032a5ce71 | 0.754 | 0.698 | 9,351 | 9,351 | 0.758 | 0.808 | 0.603 | 0.693 | 0.955 | 0.927 |  |
| archived-20261005-042924: db.jsonl | 528fc9619a | 0.756 | 0.702 | 9,359 | 9,359 | 0.767 | 0.770 | 0.614 | 0.693 | 0.982 | 0.862 |  |
| archived-20261005-042924: db.jsonl | f052397620 | 0.724 | 0.685 | 9,450 | 9,450 | 0.722 | 0.811 | 0.561 | 0.673 | 0.897 | 0.913 |  |
| archived-20261005-042924: db.jsonl | 8dc0f97f2c | 0.727 | 0.680 | 9,458 | 9,458 | 0.726 | 0.770 | 0.580 | 0.684 | 0.918 | 0.885 |  |
| archived-20261005-042924: db.jsonl | 52b80007a1 | 0.702 | 0.640 | 10,010 | 10,010 | 0.745 | 0.552 | 0.602 | 0.691 | 0.996 | 0.847 |  |
| archived-20261005-042924: db.jsonl | 5ed1ed8715 | 0.704 | 0.642 | 10,018 | 10,018 | 0.758 | 0.550 | 0.614 | 0.688 | 0.983 | 0.866 |  |
| archived-20261005-042924: db.jsonl | 9e50623ac1 | 0.660 | 0.593 | 13,073 | 13,073 | 0.670 | 0.713 | 0.481 | 0.600 | 0.909 | 0.853 |  |
| archived-20261005-042924: db.jsonl | 22b81e50c4 | 0.659 | 0.605 | 13,209 | 13,209 | 0.638 | 0.883 | 0.431 | 0.538 | 0.952 | 0.843 |  |
| archived-20261005-042924: db.jsonl | 2db525ff95 | 0.647 | 0.579 | 14,017 | 14,017 | 0.647 | 0.716 | 0.452 | 0.559 | 0.971 | 0.904 |  |
| archived-20261005-131253: db.jsonl | 422d6bcbca | 0.738 | 0.699 | 9,327 | 9,327 | 0.740 | 0.864 | 0.543 | 0.650 | 0.970 | 0.865 |  |
| archived-20261005-131253: db.jsonl | 090672993b | 0.741 | 0.700 | 9,335 | 9,335 | 0.686 | 0.856 | 0.636 | 0.684 | 0.875 | 0.774 |  |
| archived-20261005-131253: db.jsonl | 6495dcb5dd | 0.694 | 0.662 | 9,343 | 9,343 | 0.672 | 0.929 | 0.518 | 0.619 | 0.806 | 0.793 |  |
| archived-20261005-131253: db.jsonl | c40ba92d5b | 0.660 | 0.630 | 9,511 | 9,511 | 0.652 | 0.683 | 0.564 | 0.616 | 0.812 | 0.792 |  |
| archived-20261005-131253: db.jsonl | ca2ac63866 | 0.684 | 0.634 | 9,531 | 9,531 | 0.656 | 0.730 | 0.563 | 0.623 | 0.889 | 0.842 |  |
| archived-20261005-131253: db.jsonl | c61857fc89 | 0.646 | 0.633 | 10,034 | 10,034 | 0.679 | 0.688 | 0.536 | 0.623 | 0.719 | 0.856 |  |
| archived-20261005-131253: db.jsonl | b06a4cf784 | 0.670 | 0.615 | 10,246 | 10,246 | 0.647 | 0.743 | 0.538 | 0.606 | 0.859 | 0.844 |  |
| archived-20261005-131253: db.jsonl | af5e8dc29f | 0.661 | 0.604 | 10,254 | 10,254 | 0.668 | 0.679 | 0.532 | 0.607 | 0.861 | 0.830 |  |
| archived-20261005-131253: db.jsonl | a74b828e9b | 0.664 | 0.608 | 13,073 | 13,073 | 0.674 | 0.623 | 0.511 | 0.615 | 0.975 | 0.851 |  |
| archived-20261005-131253: db.jsonl | dc02ceae31 | 0.607 | 0.560 | 13,161 | 13,161 | 0.614 | 0.720 | 0.442 | 0.537 | 0.786 | 0.835 |  |
| archived-20261005-131253: db.jsonl | 15dde12f04 | 0.593 | 0.567 | 13,345 | 13,345 | 0.612 | 0.773 | 0.398 | 0.519 | 0.752 | 0.816 |  |
| archived-20261005-131253: db.jsonl | cd943ed219 | 0.591 | 0.545 | 14,081 | 14,081 | 0.604 | 0.684 | 0.403 | 0.551 | 0.786 | 0.826 |  |
| archived-20261005-144844: db.jsonl | 49b0a93f14 | 0.693 | 0.688 | 8,073 | 8,073 | 0.716 | 0.886 | 0.552 | 0.638 | 0.714 | 0.797 | yes |
| archived-20261005-144844: db.jsonl | 9f5e6d173c | 0.686 | 0.650 | 8,074 | 8,074 | 0.666 | 0.874 | 0.529 | 0.605 | 0.811 | 0.854 | yes |
| archived-20261005-144844: db.jsonl | f060a4c31f | 0.677 | 0.637 | 8,289 | 8,289 | 0.652 | 0.836 | 0.518 | 0.591 | 0.855 | 0.804 |  |
| archived-20261005-144844: db.jsonl | a306cc61fb | 0.672 | 0.615 | 8,305 | 8,305 | 0.680 | 0.631 | 0.554 | 0.598 | 0.960 | 0.841 |  |
| archived-20261005-144844: db.jsonl | 3c2d8a577b | 0.650 | 0.603 | 8,306 | 8,306 | 0.655 | 0.643 | 0.527 | 0.589 | 0.887 | 0.782 | yes |
| archived-20261005-144844: db.jsonl | 4cc12fc1e7 | 0.623 | 0.561 | 8,957 | 8,957 | 0.608 | 0.550 | 0.499 | 0.591 | 0.951 | 0.749 |  |
| archived-20261005-144844: db.jsonl | 3a7c3d6e90 | 0.599 | 0.551 | 11,777 | 11,777 | 0.600 | 0.857 | 0.364 | 0.497 | 0.826 | 0.836 |  |
| archived-20261005-144844: db.jsonl | 2b00aa6e97 | 0.609 | 0.568 | 12,145 | 12,145 | 0.616 | 0.862 | 0.362 | 0.520 | 0.839 | 0.849 |  |
| archived-20261005-144844: db.jsonl | 27a35df3fa | 0.619 | 0.570 | 12,312 | 12,312 | 0.619 | 0.571 | 0.488 | 0.565 | 0.935 | 0.761 |  |
| archived-20261005-144844: db.jsonl | ff39b37bcc | 0.637 | 0.572 | 12,584 | 12,584 | 0.642 | 0.626 | 0.472 | 0.555 | 0.997 | 0.831 |  |
| archived-20261005-144844: db.jsonl | 1cf03a8fd4 | 0.607 | 0.545 | 12,608 | 12,608 | 0.598 | 0.678 | 0.407 | 0.550 | 0.910 | 0.808 |  |
| archived-20261005-144844: db.jsonl | a214fa731c | 0.604 | 0.557 | 12,664 | 12,664 | 0.633 | 0.622 | 0.463 | 0.583 | 0.755 | 0.757 |  |

The front of all runs together, by size: 9bb527944a 0.449 at 13,073, 577c999e62 0.454 at 9,278, 959e88b0f5 0.462 at 9,140, 72ca2cf497 0.480 at 8,990, 1b602bc9bd 0.490 at 8,671, f85a63f8c7 0.503 at 8,647, 85cac726b5 0.505 at 8,614, 3d31fd4cc4 0.522 at 8,550, caf4358de8 0.529 at 8,540, be02a4c0cf 0.550 at 8,525, 3c2d8a577b 0.650 at 8,306, 8a2189b3b6 0.661 at 8,171, 9f5e6d173c 0.686 at 8,074, 49b0a93f14 0.693 at 8,073, d4739aac88 0.719 at 8,042, 3781c5e756 0.757 at 8,041, f41ab1810d 1.005 at 8,034

## The same session on two CPUs

Calibration on cpu 2: 1.003; on cpu 8: 1.007.

Speed on cpu 2 over speed on cpu 8, per design: median 1.004, 10-90% 0.991-1.018, extremes 0.986-1.031; rank agreement (Spearman) 0.99.

The front of all runs on cpu 2: 9bb527944a 0.449 at 13,073, 577c999e62 0.454 at 9,278, 959e88b0f5 0.462 at 9,140, 72ca2cf497 0.480 at 8,990, 1b602bc9bd 0.490 at 8,671, f85a63f8c7 0.503 at 8,647, 85cac726b5 0.505 at 8,614, 3d31fd4cc4 0.522 at 8,550, caf4358de8 0.529 at 8,540, be02a4c0cf 0.550 at 8,525, 3c2d8a577b 0.650 at 8,306, 8a2189b3b6 0.661 at 8,171, 9f5e6d173c 0.686 at 8,074, 49b0a93f14 0.693 at 8,073, d4739aac88 0.719 at 8,042, 3781c5e756 0.757 at 8,041, f41ab1810d 1.005 at 8,034

The front of all runs on cpu 8: 9bb527944a 0.449 at 13,073, 959e88b0f5 0.453 at 9,140, 72ca2cf497 0.476 at 8,990, 1b602bc9bd 0.482 at 8,671, 85cac726b5 0.489 at 8,614, 3d31fd4cc4 0.516 at 8,550, 6578fc6928 0.522 at 8,548, caf4358de8 0.527 at 8,540, be02a4c0cf 0.543 at 8,525, 8a2189b3b6 0.659 at 8,171, e05adba602 0.683 at 8,082, 9f5e6d173c 0.688 at 8,074, 49b0a93f14 0.692 at 8,073, d4739aac88 0.720 at 8,042, 3781c5e756 0.761 at 8,041, f41ab1810d 1.011 at 8,034

On both fronts: 14 of 17 and 16.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| 9bb527944a | 0.449 | 0.449 | 0.999 |
| 577c999e62 | 0.454 | 0.459 | 0.988 |
| 959e88b0f5 | 0.462 | 0.453 | 1.022 |
| 0212f86508 | 0.468 | 0.464 | 1.009 |
| 72ca2cf497 | 0.480 | 0.476 | 1.009 |
| aba06380d6 | 0.483 | 0.483 | 1.000 |
| 1b602bc9bd | 0.490 | 0.482 | 1.018 |
| f85a63f8c7 | 0.503 | 0.499 | 1.008 |
| 85cac726b5 | 0.505 | 0.489 | 1.031 |
| 51879a71f0 | 0.512 | 0.502 | 1.021 |
| 3d31fd4cc4 | 0.522 | 0.516 | 1.011 |
| caf4358de8 | 0.529 | 0.527 | 1.005 |
| 6578fc6928 | 0.530 | 0.522 | 1.016 |
| be02a4c0cf | 0.550 | 0.543 | 1.013 |
| cd943ed219 | 0.591 | 0.590 | 1.002 |
| 15dde12f04 | 0.593 | 0.592 | 1.003 |
| 3a7c3d6e90 | 0.599 | 0.604 | 0.991 |
| a214fa731c | 0.604 | 0.595 | 1.015 |
| 1cf03a8fd4 | 0.607 | 0.596 | 1.018 |
| dc02ceae31 | 0.607 | 0.603 | 1.007 |
| 2b00aa6e97 | 0.609 | 0.604 | 1.009 |
| 27a35df3fa | 0.619 | 0.618 | 1.002 |
| 4cc12fc1e7 | 0.623 | 0.616 | 1.011 |
| ff39b37bcc | 0.637 | 0.633 | 1.007 |
| 29ad5ba726 | 0.637 | 0.645 | 0.989 |
| 8dd8a7a146 | 0.638 | 0.645 | 0.989 |
| 05617039f6 | 0.640 | 0.635 | 1.007 |
| c61857fc89 | 0.646 | 0.648 | 0.996 |
| 2db525ff95 | 0.647 | 0.654 | 0.990 |
| e99da68667 | 0.649 | 0.646 | 1.005 |
| 3c2d8a577b | 0.650 | 0.659 | 0.987 |
| 22b81e50c4 | 0.659 | 0.652 | 1.010 |
| 9e50623ac1 | 0.660 | 0.655 | 1.007 |
| c40ba92d5b | 0.660 | 0.667 | 0.990 |
| 1769ca2a48 | 0.660 | 0.654 | 1.010 |
| 8a2189b3b6 | 0.661 | 0.659 | 1.003 |
| af5e8dc29f | 0.661 | 0.658 | 1.005 |
| a74b828e9b | 0.664 | 0.669 | 0.992 |
| b06a4cf784 | 0.670 | 0.651 | 1.029 |
| a306cc61fb | 0.672 | 0.668 | 1.006 |
| 32600cab87 | 0.672 | 0.674 | 0.998 |
| f060a4c31f | 0.677 | 0.681 | 0.995 |
| 0b1d16def9 | 0.678 | 0.675 | 1.004 |
| 66eb4a8f15 | 0.680 | 0.680 | 1.000 |
| 448ef1ef43 | 0.681 | 0.684 | 0.996 |
| 14f6036a4b | 0.683 | 0.670 | 1.020 |
| ca2ac63866 | 0.684 | 0.681 | 1.005 |
| 312ad2edaa | 0.685 | 0.673 | 1.018 |
| 9f5e6d173c | 0.686 | 0.688 | 0.996 |
| f66d74a27c | 0.690 | 0.688 | 1.003 |
| e0cbf09bc2 | 0.690 | 0.700 | 0.986 |
| 60753a0eb0 | 0.691 | 0.687 | 1.005 |
| 4cb3fa9172 | 0.691 | 0.698 | 0.989 |
| a27aa49d8e | 0.693 | 0.698 | 0.992 |
| 49b0a93f14 | 0.693 | 0.692 | 1.000 |
| 6495dcb5dd | 0.694 | 0.701 | 0.990 |
| 38d187239c | 0.694 | 0.698 | 0.995 |
| e05adba602 | 0.695 | 0.683 | 1.017 |
| bb8a0cb575 | 0.698 | 0.694 | 1.005 |
| 52b80007a1 | 0.702 | 0.698 | 1.006 |
| c297551359 | 0.703 | 0.703 | 1.000 |
| 12d8e18511 | 0.703 | 0.701 | 1.003 |
| 38d91795a2 | 0.704 | 0.710 | 0.991 |
| 5ed1ed8715 | 0.704 | 0.704 | 0.999 |
| 6463752a82 | 0.706 | 0.694 | 1.017 |
| d4739aac88 | 0.719 | 0.720 | 0.999 |
| 7fe7f039bd | 0.721 | 0.720 | 1.001 |
| 8cbc6dd05c | 0.722 | 0.721 | 1.001 |
| 84e302c470 | 0.723 | 0.722 | 1.001 |
| f4a6dd9a13 | 0.723 | 0.723 | 1.001 |
| f052397620 | 0.724 | 0.718 | 1.008 |
| 8dc0f97f2c | 0.727 | 0.718 | 1.013 |
| e8f1dd3ca2 | 0.732 | 0.718 | 1.019 |
| 53ec9bedde | 0.733 | 0.728 | 1.007 |
| a285fa6ba3 | 0.736 | 0.730 | 1.007 |
| 57a9dcc7cb | 0.736 | 0.731 | 1.006 |
| 422d6bcbca | 0.738 | 0.736 | 1.003 |
| 090672993b | 0.741 | 0.730 | 1.016 |
| 05dcc81cdc | 0.743 | 0.741 | 1.003 |
| 550df563ee | 0.749 | 0.739 | 1.013 |
| 3453246bdf | 0.750 | 0.746 | 1.006 |
| 57e0e77c09 | 0.751 | 0.751 | 1.000 |
| 4032a5ce71 | 0.754 | 0.757 | 0.996 |
| 6738aed13f | 0.756 | 0.762 | 0.992 |
| 9cd791dd84 | 0.756 | 0.760 | 0.995 |
| 528fc9619a | 0.756 | 0.751 | 1.007 |
| 3781c5e756 | 0.757 | 0.761 | 0.994 |
| 595fc2b8f4 | 0.761 | 0.751 | 1.014 |
| 4f010d8ab9 | 0.763 | 0.762 | 1.001 |
| 5b70f3dd64 | 0.766 | 0.769 | 0.996 |
| 0ebf0445e0 | 0.773 | 0.763 | 1.013 |
| 90018981c6 | 0.775 | 0.774 | 1.001 |
| c17103bf95 | 0.777 | 0.780 | 0.997 |
| 98736f0596 | 0.779 | 0.776 | 1.004 |
| a4e82e02e5 | 0.806 | 0.799 | 1.009 |
| 672538daf5 | 0.824 | 0.823 | 1.001 |
| 83cb81c383 | 0.845 | 0.830 | 1.018 |
| f41ab1810d | 1.005 | 1.011 | 0.993 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 7 - Iteration 45: seeds 1-9, after seed 9

`seed 9 then experiment compare-fronts.py --rounds 10 --cpus 2,8`, commit
807d0d63: eleven databases, 109 front designs, five workloads, sieve held
out. Twelve minutes. **Calibration 1.000** (every workload 0.988-1.010).
The CPUs agree: per design median 1.000, 10-90% 0.994-1.009, ranks 1.00;
13 designs on both CPUs' fronts.

**The front of all runs**: seed 9's eight from 7,019 bytes (0.794) to
7,725 (0.515) - none of them with an earlier design as small - and seed
8's seven from 8,614 (0.508) to 13,073 (0.442, the fastest).

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 1.000** (kernel 1.009, fib 0.988, parse 1.010, corpus 1.000, loop 0.995, sieve 1.000).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | c513ef17b0 | 0.794 | 0.781 | 7,019 | 7,019 | 0.844 | 0.783 | 0.628 | 0.760 | 1.000 | 0.864 | yes |
| this clone: db.jsonl | 57d12a1bb0 | 0.753 | 0.756 | 7,020 | 7,020 | 0.773 | 0.890 | 0.604 | 0.701 | 0.829 | 0.848 | yes |
| this clone: db.jsonl | ee4d8f8a50 | 0.723 | 0.723 | 7,027 | 7,027 | 0.782 | 0.771 | 0.609 | 0.706 | 0.761 | 0.856 | yes |
| this clone: db.jsonl | ccce4784b8 | 0.694 | 0.681 | 7,091 | 7,091 | 0.741 | 0.718 | 0.638 | 0.697 | 0.680 | 0.834 | yes |
| this clone: db.jsonl | 88792f1798 | 0.655 | 0.653 | 7,220 | 7,220 | 0.698 | 0.727 | 0.546 | 0.630 | 0.692 | 0.795 | yes |
| this clone: db.jsonl | 2367cb920c | 0.546 | 0.538 | 7,510 | 7,510 | 0.744 | 0.792 | 0.611 | 0.705 | 0.191 | 0.612 | yes |
| this clone: db.jsonl | 853cfb9d36 | 0.551 | 0.536 | 7,651 | 7,651 | 0.745 | 0.819 | 0.622 | 0.698 | 0.192 | 0.637 |  |
| this clone: db.jsonl | fa23f401cd | 0.541 | 0.525 | 7,692 | 7,692 | 0.701 | 0.873 | 0.613 | 0.658 | 0.188 | 0.645 | yes |
| this clone: db.jsonl | 45d2ff7e01 | 0.515 | 0.500 | 7,725 | 7,725 | 0.703 | 0.715 | 0.558 | 0.642 | 0.201 | 0.666 | yes |
| this clone: db.jsonl | f084674b22 | 0.519 | 0.516 | 9,198 | 9,198 | 0.710 | 0.726 | 0.576 | 0.640 | 0.198 | 0.668 |  |
| this clone: db.jsonl | 9d89f6ba0e | 0.499 | 0.487 | 13,065 | 13,065 | 0.672 | 0.776 | 0.500 | 0.613 | 0.193 | 0.668 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 595fc2b8f4 | 0.757 | 0.784 | 9,662 | 9,761 | 0.744 | 0.707 | 0.638 | 0.704 | 1.051 | 0.834 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 8cbc6dd05c | 0.732 | 0.742 | 9,694 | 9,809 | 0.735 | 0.795 | 0.613 | 0.685 | 0.858 | 0.808 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 6738aed13f | 0.763 | 0.755 | 9,694 | 9,793 | 0.784 | 0.696 | 0.633 | 0.703 | 1.064 | 0.832 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 312ad2edaa | 0.688 | 0.716 | 13,344 | 13,456 | 0.692 | 0.726 | 0.550 | 0.628 | 0.891 | 0.837 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 05617039f6 | 0.637 | 0.674 | 13,352 | 13,488 | 0.663 | 0.794 | 0.475 | 0.603 | 0.693 | 0.822 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 0b1d16def9 | 0.691 | 0.705 | 13,352 | 13,464 | 0.715 | 0.822 | 0.522 | 0.637 | 0.804 | 0.862 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 57a9dcc7cb | 0.741 | 0.680 | 13,368 | 13,480 | 0.709 | 0.922 | 0.548 | 0.653 | 0.953 | 0.887 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 32600cab87 | 0.680 | 0.662 | 13,528 | 13,656 | 0.675 | 0.966 | 0.514 | 0.617 | 0.702 | 0.844 |  |
| archived-20261004-200423: db-seed1.jsonl | 83cb81c383 | 0.843 | 0.705 | 9,662 | 9,761 | 0.773 | 1.003 | 0.692 | 0.741 | 1.068 | 0.899 |  |
| archived-20261004-200423: db-seed1.jsonl | 5b70f3dd64 | 0.768 | 0.649 | 9,694 | 9,801 | 0.741 | 0.955 | 0.626 | 0.699 | 0.860 | 0.821 |  |
| archived-20261004-200423: db-seed1.jsonl | a4e82e02e5 | 0.803 | 0.654 | 9,694 | 9,809 | 0.776 | 0.915 | 0.651 | 0.736 | 0.982 | 0.905 |  |
| archived-20261004-200423: db-seed1.jsonl | 53ec9bedde | 0.727 | 0.670 | 13,336 | 13,464 | 0.745 | 0.762 | 0.612 | 0.681 | 0.859 | 0.838 |  |
| archived-20261004-200423: db-seed1.jsonl | 448ef1ef43 | 0.691 | 0.620 | 13,368 | 13,488 | 0.684 | 0.960 | 0.494 | 0.607 | 0.800 | 0.833 |  |
| archived-20261004-200423: db-seed1.jsonl | 38d187239c | 0.695 | 0.609 | 13,368 | 13,480 | 0.708 | 0.825 | 0.551 | 0.635 | 0.793 | 0.819 |  |
| archived-20261004-200423: db-seed2.jsonl | 0ebf0445e0 | 0.774 | 0.667 | 9,662 | 9,761 | 0.797 | 0.702 | 0.686 | 0.742 | 0.972 | 0.903 |  |
| archived-20261004-200423: db-seed2.jsonl | c17103bf95 | 0.788 | 0.725 | 9,662 | 9,769 | 0.804 | 0.760 | 0.720 | 0.757 | 0.914 | 0.898 |  |
| archived-20261004-200423: db-seed2.jsonl | a285fa6ba3 | 0.737 | 0.666 | 13,352 | 13,464 | 0.762 | 0.696 | 0.629 | 0.708 | 0.923 | 0.864 |  |
| archived-20261004-200423: db-seed2.jsonl | 57e0e77c09 | 0.756 | 0.657 | 13,352 | 13,480 | 0.721 | 1.048 | 0.536 | 0.651 | 0.933 | 0.893 |  |
| archived-20261004-200423: db-seed2.jsonl | 9cd791dd84 | 0.759 | 0.619 | 13,368 | 13,472 | 0.732 | 0.897 | 0.576 | 0.668 | 0.997 | 0.899 |  |
| archived-20261004-200423: db.jsonl | 550df563ee | 0.744 | 0.696 | 9,646 | 9,745 | 0.703 | 0.780 | 0.621 | 0.686 | 0.977 | 0.839 |  |
| archived-20261004-200423: db.jsonl | f4a6dd9a13 | 0.730 | 0.683 | 9,662 | 9,761 | 0.743 | 0.661 | 0.617 | 0.701 | 0.975 | 0.807 |  |
| archived-20261004-200423: db.jsonl | 60753a0eb0 | 0.686 | 0.622 | 9,686 | 9,785 | 0.687 | 0.670 | 0.566 | 0.648 | 0.900 | 0.780 |  |
| archived-20261004-200423: db.jsonl | 8dd8a7a146 | 0.649 | 0.595 | 13,352 | 13,464 | 0.649 | 0.664 | 0.514 | 0.606 | 0.858 | 0.788 |  |
| archived-20261004-214724: db.jsonl | 3453246bdf | 0.750 | 0.727 | 9,335 | 9,335 | 0.759 | 0.687 | 0.674 | 0.746 | 0.908 | 0.875 |  |
| archived-20261004-214724: db.jsonl | 672538daf5 | 0.835 | 0.780 | 9,351 | 9,351 | 0.821 | 0.838 | 0.717 | 0.793 | 1.037 | 0.885 |  |
| archived-20261004-214724: db.jsonl | 7fe7f039bd | 0.724 | 0.702 | 9,450 | 9,450 | 0.765 | 0.699 | 0.615 | 0.722 | 0.835 | 0.871 |  |
| archived-20261004-214724: db.jsonl | 38d91795a2 | 0.716 | 0.678 | 9,474 | 9,474 | 0.758 | 0.653 | 0.620 | 0.723 | 0.850 | 0.867 |  |
| archived-20261004-214724: db.jsonl | 6463752a82 | 0.701 | 0.669 | 9,523 | 9,523 | 0.714 | 0.713 | 0.588 | 0.657 | 0.865 | 0.858 |  |
| archived-20261004-214724: db.jsonl | 90018981c6 | 0.771 | 0.696 | 9,678 | 9,678 | 0.738 | 0.808 | 0.635 | 0.714 | 1.010 | 0.877 |  |
| archived-20261004-214724: db.jsonl | e0cbf09bc2 | 0.702 | 0.666 | 13,057 | 13,057 | 0.697 | 0.755 | 0.528 | 0.644 | 0.952 | 0.880 |  |
| archived-20261004-214724: db.jsonl | 1769ca2a48 | 0.663 | 0.603 | 13,209 | 13,209 | 0.689 | 0.623 | 0.538 | 0.643 | 0.860 | 0.821 |  |
| archived-20261004-214724: db.jsonl | 14f6036a4b | 0.681 | 0.627 | 13,217 | 13,217 | 0.675 | 0.821 | 0.478 | 0.600 | 0.921 | 0.901 |  |
| archived-20261004-214724: db.jsonl | 29ad5ba726 | 0.646 | 0.589 | 13,352 | 13,352 | 0.657 | 0.760 | 0.494 | 0.587 | 0.778 | 0.817 |  |
| archived-20261004-214724: db.jsonl | 12d8e18511 | 0.705 | 0.667 | 13,360 | 13,360 | 0.695 | 0.850 | 0.524 | 0.615 | 0.917 | 0.945 |  |
| archived-20261005-013645: db.jsonl | 05dcc81cdc | 0.744 | 0.688 | 9,335 | 9,335 | 0.734 | 0.811 | 0.605 | 0.685 | 0.922 | 0.896 |  |
| archived-20261005-013645: db.jsonl | c297551359 | 0.710 | 0.682 | 9,450 | 9,450 | 0.745 | 0.661 | 0.630 | 0.705 | 0.823 | 0.858 |  |
| archived-20261005-013645: db.jsonl | e8f1dd3ca2 | 0.726 | 0.678 | 9,458 | 9,458 | 0.704 | 0.817 | 0.560 | 0.652 | 0.958 | 0.885 |  |
| archived-20261005-013645: db.jsonl | 66eb4a8f15 | 0.681 | 0.641 | 13,057 | 13,057 | 0.705 | 0.685 | 0.520 | 0.640 | 0.912 | 0.865 |  |
| archived-20261005-013645: db.jsonl | 84e302c470 | 0.727 | 0.657 | 13,065 | 13,065 | 0.732 | 0.756 | 0.552 | 0.662 | 1.003 | 0.904 |  |
| archived-20261005-013645: db.jsonl | 4cb3fa9172 | 0.688 | 0.626 | 13,073 | 13,073 | 0.668 | 0.793 | 0.498 | 0.600 | 0.972 | 0.882 |  |
| archived-20261005-013645: db.jsonl | e99da68667 | 0.658 | 0.581 | 13,201 | 13,201 | 0.632 | 0.770 | 0.451 | 0.567 | 0.994 | 0.873 |  |
| archived-20261005-042924: db.jsonl | 98736f0596 | 0.781 | 0.731 | 9,335 | 9,335 | 0.799 | 0.735 | 0.667 | 0.741 | 1.001 | 0.918 |  |
| archived-20261005-042924: db.jsonl | 4f010d8ab9 | 0.768 | 0.721 | 9,343 | 9,343 | 0.763 | 0.734 | 0.661 | 0.717 | 1.008 | 0.902 |  |
| archived-20261005-042924: db.jsonl | 4032a5ce71 | 0.757 | 0.698 | 9,351 | 9,351 | 0.755 | 0.809 | 0.598 | 0.708 | 0.961 | 0.923 |  |
| archived-20261005-042924: db.jsonl | 528fc9619a | 0.749 | 0.702 | 9,359 | 9,359 | 0.771 | 0.731 | 0.610 | 0.701 | 0.977 | 0.884 |  |
| archived-20261005-042924: db.jsonl | f052397620 | 0.733 | 0.685 | 9,450 | 9,450 | 0.734 | 0.809 | 0.576 | 0.689 | 0.901 | 0.907 |  |
| archived-20261005-042924: db.jsonl | 8dc0f97f2c | 0.732 | 0.680 | 9,458 | 9,458 | 0.751 | 0.764 | 0.583 | 0.684 | 0.918 | 0.868 |  |
| archived-20261005-042924: db.jsonl | 52b80007a1 | 0.695 | 0.640 | 10,010 | 10,010 | 0.735 | 0.549 | 0.595 | 0.686 | 0.984 | 0.866 |  |
| archived-20261005-042924: db.jsonl | 5ed1ed8715 | 0.704 | 0.642 | 10,018 | 10,018 | 0.745 | 0.551 | 0.599 | 0.699 | 1.008 | 0.860 |  |
| archived-20261005-042924: db.jsonl | 9e50623ac1 | 0.655 | 0.593 | 13,073 | 13,073 | 0.664 | 0.700 | 0.481 | 0.597 | 0.902 | 0.872 |  |
| archived-20261005-042924: db.jsonl | 22b81e50c4 | 0.661 | 0.605 | 13,209 | 13,209 | 0.639 | 0.887 | 0.425 | 0.559 | 0.935 | 0.890 |  |
| archived-20261005-042924: db.jsonl | 2db525ff95 | 0.654 | 0.579 | 14,017 | 14,017 | 0.648 | 0.719 | 0.455 | 0.591 | 0.953 | 0.905 |  |
| archived-20261005-131253: db.jsonl | 422d6bcbca | 0.739 | 0.699 | 9,327 | 9,327 | 0.750 | 0.862 | 0.540 | 0.657 | 0.959 | 0.866 |  |
| archived-20261005-131253: db.jsonl | 090672993b | 0.742 | 0.700 | 9,335 | 9,335 | 0.713 | 0.821 | 0.636 | 0.686 | 0.883 | 0.783 |  |
| archived-20261005-131253: db.jsonl | 6495dcb5dd | 0.702 | 0.662 | 9,343 | 9,343 | 0.668 | 0.931 | 0.531 | 0.632 | 0.815 | 0.791 |  |
| archived-20261005-131253: db.jsonl | c40ba92d5b | 0.666 | 0.630 | 9,511 | 9,511 | 0.679 | 0.689 | 0.563 | 0.632 | 0.786 | 0.795 |  |
| archived-20261005-131253: db.jsonl | ca2ac63866 | 0.684 | 0.634 | 9,531 | 9,531 | 0.658 | 0.731 | 0.558 | 0.625 | 0.893 | 0.859 |  |
| archived-20261005-131253: db.jsonl | c61857fc89 | 0.657 | 0.633 | 10,034 | 10,034 | 0.689 | 0.709 | 0.538 | 0.637 | 0.731 | 0.843 |  |
| archived-20261005-131253: db.jsonl | b06a4cf784 | 0.661 | 0.615 | 10,246 | 10,246 | 0.643 | 0.698 | 0.535 | 0.610 | 0.860 | 0.841 |  |
| archived-20261005-131253: db.jsonl | af5e8dc29f | 0.665 | 0.604 | 10,254 | 10,254 | 0.657 | 0.673 | 0.535 | 0.626 | 0.879 | 0.824 |  |
| archived-20261005-131253: db.jsonl | a74b828e9b | 0.667 | 0.608 | 13,073 | 13,073 | 0.685 | 0.632 | 0.505 | 0.623 | 0.967 | 0.843 |  |
| archived-20261005-131253: db.jsonl | dc02ceae31 | 0.610 | 0.560 | 13,161 | 13,161 | 0.618 | 0.722 | 0.433 | 0.550 | 0.793 | 0.844 |  |
| archived-20261005-131253: db.jsonl | 15dde12f04 | 0.602 | 0.567 | 13,345 | 13,345 | 0.620 | 0.751 | 0.403 | 0.544 | 0.773 | 0.826 |  |
| archived-20261005-131253: db.jsonl | cd943ed219 | 0.593 | 0.545 | 14,081 | 14,081 | 0.610 | 0.680 | 0.407 | 0.547 | 0.794 | 0.843 |  |
| archived-20261005-144844: db.jsonl | 49b0a93f14 | 0.695 | 0.688 | 8,073 | 8,073 | 0.721 | 0.872 | 0.566 | 0.650 | 0.703 | 0.835 |  |
| archived-20261005-144844: db.jsonl | 9f5e6d173c | 0.698 | 0.650 | 8,074 | 8,074 | 0.673 | 0.903 | 0.531 | 0.626 | 0.817 | 0.829 |  |
| archived-20261005-144844: db.jsonl | f060a4c31f | 0.681 | 0.637 | 8,289 | 8,289 | 0.648 | 0.840 | 0.520 | 0.598 | 0.869 | 0.810 |  |
| archived-20261005-144844: db.jsonl | a306cc61fb | 0.674 | 0.615 | 8,305 | 8,305 | 0.680 | 0.634 | 0.558 | 0.619 | 0.936 | 0.812 |  |
| archived-20261005-144844: db.jsonl | 3c2d8a577b | 0.656 | 0.603 | 8,306 | 8,306 | 0.677 | 0.635 | 0.527 | 0.613 | 0.875 | 0.813 |  |
| archived-20261005-144844: db.jsonl | 4cc12fc1e7 | 0.633 | 0.561 | 8,957 | 8,957 | 0.636 | 0.563 | 0.507 | 0.601 | 0.930 | 0.768 |  |
| archived-20261005-144844: db.jsonl | 3a7c3d6e90 | 0.607 | 0.551 | 11,777 | 11,777 | 0.615 | 0.854 | 0.358 | 0.530 | 0.826 | 0.855 |  |
| archived-20261005-144844: db.jsonl | 2b00aa6e97 | 0.611 | 0.568 | 12,145 | 12,145 | 0.602 | 0.863 | 0.363 | 0.545 | 0.830 | 0.862 |  |
| archived-20261005-144844: db.jsonl | 27a35df3fa | 0.630 | 0.570 | 12,312 | 12,312 | 0.633 | 0.578 | 0.494 | 0.583 | 0.943 | 0.778 |  |
| archived-20261005-144844: db.jsonl | ff39b37bcc | 0.635 | 0.572 | 12,584 | 12,584 | 0.637 | 0.628 | 0.462 | 0.572 | 0.974 | 0.842 |  |
| archived-20261005-144844: db.jsonl | 1cf03a8fd4 | 0.611 | 0.545 | 12,608 | 12,608 | 0.610 | 0.691 | 0.403 | 0.550 | 0.914 | 0.811 |  |
| archived-20261005-144844: db.jsonl | a214fa731c | 0.601 | 0.557 | 12,664 | 12,664 | 0.646 | 0.611 | 0.452 | 0.579 | 0.757 | 0.783 |  |
| archived-20261005-164554: db.jsonl | f41ab1810d | 1.011 | 1.008 | 8,034 | 8,034 | 1.026 | 1.250 | 0.804 | 0.938 | 1.093 | 1.171 |  |
| archived-20261005-164554: db.jsonl | 3781c5e756 | 0.767 | 0.758 | 8,041 | 8,041 | 0.769 | 0.962 | 0.609 | 0.701 | 0.839 | 0.859 |  |
| archived-20261005-164554: db.jsonl | d4739aac88 | 0.725 | 0.723 | 8,042 | 8,042 | 0.806 | 0.730 | 0.632 | 0.744 | 0.725 | 0.881 |  |
| archived-20261005-164554: db.jsonl | e05adba602 | 0.693 | 0.687 | 8,082 | 8,082 | 0.715 | 0.769 | 0.548 | 0.666 | 0.797 | 0.814 |  |
| archived-20261005-164554: db.jsonl | bb8a0cb575 | 0.701 | 0.688 | 8,099 | 8,099 | 0.749 | 0.770 | 0.562 | 0.688 | 0.756 | 0.837 |  |
| archived-20261005-164554: db.jsonl | a27aa49d8e | 0.703 | 0.693 | 8,163 | 8,163 | 0.685 | 0.854 | 0.527 | 0.629 | 0.883 | 0.841 |  |
| archived-20261005-164554: db.jsonl | 8a2189b3b6 | 0.656 | 0.646 | 8,171 | 8,171 | 0.673 | 0.756 | 0.512 | 0.616 | 0.758 | 0.839 |  |
| archived-20261005-164554: db.jsonl | f66d74a27c | 0.687 | 0.682 | 8,210 | 8,210 | 0.690 | 0.879 | 0.518 | 0.635 | 0.764 | 0.826 |  |
| archived-20261005-164554: db.jsonl | be02a4c0cf | 0.551 | 0.533 | 8,525 | 8,525 | 0.787 | 0.780 | 0.613 | 0.710 | 0.190 | 0.602 |  |
| archived-20261005-164554: db.jsonl | caf4358de8 | 0.544 | 0.514 | 8,540 | 8,540 | 0.766 | 0.757 | 0.595 | 0.692 | 0.199 | 0.618 |  |
| archived-20261005-164554: db.jsonl | 6578fc6928 | 0.533 | 0.515 | 8,548 | 8,548 | 0.700 | 0.763 | 0.531 | 0.639 | 0.237 | 0.583 |  |
| archived-20261005-164554: db.jsonl | 3d31fd4cc4 | 0.528 | 0.502 | 8,550 | 8,550 | 0.700 | 0.866 | 0.522 | 0.624 | 0.207 | 0.660 |  |
| archived-20261005-164554: db.jsonl | 85cac726b5 | 0.508 | 0.484 | 8,614 | 8,614 | 0.655 | 0.861 | 0.524 | 0.609 | 0.187 | 0.628 | yes |
| archived-20261005-164554: db.jsonl | f85a63f8c7 | 0.502 | 0.481 | 8,647 | 8,647 | 0.648 | 0.853 | 0.524 | 0.596 | 0.185 | 0.622 | yes |
| archived-20261005-164554: db.jsonl | 51879a71f0 | 0.514 | 0.513 | 8,664 | 8,664 | 0.684 | 0.752 | 0.562 | 0.643 | 0.192 | 0.644 |  |
| archived-20261005-164554: db.jsonl | 1b602bc9bd | 0.500 | 0.478 | 8,671 | 8,671 | 0.676 | 0.788 | 0.483 | 0.603 | 0.201 | 0.589 | yes |
| archived-20261005-164554: db.jsonl | 72ca2cf497 | 0.487 | 0.469 | 8,990 | 8,990 | 0.652 | 0.667 | 0.510 | 0.609 | 0.203 | 0.530 | yes |
| archived-20261005-164554: db.jsonl | 959e88b0f5 | 0.469 | 0.458 | 9,140 | 9,140 | 0.665 | 0.529 | 0.515 | 0.629 | 0.199 | 0.546 | yes |
| archived-20261005-164554: db.jsonl | 577c999e62 | 0.466 | 0.443 | 9,278 | 9,278 | 0.652 | 0.555 | 0.509 | 0.603 | 0.198 | 0.529 | yes |
| archived-20261005-164554: db.jsonl | aba06380d6 | 0.488 | 0.462 | 12,353 | 12,353 | 0.663 | 0.769 | 0.482 | 0.592 | 0.189 | 0.635 |  |
| archived-20261005-164554: db.jsonl | 0212f86508 | 0.480 | 0.453 | 12,377 | 12,377 | 0.640 | 0.792 | 0.455 | 0.548 | 0.201 | 0.620 |  |
| archived-20261005-164554: db.jsonl | 9bb527944a | 0.442 | 0.430 | 13,073 | 13,073 | 0.623 | 0.555 | 0.437 | 0.557 | 0.201 | 0.557 | yes |

The front of all runs together, by size: 9bb527944a 0.442 at 13,073, 577c999e62 0.466 at 9,278, 959e88b0f5 0.469 at 9,140, 72ca2cf497 0.487 at 8,990, 1b602bc9bd 0.500 at 8,671, f85a63f8c7 0.502 at 8,647, 85cac726b5 0.508 at 8,614, 45d2ff7e01 0.515 at 7,725, fa23f401cd 0.541 at 7,692, 2367cb920c 0.546 at 7,510, 88792f1798 0.655 at 7,220, ccce4784b8 0.694 at 7,091, ee4d8f8a50 0.723 at 7,027, 57d12a1bb0 0.753 at 7,020, c513ef17b0 0.794 at 7,019

## The same session on two CPUs

Calibration on cpu 2: 1.000; on cpu 8: 1.004.

Speed on cpu 2 over speed on cpu 8, per design: median 1.000, 10-90% 0.994-1.009, extremes 0.988-1.038; rank agreement (Spearman) 1.00.

The front of all runs on cpu 2: 9bb527944a 0.442 at 13,073, 577c999e62 0.466 at 9,278, 959e88b0f5 0.469 at 9,140, 72ca2cf497 0.487 at 8,990, 1b602bc9bd 0.500 at 8,671, f85a63f8c7 0.502 at 8,647, 85cac726b5 0.508 at 8,614, 45d2ff7e01 0.515 at 7,725, fa23f401cd 0.541 at 7,692, 2367cb920c 0.546 at 7,510, 88792f1798 0.655 at 7,220, ccce4784b8 0.694 at 7,091, ee4d8f8a50 0.723 at 7,027, 57d12a1bb0 0.753 at 7,020, c513ef17b0 0.794 at 7,019

The front of all runs on cpu 8: 9bb527944a 0.441 at 13,073, 577c999e62 0.466 at 9,278, 959e88b0f5 0.471 at 9,140, 72ca2cf497 0.482 at 8,990, 1b602bc9bd 0.494 at 8,671, 45d2ff7e01 0.496 at 7,725, fa23f401cd 0.542 at 7,692, 853cfb9d36 0.547 at 7,651, 2367cb920c 0.550 at 7,510, 88792f1798 0.655 at 7,220, ccce4784b8 0.683 at 7,091, ee4d8f8a50 0.728 at 7,027, 57d12a1bb0 0.761 at 7,020, c513ef17b0 0.789 at 7,019

On both fronts: 13 of 15 and 14.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| 9bb527944a | 0.442 | 0.441 | 1.004 |
| 577c999e62 | 0.466 | 0.466 | 0.999 |
| 959e88b0f5 | 0.469 | 0.471 | 0.997 |
| 0212f86508 | 0.480 | 0.476 | 1.008 |
| 72ca2cf497 | 0.487 | 0.482 | 1.011 |
| aba06380d6 | 0.488 | 0.491 | 0.994 |
| 9d89f6ba0e | 0.499 | 0.496 | 1.005 |
| 1b602bc9bd | 0.500 | 0.494 | 1.011 |
| f85a63f8c7 | 0.502 | 0.502 | 1.000 |
| 85cac726b5 | 0.508 | 0.509 | 0.998 |
| 51879a71f0 | 0.514 | 0.515 | 0.997 |
| 45d2ff7e01 | 0.515 | 0.496 | 1.038 |
| f084674b22 | 0.519 | 0.517 | 1.004 |
| 3d31fd4cc4 | 0.528 | 0.525 | 1.005 |
| 6578fc6928 | 0.533 | 0.526 | 1.013 |
| fa23f401cd | 0.541 | 0.542 | 0.999 |
| caf4358de8 | 0.544 | 0.544 | 1.000 |
| 2367cb920c | 0.546 | 0.550 | 0.992 |
| be02a4c0cf | 0.551 | 0.551 | 1.000 |
| 853cfb9d36 | 0.551 | 0.547 | 1.008 |
| cd943ed219 | 0.593 | 0.596 | 0.995 |
| a214fa731c | 0.601 | 0.603 | 0.996 |
| 15dde12f04 | 0.602 | 0.601 | 1.001 |
| 3a7c3d6e90 | 0.607 | 0.608 | 0.998 |
| dc02ceae31 | 0.610 | 0.610 | 1.000 |
| 1cf03a8fd4 | 0.611 | 0.610 | 1.003 |
| 2b00aa6e97 | 0.611 | 0.610 | 1.003 |
| 27a35df3fa | 0.630 | 0.627 | 1.005 |
| 4cc12fc1e7 | 0.633 | 0.626 | 1.011 |
| ff39b37bcc | 0.635 | 0.636 | 0.998 |
| 05617039f6 | 0.637 | 0.640 | 0.995 |
| 29ad5ba726 | 0.646 | 0.648 | 0.997 |
| 8dd8a7a146 | 0.649 | 0.653 | 0.994 |
| 2db525ff95 | 0.654 | 0.648 | 1.010 |
| 9e50623ac1 | 0.655 | 0.657 | 0.996 |
| 88792f1798 | 0.655 | 0.655 | 1.000 |
| 3c2d8a577b | 0.656 | 0.659 | 0.995 |
| 8a2189b3b6 | 0.656 | 0.656 | 1.001 |
| c61857fc89 | 0.657 | 0.655 | 1.003 |
| e99da68667 | 0.658 | 0.661 | 0.995 |
| 22b81e50c4 | 0.661 | 0.660 | 1.000 |
| b06a4cf784 | 0.661 | 0.663 | 0.996 |
| 1769ca2a48 | 0.663 | 0.661 | 1.003 |
| af5e8dc29f | 0.665 | 0.666 | 0.999 |
| c40ba92d5b | 0.666 | 0.666 | 1.000 |
| a74b828e9b | 0.667 | 0.668 | 0.999 |
| a306cc61fb | 0.674 | 0.670 | 1.007 |
| 32600cab87 | 0.680 | 0.681 | 0.998 |
| 14f6036a4b | 0.681 | 0.676 | 1.007 |
| 66eb4a8f15 | 0.681 | 0.682 | 0.999 |
| f060a4c31f | 0.681 | 0.682 | 1.000 |
| ca2ac63866 | 0.684 | 0.680 | 1.005 |
| 60753a0eb0 | 0.686 | 0.691 | 0.993 |
| f66d74a27c | 0.687 | 0.686 | 1.001 |
| 4cb3fa9172 | 0.688 | 0.680 | 1.012 |
| 312ad2edaa | 0.688 | 0.689 | 0.998 |
| 0b1d16def9 | 0.691 | 0.682 | 1.012 |
| 448ef1ef43 | 0.691 | 0.697 | 0.992 |
| e05adba602 | 0.693 | 0.692 | 1.002 |
| ccce4784b8 | 0.694 | 0.683 | 1.016 |
| 38d187239c | 0.695 | 0.694 | 1.002 |
| 52b80007a1 | 0.695 | 0.703 | 0.990 |
| 49b0a93f14 | 0.695 | 0.698 | 0.996 |
| 9f5e6d173c | 0.698 | 0.697 | 1.000 |
| bb8a0cb575 | 0.701 | 0.700 | 1.001 |
| 6463752a82 | 0.701 | 0.708 | 0.991 |
| 6495dcb5dd | 0.702 | 0.695 | 1.009 |
| e0cbf09bc2 | 0.702 | 0.701 | 1.002 |
| a27aa49d8e | 0.703 | 0.706 | 0.995 |
| 5ed1ed8715 | 0.704 | 0.704 | 1.001 |
| 12d8e18511 | 0.705 | 0.709 | 0.995 |
| c297551359 | 0.710 | 0.706 | 1.006 |
| 38d91795a2 | 0.716 | 0.713 | 1.005 |
| ee4d8f8a50 | 0.723 | 0.728 | 0.994 |
| 7fe7f039bd | 0.724 | 0.724 | 0.999 |
| d4739aac88 | 0.725 | 0.725 | 1.001 |
| e8f1dd3ca2 | 0.726 | 0.729 | 0.995 |
| 53ec9bedde | 0.727 | 0.732 | 0.993 |
| 84e302c470 | 0.727 | 0.725 | 1.002 |
| f4a6dd9a13 | 0.730 | 0.725 | 1.007 |
| 8dc0f97f2c | 0.732 | 0.727 | 1.006 |
| 8cbc6dd05c | 0.732 | 0.727 | 1.008 |
| f052397620 | 0.733 | 0.723 | 1.014 |
| a285fa6ba3 | 0.737 | 0.734 | 1.004 |
| 422d6bcbca | 0.739 | 0.743 | 0.994 |
| 57a9dcc7cb | 0.741 | 0.737 | 1.005 |
| 090672993b | 0.742 | 0.740 | 1.004 |
| 05dcc81cdc | 0.744 | 0.747 | 0.996 |
| 550df563ee | 0.744 | 0.745 | 0.998 |
| 528fc9619a | 0.749 | 0.758 | 0.988 |
| 3453246bdf | 0.750 | 0.749 | 1.002 |
| 57d12a1bb0 | 0.753 | 0.761 | 0.989 |
| 57e0e77c09 | 0.756 | 0.760 | 0.994 |
| 595fc2b8f4 | 0.757 | 0.761 | 0.995 |
| 4032a5ce71 | 0.757 | 0.753 | 1.005 |
| 9cd791dd84 | 0.759 | 0.759 | 1.000 |
| 6738aed13f | 0.763 | 0.759 | 1.005 |
| 3781c5e756 | 0.767 | 0.767 | 0.999 |
| 5b70f3dd64 | 0.768 | 0.767 | 1.001 |
| 4f010d8ab9 | 0.768 | 0.765 | 1.004 |
| 90018981c6 | 0.771 | 0.774 | 0.997 |
| 0ebf0445e0 | 0.774 | 0.775 | 0.998 |
| 98736f0596 | 0.781 | 0.779 | 1.002 |
| c17103bf95 | 0.788 | 0.783 | 1.007 |
| c513ef17b0 | 0.794 | 0.789 | 1.007 |
| a4e82e02e5 | 0.803 | 0.809 | 0.993 |
| 672538daf5 | 0.835 | 0.829 | 1.007 |
| 83cb81c383 | 0.843 | 0.838 | 1.005 |
| f41ab1810d | 1.011 | 1.004 | 1.008 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 8 - Iteration 47: seeds 1-10, after seed 10 (the fronts carried in)

`seed 10 then experiment compare-fronts.py --rounds 10 --cpus 2,8`, commit
5dd1379b: twelve databases, 131 front designs (seed 10: its own 22; the
carried ones counted for their runs), five workloads, sieve held out.
Fourteen minutes. **Calibration 1.004.** The CPUs agree: per design median
1.001, 10-90% 0.992-1.009, ranks 1.00; 13 designs on both CPUs' fronts.

**The front of all runs**: seed 10's fifteen, from 6,977 bytes (0.760) to
12,145 (0.438), and seed 8's 9bb527944a, the fastest at 0.436.

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 1.004** (kernel 1.002, fib 1.019, parse 0.999, corpus 1.003, loop 0.995, sieve 0.993).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 295a6acd98 | 0.760 | 0.755 | 6,977 | 6,977 | 0.789 | 0.819 | 0.624 | 0.711 | 0.882 | 0.879 | yes |
| this clone: db.jsonl | 82e7e4dc0d | 0.729 | 0.726 | 6,979 | 6,979 | 0.771 | 0.827 | 0.583 | 0.688 | 0.805 | 0.871 | yes |
| this clone: db.jsonl | 9385a8fcbb | 0.697 | 0.690 | 6,994 | 6,994 | 0.699 | 0.884 | 0.546 | 0.660 | 0.737 | 0.828 | yes |
| this clone: db.jsonl | bf413bef91 | 0.668 | 0.681 | 7,002 | 7,002 | 0.702 | 0.700 | 0.531 | 0.640 | 0.796 | 0.851 | yes |
| this clone: db.jsonl | c25a5e1714 | 0.671 | 0.668 | 7,010 | 7,010 | 0.732 | 0.711 | 0.540 | 0.648 | 0.748 | 0.861 |  |
| this clone: db.jsonl | 7380e8bcb1 | 0.661 | 0.658 | 7,050 | 7,050 | 0.674 | 0.762 | 0.533 | 0.617 | 0.748 | 0.817 | yes |
| this clone: db.jsonl | 5df0608416 | 0.657 | 0.659 | 7,059 | 7,059 | 0.668 | 0.761 | 0.533 | 0.612 | 0.737 | 0.805 | yes |
| this clone: db.jsonl | d8d62beb78 | 0.555 | 0.545 | 7,106 | 7,106 | 0.748 | 0.869 | 0.601 | 0.687 | 0.196 | 0.664 | yes |
| this clone: db.jsonl | f3988ea716 | 0.517 | 0.510 | 7,113 | 7,113 | 0.688 | 0.771 | 0.563 | 0.638 | 0.194 | 0.650 | yes |
| this clone: db.jsonl | 2ed8b1583e | 0.509 | 0.509 | 7,129 | 7,129 | 0.693 | 0.801 | 0.524 | 0.627 | 0.188 | 0.585 | yes |
| this clone: db.jsonl | 641b85143d | 0.507 | 0.501 | 7,178 | 7,178 | 0.666 | 0.777 | 0.535 | 0.633 | 0.191 | 0.592 | yes |
| this clone: db.jsonl | 96f2d8bfd7 | 0.486 | 0.490 | 7,236 | 7,236 | 0.651 | 0.760 | 0.490 | 0.606 | 0.185 | 0.560 | yes |
| this clone: db.jsonl | 55ca1dfdb5 | 0.501 | 0.499 | 7,550 | 7,550 | 0.669 | 0.763 | 0.535 | 0.609 | 0.191 | 0.583 |  |
| this clone: db.jsonl | 0e8b212e50 | 0.506 | 0.507 | 7,558 | 7,558 | 0.646 | 0.851 | 0.522 | 0.605 | 0.191 | 0.608 |  |
| this clone: db.jsonl | 7a8d429413 | 0.486 | 0.479 | 7,714 | 7,714 | 0.719 | 0.515 | 0.535 | 0.658 | 0.207 | 0.560 | yes |
| this clone: db.jsonl | 85a977e3ed | 0.487 | 0.486 | 7,804 | 7,804 | 0.703 | 0.583 | 0.564 | 0.663 | 0.179 | 0.529 |  |
| this clone: db.jsonl | cda8cad59b | 0.496 | 0.492 | 7,949 | 7,949 | 0.741 | 0.581 | 0.541 | 0.658 | 0.195 | 0.600 |  |
| this clone: db.jsonl | 049e0c9c48 | 0.462 | 0.457 | 7,973 | 7,973 | 0.672 | 0.512 | 0.510 | 0.610 | 0.197 | 0.540 | yes |
| this clone: db.jsonl | 6827e42d47 | 0.455 | 0.451 | 8,352 | 8,352 | 0.654 | 0.508 | 0.521 | 0.588 | 0.192 | 0.534 | yes |
| this clone: db.jsonl | ff306b06c1 | 0.438 | 0.451 | 12,145 | 12,145 | 0.627 | 0.508 | 0.449 | 0.571 | 0.198 | 0.560 | yes |
| this clone: db.jsonl | 84a09433d4 | 0.439 | 0.435 | 12,585 | 12,585 | 0.626 | 0.541 | 0.434 | 0.564 | 0.196 | 0.558 |  |
| this clone: db.jsonl | ff3e6b2a34 | 0.440 | 0.438 | 13,073 | 13,073 | 0.631 | 0.554 | 0.441 | 0.552 | 0.194 | 0.567 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 595fc2b8f4 | 0.761 | 0.784 | 9,662 | 9,761 | 0.749 | 0.719 | 0.640 | 0.706 | 1.046 | 0.839 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 8cbc6dd05c | 0.727 | 0.742 | 9,694 | 9,809 | 0.729 | 0.770 | 0.614 | 0.673 | 0.874 | 0.821 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 6738aed13f | 0.767 | 0.755 | 9,694 | 9,793 | 0.776 | 0.699 | 0.636 | 0.715 | 1.074 | 0.852 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 312ad2edaa | 0.686 | 0.716 | 13,344 | 13,456 | 0.698 | 0.724 | 0.539 | 0.631 | 0.887 | 0.834 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 05617039f6 | 0.641 | 0.674 | 13,352 | 13,488 | 0.678 | 0.789 | 0.473 | 0.601 | 0.712 | 0.799 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 0b1d16def9 | 0.684 | 0.705 | 13,352 | 13,464 | 0.702 | 0.824 | 0.506 | 0.637 | 0.799 | 0.827 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 57a9dcc7cb | 0.731 | 0.680 | 13,368 | 13,480 | 0.700 | 0.887 | 0.542 | 0.648 | 0.957 | 0.906 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 32600cab87 | 0.687 | 0.662 | 13,528 | 13,656 | 0.680 | 0.987 | 0.523 | 0.625 | 0.697 | 0.849 |  |
| archived-20261004-200423: db-seed1.jsonl | 83cb81c383 | 0.838 | 0.705 | 9,662 | 9,761 | 0.770 | 1.006 | 0.686 | 0.735 | 1.058 | 0.925 |  |
| archived-20261004-200423: db-seed1.jsonl | 5b70f3dd64 | 0.763 | 0.649 | 9,694 | 9,801 | 0.725 | 0.964 | 0.627 | 0.683 | 0.866 | 0.817 |  |
| archived-20261004-200423: db-seed1.jsonl | a4e82e02e5 | 0.804 | 0.654 | 9,694 | 9,809 | 0.781 | 0.897 | 0.663 | 0.732 | 0.989 | 0.903 |  |
| archived-20261004-200423: db-seed1.jsonl | 53ec9bedde | 0.732 | 0.670 | 13,336 | 13,464 | 0.750 | 0.756 | 0.619 | 0.698 | 0.858 | 0.852 |  |
| archived-20261004-200423: db-seed1.jsonl | 448ef1ef43 | 0.695 | 0.620 | 13,368 | 13,488 | 0.683 | 0.970 | 0.503 | 0.607 | 0.800 | 0.859 |  |
| archived-20261004-200423: db-seed1.jsonl | 38d187239c | 0.698 | 0.609 | 13,368 | 13,480 | 0.710 | 0.846 | 0.545 | 0.640 | 0.790 | 0.830 |  |
| archived-20261004-200423: db-seed2.jsonl | 0ebf0445e0 | 0.772 | 0.667 | 9,662 | 9,761 | 0.798 | 0.692 | 0.692 | 0.740 | 0.970 | 0.872 |  |
| archived-20261004-200423: db-seed2.jsonl | c17103bf95 | 0.783 | 0.725 | 9,662 | 9,769 | 0.788 | 0.756 | 0.709 | 0.762 | 0.914 | 0.880 |  |
| archived-20261004-200423: db-seed2.jsonl | a285fa6ba3 | 0.738 | 0.666 | 13,352 | 13,464 | 0.761 | 0.704 | 0.630 | 0.701 | 0.927 | 0.883 |  |
| archived-20261004-200423: db-seed2.jsonl | 57e0e77c09 | 0.753 | 0.657 | 13,352 | 13,480 | 0.716 | 1.044 | 0.549 | 0.641 | 0.920 | 0.876 |  |
| archived-20261004-200423: db-seed2.jsonl | 9cd791dd84 | 0.759 | 0.619 | 13,368 | 13,472 | 0.742 | 0.894 | 0.566 | 0.668 | 1.007 | 0.864 |  |
| archived-20261004-200423: db.jsonl | 550df563ee | 0.745 | 0.696 | 9,646 | 9,745 | 0.701 | 0.787 | 0.623 | 0.679 | 0.981 | 0.853 |  |
| archived-20261004-200423: db.jsonl | f4a6dd9a13 | 0.731 | 0.683 | 9,662 | 9,761 | 0.747 | 0.662 | 0.621 | 0.701 | 0.972 | 0.787 |  |
| archived-20261004-200423: db.jsonl | 60753a0eb0 | 0.687 | 0.622 | 9,686 | 9,785 | 0.687 | 0.652 | 0.581 | 0.676 | 0.871 | 0.805 |  |
| archived-20261004-200423: db.jsonl | 8dd8a7a146 | 0.646 | 0.595 | 13,352 | 13,464 | 0.649 | 0.665 | 0.525 | 0.591 | 0.843 | 0.798 |  |
| archived-20261004-214724: db.jsonl | 3453246bdf | 0.745 | 0.727 | 9,335 | 9,335 | 0.756 | 0.688 | 0.662 | 0.736 | 0.902 | 0.881 |  |
| archived-20261004-214724: db.jsonl | 672538daf5 | 0.830 | 0.780 | 9,351 | 9,351 | 0.817 | 0.838 | 0.719 | 0.767 | 1.041 | 0.882 |  |
| archived-20261004-214724: db.jsonl | 7fe7f039bd | 0.731 | 0.702 | 9,450 | 9,450 | 0.761 | 0.717 | 0.644 | 0.707 | 0.838 | 0.874 |  |
| archived-20261004-214724: db.jsonl | 38d91795a2 | 0.715 | 0.678 | 9,474 | 9,474 | 0.756 | 0.653 | 0.617 | 0.718 | 0.852 | 0.872 |  |
| archived-20261004-214724: db.jsonl | 6463752a82 | 0.708 | 0.669 | 9,523 | 9,523 | 0.709 | 0.718 | 0.587 | 0.674 | 0.886 | 0.864 |  |
| archived-20261004-214724: db.jsonl | 90018981c6 | 0.777 | 0.696 | 9,678 | 9,678 | 0.745 | 0.831 | 0.639 | 0.710 | 1.007 | 0.864 |  |
| archived-20261004-214724: db.jsonl | e0cbf09bc2 | 0.703 | 0.666 | 13,057 | 13,057 | 0.692 | 0.762 | 0.534 | 0.642 | 0.950 | 0.888 |  |
| archived-20261004-214724: db.jsonl | 1769ca2a48 | 0.660 | 0.603 | 13,209 | 13,209 | 0.697 | 0.624 | 0.529 | 0.633 | 0.864 | 0.832 |  |
| archived-20261004-214724: db.jsonl | 14f6036a4b | 0.685 | 0.627 | 13,217 | 13,217 | 0.673 | 0.831 | 0.488 | 0.604 | 0.914 | 0.900 |  |
| archived-20261004-214724: db.jsonl | 29ad5ba726 | 0.649 | 0.589 | 13,352 | 13,352 | 0.642 | 0.759 | 0.493 | 0.591 | 0.810 | 0.831 |  |
| archived-20261004-214724: db.jsonl | 12d8e18511 | 0.707 | 0.667 | 13,360 | 13,360 | 0.677 | 0.858 | 0.531 | 0.621 | 0.921 | 0.934 |  |
| archived-20261005-013645: db.jsonl | 05dcc81cdc | 0.744 | 0.688 | 9,335 | 9,335 | 0.731 | 0.809 | 0.608 | 0.695 | 0.911 | 0.897 |  |
| archived-20261005-013645: db.jsonl | c297551359 | 0.708 | 0.682 | 9,450 | 9,450 | 0.733 | 0.661 | 0.641 | 0.693 | 0.826 | 0.878 |  |
| archived-20261005-013645: db.jsonl | e8f1dd3ca2 | 0.730 | 0.678 | 9,458 | 9,458 | 0.697 | 0.811 | 0.577 | 0.660 | 0.960 | 0.894 |  |
| archived-20261005-013645: db.jsonl | 66eb4a8f15 | 0.686 | 0.641 | 13,057 | 13,057 | 0.705 | 0.690 | 0.532 | 0.642 | 0.914 | 0.876 |  |
| archived-20261005-013645: db.jsonl | 84e302c470 | 0.730 | 0.657 | 13,065 | 13,065 | 0.727 | 0.754 | 0.557 | 0.668 | 1.016 | 0.895 |  |
| archived-20261005-013645: db.jsonl | 4cb3fa9172 | 0.688 | 0.626 | 13,073 | 13,073 | 0.663 | 0.810 | 0.496 | 0.595 | 0.975 | 0.890 |  |
| archived-20261005-013645: db.jsonl | e99da68667 | 0.657 | 0.581 | 13,201 | 13,201 | 0.635 | 0.779 | 0.446 | 0.559 | 0.988 | 0.859 |  |
| archived-20261005-042924: db.jsonl | 98736f0596 | 0.775 | 0.731 | 9,335 | 9,335 | 0.779 | 0.734 | 0.672 | 0.734 | 0.994 | 0.903 |  |
| archived-20261005-042924: db.jsonl | 4f010d8ab9 | 0.763 | 0.721 | 9,343 | 9,343 | 0.759 | 0.727 | 0.653 | 0.712 | 1.010 | 0.905 |  |
| archived-20261005-042924: db.jsonl | 4032a5ce71 | 0.757 | 0.698 | 9,351 | 9,351 | 0.752 | 0.807 | 0.609 | 0.705 | 0.956 | 0.929 |  |
| archived-20261005-042924: db.jsonl | 528fc9619a | 0.751 | 0.702 | 9,359 | 9,359 | 0.751 | 0.740 | 0.617 | 0.704 | 0.987 | 0.892 |  |
| archived-20261005-042924: db.jsonl | f052397620 | 0.725 | 0.685 | 9,450 | 9,450 | 0.725 | 0.794 | 0.568 | 0.681 | 0.898 | 0.903 |  |
| archived-20261005-042924: db.jsonl | 8dc0f97f2c | 0.723 | 0.680 | 9,458 | 9,458 | 0.713 | 0.766 | 0.577 | 0.676 | 0.925 | 0.888 |  |
| archived-20261005-042924: db.jsonl | 52b80007a1 | 0.706 | 0.640 | 10,010 | 10,010 | 0.738 | 0.574 | 0.600 | 0.693 | 0.992 | 0.858 |  |
| archived-20261005-042924: db.jsonl | 5ed1ed8715 | 0.712 | 0.642 | 10,018 | 10,018 | 0.758 | 0.546 | 0.628 | 0.699 | 1.009 | 0.859 |  |
| archived-20261005-042924: db.jsonl | 9e50623ac1 | 0.662 | 0.593 | 13,073 | 13,073 | 0.664 | 0.699 | 0.496 | 0.605 | 0.913 | 0.849 |  |
| archived-20261005-042924: db.jsonl | 22b81e50c4 | 0.659 | 0.605 | 13,209 | 13,209 | 0.647 | 0.874 | 0.421 | 0.560 | 0.930 | 0.887 |  |
| archived-20261005-042924: db.jsonl | 2db525ff95 | 0.647 | 0.579 | 14,017 | 14,017 | 0.642 | 0.704 | 0.447 | 0.590 | 0.954 | 0.910 |  |
| archived-20261005-131253: db.jsonl | 422d6bcbca | 0.731 | 0.699 | 9,327 | 9,327 | 0.737 | 0.843 | 0.543 | 0.651 | 0.950 | 0.866 |  |
| archived-20261005-131253: db.jsonl | 090672993b | 0.740 | 0.700 | 9,335 | 9,335 | 0.713 | 0.826 | 0.633 | 0.680 | 0.874 | 0.768 |  |
| archived-20261005-131253: db.jsonl | 6495dcb5dd | 0.698 | 0.662 | 9,343 | 9,343 | 0.663 | 0.938 | 0.515 | 0.631 | 0.818 | 0.815 |  |
| archived-20261005-131253: db.jsonl | c40ba92d5b | 0.671 | 0.630 | 9,511 | 9,511 | 0.678 | 0.685 | 0.575 | 0.628 | 0.813 | 0.793 |  |
| archived-20261005-131253: db.jsonl | ca2ac63866 | 0.682 | 0.634 | 9,531 | 9,531 | 0.659 | 0.730 | 0.552 | 0.617 | 0.900 | 0.868 |  |
| archived-20261005-131253: db.jsonl | c61857fc89 | 0.657 | 0.633 | 10,034 | 10,034 | 0.689 | 0.710 | 0.531 | 0.638 | 0.741 | 0.851 |  |
| archived-20261005-131253: db.jsonl | b06a4cf784 | 0.658 | 0.615 | 10,246 | 10,246 | 0.634 | 0.703 | 0.524 | 0.612 | 0.864 | 0.833 |  |
| archived-20261005-131253: db.jsonl | af5e8dc29f | 0.665 | 0.604 | 10,254 | 10,254 | 0.659 | 0.669 | 0.543 | 0.611 | 0.886 | 0.845 |  |
| archived-20261005-131253: db.jsonl | a74b828e9b | 0.664 | 0.608 | 13,073 | 13,073 | 0.680 | 0.634 | 0.506 | 0.610 | 0.973 | 0.839 |  |
| archived-20261005-131253: db.jsonl | dc02ceae31 | 0.608 | 0.560 | 13,161 | 13,161 | 0.621 | 0.738 | 0.425 | 0.545 | 0.783 | 0.841 |  |
| archived-20261005-131253: db.jsonl | 15dde12f04 | 0.597 | 0.567 | 13,345 | 13,345 | 0.625 | 0.754 | 0.389 | 0.538 | 0.771 | 0.818 |  |
| archived-20261005-131253: db.jsonl | cd943ed219 | 0.588 | 0.545 | 14,081 | 14,081 | 0.621 | 0.662 | 0.401 | 0.542 | 0.787 | 0.833 |  |
| archived-20261005-144844: db.jsonl | 49b0a93f14 | 0.701 | 0.688 | 8,073 | 8,073 | 0.719 | 0.900 | 0.554 | 0.659 | 0.715 | 0.818 |  |
| archived-20261005-144844: db.jsonl | 9f5e6d173c | 0.694 | 0.650 | 8,074 | 8,074 | 0.674 | 0.897 | 0.527 | 0.611 | 0.827 | 0.815 |  |
| archived-20261005-144844: db.jsonl | f060a4c31f | 0.684 | 0.637 | 8,289 | 8,289 | 0.651 | 0.845 | 0.528 | 0.595 | 0.869 | 0.789 |  |
| archived-20261005-144844: db.jsonl | a306cc61fb | 0.672 | 0.615 | 8,305 | 8,305 | 0.675 | 0.645 | 0.540 | 0.606 | 0.957 | 0.810 |  |
| archived-20261005-144844: db.jsonl | 3c2d8a577b | 0.656 | 0.603 | 8,306 | 8,306 | 0.678 | 0.637 | 0.532 | 0.607 | 0.874 | 0.799 |  |
| archived-20261005-144844: db.jsonl | 4cc12fc1e7 | 0.628 | 0.561 | 8,957 | 8,957 | 0.629 | 0.558 | 0.503 | 0.594 | 0.930 | 0.758 |  |
| archived-20261005-144844: db.jsonl | 3a7c3d6e90 | 0.610 | 0.551 | 11,777 | 11,777 | 0.616 | 0.865 | 0.363 | 0.530 | 0.828 | 0.857 |  |
| archived-20261005-144844: db.jsonl | 2b00aa6e97 | 0.608 | 0.568 | 12,145 | 12,145 | 0.600 | 0.865 | 0.362 | 0.518 | 0.854 | 0.875 |  |
| archived-20261005-144844: db.jsonl | 27a35df3fa | 0.629 | 0.570 | 12,312 | 12,312 | 0.643 | 0.583 | 0.483 | 0.583 | 0.932 | 0.783 |  |
| archived-20261005-144844: db.jsonl | ff39b37bcc | 0.634 | 0.572 | 12,584 | 12,584 | 0.633 | 0.631 | 0.461 | 0.572 | 0.969 | 0.840 |  |
| archived-20261005-144844: db.jsonl | 1cf03a8fd4 | 0.605 | 0.545 | 12,608 | 12,608 | 0.598 | 0.679 | 0.400 | 0.545 | 0.912 | 0.819 |  |
| archived-20261005-144844: db.jsonl | a214fa731c | 0.601 | 0.557 | 12,664 | 12,664 | 0.645 | 0.615 | 0.452 | 0.572 | 0.766 | 0.770 |  |
| archived-20261005-164554: db.jsonl | f41ab1810d | 1.008 | 1.008 | 8,034 | 8,034 | 1.038 | 1.250 | 0.789 | 0.932 | 1.090 | 1.148 |  |
| archived-20261005-164554: db.jsonl | 3781c5e756 | 0.759 | 0.758 | 8,041 | 8,041 | 0.767 | 0.941 | 0.594 | 0.696 | 0.841 | 0.867 |  |
| archived-20261005-164554: db.jsonl | d4739aac88 | 0.722 | 0.723 | 8,042 | 8,042 | 0.789 | 0.718 | 0.639 | 0.731 | 0.745 | 0.879 |  |
| archived-20261005-164554: db.jsonl | e05adba602 | 0.696 | 0.687 | 8,082 | 8,082 | 0.730 | 0.779 | 0.538 | 0.670 | 0.799 | 0.808 |  |
| archived-20261005-164554: db.jsonl | bb8a0cb575 | 0.699 | 0.688 | 8,099 | 8,099 | 0.761 | 0.784 | 0.544 | 0.695 | 0.738 | 0.843 |  |
| archived-20261005-164554: db.jsonl | a27aa49d8e | 0.699 | 0.693 | 8,163 | 8,163 | 0.683 | 0.858 | 0.523 | 0.610 | 0.890 | 0.848 |  |
| archived-20261005-164554: db.jsonl | 8a2189b3b6 | 0.664 | 0.646 | 8,171 | 8,171 | 0.679 | 0.763 | 0.528 | 0.613 | 0.766 | 0.851 |  |
| archived-20261005-164554: db.jsonl | f66d74a27c | 0.687 | 0.682 | 8,210 | 8,210 | 0.690 | 0.875 | 0.515 | 0.640 | 0.771 | 0.834 |  |
| archived-20261005-164554: db.jsonl | be02a4c0cf | 0.551 | 0.533 | 8,525 | 8,525 | 0.781 | 0.771 | 0.612 | 0.706 | 0.195 | 0.605 |  |
| archived-20261005-164554: db.jsonl | caf4358de8 | 0.542 | 0.514 | 8,540 | 8,540 | 0.769 | 0.774 | 0.602 | 0.690 | 0.189 | 0.629 |  |
| archived-20261005-164554: db.jsonl | 6578fc6928 | 0.527 | 0.515 | 8,548 | 8,548 | 0.707 | 0.763 | 0.522 | 0.634 | 0.228 | 0.594 |  |
| archived-20261005-164554: db.jsonl | 3d31fd4cc4 | 0.522 | 0.502 | 8,550 | 8,550 | 0.700 | 0.849 | 0.520 | 0.617 | 0.204 | 0.644 |  |
| archived-20261005-164554: db.jsonl | 85cac726b5 | 0.508 | 0.484 | 8,614 | 8,614 | 0.649 | 0.863 | 0.531 | 0.604 | 0.189 | 0.605 |  |
| archived-20261005-164554: db.jsonl | f85a63f8c7 | 0.503 | 0.481 | 8,647 | 8,647 | 0.646 | 0.852 | 0.528 | 0.601 | 0.185 | 0.631 |  |
| archived-20261005-164554: db.jsonl | 51879a71f0 | 0.512 | 0.513 | 8,664 | 8,664 | 0.689 | 0.747 | 0.563 | 0.638 | 0.190 | 0.653 |  |
| archived-20261005-164554: db.jsonl | 1b602bc9bd | 0.496 | 0.478 | 8,671 | 8,671 | 0.666 | 0.793 | 0.491 | 0.609 | 0.190 | 0.588 |  |
| archived-20261005-164554: db.jsonl | 72ca2cf497 | 0.484 | 0.469 | 8,990 | 8,990 | 0.660 | 0.671 | 0.512 | 0.595 | 0.197 | 0.507 |  |
| archived-20261005-164554: db.jsonl | 959e88b0f5 | 0.473 | 0.458 | 9,140 | 9,140 | 0.686 | 0.543 | 0.518 | 0.629 | 0.195 | 0.525 |  |
| archived-20261005-164554: db.jsonl | 577c999e62 | 0.463 | 0.443 | 9,278 | 9,278 | 0.655 | 0.554 | 0.507 | 0.608 | 0.190 | 0.529 |  |
| archived-20261005-164554: db.jsonl | aba06380d6 | 0.487 | 0.462 | 12,353 | 12,353 | 0.655 | 0.765 | 0.491 | 0.593 | 0.188 | 0.642 |  |
| archived-20261005-164554: db.jsonl | 0212f86508 | 0.478 | 0.453 | 12,377 | 12,377 | 0.641 | 0.795 | 0.448 | 0.558 | 0.196 | 0.627 |  |
| archived-20261005-164554: db.jsonl | 9bb527944a | 0.436 | 0.430 | 13,073 | 13,073 | 0.613 | 0.555 | 0.430 | 0.562 | 0.193 | 0.549 | yes |
| archived-20261005-175214: db.jsonl | c513ef17b0 | 0.793 | 0.781 | 7,019 | 7,019 | 0.847 | 0.769 | 0.629 | 0.760 | 1.006 | 0.864 |  |
| archived-20261005-175214: db.jsonl | 57d12a1bb0 | 0.760 | 0.756 | 7,020 | 7,020 | 0.768 | 0.918 | 0.604 | 0.718 | 0.831 | 0.858 |  |
| archived-20261005-175214: db.jsonl | ee4d8f8a50 | 0.725 | 0.723 | 7,027 | 7,027 | 0.789 | 0.753 | 0.617 | 0.708 | 0.773 | 0.851 |  |
| archived-20261005-175214: db.jsonl | ccce4784b8 | 0.689 | 0.681 | 7,091 | 7,091 | 0.739 | 0.719 | 0.606 | 0.701 | 0.687 | 0.844 |  |
| archived-20261005-175214: db.jsonl | 88792f1798 | 0.661 | 0.653 | 7,220 | 7,220 | 0.694 | 0.753 | 0.552 | 0.640 | 0.685 | 0.839 |  |
| archived-20261005-175214: db.jsonl | 2367cb920c | 0.543 | 0.538 | 7,510 | 7,510 | 0.748 | 0.805 | 0.608 | 0.683 | 0.190 | 0.610 |  |
| archived-20261005-175214: db.jsonl | 853cfb9d36 | 0.552 | 0.536 | 7,651 | 7,651 | 0.752 | 0.809 | 0.633 | 0.703 | 0.190 | 0.636 |  |
| archived-20261005-175214: db.jsonl | fa23f401cd | 0.537 | 0.525 | 7,692 | 7,692 | 0.695 | 0.868 | 0.598 | 0.656 | 0.188 | 0.648 |  |
| archived-20261005-175214: db.jsonl | 45d2ff7e01 | 0.512 | 0.500 | 7,725 | 7,725 | 0.701 | 0.723 | 0.558 | 0.639 | 0.194 | 0.648 |  |
| archived-20261005-175214: db.jsonl | f084674b22 | 0.511 | 0.516 | 9,198 | 9,198 | 0.704 | 0.718 | 0.568 | 0.649 | 0.188 | 0.642 |  |
| archived-20261005-175214: db.jsonl | 9d89f6ba0e | 0.493 | 0.487 | 13,065 | 13,065 | 0.671 | 0.779 | 0.503 | 0.594 | 0.186 | 0.682 |  |

The front of all runs together, by size: 9bb527944a 0.436 at 13,073, ff306b06c1 0.438 at 12,145, 6827e42d47 0.455 at 8,352, 049e0c9c48 0.462 at 7,973, 7a8d429413 0.486 at 7,714, 96f2d8bfd7 0.486 at 7,236, 641b85143d 0.507 at 7,178, 2ed8b1583e 0.509 at 7,129, f3988ea716 0.517 at 7,113, d8d62beb78 0.555 at 7,106, 5df0608416 0.657 at 7,059, 7380e8bcb1 0.661 at 7,050, bf413bef91 0.668 at 7,002, 9385a8fcbb 0.697 at 6,994, 82e7e4dc0d 0.729 at 6,979, 295a6acd98 0.760 at 6,977

## The same session on two CPUs

Calibration on cpu 2: 1.004; on cpu 8: 1.003.

Speed on cpu 2 over speed on cpu 8, per design: median 1.001, 10-90% 0.992-1.009, extremes 0.983-1.017; rank agreement (Spearman) 1.00.

The front of all runs on cpu 2: 9bb527944a 0.436 at 13,073, ff306b06c1 0.438 at 12,145, 6827e42d47 0.455 at 8,352, 049e0c9c48 0.462 at 7,973, 7a8d429413 0.486 at 7,714, 96f2d8bfd7 0.486 at 7,236, 641b85143d 0.507 at 7,178, 2ed8b1583e 0.509 at 7,129, f3988ea716 0.517 at 7,113, d8d62beb78 0.555 at 7,106, 5df0608416 0.657 at 7,059, 7380e8bcb1 0.661 at 7,050, bf413bef91 0.668 at 7,002, 9385a8fcbb 0.697 at 6,994, 82e7e4dc0d 0.729 at 6,979, 295a6acd98 0.760 at 6,977

The front of all runs on cpu 8: ff306b06c1 0.436 at 12,145, 049e0c9c48 0.459 at 7,973, 7a8d429413 0.478 at 7,714, 96f2d8bfd7 0.488 at 7,236, 641b85143d 0.499 at 7,178, 2ed8b1583e 0.513 at 7,129, f3988ea716 0.520 at 7,113, d8d62beb78 0.548 at 7,106, 7380e8bcb1 0.661 at 7,050, bf413bef91 0.672 at 7,002, 9385a8fcbb 0.694 at 6,994, 82e7e4dc0d 0.730 at 6,979, 295a6acd98 0.760 at 6,977

On both fronts: 13 of 16 and 13.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| 9bb527944a | 0.436 | 0.438 | 0.995 |
| ff306b06c1 | 0.438 | 0.436 | 1.005 |
| 84a09433d4 | 0.439 | 0.439 | 0.999 |
| ff3e6b2a34 | 0.440 | 0.440 | 1.002 |
| 6827e42d47 | 0.455 | 0.460 | 0.989 |
| 049e0c9c48 | 0.462 | 0.459 | 1.007 |
| 577c999e62 | 0.463 | 0.464 | 0.997 |
| 959e88b0f5 | 0.473 | 0.466 | 1.015 |
| 0212f86508 | 0.478 | 0.471 | 1.015 |
| 72ca2cf497 | 0.484 | 0.484 | 1.001 |
| 7a8d429413 | 0.486 | 0.478 | 1.016 |
| 96f2d8bfd7 | 0.486 | 0.488 | 0.997 |
| 85a977e3ed | 0.487 | 0.491 | 0.992 |
| aba06380d6 | 0.487 | 0.489 | 0.996 |
| 9d89f6ba0e | 0.493 | 0.497 | 0.992 |
| cda8cad59b | 0.496 | 0.488 | 1.017 |
| 1b602bc9bd | 0.496 | 0.493 | 1.007 |
| 55ca1dfdb5 | 0.501 | 0.497 | 1.009 |
| f85a63f8c7 | 0.503 | 0.503 | 1.000 |
| 0e8b212e50 | 0.506 | 0.504 | 1.003 |
| 641b85143d | 0.507 | 0.499 | 1.015 |
| 85cac726b5 | 0.508 | 0.504 | 1.008 |
| 2ed8b1583e | 0.509 | 0.513 | 0.993 |
| f084674b22 | 0.511 | 0.519 | 0.985 |
| 45d2ff7e01 | 0.512 | 0.505 | 1.013 |
| 51879a71f0 | 0.512 | 0.515 | 0.995 |
| f3988ea716 | 0.517 | 0.520 | 0.995 |
| 3d31fd4cc4 | 0.522 | 0.522 | 1.000 |
| 6578fc6928 | 0.527 | 0.533 | 0.989 |
| fa23f401cd | 0.537 | 0.537 | 0.999 |
| caf4358de8 | 0.542 | 0.541 | 1.002 |
| 2367cb920c | 0.543 | 0.544 | 0.999 |
| be02a4c0cf | 0.551 | 0.545 | 1.011 |
| 853cfb9d36 | 0.552 | 0.544 | 1.015 |
| d8d62beb78 | 0.555 | 0.548 | 1.011 |
| cd943ed219 | 0.588 | 0.591 | 0.995 |
| 15dde12f04 | 0.597 | 0.599 | 0.997 |
| a214fa731c | 0.601 | 0.597 | 1.007 |
| 1cf03a8fd4 | 0.605 | 0.605 | 1.000 |
| 2b00aa6e97 | 0.608 | 0.607 | 1.002 |
| dc02ceae31 | 0.608 | 0.608 | 1.001 |
| 3a7c3d6e90 | 0.610 | 0.609 | 1.002 |
| 4cc12fc1e7 | 0.628 | 0.624 | 1.007 |
| 27a35df3fa | 0.629 | 0.630 | 0.999 |
| ff39b37bcc | 0.634 | 0.633 | 1.001 |
| 05617039f6 | 0.641 | 0.645 | 0.995 |
| 8dd8a7a146 | 0.646 | 0.646 | 1.001 |
| 2db525ff95 | 0.647 | 0.649 | 0.997 |
| 29ad5ba726 | 0.649 | 0.646 | 1.005 |
| 3c2d8a577b | 0.656 | 0.659 | 0.996 |
| e99da68667 | 0.657 | 0.651 | 1.009 |
| 5df0608416 | 0.657 | 0.661 | 0.993 |
| c61857fc89 | 0.657 | 0.655 | 1.004 |
| b06a4cf784 | 0.658 | 0.658 | 1.000 |
| 22b81e50c4 | 0.659 | 0.660 | 0.999 |
| 1769ca2a48 | 0.660 | 0.663 | 0.996 |
| 7380e8bcb1 | 0.661 | 0.661 | 1.000 |
| 88792f1798 | 0.661 | 0.663 | 0.998 |
| 9e50623ac1 | 0.662 | 0.659 | 1.005 |
| 8a2189b3b6 | 0.664 | 0.658 | 1.009 |
| a74b828e9b | 0.664 | 0.670 | 0.991 |
| af5e8dc29f | 0.665 | 0.668 | 0.995 |
| bf413bef91 | 0.668 | 0.672 | 0.993 |
| c25a5e1714 | 0.671 | 0.672 | 0.999 |
| c40ba92d5b | 0.671 | 0.663 | 1.013 |
| a306cc61fb | 0.672 | 0.679 | 0.989 |
| ca2ac63866 | 0.682 | 0.683 | 0.998 |
| 0b1d16def9 | 0.684 | 0.674 | 1.014 |
| f060a4c31f | 0.684 | 0.680 | 1.007 |
| 14f6036a4b | 0.685 | 0.678 | 1.010 |
| 66eb4a8f15 | 0.686 | 0.684 | 1.003 |
| 312ad2edaa | 0.686 | 0.686 | 1.001 |
| 32600cab87 | 0.687 | 0.685 | 1.002 |
| 60753a0eb0 | 0.687 | 0.690 | 0.995 |
| f66d74a27c | 0.687 | 0.688 | 0.999 |
| 4cb3fa9172 | 0.688 | 0.682 | 1.009 |
| ccce4784b8 | 0.689 | 0.687 | 1.002 |
| 9f5e6d173c | 0.694 | 0.690 | 1.005 |
| 448ef1ef43 | 0.695 | 0.700 | 0.992 |
| e05adba602 | 0.696 | 0.694 | 1.004 |
| 9385a8fcbb | 0.697 | 0.694 | 1.004 |
| 38d187239c | 0.698 | 0.694 | 1.006 |
| 6495dcb5dd | 0.698 | 0.694 | 1.006 |
| a27aa49d8e | 0.699 | 0.702 | 0.995 |
| bb8a0cb575 | 0.699 | 0.696 | 1.004 |
| 49b0a93f14 | 0.701 | 0.698 | 1.004 |
| e0cbf09bc2 | 0.703 | 0.699 | 1.005 |
| 52b80007a1 | 0.706 | 0.701 | 1.007 |
| 12d8e18511 | 0.707 | 0.710 | 0.995 |
| c297551359 | 0.708 | 0.713 | 0.992 |
| 6463752a82 | 0.708 | 0.706 | 1.004 |
| 5ed1ed8715 | 0.712 | 0.713 | 0.998 |
| 38d91795a2 | 0.715 | 0.712 | 1.004 |
| d4739aac88 | 0.722 | 0.723 | 0.999 |
| 8dc0f97f2c | 0.723 | 0.724 | 0.998 |
| f052397620 | 0.725 | 0.728 | 0.996 |
| ee4d8f8a50 | 0.725 | 0.714 | 1.015 |
| 8cbc6dd05c | 0.727 | 0.727 | 1.000 |
| 82e7e4dc0d | 0.729 | 0.730 | 0.998 |
| e8f1dd3ca2 | 0.730 | 0.734 | 0.994 |
| 84e302c470 | 0.730 | 0.728 | 1.002 |
| 7fe7f039bd | 0.731 | 0.725 | 1.008 |
| 57a9dcc7cb | 0.731 | 0.730 | 1.002 |
| 422d6bcbca | 0.731 | 0.738 | 0.990 |
| f4a6dd9a13 | 0.731 | 0.732 | 0.999 |
| 53ec9bedde | 0.732 | 0.728 | 1.005 |
| a285fa6ba3 | 0.738 | 0.733 | 1.007 |
| 090672993b | 0.740 | 0.739 | 1.001 |
| 05dcc81cdc | 0.744 | 0.744 | 1.000 |
| 3453246bdf | 0.745 | 0.753 | 0.988 |
| 550df563ee | 0.745 | 0.741 | 1.005 |
| 528fc9619a | 0.751 | 0.763 | 0.983 |
| 57e0e77c09 | 0.753 | 0.753 | 1.000 |
| 4032a5ce71 | 0.757 | 0.755 | 1.003 |
| 3781c5e756 | 0.759 | 0.762 | 0.995 |
| 9cd791dd84 | 0.759 | 0.761 | 0.998 |
| 295a6acd98 | 0.760 | 0.760 | 0.999 |
| 57d12a1bb0 | 0.760 | 0.760 | 1.001 |
| 595fc2b8f4 | 0.761 | 0.761 | 0.999 |
| 4f010d8ab9 | 0.763 | 0.768 | 0.994 |
| 5b70f3dd64 | 0.763 | 0.771 | 0.991 |
| 6738aed13f | 0.767 | 0.763 | 1.005 |
| 0ebf0445e0 | 0.772 | 0.776 | 0.995 |
| 98736f0596 | 0.775 | 0.784 | 0.989 |
| 90018981c6 | 0.777 | 0.776 | 1.002 |
| c17103bf95 | 0.783 | 0.787 | 0.995 |
| c513ef17b0 | 0.793 | 0.789 | 1.005 |
| a4e82e02e5 | 0.804 | 0.797 | 1.009 |
| 672538daf5 | 0.830 | 0.830 | 0.999 |
| 83cb81c383 | 0.838 | 0.838 | 1.001 |
| f41ab1810d | 1.008 | 0.999 | 1.009 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 9 - Iteration 52: seeds 1-11, after seed 11 (the Forth sources' batch)

`seed 11 then experiment compare-fronts.py --rounds 10 --cpus 2,8`, commit
557bd718: thirteen databases, 144 front designs, five workloads, sieve
held out. Sixteen minutes. **Calibration 1.007** (fib 1.023, the rest
0.994-1.016). The CPUs agree: per design median 1.003, 10-90% 0.994-1.013,
ranks 1.00; 11 of 11 designs on both CPUs' fronts.

**The front of all runs: seed 11's eleven**, 6,971 bytes (0.727) to 8,030
(0.413, the fastest yet); seed 8's 0.436 at 13,073 off it.

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 1.007** (kernel 1.003, fib 1.023, parse 0.994, corpus 0.998, loop 1.016, sieve 0.999).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 7cb20d14b1 | 0.727 | 0.718 | 6,971 | 6,971 | 0.792 | 0.755 | 0.583 | 0.716 | 0.814 | 0.891 | yes |
| this clone: db.jsonl | d0d304e240 | 0.691 | 0.684 | 6,977 | 6,977 | 0.705 | 0.803 | 0.517 | 0.644 | 0.834 | 0.841 | yes |
| this clone: db.jsonl | 98e6135b93 | 0.677 | 0.678 | 6,978 | 6,978 | 0.663 | 0.758 | 0.508 | 0.618 | 0.899 | 0.866 | yes |
| this clone: db.jsonl | 6ba318d95c | 0.605 | 0.601 | 6,989 | 6,989 | 0.609 | 0.736 | 0.427 | 0.521 | 0.814 | 0.840 | yes |
| this clone: db.jsonl | 7b9675c9ef | 0.606 | 0.604 | 7,004 | 7,004 | 0.623 | 0.738 | 0.443 | 0.550 | 0.728 | 0.805 |  |
| this clone: db.jsonl | 31a3ceea45 | 0.591 | 0.582 | 7,037 | 7,037 | 0.587 | 0.746 | 0.434 | 0.526 | 0.721 | 0.797 | yes |
| this clone: db.jsonl | 3f1d365b3b | 0.597 | 0.590 | 7,061 | 7,061 | 0.599 | 0.708 | 0.432 | 0.526 | 0.784 | 0.824 |  |
| this clone: db.jsonl | 63919635b7 | 0.507 | 0.502 | 7,089 | 7,089 | 0.688 | 0.700 | 0.516 | 0.610 | 0.222 | 0.586 | yes |
| this clone: db.jsonl | 2c9b948725 | 0.485 | 0.481 | 7,097 | 7,097 | 0.613 | 0.964 | 0.444 | 0.509 | 0.200 | 0.664 | yes |
| this clone: db.jsonl | cac62ca533 | 0.459 | 0.450 | 7,105 | 7,105 | 0.590 | 0.850 | 0.426 | 0.516 | 0.186 | 0.616 | yes |
| this clone: db.jsonl | 627568164d | 0.444 | 0.447 | 7,147 | 7,147 | 0.604 | 0.710 | 0.412 | 0.510 | 0.191 | 0.673 | yes |
| this clone: db.jsonl | 37b502fac7 | 0.433 | 0.433 | 7,238 | 7,238 | 0.576 | 0.704 | 0.404 | 0.494 | 0.188 | 0.576 | yes |
| this clone: db.jsonl | ced47e8cfa | 0.413 | 0.406 | 8,030 | 8,030 | 0.600 | 0.479 | 0.417 | 0.521 | 0.193 | 0.567 | yes |
| archived-20261004-200423: db-rehearsal.jsonl | 595fc2b8f4 | 0.762 | 0.784 | 9,662 | 9,761 | 0.742 | 0.722 | 0.657 | 0.701 | 1.042 | 0.828 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 8cbc6dd05c | 0.727 | 0.742 | 9,694 | 9,809 | 0.725 | 0.779 | 0.612 | 0.681 | 0.861 | 0.795 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 6738aed13f | 0.762 | 0.755 | 9,694 | 9,793 | 0.757 | 0.697 | 0.634 | 0.711 | 1.080 | 0.863 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 312ad2edaa | 0.685 | 0.716 | 13,344 | 13,456 | 0.673 | 0.725 | 0.553 | 0.630 | 0.889 | 0.862 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 05617039f6 | 0.638 | 0.674 | 13,352 | 13,488 | 0.662 | 0.801 | 0.477 | 0.595 | 0.702 | 0.816 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 0b1d16def9 | 0.679 | 0.705 | 13,352 | 13,464 | 0.709 | 0.824 | 0.495 | 0.626 | 0.800 | 0.857 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 57a9dcc7cb | 0.734 | 0.680 | 13,368 | 13,480 | 0.717 | 0.912 | 0.539 | 0.635 | 0.954 | 0.908 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 32600cab87 | 0.676 | 0.662 | 13,528 | 13,656 | 0.670 | 0.968 | 0.516 | 0.608 | 0.691 | 0.849 |  |
| archived-20261004-200423: db-seed1.jsonl | 83cb81c383 | 0.840 | 0.705 | 9,662 | 9,761 | 0.785 | 0.993 | 0.691 | 0.742 | 1.050 | 0.929 |  |
| archived-20261004-200423: db-seed1.jsonl | 5b70f3dd64 | 0.769 | 0.649 | 9,694 | 9,801 | 0.742 | 0.947 | 0.632 | 0.695 | 0.871 | 0.821 |  |
| archived-20261004-200423: db-seed1.jsonl | a4e82e02e5 | 0.794 | 0.654 | 9,694 | 9,809 | 0.782 | 0.874 | 0.649 | 0.725 | 0.982 | 0.927 |  |
| archived-20261004-200423: db-seed1.jsonl | 53ec9bedde | 0.730 | 0.670 | 13,336 | 13,464 | 0.749 | 0.775 | 0.613 | 0.684 | 0.850 | 0.836 |  |
| archived-20261004-200423: db-seed1.jsonl | 448ef1ef43 | 0.687 | 0.620 | 13,368 | 13,488 | 0.669 | 0.947 | 0.498 | 0.610 | 0.798 | 0.853 |  |
| archived-20261004-200423: db-seed1.jsonl | 38d187239c | 0.691 | 0.609 | 13,368 | 13,480 | 0.707 | 0.835 | 0.545 | 0.629 | 0.780 | 0.831 |  |
| archived-20261004-200423: db-seed2.jsonl | 0ebf0445e0 | 0.770 | 0.667 | 9,662 | 9,761 | 0.782 | 0.694 | 0.686 | 0.741 | 0.978 | 0.876 |  |
| archived-20261004-200423: db-seed2.jsonl | c17103bf95 | 0.779 | 0.725 | 9,662 | 9,769 | 0.797 | 0.738 | 0.703 | 0.760 | 0.910 | 0.888 |  |
| archived-20261004-200423: db-seed2.jsonl | a285fa6ba3 | 0.737 | 0.666 | 13,352 | 13,464 | 0.763 | 0.703 | 0.623 | 0.700 | 0.929 | 0.859 |  |
| archived-20261004-200423: db-seed2.jsonl | 57e0e77c09 | 0.746 | 0.657 | 13,352 | 13,480 | 0.701 | 1.036 | 0.539 | 0.637 | 0.924 | 0.885 |  |
| archived-20261004-200423: db-seed2.jsonl | 9cd791dd84 | 0.757 | 0.619 | 13,368 | 13,472 | 0.733 | 0.867 | 0.578 | 0.680 | 0.994 | 0.889 |  |
| archived-20261004-200423: db.jsonl | 550df563ee | 0.729 | 0.696 | 9,646 | 9,745 | 0.696 | 0.748 | 0.610 | 0.667 | 0.974 | 0.842 |  |
| archived-20261004-200423: db.jsonl | f4a6dd9a13 | 0.727 | 0.683 | 9,662 | 9,761 | 0.732 | 0.665 | 0.614 | 0.700 | 0.974 | 0.795 |  |
| archived-20261004-200423: db.jsonl | 60753a0eb0 | 0.692 | 0.622 | 9,686 | 9,785 | 0.705 | 0.652 | 0.579 | 0.665 | 0.897 | 0.778 |  |
| archived-20261004-200423: db.jsonl | 8dd8a7a146 | 0.653 | 0.595 | 13,352 | 13,464 | 0.668 | 0.663 | 0.524 | 0.592 | 0.862 | 0.796 |  |
| archived-20261004-214724: db.jsonl | 3453246bdf | 0.752 | 0.727 | 9,335 | 9,335 | 0.762 | 0.688 | 0.683 | 0.739 | 0.908 | 0.867 |  |
| archived-20261004-214724: db.jsonl | 672538daf5 | 0.834 | 0.780 | 9,351 | 9,351 | 0.806 | 0.865 | 0.701 | 0.793 | 1.040 | 0.877 |  |
| archived-20261004-214724: db.jsonl | 7fe7f039bd | 0.719 | 0.702 | 9,450 | 9,450 | 0.759 | 0.700 | 0.611 | 0.698 | 0.849 | 0.889 |  |
| archived-20261004-214724: db.jsonl | 38d91795a2 | 0.715 | 0.678 | 9,474 | 9,474 | 0.750 | 0.653 | 0.619 | 0.715 | 0.863 | 0.861 |  |
| archived-20261004-214724: db.jsonl | 6463752a82 | 0.704 | 0.669 | 9,523 | 9,523 | 0.703 | 0.721 | 0.583 | 0.671 | 0.874 | 0.894 |  |
| archived-20261004-214724: db.jsonl | 90018981c6 | 0.777 | 0.696 | 9,678 | 9,678 | 0.722 | 0.820 | 0.656 | 0.722 | 1.009 | 0.876 |  |
| archived-20261004-214724: db.jsonl | e0cbf09bc2 | 0.702 | 0.666 | 13,057 | 13,057 | 0.698 | 0.758 | 0.525 | 0.643 | 0.951 | 0.883 |  |
| archived-20261004-214724: db.jsonl | 1769ca2a48 | 0.659 | 0.603 | 13,209 | 13,209 | 0.689 | 0.623 | 0.522 | 0.639 | 0.866 | 0.845 |  |
| archived-20261004-214724: db.jsonl | 14f6036a4b | 0.681 | 0.627 | 13,217 | 13,217 | 0.666 | 0.828 | 0.477 | 0.598 | 0.929 | 0.905 |  |
| archived-20261004-214724: db.jsonl | 29ad5ba726 | 0.650 | 0.589 | 13,352 | 13,352 | 0.676 | 0.748 | 0.487 | 0.590 | 0.797 | 0.796 |  |
| archived-20261004-214724: db.jsonl | 12d8e18511 | 0.709 | 0.667 | 13,360 | 13,360 | 0.694 | 0.851 | 0.536 | 0.616 | 0.920 | 0.915 |  |
| archived-20261005-013645: db.jsonl | 05dcc81cdc | 0.742 | 0.688 | 9,335 | 9,335 | 0.725 | 0.803 | 0.594 | 0.699 | 0.930 | 0.887 |  |
| archived-20261005-013645: db.jsonl | c297551359 | 0.707 | 0.682 | 9,450 | 9,450 | 0.736 | 0.662 | 0.634 | 0.701 | 0.819 | 0.874 |  |
| archived-20261005-013645: db.jsonl | e8f1dd3ca2 | 0.736 | 0.678 | 9,458 | 9,458 | 0.694 | 0.852 | 0.579 | 0.657 | 0.961 | 0.883 |  |
| archived-20261005-013645: db.jsonl | 66eb4a8f15 | 0.687 | 0.641 | 13,057 | 13,057 | 0.706 | 0.686 | 0.528 | 0.644 | 0.926 | 0.894 |  |
| archived-20261005-013645: db.jsonl | 84e302c470 | 0.725 | 0.657 | 13,065 | 13,065 | 0.735 | 0.752 | 0.542 | 0.662 | 1.011 | 0.919 |  |
| archived-20261005-013645: db.jsonl | 4cb3fa9172 | 0.685 | 0.626 | 13,073 | 13,073 | 0.664 | 0.802 | 0.477 | 0.600 | 0.986 | 0.886 |  |
| archived-20261005-013645: db.jsonl | e99da68667 | 0.661 | 0.581 | 13,201 | 13,201 | 0.629 | 0.769 | 0.457 | 0.567 | 1.010 | 0.879 |  |
| archived-20261005-042924: db.jsonl | 98736f0596 | 0.781 | 0.731 | 9,335 | 9,335 | 0.787 | 0.737 | 0.669 | 0.735 | 1.017 | 0.929 |  |
| archived-20261005-042924: db.jsonl | 4f010d8ab9 | 0.771 | 0.721 | 9,343 | 9,343 | 0.787 | 0.749 | 0.645 | 0.710 | 1.011 | 0.918 |  |
| archived-20261005-042924: db.jsonl | 4032a5ce71 | 0.752 | 0.698 | 9,351 | 9,351 | 0.759 | 0.805 | 0.603 | 0.694 | 0.940 | 0.905 |  |
| archived-20261005-042924: db.jsonl | 528fc9619a | 0.755 | 0.702 | 9,359 | 9,359 | 0.754 | 0.763 | 0.608 | 0.710 | 0.988 | 0.896 |  |
| archived-20261005-042924: db.jsonl | f052397620 | 0.735 | 0.685 | 9,450 | 9,450 | 0.743 | 0.805 | 0.586 | 0.682 | 0.900 | 0.894 |  |
| archived-20261005-042924: db.jsonl | 8dc0f97f2c | 0.724 | 0.680 | 9,458 | 9,458 | 0.712 | 0.758 | 0.585 | 0.678 | 0.931 | 0.886 |  |
| archived-20261005-042924: db.jsonl | 52b80007a1 | 0.702 | 0.640 | 10,010 | 10,010 | 0.750 | 0.550 | 0.601 | 0.691 | 0.998 | 0.859 |  |
| archived-20261005-042924: db.jsonl | 5ed1ed8715 | 0.703 | 0.642 | 10,018 | 10,018 | 0.738 | 0.546 | 0.615 | 0.700 | 0.988 | 0.871 |  |
| archived-20261005-042924: db.jsonl | 9e50623ac1 | 0.660 | 0.593 | 13,073 | 13,073 | 0.668 | 0.711 | 0.488 | 0.594 | 0.909 | 0.844 |  |
| archived-20261005-042924: db.jsonl | 22b81e50c4 | 0.651 | 0.605 | 13,209 | 13,209 | 0.636 | 0.863 | 0.414 | 0.551 | 0.933 | 0.894 |  |
| archived-20261005-042924: db.jsonl | 2db525ff95 | 0.657 | 0.579 | 14,017 | 14,017 | 0.653 | 0.711 | 0.458 | 0.590 | 0.978 | 0.908 |  |
| archived-20261005-131253: db.jsonl | 422d6bcbca | 0.736 | 0.699 | 9,327 | 9,327 | 0.747 | 0.856 | 0.538 | 0.660 | 0.954 | 0.857 |  |
| archived-20261005-131253: db.jsonl | 090672993b | 0.743 | 0.700 | 9,335 | 9,335 | 0.704 | 0.829 | 0.640 | 0.677 | 0.894 | 0.788 |  |
| archived-20261005-131253: db.jsonl | 6495dcb5dd | 0.693 | 0.662 | 9,343 | 9,343 | 0.666 | 0.928 | 0.515 | 0.621 | 0.810 | 0.819 |  |
| archived-20261005-131253: db.jsonl | c40ba92d5b | 0.665 | 0.630 | 9,511 | 9,511 | 0.666 | 0.687 | 0.562 | 0.630 | 0.802 | 0.783 |  |
| archived-20261005-131253: db.jsonl | ca2ac63866 | 0.681 | 0.634 | 9,531 | 9,531 | 0.659 | 0.730 | 0.552 | 0.620 | 0.893 | 0.856 |  |
| archived-20261005-131253: db.jsonl | c61857fc89 | 0.655 | 0.633 | 10,034 | 10,034 | 0.680 | 0.707 | 0.530 | 0.634 | 0.745 | 0.853 |  |
| archived-20261005-131253: db.jsonl | b06a4cf784 | 0.656 | 0.615 | 10,246 | 10,246 | 0.642 | 0.700 | 0.522 | 0.607 | 0.855 | 0.839 |  |
| archived-20261005-131253: db.jsonl | af5e8dc29f | 0.668 | 0.604 | 10,254 | 10,254 | 0.654 | 0.700 | 0.532 | 0.623 | 0.874 | 0.828 |  |
| archived-20261005-131253: db.jsonl | a74b828e9b | 0.670 | 0.608 | 13,073 | 13,073 | 0.680 | 0.636 | 0.511 | 0.618 | 0.994 | 0.845 |  |
| archived-20261005-131253: db.jsonl | dc02ceae31 | 0.606 | 0.560 | 13,161 | 13,161 | 0.621 | 0.724 | 0.434 | 0.539 | 0.776 | 0.827 |  |
| archived-20261005-131253: db.jsonl | 15dde12f04 | 0.603 | 0.567 | 13,345 | 13,345 | 0.629 | 0.760 | 0.405 | 0.532 | 0.772 | 0.844 |  |
| archived-20261005-131253: db.jsonl | cd943ed219 | 0.592 | 0.545 | 14,081 | 14,081 | 0.622 | 0.683 | 0.407 | 0.533 | 0.791 | 0.845 |  |
| archived-20261005-144844: db.jsonl | 49b0a93f14 | 0.697 | 0.688 | 8,073 | 8,073 | 0.704 | 0.884 | 0.560 | 0.658 | 0.719 | 0.832 |  |
| archived-20261005-144844: db.jsonl | 9f5e6d173c | 0.692 | 0.650 | 8,074 | 8,074 | 0.664 | 0.908 | 0.527 | 0.612 | 0.813 | 0.807 |  |
| archived-20261005-144844: db.jsonl | f060a4c31f | 0.683 | 0.637 | 8,289 | 8,289 | 0.643 | 0.845 | 0.526 | 0.596 | 0.872 | 0.818 |  |
| archived-20261005-144844: db.jsonl | a306cc61fb | 0.675 | 0.615 | 8,305 | 8,305 | 0.664 | 0.636 | 0.561 | 0.618 | 0.958 | 0.805 |  |
| archived-20261005-144844: db.jsonl | 3c2d8a577b | 0.659 | 0.603 | 8,306 | 8,306 | 0.682 | 0.638 | 0.536 | 0.609 | 0.877 | 0.801 |  |
| archived-20261005-144844: db.jsonl | 4cc12fc1e7 | 0.627 | 0.561 | 8,957 | 8,957 | 0.630 | 0.552 | 0.507 | 0.583 | 0.944 | 0.767 |  |
| archived-20261005-144844: db.jsonl | 3a7c3d6e90 | 0.607 | 0.551 | 11,777 | 11,777 | 0.603 | 0.867 | 0.359 | 0.521 | 0.841 | 0.845 |  |
| archived-20261005-144844: db.jsonl | 2b00aa6e97 | 0.613 | 0.568 | 12,145 | 12,145 | 0.614 | 0.879 | 0.358 | 0.525 | 0.854 | 0.831 |  |
| archived-20261005-144844: db.jsonl | 27a35df3fa | 0.623 | 0.570 | 12,312 | 12,312 | 0.625 | 0.581 | 0.487 | 0.567 | 0.936 | 0.785 |  |
| archived-20261005-144844: db.jsonl | ff39b37bcc | 0.635 | 0.572 | 12,584 | 12,584 | 0.628 | 0.627 | 0.465 | 0.574 | 0.982 | 0.825 |  |
| archived-20261005-144844: db.jsonl | 1cf03a8fd4 | 0.606 | 0.545 | 12,608 | 12,608 | 0.597 | 0.691 | 0.403 | 0.544 | 0.900 | 0.819 |  |
| archived-20261005-144844: db.jsonl | a214fa731c | 0.597 | 0.557 | 12,664 | 12,664 | 0.640 | 0.609 | 0.449 | 0.563 | 0.767 | 0.781 |  |
| archived-20261005-164554: db.jsonl | f41ab1810d | 1.014 | 1.008 | 8,034 | 8,034 | 1.020 | 1.253 | 0.811 | 0.939 | 1.102 | 1.143 |  |
| archived-20261005-164554: db.jsonl | 3781c5e756 | 0.766 | 0.758 | 8,041 | 8,041 | 0.768 | 0.961 | 0.612 | 0.691 | 0.847 | 0.857 |  |
| archived-20261005-164554: db.jsonl | d4739aac88 | 0.725 | 0.723 | 8,042 | 8,042 | 0.792 | 0.728 | 0.640 | 0.735 | 0.737 | 0.858 |  |
| archived-20261005-164554: db.jsonl | e05adba602 | 0.697 | 0.687 | 8,082 | 8,082 | 0.725 | 0.789 | 0.538 | 0.659 | 0.810 | 0.802 |  |
| archived-20261005-164554: db.jsonl | bb8a0cb575 | 0.702 | 0.688 | 8,099 | 8,099 | 0.756 | 0.782 | 0.557 | 0.696 | 0.744 | 0.843 |  |
| archived-20261005-164554: db.jsonl | a27aa49d8e | 0.698 | 0.693 | 8,163 | 8,163 | 0.676 | 0.848 | 0.519 | 0.622 | 0.897 | 0.860 |  |
| archived-20261005-164554: db.jsonl | 8a2189b3b6 | 0.655 | 0.646 | 8,171 | 8,171 | 0.674 | 0.762 | 0.515 | 0.604 | 0.755 | 0.847 |  |
| archived-20261005-164554: db.jsonl | f66d74a27c | 0.685 | 0.682 | 8,210 | 8,210 | 0.690 | 0.879 | 0.518 | 0.625 | 0.770 | 0.816 |  |
| archived-20261005-164554: db.jsonl | be02a4c0cf | 0.552 | 0.533 | 8,525 | 8,525 | 0.785 | 0.771 | 0.612 | 0.704 | 0.195 | 0.600 |  |
| archived-20261005-164554: db.jsonl | caf4358de8 | 0.537 | 0.514 | 8,540 | 8,540 | 0.767 | 0.754 | 0.578 | 0.693 | 0.192 | 0.634 |  |
| archived-20261005-164554: db.jsonl | 6578fc6928 | 0.531 | 0.515 | 8,548 | 8,548 | 0.708 | 0.771 | 0.527 | 0.627 | 0.235 | 0.589 |  |
| archived-20261005-164554: db.jsonl | 3d31fd4cc4 | 0.526 | 0.502 | 8,550 | 8,550 | 0.697 | 0.862 | 0.525 | 0.618 | 0.206 | 0.668 |  |
| archived-20261005-164554: db.jsonl | 85cac726b5 | 0.505 | 0.484 | 8,614 | 8,614 | 0.641 | 0.877 | 0.530 | 0.605 | 0.181 | 0.635 |  |
| archived-20261005-164554: db.jsonl | f85a63f8c7 | 0.499 | 0.481 | 8,647 | 8,647 | 0.651 | 0.859 | 0.528 | 0.596 | 0.176 | 0.602 |  |
| archived-20261005-164554: db.jsonl | 51879a71f0 | 0.508 | 0.513 | 8,664 | 8,664 | 0.680 | 0.755 | 0.551 | 0.614 | 0.194 | 0.661 |  |
| archived-20261005-164554: db.jsonl | 1b602bc9bd | 0.496 | 0.478 | 8,671 | 8,671 | 0.667 | 0.780 | 0.490 | 0.610 | 0.194 | 0.585 |  |
| archived-20261005-164554: db.jsonl | 72ca2cf497 | 0.481 | 0.469 | 8,990 | 8,990 | 0.649 | 0.664 | 0.510 | 0.602 | 0.195 | 0.531 |  |
| archived-20261005-164554: db.jsonl | 959e88b0f5 | 0.471 | 0.458 | 9,140 | 9,140 | 0.678 | 0.537 | 0.510 | 0.628 | 0.199 | 0.526 |  |
| archived-20261005-164554: db.jsonl | 577c999e62 | 0.469 | 0.443 | 9,278 | 9,278 | 0.664 | 0.558 | 0.505 | 0.602 | 0.201 | 0.530 |  |
| archived-20261005-164554: db.jsonl | aba06380d6 | 0.490 | 0.462 | 12,353 | 12,353 | 0.665 | 0.771 | 0.483 | 0.607 | 0.187 | 0.644 |  |
| archived-20261005-164554: db.jsonl | 0212f86508 | 0.470 | 0.453 | 12,377 | 12,377 | 0.637 | 0.796 | 0.442 | 0.557 | 0.183 | 0.611 |  |
| archived-20261005-164554: db.jsonl | 9bb527944a | 0.436 | 0.430 | 13,073 | 13,073 | 0.608 | 0.556 | 0.434 | 0.560 | 0.191 | 0.562 |  |
| archived-20261005-175214: db.jsonl | c513ef17b0 | 0.792 | 0.781 | 7,019 | 7,019 | 0.843 | 0.773 | 0.637 | 0.749 | 1.005 | 0.867 |  |
| archived-20261005-175214: db.jsonl | 57d12a1bb0 | 0.756 | 0.756 | 7,020 | 7,020 | 0.757 | 0.897 | 0.601 | 0.718 | 0.844 | 0.847 |  |
| archived-20261005-175214: db.jsonl | ee4d8f8a50 | 0.722 | 0.723 | 7,027 | 7,027 | 0.787 | 0.748 | 0.619 | 0.707 | 0.759 | 0.837 |  |
| archived-20261005-175214: db.jsonl | ccce4784b8 | 0.694 | 0.681 | 7,091 | 7,091 | 0.752 | 0.729 | 0.621 | 0.697 | 0.677 | 0.843 |  |
| archived-20261005-175214: db.jsonl | 88792f1798 | 0.662 | 0.653 | 7,220 | 7,220 | 0.700 | 0.746 | 0.557 | 0.641 | 0.683 | 0.815 |  |
| archived-20261005-175214: db.jsonl | 2367cb920c | 0.543 | 0.538 | 7,510 | 7,510 | 0.743 | 0.789 | 0.602 | 0.691 | 0.193 | 0.618 |  |
| archived-20261005-175214: db.jsonl | 853cfb9d36 | 0.544 | 0.536 | 7,651 | 7,651 | 0.736 | 0.835 | 0.622 | 0.698 | 0.178 | 0.647 |  |
| archived-20261005-175214: db.jsonl | fa23f401cd | 0.536 | 0.525 | 7,692 | 7,692 | 0.702 | 0.862 | 0.602 | 0.649 | 0.187 | 0.641 |  |
| archived-20261005-175214: db.jsonl | 45d2ff7e01 | 0.510 | 0.500 | 7,725 | 7,725 | 0.691 | 0.725 | 0.556 | 0.645 | 0.192 | 0.669 |  |
| archived-20261005-175214: db.jsonl | f084674b22 | 0.517 | 0.516 | 9,198 | 9,198 | 0.699 | 0.725 | 0.581 | 0.653 | 0.193 | 0.661 |  |
| archived-20261005-175214: db.jsonl | 9d89f6ba0e | 0.491 | 0.487 | 13,065 | 13,065 | 0.664 | 0.773 | 0.510 | 0.607 | 0.180 | 0.669 |  |
| archived-20261005-204503: db.jsonl | 295a6acd98 | 0.760 | 0.755 | 6,977 | 6,977 | 0.765 | 0.832 | 0.623 | 0.715 | 0.898 | 0.862 |  |
| archived-20261005-204503: db.jsonl | 82e7e4dc0d | 0.731 | 0.726 | 6,979 | 6,979 | 0.779 | 0.819 | 0.580 | 0.704 | 0.804 | 0.844 |  |
| archived-20261005-204503: db.jsonl | 9385a8fcbb | 0.692 | 0.690 | 6,994 | 6,994 | 0.702 | 0.873 | 0.545 | 0.642 | 0.739 | 0.834 |  |
| archived-20261005-204503: db.jsonl | bf413bef91 | 0.671 | 0.681 | 7,002 | 7,002 | 0.707 | 0.701 | 0.536 | 0.639 | 0.800 | 0.832 |  |
| archived-20261005-204503: db.jsonl | c25a5e1714 | 0.675 | 0.668 | 7,010 | 7,010 | 0.735 | 0.714 | 0.555 | 0.630 | 0.762 | 0.842 |  |
| archived-20261005-204503: db.jsonl | 7380e8bcb1 | 0.665 | 0.658 | 7,050 | 7,050 | 0.680 | 0.760 | 0.536 | 0.633 | 0.744 | 0.819 |  |
| archived-20261005-204503: db.jsonl | 5df0608416 | 0.659 | 0.659 | 7,059 | 7,059 | 0.663 | 0.759 | 0.532 | 0.624 | 0.744 | 0.826 |  |
| archived-20261005-204503: db.jsonl | d8d62beb78 | 0.548 | 0.545 | 7,106 | 7,106 | 0.734 | 0.879 | 0.586 | 0.693 | 0.189 | 0.677 |  |
| archived-20261005-204503: db.jsonl | f3988ea716 | 0.515 | 0.510 | 7,113 | 7,113 | 0.704 | 0.762 | 0.568 | 0.646 | 0.184 | 0.629 |  |
| archived-20261005-204503: db.jsonl | 2ed8b1583e | 0.514 | 0.509 | 7,129 | 7,129 | 0.698 | 0.782 | 0.535 | 0.632 | 0.194 | 0.606 |  |
| archived-20261005-204503: db.jsonl | 641b85143d | 0.505 | 0.501 | 7,178 | 7,178 | 0.670 | 0.760 | 0.545 | 0.627 | 0.189 | 0.594 |  |
| archived-20261005-204503: db.jsonl | 96f2d8bfd7 | 0.490 | 0.490 | 7,236 | 7,236 | 0.653 | 0.762 | 0.507 | 0.593 | 0.189 | 0.566 |  |
| archived-20261005-204503: db.jsonl | 55ca1dfdb5 | 0.505 | 0.499 | 7,550 | 7,550 | 0.679 | 0.751 | 0.543 | 0.630 | 0.188 | 0.601 |  |
| archived-20261005-204503: db.jsonl | 0e8b212e50 | 0.508 | 0.507 | 7,558 | 7,558 | 0.654 | 0.861 | 0.533 | 0.602 | 0.186 | 0.628 |  |
| archived-20261005-204503: db.jsonl | 7a8d429413 | 0.483 | 0.479 | 7,714 | 7,714 | 0.719 | 0.526 | 0.525 | 0.647 | 0.204 | 0.559 |  |
| archived-20261005-204503: db.jsonl | 85a977e3ed | 0.494 | 0.486 | 7,804 | 7,804 | 0.711 | 0.581 | 0.567 | 0.677 | 0.185 | 0.526 |  |
| archived-20261005-204503: db.jsonl | cda8cad59b | 0.494 | 0.492 | 7,949 | 7,949 | 0.718 | 0.581 | 0.542 | 0.660 | 0.196 | 0.588 |  |
| archived-20261005-204503: db.jsonl | 049e0c9c48 | 0.466 | 0.457 | 7,973 | 7,973 | 0.680 | 0.527 | 0.518 | 0.612 | 0.193 | 0.534 |  |
| archived-20261005-204503: db.jsonl | 6827e42d47 | 0.462 | 0.451 | 8,352 | 8,352 | 0.655 | 0.505 | 0.515 | 0.607 | 0.204 | 0.533 |  |
| archived-20261005-204503: db.jsonl | ff306b06c1 | 0.434 | 0.451 | 12,145 | 12,145 | 0.618 | 0.506 | 0.454 | 0.565 | 0.191 | 0.571 |  |
| archived-20261005-204503: db.jsonl | 84a09433d4 | 0.442 | 0.435 | 12,585 | 12,585 | 0.614 | 0.551 | 0.437 | 0.563 | 0.204 | 0.576 |  |
| archived-20261005-204503: db.jsonl | ff3e6b2a34 | 0.439 | 0.438 | 13,073 | 13,073 | 0.617 | 0.552 | 0.444 | 0.555 | 0.195 | 0.566 |  |

The front of all runs together, by size: ced47e8cfa 0.413 at 8,030, 37b502fac7 0.433 at 7,238, 627568164d 0.444 at 7,147, cac62ca533 0.459 at 7,105, 2c9b948725 0.485 at 7,097, 63919635b7 0.507 at 7,089, 31a3ceea45 0.591 at 7,037, 6ba318d95c 0.605 at 6,989, 98e6135b93 0.677 at 6,978, d0d304e240 0.691 at 6,977, 7cb20d14b1 0.727 at 6,971

## The same session on two CPUs

Calibration on cpu 2: 1.007; on cpu 8: 0.999.

Speed on cpu 2 over speed on cpu 8, per design: median 1.003, 10-90% 0.994-1.013, extremes 0.983-1.037; rank agreement (Spearman) 1.00.

The front of all runs on cpu 2: ced47e8cfa 0.413 at 8,030, 37b502fac7 0.433 at 7,238, 627568164d 0.444 at 7,147, cac62ca533 0.459 at 7,105, 2c9b948725 0.485 at 7,097, 63919635b7 0.507 at 7,089, 31a3ceea45 0.591 at 7,037, 6ba318d95c 0.605 at 6,989, 98e6135b93 0.677 at 6,978, d0d304e240 0.691 at 6,977, 7cb20d14b1 0.727 at 6,971

The front of all runs on cpu 8: ced47e8cfa 0.412 at 8,030, 37b502fac7 0.433 at 7,238, 627568164d 0.443 at 7,147, cac62ca533 0.458 at 7,105, 2c9b948725 0.490 at 7,097, 63919635b7 0.505 at 7,089, 31a3ceea45 0.584 at 7,037, 6ba318d95c 0.603 at 6,989, 98e6135b93 0.677 at 6,978, d0d304e240 0.698 at 6,977, 7cb20d14b1 0.726 at 6,971

On both fronts: 11 of 11 and 11.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| ced47e8cfa | 0.413 | 0.412 | 1.003 |
| 37b502fac7 | 0.433 | 0.433 | 1.000 |
| ff306b06c1 | 0.434 | 0.437 | 0.992 |
| 9bb527944a | 0.436 | 0.435 | 1.003 |
| ff3e6b2a34 | 0.439 | 0.436 | 1.009 |
| 84a09433d4 | 0.442 | 0.438 | 1.010 |
| 627568164d | 0.444 | 0.443 | 1.001 |
| cac62ca533 | 0.459 | 0.458 | 1.003 |
| 6827e42d47 | 0.462 | 0.460 | 1.003 |
| 049e0c9c48 | 0.466 | 0.456 | 1.022 |
| 577c999e62 | 0.469 | 0.460 | 1.019 |
| 0212f86508 | 0.470 | 0.474 | 0.990 |
| 959e88b0f5 | 0.471 | 0.466 | 1.011 |
| 72ca2cf497 | 0.481 | 0.480 | 1.002 |
| 7a8d429413 | 0.483 | 0.483 | 1.000 |
| 2c9b948725 | 0.485 | 0.490 | 0.989 |
| 96f2d8bfd7 | 0.490 | 0.472 | 1.037 |
| aba06380d6 | 0.490 | 0.486 | 1.009 |
| 9d89f6ba0e | 0.491 | 0.495 | 0.993 |
| cda8cad59b | 0.494 | 0.493 | 1.001 |
| 85a977e3ed | 0.494 | 0.494 | 1.000 |
| 1b602bc9bd | 0.496 | 0.491 | 1.010 |
| f85a63f8c7 | 0.499 | 0.504 | 0.991 |
| 85cac726b5 | 0.505 | 0.498 | 1.014 |
| 641b85143d | 0.505 | 0.498 | 1.013 |
| 55ca1dfdb5 | 0.505 | 0.504 | 1.003 |
| 63919635b7 | 0.507 | 0.505 | 1.006 |
| 0e8b212e50 | 0.508 | 0.507 | 1.001 |
| 51879a71f0 | 0.508 | 0.514 | 0.987 |
| 45d2ff7e01 | 0.510 | 0.500 | 1.019 |
| 2ed8b1583e | 0.514 | 0.508 | 1.012 |
| f3988ea716 | 0.515 | 0.517 | 0.996 |
| f084674b22 | 0.517 | 0.515 | 1.004 |
| 3d31fd4cc4 | 0.526 | 0.521 | 1.010 |
| 6578fc6928 | 0.531 | 0.531 | 1.000 |
| fa23f401cd | 0.536 | 0.543 | 0.987 |
| caf4358de8 | 0.537 | 0.533 | 1.007 |
| 2367cb920c | 0.543 | 0.540 | 1.005 |
| 853cfb9d36 | 0.544 | 0.546 | 0.995 |
| d8d62beb78 | 0.548 | 0.544 | 1.009 |
| be02a4c0cf | 0.552 | 0.553 | 0.998 |
| 31a3ceea45 | 0.591 | 0.584 | 1.011 |
| cd943ed219 | 0.592 | 0.584 | 1.014 |
| a214fa731c | 0.597 | 0.597 | 1.000 |
| 3f1d365b3b | 0.597 | 0.589 | 1.013 |
| 15dde12f04 | 0.603 | 0.599 | 1.006 |
| 6ba318d95c | 0.605 | 0.603 | 1.004 |
| 1cf03a8fd4 | 0.606 | 0.606 | 0.999 |
| dc02ceae31 | 0.606 | 0.608 | 0.996 |
| 7b9675c9ef | 0.606 | 0.610 | 0.993 |
| 3a7c3d6e90 | 0.607 | 0.604 | 1.004 |
| 2b00aa6e97 | 0.613 | 0.607 | 1.010 |
| 27a35df3fa | 0.623 | 0.627 | 0.994 |
| 4cc12fc1e7 | 0.627 | 0.619 | 1.013 |
| ff39b37bcc | 0.635 | 0.629 | 1.009 |
| 05617039f6 | 0.638 | 0.638 | 1.000 |
| 29ad5ba726 | 0.650 | 0.647 | 1.004 |
| 22b81e50c4 | 0.651 | 0.654 | 0.995 |
| 8dd8a7a146 | 0.653 | 0.646 | 1.011 |
| c61857fc89 | 0.655 | 0.651 | 1.006 |
| 8a2189b3b6 | 0.655 | 0.651 | 1.006 |
| b06a4cf784 | 0.656 | 0.658 | 0.998 |
| 2db525ff95 | 0.657 | 0.649 | 1.012 |
| 1769ca2a48 | 0.659 | 0.661 | 0.997 |
| 5df0608416 | 0.659 | 0.658 | 1.001 |
| 3c2d8a577b | 0.659 | 0.654 | 1.008 |
| 9e50623ac1 | 0.660 | 0.662 | 0.997 |
| e99da68667 | 0.661 | 0.649 | 1.019 |
| 88792f1798 | 0.662 | 0.653 | 1.014 |
| c40ba92d5b | 0.665 | 0.664 | 1.001 |
| 7380e8bcb1 | 0.665 | 0.665 | 1.001 |
| af5e8dc29f | 0.668 | 0.661 | 1.010 |
| a74b828e9b | 0.670 | 0.667 | 1.005 |
| bf413bef91 | 0.671 | 0.667 | 1.006 |
| c25a5e1714 | 0.675 | 0.670 | 1.007 |
| a306cc61fb | 0.675 | 0.672 | 1.004 |
| 32600cab87 | 0.676 | 0.676 | 0.999 |
| 98e6135b93 | 0.677 | 0.677 | 1.000 |
| 0b1d16def9 | 0.679 | 0.683 | 0.995 |
| 14f6036a4b | 0.681 | 0.675 | 1.008 |
| ca2ac63866 | 0.681 | 0.683 | 0.998 |
| f060a4c31f | 0.683 | 0.684 | 0.998 |
| 4cb3fa9172 | 0.685 | 0.684 | 1.001 |
| f66d74a27c | 0.685 | 0.685 | 1.000 |
| 312ad2edaa | 0.685 | 0.686 | 1.000 |
| 66eb4a8f15 | 0.687 | 0.677 | 1.014 |
| 448ef1ef43 | 0.687 | 0.691 | 0.995 |
| d0d304e240 | 0.691 | 0.698 | 0.990 |
| 38d187239c | 0.691 | 0.694 | 0.996 |
| 9385a8fcbb | 0.692 | 0.687 | 1.007 |
| 9f5e6d173c | 0.692 | 0.692 | 0.999 |
| 60753a0eb0 | 0.692 | 0.684 | 1.013 |
| 6495dcb5dd | 0.693 | 0.689 | 1.006 |
| ccce4784b8 | 0.694 | 0.688 | 1.008 |
| e05adba602 | 0.697 | 0.699 | 0.997 |
| 49b0a93f14 | 0.697 | 0.695 | 1.003 |
| a27aa49d8e | 0.698 | 0.700 | 0.998 |
| e0cbf09bc2 | 0.702 | 0.699 | 1.004 |
| bb8a0cb575 | 0.702 | 0.694 | 1.011 |
| 52b80007a1 | 0.702 | 0.699 | 1.005 |
| 5ed1ed8715 | 0.703 | 0.709 | 0.992 |
| 6463752a82 | 0.704 | 0.714 | 0.986 |
| c297551359 | 0.707 | 0.702 | 1.008 |
| 12d8e18511 | 0.709 | 0.710 | 0.999 |
| 38d91795a2 | 0.715 | 0.709 | 1.009 |
| 7fe7f039bd | 0.719 | 0.722 | 0.996 |
| ee4d8f8a50 | 0.722 | 0.721 | 1.001 |
| 8dc0f97f2c | 0.724 | 0.723 | 1.002 |
| d4739aac88 | 0.725 | 0.720 | 1.007 |
| 84e302c470 | 0.725 | 0.722 | 1.004 |
| 8cbc6dd05c | 0.727 | 0.726 | 1.000 |
| 7cb20d14b1 | 0.727 | 0.726 | 1.002 |
| f4a6dd9a13 | 0.727 | 0.722 | 1.007 |
| 550df563ee | 0.729 | 0.741 | 0.983 |
| 53ec9bedde | 0.730 | 0.734 | 0.994 |
| 82e7e4dc0d | 0.731 | 0.723 | 1.011 |
| 57a9dcc7cb | 0.734 | 0.738 | 0.994 |
| f052397620 | 0.735 | 0.733 | 1.003 |
| e8f1dd3ca2 | 0.736 | 0.728 | 1.011 |
| 422d6bcbca | 0.736 | 0.729 | 1.010 |
| a285fa6ba3 | 0.737 | 0.734 | 1.003 |
| 05dcc81cdc | 0.742 | 0.740 | 1.003 |
| 090672993b | 0.743 | 0.739 | 1.005 |
| 57e0e77c09 | 0.746 | 0.753 | 0.991 |
| 3453246bdf | 0.752 | 0.746 | 1.008 |
| 4032a5ce71 | 0.752 | 0.747 | 1.007 |
| 528fc9619a | 0.755 | 0.750 | 1.006 |
| 57d12a1bb0 | 0.756 | 0.752 | 1.005 |
| 9cd791dd84 | 0.757 | 0.754 | 1.004 |
| 295a6acd98 | 0.760 | 0.749 | 1.015 |
| 595fc2b8f4 | 0.762 | 0.761 | 1.001 |
| 6738aed13f | 0.762 | 0.762 | 1.000 |
| 3781c5e756 | 0.766 | 0.763 | 1.004 |
| 5b70f3dd64 | 0.769 | 0.756 | 1.017 |
| 0ebf0445e0 | 0.770 | 0.772 | 0.996 |
| 4f010d8ab9 | 0.771 | 0.769 | 1.004 |
| 90018981c6 | 0.777 | 0.775 | 1.003 |
| c17103bf95 | 0.779 | 0.783 | 0.995 |
| 98736f0596 | 0.781 | 0.776 | 1.006 |
| c513ef17b0 | 0.792 | 0.792 | 1.001 |
| a4e82e02e5 | 0.794 | 0.799 | 0.994 |
| 672538daf5 | 0.834 | 0.818 | 1.019 |
| 83cb81c383 | 0.840 | 0.829 | 1.014 |
| f41ab1810d | 1.014 | 1.004 | 1.010 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 10 - Iteration 53: seeds 1-12, after seed 12 (THREAD-FIND first)

`seed 12 then experiment compare-fronts.py --rounds 10 --cpus 2,8`, commit
011ae717: fourteen databases, 157 front designs, five workloads, sieve
held out. Seventeen minutes. **Calibration 0.994** (corpus 0.977, the rest
0.985-1.014). The CPUs agree: per design median 0.999, 10-90% 0.989-1.010,
ranks 1.00; 10 of 12 and 11 designs on both CPUs' fronts.

**The front of all runs: seed 12's twelve**, 6,941 bytes (0.646) to 9,014
(0.326, the fastest yet).

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 0.994** (kernel 1.002, fib 1.014, parse 0.985, corpus 0.977, loop 0.994, sieve 0.988).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 2816900bac | 0.646 | 0.638 | 6,941 | 6,941 | 0.605 | 0.778 | 0.493 | 0.564 | 0.862 | 0.816 | yes |
| this clone: db.jsonl | 46fbc9e912 | 0.501 | 0.491 | 6,966 | 6,966 | 0.500 | 0.951 | 0.245 | 0.406 | 0.665 | 0.761 | yes |
| this clone: db.jsonl | c2d99350f1 | 0.490 | 0.481 | 6,974 | 6,974 | 0.517 | 0.697 | 0.226 | 0.399 | 0.869 | 0.874 | yes |
| this clone: db.jsonl | 0f90ffc36a | 0.485 | 0.474 | 6,998 | 6,998 | 0.502 | 0.735 | 0.239 | 0.411 | 0.739 | 0.841 | yes |
| this clone: db.jsonl | 988d608671 | 0.485 | 0.478 | 7,014 | 7,014 | 0.523 | 0.718 | 0.239 | 0.400 | 0.747 | 0.821 | yes |
| this clone: db.jsonl | 20b3bde0c3 | 0.397 | 0.385 | 7,097 | 7,097 | 0.511 | 0.889 | 0.278 | 0.414 | 0.189 | 0.673 | yes |
| this clone: db.jsonl | 35135bde2f | 0.379 | 0.371 | 7,105 | 7,105 | 0.478 | 0.799 | 0.239 | 0.382 | 0.225 | 0.642 | yes |
| this clone: db.jsonl | 9a482dbeaf | 0.355 | 0.351 | 7,334 | 7,334 | 0.471 | 0.866 | 0.218 | 0.353 | 0.180 | 0.556 | yes |
| this clone: db.jsonl | 040e367ce9 | 0.349 | 0.343 | 7,753 | 7,753 | 0.468 | 0.791 | 0.224 | 0.360 | 0.174 | 0.570 | yes |
| this clone: db.jsonl | 1918ae250d | 0.349 | 0.346 | 7,820 | 7,820 | 0.506 | 0.521 | 0.226 | 0.395 | 0.221 | 0.533 | yes |
| this clone: db.jsonl | 9102e1dea9 | 0.331 | 0.316 | 7,958 | 7,958 | 0.472 | 0.602 | 0.212 | 0.364 | 0.180 | 0.486 | yes |
| this clone: db.jsonl | c9f3c95232 | 0.332 | 0.330 | 7,966 | 7,966 | 0.485 | 0.572 | 0.223 | 0.371 | 0.176 | 0.496 |  |
| this clone: db.jsonl | dcbaf0e29f | 0.326 | 0.329 | 9,014 | 9,014 | 0.465 | 0.596 | 0.218 | 0.350 | 0.174 | 0.471 | yes |
| archived-20261004-200423: db-rehearsal.jsonl | 595fc2b8f4 | 0.748 | 0.784 | 9,662 | 9,761 | 0.728 | 0.700 | 0.621 | 0.708 | 1.050 | 0.835 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 8cbc6dd05c | 0.724 | 0.742 | 9,694 | 9,809 | 0.706 | 0.788 | 0.617 | 0.676 | 0.859 | 0.801 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 6738aed13f | 0.764 | 0.755 | 9,694 | 9,793 | 0.763 | 0.706 | 0.628 | 0.724 | 1.064 | 0.858 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 312ad2edaa | 0.687 | 0.716 | 13,344 | 13,456 | 0.702 | 0.721 | 0.538 | 0.637 | 0.885 | 0.847 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 05617039f6 | 0.643 | 0.674 | 13,352 | 13,488 | 0.680 | 0.811 | 0.471 | 0.606 | 0.699 | 0.796 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 0b1d16def9 | 0.672 | 0.705 | 13,352 | 13,464 | 0.701 | 0.795 | 0.499 | 0.626 | 0.788 | 0.846 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 57a9dcc7cb | 0.733 | 0.680 | 13,368 | 13,480 | 0.708 | 0.906 | 0.542 | 0.643 | 0.948 | 0.884 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 32600cab87 | 0.675 | 0.662 | 13,528 | 13,656 | 0.681 | 0.946 | 0.505 | 0.621 | 0.692 | 0.820 |  |
| archived-20261004-200423: db-seed1.jsonl | 83cb81c383 | 0.844 | 0.705 | 9,662 | 9,761 | 0.773 | 1.001 | 0.706 | 0.740 | 1.058 | 0.930 |  |
| archived-20261004-200423: db-seed1.jsonl | 5b70f3dd64 | 0.771 | 0.649 | 9,694 | 9,801 | 0.736 | 0.978 | 0.629 | 0.694 | 0.865 | 0.819 |  |
| archived-20261004-200423: db-seed1.jsonl | a4e82e02e5 | 0.799 | 0.654 | 9,694 | 9,809 | 0.789 | 0.868 | 0.658 | 0.727 | 0.995 | 0.898 |  |
| archived-20261004-200423: db-seed1.jsonl | 53ec9bedde | 0.730 | 0.670 | 13,336 | 13,464 | 0.752 | 0.783 | 0.615 | 0.672 | 0.852 | 0.838 |  |
| archived-20261004-200423: db-seed1.jsonl | 448ef1ef43 | 0.686 | 0.620 | 13,368 | 13,488 | 0.674 | 0.950 | 0.493 | 0.604 | 0.797 | 0.836 |  |
| archived-20261004-200423: db-seed1.jsonl | 38d187239c | 0.692 | 0.609 | 13,368 | 13,480 | 0.707 | 0.854 | 0.536 | 0.622 | 0.790 | 0.819 |  |
| archived-20261004-200423: db-seed2.jsonl | 0ebf0445e0 | 0.767 | 0.667 | 9,662 | 9,761 | 0.790 | 0.671 | 0.693 | 0.743 | 0.974 | 0.897 |  |
| archived-20261004-200423: db-seed2.jsonl | c17103bf95 | 0.780 | 0.725 | 9,662 | 9,769 | 0.784 | 0.762 | 0.694 | 0.765 | 0.913 | 0.885 |  |
| archived-20261004-200423: db-seed2.jsonl | a285fa6ba3 | 0.732 | 0.666 | 13,352 | 13,464 | 0.756 | 0.705 | 0.608 | 0.703 | 0.925 | 0.895 |  |
| archived-20261004-200423: db-seed2.jsonl | 57e0e77c09 | 0.755 | 0.657 | 13,352 | 13,480 | 0.727 | 1.048 | 0.544 | 0.642 | 0.920 | 0.867 |  |
| archived-20261004-200423: db-seed2.jsonl | 9cd791dd84 | 0.755 | 0.619 | 13,368 | 13,472 | 0.741 | 0.863 | 0.572 | 0.669 | 1.003 | 0.885 |  |
| archived-20261004-200423: db.jsonl | 550df563ee | 0.745 | 0.696 | 9,646 | 9,745 | 0.706 | 0.776 | 0.628 | 0.680 | 0.983 | 0.851 |  |
| archived-20261004-200423: db.jsonl | f4a6dd9a13 | 0.725 | 0.683 | 9,662 | 9,761 | 0.733 | 0.663 | 0.611 | 0.702 | 0.964 | 0.803 |  |
| archived-20261004-200423: db.jsonl | 60753a0eb0 | 0.690 | 0.622 | 9,686 | 9,785 | 0.690 | 0.657 | 0.583 | 0.658 | 0.899 | 0.790 |  |
| archived-20261004-200423: db.jsonl | 8dd8a7a146 | 0.647 | 0.595 | 13,352 | 13,464 | 0.648 | 0.662 | 0.513 | 0.606 | 0.851 | 0.805 |  |
| archived-20261004-214724: db.jsonl | 3453246bdf | 0.747 | 0.727 | 9,335 | 9,335 | 0.759 | 0.688 | 0.675 | 0.742 | 0.889 | 0.864 |  |
| archived-20261004-214724: db.jsonl | 672538daf5 | 0.823 | 0.780 | 9,351 | 9,351 | 0.807 | 0.827 | 0.716 | 0.775 | 1.020 | 0.888 |  |
| archived-20261004-214724: db.jsonl | 7fe7f039bd | 0.722 | 0.702 | 9,450 | 9,450 | 0.756 | 0.709 | 0.627 | 0.705 | 0.830 | 0.873 |  |
| archived-20261004-214724: db.jsonl | 38d91795a2 | 0.709 | 0.678 | 9,474 | 9,474 | 0.737 | 0.646 | 0.612 | 0.719 | 0.854 | 0.838 |  |
| archived-20261004-214724: db.jsonl | 6463752a82 | 0.707 | 0.669 | 9,523 | 9,523 | 0.715 | 0.712 | 0.583 | 0.673 | 0.888 | 0.859 |  |
| archived-20261004-214724: db.jsonl | 90018981c6 | 0.770 | 0.696 | 9,678 | 9,678 | 0.732 | 0.818 | 0.645 | 0.697 | 1.007 | 0.880 |  |
| archived-20261004-214724: db.jsonl | e0cbf09bc2 | 0.694 | 0.666 | 13,057 | 13,057 | 0.675 | 0.756 | 0.519 | 0.645 | 0.939 | 0.882 |  |
| archived-20261004-214724: db.jsonl | 1769ca2a48 | 0.659 | 0.603 | 13,209 | 13,209 | 0.681 | 0.616 | 0.529 | 0.643 | 0.868 | 0.858 |  |
| archived-20261004-214724: db.jsonl | 14f6036a4b | 0.674 | 0.627 | 13,217 | 13,217 | 0.661 | 0.809 | 0.469 | 0.595 | 0.933 | 0.882 |  |
| archived-20261004-214724: db.jsonl | 29ad5ba726 | 0.659 | 0.589 | 13,352 | 13,352 | 0.665 | 0.776 | 0.513 | 0.591 | 0.795 | 0.834 |  |
| archived-20261004-214724: db.jsonl | 12d8e18511 | 0.698 | 0.667 | 13,360 | 13,360 | 0.678 | 0.841 | 0.520 | 0.607 | 0.920 | 0.922 |  |
| archived-20261005-013645: db.jsonl | 05dcc81cdc | 0.743 | 0.688 | 9,335 | 9,335 | 0.737 | 0.812 | 0.603 | 0.693 | 0.908 | 0.875 |  |
| archived-20261005-013645: db.jsonl | c297551359 | 0.707 | 0.682 | 9,450 | 9,450 | 0.741 | 0.663 | 0.627 | 0.693 | 0.827 | 0.880 |  |
| archived-20261005-013645: db.jsonl | e8f1dd3ca2 | 0.730 | 0.678 | 9,458 | 9,458 | 0.702 | 0.809 | 0.580 | 0.650 | 0.965 | 0.897 |  |
| archived-20261005-013645: db.jsonl | 66eb4a8f15 | 0.681 | 0.641 | 13,057 | 13,057 | 0.689 | 0.698 | 0.534 | 0.629 | 0.905 | 0.879 |  |
| archived-20261005-013645: db.jsonl | 84e302c470 | 0.721 | 0.657 | 13,065 | 13,065 | 0.723 | 0.751 | 0.544 | 0.656 | 1.009 | 0.901 |  |
| archived-20261005-013645: db.jsonl | 4cb3fa9172 | 0.678 | 0.626 | 13,073 | 13,073 | 0.654 | 0.801 | 0.481 | 0.598 | 0.955 | 0.870 |  |
| archived-20261005-013645: db.jsonl | e99da68667 | 0.652 | 0.581 | 13,201 | 13,201 | 0.622 | 0.765 | 0.448 | 0.555 | 0.996 | 0.886 |  |
| archived-20261005-042924: db.jsonl | 98736f0596 | 0.777 | 0.731 | 9,335 | 9,335 | 0.773 | 0.730 | 0.691 | 0.727 | 1.001 | 0.898 |  |
| archived-20261005-042924: db.jsonl | 4f010d8ab9 | 0.769 | 0.721 | 9,343 | 9,343 | 0.783 | 0.741 | 0.659 | 0.717 | 0.985 | 0.910 |  |
| archived-20261005-042924: db.jsonl | 4032a5ce71 | 0.759 | 0.698 | 9,351 | 9,351 | 0.756 | 0.802 | 0.609 | 0.713 | 0.958 | 0.930 |  |
| archived-20261005-042924: db.jsonl | 528fc9619a | 0.753 | 0.702 | 9,359 | 9,359 | 0.754 | 0.763 | 0.606 | 0.703 | 0.986 | 0.933 |  |
| archived-20261005-042924: db.jsonl | f052397620 | 0.730 | 0.685 | 9,450 | 9,450 | 0.721 | 0.835 | 0.574 | 0.671 | 0.897 | 0.899 |  |
| archived-20261005-042924: db.jsonl | 8dc0f97f2c | 0.730 | 0.680 | 9,458 | 9,458 | 0.734 | 0.762 | 0.580 | 0.695 | 0.920 | 0.883 |  |
| archived-20261005-042924: db.jsonl | 52b80007a1 | 0.700 | 0.640 | 10,010 | 10,010 | 0.748 | 0.548 | 0.601 | 0.687 | 0.993 | 0.876 |  |
| archived-20261005-042924: db.jsonl | 5ed1ed8715 | 0.709 | 0.642 | 10,018 | 10,018 | 0.752 | 0.550 | 0.625 | 0.693 | 1.003 | 0.845 |  |
| archived-20261005-042924: db.jsonl | 9e50623ac1 | 0.659 | 0.593 | 13,073 | 13,073 | 0.670 | 0.716 | 0.484 | 0.596 | 0.900 | 0.853 |  |
| archived-20261005-042924: db.jsonl | 22b81e50c4 | 0.652 | 0.605 | 13,209 | 13,209 | 0.635 | 0.883 | 0.404 | 0.555 | 0.935 | 0.888 |  |
| archived-20261005-042924: db.jsonl | 2db525ff95 | 0.655 | 0.579 | 14,017 | 14,017 | 0.656 | 0.707 | 0.451 | 0.587 | 0.979 | 0.907 |  |
| archived-20261005-131253: db.jsonl | 422d6bcbca | 0.738 | 0.699 | 9,327 | 9,327 | 0.748 | 0.831 | 0.550 | 0.667 | 0.958 | 0.876 |  |
| archived-20261005-131253: db.jsonl | 090672993b | 0.738 | 0.700 | 9,335 | 9,335 | 0.703 | 0.833 | 0.628 | 0.688 | 0.867 | 0.791 |  |
| archived-20261005-131253: db.jsonl | 6495dcb5dd | 0.698 | 0.662 | 9,343 | 9,343 | 0.676 | 0.928 | 0.516 | 0.630 | 0.812 | 0.785 |  |
| archived-20261005-131253: db.jsonl | c40ba92d5b | 0.665 | 0.630 | 9,511 | 9,511 | 0.665 | 0.685 | 0.572 | 0.627 | 0.797 | 0.783 |  |
| archived-20261005-131253: db.jsonl | ca2ac63866 | 0.676 | 0.634 | 9,531 | 9,531 | 0.656 | 0.719 | 0.549 | 0.618 | 0.885 | 0.832 |  |
| archived-20261005-131253: db.jsonl | c61857fc89 | 0.652 | 0.633 | 10,034 | 10,034 | 0.677 | 0.678 | 0.542 | 0.636 | 0.743 | 0.837 |  |
| archived-20261005-131253: db.jsonl | b06a4cf784 | 0.658 | 0.615 | 10,246 | 10,246 | 0.641 | 0.692 | 0.537 | 0.614 | 0.846 | 0.830 |  |
| archived-20261005-131253: db.jsonl | af5e8dc29f | 0.664 | 0.604 | 10,254 | 10,254 | 0.644 | 0.676 | 0.547 | 0.618 | 0.878 | 0.814 |  |
| archived-20261005-131253: db.jsonl | a74b828e9b | 0.663 | 0.608 | 13,073 | 13,073 | 0.687 | 0.623 | 0.508 | 0.612 | 0.965 | 0.839 |  |
| archived-20261005-131253: db.jsonl | dc02ceae31 | 0.605 | 0.560 | 13,161 | 13,161 | 0.614 | 0.723 | 0.437 | 0.547 | 0.765 | 0.831 |  |
| archived-20261005-131253: db.jsonl | 15dde12f04 | 0.598 | 0.567 | 13,345 | 13,345 | 0.621 | 0.751 | 0.403 | 0.531 | 0.765 | 0.817 |  |
| archived-20261005-131253: db.jsonl | cd943ed219 | 0.588 | 0.545 | 14,081 | 14,081 | 0.607 | 0.685 | 0.402 | 0.543 | 0.775 | 0.828 |  |
| archived-20261005-144844: db.jsonl | 49b0a93f14 | 0.696 | 0.688 | 8,073 | 8,073 | 0.709 | 0.883 | 0.552 | 0.658 | 0.718 | 0.829 |  |
| archived-20261005-144844: db.jsonl | 9f5e6d173c | 0.694 | 0.650 | 8,074 | 8,074 | 0.667 | 0.912 | 0.523 | 0.616 | 0.820 | 0.831 |  |
| archived-20261005-144844: db.jsonl | f060a4c31f | 0.681 | 0.637 | 8,289 | 8,289 | 0.647 | 0.847 | 0.518 | 0.591 | 0.872 | 0.803 |  |
| archived-20261005-144844: db.jsonl | a306cc61fb | 0.678 | 0.615 | 8,305 | 8,305 | 0.674 | 0.638 | 0.560 | 0.612 | 0.969 | 0.795 |  |
| archived-20261005-144844: db.jsonl | 3c2d8a577b | 0.652 | 0.603 | 8,306 | 8,306 | 0.658 | 0.627 | 0.530 | 0.609 | 0.883 | 0.792 |  |
| archived-20261005-144844: db.jsonl | 4cc12fc1e7 | 0.623 | 0.561 | 8,957 | 8,957 | 0.630 | 0.547 | 0.494 | 0.589 | 0.934 | 0.772 |  |
| archived-20261005-144844: db.jsonl | 3a7c3d6e90 | 0.612 | 0.551 | 11,777 | 11,777 | 0.615 | 0.848 | 0.375 | 0.524 | 0.839 | 0.870 |  |
| archived-20261005-144844: db.jsonl | 2b00aa6e97 | 0.602 | 0.568 | 12,145 | 12,145 | 0.600 | 0.830 | 0.362 | 0.519 | 0.842 | 0.880 |  |
| archived-20261005-144844: db.jsonl | 27a35df3fa | 0.627 | 0.570 | 12,312 | 12,312 | 0.641 | 0.583 | 0.480 | 0.580 | 0.935 | 0.777 |  |
| archived-20261005-144844: db.jsonl | ff39b37bcc | 0.637 | 0.572 | 12,584 | 12,584 | 0.628 | 0.628 | 0.479 | 0.565 | 0.978 | 0.833 |  |
| archived-20261005-144844: db.jsonl | 1cf03a8fd4 | 0.605 | 0.545 | 12,608 | 12,608 | 0.602 | 0.691 | 0.404 | 0.540 | 0.894 | 0.838 |  |
| archived-20261005-144844: db.jsonl | a214fa731c | 0.591 | 0.557 | 12,664 | 12,664 | 0.639 | 0.589 | 0.453 | 0.561 | 0.756 | 0.737 |  |
| archived-20261005-164554: db.jsonl | f41ab1810d | 1.010 | 1.008 | 8,034 | 8,034 | 1.016 | 1.256 | 0.807 | 0.927 | 1.101 | 1.157 |  |
| archived-20261005-164554: db.jsonl | 3781c5e756 | 0.765 | 0.758 | 8,041 | 8,041 | 0.760 | 0.957 | 0.606 | 0.701 | 0.847 | 0.856 |  |
| archived-20261005-164554: db.jsonl | d4739aac88 | 0.718 | 0.723 | 8,042 | 8,042 | 0.796 | 0.713 | 0.627 | 0.732 | 0.731 | 0.860 |  |
| archived-20261005-164554: db.jsonl | e05adba602 | 0.693 | 0.687 | 8,082 | 8,082 | 0.720 | 0.759 | 0.552 | 0.674 | 0.789 | 0.823 |  |
| archived-20261005-164554: db.jsonl | bb8a0cb575 | 0.699 | 0.688 | 8,099 | 8,099 | 0.748 | 0.769 | 0.565 | 0.691 | 0.741 | 0.849 |  |
| archived-20261005-164554: db.jsonl | a27aa49d8e | 0.698 | 0.693 | 8,163 | 8,163 | 0.687 | 0.851 | 0.511 | 0.629 | 0.882 | 0.825 |  |
| archived-20261005-164554: db.jsonl | 8a2189b3b6 | 0.654 | 0.646 | 8,171 | 8,171 | 0.674 | 0.763 | 0.505 | 0.602 | 0.764 | 0.856 |  |
| archived-20261005-164554: db.jsonl | f66d74a27c | 0.685 | 0.682 | 8,210 | 8,210 | 0.695 | 0.885 | 0.513 | 0.623 | 0.769 | 0.809 |  |
| archived-20261005-164554: db.jsonl | be02a4c0cf | 0.548 | 0.533 | 8,525 | 8,525 | 0.785 | 0.774 | 0.598 | 0.699 | 0.195 | 0.573 |  |
| archived-20261005-164554: db.jsonl | caf4358de8 | 0.538 | 0.514 | 8,540 | 8,540 | 0.748 | 0.761 | 0.587 | 0.694 | 0.195 | 0.623 |  |
| archived-20261005-164554: db.jsonl | 6578fc6928 | 0.528 | 0.515 | 8,548 | 8,548 | 0.710 | 0.764 | 0.520 | 0.630 | 0.230 | 0.589 |  |
| archived-20261005-164554: db.jsonl | 3d31fd4cc4 | 0.524 | 0.502 | 8,550 | 8,550 | 0.693 | 0.877 | 0.508 | 0.625 | 0.205 | 0.635 |  |
| archived-20261005-164554: db.jsonl | 85cac726b5 | 0.504 | 0.484 | 8,614 | 8,614 | 0.641 | 0.872 | 0.521 | 0.600 | 0.186 | 0.620 |  |
| archived-20261005-164554: db.jsonl | f85a63f8c7 | 0.502 | 0.481 | 8,647 | 8,647 | 0.650 | 0.834 | 0.542 | 0.592 | 0.183 | 0.622 |  |
| archived-20261005-164554: db.jsonl | 51879a71f0 | 0.509 | 0.513 | 8,664 | 8,664 | 0.684 | 0.735 | 0.561 | 0.633 | 0.191 | 0.644 |  |
| archived-20261005-164554: db.jsonl | 1b602bc9bd | 0.486 | 0.478 | 8,671 | 8,671 | 0.660 | 0.786 | 0.497 | 0.599 | 0.176 | 0.580 |  |
| archived-20261005-164554: db.jsonl | 72ca2cf497 | 0.484 | 0.469 | 8,990 | 8,990 | 0.649 | 0.666 | 0.513 | 0.600 | 0.200 | 0.531 |  |
| archived-20261005-164554: db.jsonl | 959e88b0f5 | 0.466 | 0.458 | 9,140 | 9,140 | 0.683 | 0.531 | 0.508 | 0.630 | 0.189 | 0.549 |  |
| archived-20261005-164554: db.jsonl | 577c999e62 | 0.462 | 0.443 | 9,278 | 9,278 | 0.667 | 0.542 | 0.500 | 0.596 | 0.195 | 0.521 |  |
| archived-20261005-164554: db.jsonl | aba06380d6 | 0.490 | 0.462 | 12,353 | 12,353 | 0.673 | 0.772 | 0.482 | 0.593 | 0.190 | 0.625 |  |
| archived-20261005-164554: db.jsonl | 0212f86508 | 0.473 | 0.453 | 12,377 | 12,377 | 0.634 | 0.792 | 0.447 | 0.547 | 0.193 | 0.614 |  |
| archived-20261005-164554: db.jsonl | 9bb527944a | 0.439 | 0.430 | 13,073 | 13,073 | 0.615 | 0.553 | 0.450 | 0.554 | 0.192 | 0.561 |  |
| archived-20261005-175214: db.jsonl | c513ef17b0 | 0.787 | 0.781 | 7,019 | 7,019 | 0.830 | 0.773 | 0.622 | 0.759 | 0.999 | 0.867 |  |
| archived-20261005-175214: db.jsonl | 57d12a1bb0 | 0.763 | 0.756 | 7,020 | 7,020 | 0.764 | 0.905 | 0.610 | 0.723 | 0.849 | 0.818 |  |
| archived-20261005-175214: db.jsonl | ee4d8f8a50 | 0.711 | 0.723 | 7,027 | 7,027 | 0.774 | 0.728 | 0.608 | 0.697 | 0.761 | 0.842 |  |
| archived-20261005-175214: db.jsonl | ccce4784b8 | 0.701 | 0.681 | 7,091 | 7,091 | 0.759 | 0.728 | 0.626 | 0.692 | 0.705 | 0.822 |  |
| archived-20261005-175214: db.jsonl | 88792f1798 | 0.661 | 0.653 | 7,220 | 7,220 | 0.683 | 0.746 | 0.549 | 0.637 | 0.706 | 0.823 |  |
| archived-20261005-175214: db.jsonl | 2367cb920c | 0.538 | 0.538 | 7,510 | 7,510 | 0.745 | 0.792 | 0.599 | 0.691 | 0.184 | 0.615 |  |
| archived-20261005-175214: db.jsonl | 853cfb9d36 | 0.551 | 0.536 | 7,651 | 7,651 | 0.756 | 0.817 | 0.633 | 0.708 | 0.184 | 0.632 |  |
| archived-20261005-175214: db.jsonl | fa23f401cd | 0.538 | 0.525 | 7,692 | 7,692 | 0.703 | 0.887 | 0.590 | 0.665 | 0.185 | 0.644 |  |
| archived-20261005-175214: db.jsonl | 45d2ff7e01 | 0.507 | 0.500 | 7,725 | 7,725 | 0.697 | 0.696 | 0.566 | 0.639 | 0.191 | 0.646 |  |
| archived-20261005-175214: db.jsonl | f084674b22 | 0.516 | 0.516 | 9,198 | 9,198 | 0.708 | 0.722 | 0.559 | 0.651 | 0.196 | 0.635 |  |
| archived-20261005-175214: db.jsonl | 9d89f6ba0e | 0.485 | 0.487 | 13,065 | 13,065 | 0.640 | 0.757 | 0.502 | 0.599 | 0.184 | 0.666 |  |
| archived-20261005-204503: db.jsonl | 295a6acd98 | 0.763 | 0.755 | 6,977 | 6,977 | 0.786 | 0.821 | 0.630 | 0.712 | 0.896 | 0.871 |  |
| archived-20261005-204503: db.jsonl | 82e7e4dc0d | 0.724 | 0.726 | 6,979 | 6,979 | 0.776 | 0.838 | 0.565 | 0.676 | 0.799 | 0.843 |  |
| archived-20261005-204503: db.jsonl | 9385a8fcbb | 0.692 | 0.690 | 6,994 | 6,994 | 0.709 | 0.860 | 0.540 | 0.652 | 0.738 | 0.817 |  |
| archived-20261005-204503: db.jsonl | bf413bef91 | 0.665 | 0.681 | 7,002 | 7,002 | 0.693 | 0.707 | 0.548 | 0.634 | 0.763 | 0.847 |  |
| archived-20261005-204503: db.jsonl | c25a5e1714 | 0.670 | 0.668 | 7,010 | 7,010 | 0.735 | 0.715 | 0.535 | 0.646 | 0.747 | 0.825 |  |
| archived-20261005-204503: db.jsonl | 7380e8bcb1 | 0.660 | 0.658 | 7,050 | 7,050 | 0.668 | 0.760 | 0.528 | 0.625 | 0.746 | 0.838 |  |
| archived-20261005-204503: db.jsonl | 5df0608416 | 0.661 | 0.659 | 7,059 | 7,059 | 0.667 | 0.758 | 0.538 | 0.621 | 0.748 | 0.824 |  |
| archived-20261005-204503: db.jsonl | d8d62beb78 | 0.554 | 0.545 | 7,106 | 7,106 | 0.745 | 0.878 | 0.592 | 0.693 | 0.194 | 0.659 |  |
| archived-20261005-204503: db.jsonl | f3988ea716 | 0.523 | 0.510 | 7,113 | 7,113 | 0.708 | 0.766 | 0.568 | 0.647 | 0.197 | 0.645 |  |
| archived-20261005-204503: db.jsonl | 2ed8b1583e | 0.506 | 0.509 | 7,129 | 7,129 | 0.685 | 0.790 | 0.525 | 0.619 | 0.190 | 0.610 |  |
| archived-20261005-204503: db.jsonl | 641b85143d | 0.496 | 0.501 | 7,178 | 7,178 | 0.683 | 0.755 | 0.545 | 0.606 | 0.176 | 0.594 |  |
| archived-20261005-204503: db.jsonl | 96f2d8bfd7 | 0.484 | 0.490 | 7,236 | 7,236 | 0.645 | 0.762 | 0.490 | 0.593 | 0.186 | 0.549 |  |
| archived-20261005-204503: db.jsonl | 55ca1dfdb5 | 0.505 | 0.499 | 7,550 | 7,550 | 0.670 | 0.766 | 0.547 | 0.619 | 0.188 | 0.602 |  |
| archived-20261005-204503: db.jsonl | 0e8b212e50 | 0.506 | 0.507 | 7,558 | 7,558 | 0.655 | 0.840 | 0.535 | 0.608 | 0.185 | 0.621 |  |
| archived-20261005-204503: db.jsonl | 7a8d429413 | 0.483 | 0.479 | 7,714 | 7,714 | 0.720 | 0.513 | 0.525 | 0.663 | 0.204 | 0.562 |  |
| archived-20261005-204503: db.jsonl | 85a977e3ed | 0.487 | 0.486 | 7,804 | 7,804 | 0.703 | 0.588 | 0.559 | 0.663 | 0.178 | 0.527 |  |
| archived-20261005-204503: db.jsonl | cda8cad59b | 0.485 | 0.492 | 7,949 | 7,949 | 0.739 | 0.578 | 0.516 | 0.663 | 0.184 | 0.591 |  |
| archived-20261005-204503: db.jsonl | 049e0c9c48 | 0.461 | 0.457 | 7,973 | 7,973 | 0.658 | 0.526 | 0.511 | 0.610 | 0.194 | 0.523 |  |
| archived-20261005-204503: db.jsonl | 6827e42d47 | 0.457 | 0.451 | 8,352 | 8,352 | 0.649 | 0.502 | 0.507 | 0.610 | 0.198 | 0.533 |  |
| archived-20261005-204503: db.jsonl | ff306b06c1 | 0.437 | 0.451 | 12,145 | 12,145 | 0.633 | 0.509 | 0.452 | 0.566 | 0.193 | 0.574 |  |
| archived-20261005-204503: db.jsonl | 84a09433d4 | 0.436 | 0.435 | 12,585 | 12,585 | 0.627 | 0.552 | 0.427 | 0.559 | 0.192 | 0.549 |  |
| archived-20261005-204503: db.jsonl | ff3e6b2a34 | 0.443 | 0.438 | 13,073 | 13,073 | 0.615 | 0.560 | 0.446 | 0.558 | 0.198 | 0.556 |  |
| archived-20261005-222307: db.jsonl | 7cb20d14b1 | 0.719 | 0.718 | 6,971 | 6,971 | 0.757 | 0.740 | 0.580 | 0.705 | 0.838 | 0.861 |  |
| archived-20261005-222307: db.jsonl | d0d304e240 | 0.699 | 0.684 | 6,977 | 6,977 | 0.718 | 0.815 | 0.534 | 0.639 | 0.835 | 0.863 |  |
| archived-20261005-222307: db.jsonl | 98e6135b93 | 0.682 | 0.678 | 6,978 | 6,978 | 0.660 | 0.792 | 0.517 | 0.607 | 0.897 | 0.861 |  |
| archived-20261005-222307: db.jsonl | 6ba318d95c | 0.599 | 0.601 | 6,989 | 6,989 | 0.596 | 0.719 | 0.422 | 0.521 | 0.819 | 0.860 |  |
| archived-20261005-222307: db.jsonl | 7b9675c9ef | 0.606 | 0.604 | 7,004 | 7,004 | 0.616 | 0.755 | 0.446 | 0.543 | 0.728 | 0.843 |  |
| archived-20261005-222307: db.jsonl | 31a3ceea45 | 0.593 | 0.582 | 7,037 | 7,037 | 0.588 | 0.759 | 0.438 | 0.521 | 0.719 | 0.823 |  |
| archived-20261005-222307: db.jsonl | 3f1d365b3b | 0.592 | 0.590 | 7,061 | 7,061 | 0.587 | 0.717 | 0.437 | 0.507 | 0.784 | 0.845 |  |
| archived-20261005-222307: db.jsonl | 63919635b7 | 0.503 | 0.502 | 7,089 | 7,089 | 0.668 | 0.696 | 0.512 | 0.603 | 0.224 | 0.576 |  |
| archived-20261005-222307: db.jsonl | 2c9b948725 | 0.483 | 0.481 | 7,097 | 7,097 | 0.610 | 0.960 | 0.443 | 0.520 | 0.195 | 0.656 |  |
| archived-20261005-222307: db.jsonl | cac62ca533 | 0.457 | 0.450 | 7,105 | 7,105 | 0.585 | 0.837 | 0.420 | 0.512 | 0.189 | 0.635 |  |
| archived-20261005-222307: db.jsonl | 627568164d | 0.440 | 0.447 | 7,147 | 7,147 | 0.603 | 0.700 | 0.402 | 0.516 | 0.189 | 0.624 |  |
| archived-20261005-222307: db.jsonl | 37b502fac7 | 0.435 | 0.433 | 7,238 | 7,238 | 0.575 | 0.697 | 0.410 | 0.502 | 0.188 | 0.588 |  |
| archived-20261005-222307: db.jsonl | ced47e8cfa | 0.417 | 0.406 | 8,030 | 8,030 | 0.602 | 0.475 | 0.420 | 0.524 | 0.200 | 0.573 |  |

The front of all runs together, by size: dcbaf0e29f 0.326 at 9,014, 9102e1dea9 0.331 at 7,958, 1918ae250d 0.349 at 7,820, 040e367ce9 0.349 at 7,753, 9a482dbeaf 0.355 at 7,334, 35135bde2f 0.379 at 7,105, 20b3bde0c3 0.397 at 7,097, 988d608671 0.485 at 7,014, 0f90ffc36a 0.485 at 6,998, c2d99350f1 0.490 at 6,974, 46fbc9e912 0.501 at 6,966, 2816900bac 0.646 at 6,941

## The same session on two CPUs

Calibration on cpu 2: 0.994; on cpu 8: 1.001.

Speed on cpu 2 over speed on cpu 8, per design: median 0.999, 10-90% 0.989-1.010, extremes 0.979-1.029; rank agreement (Spearman) 1.00.

The front of all runs on cpu 2: dcbaf0e29f 0.326 at 9,014, 9102e1dea9 0.331 at 7,958, 1918ae250d 0.349 at 7,820, 040e367ce9 0.349 at 7,753, 9a482dbeaf 0.355 at 7,334, 35135bde2f 0.379 at 7,105, 20b3bde0c3 0.397 at 7,097, 988d608671 0.485 at 7,014, 0f90ffc36a 0.485 at 6,998, c2d99350f1 0.490 at 6,974, 46fbc9e912 0.501 at 6,966, 2816900bac 0.646 at 6,941

The front of all runs on cpu 8: dcbaf0e29f 0.331 at 9,014, c9f3c95232 0.335 at 7,966, 9102e1dea9 0.336 at 7,958, 1918ae250d 0.341 at 7,820, 9a482dbeaf 0.349 at 7,334, 35135bde2f 0.380 at 7,105, 20b3bde0c3 0.397 at 7,097, 0f90ffc36a 0.484 at 6,998, c2d99350f1 0.493 at 6,974, 46fbc9e912 0.499 at 6,966, 2816900bac 0.656 at 6,941

On both fronts: 10 of 12 and 11.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| dcbaf0e29f | 0.326 | 0.331 | 0.983 |
| 9102e1dea9 | 0.331 | 0.336 | 0.984 |
| c9f3c95232 | 0.332 | 0.335 | 0.991 |
| 1918ae250d | 0.349 | 0.341 | 1.023 |
| 040e367ce9 | 0.349 | 0.356 | 0.981 |
| 9a482dbeaf | 0.355 | 0.349 | 1.019 |
| 35135bde2f | 0.379 | 0.380 | 0.999 |
| 20b3bde0c3 | 0.397 | 0.397 | 1.001 |
| ced47e8cfa | 0.417 | 0.414 | 1.007 |
| 37b502fac7 | 0.435 | 0.437 | 0.994 |
| 84a09433d4 | 0.436 | 0.436 | 1.001 |
| ff306b06c1 | 0.437 | 0.425 | 1.029 |
| 9bb527944a | 0.439 | 0.438 | 1.002 |
| 627568164d | 0.440 | 0.441 | 0.997 |
| ff3e6b2a34 | 0.443 | 0.441 | 1.004 |
| cac62ca533 | 0.457 | 0.459 | 0.994 |
| 6827e42d47 | 0.457 | 0.457 | 1.000 |
| 049e0c9c48 | 0.461 | 0.458 | 1.007 |
| 577c999e62 | 0.462 | 0.458 | 1.008 |
| 959e88b0f5 | 0.466 | 0.461 | 1.010 |
| 0212f86508 | 0.473 | 0.470 | 1.006 |
| 7a8d429413 | 0.483 | 0.481 | 1.004 |
| 2c9b948725 | 0.483 | 0.484 | 0.998 |
| 96f2d8bfd7 | 0.484 | 0.481 | 1.005 |
| 72ca2cf497 | 0.484 | 0.480 | 1.010 |
| 9d89f6ba0e | 0.485 | 0.492 | 0.985 |
| 988d608671 | 0.485 | 0.485 | 0.999 |
| 0f90ffc36a | 0.485 | 0.484 | 1.003 |
| cda8cad59b | 0.485 | 0.487 | 0.997 |
| 1b602bc9bd | 0.486 | 0.494 | 0.983 |
| 85a977e3ed | 0.487 | 0.492 | 0.990 |
| c2d99350f1 | 0.490 | 0.493 | 0.994 |
| aba06380d6 | 0.490 | 0.486 | 1.009 |
| 641b85143d | 0.496 | 0.500 | 0.991 |
| 46fbc9e912 | 0.501 | 0.499 | 1.003 |
| f85a63f8c7 | 0.502 | 0.504 | 0.997 |
| 63919635b7 | 0.503 | 0.496 | 1.013 |
| 85cac726b5 | 0.504 | 0.495 | 1.018 |
| 55ca1dfdb5 | 0.505 | 0.504 | 1.002 |
| 0e8b212e50 | 0.506 | 0.506 | 0.999 |
| 2ed8b1583e | 0.506 | 0.513 | 0.987 |
| 45d2ff7e01 | 0.507 | 0.506 | 1.001 |
| 51879a71f0 | 0.509 | 0.507 | 1.004 |
| f084674b22 | 0.516 | 0.515 | 1.001 |
| f3988ea716 | 0.523 | 0.513 | 1.019 |
| 3d31fd4cc4 | 0.524 | 0.523 | 1.001 |
| 6578fc6928 | 0.528 | 0.530 | 0.997 |
| 2367cb920c | 0.538 | 0.545 | 0.987 |
| caf4358de8 | 0.538 | 0.540 | 0.996 |
| fa23f401cd | 0.538 | 0.540 | 0.998 |
| be02a4c0cf | 0.548 | 0.544 | 1.007 |
| 853cfb9d36 | 0.551 | 0.554 | 0.996 |
| d8d62beb78 | 0.554 | 0.550 | 1.008 |
| cd943ed219 | 0.588 | 0.587 | 1.002 |
| a214fa731c | 0.591 | 0.600 | 0.986 |
| 3f1d365b3b | 0.592 | 0.592 | 1.001 |
| 31a3ceea45 | 0.593 | 0.589 | 1.006 |
| 15dde12f04 | 0.598 | 0.600 | 0.997 |
| 6ba318d95c | 0.599 | 0.605 | 0.991 |
| 2b00aa6e97 | 0.602 | 0.606 | 0.992 |
| dc02ceae31 | 0.605 | 0.606 | 0.999 |
| 1cf03a8fd4 | 0.605 | 0.602 | 1.005 |
| 7b9675c9ef | 0.606 | 0.607 | 0.999 |
| 3a7c3d6e90 | 0.612 | 0.609 | 1.006 |
| 4cc12fc1e7 | 0.623 | 0.628 | 0.992 |
| 27a35df3fa | 0.627 | 0.631 | 0.995 |
| ff39b37bcc | 0.637 | 0.633 | 1.006 |
| 05617039f6 | 0.643 | 0.641 | 1.003 |
| 2816900bac | 0.646 | 0.656 | 0.985 |
| 8dd8a7a146 | 0.647 | 0.641 | 1.010 |
| c61857fc89 | 0.652 | 0.658 | 0.990 |
| 3c2d8a577b | 0.652 | 0.659 | 0.989 |
| 22b81e50c4 | 0.652 | 0.655 | 0.995 |
| e99da68667 | 0.652 | 0.654 | 0.997 |
| 8a2189b3b6 | 0.654 | 0.650 | 1.006 |
| 2db525ff95 | 0.655 | 0.658 | 0.995 |
| b06a4cf784 | 0.658 | 0.658 | 1.001 |
| 1769ca2a48 | 0.659 | 0.660 | 0.997 |
| 9e50623ac1 | 0.659 | 0.656 | 1.004 |
| 29ad5ba726 | 0.659 | 0.645 | 1.022 |
| 7380e8bcb1 | 0.660 | 0.660 | 1.000 |
| 88792f1798 | 0.661 | 0.654 | 1.010 |
| 5df0608416 | 0.661 | 0.661 | 1.001 |
| a74b828e9b | 0.663 | 0.665 | 0.997 |
| af5e8dc29f | 0.664 | 0.666 | 0.997 |
| bf413bef91 | 0.665 | 0.670 | 0.992 |
| c40ba92d5b | 0.665 | 0.662 | 1.005 |
| c25a5e1714 | 0.670 | 0.674 | 0.995 |
| 0b1d16def9 | 0.672 | 0.678 | 0.992 |
| 14f6036a4b | 0.674 | 0.680 | 0.991 |
| 32600cab87 | 0.675 | 0.678 | 0.995 |
| ca2ac63866 | 0.676 | 0.681 | 0.993 |
| a306cc61fb | 0.678 | 0.672 | 1.008 |
| 4cb3fa9172 | 0.678 | 0.684 | 0.992 |
| 66eb4a8f15 | 0.681 | 0.687 | 0.991 |
| f060a4c31f | 0.681 | 0.677 | 1.005 |
| 98e6135b93 | 0.682 | 0.675 | 1.010 |
| f66d74a27c | 0.685 | 0.689 | 0.995 |
| 448ef1ef43 | 0.686 | 0.693 | 0.989 |
| 312ad2edaa | 0.687 | 0.686 | 1.002 |
| 60753a0eb0 | 0.690 | 0.697 | 0.990 |
| 9385a8fcbb | 0.692 | 0.696 | 0.994 |
| 38d187239c | 0.692 | 0.696 | 0.995 |
| e05adba602 | 0.693 | 0.694 | 1.000 |
| e0cbf09bc2 | 0.694 | 0.699 | 0.993 |
| 9f5e6d173c | 0.694 | 0.692 | 1.002 |
| 49b0a93f14 | 0.696 | 0.688 | 1.012 |
| 12d8e18511 | 0.698 | 0.708 | 0.985 |
| a27aa49d8e | 0.698 | 0.691 | 1.010 |
| 6495dcb5dd | 0.698 | 0.700 | 0.997 |
| bb8a0cb575 | 0.699 | 0.698 | 1.000 |
| d0d304e240 | 0.699 | 0.695 | 1.005 |
| 52b80007a1 | 0.700 | 0.708 | 0.988 |
| ccce4784b8 | 0.701 | 0.690 | 1.016 |
| c297551359 | 0.707 | 0.705 | 1.002 |
| 6463752a82 | 0.707 | 0.710 | 0.996 |
| 38d91795a2 | 0.709 | 0.714 | 0.993 |
| 5ed1ed8715 | 0.709 | 0.710 | 1.000 |
| ee4d8f8a50 | 0.711 | 0.726 | 0.979 |
| d4739aac88 | 0.718 | 0.726 | 0.988 |
| 7cb20d14b1 | 0.719 | 0.721 | 0.998 |
| 84e302c470 | 0.721 | 0.718 | 1.005 |
| 7fe7f039bd | 0.722 | 0.725 | 0.996 |
| 82e7e4dc0d | 0.724 | 0.724 | 1.000 |
| 8cbc6dd05c | 0.724 | 0.728 | 0.995 |
| f4a6dd9a13 | 0.725 | 0.727 | 0.998 |
| e8f1dd3ca2 | 0.730 | 0.721 | 1.012 |
| 53ec9bedde | 0.730 | 0.734 | 0.995 |
| 8dc0f97f2c | 0.730 | 0.725 | 1.007 |
| f052397620 | 0.730 | 0.717 | 1.019 |
| a285fa6ba3 | 0.732 | 0.735 | 0.997 |
| 57a9dcc7cb | 0.733 | 0.734 | 0.999 |
| 422d6bcbca | 0.738 | 0.731 | 1.009 |
| 090672993b | 0.738 | 0.738 | 1.000 |
| 05dcc81cdc | 0.743 | 0.742 | 1.001 |
| 550df563ee | 0.745 | 0.740 | 1.007 |
| 3453246bdf | 0.747 | 0.750 | 0.996 |
| 595fc2b8f4 | 0.748 | 0.758 | 0.988 |
| 528fc9619a | 0.753 | 0.752 | 1.001 |
| 57e0e77c09 | 0.755 | 0.754 | 1.001 |
| 9cd791dd84 | 0.755 | 0.760 | 0.993 |
| 4032a5ce71 | 0.759 | 0.759 | 1.001 |
| 57d12a1bb0 | 0.763 | 0.749 | 1.019 |
| 295a6acd98 | 0.763 | 0.766 | 0.996 |
| 6738aed13f | 0.764 | 0.752 | 1.016 |
| 3781c5e756 | 0.765 | 0.761 | 1.005 |
| 0ebf0445e0 | 0.767 | 0.773 | 0.993 |
| 4f010d8ab9 | 0.769 | 0.758 | 1.015 |
| 90018981c6 | 0.770 | 0.779 | 0.988 |
| 5b70f3dd64 | 0.771 | 0.768 | 1.004 |
| 98736f0596 | 0.777 | 0.778 | 0.999 |
| c17103bf95 | 0.780 | 0.786 | 0.993 |
| c513ef17b0 | 0.787 | 0.781 | 1.008 |
| a4e82e02e5 | 0.799 | 0.807 | 0.991 |
| 672538daf5 | 0.823 | 0.830 | 0.992 |
| 83cb81c383 | 0.844 | 0.832 | 1.014 |
| f41ab1810d | 1.010 | 1.008 | 1.002 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 11 - Iteration 56: seeds 1-13, after seed 13 (the input side)

`seed 13 then experiment compare-fronts.py --rounds 10 --cpus 2,8`, commit
5bc9190b: fifteen databases, 173 front designs, five workloads, sieve held
out. Nineteen minutes. **Calibration 0.994** (parse 0.980, the rest
0.988-1.010). The CPUs agree: per design median 1.002, 10-90% 0.990-1.012,
ranks 1.00; 9 of 10 and 11 designs on both CPUs' fronts.

**The front of all runs: seed 13's ten**, 6,903 bytes (0.436) to 7,799
(0.284, the fastest yet); nothing larger is on it.

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 0.994** (kernel 1.007, fib 0.988, parse 0.980, corpus 1.002, loop 0.995, sieve 1.010).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 5347899701 | 0.436 | 0.431 | 6,903 | 6,903 | 0.419 | 0.785 | 0.180 | 0.331 | 0.800 | 0.818 | yes |
| this clone: db.jsonl | 097ff5bdce | 0.418 | 0.406 | 6,913 | 6,913 | 0.414 | 0.744 | 0.175 | 0.327 | 0.721 | 0.788 | yes |
| this clone: db.jsonl | 520f651e31 | 0.411 | 0.406 | 6,914 | 6,914 | 0.407 | 0.723 | 0.179 | 0.330 | 0.677 | 0.786 | yes |
| this clone: db.jsonl | e973e9ada8 | 0.413 | 0.405 | 6,940 | 6,940 | 0.419 | 0.741 | 0.184 | 0.320 | 0.655 | 0.766 |  |
| this clone: db.jsonl | 403bda0b3f | 0.329 | 0.315 | 7,017 | 7,017 | 0.429 | 0.773 | 0.181 | 0.331 | 0.192 | 0.568 | yes |
| this clone: db.jsonl | ccf0eb9891 | 0.334 | 0.324 | 7,068 | 7,068 | 0.421 | 0.729 | 0.178 | 0.329 | 0.233 | 0.575 |  |
| this clone: db.jsonl | 1a5dc48b9c | 0.317 | 0.308 | 7,092 | 7,092 | 0.356 | 0.844 | 0.170 | 0.293 | 0.214 | 0.537 | yes |
| this clone: db.jsonl | bdb87d827e | 0.319 | 0.304 | 7,124 | 7,124 | 0.387 | 0.935 | 0.157 | 0.292 | 0.197 | 0.513 |  |
| this clone: db.jsonl | ed927db5ce | 0.317 | 0.304 | 7,132 | 7,132 | 0.393 | 0.908 | 0.159 | 0.296 | 0.192 | 0.582 |  |
| this clone: db.jsonl | 76684cada6 | 0.304 | 0.303 | 7,166 | 7,166 | 0.379 | 0.791 | 0.157 | 0.298 | 0.185 | 0.542 | yes |
| this clone: db.jsonl | 103cbedc80 | 0.298 | 0.290 | 7,238 | 7,238 | 0.368 | 0.768 | 0.162 | 0.286 | 0.179 | 0.530 | yes |
| this clone: db.jsonl | 9c85c7d9f5 | 0.297 | 0.280 | 7,246 | 7,246 | 0.376 | 0.726 | 0.164 | 0.284 | 0.184 | 0.533 | yes |
| this clone: db.jsonl | 3218bf9f21 | 0.293 | 0.287 | 7,666 | 7,666 | 0.359 | 0.751 | 0.162 | 0.286 | 0.172 | 0.565 | yes |
| this clone: db.jsonl | cd8075731e | 0.293 | 0.278 | 7,773 | 7,773 | 0.404 | 0.551 | 0.161 | 0.305 | 0.198 | 0.470 |  |
| this clone: db.jsonl | ad62971982 | 0.284 | 0.268 | 7,799 | 7,799 | 0.381 | 0.612 | 0.151 | 0.290 | 0.180 | 0.481 | yes |
| this clone: db.jsonl | db3dcdb1f8 | 0.289 | 0.272 | 10,181 | 10,181 | 0.387 | 0.582 | 0.159 | 0.299 | 0.187 | 0.565 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 595fc2b8f4 | 0.764 | 0.784 | 9,662 | 9,761 | 0.747 | 0.722 | 0.643 | 0.711 | 1.056 | 0.829 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 8cbc6dd05c | 0.723 | 0.742 | 9,694 | 9,809 | 0.716 | 0.783 | 0.600 | 0.672 | 0.872 | 0.809 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 6738aed13f | 0.758 | 0.755 | 9,694 | 9,793 | 0.738 | 0.671 | 0.650 | 0.720 | 1.080 | 0.856 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 312ad2edaa | 0.691 | 0.716 | 13,344 | 13,456 | 0.713 | 0.723 | 0.551 | 0.623 | 0.892 | 0.856 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 05617039f6 | 0.642 | 0.674 | 13,352 | 13,488 | 0.678 | 0.786 | 0.478 | 0.595 | 0.719 | 0.812 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 0b1d16def9 | 0.675 | 0.705 | 13,352 | 13,464 | 0.711 | 0.797 | 0.493 | 0.623 | 0.809 | 0.867 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 57a9dcc7cb | 0.738 | 0.680 | 13,368 | 13,480 | 0.717 | 0.913 | 0.539 | 0.650 | 0.956 | 0.884 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 32600cab87 | 0.680 | 0.662 | 13,528 | 13,656 | 0.680 | 0.954 | 0.523 | 0.614 | 0.697 | 0.838 |  |
| archived-20261004-200423: db-seed1.jsonl | 83cb81c383 | 0.835 | 0.705 | 9,662 | 9,761 | 0.771 | 1.002 | 0.683 | 0.737 | 1.041 | 0.923 |  |
| archived-20261004-200423: db-seed1.jsonl | 5b70f3dd64 | 0.763 | 0.649 | 9,694 | 9,801 | 0.738 | 0.945 | 0.640 | 0.675 | 0.857 | 0.808 |  |
| archived-20261004-200423: db-seed1.jsonl | a4e82e02e5 | 0.803 | 0.654 | 9,694 | 9,809 | 0.768 | 0.906 | 0.669 | 0.719 | 0.995 | 0.893 |  |
| archived-20261004-200423: db-seed1.jsonl | 53ec9bedde | 0.728 | 0.670 | 13,336 | 13,464 | 0.755 | 0.752 | 0.616 | 0.687 | 0.853 | 0.837 |  |
| archived-20261004-200423: db-seed1.jsonl | 38d187239c | 0.694 | 0.609 | 13,368 | 13,480 | 0.711 | 0.842 | 0.543 | 0.634 | 0.782 | 0.836 |  |
| archived-20261004-200423: db-seed1.jsonl | 448ef1ef43 | 0.697 | 0.620 | 13,368 | 13,488 | 0.682 | 0.954 | 0.516 | 0.613 | 0.801 | 0.836 |  |
| archived-20261004-200423: db-seed2.jsonl | 0ebf0445e0 | 0.776 | 0.667 | 9,662 | 9,761 | 0.792 | 0.706 | 0.691 | 0.733 | 0.992 | 0.869 |  |
| archived-20261004-200423: db-seed2.jsonl | c17103bf95 | 0.785 | 0.725 | 9,662 | 9,769 | 0.790 | 0.777 | 0.698 | 0.764 | 0.912 | 0.883 |  |
| archived-20261004-200423: db-seed2.jsonl | a285fa6ba3 | 0.741 | 0.666 | 13,352 | 13,464 | 0.759 | 0.707 | 0.630 | 0.714 | 0.927 | 0.875 |  |
| archived-20261004-200423: db-seed2.jsonl | 57e0e77c09 | 0.757 | 0.657 | 13,352 | 13,480 | 0.722 | 1.041 | 0.545 | 0.647 | 0.938 | 0.874 |  |
| archived-20261004-200423: db-seed2.jsonl | 9cd791dd84 | 0.759 | 0.619 | 13,368 | 13,472 | 0.736 | 0.905 | 0.573 | 0.675 | 0.975 | 0.895 |  |
| archived-20261004-200423: db.jsonl | 550df563ee | 0.734 | 0.696 | 9,646 | 9,745 | 0.706 | 0.748 | 0.615 | 0.675 | 0.975 | 0.841 |  |
| archived-20261004-200423: db.jsonl | f4a6dd9a13 | 0.727 | 0.683 | 9,662 | 9,761 | 0.745 | 0.663 | 0.605 | 0.693 | 0.977 | 0.781 |  |
| archived-20261004-200423: db.jsonl | 60753a0eb0 | 0.690 | 0.622 | 9,686 | 9,785 | 0.690 | 0.665 | 0.566 | 0.668 | 0.904 | 0.799 |  |
| archived-20261004-200423: db.jsonl | 8dd8a7a146 | 0.649 | 0.595 | 13,352 | 13,464 | 0.645 | 0.667 | 0.516 | 0.602 | 0.862 | 0.814 |  |
| archived-20261004-214724: db.jsonl | 3453246bdf | 0.752 | 0.727 | 9,335 | 9,335 | 0.780 | 0.694 | 0.663 | 0.747 | 0.899 | 0.873 |  |
| archived-20261004-214724: db.jsonl | 672538daf5 | 0.823 | 0.780 | 9,351 | 9,351 | 0.817 | 0.838 | 0.704 | 0.776 | 1.009 | 0.880 |  |
| archived-20261004-214724: db.jsonl | 7fe7f039bd | 0.715 | 0.702 | 9,450 | 9,450 | 0.750 | 0.688 | 0.618 | 0.715 | 0.822 | 0.860 |  |
| archived-20261004-214724: db.jsonl | 38d91795a2 | 0.707 | 0.678 | 9,474 | 9,474 | 0.741 | 0.655 | 0.604 | 0.705 | 0.854 | 0.860 |  |
| archived-20261004-214724: db.jsonl | 6463752a82 | 0.711 | 0.669 | 9,523 | 9,523 | 0.718 | 0.724 | 0.585 | 0.672 | 0.887 | 0.867 |  |
| archived-20261004-214724: db.jsonl | 90018981c6 | 0.786 | 0.696 | 9,678 | 9,678 | 0.754 | 0.804 | 0.672 | 0.730 | 1.007 | 0.887 |  |
| archived-20261004-214724: db.jsonl | e0cbf09bc2 | 0.699 | 0.666 | 13,057 | 13,057 | 0.693 | 0.761 | 0.527 | 0.644 | 0.931 | 0.869 |  |
| archived-20261004-214724: db.jsonl | 1769ca2a48 | 0.659 | 0.603 | 13,209 | 13,209 | 0.695 | 0.603 | 0.530 | 0.644 | 0.872 | 0.823 |  |
| archived-20261004-214724: db.jsonl | 14f6036a4b | 0.681 | 0.627 | 13,217 | 13,217 | 0.671 | 0.833 | 0.481 | 0.598 | 0.913 | 0.910 |  |
| archived-20261004-214724: db.jsonl | 29ad5ba726 | 0.642 | 0.589 | 13,352 | 13,352 | 0.659 | 0.758 | 0.487 | 0.571 | 0.784 | 0.834 |  |
| archived-20261004-214724: db.jsonl | 12d8e18511 | 0.709 | 0.667 | 13,360 | 13,360 | 0.688 | 0.846 | 0.533 | 0.624 | 0.928 | 0.959 |  |
| archived-20261005-013645: db.jsonl | 05dcc81cdc | 0.740 | 0.688 | 9,335 | 9,335 | 0.727 | 0.795 | 0.606 | 0.691 | 0.919 | 0.876 |  |
| archived-20261005-013645: db.jsonl | c297551359 | 0.706 | 0.682 | 9,450 | 9,450 | 0.725 | 0.666 | 0.630 | 0.703 | 0.821 | 0.859 |  |
| archived-20261005-013645: db.jsonl | e8f1dd3ca2 | 0.736 | 0.678 | 9,458 | 9,458 | 0.698 | 0.816 | 0.594 | 0.668 | 0.959 | 0.900 |  |
| archived-20261005-013645: db.jsonl | 66eb4a8f15 | 0.687 | 0.641 | 13,057 | 13,057 | 0.709 | 0.684 | 0.531 | 0.651 | 0.912 | 0.870 |  |
| archived-20261005-013645: db.jsonl | 84e302c470 | 0.722 | 0.657 | 13,065 | 13,065 | 0.726 | 0.757 | 0.542 | 0.650 | 1.014 | 0.915 |  |
| archived-20261005-013645: db.jsonl | 4cb3fa9172 | 0.687 | 0.626 | 13,073 | 13,073 | 0.653 | 0.819 | 0.485 | 0.604 | 0.975 | 0.893 |  |
| archived-20261005-013645: db.jsonl | e99da68667 | 0.654 | 0.581 | 13,201 | 13,201 | 0.617 | 0.769 | 0.453 | 0.560 | 0.995 | 0.860 |  |
| archived-20261005-042924: db.jsonl | 98736f0596 | 0.783 | 0.731 | 9,335 | 9,335 | 0.794 | 0.733 | 0.674 | 0.747 | 1.007 | 0.901 |  |
| archived-20261005-042924: db.jsonl | 4f010d8ab9 | 0.769 | 0.721 | 9,343 | 9,343 | 0.785 | 0.737 | 0.643 | 0.718 | 1.010 | 0.897 |  |
| archived-20261005-042924: db.jsonl | 4032a5ce71 | 0.753 | 0.698 | 9,351 | 9,351 | 0.771 | 0.776 | 0.597 | 0.706 | 0.959 | 0.945 |  |
| archived-20261005-042924: db.jsonl | 528fc9619a | 0.751 | 0.702 | 9,359 | 9,359 | 0.758 | 0.763 | 0.598 | 0.701 | 0.986 | 0.876 |  |
| archived-20261005-042924: db.jsonl | f052397620 | 0.727 | 0.685 | 9,450 | 9,450 | 0.719 | 0.807 | 0.582 | 0.681 | 0.887 | 0.903 |  |
| archived-20261005-042924: db.jsonl | 8dc0f97f2c | 0.722 | 0.680 | 9,458 | 9,458 | 0.721 | 0.756 | 0.588 | 0.676 | 0.907 | 0.871 |  |
| archived-20261005-042924: db.jsonl | 52b80007a1 | 0.700 | 0.640 | 10,010 | 10,010 | 0.738 | 0.546 | 0.595 | 0.702 | 1.001 | 0.858 |  |
| archived-20261005-042924: db.jsonl | 5ed1ed8715 | 0.707 | 0.642 | 10,018 | 10,018 | 0.742 | 0.545 | 0.619 | 0.704 | 1.002 | 0.859 |  |
| archived-20261005-042924: db.jsonl | 9e50623ac1 | 0.657 | 0.593 | 13,073 | 13,073 | 0.668 | 0.708 | 0.480 | 0.588 | 0.914 | 0.851 |  |
| archived-20261005-042924: db.jsonl | 22b81e50c4 | 0.655 | 0.605 | 13,209 | 13,209 | 0.640 | 0.884 | 0.421 | 0.553 | 0.919 | 0.885 |  |
| archived-20261005-042924: db.jsonl | 2db525ff95 | 0.643 | 0.579 | 14,017 | 14,017 | 0.645 | 0.684 | 0.440 | 0.583 | 0.968 | 0.918 |  |
| archived-20261005-131253: db.jsonl | 422d6bcbca | 0.736 | 0.699 | 9,327 | 9,327 | 0.747 | 0.863 | 0.537 | 0.653 | 0.958 | 0.869 |  |
| archived-20261005-131253: db.jsonl | 090672993b | 0.737 | 0.700 | 9,335 | 9,335 | 0.707 | 0.812 | 0.637 | 0.678 | 0.877 | 0.776 |  |
| archived-20261005-131253: db.jsonl | 6495dcb5dd | 0.693 | 0.662 | 9,343 | 9,343 | 0.670 | 0.918 | 0.514 | 0.623 | 0.811 | 0.800 |  |
| archived-20261005-131253: db.jsonl | c40ba92d5b | 0.671 | 0.630 | 9,511 | 9,511 | 0.675 | 0.695 | 0.565 | 0.641 | 0.802 | 0.796 |  |
| archived-20261005-131253: db.jsonl | ca2ac63866 | 0.684 | 0.634 | 9,531 | 9,531 | 0.660 | 0.738 | 0.562 | 0.615 | 0.892 | 0.855 |  |
| archived-20261005-131253: db.jsonl | c61857fc89 | 0.654 | 0.633 | 10,034 | 10,034 | 0.680 | 0.703 | 0.537 | 0.630 | 0.738 | 0.857 |  |
| archived-20261005-131253: db.jsonl | b06a4cf784 | 0.660 | 0.615 | 10,246 | 10,246 | 0.638 | 0.702 | 0.534 | 0.605 | 0.863 | 0.833 |  |
| archived-20261005-131253: db.jsonl | af5e8dc29f | 0.661 | 0.604 | 10,254 | 10,254 | 0.642 | 0.691 | 0.523 | 0.622 | 0.872 | 0.835 |  |
| archived-20261005-131253: db.jsonl | a74b828e9b | 0.668 | 0.608 | 13,073 | 13,073 | 0.688 | 0.630 | 0.512 | 0.622 | 0.962 | 0.839 |  |
| archived-20261005-131253: db.jsonl | dc02ceae31 | 0.610 | 0.560 | 13,161 | 13,161 | 0.614 | 0.717 | 0.440 | 0.551 | 0.789 | 0.842 |  |
| archived-20261005-131253: db.jsonl | 15dde12f04 | 0.597 | 0.567 | 13,345 | 13,345 | 0.620 | 0.760 | 0.399 | 0.533 | 0.757 | 0.812 |  |
| archived-20261005-131253: db.jsonl | cd943ed219 | 0.589 | 0.545 | 14,081 | 14,081 | 0.627 | 0.685 | 0.391 | 0.548 | 0.770 | 0.806 |  |
| archived-20261005-144844: db.jsonl | 49b0a93f14 | 0.693 | 0.688 | 8,073 | 8,073 | 0.714 | 0.886 | 0.547 | 0.653 | 0.709 | 0.844 |  |
| archived-20261005-144844: db.jsonl | 9f5e6d173c | 0.690 | 0.650 | 8,074 | 8,074 | 0.664 | 0.897 | 0.521 | 0.614 | 0.821 | 0.825 |  |
| archived-20261005-144844: db.jsonl | f060a4c31f | 0.684 | 0.637 | 8,289 | 8,289 | 0.646 | 0.842 | 0.527 | 0.600 | 0.872 | 0.800 |  |
| archived-20261005-144844: db.jsonl | a306cc61fb | 0.670 | 0.615 | 8,305 | 8,305 | 0.675 | 0.633 | 0.558 | 0.611 | 0.925 | 0.816 |  |
| archived-20261005-144844: db.jsonl | 3c2d8a577b | 0.657 | 0.603 | 8,306 | 8,306 | 0.668 | 0.633 | 0.532 | 0.614 | 0.883 | 0.793 |  |
| archived-20261005-144844: db.jsonl | 4cc12fc1e7 | 0.624 | 0.561 | 8,957 | 8,957 | 0.625 | 0.555 | 0.499 | 0.592 | 0.926 | 0.771 |  |
| archived-20261005-144844: db.jsonl | 3a7c3d6e90 | 0.606 | 0.551 | 11,777 | 11,777 | 0.605 | 0.862 | 0.358 | 0.524 | 0.836 | 0.861 |  |
| archived-20261005-144844: db.jsonl | 2b00aa6e97 | 0.609 | 0.568 | 12,145 | 12,145 | 0.604 | 0.867 | 0.363 | 0.535 | 0.826 | 0.871 |  |
| archived-20261005-144844: db.jsonl | 27a35df3fa | 0.629 | 0.570 | 12,312 | 12,312 | 0.627 | 0.581 | 0.490 | 0.587 | 0.941 | 0.778 |  |
| archived-20261005-144844: db.jsonl | ff39b37bcc | 0.633 | 0.572 | 12,584 | 12,584 | 0.635 | 0.626 | 0.464 | 0.574 | 0.961 | 0.825 |  |
| archived-20261005-144844: db.jsonl | 1cf03a8fd4 | 0.609 | 0.545 | 12,608 | 12,608 | 0.605 | 0.686 | 0.407 | 0.540 | 0.916 | 0.824 |  |
| archived-20261005-144844: db.jsonl | a214fa731c | 0.594 | 0.557 | 12,664 | 12,664 | 0.631 | 0.610 | 0.438 | 0.568 | 0.773 | 0.767 |  |
| archived-20261005-164554: db.jsonl | f41ab1810d | 1.009 | 1.008 | 8,034 | 8,034 | 1.018 | 1.251 | 0.816 | 0.914 | 1.100 | 1.150 |  |
| archived-20261005-164554: db.jsonl | 3781c5e756 | 0.759 | 0.758 | 8,041 | 8,041 | 0.763 | 0.936 | 0.596 | 0.703 | 0.840 | 0.853 |  |
| archived-20261005-164554: db.jsonl | d4739aac88 | 0.719 | 0.723 | 8,042 | 8,042 | 0.789 | 0.719 | 0.637 | 0.728 | 0.731 | 0.891 |  |
| archived-20261005-164554: db.jsonl | e05adba602 | 0.696 | 0.687 | 8,082 | 8,082 | 0.725 | 0.774 | 0.547 | 0.664 | 0.801 | 0.824 |  |
| archived-20261005-164554: db.jsonl | bb8a0cb575 | 0.690 | 0.688 | 8,099 | 8,099 | 0.754 | 0.755 | 0.543 | 0.692 | 0.730 | 0.828 |  |
| archived-20261005-164554: db.jsonl | a27aa49d8e | 0.704 | 0.693 | 8,163 | 8,163 | 0.688 | 0.855 | 0.523 | 0.633 | 0.888 | 0.860 |  |
| archived-20261005-164554: db.jsonl | 8a2189b3b6 | 0.660 | 0.646 | 8,171 | 8,171 | 0.677 | 0.764 | 0.514 | 0.617 | 0.764 | 0.848 |  |
| archived-20261005-164554: db.jsonl | f66d74a27c | 0.686 | 0.682 | 8,210 | 8,210 | 0.693 | 0.886 | 0.519 | 0.616 | 0.775 | 0.819 |  |
| archived-20261005-164554: db.jsonl | be02a4c0cf | 0.544 | 0.533 | 8,525 | 8,525 | 0.764 | 0.776 | 0.604 | 0.702 | 0.190 | 0.606 |  |
| archived-20261005-164554: db.jsonl | caf4358de8 | 0.537 | 0.514 | 8,540 | 8,540 | 0.777 | 0.756 | 0.591 | 0.698 | 0.184 | 0.623 |  |
| archived-20261005-164554: db.jsonl | 6578fc6928 | 0.522 | 0.515 | 8,548 | 8,548 | 0.698 | 0.770 | 0.526 | 0.634 | 0.217 | 0.611 |  |
| archived-20261005-164554: db.jsonl | 3d31fd4cc4 | 0.524 | 0.502 | 8,550 | 8,550 | 0.710 | 0.864 | 0.508 | 0.622 | 0.203 | 0.668 |  |
| archived-20261005-164554: db.jsonl | 85cac726b5 | 0.502 | 0.484 | 8,614 | 8,614 | 0.649 | 0.826 | 0.533 | 0.597 | 0.187 | 0.620 |  |
| archived-20261005-164554: db.jsonl | f85a63f8c7 | 0.505 | 0.481 | 8,647 | 8,647 | 0.648 | 0.860 | 0.536 | 0.601 | 0.183 | 0.610 |  |
| archived-20261005-164554: db.jsonl | 51879a71f0 | 0.507 | 0.513 | 8,664 | 8,664 | 0.683 | 0.749 | 0.561 | 0.638 | 0.183 | 0.651 |  |
| archived-20261005-164554: db.jsonl | 1b602bc9bd | 0.497 | 0.478 | 8,671 | 8,671 | 0.669 | 0.793 | 0.488 | 0.600 | 0.196 | 0.588 |  |
| archived-20261005-164554: db.jsonl | 72ca2cf497 | 0.476 | 0.469 | 8,990 | 8,990 | 0.653 | 0.664 | 0.506 | 0.596 | 0.187 | 0.525 |  |
| archived-20261005-164554: db.jsonl | 959e88b0f5 | 0.470 | 0.458 | 9,140 | 9,140 | 0.669 | 0.543 | 0.518 | 0.631 | 0.192 | 0.536 |  |
| archived-20261005-164554: db.jsonl | 577c999e62 | 0.465 | 0.443 | 9,278 | 9,278 | 0.640 | 0.555 | 0.506 | 0.606 | 0.198 | 0.527 |  |
| archived-20261005-164554: db.jsonl | aba06380d6 | 0.488 | 0.462 | 12,353 | 12,353 | 0.644 | 0.766 | 0.491 | 0.594 | 0.193 | 0.637 |  |
| archived-20261005-164554: db.jsonl | 0212f86508 | 0.476 | 0.453 | 12,377 | 12,377 | 0.643 | 0.790 | 0.448 | 0.557 | 0.194 | 0.598 |  |
| archived-20261005-164554: db.jsonl | 9bb527944a | 0.435 | 0.430 | 13,073 | 13,073 | 0.617 | 0.557 | 0.422 | 0.558 | 0.193 | 0.557 |  |
| archived-20261005-175214: db.jsonl | c513ef17b0 | 0.790 | 0.781 | 7,019 | 7,019 | 0.846 | 0.763 | 0.626 | 0.761 | 0.999 | 0.872 |  |
| archived-20261005-175214: db.jsonl | 57d12a1bb0 | 0.760 | 0.756 | 7,020 | 7,020 | 0.766 | 0.899 | 0.610 | 0.722 | 0.835 | 0.844 |  |
| archived-20261005-175214: db.jsonl | ee4d8f8a50 | 0.719 | 0.723 | 7,027 | 7,027 | 0.781 | 0.740 | 0.621 | 0.701 | 0.763 | 0.853 |  |
| archived-20261005-175214: db.jsonl | ccce4784b8 | 0.688 | 0.681 | 7,091 | 7,091 | 0.745 | 0.720 | 0.615 | 0.691 | 0.678 | 0.841 |  |
| archived-20261005-175214: db.jsonl | 88792f1798 | 0.659 | 0.653 | 7,220 | 7,220 | 0.688 | 0.740 | 0.551 | 0.638 | 0.693 | 0.800 |  |
| archived-20261005-175214: db.jsonl | 2367cb920c | 0.548 | 0.538 | 7,510 | 7,510 | 0.745 | 0.797 | 0.619 | 0.695 | 0.194 | 0.617 |  |
| archived-20261005-175214: db.jsonl | 853cfb9d36 | 0.548 | 0.536 | 7,651 | 7,651 | 0.746 | 0.823 | 0.625 | 0.690 | 0.187 | 0.619 |  |
| archived-20261005-175214: db.jsonl | fa23f401cd | 0.530 | 0.525 | 7,692 | 7,692 | 0.708 | 0.843 | 0.612 | 0.666 | 0.172 | 0.640 |  |
| archived-20261005-175214: db.jsonl | 45d2ff7e01 | 0.510 | 0.500 | 7,725 | 7,725 | 0.695 | 0.728 | 0.562 | 0.642 | 0.190 | 0.652 |  |
| archived-20261005-175214: db.jsonl | f084674b22 | 0.510 | 0.516 | 9,198 | 9,198 | 0.703 | 0.723 | 0.579 | 0.655 | 0.179 | 0.638 |  |
| archived-20261005-175214: db.jsonl | 9d89f6ba0e | 0.499 | 0.487 | 13,065 | 13,065 | 0.680 | 0.790 | 0.499 | 0.617 | 0.187 | 0.655 |  |
| archived-20261005-204503: db.jsonl | 295a6acd98 | 0.762 | 0.755 | 6,977 | 6,977 | 0.790 | 0.831 | 0.620 | 0.712 | 0.884 | 0.875 |  |
| archived-20261005-204503: db.jsonl | 82e7e4dc0d | 0.728 | 0.726 | 6,979 | 6,979 | 0.774 | 0.823 | 0.580 | 0.693 | 0.798 | 0.846 |  |
| archived-20261005-204503: db.jsonl | 9385a8fcbb | 0.693 | 0.690 | 6,994 | 6,994 | 0.713 | 0.874 | 0.553 | 0.636 | 0.728 | 0.838 |  |
| archived-20261005-204503: db.jsonl | bf413bef91 | 0.671 | 0.681 | 7,002 | 7,002 | 0.707 | 0.707 | 0.534 | 0.643 | 0.792 | 0.828 |  |
| archived-20261005-204503: db.jsonl | c25a5e1714 | 0.671 | 0.668 | 7,010 | 7,010 | 0.744 | 0.708 | 0.540 | 0.643 | 0.744 | 0.848 |  |
| archived-20261005-204503: db.jsonl | 7380e8bcb1 | 0.673 | 0.658 | 7,050 | 7,050 | 0.689 | 0.760 | 0.535 | 0.626 | 0.789 | 0.817 |  |
| archived-20261005-204503: db.jsonl | 5df0608416 | 0.662 | 0.659 | 7,059 | 7,059 | 0.672 | 0.760 | 0.529 | 0.629 | 0.748 | 0.816 |  |
| archived-20261005-204503: db.jsonl | d8d62beb78 | 0.554 | 0.545 | 7,106 | 7,106 | 0.746 | 0.873 | 0.599 | 0.689 | 0.193 | 0.652 |  |
| archived-20261005-204503: db.jsonl | f3988ea716 | 0.519 | 0.510 | 7,113 | 7,113 | 0.706 | 0.759 | 0.570 | 0.646 | 0.191 | 0.630 |  |
| archived-20261005-204503: db.jsonl | 2ed8b1583e | 0.511 | 0.509 | 7,129 | 7,129 | 0.701 | 0.797 | 0.518 | 0.623 | 0.192 | 0.607 |  |
| archived-20261005-204503: db.jsonl | 641b85143d | 0.503 | 0.501 | 7,178 | 7,178 | 0.673 | 0.747 | 0.539 | 0.624 | 0.190 | 0.588 |  |
| archived-20261005-204503: db.jsonl | 96f2d8bfd7 | 0.490 | 0.490 | 7,236 | 7,236 | 0.638 | 0.759 | 0.508 | 0.605 | 0.189 | 0.546 |  |
| archived-20261005-204503: db.jsonl | 55ca1dfdb5 | 0.501 | 0.499 | 7,550 | 7,550 | 0.671 | 0.762 | 0.528 | 0.622 | 0.188 | 0.585 |  |
| archived-20261005-204503: db.jsonl | 0e8b212e50 | 0.511 | 0.507 | 7,558 | 7,558 | 0.644 | 0.867 | 0.542 | 0.608 | 0.188 | 0.629 |  |
| archived-20261005-204503: db.jsonl | 7a8d429413 | 0.484 | 0.479 | 7,714 | 7,714 | 0.725 | 0.521 | 0.539 | 0.647 | 0.202 | 0.557 |  |
| archived-20261005-204503: db.jsonl | 85a977e3ed | 0.488 | 0.486 | 7,804 | 7,804 | 0.698 | 0.586 | 0.561 | 0.661 | 0.183 | 0.534 |  |
| archived-20261005-204503: db.jsonl | cda8cad59b | 0.490 | 0.492 | 7,949 | 7,949 | 0.724 | 0.573 | 0.538 | 0.663 | 0.192 | 0.600 |  |
| archived-20261005-204503: db.jsonl | 049e0c9c48 | 0.460 | 0.457 | 7,973 | 7,973 | 0.665 | 0.502 | 0.514 | 0.614 | 0.196 | 0.511 |  |
| archived-20261005-204503: db.jsonl | 6827e42d47 | 0.458 | 0.451 | 8,352 | 8,352 | 0.648 | 0.500 | 0.516 | 0.612 | 0.196 | 0.541 |  |
| archived-20261005-204503: db.jsonl | ff306b06c1 | 0.437 | 0.451 | 12,145 | 12,145 | 0.625 | 0.507 | 0.455 | 0.573 | 0.193 | 0.559 |  |
| archived-20261005-204503: db.jsonl | 84a09433d4 | 0.439 | 0.435 | 12,585 | 12,585 | 0.628 | 0.554 | 0.432 | 0.557 | 0.194 | 0.542 |  |
| archived-20261005-204503: db.jsonl | ff3e6b2a34 | 0.440 | 0.438 | 13,073 | 13,073 | 0.627 | 0.553 | 0.440 | 0.553 | 0.195 | 0.550 |  |
| archived-20261005-222307: db.jsonl | 7cb20d14b1 | 0.721 | 0.718 | 6,971 | 6,971 | 0.784 | 0.765 | 0.588 | 0.689 | 0.804 | 0.889 |  |
| archived-20261005-222307: db.jsonl | d0d304e240 | 0.696 | 0.684 | 6,977 | 6,977 | 0.728 | 0.795 | 0.529 | 0.655 | 0.816 | 0.863 |  |
| archived-20261005-222307: db.jsonl | 98e6135b93 | 0.679 | 0.678 | 6,978 | 6,978 | 0.675 | 0.777 | 0.502 | 0.606 | 0.903 | 0.848 |  |
| archived-20261005-222307: db.jsonl | 6ba318d95c | 0.601 | 0.601 | 6,989 | 6,989 | 0.605 | 0.734 | 0.421 | 0.517 | 0.809 | 0.852 |  |
| archived-20261005-222307: db.jsonl | 7b9675c9ef | 0.606 | 0.604 | 7,004 | 7,004 | 0.617 | 0.757 | 0.439 | 0.550 | 0.722 | 0.822 |  |
| archived-20261005-222307: db.jsonl | 31a3ceea45 | 0.589 | 0.582 | 7,037 | 7,037 | 0.598 | 0.742 | 0.432 | 0.518 | 0.717 | 0.827 |  |
| archived-20261005-222307: db.jsonl | 3f1d365b3b | 0.589 | 0.590 | 7,061 | 7,061 | 0.597 | 0.703 | 0.407 | 0.529 | 0.784 | 0.839 |  |
| archived-20261005-222307: db.jsonl | 63919635b7 | 0.501 | 0.502 | 7,089 | 7,089 | 0.665 | 0.700 | 0.517 | 0.608 | 0.216 | 0.587 |  |
| archived-20261005-222307: db.jsonl | 2c9b948725 | 0.490 | 0.481 | 7,097 | 7,097 | 0.618 | 0.963 | 0.445 | 0.518 | 0.206 | 0.666 |  |
| archived-20261005-222307: db.jsonl | cac62ca533 | 0.460 | 0.450 | 7,105 | 7,105 | 0.597 | 0.828 | 0.423 | 0.519 | 0.191 | 0.634 |  |
| archived-20261005-222307: db.jsonl | 627568164d | 0.441 | 0.447 | 7,147 | 7,147 | 0.604 | 0.686 | 0.420 | 0.510 | 0.187 | 0.629 |  |
| archived-20261005-222307: db.jsonl | 37b502fac7 | 0.434 | 0.433 | 7,238 | 7,238 | 0.571 | 0.705 | 0.407 | 0.511 | 0.185 | 0.595 |  |
| archived-20261005-222307: db.jsonl | ced47e8cfa | 0.415 | 0.406 | 8,030 | 8,030 | 0.597 | 0.475 | 0.421 | 0.522 | 0.198 | 0.559 |  |
| archived-20261005-235645: db.jsonl | 2816900bac | 0.651 | 0.638 | 6,941 | 6,941 | 0.615 | 0.777 | 0.496 | 0.574 | 0.857 | 0.846 |  |
| archived-20261005-235645: db.jsonl | 46fbc9e912 | 0.502 | 0.491 | 6,966 | 6,966 | 0.507 | 0.954 | 0.247 | 0.399 | 0.667 | 0.778 |  |
| archived-20261005-235645: db.jsonl | c2d99350f1 | 0.498 | 0.481 | 6,974 | 6,974 | 0.523 | 0.698 | 0.229 | 0.409 | 0.896 | 0.861 |  |
| archived-20261005-235645: db.jsonl | 0f90ffc36a | 0.485 | 0.474 | 6,998 | 6,998 | 0.512 | 0.729 | 0.239 | 0.407 | 0.741 | 0.847 |  |
| archived-20261005-235645: db.jsonl | 988d608671 | 0.482 | 0.478 | 7,014 | 7,014 | 0.527 | 0.716 | 0.236 | 0.394 | 0.741 | 0.811 |  |
| archived-20261005-235645: db.jsonl | 20b3bde0c3 | 0.384 | 0.385 | 7,097 | 7,097 | 0.522 | 0.869 | 0.247 | 0.390 | 0.190 | 0.675 |  |
| archived-20261005-235645: db.jsonl | 35135bde2f | 0.379 | 0.371 | 7,105 | 7,105 | 0.485 | 0.799 | 0.236 | 0.386 | 0.221 | 0.642 |  |
| archived-20261005-235645: db.jsonl | 9a482dbeaf | 0.354 | 0.351 | 7,334 | 7,334 | 0.466 | 0.856 | 0.217 | 0.359 | 0.179 | 0.558 |  |
| archived-20261005-235645: db.jsonl | 040e367ce9 | 0.353 | 0.343 | 7,753 | 7,753 | 0.477 | 0.803 | 0.226 | 0.361 | 0.176 | 0.574 |  |
| archived-20261005-235645: db.jsonl | 1918ae250d | 0.348 | 0.346 | 7,820 | 7,820 | 0.508 | 0.514 | 0.232 | 0.389 | 0.218 | 0.535 |  |
| archived-20261005-235645: db.jsonl | 9102e1dea9 | 0.334 | 0.316 | 7,958 | 7,958 | 0.478 | 0.600 | 0.219 | 0.370 | 0.179 | 0.465 |  |
| archived-20261005-235645: db.jsonl | c9f3c95232 | 0.336 | 0.330 | 7,966 | 7,966 | 0.487 | 0.574 | 0.226 | 0.379 | 0.179 | 0.499 |  |
| archived-20261005-235645: db.jsonl | dcbaf0e29f | 0.331 | 0.329 | 9,014 | 9,014 | 0.471 | 0.603 | 0.216 | 0.368 | 0.176 | 0.449 |  |

The front of all runs together, by size: ad62971982 0.284 at 7,799, 3218bf9f21 0.293 at 7,666, 9c85c7d9f5 0.297 at 7,246, 103cbedc80 0.298 at 7,238, 76684cada6 0.304 at 7,166, 1a5dc48b9c 0.317 at 7,092, 403bda0b3f 0.329 at 7,017, 520f651e31 0.411 at 6,914, 097ff5bdce 0.418 at 6,913, 5347899701 0.436 at 6,903

## The same session on two CPUs

Calibration on cpu 2: 0.994; on cpu 8: 1.005.

Speed on cpu 2 over speed on cpu 8, per design: median 1.002, 10-90% 0.990-1.012, extremes 0.979-1.031; rank agreement (Spearman) 1.00.

The front of all runs on cpu 2: ad62971982 0.284 at 7,799, 3218bf9f21 0.293 at 7,666, 9c85c7d9f5 0.297 at 7,246, 103cbedc80 0.298 at 7,238, 76684cada6 0.304 at 7,166, 1a5dc48b9c 0.317 at 7,092, 403bda0b3f 0.329 at 7,017, 520f651e31 0.411 at 6,914, 097ff5bdce 0.418 at 6,913, 5347899701 0.436 at 6,903

The front of all runs on cpu 8: ad62971982 0.280 at 7,799, cd8075731e 0.290 at 7,773, 9c85c7d9f5 0.295 at 7,246, 103cbedc80 0.296 at 7,238, 76684cada6 0.303 at 7,166, bdb87d827e 0.312 at 7,124, 1a5dc48b9c 0.319 at 7,092, 403bda0b3f 0.328 at 7,017, 520f651e31 0.407 at 6,914, 097ff5bdce 0.417 at 6,913, 5347899701 0.435 at 6,903

On both fronts: 9 of 10 and 11.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| ad62971982 | 0.284 | 0.280 | 1.013 |
| db3dcdb1f8 | 0.289 | 0.287 | 1.006 |
| 3218bf9f21 | 0.293 | 0.296 | 0.989 |
| cd8075731e | 0.293 | 0.290 | 1.011 |
| 9c85c7d9f5 | 0.297 | 0.295 | 1.007 |
| 103cbedc80 | 0.298 | 0.296 | 1.005 |
| 76684cada6 | 0.304 | 0.303 | 1.003 |
| 1a5dc48b9c | 0.317 | 0.319 | 0.994 |
| ed927db5ce | 0.317 | 0.316 | 1.006 |
| bdb87d827e | 0.319 | 0.312 | 1.022 |
| 403bda0b3f | 0.329 | 0.328 | 1.003 |
| dcbaf0e29f | 0.331 | 0.330 | 1.002 |
| 9102e1dea9 | 0.334 | 0.334 | 1.000 |
| ccf0eb9891 | 0.334 | 0.328 | 1.018 |
| c9f3c95232 | 0.336 | 0.334 | 1.006 |
| 1918ae250d | 0.348 | 0.353 | 0.987 |
| 040e367ce9 | 0.353 | 0.355 | 0.995 |
| 9a482dbeaf | 0.354 | 0.346 | 1.023 |
| 35135bde2f | 0.379 | 0.378 | 1.001 |
| 20b3bde0c3 | 0.384 | 0.392 | 0.979 |
| 520f651e31 | 0.411 | 0.407 | 1.012 |
| e973e9ada8 | 0.413 | 0.412 | 1.003 |
| ced47e8cfa | 0.415 | 0.414 | 1.002 |
| 097ff5bdce | 0.418 | 0.417 | 1.002 |
| 37b502fac7 | 0.434 | 0.421 | 1.031 |
| 9bb527944a | 0.435 | 0.441 | 0.987 |
| 5347899701 | 0.436 | 0.435 | 1.002 |
| ff306b06c1 | 0.437 | 0.437 | 1.001 |
| 84a09433d4 | 0.439 | 0.437 | 1.004 |
| ff3e6b2a34 | 0.440 | 0.438 | 1.005 |
| 627568164d | 0.441 | 0.441 | 1.001 |
| 6827e42d47 | 0.458 | 0.453 | 1.011 |
| 049e0c9c48 | 0.460 | 0.461 | 0.999 |
| cac62ca533 | 0.460 | 0.458 | 1.004 |
| 577c999e62 | 0.465 | 0.463 | 1.003 |
| 959e88b0f5 | 0.470 | 0.470 | 0.999 |
| 72ca2cf497 | 0.476 | 0.483 | 0.986 |
| 0212f86508 | 0.476 | 0.474 | 1.005 |
| 988d608671 | 0.482 | 0.490 | 0.983 |
| 7a8d429413 | 0.484 | 0.478 | 1.014 |
| 0f90ffc36a | 0.485 | 0.481 | 1.009 |
| aba06380d6 | 0.488 | 0.487 | 1.002 |
| 85a977e3ed | 0.488 | 0.494 | 0.988 |
| 96f2d8bfd7 | 0.490 | 0.484 | 1.011 |
| 2c9b948725 | 0.490 | 0.483 | 1.014 |
| cda8cad59b | 0.490 | 0.485 | 1.012 |
| 1b602bc9bd | 0.497 | 0.504 | 0.986 |
| c2d99350f1 | 0.498 | 0.492 | 1.012 |
| 9d89f6ba0e | 0.499 | 0.494 | 1.010 |
| 63919635b7 | 0.501 | 0.500 | 1.001 |
| 55ca1dfdb5 | 0.501 | 0.496 | 1.011 |
| 46fbc9e912 | 0.502 | 0.502 | 1.000 |
| 85cac726b5 | 0.502 | 0.499 | 1.005 |
| 641b85143d | 0.503 | 0.494 | 1.018 |
| f85a63f8c7 | 0.505 | 0.498 | 1.015 |
| 51879a71f0 | 0.507 | 0.509 | 0.995 |
| f084674b22 | 0.510 | 0.517 | 0.985 |
| 45d2ff7e01 | 0.510 | 0.508 | 1.004 |
| 0e8b212e50 | 0.511 | 0.507 | 1.007 |
| 2ed8b1583e | 0.511 | 0.510 | 1.001 |
| f3988ea716 | 0.519 | 0.515 | 1.008 |
| 6578fc6928 | 0.522 | 0.523 | 0.998 |
| 3d31fd4cc4 | 0.524 | 0.519 | 1.009 |
| fa23f401cd | 0.530 | 0.541 | 0.979 |
| caf4358de8 | 0.537 | 0.542 | 0.991 |
| be02a4c0cf | 0.544 | 0.548 | 0.993 |
| 853cfb9d36 | 0.548 | 0.546 | 1.005 |
| 2367cb920c | 0.548 | 0.546 | 1.005 |
| d8d62beb78 | 0.554 | 0.553 | 1.000 |
| cd943ed219 | 0.589 | 0.595 | 0.989 |
| 3f1d365b3b | 0.589 | 0.594 | 0.992 |
| 31a3ceea45 | 0.589 | 0.590 | 0.999 |
| a214fa731c | 0.594 | 0.602 | 0.987 |
| 15dde12f04 | 0.597 | 0.598 | 0.999 |
| 6ba318d95c | 0.601 | 0.602 | 0.999 |
| 7b9675c9ef | 0.606 | 0.605 | 1.000 |
| 3a7c3d6e90 | 0.606 | 0.606 | 1.000 |
| 1cf03a8fd4 | 0.609 | 0.606 | 1.004 |
| 2b00aa6e97 | 0.609 | 0.606 | 1.005 |
| dc02ceae31 | 0.610 | 0.603 | 1.010 |
| 4cc12fc1e7 | 0.624 | 0.624 | 1.001 |
| 27a35df3fa | 0.629 | 0.628 | 1.002 |
| ff39b37bcc | 0.633 | 0.637 | 0.994 |
| 29ad5ba726 | 0.642 | 0.648 | 0.990 |
| 05617039f6 | 0.642 | 0.642 | 1.000 |
| 2db525ff95 | 0.643 | 0.654 | 0.983 |
| 8dd8a7a146 | 0.649 | 0.642 | 1.011 |
| 2816900bac | 0.651 | 0.647 | 1.006 |
| c61857fc89 | 0.654 | 0.657 | 0.995 |
| e99da68667 | 0.654 | 0.661 | 0.990 |
| 22b81e50c4 | 0.655 | 0.660 | 0.993 |
| 9e50623ac1 | 0.657 | 0.658 | 0.997 |
| 3c2d8a577b | 0.657 | 0.655 | 1.002 |
| 88792f1798 | 0.659 | 0.648 | 1.017 |
| 1769ca2a48 | 0.659 | 0.663 | 0.995 |
| b06a4cf784 | 0.660 | 0.658 | 1.003 |
| 8a2189b3b6 | 0.660 | 0.661 | 0.999 |
| af5e8dc29f | 0.661 | 0.657 | 1.006 |
| 5df0608416 | 0.662 | 0.660 | 1.003 |
| a74b828e9b | 0.668 | 0.665 | 1.004 |
| a306cc61fb | 0.670 | 0.674 | 0.994 |
| bf413bef91 | 0.671 | 0.667 | 1.006 |
| c25a5e1714 | 0.671 | 0.674 | 0.996 |
| c40ba92d5b | 0.671 | 0.660 | 1.017 |
| 7380e8bcb1 | 0.673 | 0.662 | 1.017 |
| 0b1d16def9 | 0.675 | 0.682 | 0.991 |
| 98e6135b93 | 0.679 | 0.674 | 1.007 |
| 32600cab87 | 0.680 | 0.675 | 1.006 |
| 14f6036a4b | 0.681 | 0.676 | 1.008 |
| f060a4c31f | 0.684 | 0.687 | 0.996 |
| ca2ac63866 | 0.684 | 0.676 | 1.012 |
| f66d74a27c | 0.686 | 0.686 | 1.000 |
| 4cb3fa9172 | 0.687 | 0.692 | 0.992 |
| 66eb4a8f15 | 0.687 | 0.682 | 1.007 |
| ccce4784b8 | 0.688 | 0.696 | 0.989 |
| bb8a0cb575 | 0.690 | 0.698 | 0.988 |
| 9f5e6d173c | 0.690 | 0.693 | 0.996 |
| 60753a0eb0 | 0.690 | 0.681 | 1.013 |
| 312ad2edaa | 0.691 | 0.683 | 1.012 |
| 9385a8fcbb | 0.693 | 0.691 | 1.003 |
| 6495dcb5dd | 0.693 | 0.693 | 1.000 |
| 49b0a93f14 | 0.693 | 0.695 | 0.997 |
| 38d187239c | 0.694 | 0.694 | 1.001 |
| e05adba602 | 0.696 | 0.689 | 1.010 |
| d0d304e240 | 0.696 | 0.697 | 0.998 |
| 448ef1ef43 | 0.697 | 0.695 | 1.003 |
| e0cbf09bc2 | 0.699 | 0.694 | 1.007 |
| 52b80007a1 | 0.700 | 0.702 | 0.998 |
| a27aa49d8e | 0.704 | 0.700 | 1.006 |
| c297551359 | 0.706 | 0.708 | 0.998 |
| 5ed1ed8715 | 0.707 | 0.705 | 1.002 |
| 38d91795a2 | 0.707 | 0.714 | 0.991 |
| 12d8e18511 | 0.709 | 0.707 | 1.003 |
| 6463752a82 | 0.711 | 0.712 | 0.998 |
| 7fe7f039bd | 0.715 | 0.720 | 0.993 |
| ee4d8f8a50 | 0.719 | 0.726 | 0.990 |
| d4739aac88 | 0.719 | 0.717 | 1.003 |
| 7cb20d14b1 | 0.721 | 0.724 | 0.996 |
| 84e302c470 | 0.722 | 0.724 | 0.998 |
| 8dc0f97f2c | 0.722 | 0.723 | 0.999 |
| 8cbc6dd05c | 0.723 | 0.728 | 0.993 |
| f4a6dd9a13 | 0.727 | 0.717 | 1.014 |
| f052397620 | 0.727 | 0.721 | 1.009 |
| 82e7e4dc0d | 0.728 | 0.723 | 1.006 |
| 53ec9bedde | 0.728 | 0.725 | 1.004 |
| 550df563ee | 0.734 | 0.742 | 0.990 |
| 422d6bcbca | 0.736 | 0.736 | 1.000 |
| e8f1dd3ca2 | 0.736 | 0.738 | 0.998 |
| 090672993b | 0.737 | 0.741 | 0.995 |
| 57a9dcc7cb | 0.738 | 0.740 | 0.997 |
| 05dcc81cdc | 0.740 | 0.748 | 0.990 |
| a285fa6ba3 | 0.741 | 0.737 | 1.006 |
| 528fc9619a | 0.751 | 0.751 | 1.001 |
| 3453246bdf | 0.752 | 0.750 | 1.003 |
| 4032a5ce71 | 0.753 | 0.756 | 0.996 |
| 57e0e77c09 | 0.757 | 0.756 | 1.002 |
| 6738aed13f | 0.758 | 0.753 | 1.007 |
| 9cd791dd84 | 0.759 | 0.754 | 1.006 |
| 3781c5e756 | 0.759 | 0.762 | 0.995 |
| 57d12a1bb0 | 0.760 | 0.759 | 1.000 |
| 295a6acd98 | 0.762 | 0.763 | 0.998 |
| 5b70f3dd64 | 0.763 | 0.761 | 1.002 |
| 595fc2b8f4 | 0.764 | 0.757 | 1.009 |
| 4f010d8ab9 | 0.769 | 0.770 | 0.999 |
| 0ebf0445e0 | 0.776 | 0.776 | 0.999 |
| 98736f0596 | 0.783 | 0.776 | 1.010 |
| c17103bf95 | 0.785 | 0.786 | 1.000 |
| 90018981c6 | 0.786 | 0.786 | 0.999 |
| c513ef17b0 | 0.790 | 0.791 | 0.998 |
| a4e82e02e5 | 0.803 | 0.796 | 1.008 |
| 672538daf5 | 0.823 | 0.827 | 0.995 |
| 83cb81c383 | 0.835 | 0.839 | 0.994 |
| f41ab1810d | 1.009 | 1.003 | 1.007 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 12 - Iteration 62: seeds 1-14, after seed 14 (the whole lookup)

`seed 14 then experiment compare-fronts.py --rounds 10 --cpus 2,8`, commit
4388b682: sixteen databases, 188 front designs, five workloads, sieve held
out. Twenty minutes - the last session to re-time every run: from here
the newest four archived runs and the new one (next-run.sh,
COMPARE_LAST). **Calibration 1.000** (every workload 0.996-1.004). The
CPUs agree: per design median 1.000, 10-90% 0.990-1.012, ranks 1.00; 11
of 12 and 13 designs on both CPUs' fronts.

**The front of all runs: seed 14's eleven** - 6,903 bytes (0.433) to
8,320 (0.240, the fastest yet) - and seed 13's 097ff5bdce.

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 1.000** (kernel 1.001, fib 0.996, parse 0.999, corpus 1.004, loop 1.001, sieve 0.997).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 7f7d8e7864 | 0.433 | 0.435 | 6,903 | 6,903 | 0.419 | 0.774 | 0.178 | 0.323 | 0.812 | 0.795 | yes |
| this clone: db.jsonl | b7b4dd1166 | 0.426 | 0.422 | 6,911 | 6,911 | 0.403 | 0.805 | 0.178 | 0.326 | 0.742 | 0.785 | yes |
| this clone: db.jsonl | 3280937f3d | 0.416 | 0.416 | 6,928 | 6,928 | 0.417 | 0.738 | 0.179 | 0.332 | 0.679 | 0.818 |  |
| this clone: db.jsonl | 3c84b53247 | 0.379 | 0.377 | 6,939 | 6,939 | 0.320 | 0.851 | 0.117 | 0.244 | 1.001 | 0.829 | yes |
| this clone: db.jsonl | 9a9d2cb947 | 0.352 | 0.357 | 6,947 | 6,947 | 0.355 | 0.716 | 0.114 | 0.264 | 0.706 | 0.757 | yes |
| this clone: db.jsonl | 5e7eed1cba | 0.336 | 0.333 | 6,951 | 6,951 | 0.353 | 0.628 | 0.117 | 0.265 | 0.616 | 0.703 | yes |
| this clone: db.jsonl | 7033c6f1ab | 0.326 | 0.323 | 7,017 | 7,017 | 0.412 | 0.811 | 0.177 | 0.321 | 0.193 | 0.597 | yes |
| this clone: db.jsonl | 828c84dd15 | 0.326 | 0.317 | 7,026 | 7,026 | 0.412 | 0.745 | 0.189 | 0.333 | 0.191 | 0.539 |  |
| this clone: db.jsonl | 262f6959cc | 0.265 | 0.259 | 7,057 | 7,057 | 0.358 | 0.681 | 0.111 | 0.261 | 0.184 | 0.548 | yes |
| this clone: db.jsonl | 03fcb0e3e6 | 0.264 | 0.263 | 7,089 | 7,089 | 0.357 | 0.675 | 0.111 | 0.261 | 0.184 | 0.554 | yes |
| this clone: db.jsonl | 285b6909d1 | 0.245 | 0.248 | 7,172 | 7,172 | 0.342 | 0.639 | 0.092 | 0.235 | 0.188 | 0.544 | yes |
| this clone: db.jsonl | 453a46a8e6 | 0.252 | 0.254 | 7,188 | 7,188 | 0.337 | 0.723 | 0.098 | 0.234 | 0.181 | 0.507 |  |
| this clone: db.jsonl | 3995ab7bde | 0.244 | 0.243 | 7,286 | 7,286 | 0.322 | 0.651 | 0.100 | 0.228 | 0.181 | 0.549 | yes |
| this clone: db.jsonl | 364a0f4617 | 0.247 | 0.249 | 7,689 | 7,689 | 0.315 | 0.741 | 0.099 | 0.226 | 0.176 | 0.447 |  |
| this clone: db.jsonl | 419cce1726 | 0.240 | 0.238 | 8,320 | 8,320 | 0.333 | 0.558 | 0.101 | 0.232 | 0.181 | 0.511 | yes |
| archived-20261004-200423: db-rehearsal.jsonl | 595fc2b8f4 | 0.753 | 0.784 | 9,662 | 9,761 | 0.730 | 0.699 | 0.648 | 0.694 | 1.055 | 0.842 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 8cbc6dd05c | 0.723 | 0.742 | 9,694 | 9,809 | 0.724 | 0.794 | 0.602 | 0.667 | 0.858 | 0.792 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 6738aed13f | 0.763 | 0.755 | 9,694 | 9,793 | 0.777 | 0.698 | 0.628 | 0.707 | 1.073 | 0.854 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 312ad2edaa | 0.689 | 0.716 | 13,344 | 13,456 | 0.696 | 0.726 | 0.553 | 0.625 | 0.890 | 0.841 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 05617039f6 | 0.643 | 0.674 | 13,352 | 13,488 | 0.683 | 0.790 | 0.483 | 0.608 | 0.694 | 0.817 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 0b1d16def9 | 0.682 | 0.705 | 13,352 | 13,464 | 0.713 | 0.803 | 0.506 | 0.634 | 0.800 | 0.846 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 57a9dcc7cb | 0.741 | 0.680 | 13,368 | 13,480 | 0.705 | 0.945 | 0.535 | 0.639 | 0.977 | 0.907 |  |
| archived-20261004-200423: db-rehearsal.jsonl | 32600cab87 | 0.681 | 0.662 | 13,528 | 13,656 | 0.683 | 0.975 | 0.512 | 0.612 | 0.700 | 0.839 |  |
| archived-20261004-200423: db-seed1.jsonl | 83cb81c383 | 0.831 | 0.705 | 9,662 | 9,761 | 0.771 | 0.971 | 0.655 | 0.750 | 1.077 | 0.892 |  |
| archived-20261004-200423: db-seed1.jsonl | 5b70f3dd64 | 0.757 | 0.649 | 9,694 | 9,801 | 0.739 | 0.957 | 0.601 | 0.682 | 0.860 | 0.810 |  |
| archived-20261004-200423: db-seed1.jsonl | a4e82e02e5 | 0.802 | 0.654 | 9,694 | 9,809 | 0.782 | 0.892 | 0.656 | 0.733 | 0.989 | 0.881 |  |
| archived-20261004-200423: db-seed1.jsonl | 53ec9bedde | 0.721 | 0.670 | 13,336 | 13,464 | 0.744 | 0.774 | 0.601 | 0.672 | 0.837 | 0.827 |  |
| archived-20261004-200423: db-seed1.jsonl | 448ef1ef43 | 0.692 | 0.620 | 13,368 | 13,488 | 0.673 | 0.958 | 0.504 | 0.610 | 0.800 | 0.832 |  |
| archived-20261004-200423: db-seed1.jsonl | 38d187239c | 0.694 | 0.609 | 13,368 | 13,480 | 0.699 | 0.840 | 0.549 | 0.641 | 0.780 | 0.825 |  |
| archived-20261004-200423: db-seed2.jsonl | 0ebf0445e0 | 0.777 | 0.667 | 9,662 | 9,761 | 0.793 | 0.698 | 0.698 | 0.753 | 0.973 | 0.869 |  |
| archived-20261004-200423: db-seed2.jsonl | c17103bf95 | 0.781 | 0.725 | 9,662 | 9,769 | 0.788 | 0.755 | 0.716 | 0.755 | 0.902 | 0.896 |  |
| archived-20261004-200423: db-seed2.jsonl | a285fa6ba3 | 0.733 | 0.666 | 13,352 | 13,464 | 0.735 | 0.704 | 0.632 | 0.696 | 0.927 | 0.856 |  |
| archived-20261004-200423: db-seed2.jsonl | 57e0e77c09 | 0.763 | 0.657 | 13,352 | 13,480 | 0.725 | 1.076 | 0.545 | 0.655 | 0.930 | 0.895 |  |
| archived-20261004-200423: db-seed2.jsonl | 9cd791dd84 | 0.761 | 0.619 | 13,368 | 13,472 | 0.733 | 0.905 | 0.574 | 0.668 | 1.001 | 0.890 |  |
| archived-20261004-200423: db.jsonl | 550df563ee | 0.740 | 0.696 | 9,646 | 9,745 | 0.700 | 0.774 | 0.621 | 0.674 | 0.977 | 0.838 |  |
| archived-20261004-200423: db.jsonl | f4a6dd9a13 | 0.721 | 0.683 | 9,662 | 9,761 | 0.720 | 0.673 | 0.599 | 0.693 | 0.969 | 0.815 |  |
| archived-20261004-200423: db.jsonl | 60753a0eb0 | 0.692 | 0.622 | 9,686 | 9,785 | 0.693 | 0.662 | 0.582 | 0.670 | 0.888 | 0.789 |  |
| archived-20261004-200423: db.jsonl | 8dd8a7a146 | 0.653 | 0.595 | 13,352 | 13,464 | 0.655 | 0.658 | 0.532 | 0.605 | 0.856 | 0.790 |  |
| archived-20261004-214724: db.jsonl | 3453246bdf | 0.750 | 0.727 | 9,335 | 9,335 | 0.757 | 0.694 | 0.690 | 0.733 | 0.896 | 0.857 |  |
| archived-20261004-214724: db.jsonl | 672538daf5 | 0.821 | 0.780 | 9,351 | 9,351 | 0.812 | 0.834 | 0.700 | 0.771 | 1.022 | 0.874 |  |
| archived-20261004-214724: db.jsonl | 7fe7f039bd | 0.727 | 0.702 | 9,450 | 9,450 | 0.771 | 0.713 | 0.621 | 0.706 | 0.841 | 0.879 |  |
| archived-20261004-214724: db.jsonl | 38d91795a2 | 0.710 | 0.678 | 9,474 | 9,474 | 0.748 | 0.647 | 0.610 | 0.716 | 0.856 | 0.857 |  |
| archived-20261004-214724: db.jsonl | 6463752a82 | 0.704 | 0.669 | 9,523 | 9,523 | 0.713 | 0.720 | 0.580 | 0.675 | 0.861 | 0.859 |  |
| archived-20261004-214724: db.jsonl | 90018981c6 | 0.782 | 0.696 | 9,678 | 9,678 | 0.743 | 0.834 | 0.651 | 0.708 | 1.024 | 0.902 |  |
| archived-20261004-214724: db.jsonl | e0cbf09bc2 | 0.703 | 0.666 | 13,057 | 13,057 | 0.700 | 0.746 | 0.531 | 0.649 | 0.951 | 0.895 |  |
| archived-20261004-214724: db.jsonl | 1769ca2a48 | 0.658 | 0.603 | 13,209 | 13,209 | 0.684 | 0.616 | 0.521 | 0.648 | 0.865 | 0.841 |  |
| archived-20261004-214724: db.jsonl | 14f6036a4b | 0.682 | 0.627 | 13,217 | 13,217 | 0.674 | 0.837 | 0.478 | 0.598 | 0.916 | 0.918 |  |
| archived-20261004-214724: db.jsonl | 29ad5ba726 | 0.644 | 0.589 | 13,352 | 13,352 | 0.676 | 0.749 | 0.486 | 0.581 | 0.776 | 0.829 |  |
| archived-20261004-214724: db.jsonl | 12d8e18511 | 0.708 | 0.667 | 13,360 | 13,360 | 0.687 | 0.857 | 0.531 | 0.616 | 0.922 | 0.953 |  |
| archived-20261005-013645: db.jsonl | 05dcc81cdc | 0.745 | 0.688 | 9,335 | 9,335 | 0.735 | 0.814 | 0.599 | 0.699 | 0.913 | 0.886 |  |
| archived-20261005-013645: db.jsonl | c297551359 | 0.709 | 0.682 | 9,450 | 9,450 | 0.738 | 0.665 | 0.636 | 0.687 | 0.838 | 0.861 |  |
| archived-20261005-013645: db.jsonl | e8f1dd3ca2 | 0.731 | 0.678 | 9,458 | 9,458 | 0.700 | 0.817 | 0.580 | 0.656 | 0.959 | 0.892 |  |
| archived-20261005-013645: db.jsonl | 66eb4a8f15 | 0.677 | 0.641 | 13,057 | 13,057 | 0.695 | 0.677 | 0.531 | 0.626 | 0.911 | 0.893 |  |
| archived-20261005-013645: db.jsonl | 84e302c470 | 0.722 | 0.657 | 13,065 | 13,065 | 0.738 | 0.745 | 0.550 | 0.648 | 1.000 | 0.892 |  |
| archived-20261005-013645: db.jsonl | 4cb3fa9172 | 0.685 | 0.626 | 13,073 | 13,073 | 0.664 | 0.809 | 0.486 | 0.593 | 0.975 | 0.890 |  |
| archived-20261005-013645: db.jsonl | e99da68667 | 0.654 | 0.581 | 13,201 | 13,201 | 0.622 | 0.768 | 0.450 | 0.567 | 0.980 | 0.859 |  |
| archived-20261005-042924: db.jsonl | 98736f0596 | 0.773 | 0.731 | 9,335 | 9,335 | 0.786 | 0.727 | 0.654 | 0.725 | 1.021 | 0.911 |  |
| archived-20261005-042924: db.jsonl | 4f010d8ab9 | 0.770 | 0.721 | 9,343 | 9,343 | 0.784 | 0.734 | 0.644 | 0.719 | 1.014 | 0.894 |  |
| archived-20261005-042924: db.jsonl | 4032a5ce71 | 0.761 | 0.698 | 9,351 | 9,351 | 0.746 | 0.808 | 0.610 | 0.710 | 0.978 | 0.917 |  |
| archived-20261005-042924: db.jsonl | 528fc9619a | 0.749 | 0.702 | 9,359 | 9,359 | 0.757 | 0.763 | 0.596 | 0.689 | 0.991 | 0.880 |  |
| archived-20261005-042924: db.jsonl | f052397620 | 0.726 | 0.685 | 9,450 | 9,450 | 0.725 | 0.812 | 0.569 | 0.670 | 0.898 | 0.921 |  |
| archived-20261005-042924: db.jsonl | 8dc0f97f2c | 0.724 | 0.680 | 9,458 | 9,458 | 0.717 | 0.760 | 0.586 | 0.674 | 0.926 | 0.873 |  |
| archived-20261005-042924: db.jsonl | 52b80007a1 | 0.706 | 0.640 | 10,010 | 10,010 | 0.741 | 0.557 | 0.610 | 0.703 | 0.992 | 0.855 |  |
| archived-20261005-042924: db.jsonl | 5ed1ed8715 | 0.701 | 0.642 | 10,018 | 10,018 | 0.733 | 0.537 | 0.616 | 0.698 | 1.001 | 0.869 |  |
| archived-20261005-042924: db.jsonl | 9e50623ac1 | 0.660 | 0.593 | 13,073 | 13,073 | 0.653 | 0.717 | 0.492 | 0.596 | 0.914 | 0.863 |  |
| archived-20261005-042924: db.jsonl | 22b81e50c4 | 0.652 | 0.605 | 13,209 | 13,209 | 0.634 | 0.870 | 0.414 | 0.558 | 0.926 | 0.874 |  |
| archived-20261005-042924: db.jsonl | 2db525ff95 | 0.655 | 0.579 | 14,017 | 14,017 | 0.650 | 0.716 | 0.454 | 0.593 | 0.960 | 0.884 |  |
| archived-20261005-131253: db.jsonl | 422d6bcbca | 0.740 | 0.699 | 9,327 | 9,327 | 0.731 | 0.859 | 0.542 | 0.666 | 0.975 | 0.871 |  |
| archived-20261005-131253: db.jsonl | 090672993b | 0.735 | 0.700 | 9,335 | 9,335 | 0.702 | 0.826 | 0.632 | 0.672 | 0.875 | 0.795 |  |
| archived-20261005-131253: db.jsonl | 6495dcb5dd | 0.685 | 0.662 | 9,343 | 9,343 | 0.648 | 0.931 | 0.509 | 0.621 | 0.791 | 0.797 |  |
| archived-20261005-131253: db.jsonl | c40ba92d5b | 0.664 | 0.630 | 9,511 | 9,511 | 0.675 | 0.688 | 0.561 | 0.632 | 0.784 | 0.786 |  |
| archived-20261005-131253: db.jsonl | ca2ac63866 | 0.682 | 0.634 | 9,531 | 9,531 | 0.657 | 0.711 | 0.564 | 0.624 | 0.896 | 0.830 |  |
| archived-20261005-131253: db.jsonl | c61857fc89 | 0.658 | 0.633 | 10,034 | 10,034 | 0.691 | 0.708 | 0.538 | 0.638 | 0.736 | 0.858 |  |
| archived-20261005-131253: db.jsonl | b06a4cf784 | 0.664 | 0.615 | 10,246 | 10,246 | 0.643 | 0.704 | 0.533 | 0.612 | 0.873 | 0.839 |  |
| archived-20261005-131253: db.jsonl | af5e8dc29f | 0.669 | 0.604 | 10,254 | 10,254 | 0.661 | 0.683 | 0.545 | 0.624 | 0.872 | 0.837 |  |
| archived-20261005-131253: db.jsonl | a74b828e9b | 0.667 | 0.608 | 13,073 | 13,073 | 0.685 | 0.634 | 0.508 | 0.621 | 0.966 | 0.855 |  |
| archived-20261005-131253: db.jsonl | dc02ceae31 | 0.606 | 0.560 | 13,161 | 13,161 | 0.614 | 0.721 | 0.436 | 0.539 | 0.783 | 0.843 |  |
| archived-20261005-131253: db.jsonl | 15dde12f04 | 0.593 | 0.567 | 13,345 | 13,345 | 0.607 | 0.758 | 0.394 | 0.536 | 0.757 | 0.817 |  |
| archived-20261005-131253: db.jsonl | cd943ed219 | 0.591 | 0.545 | 14,081 | 14,081 | 0.623 | 0.682 | 0.402 | 0.537 | 0.783 | 0.825 |  |
| archived-20261005-144844: db.jsonl | 49b0a93f14 | 0.694 | 0.688 | 8,073 | 8,073 | 0.716 | 0.884 | 0.550 | 0.652 | 0.707 | 0.821 |  |
| archived-20261005-144844: db.jsonl | 9f5e6d173c | 0.690 | 0.650 | 8,074 | 8,074 | 0.673 | 0.867 | 0.527 | 0.623 | 0.818 | 0.809 |  |
| archived-20261005-144844: db.jsonl | f060a4c31f | 0.682 | 0.637 | 8,289 | 8,289 | 0.648 | 0.845 | 0.527 | 0.589 | 0.872 | 0.801 |  |
| archived-20261005-144844: db.jsonl | a306cc61fb | 0.672 | 0.615 | 8,305 | 8,305 | 0.679 | 0.630 | 0.558 | 0.614 | 0.937 | 0.787 |  |
| archived-20261005-144844: db.jsonl | 3c2d8a577b | 0.655 | 0.603 | 8,306 | 8,306 | 0.666 | 0.623 | 0.538 | 0.611 | 0.884 | 0.795 |  |
| archived-20261005-144844: db.jsonl | 4cc12fc1e7 | 0.624 | 0.561 | 8,957 | 8,957 | 0.617 | 0.550 | 0.504 | 0.592 | 0.934 | 0.773 |  |
| archived-20261005-144844: db.jsonl | 3a7c3d6e90 | 0.609 | 0.551 | 11,777 | 11,777 | 0.608 | 0.865 | 0.362 | 0.522 | 0.844 | 0.870 |  |
| archived-20261005-144844: db.jsonl | 2b00aa6e97 | 0.613 | 0.568 | 12,145 | 12,145 | 0.612 | 0.863 | 0.363 | 0.541 | 0.831 | 0.858 |  |
| archived-20261005-144844: db.jsonl | 27a35df3fa | 0.630 | 0.570 | 12,312 | 12,312 | 0.631 | 0.595 | 0.492 | 0.574 | 0.936 | 0.783 |  |
| archived-20261005-144844: db.jsonl | ff39b37bcc | 0.639 | 0.572 | 12,584 | 12,584 | 0.640 | 0.628 | 0.467 | 0.572 | 0.994 | 0.843 |  |
| archived-20261005-144844: db.jsonl | 1cf03a8fd4 | 0.610 | 0.545 | 12,608 | 12,608 | 0.617 | 0.687 | 0.409 | 0.536 | 0.909 | 0.828 |  |
| archived-20261005-144844: db.jsonl | a214fa731c | 0.604 | 0.557 | 12,664 | 12,664 | 0.639 | 0.635 | 0.451 | 0.571 | 0.774 | 0.766 |  |
| archived-20261005-164554: db.jsonl | f41ab1810d | 1.005 | 1.008 | 8,034 | 8,034 | 1.003 | 1.246 | 0.813 | 0.925 | 1.091 | 1.140 |  |
| archived-20261005-164554: db.jsonl | 3781c5e756 | 0.754 | 0.758 | 8,041 | 8,041 | 0.751 | 0.910 | 0.613 | 0.702 | 0.831 | 0.855 |  |
| archived-20261005-164554: db.jsonl | d4739aac88 | 0.729 | 0.723 | 8,042 | 8,042 | 0.809 | 0.732 | 0.634 | 0.739 | 0.742 | 0.875 |  |
| archived-20261005-164554: db.jsonl | e05adba602 | 0.694 | 0.687 | 8,082 | 8,082 | 0.721 | 0.766 | 0.547 | 0.652 | 0.817 | 0.816 |  |
| archived-20261005-164554: db.jsonl | bb8a0cb575 | 0.702 | 0.688 | 8,099 | 8,099 | 0.751 | 0.768 | 0.569 | 0.687 | 0.756 | 0.862 |  |
| archived-20261005-164554: db.jsonl | a27aa49d8e | 0.695 | 0.693 | 8,163 | 8,163 | 0.686 | 0.849 | 0.511 | 0.621 | 0.879 | 0.851 |  |
| archived-20261005-164554: db.jsonl | 8a2189b3b6 | 0.657 | 0.646 | 8,171 | 8,171 | 0.669 | 0.765 | 0.516 | 0.608 | 0.762 | 0.849 |  |
| archived-20261005-164554: db.jsonl | f66d74a27c | 0.688 | 0.682 | 8,210 | 8,210 | 0.693 | 0.864 | 0.521 | 0.640 | 0.770 | 0.814 |  |
| archived-20261005-164554: db.jsonl | be02a4c0cf | 0.549 | 0.533 | 8,525 | 8,525 | 0.792 | 0.758 | 0.614 | 0.705 | 0.192 | 0.606 |  |
| archived-20261005-164554: db.jsonl | caf4358de8 | 0.542 | 0.514 | 8,540 | 8,540 | 0.768 | 0.780 | 0.587 | 0.696 | 0.191 | 0.645 |  |
| archived-20261005-164554: db.jsonl | 6578fc6928 | 0.530 | 0.515 | 8,548 | 8,548 | 0.708 | 0.764 | 0.531 | 0.626 | 0.234 | 0.588 |  |
| archived-20261005-164554: db.jsonl | 3d31fd4cc4 | 0.527 | 0.502 | 8,550 | 8,550 | 0.706 | 0.868 | 0.524 | 0.623 | 0.203 | 0.661 |  |
| archived-20261005-164554: db.jsonl | 85cac726b5 | 0.505 | 0.484 | 8,614 | 8,614 | 0.650 | 0.859 | 0.531 | 0.599 | 0.185 | 0.614 |  |
| archived-20261005-164554: db.jsonl | f85a63f8c7 | 0.499 | 0.481 | 8,647 | 8,647 | 0.643 | 0.858 | 0.534 | 0.586 | 0.178 | 0.627 |  |
| archived-20261005-164554: db.jsonl | 51879a71f0 | 0.513 | 0.513 | 8,664 | 8,664 | 0.687 | 0.733 | 0.566 | 0.651 | 0.192 | 0.660 |  |
| archived-20261005-164554: db.jsonl | 1b602bc9bd | 0.474 | 0.478 | 8,671 | 8,671 | 0.652 | 0.776 | 0.476 | 0.583 | 0.170 | 0.588 |  |
| archived-20261005-164554: db.jsonl | 72ca2cf497 | 0.482 | 0.469 | 8,990 | 8,990 | 0.657 | 0.671 | 0.509 | 0.601 | 0.193 | 0.531 |  |
| archived-20261005-164554: db.jsonl | 959e88b0f5 | 0.473 | 0.458 | 9,140 | 9,140 | 0.689 | 0.534 | 0.520 | 0.633 | 0.196 | 0.539 |  |
| archived-20261005-164554: db.jsonl | 577c999e62 | 0.464 | 0.443 | 9,278 | 9,278 | 0.640 | 0.558 | 0.510 | 0.603 | 0.195 | 0.525 |  |
| archived-20261005-164554: db.jsonl | aba06380d6 | 0.485 | 0.462 | 12,353 | 12,353 | 0.657 | 0.764 | 0.496 | 0.584 | 0.184 | 0.628 |  |
| archived-20261005-164554: db.jsonl | 0212f86508 | 0.472 | 0.453 | 12,377 | 12,377 | 0.634 | 0.795 | 0.449 | 0.553 | 0.187 | 0.613 |  |
| archived-20261005-164554: db.jsonl | 9bb527944a | 0.436 | 0.430 | 13,073 | 13,073 | 0.608 | 0.554 | 0.433 | 0.563 | 0.191 | 0.550 |  |
| archived-20261005-175214: db.jsonl | c513ef17b0 | 0.789 | 0.781 | 7,019 | 7,019 | 0.842 | 0.755 | 0.630 | 0.755 | 1.012 | 0.883 |  |
| archived-20261005-175214: db.jsonl | 57d12a1bb0 | 0.759 | 0.756 | 7,020 | 7,020 | 0.776 | 0.885 | 0.611 | 0.727 | 0.827 | 0.828 |  |
| archived-20261005-175214: db.jsonl | ee4d8f8a50 | 0.722 | 0.723 | 7,027 | 7,027 | 0.777 | 0.767 | 0.613 | 0.713 | 0.757 | 0.863 |  |
| archived-20261005-175214: db.jsonl | ccce4784b8 | 0.692 | 0.681 | 7,091 | 7,091 | 0.759 | 0.720 | 0.608 | 0.698 | 0.683 | 0.846 |  |
| archived-20261005-175214: db.jsonl | 88792f1798 | 0.658 | 0.653 | 7,220 | 7,220 | 0.685 | 0.739 | 0.550 | 0.643 | 0.686 | 0.820 |  |
| archived-20261005-175214: db.jsonl | 2367cb920c | 0.543 | 0.538 | 7,510 | 7,510 | 0.743 | 0.815 | 0.603 | 0.691 | 0.188 | 0.619 |  |
| archived-20261005-175214: db.jsonl | 853cfb9d36 | 0.537 | 0.536 | 7,651 | 7,651 | 0.749 | 0.828 | 0.622 | 0.697 | 0.166 | 0.621 |  |
| archived-20261005-175214: db.jsonl | fa23f401cd | 0.543 | 0.525 | 7,692 | 7,692 | 0.705 | 0.862 | 0.609 | 0.666 | 0.191 | 0.635 |  |
| archived-20261005-175214: db.jsonl | 45d2ff7e01 | 0.512 | 0.500 | 7,725 | 7,725 | 0.702 | 0.721 | 0.561 | 0.639 | 0.194 | 0.664 |  |
| archived-20261005-175214: db.jsonl | f084674b22 | 0.515 | 0.516 | 9,198 | 9,198 | 0.709 | 0.714 | 0.565 | 0.659 | 0.192 | 0.645 |  |
| archived-20261005-175214: db.jsonl | 9d89f6ba0e | 0.490 | 0.487 | 13,065 | 13,065 | 0.670 | 0.775 | 0.495 | 0.598 | 0.184 | 0.670 |  |
| archived-20261005-204503: db.jsonl | 295a6acd98 | 0.760 | 0.755 | 6,977 | 6,977 | 0.786 | 0.822 | 0.624 | 0.710 | 0.886 | 0.897 |  |
| archived-20261005-204503: db.jsonl | 82e7e4dc0d | 0.731 | 0.726 | 6,979 | 6,979 | 0.773 | 0.836 | 0.574 | 0.693 | 0.812 | 0.840 |  |
| archived-20261005-204503: db.jsonl | 9385a8fcbb | 0.696 | 0.690 | 6,994 | 6,994 | 0.697 | 0.895 | 0.544 | 0.654 | 0.737 | 0.836 |  |
| archived-20261005-204503: db.jsonl | bf413bef91 | 0.667 | 0.681 | 7,002 | 7,002 | 0.700 | 0.709 | 0.531 | 0.645 | 0.776 | 0.858 |  |
| archived-20261005-204503: db.jsonl | c25a5e1714 | 0.674 | 0.668 | 7,010 | 7,010 | 0.729 | 0.712 | 0.549 | 0.642 | 0.761 | 0.853 |  |
| archived-20261005-204503: db.jsonl | 7380e8bcb1 | 0.660 | 0.658 | 7,050 | 7,050 | 0.670 | 0.762 | 0.532 | 0.617 | 0.747 | 0.845 |  |
| archived-20261005-204503: db.jsonl | 5df0608416 | 0.657 | 0.659 | 7,059 | 7,059 | 0.666 | 0.756 | 0.523 | 0.625 | 0.743 | 0.828 |  |
| archived-20261005-204503: db.jsonl | d8d62beb78 | 0.549 | 0.545 | 7,106 | 7,106 | 0.758 | 0.872 | 0.577 | 0.694 | 0.188 | 0.651 |  |
| archived-20261005-204503: db.jsonl | f3988ea716 | 0.520 | 0.510 | 7,113 | 7,113 | 0.708 | 0.771 | 0.566 | 0.641 | 0.191 | 0.646 |  |
| archived-20261005-204503: db.jsonl | 2ed8b1583e | 0.509 | 0.509 | 7,129 | 7,129 | 0.689 | 0.803 | 0.521 | 0.620 | 0.191 | 0.577 |  |
| archived-20261005-204503: db.jsonl | 641b85143d | 0.499 | 0.501 | 7,178 | 7,178 | 0.673 | 0.743 | 0.539 | 0.618 | 0.186 | 0.601 |  |
| archived-20261005-204503: db.jsonl | 96f2d8bfd7 | 0.483 | 0.490 | 7,236 | 7,236 | 0.635 | 0.769 | 0.500 | 0.598 | 0.181 | 0.569 |  |
| archived-20261005-204503: db.jsonl | 55ca1dfdb5 | 0.504 | 0.499 | 7,550 | 7,550 | 0.669 | 0.771 | 0.544 | 0.622 | 0.185 | 0.600 |  |
| archived-20261005-204503: db.jsonl | 0e8b212e50 | 0.509 | 0.507 | 7,558 | 7,558 | 0.651 | 0.864 | 0.529 | 0.603 | 0.190 | 0.628 |  |
| archived-20261005-204503: db.jsonl | 7a8d429413 | 0.474 | 0.479 | 7,714 | 7,714 | 0.709 | 0.515 | 0.538 | 0.648 | 0.188 | 0.564 |  |
| archived-20261005-204503: db.jsonl | 85a977e3ed | 0.490 | 0.486 | 7,804 | 7,804 | 0.702 | 0.578 | 0.554 | 0.666 | 0.188 | 0.550 |  |
| archived-20261005-204503: db.jsonl | cda8cad59b | 0.480 | 0.492 | 7,949 | 7,949 | 0.717 | 0.575 | 0.535 | 0.652 | 0.178 | 0.593 |  |
| archived-20261005-204503: db.jsonl | 049e0c9c48 | 0.462 | 0.457 | 7,973 | 7,973 | 0.667 | 0.512 | 0.515 | 0.612 | 0.196 | 0.536 |  |
| archived-20261005-204503: db.jsonl | 6827e42d47 | 0.459 | 0.451 | 8,352 | 8,352 | 0.660 | 0.508 | 0.513 | 0.603 | 0.196 | 0.535 |  |
| archived-20261005-204503: db.jsonl | ff306b06c1 | 0.438 | 0.451 | 12,145 | 12,145 | 0.623 | 0.537 | 0.450 | 0.551 | 0.195 | 0.568 |  |
| archived-20261005-204503: db.jsonl | 84a09433d4 | 0.439 | 0.435 | 12,585 | 12,585 | 0.612 | 0.550 | 0.435 | 0.563 | 0.197 | 0.554 |  |
| archived-20261005-204503: db.jsonl | ff3e6b2a34 | 0.436 | 0.438 | 13,073 | 13,073 | 0.612 | 0.558 | 0.438 | 0.557 | 0.189 | 0.558 |  |
| archived-20261005-222307: db.jsonl | 7cb20d14b1 | 0.730 | 0.718 | 6,971 | 6,971 | 0.777 | 0.775 | 0.594 | 0.710 | 0.819 | 0.883 |  |
| archived-20261005-222307: db.jsonl | d0d304e240 | 0.697 | 0.684 | 6,977 | 6,977 | 0.720 | 0.798 | 0.526 | 0.645 | 0.843 | 0.826 |  |
| archived-20261005-222307: db.jsonl | 98e6135b93 | 0.680 | 0.678 | 6,978 | 6,978 | 0.669 | 0.776 | 0.508 | 0.611 | 0.901 | 0.877 |  |
| archived-20261005-222307: db.jsonl | 6ba318d95c | 0.595 | 0.601 | 6,989 | 6,989 | 0.594 | 0.712 | 0.425 | 0.515 | 0.805 | 0.871 |  |
| archived-20261005-222307: db.jsonl | 7b9675c9ef | 0.610 | 0.604 | 7,004 | 7,004 | 0.626 | 0.754 | 0.444 | 0.548 | 0.733 | 0.817 |  |
| archived-20261005-222307: db.jsonl | 31a3ceea45 | 0.593 | 0.582 | 7,037 | 7,037 | 0.594 | 0.745 | 0.447 | 0.518 | 0.714 | 0.833 |  |
| archived-20261005-222307: db.jsonl | 3f1d365b3b | 0.589 | 0.590 | 7,061 | 7,061 | 0.594 | 0.707 | 0.421 | 0.520 | 0.774 | 0.841 |  |
| archived-20261005-222307: db.jsonl | 63919635b7 | 0.504 | 0.502 | 7,089 | 7,089 | 0.671 | 0.701 | 0.513 | 0.609 | 0.222 | 0.583 |  |
| archived-20261005-222307: db.jsonl | 2c9b948725 | 0.483 | 0.481 | 7,097 | 7,097 | 0.616 | 0.966 | 0.435 | 0.522 | 0.195 | 0.661 |  |
| archived-20261005-222307: db.jsonl | cac62ca533 | 0.454 | 0.450 | 7,105 | 7,105 | 0.585 | 0.843 | 0.420 | 0.505 | 0.183 | 0.623 |  |
| archived-20261005-222307: db.jsonl | 627568164d | 0.447 | 0.447 | 7,147 | 7,147 | 0.611 | 0.705 | 0.410 | 0.527 | 0.191 | 0.653 |  |
| archived-20261005-222307: db.jsonl | 37b502fac7 | 0.426 | 0.433 | 7,238 | 7,238 | 0.567 | 0.702 | 0.413 | 0.491 | 0.175 | 0.580 |  |
| archived-20261005-222307: db.jsonl | ced47e8cfa | 0.413 | 0.406 | 8,030 | 8,030 | 0.592 | 0.473 | 0.414 | 0.530 | 0.196 | 0.558 |  |
| archived-20261005-235645: db.jsonl | 2816900bac | 0.651 | 0.638 | 6,941 | 6,941 | 0.609 | 0.786 | 0.497 | 0.565 | 0.870 | 0.826 |  |
| archived-20261005-235645: db.jsonl | 46fbc9e912 | 0.502 | 0.491 | 6,966 | 6,966 | 0.497 | 0.949 | 0.248 | 0.407 | 0.667 | 0.758 |  |
| archived-20261005-235645: db.jsonl | c2d99350f1 | 0.492 | 0.481 | 6,974 | 6,974 | 0.507 | 0.701 | 0.228 | 0.398 | 0.890 | 0.878 |  |
| archived-20261005-235645: db.jsonl | 0f90ffc36a | 0.482 | 0.474 | 6,998 | 6,998 | 0.507 | 0.716 | 0.239 | 0.410 | 0.734 | 0.861 |  |
| archived-20261005-235645: db.jsonl | 988d608671 | 0.485 | 0.478 | 7,014 | 7,014 | 0.518 | 0.706 | 0.237 | 0.408 | 0.755 | 0.818 |  |
| archived-20261005-235645: db.jsonl | 20b3bde0c3 | 0.385 | 0.385 | 7,097 | 7,097 | 0.507 | 0.907 | 0.248 | 0.388 | 0.190 | 0.672 |  |
| archived-20261005-235645: db.jsonl | 35135bde2f | 0.378 | 0.371 | 7,105 | 7,105 | 0.489 | 0.811 | 0.239 | 0.379 | 0.216 | 0.630 |  |
| archived-20261005-235645: db.jsonl | 9a482dbeaf | 0.352 | 0.351 | 7,334 | 7,334 | 0.469 | 0.880 | 0.214 | 0.351 | 0.175 | 0.537 |  |
| archived-20261005-235645: db.jsonl | 040e367ce9 | 0.354 | 0.343 | 7,753 | 7,753 | 0.485 | 0.804 | 0.220 | 0.353 | 0.184 | 0.574 |  |
| archived-20261005-235645: db.jsonl | 1918ae250d | 0.350 | 0.346 | 7,820 | 7,820 | 0.504 | 0.529 | 0.230 | 0.390 | 0.220 | 0.523 |  |
| archived-20261005-235645: db.jsonl | 9102e1dea9 | 0.332 | 0.316 | 7,958 | 7,958 | 0.467 | 0.603 | 0.212 | 0.374 | 0.181 | 0.467 |  |
| archived-20261005-235645: db.jsonl | c9f3c95232 | 0.332 | 0.330 | 7,966 | 7,966 | 0.478 | 0.571 | 0.224 | 0.373 | 0.176 | 0.501 |  |
| archived-20261005-235645: db.jsonl | dcbaf0e29f | 0.334 | 0.329 | 9,014 | 9,014 | 0.472 | 0.605 | 0.220 | 0.367 | 0.180 | 0.469 |  |
| archived-20261006-012857: db.jsonl | 5347899701 | 0.433 | 0.431 | 6,903 | 6,903 | 0.413 | 0.761 | 0.181 | 0.329 | 0.810 | 0.797 |  |
| archived-20261006-012857: db.jsonl | 097ff5bdce | 0.411 | 0.406 | 6,913 | 6,913 | 0.404 | 0.715 | 0.172 | 0.328 | 0.717 | 0.776 | yes |
| archived-20261006-012857: db.jsonl | 520f651e31 | 0.417 | 0.406 | 6,914 | 6,914 | 0.415 | 0.740 | 0.181 | 0.325 | 0.695 | 0.766 |  |
| archived-20261006-012857: db.jsonl | e973e9ada8 | 0.413 | 0.405 | 6,940 | 6,940 | 0.419 | 0.729 | 0.181 | 0.331 | 0.655 | 0.782 |  |
| archived-20261006-012857: db.jsonl | 403bda0b3f | 0.330 | 0.315 | 7,017 | 7,017 | 0.432 | 0.786 | 0.187 | 0.329 | 0.187 | 0.582 |  |
| archived-20261006-012857: db.jsonl | ccf0eb9891 | 0.331 | 0.324 | 7,068 | 7,068 | 0.416 | 0.721 | 0.177 | 0.321 | 0.233 | 0.568 |  |
| archived-20261006-012857: db.jsonl | 1a5dc48b9c | 0.321 | 0.308 | 7,092 | 7,092 | 0.359 | 0.847 | 0.173 | 0.296 | 0.219 | 0.549 |  |
| archived-20261006-012857: db.jsonl | bdb87d827e | 0.318 | 0.304 | 7,124 | 7,124 | 0.382 | 0.941 | 0.159 | 0.301 | 0.190 | 0.560 |  |
| archived-20261006-012857: db.jsonl | ed927db5ce | 0.320 | 0.304 | 7,132 | 7,132 | 0.396 | 0.901 | 0.158 | 0.299 | 0.198 | 0.582 |  |
| archived-20261006-012857: db.jsonl | 76684cada6 | 0.304 | 0.303 | 7,166 | 7,166 | 0.381 | 0.787 | 0.157 | 0.291 | 0.189 | 0.550 |  |
| archived-20261006-012857: db.jsonl | 103cbedc80 | 0.301 | 0.290 | 7,238 | 7,238 | 0.370 | 0.784 | 0.162 | 0.283 | 0.186 | 0.535 |  |
| archived-20261006-012857: db.jsonl | 9c85c7d9f5 | 0.299 | 0.280 | 7,246 | 7,246 | 0.382 | 0.726 | 0.164 | 0.287 | 0.183 | 0.534 |  |
| archived-20261006-012857: db.jsonl | 3218bf9f21 | 0.293 | 0.287 | 7,666 | 7,666 | 0.361 | 0.759 | 0.161 | 0.278 | 0.176 | 0.570 |  |
| archived-20261006-012857: db.jsonl | cd8075731e | 0.291 | 0.278 | 7,773 | 7,773 | 0.395 | 0.553 | 0.161 | 0.308 | 0.193 | 0.485 |  |
| archived-20261006-012857: db.jsonl | ad62971982 | 0.284 | 0.268 | 7,799 | 7,799 | 0.373 | 0.602 | 0.156 | 0.290 | 0.181 | 0.488 |  |
| archived-20261006-012857: db.jsonl | db3dcdb1f8 | 0.287 | 0.272 | 10,181 | 10,181 | 0.386 | 0.582 | 0.160 | 0.289 | 0.187 | 0.556 |  |

The front of all runs together, by size: 419cce1726 0.240 at 8,320, 3995ab7bde 0.244 at 7,286, 285b6909d1 0.245 at 7,172, 03fcb0e3e6 0.264 at 7,089, 262f6959cc 0.265 at 7,057, 7033c6f1ab 0.326 at 7,017, 5e7eed1cba 0.336 at 6,951, 9a9d2cb947 0.352 at 6,947, 3c84b53247 0.379 at 6,939, 097ff5bdce 0.411 at 6,913, b7b4dd1166 0.426 at 6,911, 7f7d8e7864 0.433 at 6,903

## The same session on two CPUs

Calibration on cpu 2: 1.000; on cpu 8: 0.998.

Speed on cpu 2 over speed on cpu 8, per design: median 1.000, 10-90% 0.990-1.012, extremes 0.952-1.024; rank agreement (Spearman) 1.00.

The front of all runs on cpu 2: 419cce1726 0.240 at 8,320, 3995ab7bde 0.244 at 7,286, 285b6909d1 0.245 at 7,172, 03fcb0e3e6 0.264 at 7,089, 262f6959cc 0.265 at 7,057, 7033c6f1ab 0.326 at 7,017, 5e7eed1cba 0.336 at 6,951, 9a9d2cb947 0.352 at 6,947, 3c84b53247 0.379 at 6,939, 097ff5bdce 0.411 at 6,913, b7b4dd1166 0.426 at 6,911, 7f7d8e7864 0.433 at 6,903

The front of all runs on cpu 8: 419cce1726 0.235 at 8,320, 3995ab7bde 0.242 at 7,286, 285b6909d1 0.248 at 7,172, 262f6959cc 0.262 at 7,057, 7033c6f1ab 0.321 at 7,017, 5e7eed1cba 0.338 at 6,951, 9a9d2cb947 0.354 at 6,947, 3c84b53247 0.375 at 6,939, 3280937f3d 0.409 at 6,928, 520f651e31 0.413 at 6,914, 097ff5bdce 0.417 at 6,913, b7b4dd1166 0.428 at 6,911, 7f7d8e7864 0.435 at 6,903

On both fronts: 11 of 12 and 13.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| 419cce1726 | 0.240 | 0.235 | 1.021 |
| 3995ab7bde | 0.244 | 0.242 | 1.008 |
| 285b6909d1 | 0.245 | 0.248 | 0.991 |
| 364a0f4617 | 0.247 | 0.249 | 0.992 |
| 453a46a8e6 | 0.252 | 0.255 | 0.987 |
| 03fcb0e3e6 | 0.264 | 0.264 | 1.002 |
| 262f6959cc | 0.265 | 0.262 | 1.010 |
| ad62971982 | 0.284 | 0.280 | 1.013 |
| db3dcdb1f8 | 0.287 | 0.283 | 1.015 |
| cd8075731e | 0.291 | 0.292 | 0.998 |
| 3218bf9f21 | 0.293 | 0.293 | 0.999 |
| 9c85c7d9f5 | 0.299 | 0.292 | 1.024 |
| 103cbedc80 | 0.301 | 0.301 | 0.998 |
| 76684cada6 | 0.304 | 0.303 | 1.004 |
| bdb87d827e | 0.318 | 0.317 | 1.003 |
| ed927db5ce | 0.320 | 0.315 | 1.016 |
| 1a5dc48b9c | 0.321 | 0.322 | 0.998 |
| 7033c6f1ab | 0.326 | 0.321 | 1.016 |
| 828c84dd15 | 0.326 | 0.322 | 1.013 |
| 403bda0b3f | 0.330 | 0.330 | 0.998 |
| ccf0eb9891 | 0.331 | 0.329 | 1.005 |
| c9f3c95232 | 0.332 | 0.335 | 0.992 |
| 9102e1dea9 | 0.332 | 0.329 | 1.008 |
| dcbaf0e29f | 0.334 | 0.330 | 1.009 |
| 5e7eed1cba | 0.336 | 0.338 | 0.993 |
| 1918ae250d | 0.350 | 0.348 | 1.007 |
| 9a9d2cb947 | 0.352 | 0.354 | 0.994 |
| 9a482dbeaf | 0.352 | 0.356 | 0.989 |
| 040e367ce9 | 0.354 | 0.354 | 1.002 |
| 35135bde2f | 0.378 | 0.376 | 1.007 |
| 3c84b53247 | 0.379 | 0.375 | 1.009 |
| 20b3bde0c3 | 0.385 | 0.389 | 0.990 |
| 097ff5bdce | 0.411 | 0.417 | 0.985 |
| e973e9ada8 | 0.413 | 0.414 | 0.998 |
| ced47e8cfa | 0.413 | 0.410 | 1.008 |
| 3280937f3d | 0.416 | 0.409 | 1.015 |
| 520f651e31 | 0.417 | 0.413 | 1.008 |
| b7b4dd1166 | 0.426 | 0.428 | 0.995 |
| 37b502fac7 | 0.426 | 0.434 | 0.982 |
| 7f7d8e7864 | 0.433 | 0.435 | 0.994 |
| 5347899701 | 0.433 | 0.437 | 0.990 |
| 9bb527944a | 0.436 | 0.439 | 0.993 |
| ff3e6b2a34 | 0.436 | 0.439 | 0.992 |
| ff306b06c1 | 0.438 | 0.437 | 1.003 |
| 84a09433d4 | 0.439 | 0.441 | 0.994 |
| 627568164d | 0.447 | 0.441 | 1.013 |
| cac62ca533 | 0.454 | 0.461 | 0.985 |
| 6827e42d47 | 0.459 | 0.459 | 0.999 |
| 049e0c9c48 | 0.462 | 0.459 | 1.006 |
| 577c999e62 | 0.464 | 0.465 | 0.997 |
| 0212f86508 | 0.472 | 0.474 | 0.994 |
| 959e88b0f5 | 0.473 | 0.469 | 1.008 |
| 1b602bc9bd | 0.474 | 0.498 | 0.952 |
| 7a8d429413 | 0.474 | 0.482 | 0.984 |
| cda8cad59b | 0.480 | 0.491 | 0.978 |
| 72ca2cf497 | 0.482 | 0.477 | 1.011 |
| 0f90ffc36a | 0.482 | 0.485 | 0.994 |
| 2c9b948725 | 0.483 | 0.486 | 0.994 |
| 96f2d8bfd7 | 0.483 | 0.489 | 0.989 |
| aba06380d6 | 0.485 | 0.488 | 0.993 |
| 988d608671 | 0.485 | 0.483 | 1.003 |
| 85a977e3ed | 0.490 | 0.489 | 1.001 |
| 9d89f6ba0e | 0.490 | 0.500 | 0.980 |
| c2d99350f1 | 0.492 | 0.495 | 0.993 |
| f85a63f8c7 | 0.499 | 0.505 | 0.988 |
| 641b85143d | 0.499 | 0.498 | 1.002 |
| 46fbc9e912 | 0.502 | 0.501 | 1.002 |
| 55ca1dfdb5 | 0.504 | 0.502 | 1.002 |
| 63919635b7 | 0.504 | 0.506 | 0.997 |
| 85cac726b5 | 0.505 | 0.504 | 1.002 |
| 0e8b212e50 | 0.509 | 0.505 | 1.008 |
| 2ed8b1583e | 0.509 | 0.509 | 1.001 |
| 45d2ff7e01 | 0.512 | 0.511 | 1.002 |
| 51879a71f0 | 0.513 | 0.514 | 0.999 |
| f084674b22 | 0.515 | 0.515 | 1.000 |
| f3988ea716 | 0.520 | 0.521 | 0.998 |
| 3d31fd4cc4 | 0.527 | 0.519 | 1.014 |
| 6578fc6928 | 0.530 | 0.531 | 0.998 |
| 853cfb9d36 | 0.537 | 0.548 | 0.980 |
| caf4358de8 | 0.542 | 0.538 | 1.007 |
| fa23f401cd | 0.543 | 0.536 | 1.013 |
| 2367cb920c | 0.543 | 0.547 | 0.993 |
| d8d62beb78 | 0.549 | 0.546 | 1.005 |
| be02a4c0cf | 0.549 | 0.548 | 1.002 |
| 3f1d365b3b | 0.589 | 0.592 | 0.994 |
| cd943ed219 | 0.591 | 0.590 | 1.002 |
| 31a3ceea45 | 0.593 | 0.588 | 1.008 |
| 15dde12f04 | 0.593 | 0.599 | 0.991 |
| 6ba318d95c | 0.595 | 0.603 | 0.987 |
| a214fa731c | 0.604 | 0.592 | 1.020 |
| dc02ceae31 | 0.606 | 0.608 | 0.996 |
| 3a7c3d6e90 | 0.609 | 0.610 | 0.998 |
| 7b9675c9ef | 0.610 | 0.606 | 1.007 |
| 1cf03a8fd4 | 0.610 | 0.605 | 1.008 |
| 2b00aa6e97 | 0.613 | 0.609 | 1.005 |
| 4cc12fc1e7 | 0.624 | 0.626 | 0.997 |
| 27a35df3fa | 0.630 | 0.627 | 1.005 |
| ff39b37bcc | 0.639 | 0.630 | 1.014 |
| 05617039f6 | 0.643 | 0.639 | 1.006 |
| 29ad5ba726 | 0.644 | 0.645 | 0.999 |
| 2816900bac | 0.651 | 0.654 | 0.995 |
| 22b81e50c4 | 0.652 | 0.658 | 0.991 |
| 8dd8a7a146 | 0.653 | 0.642 | 1.017 |
| e99da68667 | 0.654 | 0.653 | 1.001 |
| 2db525ff95 | 0.655 | 0.650 | 1.008 |
| 3c2d8a577b | 0.655 | 0.659 | 0.994 |
| 5df0608416 | 0.657 | 0.661 | 0.993 |
| 8a2189b3b6 | 0.657 | 0.649 | 1.013 |
| 1769ca2a48 | 0.658 | 0.656 | 1.002 |
| 88792f1798 | 0.658 | 0.659 | 0.999 |
| c61857fc89 | 0.658 | 0.657 | 1.002 |
| 7380e8bcb1 | 0.660 | 0.657 | 1.005 |
| 9e50623ac1 | 0.660 | 0.661 | 0.999 |
| b06a4cf784 | 0.664 | 0.662 | 1.003 |
| c40ba92d5b | 0.664 | 0.664 | 1.000 |
| bf413bef91 | 0.667 | 0.670 | 0.996 |
| a74b828e9b | 0.667 | 0.667 | 1.001 |
| af5e8dc29f | 0.669 | 0.663 | 1.010 |
| a306cc61fb | 0.672 | 0.677 | 0.993 |
| c25a5e1714 | 0.674 | 0.676 | 0.997 |
| 66eb4a8f15 | 0.677 | 0.682 | 0.993 |
| 98e6135b93 | 0.680 | 0.673 | 1.010 |
| 32600cab87 | 0.681 | 0.677 | 1.005 |
| 0b1d16def9 | 0.682 | 0.682 | 1.000 |
| ca2ac63866 | 0.682 | 0.684 | 0.997 |
| 14f6036a4b | 0.682 | 0.680 | 1.004 |
| f060a4c31f | 0.682 | 0.681 | 1.002 |
| 4cb3fa9172 | 0.685 | 0.683 | 1.003 |
| 6495dcb5dd | 0.685 | 0.686 | 0.999 |
| f66d74a27c | 0.688 | 0.690 | 0.997 |
| 312ad2edaa | 0.689 | 0.684 | 1.008 |
| 9f5e6d173c | 0.690 | 0.688 | 1.003 |
| ccce4784b8 | 0.692 | 0.690 | 1.003 |
| 448ef1ef43 | 0.692 | 0.690 | 1.003 |
| 60753a0eb0 | 0.692 | 0.693 | 0.999 |
| 49b0a93f14 | 0.694 | 0.698 | 0.994 |
| e05adba602 | 0.694 | 0.697 | 0.996 |
| 38d187239c | 0.694 | 0.704 | 0.987 |
| a27aa49d8e | 0.695 | 0.699 | 0.995 |
| 9385a8fcbb | 0.696 | 0.692 | 1.006 |
| d0d304e240 | 0.697 | 0.700 | 0.995 |
| 5ed1ed8715 | 0.701 | 0.705 | 0.995 |
| bb8a0cb575 | 0.702 | 0.696 | 1.008 |
| e0cbf09bc2 | 0.703 | 0.702 | 1.001 |
| 6463752a82 | 0.704 | 0.706 | 0.997 |
| 52b80007a1 | 0.706 | 0.709 | 0.995 |
| 12d8e18511 | 0.708 | 0.698 | 1.014 |
| c297551359 | 0.709 | 0.706 | 1.004 |
| 38d91795a2 | 0.710 | 0.709 | 1.002 |
| 53ec9bedde | 0.721 | 0.733 | 0.984 |
| f4a6dd9a13 | 0.721 | 0.728 | 0.991 |
| 84e302c470 | 0.722 | 0.713 | 1.012 |
| ee4d8f8a50 | 0.722 | 0.727 | 0.994 |
| 8cbc6dd05c | 0.723 | 0.726 | 0.996 |
| 8dc0f97f2c | 0.724 | 0.713 | 1.016 |
| f052397620 | 0.726 | 0.728 | 0.998 |
| 7fe7f039bd | 0.727 | 0.728 | 0.999 |
| d4739aac88 | 0.729 | 0.723 | 1.007 |
| 7cb20d14b1 | 0.730 | 0.733 | 0.997 |
| 82e7e4dc0d | 0.731 | 0.721 | 1.014 |
| e8f1dd3ca2 | 0.731 | 0.728 | 1.004 |
| a285fa6ba3 | 0.733 | 0.736 | 0.995 |
| 090672993b | 0.735 | 0.738 | 0.997 |
| 422d6bcbca | 0.740 | 0.732 | 1.011 |
| 550df563ee | 0.740 | 0.740 | 1.000 |
| 57a9dcc7cb | 0.741 | 0.735 | 1.007 |
| 05dcc81cdc | 0.745 | 0.739 | 1.008 |
| 528fc9619a | 0.749 | 0.754 | 0.993 |
| 3453246bdf | 0.750 | 0.754 | 0.994 |
| 595fc2b8f4 | 0.753 | 0.754 | 0.999 |
| 3781c5e756 | 0.754 | 0.761 | 0.991 |
| 5b70f3dd64 | 0.757 | 0.766 | 0.989 |
| 57d12a1bb0 | 0.759 | 0.764 | 0.994 |
| 295a6acd98 | 0.760 | 0.758 | 1.002 |
| 9cd791dd84 | 0.761 | 0.755 | 1.008 |
| 4032a5ce71 | 0.761 | 0.754 | 1.009 |
| 6738aed13f | 0.763 | 0.759 | 1.005 |
| 57e0e77c09 | 0.763 | 0.758 | 1.007 |
| 4f010d8ab9 | 0.770 | 0.770 | 1.000 |
| 98736f0596 | 0.773 | 0.778 | 0.994 |
| 0ebf0445e0 | 0.777 | 0.774 | 1.004 |
| c17103bf95 | 0.781 | 0.784 | 0.996 |
| 90018981c6 | 0.782 | 0.778 | 1.005 |
| c513ef17b0 | 0.789 | 0.787 | 1.003 |
| a4e82e02e5 | 0.802 | 0.803 | 0.998 |
| 672538daf5 | 0.821 | 0.826 | 0.994 |
| 83cb81c383 | 0.831 | 0.840 | 0.989 |
| f41ab1810d | 1.005 | 1.010 | 0.995 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 13 - Iteration 63: seed 15 and the newest four runs

`seed 15 then experiment compare-fronts.py --rounds 10 --cpus 2,8`, commit
6d2696f7 - the first session capped (next-run.sh, COMPARE_LAST 4): seed
15 and seeds 11-14, 72 front designs, eight minutes. **Calibration
0.994** (fib 0.968, parse 0.974, the rest 1.001-1.020). The CPUs agree:
per design median 1.006, 10-90% 0.986-1.025, ranks 1.00; 13 of 14 and 15
designs on both CPUs' fronts.

**The front of all runs: seed 15's thirteen** - 6,654 bytes (0.433) to
7,958 (0.230, the fastest yet) - and seed 14's 3995ab7bde (0.238 at
7,286).

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 0.994** (kernel 1.006, fib 0.968, parse 0.974, corpus 1.006, loop 1.020, sieve 1.001).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 58c0a33fbe | 0.433 | 0.417 | 6,654 | 6,654 | 0.408 | 0.910 | 0.178 | 0.330 | 0.699 | 0.811 | yes |
| this clone: db.jsonl | 29b1a365dc | 0.420 | 0.415 | 6,655 | 6,655 | 0.419 | 0.735 | 0.185 | 0.313 | 0.731 | 0.789 | yes |
| this clone: db.jsonl | eabd014b0c | 0.400 | 0.402 | 6,673 | 6,673 | 0.396 | 0.698 | 0.177 | 0.301 | 0.694 | 0.752 | yes |
| this clone: db.jsonl | 0df4c46cec | 0.413 | 0.412 | 6,680 | 6,680 | 0.414 | 0.768 | 0.183 | 0.312 | 0.656 | 0.739 |  |
| this clone: db.jsonl | 1d44bcb8a5 | 0.353 | 0.358 | 6,693 | 6,693 | 0.344 | 0.753 | 0.111 | 0.245 | 0.780 | 0.805 | yes |
| this clone: db.jsonl | 9c2db9aebe | 0.345 | 0.353 | 6,699 | 6,699 | 0.346 | 0.693 | 0.111 | 0.245 | 0.747 | 0.733 | yes |
| this clone: db.jsonl | f1c82fbd44 | 0.342 | 0.336 | 6,700 | 6,700 | 0.306 | 0.716 | 0.103 | 0.222 | 0.937 | 0.762 | yes |
| this clone: db.jsonl | 9f9bfa4f49 | 0.338 | 0.334 | 6,711 | 6,711 | 0.306 | 0.725 | 0.107 | 0.224 | 0.831 | 0.725 | yes |
| this clone: db.jsonl | eb0033be3d | 0.328 | 0.331 | 6,759 | 6,759 | 0.292 | 0.712 | 0.103 | 0.218 | 0.819 | 0.726 | yes |
| this clone: db.jsonl | ce2e13ce87 | 0.308 | 0.311 | 6,777 | 6,777 | 0.399 | 0.722 | 0.186 | 0.317 | 0.162 | 0.595 | yes |
| this clone: db.jsonl | d1b2f540a8 | 0.251 | 0.243 | 6,817 | 6,817 | 0.363 | 0.673 | 0.106 | 0.229 | 0.167 | 0.511 | yes |
| this clone: db.jsonl | cbbc5291f8 | 0.239 | 0.246 | 6,940 | 6,940 | 0.323 | 0.679 | 0.093 | 0.216 | 0.178 | 0.517 | yes |
| this clone: db.jsonl | 773f6d9daf | 0.242 | 0.239 | 6,993 | 6,993 | 0.328 | 0.679 | 0.097 | 0.216 | 0.178 | 0.450 |  |
| this clone: db.jsonl | 8298ca5d59 | 0.234 | 0.236 | 7,310 | 7,310 | 0.323 | 0.616 | 0.091 | 0.210 | 0.184 | 0.532 | yes |
| this clone: db.jsonl | 3a96a12236 | 0.230 | 0.225 | 7,958 | 7,958 | 0.337 | 0.554 | 0.096 | 0.214 | 0.168 | 0.503 | yes |
| archived-20261005-222307: db.jsonl | 7cb20d14b1 | 0.719 | 0.718 | 6,971 | 6,971 | 0.773 | 0.749 | 0.598 | 0.692 | 0.800 | 0.907 |  |
| archived-20261005-222307: db.jsonl | d0d304e240 | 0.697 | 0.684 | 6,977 | 6,977 | 0.715 | 0.806 | 0.536 | 0.642 | 0.829 | 0.795 |  |
| archived-20261005-222307: db.jsonl | 98e6135b93 | 0.674 | 0.678 | 6,978 | 6,978 | 0.652 | 0.755 | 0.508 | 0.621 | 0.894 | 0.852 |  |
| archived-20261005-222307: db.jsonl | 6ba318d95c | 0.606 | 0.601 | 6,989 | 6,989 | 0.590 | 0.737 | 0.431 | 0.534 | 0.816 | 0.858 |  |
| archived-20261005-222307: db.jsonl | 7b9675c9ef | 0.599 | 0.604 | 7,004 | 7,004 | 0.606 | 0.747 | 0.436 | 0.547 | 0.715 | 0.843 |  |
| archived-20261005-222307: db.jsonl | 31a3ceea45 | 0.582 | 0.582 | 7,037 | 7,037 | 0.579 | 0.735 | 0.441 | 0.508 | 0.704 | 0.820 |  |
| archived-20261005-222307: db.jsonl | 3f1d365b3b | 0.590 | 0.590 | 7,061 | 7,061 | 0.597 | 0.707 | 0.422 | 0.517 | 0.777 | 0.834 |  |
| archived-20261005-222307: db.jsonl | 63919635b7 | 0.498 | 0.502 | 7,089 | 7,089 | 0.677 | 0.688 | 0.506 | 0.605 | 0.216 | 0.597 |  |
| archived-20261005-222307: db.jsonl | 2c9b948725 | 0.486 | 0.481 | 7,097 | 7,097 | 0.608 | 0.983 | 0.441 | 0.521 | 0.196 | 0.636 |  |
| archived-20261005-222307: db.jsonl | cac62ca533 | 0.456 | 0.450 | 7,105 | 7,105 | 0.603 | 0.825 | 0.425 | 0.505 | 0.185 | 0.614 |  |
| archived-20261005-222307: db.jsonl | 627568164d | 0.446 | 0.447 | 7,147 | 7,147 | 0.597 | 0.703 | 0.419 | 0.524 | 0.191 | 0.643 |  |
| archived-20261005-222307: db.jsonl | 37b502fac7 | 0.429 | 0.433 | 7,238 | 7,238 | 0.556 | 0.719 | 0.404 | 0.491 | 0.184 | 0.565 |  |
| archived-20261005-222307: db.jsonl | ced47e8cfa | 0.409 | 0.406 | 8,030 | 8,030 | 0.584 | 0.486 | 0.424 | 0.506 | 0.188 | 0.549 |  |
| archived-20261005-235645: db.jsonl | 2816900bac | 0.651 | 0.638 | 6,941 | 6,941 | 0.620 | 0.797 | 0.495 | 0.563 | 0.848 | 0.846 |  |
| archived-20261005-235645: db.jsonl | 46fbc9e912 | 0.503 | 0.491 | 6,966 | 6,966 | 0.501 | 0.978 | 0.252 | 0.396 | 0.658 | 0.767 |  |
| archived-20261005-235645: db.jsonl | c2d99350f1 | 0.490 | 0.481 | 6,974 | 6,974 | 0.512 | 0.710 | 0.230 | 0.386 | 0.877 | 0.859 |  |
| archived-20261005-235645: db.jsonl | 0f90ffc36a | 0.476 | 0.474 | 6,998 | 6,998 | 0.505 | 0.714 | 0.233 | 0.391 | 0.740 | 0.840 |  |
| archived-20261005-235645: db.jsonl | 988d608671 | 0.483 | 0.478 | 7,014 | 7,014 | 0.525 | 0.704 | 0.236 | 0.399 | 0.753 | 0.815 |  |
| archived-20261005-235645: db.jsonl | 20b3bde0c3 | 0.384 | 0.385 | 7,097 | 7,097 | 0.512 | 0.883 | 0.249 | 0.382 | 0.194 | 0.671 |  |
| archived-20261005-235645: db.jsonl | 35135bde2f | 0.366 | 0.371 | 7,105 | 7,105 | 0.483 | 0.788 | 0.234 | 0.365 | 0.201 | 0.616 |  |
| archived-20261005-235645: db.jsonl | 9a482dbeaf | 0.346 | 0.351 | 7,334 | 7,334 | 0.457 | 0.871 | 0.214 | 0.345 | 0.168 | 0.556 |  |
| archived-20261005-235645: db.jsonl | 040e367ce9 | 0.354 | 0.343 | 7,753 | 7,753 | 0.485 | 0.788 | 0.218 | 0.357 | 0.187 | 0.576 |  |
| archived-20261005-235645: db.jsonl | 1918ae250d | 0.344 | 0.346 | 7,820 | 7,820 | 0.511 | 0.526 | 0.227 | 0.370 | 0.214 | 0.540 |  |
| archived-20261005-235645: db.jsonl | 9102e1dea9 | 0.321 | 0.316 | 7,958 | 7,958 | 0.475 | 0.588 | 0.211 | 0.347 | 0.166 | 0.477 |  |
| archived-20261005-235645: db.jsonl | c9f3c95232 | 0.324 | 0.330 | 7,966 | 7,966 | 0.477 | 0.570 | 0.222 | 0.363 | 0.164 | 0.490 |  |
| archived-20261005-235645: db.jsonl | dcbaf0e29f | 0.327 | 0.329 | 9,014 | 9,014 | 0.470 | 0.604 | 0.214 | 0.353 | 0.175 | 0.467 |  |
| archived-20261006-012857: db.jsonl | 5347899701 | 0.424 | 0.431 | 6,903 | 6,903 | 0.406 | 0.751 | 0.178 | 0.317 | 0.797 | 0.790 |  |
| archived-20261006-012857: db.jsonl | 097ff5bdce | 0.418 | 0.406 | 6,913 | 6,913 | 0.402 | 0.741 | 0.179 | 0.333 | 0.718 | 0.782 |  |
| archived-20261006-012857: db.jsonl | 520f651e31 | 0.409 | 0.406 | 6,914 | 6,914 | 0.415 | 0.716 | 0.174 | 0.326 | 0.677 | 0.765 |  |
| archived-20261006-012857: db.jsonl | e973e9ada8 | 0.410 | 0.405 | 6,940 | 6,940 | 0.427 | 0.735 | 0.181 | 0.314 | 0.649 | 0.774 |  |
| archived-20261006-012857: db.jsonl | 403bda0b3f | 0.329 | 0.315 | 7,017 | 7,017 | 0.423 | 0.806 | 0.184 | 0.325 | 0.189 | 0.559 |  |
| archived-20261006-012857: db.jsonl | ccf0eb9891 | 0.326 | 0.324 | 7,068 | 7,068 | 0.414 | 0.718 | 0.173 | 0.312 | 0.230 | 0.564 |  |
| archived-20261006-012857: db.jsonl | 1a5dc48b9c | 0.305 | 0.308 | 7,092 | 7,092 | 0.353 | 0.835 | 0.170 | 0.274 | 0.192 | 0.526 |  |
| archived-20261006-012857: db.jsonl | bdb87d827e | 0.312 | 0.304 | 7,124 | 7,124 | 0.382 | 0.920 | 0.150 | 0.298 | 0.188 | 0.524 |  |
| archived-20261006-012857: db.jsonl | ed927db5ce | 0.316 | 0.304 | 7,132 | 7,132 | 0.403 | 0.880 | 0.155 | 0.285 | 0.202 | 0.584 |  |
| archived-20261006-012857: db.jsonl | 76684cada6 | 0.305 | 0.303 | 7,166 | 7,166 | 0.377 | 0.815 | 0.159 | 0.286 | 0.189 | 0.539 |  |
| archived-20261006-012857: db.jsonl | 103cbedc80 | 0.293 | 0.290 | 7,238 | 7,238 | 0.358 | 0.760 | 0.160 | 0.286 | 0.175 | 0.526 |  |
| archived-20261006-012857: db.jsonl | 9c85c7d9f5 | 0.292 | 0.280 | 7,246 | 7,246 | 0.374 | 0.742 | 0.162 | 0.263 | 0.180 | 0.525 |  |
| archived-20261006-012857: db.jsonl | 3218bf9f21 | 0.290 | 0.287 | 7,666 | 7,666 | 0.357 | 0.763 | 0.154 | 0.281 | 0.174 | 0.570 |  |
| archived-20261006-012857: db.jsonl | cd8075731e | 0.283 | 0.278 | 7,773 | 7,773 | 0.384 | 0.538 | 0.158 | 0.282 | 0.196 | 0.482 |  |
| archived-20261006-012857: db.jsonl | ad62971982 | 0.279 | 0.268 | 7,799 | 7,799 | 0.367 | 0.595 | 0.157 | 0.286 | 0.170 | 0.485 |  |
| archived-20261006-012857: db.jsonl | db3dcdb1f8 | 0.277 | 0.272 | 10,181 | 10,181 | 0.375 | 0.585 | 0.156 | 0.287 | 0.168 | 0.541 |  |
| archived-20261006-024824: db.jsonl | 7f7d8e7864 | 0.430 | 0.435 | 6,903 | 6,903 | 0.411 | 0.770 | 0.180 | 0.320 | 0.805 | 0.803 |  |
| archived-20261006-024824: db.jsonl | b7b4dd1166 | 0.421 | 0.422 | 6,911 | 6,911 | 0.410 | 0.789 | 0.174 | 0.317 | 0.742 | 0.773 |  |
| archived-20261006-024824: db.jsonl | 3280937f3d | 0.412 | 0.416 | 6,928 | 6,928 | 0.434 | 0.734 | 0.174 | 0.318 | 0.671 | 0.805 |  |
| archived-20261006-024824: db.jsonl | 3c84b53247 | 0.375 | 0.377 | 6,939 | 6,939 | 0.330 | 0.805 | 0.114 | 0.247 | 0.992 | 0.817 |  |
| archived-20261006-024824: db.jsonl | 9a9d2cb947 | 0.352 | 0.357 | 6,947 | 6,947 | 0.360 | 0.694 | 0.114 | 0.259 | 0.725 | 0.768 |  |
| archived-20261006-024824: db.jsonl | 5e7eed1cba | 0.330 | 0.333 | 6,951 | 6,951 | 0.363 | 0.619 | 0.114 | 0.250 | 0.611 | 0.696 |  |
| archived-20261006-024824: db.jsonl | 7033c6f1ab | 0.323 | 0.323 | 7,017 | 7,017 | 0.400 | 0.816 | 0.178 | 0.322 | 0.187 | 0.561 |  |
| archived-20261006-024824: db.jsonl | 828c84dd15 | 0.316 | 0.317 | 7,026 | 7,026 | 0.421 | 0.749 | 0.184 | 0.311 | 0.174 | 0.547 |  |
| archived-20261006-024824: db.jsonl | 262f6959cc | 0.257 | 0.259 | 7,057 | 7,057 | 0.352 | 0.671 | 0.108 | 0.245 | 0.179 | 0.546 |  |
| archived-20261006-024824: db.jsonl | 03fcb0e3e6 | 0.259 | 0.263 | 7,089 | 7,089 | 0.359 | 0.681 | 0.105 | 0.259 | 0.178 | 0.555 |  |
| archived-20261006-024824: db.jsonl | 285b6909d1 | 0.240 | 0.248 | 7,172 | 7,172 | 0.339 | 0.620 | 0.094 | 0.218 | 0.184 | 0.544 |  |
| archived-20261006-024824: db.jsonl | 453a46a8e6 | 0.250 | 0.254 | 7,188 | 7,188 | 0.338 | 0.710 | 0.096 | 0.233 | 0.181 | 0.498 |  |
| archived-20261006-024824: db.jsonl | 3995ab7bde | 0.238 | 0.243 | 7,286 | 7,286 | 0.315 | 0.653 | 0.097 | 0.212 | 0.179 | 0.557 | yes |
| archived-20261006-024824: db.jsonl | 364a0f4617 | 0.241 | 0.249 | 7,689 | 7,689 | 0.308 | 0.756 | 0.093 | 0.220 | 0.172 | 0.449 |  |
| archived-20261006-024824: db.jsonl | 419cce1726 | 0.232 | 0.238 | 8,320 | 8,320 | 0.327 | 0.547 | 0.098 | 0.213 | 0.181 | 0.502 |  |

The front of all runs together, by size: 3a96a12236 0.230 at 7,958, 8298ca5d59 0.234 at 7,310, 3995ab7bde 0.238 at 7,286, cbbc5291f8 0.239 at 6,940, d1b2f540a8 0.251 at 6,817, ce2e13ce87 0.308 at 6,777, eb0033be3d 0.328 at 6,759, 9f9bfa4f49 0.338 at 6,711, f1c82fbd44 0.342 at 6,700, 9c2db9aebe 0.345 at 6,699, 1d44bcb8a5 0.353 at 6,693, eabd014b0c 0.400 at 6,673, 29b1a365dc 0.420 at 6,655, 58c0a33fbe 0.433 at 6,654

## The same session on two CPUs

Calibration on cpu 2: 0.994; on cpu 8: 0.996.

Speed on cpu 2 over speed on cpu 8, per design: median 1.006, 10-90% 0.986-1.025, extremes 0.960-1.040; rank agreement (Spearman) 1.00.

The front of all runs on cpu 2: 3a96a12236 0.230 at 7,958, 8298ca5d59 0.234 at 7,310, 3995ab7bde 0.238 at 7,286, cbbc5291f8 0.239 at 6,940, d1b2f540a8 0.251 at 6,817, ce2e13ce87 0.308 at 6,777, eb0033be3d 0.328 at 6,759, 9f9bfa4f49 0.338 at 6,711, f1c82fbd44 0.342 at 6,700, 9c2db9aebe 0.345 at 6,699, 1d44bcb8a5 0.353 at 6,693, eabd014b0c 0.400 at 6,673, 29b1a365dc 0.420 at 6,655, 58c0a33fbe 0.433 at 6,654

The front of all runs on cpu 8: 419cce1726 0.227 at 8,320, 3a96a12236 0.232 at 7,958, 8298ca5d59 0.234 at 7,310, 773f6d9daf 0.237 at 6,993, cbbc5291f8 0.240 at 6,940, d1b2f540a8 0.244 at 6,817, ce2e13ce87 0.309 at 6,777, eb0033be3d 0.329 at 6,759, 9f9bfa4f49 0.333 at 6,711, f1c82fbd44 0.339 at 6,700, 9c2db9aebe 0.350 at 6,699, 1d44bcb8a5 0.354 at 6,693, eabd014b0c 0.405 at 6,673, 29b1a365dc 0.426 at 6,655, 58c0a33fbe 0.427 at 6,654

On both fronts: 13 of 14 and 15.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| 3a96a12236 | 0.230 | 0.232 | 0.992 |
| 419cce1726 | 0.232 | 0.227 | 1.021 |
| 8298ca5d59 | 0.234 | 0.234 | 0.998 |
| 3995ab7bde | 0.238 | 0.238 | 1.001 |
| cbbc5291f8 | 0.239 | 0.240 | 0.997 |
| 285b6909d1 | 0.240 | 0.243 | 0.985 |
| 364a0f4617 | 0.241 | 0.238 | 1.016 |
| 773f6d9daf | 0.242 | 0.237 | 1.024 |
| 453a46a8e6 | 0.250 | 0.246 | 1.017 |
| d1b2f540a8 | 0.251 | 0.244 | 1.025 |
| 262f6959cc | 0.257 | 0.260 | 0.987 |
| 03fcb0e3e6 | 0.259 | 0.257 | 1.011 |
| db3dcdb1f8 | 0.277 | 0.280 | 0.989 |
| ad62971982 | 0.279 | 0.278 | 1.003 |
| cd8075731e | 0.283 | 0.287 | 0.986 |
| 3218bf9f21 | 0.290 | 0.283 | 1.025 |
| 9c85c7d9f5 | 0.292 | 0.292 | 1.001 |
| 103cbedc80 | 0.293 | 0.282 | 1.040 |
| 1a5dc48b9c | 0.305 | 0.317 | 0.960 |
| 76684cada6 | 0.305 | 0.297 | 1.026 |
| ce2e13ce87 | 0.308 | 0.309 | 0.995 |
| bdb87d827e | 0.312 | 0.305 | 1.025 |
| 828c84dd15 | 0.316 | 0.317 | 0.997 |
| ed927db5ce | 0.316 | 0.305 | 1.037 |
| 9102e1dea9 | 0.321 | 0.320 | 1.003 |
| 7033c6f1ab | 0.323 | 0.317 | 1.019 |
| c9f3c95232 | 0.324 | 0.325 | 0.998 |
| ccf0eb9891 | 0.326 | 0.324 | 1.007 |
| dcbaf0e29f | 0.327 | 0.321 | 1.020 |
| eb0033be3d | 0.328 | 0.329 | 0.998 |
| 403bda0b3f | 0.329 | 0.327 | 1.005 |
| 5e7eed1cba | 0.330 | 0.328 | 1.008 |
| 9f9bfa4f49 | 0.338 | 0.333 | 1.015 |
| f1c82fbd44 | 0.342 | 0.339 | 1.007 |
| 1918ae250d | 0.344 | 0.341 | 1.009 |
| 9c2db9aebe | 0.345 | 0.350 | 0.984 |
| 9a482dbeaf | 0.346 | 0.344 | 1.006 |
| 9a9d2cb947 | 0.352 | 0.349 | 1.008 |
| 1d44bcb8a5 | 0.353 | 0.354 | 0.996 |
| 040e367ce9 | 0.354 | 0.345 | 1.027 |
| 35135bde2f | 0.366 | 0.374 | 0.978 |
| 3c84b53247 | 0.375 | 0.373 | 1.004 |
| 20b3bde0c3 | 0.384 | 0.387 | 0.993 |
| eabd014b0c | 0.400 | 0.405 | 0.987 |
| 520f651e31 | 0.409 | 0.406 | 1.007 |
| ced47e8cfa | 0.409 | 0.408 | 1.002 |
| e973e9ada8 | 0.410 | 0.403 | 1.017 |
| 3280937f3d | 0.412 | 0.403 | 1.021 |
| 0df4c46cec | 0.413 | 0.414 | 0.996 |
| 097ff5bdce | 0.418 | 0.413 | 1.014 |
| 29b1a365dc | 0.420 | 0.426 | 0.986 |
| b7b4dd1166 | 0.421 | 0.421 | 1.000 |
| 5347899701 | 0.424 | 0.438 | 0.969 |
| 37b502fac7 | 0.429 | 0.428 | 1.002 |
| 7f7d8e7864 | 0.430 | 0.428 | 1.004 |
| 58c0a33fbe | 0.433 | 0.427 | 1.016 |
| 627568164d | 0.446 | 0.443 | 1.007 |
| cac62ca533 | 0.456 | 0.445 | 1.026 |
| 0f90ffc36a | 0.476 | 0.477 | 0.996 |
| 988d608671 | 0.483 | 0.482 | 1.002 |
| 2c9b948725 | 0.486 | 0.479 | 1.014 |
| c2d99350f1 | 0.490 | 0.485 | 1.012 |
| 63919635b7 | 0.498 | 0.498 | 1.001 |
| 46fbc9e912 | 0.503 | 0.494 | 1.019 |
| 31a3ceea45 | 0.582 | 0.588 | 0.990 |
| 3f1d365b3b | 0.590 | 0.583 | 1.012 |
| 7b9675c9ef | 0.599 | 0.603 | 0.993 |
| 6ba318d95c | 0.606 | 0.597 | 1.015 |
| 2816900bac | 0.651 | 0.645 | 1.010 |
| 98e6135b93 | 0.674 | 0.662 | 1.018 |
| d0d304e240 | 0.697 | 0.689 | 1.012 |
| 7cb20d14b1 | 0.719 | 0.734 | 0.979 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 14 - Iteration 72: seed 16 (the two-bit tag) and the newest four

`seed 16 tag2 then experiment compare-fronts.py --rounds 10 --cpus 2,8`,
commit 10af4929: seed 16 - every design in the tag - and seeds 12-15, 70
front designs, eight minutes. **Calibration 1.001** (corpus 0.976, the
rest 0.988-1.011). The CPUs: per design median 1.009, 10-90% 0.994-1.031,
ranks 0.99; 9 of 13 and 10 designs on both fronts.

**The front of all runs: the old format's** - seed 15's twelve, seed
14's 285b6909d1. Seed 16's front, 7,009-7,708 bytes, is behind it by the
format's price.

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 1.001** (kernel 1.007, fib 1.007, parse 1.011, corpus 0.976, loop 1.003, sieve 0.988).

| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 0826d64cd9 | 0.424 | 0.420 | 7,009 | 7,009 | 0.462 | 0.547 | 0.176 | 0.330 | 0.938 | 0.732 |  |
| this clone: db.jsonl | 69270766bd | 0.363 | 0.372 | 7,049 | 7,049 | 0.402 | 0.633 | 0.110 | 0.242 | 0.937 | 0.785 |  |
| this clone: db.jsonl | df2ac6c7ab | 0.339 | 0.338 | 7,050 | 7,050 | 0.407 | 0.452 | 0.109 | 0.246 | 0.900 | 0.768 |  |
| this clone: db.jsonl | 323f2ccfb8 | 0.330 | 0.334 | 7,105 | 7,105 | 0.345 | 0.628 | 0.104 | 0.203 | 0.860 | 0.781 |  |
| this clone: db.jsonl | 7c49a5ffca | 0.330 | 0.324 | 7,123 | 7,123 | 0.363 | 0.551 | 0.097 | 0.215 | 0.935 | 0.837 |  |
| this clone: db.jsonl | 2b5e92dd57 | 0.346 | 0.345 | 7,186 | 7,186 | 0.495 | 0.870 | 0.191 | 0.336 | 0.178 | 0.561 |  |
| this clone: db.jsonl | bfa7370096 | 0.338 | 0.326 | 7,202 | 7,202 | 0.376 | 0.615 | 0.107 | 0.215 | 0.823 | 0.761 |  |
| this clone: db.jsonl | 19104ead72 | 0.303 | 0.308 | 7,225 | 7,225 | 0.429 | 0.896 | 0.121 | 0.269 | 0.205 | 0.582 |  |
| this clone: db.jsonl | 4bb0870716 | 0.258 | 0.250 | 7,226 | 7,226 | 0.419 | 0.445 | 0.109 | 0.245 | 0.229 | 0.532 |  |
| this clone: db.jsonl | 4446c9069e | 0.250 | 0.239 | 7,274 | 7,274 | 0.393 | 0.546 | 0.107 | 0.228 | 0.186 | 0.511 |  |
| this clone: db.jsonl | 343d881df1 | 0.243 | 0.242 | 7,708 | 7,708 | 0.350 | 0.540 | 0.102 | 0.209 | 0.209 | 0.565 |  |
| archived-20261005-235645: db.jsonl | 2816900bac | 0.655 | 0.638 | 6,941 | 6,941 | 0.617 | 0.803 | 0.493 | 0.571 | 0.865 | 0.832 |  |
| archived-20261005-235645: db.jsonl | 46fbc9e912 | 0.545 | 0.491 | 6,966 | 6,966 | 0.513 | 0.979 | 0.246 | 0.403 | 0.966 | 0.811 |  |
| archived-20261005-235645: db.jsonl | c2d99350f1 | 0.517 | 0.481 | 6,974 | 6,974 | 0.515 | 0.952 | 0.232 | 0.384 | 0.845 | 0.887 |  |
| archived-20261005-235645: db.jsonl | 0f90ffc36a | 0.530 | 0.474 | 6,998 | 6,998 | 0.554 | 0.954 | 0.248 | 0.407 | 0.782 | 0.814 |  |
| archived-20261005-235645: db.jsonl | 988d608671 | 0.507 | 0.478 | 7,014 | 7,014 | 0.508 | 0.977 | 0.234 | 0.391 | 0.742 | 0.778 |  |
| archived-20261005-235645: db.jsonl | 20b3bde0c3 | 0.384 | 0.385 | 7,097 | 7,097 | 0.510 | 0.916 | 0.252 | 0.388 | 0.182 | 0.685 |  |
| archived-20261005-235645: db.jsonl | 35135bde2f | 0.372 | 0.371 | 7,105 | 7,105 | 0.480 | 0.806 | 0.241 | 0.365 | 0.210 | 0.644 |  |
| archived-20261005-235645: db.jsonl | 9a482dbeaf | 0.359 | 0.351 | 7,334 | 7,334 | 0.463 | 0.933 | 0.217 | 0.350 | 0.183 | 0.590 |  |
| archived-20261005-235645: db.jsonl | 040e367ce9 | 0.351 | 0.343 | 7,753 | 7,753 | 0.473 | 0.841 | 0.229 | 0.344 | 0.171 | 0.592 |  |
| archived-20261005-235645: db.jsonl | 1918ae250d | 0.347 | 0.346 | 7,820 | 7,820 | 0.498 | 0.682 | 0.225 | 0.377 | 0.176 | 0.541 |  |
| archived-20261005-235645: db.jsonl | 9102e1dea9 | 0.327 | 0.316 | 7,958 | 7,958 | 0.450 | 0.629 | 0.218 | 0.350 | 0.175 | 0.523 |  |
| archived-20261005-235645: db.jsonl | c9f3c95232 | 0.326 | 0.330 | 7,966 | 7,966 | 0.484 | 0.507 | 0.233 | 0.365 | 0.177 | 0.483 |  |
| archived-20261005-235645: db.jsonl | dcbaf0e29f | 0.322 | 0.329 | 9,014 | 9,014 | 0.456 | 0.606 | 0.217 | 0.336 | 0.172 | 0.541 |  |
| archived-20261006-012857: db.jsonl | 5347899701 | 0.448 | 0.431 | 6,903 | 6,903 | 0.406 | 0.991 | 0.181 | 0.318 | 0.779 | 0.801 |  |
| archived-20261006-012857: db.jsonl | 097ff5bdce | 0.443 | 0.406 | 6,913 | 6,913 | 0.426 | 0.856 | 0.187 | 0.328 | 0.765 | 0.836 |  |
| archived-20261006-012857: db.jsonl | 520f651e31 | 0.441 | 0.406 | 6,914 | 6,914 | 0.430 | 0.947 | 0.183 | 0.320 | 0.700 | 0.758 |  |
| archived-20261006-012857: db.jsonl | e973e9ada8 | 0.420 | 0.405 | 6,940 | 6,940 | 0.395 | 0.875 | 0.175 | 0.329 | 0.661 | 0.747 |  |
| archived-20261006-012857: db.jsonl | 403bda0b3f | 0.338 | 0.315 | 7,017 | 7,017 | 0.407 | 1.006 | 0.178 | 0.313 | 0.193 | 0.586 |  |
| archived-20261006-012857: db.jsonl | ccf0eb9891 | 0.330 | 0.324 | 7,068 | 7,068 | 0.411 | 0.868 | 0.182 | 0.319 | 0.189 | 0.628 |  |
| archived-20261006-012857: db.jsonl | 1a5dc48b9c | 0.314 | 0.308 | 7,092 | 7,092 | 0.343 | 0.835 | 0.170 | 0.294 | 0.213 | 0.534 |  |
| archived-20261006-012857: db.jsonl | bdb87d827e | 0.303 | 0.304 | 7,124 | 7,124 | 0.377 | 0.749 | 0.156 | 0.301 | 0.193 | 0.589 |  |
| archived-20261006-012857: db.jsonl | ed927db5ce | 0.308 | 0.304 | 7,132 | 7,132 | 0.385 | 0.816 | 0.162 | 0.283 | 0.192 | 0.583 |  |
| archived-20261006-012857: db.jsonl | 76684cada6 | 0.319 | 0.303 | 7,166 | 7,166 | 0.389 | 0.996 | 0.163 | 0.285 | 0.182 | 0.541 |  |
| archived-20261006-012857: db.jsonl | 103cbedc80 | 0.301 | 0.290 | 7,238 | 7,238 | 0.391 | 0.793 | 0.164 | 0.278 | 0.174 | 0.546 |  |
| archived-20261006-012857: db.jsonl | 9c85c7d9f5 | 0.305 | 0.280 | 7,246 | 7,246 | 0.382 | 0.884 | 0.166 | 0.271 | 0.173 | 0.566 |  |
| archived-20261006-012857: db.jsonl | 3218bf9f21 | 0.305 | 0.287 | 7,666 | 7,666 | 0.375 | 0.805 | 0.170 | 0.275 | 0.188 | 0.583 |  |
| archived-20261006-012857: db.jsonl | cd8075731e | 0.295 | 0.278 | 7,773 | 7,773 | 0.397 | 0.617 | 0.152 | 0.311 | 0.192 | 0.493 |  |
| archived-20261006-012857: db.jsonl | ad62971982 | 0.295 | 0.268 | 7,799 | 7,799 | 0.377 | 0.725 | 0.159 | 0.292 | 0.176 | 0.481 |  |
| archived-20261006-012857: db.jsonl | db3dcdb1f8 | 0.285 | 0.272 | 10,181 | 10,181 | 0.374 | 0.635 | 0.158 | 0.288 | 0.175 | 0.550 |  |
| archived-20261006-024824: db.jsonl | 7f7d8e7864 | 0.453 | 0.435 | 6,903 | 6,903 | 0.424 | 0.985 | 0.181 | 0.310 | 0.817 | 0.803 |  |
| archived-20261006-024824: db.jsonl | b7b4dd1166 | 0.453 | 0.422 | 6,911 | 6,911 | 0.415 | 0.915 | 0.186 | 0.326 | 0.825 | 0.836 |  |
| archived-20261006-024824: db.jsonl | 3280937f3d | 0.419 | 0.416 | 6,928 | 6,928 | 0.426 | 0.758 | 0.181 | 0.330 | 0.670 | 0.775 |  |
| archived-20261006-024824: db.jsonl | 3c84b53247 | 0.375 | 0.377 | 6,939 | 6,939 | 0.310 | 0.898 | 0.114 | 0.235 | 0.983 | 0.820 |  |
| archived-20261006-024824: db.jsonl | 9a9d2cb947 | 0.347 | 0.357 | 6,947 | 6,947 | 0.354 | 0.650 | 0.110 | 0.263 | 0.758 | 0.737 |  |
| archived-20261006-024824: db.jsonl | 5e7eed1cba | 0.378 | 0.333 | 6,951 | 6,951 | 0.374 | 0.964 | 0.116 | 0.261 | 0.704 | 0.800 |  |
| archived-20261006-024824: db.jsonl | 7033c6f1ab | 0.330 | 0.323 | 7,017 | 7,017 | 0.416 | 0.945 | 0.183 | 0.312 | 0.176 | 0.581 |  |
| archived-20261006-024824: db.jsonl | 828c84dd15 | 0.314 | 0.317 | 7,026 | 7,026 | 0.420 | 0.726 | 0.181 | 0.306 | 0.182 | 0.578 |  |
| archived-20261006-024824: db.jsonl | 262f6959cc | 0.265 | 0.259 | 7,057 | 7,057 | 0.361 | 0.678 | 0.116 | 0.263 | 0.174 | 0.530 |  |
| archived-20261006-024824: db.jsonl | 03fcb0e3e6 | 0.255 | 0.263 | 7,089 | 7,089 | 0.357 | 0.675 | 0.112 | 0.241 | 0.167 | 0.521 |  |
| archived-20261006-024824: db.jsonl | 285b6909d1 | 0.240 | 0.248 | 7,172 | 7,172 | 0.343 | 0.619 | 0.097 | 0.212 | 0.183 | 0.541 | yes |
| archived-20261006-024824: db.jsonl | 453a46a8e6 | 0.264 | 0.254 | 7,188 | 7,188 | 0.336 | 0.911 | 0.096 | 0.232 | 0.189 | 0.549 |  |
| archived-20261006-024824: db.jsonl | 3995ab7bde | 0.263 | 0.243 | 7,286 | 7,286 | 0.337 | 0.968 | 0.101 | 0.228 | 0.168 | 0.554 |  |
| archived-20261006-024824: db.jsonl | 364a0f4617 | 0.252 | 0.249 | 7,689 | 7,689 | 0.335 | 0.684 | 0.099 | 0.214 | 0.211 | 0.563 |  |
| archived-20261006-024824: db.jsonl | 419cce1726 | 0.241 | 0.238 | 8,320 | 8,320 | 0.337 | 0.616 | 0.099 | 0.230 | 0.173 | 0.505 |  |
| archived-20261006-131903: db.jsonl | 58c0a33fbe | 0.451 | 0.417 | 6,654 | 6,654 | 0.408 | 0.947 | 0.170 | 0.309 | 0.916 | 0.839 | yes |
| archived-20261006-131903: db.jsonl | 29b1a365dc | 0.420 | 0.415 | 6,655 | 6,655 | 0.400 | 0.775 | 0.181 | 0.318 | 0.732 | 0.779 | yes |
| archived-20261006-131903: db.jsonl | eabd014b0c | 0.421 | 0.402 | 6,673 | 6,673 | 0.410 | 0.839 | 0.183 | 0.304 | 0.693 | 0.742 |  |
| archived-20261006-131903: db.jsonl | 0df4c46cec | 0.404 | 0.412 | 6,680 | 6,680 | 0.394 | 0.822 | 0.176 | 0.312 | 0.606 | 0.745 | yes |
| archived-20261006-131903: db.jsonl | 1d44bcb8a5 | 0.366 | 0.358 | 6,693 | 6,693 | 0.350 | 0.803 | 0.113 | 0.233 | 0.895 | 0.851 | yes |
| archived-20261006-131903: db.jsonl | 9c2db9aebe | 0.371 | 0.353 | 6,699 | 6,699 | 0.367 | 0.826 | 0.120 | 0.243 | 0.789 | 0.791 |  |
| archived-20261006-131903: db.jsonl | f1c82fbd44 | 0.344 | 0.336 | 6,700 | 6,700 | 0.306 | 0.684 | 0.109 | 0.227 | 0.936 | 0.761 | yes |
| archived-20261006-131903: db.jsonl | 9f9bfa4f49 | 0.343 | 0.334 | 6,711 | 6,711 | 0.297 | 0.798 | 0.109 | 0.225 | 0.816 | 0.734 | yes |
| archived-20261006-131903: db.jsonl | eb0033be3d | 0.342 | 0.331 | 6,759 | 6,759 | 0.299 | 0.802 | 0.108 | 0.221 | 0.815 | 0.723 | yes |
| archived-20261006-131903: db.jsonl | ce2e13ce87 | 0.332 | 0.311 | 6,777 | 6,777 | 0.424 | 1.005 | 0.188 | 0.301 | 0.167 | 0.567 | yes |
| archived-20261006-131903: db.jsonl | d1b2f540a8 | 0.262 | 0.243 | 6,817 | 6,817 | 0.340 | 0.902 | 0.106 | 0.235 | 0.163 | 0.565 | yes |
| archived-20261006-131903: db.jsonl | cbbc5291f8 | 0.263 | 0.246 | 6,940 | 6,940 | 0.336 | 1.022 | 0.100 | 0.205 | 0.179 | 0.593 |  |
| archived-20261006-131903: db.jsonl | 773f6d9daf | 0.242 | 0.239 | 6,993 | 6,993 | 0.326 | 0.709 | 0.094 | 0.218 | 0.175 | 0.529 | yes |
| archived-20261006-131903: db.jsonl | 8298ca5d59 | 0.236 | 0.236 | 7,310 | 7,310 | 0.323 | 0.599 | 0.095 | 0.232 | 0.170 | 0.526 | yes |
| archived-20261006-131903: db.jsonl | 3a96a12236 | 0.233 | 0.225 | 7,958 | 7,958 | 0.334 | 0.554 | 0.096 | 0.222 | 0.172 | 0.520 | yes |

The front of all runs together, by size: 3a96a12236 0.233 at 7,958, 8298ca5d59 0.236 at 7,310, 285b6909d1 0.240 at 7,172, 773f6d9daf 0.242 at 6,993, d1b2f540a8 0.262 at 6,817, ce2e13ce87 0.332 at 6,777, eb0033be3d 0.342 at 6,759, 9f9bfa4f49 0.343 at 6,711, f1c82fbd44 0.344 at 6,700, 1d44bcb8a5 0.366 at 6,693, 0df4c46cec 0.404 at 6,680, 29b1a365dc 0.420 at 6,655, 58c0a33fbe 0.451 at 6,654

## The same session on two CPUs

Calibration on cpu 2: 1.001; on cpu 8: 1.005.

Speed on cpu 2 over speed on cpu 8, per design: median 1.009, 10-90% 0.994-1.031, extremes 0.979-1.045; rank agreement (Spearman) 0.99.

The front of all runs on cpu 2: 3a96a12236 0.233 at 7,958, 8298ca5d59 0.236 at 7,310, 285b6909d1 0.240 at 7,172, 773f6d9daf 0.242 at 6,993, d1b2f540a8 0.262 at 6,817, ce2e13ce87 0.332 at 6,777, eb0033be3d 0.342 at 6,759, 9f9bfa4f49 0.343 at 6,711, f1c82fbd44 0.344 at 6,700, 1d44bcb8a5 0.366 at 6,693, 0df4c46cec 0.404 at 6,680, 29b1a365dc 0.420 at 6,655, 58c0a33fbe 0.451 at 6,654

The front of all runs on cpu 8: 8298ca5d59 0.229 at 7,310, 773f6d9daf 0.239 at 6,993, d1b2f540a8 0.264 at 6,817, ce2e13ce87 0.326 at 6,777, f1c82fbd44 0.336 at 6,700, 1d44bcb8a5 0.365 at 6,693, 0df4c46cec 0.404 at 6,680, eabd014b0c 0.416 at 6,673, 29b1a365dc 0.419 at 6,655, 58c0a33fbe 0.445 at 6,654

On both fronts: 9 of 13 and 10.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| 3a96a12236 | 0.233 | 0.231 | 1.007 |
| 8298ca5d59 | 0.236 | 0.229 | 1.028 |
| 285b6909d1 | 0.240 | 0.239 | 1.002 |
| 419cce1726 | 0.241 | 0.237 | 1.016 |
| 773f6d9daf | 0.242 | 0.239 | 1.013 |
| 343d881df1 | 0.243 | 0.243 | 0.998 |
| 4446c9069e | 0.250 | 0.246 | 1.015 |
| 364a0f4617 | 0.252 | 0.249 | 1.015 |
| 03fcb0e3e6 | 0.255 | 0.260 | 0.984 |
| 4bb0870716 | 0.258 | 0.255 | 1.009 |
| d1b2f540a8 | 0.262 | 0.264 | 0.994 |
| cbbc5291f8 | 0.263 | 0.265 | 0.995 |
| 3995ab7bde | 0.263 | 0.255 | 1.033 |
| 453a46a8e6 | 0.264 | 0.257 | 1.028 |
| 262f6959cc | 0.265 | 0.257 | 1.029 |
| db3dcdb1f8 | 0.285 | 0.279 | 1.021 |
| cd8075731e | 0.295 | 0.286 | 1.031 |
| ad62971982 | 0.295 | 0.288 | 1.024 |
| 103cbedc80 | 0.301 | 0.303 | 0.991 |
| bdb87d827e | 0.303 | 0.291 | 1.040 |
| 19104ead72 | 0.303 | 0.302 | 1.003 |
| 9c85c7d9f5 | 0.305 | 0.297 | 1.027 |
| 3218bf9f21 | 0.305 | 0.300 | 1.018 |
| ed927db5ce | 0.308 | 0.309 | 0.998 |
| 1a5dc48b9c | 0.314 | 0.303 | 1.039 |
| 828c84dd15 | 0.314 | 0.314 | 1.000 |
| 76684cada6 | 0.319 | 0.316 | 1.009 |
| dcbaf0e29f | 0.322 | 0.325 | 0.992 |
| c9f3c95232 | 0.326 | 0.326 | 1.000 |
| 9102e1dea9 | 0.327 | 0.331 | 0.988 |
| 7c49a5ffca | 0.330 | 0.328 | 1.005 |
| ccf0eb9891 | 0.330 | 0.325 | 1.016 |
| 7033c6f1ab | 0.330 | 0.334 | 0.988 |
| 323f2ccfb8 | 0.330 | 0.338 | 0.979 |
| ce2e13ce87 | 0.332 | 0.326 | 1.018 |
| bfa7370096 | 0.338 | 0.327 | 1.034 |
| 403bda0b3f | 0.338 | 0.333 | 1.014 |
| df2ac6c7ab | 0.339 | 0.337 | 1.005 |
| eb0033be3d | 0.342 | 0.339 | 1.008 |
| 9f9bfa4f49 | 0.343 | 0.339 | 1.012 |
| f1c82fbd44 | 0.344 | 0.336 | 1.026 |
| 2b5e92dd57 | 0.346 | 0.331 | 1.045 |
| 1918ae250d | 0.347 | 0.344 | 1.010 |
| 9a9d2cb947 | 0.347 | 0.343 | 1.013 |
| 040e367ce9 | 0.351 | 0.351 | 1.002 |
| 9a482dbeaf | 0.359 | 0.361 | 0.995 |
| 69270766bd | 0.363 | 0.367 | 0.989 |
| 1d44bcb8a5 | 0.366 | 0.365 | 1.004 |
| 9c2db9aebe | 0.371 | 0.367 | 1.009 |
| 35135bde2f | 0.372 | 0.372 | 1.001 |
| 3c84b53247 | 0.375 | 0.374 | 1.001 |
| 5e7eed1cba | 0.378 | 0.372 | 1.015 |
| 20b3bde0c3 | 0.384 | 0.386 | 0.994 |
| 0df4c46cec | 0.404 | 0.404 | 1.001 |
| 3280937f3d | 0.419 | 0.410 | 1.021 |
| e973e9ada8 | 0.420 | 0.410 | 1.026 |
| 29b1a365dc | 0.420 | 0.419 | 1.002 |
| eabd014b0c | 0.421 | 0.416 | 1.012 |
| 0826d64cd9 | 0.424 | 0.408 | 1.040 |
| 520f651e31 | 0.441 | 0.443 | 0.995 |
| 097ff5bdce | 0.443 | 0.444 | 0.998 |
| 5347899701 | 0.448 | 0.449 | 0.998 |
| 58c0a33fbe | 0.451 | 0.445 | 1.013 |
| b7b4dd1166 | 0.453 | 0.451 | 1.004 |
| 7f7d8e7864 | 0.453 | 0.448 | 1.013 |
| 988d608671 | 0.507 | 0.509 | 0.997 |
| c2d99350f1 | 0.517 | 0.516 | 1.001 |
| 0f90ffc36a | 0.530 | 0.514 | 1.031 |
| 46fbc9e912 | 0.545 | 0.533 | 1.023 |
| 2816900bac | 0.655 | 0.644 | 1.017 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 15 - Iteration 76: seed 17 (the tag, the last run under the old rules) and the newest four

`seed 17 tag2 then experiment compare-fronts.py --rounds 10 --cpus 2,8`,
commit 248cb518: seeds 13-17, 72 front designs. **Calibration 0.993**
(0.979-1.019). The CPUs: median 1.003, 10-90% 0.988-1.019, ranks 0.99; 10 of
15 and 11 on both fronts.

**The front of all runs: 15 designs - seed 15's twelve, seed 14's one,
and the first two in the tag, seed 17's a36dc45e12 (0.233 at 7,283) and
5671742b27 (0.233 at 7,690).**

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 0.993** (kernel 0.983, fib 0.990, parse 0.979, corpus 0.993, loop 1.019, sieve 1.005).

| run | design | speed now | recorded | size now | recorded | engine KB | peak RSS MB | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 3d312e796e | 0.413 | 0.419 | 7,009 | 7,009 | 14.5 | 1.2 | 0.433 | 0.552 | 0.176 | 0.312 | 0.916 | 0.766 |  |
| this clone: db.jsonl | a1ff4b8022 | 0.387 | 0.388 | 7,043 | 7,043 | 16.1 | 1.2 | 0.394 | 0.799 | 0.117 | 0.240 | 0.984 | 0.845 |  |
| this clone: db.jsonl | 3405116655 | 0.347 | 0.353 | 7,049 | 7,049 | 16.8 | 1.2 | 0.385 | 0.491 | 0.111 | 0.261 | 0.917 | 0.770 |  |
| this clone: db.jsonl | 4ba5b2c147 | 0.337 | 0.338 | 7,057 | 7,057 | 16.6 | 1.2 | 0.403 | 0.438 | 0.111 | 0.259 | 0.864 | 0.776 |  |
| this clone: db.jsonl | 0c5782b28a | 0.341 | 0.343 | 7,073 | 7,073 | 16.6 | 1.2 | 0.406 | 0.451 | 0.112 | 0.249 | 0.912 | 0.797 |  |
| this clone: db.jsonl | 31e4e22b2e | 0.338 | 0.343 | 7,085 | 7,085 | 16.2 | 1.2 | 0.370 | 0.554 | 0.102 | 0.227 | 0.938 | 0.746 |  |
| this clone: db.jsonl | a1578b537c | 0.335 | 0.334 | 7,120 | 7,120 | 17.1 | 1.2 | 0.346 | 0.574 | 0.101 | 0.228 | 0.925 | 0.774 |  |
| this clone: db.jsonl | e6a3c1fb8c | 0.314 | 0.318 | 7,130 | 7,130 | 17.3 | 1.2 | 0.342 | 0.439 | 0.099 | 0.232 | 0.892 | 0.766 |  |
| this clone: db.jsonl | ce3a84b4a0 | 0.298 | 0.307 | 7,217 | 7,217 | 16.2 | 1.2 | 0.404 | 0.732 | 0.114 | 0.242 | 0.288 | 0.585 |  |
| this clone: db.jsonl | 6583b9f742 | 0.269 | 0.277 | 7,218 | 7,218 | 16.7 | 1.3 | 0.387 | 0.564 | 0.109 | 0.239 | 0.246 | 0.547 |  |
| this clone: db.jsonl | 2b7e66e1f3 | 0.258 | 0.260 | 7,226 | 7,226 | 17.1 | 1.2 | 0.420 | 0.448 | 0.111 | 0.232 | 0.236 | 0.540 |  |
| this clone: db.jsonl | 38de166d54 | 0.264 | 0.267 | 7,234 | 7,234 | 17.1 | 1.2 | 0.401 | 0.528 | 0.110 | 0.237 | 0.235 | 0.526 |  |
| this clone: db.jsonl | 2b55d23a18 | 0.249 | 0.251 | 7,266 | 7,266 | 45.2 | 1.2 | 0.359 | 0.580 | 0.108 | 0.230 | 0.186 | 0.473 |  |
| this clone: db.jsonl | a36dc45e12 | 0.233 | 0.235 | 7,283 | 7,283 | 17.3 | 1.2 | 0.362 | 0.431 | 0.099 | 0.228 | 0.195 | 0.574 | yes |
| this clone: db.jsonl | 5671742b27 | 0.233 | 0.234 | 7,690 | 7,690 | 17.2 | 1.2 | 0.341 | 0.440 | 0.102 | 0.224 | 0.198 | 0.550 | yes |
| archived-20261006-012857: db.jsonl | 5347899701 | 0.454 | 0.431 | 6,903 | 6,903 | 37.2 | 1.2 | 0.426 | 0.945 | 0.181 | 0.328 | 0.802 | 0.810 |  |
| archived-20261006-012857: db.jsonl | 097ff5bdce | 0.440 | 0.406 | 6,913 | 6,913 | 32.0 | 1.3 | 0.414 | 0.841 | 0.183 | 0.338 | 0.765 | 0.837 |  |
| archived-20261006-012857: db.jsonl | 520f651e31 | 0.442 | 0.406 | 6,914 | 6,914 | 35.1 | 1.2 | 0.421 | 0.956 | 0.183 | 0.320 | 0.717 | 0.783 |  |
| archived-20261006-012857: db.jsonl | e973e9ada8 | 0.419 | 0.405 | 6,940 | 6,940 | 36.0 | 1.3 | 0.400 | 0.853 | 0.173 | 0.319 | 0.686 | 0.740 |  |
| archived-20261006-012857: db.jsonl | 403bda0b3f | 0.336 | 0.315 | 7,017 | 7,017 | 35.7 | 1.2 | 0.409 | 1.034 | 0.173 | 0.315 | 0.186 | 0.574 |  |
| archived-20261006-012857: db.jsonl | ccf0eb9891 | 0.333 | 0.324 | 7,068 | 7,068 | 35.7 | 1.3 | 0.412 | 0.868 | 0.180 | 0.327 | 0.194 | 0.600 |  |
| archived-20261006-012857: db.jsonl | 1a5dc48b9c | 0.312 | 0.308 | 7,092 | 7,092 | 17.2 | 1.2 | 0.359 | 0.821 | 0.172 | 0.289 | 0.203 | 0.523 |  |
| archived-20261006-012857: db.jsonl | bdb87d827e | 0.295 | 0.304 | 7,124 | 7,124 | 35.4 | 1.3 | 0.377 | 0.774 | 0.155 | 0.277 | 0.179 | 0.554 |  |
| archived-20261006-012857: db.jsonl | ed927db5ce | 0.312 | 0.304 | 7,132 | 7,132 | 35.5 | 1.2 | 0.389 | 0.836 | 0.158 | 0.296 | 0.195 | 0.595 |  |
| archived-20261006-012857: db.jsonl | 76684cada6 | 0.320 | 0.303 | 7,166 | 7,166 | 34.3 | 1.3 | 0.377 | 1.058 | 0.165 | 0.291 | 0.174 | 0.548 |  |
| archived-20261006-012857: db.jsonl | 103cbedc80 | 0.296 | 0.290 | 7,238 | 7,238 | 36.8 | 1.2 | 0.381 | 0.775 | 0.160 | 0.272 | 0.178 | 0.544 |  |
| archived-20261006-012857: db.jsonl | 9c85c7d9f5 | 0.309 | 0.280 | 7,246 | 7,246 | 36.6 | 1.2 | 0.362 | 0.919 | 0.168 | 0.286 | 0.178 | 0.569 |  |
| archived-20261006-012857: db.jsonl | 3218bf9f21 | 0.299 | 0.287 | 7,666 | 7,666 | 35.3 | 1.2 | 0.380 | 0.761 | 0.167 | 0.281 | 0.176 | 0.583 |  |
| archived-20261006-012857: db.jsonl | cd8075731e | 0.288 | 0.278 | 7,773 | 7,773 | 34.3 | 1.2 | 0.386 | 0.628 | 0.155 | 0.297 | 0.177 | 0.481 |  |
| archived-20261006-012857: db.jsonl | ad62971982 | 0.288 | 0.268 | 7,799 | 7,799 | 35.5 | 1.2 | 0.378 | 0.680 | 0.158 | 0.281 | 0.173 | 0.464 |  |
| archived-20261006-012857: db.jsonl | db3dcdb1f8 | 0.277 | 0.272 | 10,181 | 10,181 | 37.9 | 1.2 | 0.382 | 0.628 | 0.154 | 0.267 | 0.166 | 0.541 |  |
| archived-20261006-024824: db.jsonl | 7f7d8e7864 | 0.466 | 0.435 | 6,903 | 6,903 | 37.2 | 1.2 | 0.421 | 1.012 | 0.190 | 0.335 | 0.810 | 0.816 |  |
| archived-20261006-024824: db.jsonl | b7b4dd1166 | 0.447 | 0.422 | 6,911 | 6,911 | 35.3 | 1.2 | 0.417 | 0.888 | 0.181 | 0.322 | 0.823 | 0.823 |  |
| archived-20261006-024824: db.jsonl | 3280937f3d | 0.417 | 0.416 | 6,928 | 6,928 | 35.8 | 1.2 | 0.426 | 0.764 | 0.175 | 0.329 | 0.671 | 0.767 |  |
| archived-20261006-024824: db.jsonl | 3c84b53247 | 0.377 | 0.377 | 6,939 | 6,939 | 19.3 | 1.2 | 0.310 | 0.892 | 0.114 | 0.245 | 0.981 | 0.820 |  |
| archived-20261006-024824: db.jsonl | 9a9d2cb947 | 0.345 | 0.357 | 6,947 | 6,947 | 39.9 | 1.3 | 0.353 | 0.643 | 0.110 | 0.261 | 0.747 | 0.728 |  |
| archived-20261006-024824: db.jsonl | 5e7eed1cba | 0.374 | 0.333 | 6,951 | 6,951 | 39.2 | 1.2 | 0.359 | 0.929 | 0.120 | 0.264 | 0.693 | 0.795 |  |
| archived-20261006-024824: db.jsonl | 7033c6f1ab | 0.333 | 0.323 | 7,017 | 7,017 | 35.3 | 1.2 | 0.416 | 0.910 | 0.185 | 0.317 | 0.184 | 0.606 |  |
| archived-20261006-024824: db.jsonl | 828c84dd15 | 0.318 | 0.317 | 7,026 | 7,026 | 35.4 | 1.3 | 0.412 | 0.725 | 0.184 | 0.315 | 0.188 | 0.579 |  |
| archived-20261006-024824: db.jsonl | 262f6959cc | 0.260 | 0.259 | 7,057 | 7,057 | 38.2 | 1.2 | 0.350 | 0.672 | 0.116 | 0.248 | 0.177 | 0.537 |  |
| archived-20261006-024824: db.jsonl | 03fcb0e3e6 | 0.261 | 0.263 | 7,089 | 7,089 | 38.2 | 1.3 | 0.347 | 0.650 | 0.113 | 0.263 | 0.181 | 0.517 |  |
| archived-20261006-024824: db.jsonl | 285b6909d1 | 0.244 | 0.248 | 7,172 | 7,172 | 39.6 | 1.2 | 0.326 | 0.609 | 0.095 | 0.231 | 0.197 | 0.538 | yes |
| archived-20261006-024824: db.jsonl | 453a46a8e6 | 0.260 | 0.254 | 7,188 | 7,188 | 39.1 | 1.3 | 0.337 | 0.917 | 0.096 | 0.232 | 0.172 | 0.562 |  |
| archived-20261006-024824: db.jsonl | 3995ab7bde | 0.262 | 0.243 | 7,286 | 7,286 | 42.0 | 1.2 | 0.327 | 1.003 | 0.099 | 0.217 | 0.178 | 0.528 |  |
| archived-20261006-024824: db.jsonl | 364a0f4617 | 0.250 | 0.249 | 7,689 | 7,689 | 39.6 | 1.2 | 0.325 | 0.674 | 0.099 | 0.215 | 0.210 | 0.572 |  |
| archived-20261006-024824: db.jsonl | 419cce1726 | 0.239 | 0.238 | 8,320 | 8,320 | 42.0 | 1.3 | 0.332 | 0.616 | 0.100 | 0.221 | 0.174 | 0.526 |  |
| archived-20261006-131903: db.jsonl | 58c0a33fbe | 0.451 | 0.417 | 6,654 | 6,654 | 37.2 | 1.2 | 0.410 | 0.916 | 0.175 | 0.310 | 0.918 | 0.835 | yes |
| archived-20261006-131903: db.jsonl | 29b1a365dc | 0.421 | 0.415 | 6,655 | 6,655 | 36.3 | 1.2 | 0.407 | 0.747 | 0.183 | 0.316 | 0.749 | 0.795 | yes |
| archived-20261006-131903: db.jsonl | eabd014b0c | 0.421 | 0.402 | 6,673 | 6,673 | 35.6 | 1.2 | 0.413 | 0.836 | 0.177 | 0.308 | 0.699 | 0.738 |  |
| archived-20261006-131903: db.jsonl | 0df4c46cec | 0.402 | 0.412 | 6,680 | 6,680 | 35.8 | 1.2 | 0.399 | 0.818 | 0.170 | 0.309 | 0.611 | 0.718 | yes |
| archived-20261006-131903: db.jsonl | 1d44bcb8a5 | 0.370 | 0.358 | 6,693 | 6,693 | 42.4 | 1.2 | 0.351 | 0.802 | 0.114 | 0.251 | 0.864 | 0.830 | yes |
| archived-20261006-131903: db.jsonl | 9c2db9aebe | 0.371 | 0.353 | 6,699 | 6,699 | 40.9 | 1.2 | 0.369 | 0.812 | 0.120 | 0.247 | 0.796 | 0.785 |  |
| archived-20261006-131903: db.jsonl | f1c82fbd44 | 0.347 | 0.336 | 6,700 | 6,700 | 17.4 | 1.2 | 0.306 | 0.727 | 0.102 | 0.228 | 0.965 | 0.737 | yes |
| archived-20261006-131903: db.jsonl | 9f9bfa4f49 | 0.343 | 0.334 | 6,711 | 6,711 | 18.8 | 1.2 | 0.301 | 0.821 | 0.108 | 0.216 | 0.829 | 0.737 | yes |
| archived-20261006-131903: db.jsonl | eb0033be3d | 0.339 | 0.331 | 6,759 | 6,759 | 18.8 | 1.2 | 0.283 | 0.797 | 0.110 | 0.224 | 0.805 | 0.750 | yes |
| archived-20261006-131903: db.jsonl | ce2e13ce87 | 0.334 | 0.311 | 6,777 | 6,777 | 35.4 | 1.3 | 0.412 | 1.000 | 0.186 | 0.315 | 0.171 | 0.572 | yes |
| archived-20261006-131903: db.jsonl | d1b2f540a8 | 0.262 | 0.243 | 6,817 | 6,817 | 39.1 | 1.2 | 0.328 | 0.918 | 0.108 | 0.231 | 0.163 | 0.566 | yes |
| archived-20261006-131903: db.jsonl | cbbc5291f8 | 0.257 | 0.246 | 6,940 | 6,940 | 38.6 | 1.2 | 0.331 | 1.009 | 0.100 | 0.205 | 0.166 | 0.580 | yes |
| archived-20261006-131903: db.jsonl | 773f6d9daf | 0.245 | 0.239 | 6,993 | 6,993 | 39.9 | 1.2 | 0.326 | 0.707 | 0.095 | 0.225 | 0.178 | 0.525 | yes |
| archived-20261006-131903: db.jsonl | 8298ca5d59 | 0.237 | 0.236 | 7,310 | 7,310 | 39.6 | 1.2 | 0.334 | 0.592 | 0.095 | 0.231 | 0.174 | 0.531 |  |
| archived-20261006-131903: db.jsonl | 3a96a12236 | 0.230 | 0.225 | 7,958 | 7,958 | 39.9 | 1.3 | 0.327 | 0.557 | 0.095 | 0.217 | 0.173 | 0.510 | yes |
| archived-20261006-160616: db.jsonl | 0826d64cd9 | 0.413 | 0.415 | 7,009 | 7,009 | 14.5 | 1.2 | 0.445 | 0.543 | 0.174 | 0.311 | 0.918 | 0.770 |  |
| archived-20261006-160616: db.jsonl | 69270766bd | 0.366 | 0.366 | 7,049 | 7,049 | 16.2 | 1.2 | 0.400 | 0.639 | 0.108 | 0.252 | 0.942 | 0.798 |  |
| archived-20261006-160616: db.jsonl | df2ac6c7ab | 0.334 | 0.336 | 7,050 | 7,050 | 17.1 | 1.2 | 0.407 | 0.457 | 0.105 | 0.243 | 0.872 | 0.775 |  |
| archived-20261006-160616: db.jsonl | 323f2ccfb8 | 0.334 | 0.337 | 7,105 | 7,105 | 17.1 | 1.2 | 0.333 | 0.630 | 0.099 | 0.231 | 0.874 | 0.727 |  |
| archived-20261006-160616: db.jsonl | 7c49a5ffca | 0.334 | 0.333 | 7,123 | 7,123 | 16.4 | 1.2 | 0.356 | 0.550 | 0.099 | 0.227 | 0.946 | 0.824 |  |
| archived-20261006-160616: db.jsonl | 2b5e92dd57 | 0.342 | 0.336 | 7,186 | 7,186 | 41.3 | 1.2 | 0.491 | 0.847 | 0.187 | 0.337 | 0.178 | 0.546 |  |
| archived-20261006-160616: db.jsonl | bfa7370096 | 0.334 | 0.339 | 7,202 | 7,202 | 45.3 | 1.2 | 0.373 | 0.610 | 0.099 | 0.230 | 0.803 | 0.757 |  |
| archived-20261006-160616: db.jsonl | 19104ead72 | 0.300 | 0.301 | 7,225 | 7,225 | 46.0 | 1.2 | 0.428 | 0.900 | 0.115 | 0.262 | 0.210 | 0.592 |  |
| archived-20261006-160616: db.jsonl | 4bb0870716 | 0.259 | 0.256 | 7,226 | 7,226 | 17.1 | 1.2 | 0.419 | 0.451 | 0.111 | 0.243 | 0.226 | 0.540 |  |
| archived-20261006-160616: db.jsonl | 4446c9069e | 0.248 | 0.251 | 7,274 | 7,274 | 16.2 | 1.2 | 0.377 | 0.529 | 0.106 | 0.229 | 0.193 | 0.482 |  |
| archived-20261006-160616: db.jsonl | 343d881df1 | 0.243 | 0.237 | 7,708 | 7,708 | 17.3 | 1.2 | 0.357 | 0.546 | 0.102 | 0.215 | 0.196 | 0.552 |  |

The front of all runs together, by size: 3a96a12236 0.230 at 7,958, 5671742b27 0.233 at 7,690, a36dc45e12 0.233 at 7,283, 285b6909d1 0.244 at 7,172, 773f6d9daf 0.245 at 6,993, cbbc5291f8 0.257 at 6,940, d1b2f540a8 0.262 at 6,817, ce2e13ce87 0.334 at 6,777, eb0033be3d 0.339 at 6,759, 9f9bfa4f49 0.343 at 6,711, f1c82fbd44 0.347 at 6,700, 1d44bcb8a5 0.370 at 6,693, 0df4c46cec 0.402 at 6,680, 29b1a365dc 0.421 at 6,655, 58c0a33fbe 0.451 at 6,654

## The same session on two CPUs

Calibration on cpu 2: 0.993; on cpu 8: 1.015.

Speed on cpu 2 over speed on cpu 8, per design: median 1.003, 10-90% 0.988-1.019, extremes 0.968-1.038; rank agreement (Spearman) 0.99.

The front of all runs on cpu 2: 3a96a12236 0.230 at 7,958, 5671742b27 0.233 at 7,690, a36dc45e12 0.233 at 7,283, 285b6909d1 0.244 at 7,172, 773f6d9daf 0.245 at 6,993, cbbc5291f8 0.257 at 6,940, d1b2f540a8 0.262 at 6,817, ce2e13ce87 0.334 at 6,777, eb0033be3d 0.339 at 6,759, 9f9bfa4f49 0.343 at 6,711, f1c82fbd44 0.347 at 6,700, 1d44bcb8a5 0.370 at 6,693, 0df4c46cec 0.402 at 6,680, 29b1a365dc 0.421 at 6,655, 58c0a33fbe 0.451 at 6,654

The front of all runs on cpu 8: 8298ca5d59 0.230 at 7,310, a36dc45e12 0.231 at 7,283, 285b6909d1 0.239 at 7,172, 773f6d9daf 0.244 at 6,993, d1b2f540a8 0.263 at 6,817, ce2e13ce87 0.333 at 6,777, f1c82fbd44 0.334 at 6,700, 1d44bcb8a5 0.366 at 6,693, 0df4c46cec 0.404 at 6,680, 29b1a365dc 0.419 at 6,655, 58c0a33fbe 0.449 at 6,654

On both fronts: 10 of 15 and 11.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| 3a96a12236 | 0.230 | 0.231 | 0.998 |
| 5671742b27 | 0.233 | 0.231 | 1.006 |
| a36dc45e12 | 0.233 | 0.231 | 1.011 |
| 8298ca5d59 | 0.237 | 0.230 | 1.032 |
| 419cce1726 | 0.239 | 0.239 | 0.999 |
| 343d881df1 | 0.243 | 0.242 | 1.003 |
| 285b6909d1 | 0.244 | 0.239 | 1.019 |
| 773f6d9daf | 0.245 | 0.244 | 1.003 |
| 4446c9069e | 0.248 | 0.244 | 1.017 |
| 2b55d23a18 | 0.249 | 0.248 | 1.005 |
| 364a0f4617 | 0.250 | 0.254 | 0.986 |
| cbbc5291f8 | 0.257 | 0.266 | 0.968 |
| 2b7e66e1f3 | 0.258 | 0.257 | 1.003 |
| 4bb0870716 | 0.259 | 0.257 | 1.005 |
| 453a46a8e6 | 0.260 | 0.260 | 0.998 |
| 262f6959cc | 0.260 | 0.264 | 0.986 |
| 03fcb0e3e6 | 0.261 | 0.260 | 1.005 |
| d1b2f540a8 | 0.262 | 0.263 | 0.993 |
| 3995ab7bde | 0.262 | 0.262 | 1.004 |
| 38de166d54 | 0.264 | 0.260 | 1.015 |
| 6583b9f742 | 0.269 | 0.270 | 0.996 |
| db3dcdb1f8 | 0.277 | 0.284 | 0.975 |
| ad62971982 | 0.288 | 0.289 | 0.994 |
| cd8075731e | 0.288 | 0.291 | 0.988 |
| bdb87d827e | 0.295 | 0.297 | 0.995 |
| 103cbedc80 | 0.296 | 0.293 | 1.011 |
| ce3a84b4a0 | 0.298 | 0.297 | 1.003 |
| 3218bf9f21 | 0.299 | 0.301 | 0.993 |
| 19104ead72 | 0.300 | 0.304 | 0.988 |
| 9c85c7d9f5 | 0.309 | 0.298 | 1.038 |
| ed927db5ce | 0.312 | 0.313 | 0.998 |
| 1a5dc48b9c | 0.312 | 0.316 | 0.989 |
| e6a3c1fb8c | 0.314 | 0.304 | 1.033 |
| 828c84dd15 | 0.318 | 0.320 | 0.994 |
| 76684cada6 | 0.320 | 0.323 | 0.988 |
| 7033c6f1ab | 0.333 | 0.330 | 1.008 |
| ccf0eb9891 | 0.333 | 0.327 | 1.019 |
| ce2e13ce87 | 0.334 | 0.333 | 1.001 |
| 7c49a5ffca | 0.334 | 0.334 | 0.999 |
| bfa7370096 | 0.334 | 0.326 | 1.023 |
| df2ac6c7ab | 0.334 | 0.335 | 0.996 |
| 323f2ccfb8 | 0.334 | 0.330 | 1.014 |
| a1578b537c | 0.335 | 0.334 | 1.004 |
| 403bda0b3f | 0.336 | 0.332 | 1.011 |
| 4ba5b2c147 | 0.337 | 0.335 | 1.008 |
| 31e4e22b2e | 0.338 | 0.330 | 1.024 |
| eb0033be3d | 0.339 | 0.339 | 0.999 |
| 0c5782b28a | 0.341 | 0.335 | 1.018 |
| 2b5e92dd57 | 0.342 | 0.336 | 1.017 |
| 9f9bfa4f49 | 0.343 | 0.340 | 1.011 |
| 9a9d2cb947 | 0.345 | 0.344 | 1.001 |
| f1c82fbd44 | 0.347 | 0.334 | 1.037 |
| 3405116655 | 0.347 | 0.348 | 0.996 |
| 69270766bd | 0.366 | 0.368 | 0.995 |
| 1d44bcb8a5 | 0.370 | 0.366 | 1.010 |
| 9c2db9aebe | 0.371 | 0.369 | 1.006 |
| 5e7eed1cba | 0.374 | 0.375 | 0.998 |
| 3c84b53247 | 0.377 | 0.376 | 1.002 |
| a1ff4b8022 | 0.387 | 0.393 | 0.985 |
| 0df4c46cec | 0.402 | 0.404 | 0.994 |
| 0826d64cd9 | 0.413 | 0.415 | 0.995 |
| 3d312e796e | 0.413 | 0.412 | 1.001 |
| 3280937f3d | 0.417 | 0.409 | 1.018 |
| e973e9ada8 | 0.419 | 0.416 | 1.007 |
| 29b1a365dc | 0.421 | 0.419 | 1.005 |
| eabd014b0c | 0.421 | 0.419 | 1.005 |
| 097ff5bdce | 0.440 | 0.451 | 0.976 |
| 520f651e31 | 0.442 | 0.439 | 1.006 |
| b7b4dd1166 | 0.447 | 0.449 | 0.995 |
| 58c0a33fbe | 0.451 | 0.449 | 1.005 |
| 5347899701 | 0.454 | 0.453 | 1.002 |
| 7f7d8e7864 | 0.466 | 0.455 | 1.025 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 16 - Iteration 77: seed 18 (three objectives) and the newest four

`seed 18 tag2 then experiment compare-fronts.py --rounds 10 --cpus 2,8`,
commit 4df4076c: seeds 14-18 measured under the new objectives - every
engine without the C library, binary + image and memory beside speed;
114 designs. **Calibration 1.004.** The CPUs: median 1.002, 10-90%
0.992-1.027, ranks 1.00; 33 of 40 and 38 on both fronts.

**The front of all runs: 39-40 designs, 35 of them seed 18's - and 18-19
there by memory alone**, each a page or less from a design faster and
smaller. With 8 KB of tolerance (Iteration 77) the front is the 21 of the
speed-and-size front: 19 of seed 18, seed 15's 3a96a12236 and seed 14's
419cce1726.

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 1.004** (kernel 1.008, fib 0.998, parse 1.000, corpus 1.006, loop 1.006, sieve 1.034).

| run | design | speed now | recorded | size now | recorded | binary | binary + image | memory KB | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 4996bc41b8 | 0.568 | 0.586 | 7,051 | 7,051 | 25,280 | 32,331 | 208.0 | 0.562 | 1.214 | 0.224 | 0.321 | 1.203 | 1.071 | yes |
| this clone: db.jsonl | 844716c23e | 0.587 | 0.589 | 7,051 | 7,051 | 25,280 | 32,331 | 208.0 | 0.567 | 1.213 | 0.228 | 0.373 | 1.190 | 1.074 |  |
| this clone: db.jsonl | 776c86e476 | 0.577 | 0.574 | 7,059 | 7,059 | 25,280 | 32,339 | 208.0 | 0.572 | 1.131 | 0.223 | 0.372 | 1.192 | 1.054 |  |
| this clone: db.jsonl | 5c495fe0f3 | 0.569 | 0.568 | 7,090 | 7,090 | 25,280 | 32,370 | 212.0 | 0.552 | 1.161 | 0.224 | 0.360 | 1.150 | 1.025 |  |
| this clone: db.jsonl | f27cc3ce5a | 0.558 | 0.559 | 7,108 | 7,108 | 25,280 | 32,388 | 212.0 | 0.536 | 1.113 | 0.221 | 0.350 | 1.168 | 1.014 | yes |
| this clone: db.jsonl | 51a8931db2 | 0.388 | 0.385 | 7,115 | 7,115 | 29,352 | 36,467 | 212.0 | 0.380 | 0.786 | 0.111 | 0.242 | 1.096 | 0.946 | yes |
| this clone: db.jsonl | 4542a08fb0 | 0.465 | 0.466 | 7,194 | 7,194 | 25,280 | 32,474 | 212.0 | 0.583 | 1.095 | 0.230 | 0.375 | 0.393 | 0.726 | yes |
| this clone: db.jsonl | 8252421ca2 | 0.482 | 0.482 | 7,194 | 7,194 | 25,280 | 32,474 | 208.0 | 0.606 | 1.149 | 0.240 | 0.390 | 0.397 | 0.725 | yes |
| this clone: db.jsonl | 8a6365a3ff | 0.411 | 0.406 | 7,217 | 7,217 | 29,376 | 36,593 | 212.0 | 0.527 | 1.110 | 0.148 | 0.295 | 0.459 | 0.744 |  |
| this clone: db.jsonl | 2789713e31 | 0.400 | 0.398 | 7,242 | 7,242 | 29,376 | 36,618 | 208.0 | 0.514 | 1.089 | 0.154 | 0.299 | 0.397 | 0.750 | yes |
| this clone: db.jsonl | d26dfdeda4 | 0.466 | 0.461 | 7,250 | 7,250 | 25,280 | 32,530 | 208.0 | 0.574 | 1.145 | 0.232 | 0.365 | 0.395 | 0.733 | yes |
| this clone: db.jsonl | dac6ff750a | 0.394 | 0.392 | 7,258 | 7,258 | 29,376 | 36,634 | 210.0 | 0.524 | 1.011 | 0.156 | 0.297 | 0.388 | 0.715 | yes |
| this clone: db.jsonl | 2a2c2b4256 | 0.457 | 0.457 | 7,258 | 7,258 | 25,280 | 32,538 | 208.0 | 0.568 | 1.123 | 0.222 | 0.356 | 0.395 | 0.736 | yes |
| this clone: db.jsonl | e570f69332 | 0.440 | 0.434 | 7,274 | 7,274 | 25,280 | 32,554 | 216.0 | 0.509 | 1.124 | 0.220 | 0.331 | 0.394 | 0.717 | yes |
| this clone: db.jsonl | f48c2a5150 | 0.377 | 0.377 | 7,276 | 7,276 | 29,376 | 36,652 | 212.0 | 0.396 | 0.932 | 0.203 | 0.301 | 0.340 | 0.686 | yes |
| this clone: db.jsonl | a170190b5a | 0.395 | 0.386 | 7,298 | 7,298 | 29,376 | 36,674 | 208.0 | 0.520 | 1.170 | 0.145 | 0.287 | 0.377 | 0.729 | yes |
| this clone: db.jsonl | 2117a45620 | 0.278 | 0.274 | 7,307 | 7,307 | 33,448 | 40,755 | 216.0 | 0.422 | 0.494 | 0.116 | 0.256 | 0.271 | 0.533 |  |
| this clone: db.jsonl | 4e3a904b8e | 0.255 | 0.255 | 7,323 | 7,323 | 62,128 | 69,451 | 232.0 | 0.379 | 0.591 | 0.105 | 0.238 | 0.193 | 0.510 |  |
| this clone: db.jsonl | 69842b04ad | 0.274 | 0.268 | 7,323 | 7,323 | 33,448 | 40,771 | 216.0 | 0.386 | 0.694 | 0.105 | 0.239 | 0.230 | 0.588 | yes |
| this clone: db.jsonl | 609b436e3a | 0.450 | 0.450 | 7,329 | 7,329 | 25,280 | 32,609 | 212.0 | 0.563 | 1.067 | 0.221 | 0.364 | 0.381 | 0.720 | yes |
| this clone: db.jsonl | 0f3d5dae58 | 0.361 | 0.352 | 7,331 | 7,331 | 29,376 | 36,707 | 216.0 | 0.467 | 0.959 | 0.131 | 0.259 | 0.404 | 0.727 | yes |
| this clone: db.jsonl | bbab8560dd | 0.258 | 0.261 | 7,338 | 7,338 | 33,448 | 40,786 | 216.0 | 0.383 | 0.550 | 0.097 | 0.228 | 0.246 | 0.535 | yes |
| this clone: db.jsonl | 1c4300cbbb | 0.284 | 0.285 | 7,338 | 7,338 | 33,448 | 40,786 | 216.0 | 0.412 | 0.668 | 0.103 | 0.235 | 0.275 | 0.613 |  |
| this clone: db.jsonl | c13c77dc7c | 0.288 | 0.286 | 7,339 | 7,339 | 33,472 | 40,811 | 208.0 | 0.395 | 0.658 | 0.110 | 0.234 | 0.293 | 0.625 | yes |
| this clone: db.jsonl | b0a896c3c3 | 0.359 | 0.358 | 7,347 | 7,347 | 29,376 | 36,723 | 216.0 | 0.454 | 1.037 | 0.128 | 0.262 | 0.381 | 0.730 | yes |
| this clone: db.jsonl | 416077aa2f | 0.277 | 0.272 | 7,349 | 7,349 | 33,448 | 40,797 | 212.0 | 0.381 | 0.743 | 0.110 | 0.229 | 0.228 | 0.578 | yes |
| this clone: db.jsonl | 0cf9f1e76a | 0.268 | 0.265 | 7,365 | 7,365 | 62,128 | 69,493 | 232.0 | 0.402 | 0.731 | 0.107 | 0.235 | 0.188 | 0.563 |  |
| this clone: db.jsonl | 740331292d | 0.467 | 0.467 | 7,505 | 7,505 | 25,280 | 32,785 | 208.0 | 0.584 | 1.111 | 0.225 | 0.367 | 0.413 | 0.755 |  |
| this clone: db.jsonl | 03cf426d67 | 0.451 | 0.448 | 7,539 | 7,539 | 25,280 | 32,819 | 208.0 | 0.522 | 1.207 | 0.224 | 0.340 | 0.388 | 0.750 | yes |
| this clone: db.jsonl | a03ef495f5 | 0.301 | 0.301 | 7,644 | 7,644 | 29,352 | 36,996 | 216.0 | 0.409 | 0.775 | 0.110 | 0.260 | 0.274 | 0.559 | yes |
| this clone: db.jsonl | 63e3305540 | 0.444 | 0.438 | 7,664 | 7,664 | 25,280 | 32,944 | 212.0 | 0.537 | 1.201 | 0.215 | 0.323 | 0.384 | 0.729 | yes |
| this clone: db.jsonl | 0039591d51 | 0.444 | 0.442 | 7,675 | 7,675 | 25,280 | 32,955 | 212.0 | 0.578 | 1.076 | 0.223 | 0.345 | 0.359 | 0.730 | yes |
| this clone: db.jsonl | b46a9c7ad4 | 0.447 | 0.447 | 7,677 | 7,677 | 25,280 | 32,957 | 208.0 | 0.569 | 1.045 | 0.221 | 0.348 | 0.390 | 0.752 | yes |
| this clone: db.jsonl | 301a268219 | 0.446 | 0.444 | 7,683 | 7,683 | 25,280 | 32,963 | 212.0 | 0.531 | 1.144 | 0.220 | 0.336 | 0.394 | 0.739 |  |
| this clone: db.jsonl | a808c92923 | 0.455 | 0.456 | 7,698 | 7,698 | 25,280 | 32,978 | 208.0 | 0.592 | 1.107 | 0.227 | 0.367 | 0.358 | 0.743 |  |
| this clone: db.jsonl | 7d7f1bf4fa | 0.297 | 0.291 | 7,707 | 7,707 | 29,352 | 37,059 | 212.0 | 0.393 | 0.782 | 0.112 | 0.235 | 0.283 | 0.607 | yes |
| this clone: db.jsonl | 064ee4f23a | 0.264 | 0.263 | 7,718 | 7,718 | 33,448 | 41,166 | 212.0 | 0.411 | 0.554 | 0.108 | 0.228 | 0.229 | 0.609 | yes |
| this clone: db.jsonl | ca2e692954 | 0.275 | 0.273 | 7,738 | 7,738 | 33,448 | 41,186 | 208.0 | 0.354 | 0.759 | 0.106 | 0.226 | 0.243 | 0.596 | yes |
| this clone: db.jsonl | 7075e8f2b1 | 0.277 | 0.278 | 7,738 | 7,738 | 33,448 | 41,186 | 208.0 | 0.377 | 0.685 | 0.110 | 0.225 | 0.256 | 0.572 |  |
| this clone: db.jsonl | 9f9c8fdb94 | 0.313 | 0.310 | 7,744 | 7,744 | 33,448 | 41,192 | 208.0 | 0.437 | 0.790 | 0.111 | 0.245 | 0.321 | 0.637 |  |
| this clone: db.jsonl | ccc8da3b12 | 0.300 | 0.300 | 7,759 | 7,759 | 33,448 | 41,207 | 208.0 | 0.407 | 0.555 | 0.106 | 0.249 | 0.407 | 0.681 |  |
| this clone: db.jsonl | e076a00103 | 0.277 | 0.274 | 7,783 | 7,783 | 29,352 | 37,135 | 216.0 | 0.394 | 0.632 | 0.112 | 0.234 | 0.254 | 0.613 | yes |
| this clone: db.jsonl | 2bdab2950f | 0.278 | 0.278 | 7,783 | 7,783 | 29,352 | 37,135 | 216.0 | 0.397 | 0.630 | 0.112 | 0.234 | 0.254 | 0.608 |  |
| this clone: db.jsonl | 7f07a469cb | 0.390 | 0.390 | 7,801 | 7,801 | 29,376 | 37,177 | 208.0 | 0.514 | 1.191 | 0.139 | 0.284 | 0.373 | 0.750 | yes |
| this clone: db.jsonl | 4daab7895a | 0.426 | 0.425 | 7,806 | 7,806 | 25,280 | 33,086 | 212.0 | 0.521 | 1.081 | 0.215 | 0.326 | 0.356 | 0.717 | yes |
| this clone: db.jsonl | 7125b151e4 | 0.277 | 0.273 | 7,970 | 7,970 | 33,448 | 41,418 | 212.0 | 0.399 | 0.603 | 0.105 | 0.246 | 0.264 | 0.584 |  |
| this clone: db.jsonl | 60c95fbea3 | 0.243 | 0.239 | 8,332 | 8,332 | 66,216 | 74,548 | 232.0 | 0.382 | 0.433 | 0.105 | 0.231 | 0.213 | 0.570 | yes |
| this clone: db.jsonl | 9517490eb3 | 0.256 | 0.258 | 8,350 | 8,350 | 33,448 | 41,798 | 212.0 | 0.380 | 0.600 | 0.108 | 0.234 | 0.193 | 0.609 | yes |
| this clone: db.jsonl | 0bab7fed3e | 0.254 | 0.252 | 8,357 | 8,357 | 33,448 | 41,805 | 212.0 | 0.377 | 0.600 | 0.108 | 0.233 | 0.187 | 0.592 | yes |
| this clone: db.jsonl | 436af85b80 | 0.252 | 0.249 | 8,401 | 8,401 | 33,448 | 41,849 | 216.0 | 0.394 | 0.514 | 0.109 | 0.246 | 0.186 | 0.495 | yes |
| this clone: db.jsonl | 44af4fb785 | 0.253 | 0.252 | 9,413 | 9,413 | 33,448 | 42,861 | 212.0 | 0.370 | 0.602 | 0.107 | 0.230 | 0.187 | 0.609 | yes |
| this clone: db.jsonl | 98d7746633 | 0.281 | 0.282 | 9,598 | 9,598 | 29,352 | 38,950 | 216.0 | 0.381 | 0.643 | 0.107 | 0.230 | 0.288 | 0.644 |  |
| this clone: db.jsonl | 76ab789fed | 0.264 | 0.264 | 9,606 | 9,606 | 29,352 | 38,958 | 220.0 | 0.367 | 0.590 | 0.106 | 0.221 | 0.253 | 0.615 | yes |
| this clone: db.jsonl | eef03e6a19 | 1.081 | 1.087 | 25,144 | 25,144 | 25,256 | 50,400 | 204.0 | 1.212 | 0.893 | 1.135 | 1.151 | 1.044 | 1.044 |  |
| this clone: db.jsonl | 35728dddcf | 1.085 | 1.080 | 25,144 | 25,144 | 25,280 | 50,424 | 204.0 | 1.202 | 0.970 | 1.121 | 1.154 | 0.996 | 1.068 |  |
| this clone: db.jsonl | 0350ea6ee2 | 1.195 | 1.182 | 25,144 | 25,144 | 21,184 | 46,328 | 204.0 | 1.317 | 1.012 | 1.248 | 1.271 | 1.152 | 1.118 |  |
| archived-20261006-024824: db.jsonl | 7f7d8e7864 | 0.476 | 0.435 | 6,903 | 6,903 | 58,024 | 64,927 | 208.0 | 0.429 | 0.942 | 0.198 | 0.340 | 0.898 | 0.872 |  |
| archived-20261006-024824: db.jsonl | b7b4dd1166 | 0.435 | 0.422 | 6,911 | 6,911 | 53,928 | 60,839 | 216.0 | 0.420 | 0.739 | 0.191 | 0.333 | 0.788 | 0.813 |  |
| archived-20261006-024824: db.jsonl | 097ff5bdce | 0.462 | 0.410 | 6,913 | 6,913 | 49,856 | 56,769 | 216.0 | 0.426 | 0.849 | 0.195 | 0.339 | 0.882 | 0.851 |  |
| archived-20261006-024824: db.jsonl | 520f651e31 | 0.470 | 0.411 | 6,914 | 6,914 | 53,928 | 60,842 | 216.0 | 0.418 | 0.967 | 0.187 | 0.328 | 0.928 | 0.850 |  |
| archived-20261006-024824: db.jsonl | 3280937f3d | 0.453 | 0.416 | 6,928 | 6,928 | 53,936 | 60,864 | 216.0 | 0.430 | 0.792 | 0.190 | 0.336 | 0.873 | 0.877 |  |
| archived-20261006-024824: db.jsonl | 3c84b53247 | 0.391 | 0.377 | 6,939 | 6,939 | 37,544 | 44,483 | 204.0 | 0.322 | 0.906 | 0.113 | 0.245 | 1.129 | 0.893 | yes |
| archived-20261006-024824: db.jsonl | 9a9d2cb947 | 0.394 | 0.357 | 6,947 | 6,947 | 58,024 | 64,971 | 216.0 | 0.375 | 0.886 | 0.123 | 0.274 | 0.844 | 0.831 |  |
| archived-20261006-024824: db.jsonl | 5e7eed1cba | 0.373 | 0.333 | 6,951 | 6,951 | 58,024 | 64,975 | 216.0 | 0.365 | 0.798 | 0.122 | 0.264 | 0.762 | 0.859 |  |
| archived-20261006-024824: db.jsonl | 7033c6f1ab | 0.330 | 0.323 | 7,017 | 7,017 | 53,928 | 60,945 | 216.0 | 0.424 | 0.744 | 0.188 | 0.321 | 0.205 | 0.615 |  |
| archived-20261006-024824: db.jsonl | 828c84dd15 | 0.369 | 0.317 | 7,026 | 7,026 | 53,928 | 60,954 | 216.0 | 0.429 | 0.956 | 0.193 | 0.330 | 0.263 | 0.650 |  |
| archived-20261006-024824: db.jsonl | 262f6959cc | 0.271 | 0.259 | 7,057 | 7,057 | 58,024 | 65,081 | 216.0 | 0.346 | 0.675 | 0.116 | 0.265 | 0.203 | 0.574 |  |
| archived-20261006-024824: db.jsonl | 03fcb0e3e6 | 0.270 | 0.263 | 7,089 | 7,089 | 58,024 | 65,113 | 216.0 | 0.356 | 0.675 | 0.113 | 0.266 | 0.199 | 0.566 |  |
| archived-20261006-024824: db.jsonl | 285b6909d1 | 0.283 | 0.248 | 7,172 | 7,172 | 58,032 | 65,204 | 216.0 | 0.342 | 0.812 | 0.106 | 0.248 | 0.249 | 0.616 |  |
| archived-20261006-024824: db.jsonl | 453a46a8e6 | 0.276 | 0.254 | 7,188 | 7,188 | 58,024 | 65,212 | 216.0 | 0.349 | 0.910 | 0.101 | 0.238 | 0.209 | 0.593 |  |
| archived-20261006-024824: db.jsonl | 3995ab7bde | 0.273 | 0.243 | 7,286 | 7,286 | 62,120 | 69,406 | 208.0 | 0.332 | 0.970 | 0.102 | 0.229 | 0.200 | 0.578 | yes |
| archived-20261006-024824: db.jsonl | 364a0f4617 | 0.257 | 0.249 | 7,689 | 7,689 | 58,024 | 65,713 | 216.0 | 0.319 | 0.820 | 0.099 | 0.228 | 0.192 | 0.535 |  |
| archived-20261006-024824: db.jsonl | 419cce1726 | 0.247 | 0.238 | 8,320 | 8,320 | 62,120 | 70,440 | 212.0 | 0.313 | 0.622 | 0.103 | 0.229 | 0.201 | 0.544 | yes |
| archived-20261006-131903: db.jsonl | 58c0a33fbe | 0.468 | 0.417 | 6,654 | 6,654 | 58,048 | 64,702 | 216.0 | 0.413 | 0.887 | 0.192 | 0.327 | 0.981 | 0.850 |  |
| archived-20261006-131903: db.jsonl | 29b1a365dc | 0.426 | 0.415 | 6,655 | 6,655 | 53,928 | 60,583 | 216.0 | 0.406 | 0.800 | 0.177 | 0.311 | 0.791 | 0.865 |  |
| archived-20261006-131903: db.jsonl | eabd014b0c | 0.450 | 0.402 | 6,673 | 6,673 | 53,928 | 60,601 | 216.0 | 0.414 | 0.879 | 0.179 | 0.317 | 0.889 | 0.863 |  |
| archived-20261006-131903: db.jsonl | 0df4c46cec | 0.421 | 0.412 | 6,680 | 6,680 | 53,928 | 60,608 | 216.0 | 0.419 | 0.706 | 0.178 | 0.320 | 0.779 | 0.833 |  |
| archived-20261006-131903: db.jsonl | 1d44bcb8a5 | 0.413 | 0.358 | 6,693 | 6,693 | 62,232 | 68,925 | 216.0 | 0.367 | 0.873 | 0.125 | 0.264 | 1.138 | 0.912 |  |
| archived-20261006-131903: db.jsonl | 9c2db9aebe | 0.380 | 0.353 | 6,699 | 6,699 | 62,208 | 68,907 | 216.0 | 0.360 | 0.858 | 0.117 | 0.255 | 0.860 | 0.815 |  |
| archived-20261006-131903: db.jsonl | f1c82fbd44 | 0.370 | 0.336 | 6,700 | 6,700 | 37,544 | 44,244 | 208.0 | 0.313 | 0.861 | 0.107 | 0.228 | 1.067 | 0.816 |  |
| archived-20261006-131903: db.jsonl | 9f9bfa4f49 | 0.367 | 0.334 | 6,711 | 6,711 | 37,632 | 44,343 | 208.0 | 0.320 | 0.837 | 0.122 | 0.242 | 0.839 | 0.730 |  |
| archived-20261006-131903: db.jsonl | eb0033be3d | 0.359 | 0.331 | 6,759 | 6,759 | 37,632 | 44,391 | 212.0 | 0.319 | 0.861 | 0.120 | 0.231 | 0.785 | 0.711 |  |
| archived-20261006-131903: db.jsonl | ce2e13ce87 | 0.331 | 0.311 | 6,777 | 6,777 | 53,936 | 60,713 | 216.0 | 0.414 | 0.838 | 0.186 | 0.320 | 0.194 | 0.635 |  |
| archived-20261006-131903: db.jsonl | d1b2f540a8 | 0.285 | 0.243 | 6,817 | 6,817 | 58,024 | 64,841 | 216.0 | 0.356 | 0.895 | 0.116 | 0.254 | 0.199 | 0.564 |  |
| archived-20261006-131903: db.jsonl | cbbc5291f8 | 0.253 | 0.246 | 6,940 | 6,940 | 58,024 | 64,964 | 216.0 | 0.333 | 0.756 | 0.095 | 0.219 | 0.197 | 0.552 |  |
| archived-20261006-131903: db.jsonl | 773f6d9daf | 0.267 | 0.239 | 6,993 | 6,993 | 58,032 | 65,025 | 216.0 | 0.336 | 0.934 | 0.098 | 0.224 | 0.198 | 0.583 |  |
| archived-20261006-131903: db.jsonl | 8298ca5d59 | 0.276 | 0.236 | 7,310 | 7,310 | 58,032 | 65,342 | 216.0 | 0.343 | 0.787 | 0.105 | 0.237 | 0.241 | 0.613 |  |
| archived-20261006-131903: db.jsonl | 3a96a12236 | 0.249 | 0.225 | 7,958 | 7,958 | 58,024 | 65,982 | 216.0 | 0.329 | 0.671 | 0.098 | 0.227 | 0.195 | 0.514 | yes |
| archived-20261006-160616: db.jsonl | 0826d64cd9 | 0.501 | 0.415 | 7,009 | 7,009 | 33,448 | 40,457 | 216.0 | 0.532 | 0.759 | 0.199 | 0.359 | 1.101 | 0.916 |  |
| archived-20261006-160616: db.jsonl | 69270766bd | 0.415 | 0.366 | 7,049 | 7,049 | 33,448 | 40,497 | 216.0 | 0.441 | 0.763 | 0.122 | 0.277 | 1.083 | 0.924 |  |
| archived-20261006-160616: db.jsonl | df2ac6c7ab | 0.398 | 0.336 | 7,050 | 7,050 | 37,544 | 44,594 | 216.0 | 0.443 | 0.671 | 0.119 | 0.275 | 1.032 | 0.874 |  |
| archived-20261006-160616: db.jsonl | 323f2ccfb8 | 0.386 | 0.337 | 7,105 | 7,105 | 37,544 | 44,649 | 216.0 | 0.377 | 0.776 | 0.109 | 0.244 | 1.105 | 0.923 |  |
| archived-20261006-160616: db.jsonl | 7c49a5ffca | 0.388 | 0.333 | 7,123 | 7,123 | 37,544 | 44,667 | 212.0 | 0.390 | 0.827 | 0.112 | 0.233 | 1.045 | 0.892 |  |
| archived-20261006-160616: db.jsonl | 2b5e92dd57 | 0.334 | 0.336 | 7,186 | 7,186 | 62,120 | 69,306 | 232.0 | 0.503 | 0.648 | 0.192 | 0.340 | 0.195 | 0.586 |  |
| archived-20261006-160616: db.jsonl | bfa7370096 | 0.369 | 0.339 | 7,202 | 7,202 | 66,216 | 73,418 | 232.0 | 0.362 | 0.865 | 0.100 | 0.236 | 0.923 | 0.843 |  |
| archived-20261006-160616: db.jsonl | 19104ead72 | 0.307 | 0.301 | 7,225 | 7,225 | 66,216 | 73,441 | 232.0 | 0.419 | 0.852 | 0.118 | 0.271 | 0.237 | 0.624 |  |
| archived-20261006-160616: db.jsonl | 4bb0870716 | 0.300 | 0.256 | 7,226 | 7,226 | 37,544 | 44,770 | 216.0 | 0.448 | 0.679 | 0.126 | 0.265 | 0.238 | 0.608 |  |
| archived-20261006-160616: db.jsonl | 4446c9069e | 0.288 | 0.251 | 7,274 | 7,274 | 33,448 | 40,722 | 216.0 | 0.417 | 0.622 | 0.117 | 0.246 | 0.267 | 0.624 |  |
| archived-20261006-160616: db.jsonl | 343d881df1 | 0.288 | 0.237 | 7,708 | 7,708 | 37,544 | 45,252 | 212.0 | 0.393 | 0.664 | 0.114 | 0.243 | 0.276 | 0.613 |  |
| archived-20261006-170257: db.jsonl | 3d312e796e | 0.501 | 0.419 | 7,009 | 7,009 | 33,448 | 40,457 | 216.0 | 0.526 | 0.762 | 0.201 | 0.353 | 1.104 | 0.916 |  |
| archived-20261006-170257: db.jsonl | a1ff4b8022 | 0.409 | 0.388 | 7,043 | 7,043 | 33,448 | 40,491 | 216.0 | 0.442 | 0.705 | 0.126 | 0.271 | 1.080 | 0.905 |  |
| archived-20261006-170257: db.jsonl | 3405116655 | 0.394 | 0.353 | 7,049 | 7,049 | 37,544 | 44,593 | 212.0 | 0.437 | 0.669 | 0.121 | 0.272 | 0.989 | 0.863 |  |
| archived-20261006-170257: db.jsonl | 4ba5b2c147 | 0.408 | 0.338 | 7,057 | 7,057 | 33,448 | 40,505 | 216.0 | 0.437 | 0.725 | 0.121 | 0.274 | 1.075 | 0.885 |  |
| archived-20261006-170257: db.jsonl | 0c5782b28a | 0.414 | 0.343 | 7,073 | 7,073 | 33,448 | 40,521 | 216.0 | 0.436 | 0.726 | 0.123 | 0.277 | 1.128 | 0.895 |  |
| archived-20261006-170257: db.jsonl | 31e4e22b2e | 0.381 | 0.343 | 7,085 | 7,085 | 33,448 | 40,533 | 216.0 | 0.415 | 0.629 | 0.114 | 0.247 | 1.096 | 0.974 |  |
| archived-20261006-170257: db.jsonl | a1578b537c | 0.392 | 0.334 | 7,120 | 7,120 | 37,544 | 44,664 | 216.0 | 0.380 | 0.793 | 0.112 | 0.244 | 1.128 | 0.992 |  |
| archived-20261006-170257: db.jsonl | e6a3c1fb8c | 0.391 | 0.318 | 7,130 | 7,130 | 37,544 | 44,674 | 212.0 | 0.380 | 0.818 | 0.111 | 0.239 | 1.105 | 0.936 |  |
| archived-20261006-170257: db.jsonl | ce3a84b4a0 | 0.322 | 0.307 | 7,217 | 7,217 | 33,448 | 40,665 | 216.0 | 0.438 | 0.806 | 0.121 | 0.264 | 0.308 | 0.591 |  |
| archived-20261006-170257: db.jsonl | 6583b9f742 | 0.319 | 0.277 | 7,218 | 7,218 | 37,544 | 44,762 | 216.0 | 0.456 | 0.789 | 0.125 | 0.261 | 0.281 | 0.643 |  |
| archived-20261006-170257: db.jsonl | 2b7e66e1f3 | 0.300 | 0.260 | 7,226 | 7,226 | 37,544 | 44,770 | 216.0 | 0.449 | 0.674 | 0.127 | 0.266 | 0.240 | 0.609 |  |
| archived-20261006-170257: db.jsonl | 38de166d54 | 0.299 | 0.267 | 7,234 | 7,234 | 37,544 | 44,778 | 216.0 | 0.454 | 0.656 | 0.127 | 0.269 | 0.235 | 0.616 |  |
| archived-20261006-170257: db.jsonl | 2b55d23a18 | 0.283 | 0.251 | 7,266 | 7,266 | 66,216 | 73,482 | 232.0 | 0.354 | 0.857 | 0.103 | 0.221 | 0.262 | 0.559 |  |
| archived-20261006-170257: db.jsonl | a36dc45e12 | 0.286 | 0.235 | 7,283 | 7,283 | 37,544 | 44,827 | 212.0 | 0.395 | 0.701 | 0.114 | 0.239 | 0.255 | 0.617 |  |
| archived-20261006-170257: db.jsonl | 5671742b27 | 0.306 | 0.234 | 7,690 | 7,690 | 37,544 | 45,234 | 212.0 | 0.386 | 0.867 | 0.112 | 0.242 | 0.296 | 0.650 |  |

The front of all runs together (speed, binary + image, peak memory), by binary + image: 60c95fbea3 0.243 at 74,548, 232.0 KB, 419cce1726 0.247 at 70,440, 212.0 KB, 3995ab7bde 0.273 at 69,406, 208.0 KB, 3a96a12236 0.249 at 65,982, 216.0 KB, 3c84b53247 0.391 at 44,483, 204.0 KB, 44af4fb785 0.253 at 42,861, 212.0 KB, 436af85b80 0.252 at 41,849, 216.0 KB, 0bab7fed3e 0.254 at 41,805, 212.0 KB, 9517490eb3 0.256 at 41,798, 212.0 KB, ca2e692954 0.275 at 41,186, 208.0 KB, 064ee4f23a 0.264 at 41,166, 212.0 KB, c13c77dc7c 0.288 at 40,811, 208.0 KB, 416077aa2f 0.277 at 40,797, 212.0 KB, bbab8560dd 0.258 at 40,786, 216.0 KB, 69842b04ad 0.274 at 40,771, 216.0 KB, 76ab789fed 0.264 at 38,958, 220.0 KB, 7f07a469cb 0.390 at 37,177, 208.0 KB, e076a00103 0.277 at 37,135, 216.0 KB, 7d7f1bf4fa 0.297 at 37,059, 212.0 KB, a03ef495f5 0.301 at 36,996, 216.0 KB, b0a896c3c3 0.359 at 36,723, 216.0 KB, 0f3d5dae58 0.361 at 36,707, 216.0 KB, a170190b5a 0.395 at 36,674, 208.0 KB, f48c2a5150 0.377 at 36,652, 212.0 KB, dac6ff750a 0.394 at 36,634, 210.0 KB, 2789713e31 0.400 at 36,618, 208.0 KB, 51a8931db2 0.388 at 36,467, 212.0 KB, 4daab7895a 0.426 at 33,086, 212.0 KB, b46a9c7ad4 0.447 at 32,957, 208.0 KB, 0039591d51 0.444 at 32,955, 212.0 KB, 63e3305540 0.444 at 32,944, 212.0 KB, 03cf426d67 0.451 at 32,819, 208.0 KB, 609b436e3a 0.450 at 32,609, 212.0 KB, e570f69332 0.440 at 32,554, 216.0 KB, 2a2c2b4256 0.457 at 32,538, 208.0 KB, d26dfdeda4 0.466 at 32,530, 208.0 KB, 4542a08fb0 0.465 at 32,474, 212.0 KB, 8252421ca2 0.482 at 32,474, 208.0 KB, f27cc3ce5a 0.558 at 32,388, 212.0 KB, 4996bc41b8 0.568 at 32,331, 208.0 KB

On the front by memory alone: 19 of 40 - 3995ab7bde 0.273 at 69,406, 208.0 KB, 3c84b53247 0.391 at 44,483, 204.0 KB, 44af4fb785 0.253 at 42,861, 212.0 KB, ca2e692954 0.275 at 41,186, 208.0 KB, 064ee4f23a 0.264 at 41,166, 212.0 KB, c13c77dc7c 0.288 at 40,811, 208.0 KB, 416077aa2f 0.277 at 40,797, 212.0 KB, 69842b04ad 0.274 at 40,771, 216.0 KB, 7f07a469cb 0.390 at 37,177, 208.0 KB, a170190b5a 0.395 at 36,674, 208.0 KB, dac6ff750a 0.394 at 36,634, 210.0 KB, 2789713e31 0.400 at 36,618, 208.0 KB, b46a9c7ad4 0.447 at 32,957, 208.0 KB, 0039591d51 0.444 at 32,955, 212.0 KB, 63e3305540 0.444 at 32,944, 212.0 KB, 03cf426d67 0.451 at 32,819, 208.0 KB, 609b436e3a 0.450 at 32,609, 212.0 KB, d26dfdeda4 0.466 at 32,530, 208.0 KB, 8252421ca2 0.482 at 32,474, 208.0 KB

## The same session on two CPUs

Calibration on cpu 2: 1.004; on cpu 8: 1.000.

Speed on cpu 2 over speed on cpu 8, per design: median 1.002, 10-90% 0.992-1.027, extremes 0.974-1.057; rank agreement (Spearman) 1.00.

The front of all runs on cpu 2: 60c95fbea3 0.243 at 74,548, 419cce1726 0.247 at 70,440, 3995ab7bde 0.273 at 69,406, 3a96a12236 0.249 at 65,982, 3c84b53247 0.391 at 44,483, 44af4fb785 0.253 at 42,861, 436af85b80 0.252 at 41,849, 0bab7fed3e 0.254 at 41,805, 9517490eb3 0.256 at 41,798, ca2e692954 0.275 at 41,186, 064ee4f23a 0.264 at 41,166, c13c77dc7c 0.288 at 40,811, 416077aa2f 0.277 at 40,797, bbab8560dd 0.258 at 40,786, 69842b04ad 0.274 at 40,771, 76ab789fed 0.264 at 38,958, 7f07a469cb 0.390 at 37,177, e076a00103 0.277 at 37,135, 7d7f1bf4fa 0.297 at 37,059, a03ef495f5 0.301 at 36,996, b0a896c3c3 0.359 at 36,723, 0f3d5dae58 0.361 at 36,707, a170190b5a 0.395 at 36,674, f48c2a5150 0.377 at 36,652, dac6ff750a 0.394 at 36,634, 2789713e31 0.400 at 36,618, 51a8931db2 0.388 at 36,467, 4daab7895a 0.426 at 33,086, b46a9c7ad4 0.447 at 32,957, 0039591d51 0.444 at 32,955, 63e3305540 0.444 at 32,944, 03cf426d67 0.451 at 32,819, 609b436e3a 0.450 at 32,609, e570f69332 0.440 at 32,554, 2a2c2b4256 0.457 at 32,538, d26dfdeda4 0.466 at 32,530, 8252421ca2 0.482 at 32,474, 4542a08fb0 0.465 at 32,474, f27cc3ce5a 0.558 at 32,388, 4996bc41b8 0.568 at 32,331

The front of all runs on cpu 8: 60c95fbea3 0.240 at 74,548, 3c84b53247 0.374 at 44,483, 436af85b80 0.245 at 41,849, 0bab7fed3e 0.246 at 41,805, 9517490eb3 0.254 at 41,798, 7075e8f2b1 0.270 at 41,186, 064ee4f23a 0.267 at 41,166, c13c77dc7c 0.290 at 40,811, 416077aa2f 0.280 at 40,797, bbab8560dd 0.257 at 40,786, 69842b04ad 0.266 at 40,771, 2117a45620 0.275 at 40,755, 76ab789fed 0.265 at 38,958, e076a00103 0.277 at 37,135, 7d7f1bf4fa 0.281 at 37,059, a03ef495f5 0.301 at 36,996, b0a896c3c3 0.355 at 36,723, 0f3d5dae58 0.357 at 36,707, a170190b5a 0.382 at 36,674, f48c2a5150 0.377 at 36,652, dac6ff750a 0.394 at 36,634, 2789713e31 0.395 at 36,618, 51a8931db2 0.387 at 36,467, 4daab7895a 0.418 at 33,086, b46a9c7ad4 0.448 at 32,957, 0039591d51 0.431 at 32,955, 63e3305540 0.445 at 32,944, 03cf426d67 0.452 at 32,819, 609b436e3a 0.449 at 32,609, e570f69332 0.441 at 32,554, 2a2c2b4256 0.459 at 32,538, d26dfdeda4 0.460 at 32,530, 8252421ca2 0.481 at 32,474, 4542a08fb0 0.467 at 32,474, f27cc3ce5a 0.559 at 32,388, 5c495fe0f3 0.568 at 32,370, 776c86e476 0.579 at 32,339, 844716c23e 0.583 at 32,331

On both fronts: 33 of 40 and 38.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| 60c95fbea3 | 0.243 | 0.240 | 1.014 |
| 419cce1726 | 0.247 | 0.251 | 0.984 |
| 3a96a12236 | 0.249 | 0.249 | 1.001 |
| 436af85b80 | 0.252 | 0.245 | 1.027 |
| 44af4fb785 | 0.253 | 0.253 | 0.996 |
| cbbc5291f8 | 0.253 | 0.248 | 1.019 |
| 0bab7fed3e | 0.254 | 0.246 | 1.034 |
| 4e3a904b8e | 0.255 | 0.253 | 1.009 |
| 9517490eb3 | 0.256 | 0.254 | 1.008 |
| 364a0f4617 | 0.257 | 0.256 | 1.006 |
| bbab8560dd | 0.258 | 0.257 | 1.005 |
| 76ab789fed | 0.264 | 0.265 | 0.998 |
| 064ee4f23a | 0.264 | 0.267 | 0.988 |
| 773f6d9daf | 0.267 | 0.268 | 0.997 |
| 0cf9f1e76a | 0.268 | 0.269 | 0.998 |
| 03fcb0e3e6 | 0.270 | 0.275 | 0.985 |
| 262f6959cc | 0.271 | 0.273 | 0.992 |
| 3995ab7bde | 0.273 | 0.273 | 1.001 |
| 69842b04ad | 0.274 | 0.266 | 1.031 |
| ca2e692954 | 0.275 | 0.276 | 0.995 |
| 453a46a8e6 | 0.276 | 0.276 | 1.000 |
| 8298ca5d59 | 0.276 | 0.274 | 1.010 |
| 416077aa2f | 0.277 | 0.280 | 0.989 |
| 7125b151e4 | 0.277 | 0.275 | 1.008 |
| 7075e8f2b1 | 0.277 | 0.270 | 1.029 |
| e076a00103 | 0.277 | 0.277 | 1.001 |
| 2bdab2950f | 0.278 | 0.280 | 0.992 |
| 2117a45620 | 0.278 | 0.275 | 1.014 |
| 98d7746633 | 0.281 | 0.279 | 1.006 |
| 2b55d23a18 | 0.283 | 0.283 | 0.999 |
| 285b6909d1 | 0.283 | 0.270 | 1.049 |
| 1c4300cbbb | 0.284 | 0.280 | 1.012 |
| d1b2f540a8 | 0.285 | 0.281 | 1.014 |
| a36dc45e12 | 0.286 | 0.289 | 0.992 |
| c13c77dc7c | 0.288 | 0.290 | 0.992 |
| 4446c9069e | 0.288 | 0.285 | 1.011 |
| 343d881df1 | 0.288 | 0.284 | 1.016 |
| 7d7f1bf4fa | 0.297 | 0.281 | 1.056 |
| 38de166d54 | 0.299 | 0.300 | 0.998 |
| ccc8da3b12 | 0.300 | 0.296 | 1.013 |
| 4bb0870716 | 0.300 | 0.294 | 1.019 |
| 2b7e66e1f3 | 0.300 | 0.294 | 1.022 |
| a03ef495f5 | 0.301 | 0.301 | 1.001 |
| 5671742b27 | 0.306 | 0.303 | 1.010 |
| 19104ead72 | 0.307 | 0.306 | 1.002 |
| 9f9c8fdb94 | 0.313 | 0.309 | 1.014 |
| 6583b9f742 | 0.319 | 0.319 | 0.999 |
| ce3a84b4a0 | 0.322 | 0.321 | 1.003 |
| 7033c6f1ab | 0.330 | 0.331 | 0.998 |
| ce2e13ce87 | 0.331 | 0.330 | 1.004 |
| 2b5e92dd57 | 0.334 | 0.325 | 1.028 |
| eb0033be3d | 0.359 | 0.354 | 1.016 |
| b0a896c3c3 | 0.359 | 0.355 | 1.011 |
| 0f3d5dae58 | 0.361 | 0.357 | 1.011 |
| 9f9bfa4f49 | 0.367 | 0.369 | 0.996 |
| bfa7370096 | 0.369 | 0.370 | 0.997 |
| 828c84dd15 | 0.369 | 0.368 | 1.005 |
| f1c82fbd44 | 0.370 | 0.371 | 1.000 |
| 5e7eed1cba | 0.373 | 0.372 | 1.001 |
| f48c2a5150 | 0.377 | 0.377 | 1.001 |
| 9c2db9aebe | 0.380 | 0.381 | 0.998 |
| 31e4e22b2e | 0.381 | 0.390 | 0.977 |
| 323f2ccfb8 | 0.386 | 0.385 | 1.002 |
| 7c49a5ffca | 0.388 | 0.392 | 0.990 |
| 51a8931db2 | 0.388 | 0.387 | 1.002 |
| 7f07a469cb | 0.390 | 0.387 | 1.009 |
| 3c84b53247 | 0.391 | 0.374 | 1.044 |
| e6a3c1fb8c | 0.391 | 0.391 | 0.999 |
| a1578b537c | 0.392 | 0.387 | 1.013 |
| dac6ff750a | 0.394 | 0.394 | 0.999 |
| 9a9d2cb947 | 0.394 | 0.390 | 1.010 |
| 3405116655 | 0.394 | 0.398 | 0.990 |
| a170190b5a | 0.395 | 0.382 | 1.033 |
| df2ac6c7ab | 0.398 | 0.397 | 1.003 |
| 2789713e31 | 0.400 | 0.395 | 1.013 |
| 4ba5b2c147 | 0.408 | 0.408 | 1.000 |
| a1ff4b8022 | 0.409 | 0.406 | 1.009 |
| 8a6365a3ff | 0.411 | 0.389 | 1.057 |
| 1d44bcb8a5 | 0.413 | 0.413 | 0.999 |
| 0c5782b28a | 0.414 | 0.413 | 1.002 |
| 69270766bd | 0.415 | 0.412 | 1.005 |
| 0df4c46cec | 0.421 | 0.422 | 0.996 |
| 4daab7895a | 0.426 | 0.418 | 1.019 |
| 29b1a365dc | 0.426 | 0.428 | 0.996 |
| b7b4dd1166 | 0.435 | 0.434 | 1.002 |
| e570f69332 | 0.440 | 0.441 | 0.997 |
| 0039591d51 | 0.444 | 0.431 | 1.030 |
| 63e3305540 | 0.444 | 0.445 | 0.998 |
| 301a268219 | 0.446 | 0.444 | 1.005 |
| b46a9c7ad4 | 0.447 | 0.448 | 0.998 |
| eabd014b0c | 0.450 | 0.442 | 1.018 |
| 609b436e3a | 0.450 | 0.449 | 1.001 |
| 03cf426d67 | 0.451 | 0.452 | 0.997 |
| 3280937f3d | 0.453 | 0.455 | 0.995 |
| a808c92923 | 0.455 | 0.455 | 1.000 |
| 2a2c2b4256 | 0.457 | 0.459 | 0.995 |
| 097ff5bdce | 0.462 | 0.446 | 1.036 |
| 4542a08fb0 | 0.465 | 0.467 | 0.995 |
| d26dfdeda4 | 0.466 | 0.460 | 1.014 |
| 740331292d | 0.467 | 0.469 | 0.995 |
| 58c0a33fbe | 0.468 | 0.471 | 0.994 |
| 520f651e31 | 0.470 | 0.469 | 1.002 |
| 7f7d8e7864 | 0.476 | 0.475 | 1.002 |
| 8252421ca2 | 0.482 | 0.481 | 1.001 |
| 3d312e796e | 0.501 | 0.500 | 1.001 |
| 0826d64cd9 | 0.501 | 0.500 | 1.003 |
| f27cc3ce5a | 0.558 | 0.559 | 0.998 |
| 4996bc41b8 | 0.568 | 0.583 | 0.974 |
| 5c495fe0f3 | 0.569 | 0.568 | 1.001 |
| 776c86e476 | 0.577 | 0.579 | 0.997 |
| 844716c23e | 0.587 | 0.583 | 1.007 |
| eef03e6a19 | 1.081 | 1.090 | 0.991 |
| 35728dddcf | 1.085 | 1.085 | 1.000 |
| 0350ea6ee2 | 1.195 | 1.194 | 1.001 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 17 - Iteration 78: seed 19 and the newest four

`seed 19 tag2 then experiment compare-fronts.py --rounds 10 --cpus 2,8`,
commit 6482259b: seeds 15-19, 116 designs; memory within 8 KB a tie.
**Calibration 1.009.** The CPUs: median 1.003, 10-90% 0.988-1.026, ranks
1.00; 14 of 18 and 18 on both fronts. **The front of all runs: 18, by
memory alone 0** - 12 of seed 19, 6 of seed 18. The stopping rule: seed 19
small (fastest +2.5%, smallest total +0.1%, least memory none).

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 1.009** (kernel 1.018, fib 1.001, parse 0.999, corpus 1.021, loop 1.005, sieve 1.023).

| run | design | speed now | recorded | size now | recorded | binary | binary + image | memory KB | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | f69da4fcc8 | 0.601 | 0.605 | 7,019 | 7,019 | 25,280 | 32,299 | 212.0 | 0.582 | 1.114 | 0.237 | 0.392 | 1.302 | 1.058 | yes |
| this clone: db.jsonl | 263788ab64 | 0.558 | 0.561 | 7,032 | 7,032 | 25,280 | 32,312 | 208.0 | 0.509 | 1.201 | 0.213 | 0.335 | 1.246 | 1.081 | yes |
| this clone: db.jsonl | 2f4c1d82ec | 0.549 | 0.541 | 7,056 | 7,056 | 25,280 | 32,336 | 208.0 | 0.501 | 1.105 | 0.212 | 0.338 | 1.260 | 1.057 | yes |
| this clone: db.jsonl | 775d8dda6e | 0.357 | 0.357 | 7,091 | 7,091 | 29,352 | 36,443 | 212.0 | 0.355 | 0.653 | 0.109 | 0.231 | 0.986 | 0.855 | yes |
| this clone: db.jsonl | 570f49c26e | 0.353 | 0.350 | 7,102 | 7,102 | 29,352 | 36,454 | 212.0 | 0.357 | 0.604 | 0.099 | 0.231 | 1.110 | 0.875 | yes |
| this clone: db.jsonl | 9fac496194 | 0.348 | 0.347 | 7,115 | 7,115 | 29,352 | 36,467 | 212.0 | 0.359 | 0.624 | 0.098 | 0.226 | 1.025 | 0.863 | yes |
| this clone: db.jsonl | b00da878bf | 0.465 | 0.469 | 7,210 | 7,210 | 25,280 | 32,490 | 216.0 | 0.564 | 1.121 | 0.233 | 0.376 | 0.395 | 0.716 |  |
| this clone: db.jsonl | 635a47fd26 | 0.458 | 0.448 | 7,260 | 7,260 | 25,280 | 32,540 | 208.0 | 0.578 | 1.103 | 0.222 | 0.354 | 0.403 | 0.730 |  |
| this clone: db.jsonl | 74ea2d2e27 | 0.299 | 0.304 | 7,274 | 7,274 | 29,352 | 36,626 | 212.0 | 0.397 | 0.513 | 0.172 | 0.286 | 0.239 | 0.579 | yes |
| this clone: db.jsonl | 8f0973fc8f | 0.433 | 0.438 | 7,274 | 7,274 | 25,280 | 32,554 | 212.0 | 0.521 | 1.116 | 0.217 | 0.304 | 0.396 | 0.711 | yes |
| this clone: db.jsonl | c57aebeb3e | 0.271 | 0.277 | 7,282 | 7,282 | 29,352 | 36,634 | 212.0 | 0.363 | 0.598 | 0.108 | 0.226 | 0.279 | 0.586 | yes |
| this clone: db.jsonl | 272854107e | 0.272 | 0.275 | 7,290 | 7,290 | 29,352 | 36,642 | 212.0 | 0.367 | 0.644 | 0.107 | 0.227 | 0.261 | 0.609 |  |
| this clone: db.jsonl | ae5d7cdaae | 0.434 | 0.434 | 7,317 | 7,317 | 25,280 | 32,597 | 212.0 | 0.530 | 1.121 | 0.218 | 0.328 | 0.362 | 0.733 |  |
| this clone: db.jsonl | d05d104578 | 0.430 | 0.436 | 7,466 | 7,466 | 25,280 | 32,746 | 212.0 | 0.492 | 1.104 | 0.219 | 0.328 | 0.377 | 0.702 | yes |
| this clone: db.jsonl | 870c24c9cf | 0.439 | 0.440 | 7,632 | 7,632 | 25,280 | 32,912 | 212.0 | 0.512 | 1.118 | 0.215 | 0.325 | 0.405 | 0.716 |  |
| this clone: db.jsonl | 7670d35541 | 0.274 | 0.273 | 7,682 | 7,682 | 29,352 | 37,034 | 212.0 | 0.405 | 0.555 | 0.105 | 0.229 | 0.285 | 0.611 |  |
| this clone: db.jsonl | 1a90a3e004 | 0.261 | 0.257 | 7,712 | 7,712 | 29,352 | 37,064 | 212.0 | 0.368 | 0.611 | 0.106 | 0.222 | 0.228 | 0.492 | yes |
| this clone: db.jsonl | cc0b1e2aeb | 0.238 | 0.241 | 9,064 | 9,064 | 33,448 | 42,512 | 216.0 | 0.357 | 0.559 | 0.103 | 0.230 | 0.163 | 0.510 | yes |
| this clone: db.jsonl | d60e3aab99 | 0.253 | 0.253 | 9,064 | 9,064 | 37,544 | 46,608 | 216.0 | 0.359 | 0.605 | 0.105 | 0.227 | 0.202 | 0.509 |  |
| archived-20261006-131903: db.jsonl | 58c0a33fbe | 0.470 | 0.417 | 6,654 | 6,654 | 58,048 | 64,702 | 216.0 | 0.416 | 0.887 | 0.192 | 0.330 | 0.980 | 0.869 |  |
| archived-20261006-131903: db.jsonl | 29b1a365dc | 0.427 | 0.415 | 6,655 | 6,655 | 53,928 | 60,583 | 216.0 | 0.400 | 0.803 | 0.177 | 0.317 | 0.791 | 0.821 |  |
| archived-20261006-131903: db.jsonl | eabd014b0c | 0.442 | 0.402 | 6,673 | 6,673 | 53,928 | 60,601 | 216.0 | 0.397 | 0.885 | 0.182 | 0.307 | 0.855 | 0.879 |  |
| archived-20261006-131903: db.jsonl | 0df4c46cec | 0.421 | 0.412 | 6,680 | 6,680 | 53,928 | 60,608 | 216.0 | 0.417 | 0.716 | 0.181 | 0.319 | 0.774 | 0.821 |  |
| archived-20261006-131903: db.jsonl | 1d44bcb8a5 | 0.410 | 0.358 | 6,693 | 6,693 | 62,232 | 68,925 | 216.0 | 0.372 | 0.885 | 0.121 | 0.256 | 1.140 | 0.894 |  |
| archived-20261006-131903: db.jsonl | 9c2db9aebe | 0.385 | 0.353 | 6,699 | 6,699 | 62,208 | 68,907 | 216.0 | 0.377 | 0.858 | 0.119 | 0.259 | 0.852 | 0.787 |  |
| archived-20261006-131903: db.jsonl | f1c82fbd44 | 0.369 | 0.336 | 6,700 | 6,700 | 37,544 | 44,244 | 208.0 | 0.320 | 0.843 | 0.104 | 0.232 | 1.040 | 0.813 |  |
| archived-20261006-131903: db.jsonl | 9f9bfa4f49 | 0.368 | 0.334 | 6,711 | 6,711 | 37,632 | 44,343 | 208.0 | 0.320 | 0.852 | 0.121 | 0.240 | 0.857 | 0.735 |  |
| archived-20261006-131903: db.jsonl | eb0033be3d | 0.358 | 0.331 | 6,759 | 6,759 | 37,632 | 44,391 | 208.0 | 0.317 | 0.843 | 0.120 | 0.232 | 0.781 | 0.720 |  |
| archived-20261006-131903: db.jsonl | ce2e13ce87 | 0.332 | 0.311 | 6,777 | 6,777 | 53,936 | 60,713 | 216.0 | 0.418 | 0.835 | 0.186 | 0.318 | 0.195 | 0.638 |  |
| archived-20261006-131903: db.jsonl | d1b2f540a8 | 0.283 | 0.243 | 6,817 | 6,817 | 58,024 | 64,841 | 216.0 | 0.353 | 0.893 | 0.116 | 0.247 | 0.199 | 0.571 |  |
| archived-20261006-131903: db.jsonl | cbbc5291f8 | 0.254 | 0.246 | 6,940 | 6,940 | 58,024 | 64,964 | 216.0 | 0.335 | 0.754 | 0.097 | 0.223 | 0.195 | 0.557 |  |
| archived-20261006-131903: db.jsonl | 773f6d9daf | 0.269 | 0.239 | 6,993 | 6,993 | 58,032 | 65,025 | 216.0 | 0.335 | 0.940 | 0.099 | 0.231 | 0.197 | 0.577 |  |
| archived-20261006-131903: db.jsonl | 8298ca5d59 | 0.276 | 0.236 | 7,310 | 7,310 | 58,032 | 65,342 | 216.0 | 0.337 | 0.802 | 0.105 | 0.234 | 0.243 | 0.612 |  |
| archived-20261006-131903: db.jsonl | 3a96a12236 | 0.249 | 0.225 | 7,958 | 7,958 | 58,024 | 65,982 | 216.0 | 0.324 | 0.669 | 0.097 | 0.232 | 0.197 | 0.513 |  |
| archived-20261006-160616: db.jsonl | 0826d64cd9 | 0.498 | 0.415 | 7,009 | 7,009 | 33,448 | 40,457 | 216.0 | 0.523 | 0.765 | 0.198 | 0.350 | 1.103 | 0.909 |  |
| archived-20261006-160616: db.jsonl | 69270766bd | 0.412 | 0.366 | 7,049 | 7,049 | 33,448 | 40,497 | 216.0 | 0.436 | 0.767 | 0.124 | 0.261 | 1.092 | 0.916 |  |
| archived-20261006-160616: db.jsonl | df2ac6c7ab | 0.402 | 0.336 | 7,050 | 7,050 | 37,544 | 44,594 | 216.0 | 0.446 | 0.672 | 0.124 | 0.271 | 1.035 | 0.873 |  |
| archived-20261006-160616: db.jsonl | 323f2ccfb8 | 0.383 | 0.337 | 7,105 | 7,105 | 37,544 | 44,649 | 216.0 | 0.383 | 0.770 | 0.109 | 0.231 | 1.110 | 0.934 |  |
| archived-20261006-160616: db.jsonl | 7c49a5ffca | 0.386 | 0.333 | 7,123 | 7,123 | 37,544 | 44,667 | 212.0 | 0.382 | 0.813 | 0.112 | 0.235 | 1.039 | 0.911 |  |
| archived-20261006-160616: db.jsonl | 2b5e92dd57 | 0.332 | 0.336 | 7,186 | 7,186 | 62,120 | 69,306 | 232.0 | 0.502 | 0.647 | 0.191 | 0.337 | 0.193 | 0.592 |  |
| archived-20261006-160616: db.jsonl | bfa7370096 | 0.368 | 0.339 | 7,202 | 7,202 | 66,216 | 73,418 | 232.0 | 0.360 | 0.874 | 0.101 | 0.230 | 0.920 | 0.804 |  |
| archived-20261006-160616: db.jsonl | 19104ead72 | 0.303 | 0.301 | 7,225 | 7,225 | 66,216 | 73,441 | 232.0 | 0.421 | 0.853 | 0.119 | 0.274 | 0.217 | 0.616 |  |
| archived-20261006-160616: db.jsonl | 4bb0870716 | 0.297 | 0.256 | 7,226 | 7,226 | 37,544 | 44,770 | 216.0 | 0.452 | 0.675 | 0.125 | 0.264 | 0.229 | 0.599 |  |
| archived-20261006-160616: db.jsonl | 4446c9069e | 0.294 | 0.251 | 7,274 | 7,274 | 33,448 | 40,722 | 216.0 | 0.424 | 0.632 | 0.120 | 0.248 | 0.275 | 0.601 |  |
| archived-20261006-160616: db.jsonl | 343d881df1 | 0.286 | 0.237 | 7,708 | 7,708 | 37,544 | 45,252 | 212.0 | 0.397 | 0.663 | 0.112 | 0.232 | 0.279 | 0.612 |  |
| archived-20261006-170257: db.jsonl | 3d312e796e | 0.499 | 0.419 | 7,009 | 7,009 | 33,448 | 40,457 | 216.0 | 0.519 | 0.765 | 0.198 | 0.355 | 1.108 | 0.916 |  |
| archived-20261006-170257: db.jsonl | a1ff4b8022 | 0.409 | 0.388 | 7,043 | 7,043 | 33,448 | 40,491 | 216.0 | 0.440 | 0.700 | 0.127 | 0.274 | 1.077 | 0.886 |  |
| archived-20261006-170257: db.jsonl | 3405116655 | 0.397 | 0.353 | 7,049 | 7,049 | 37,544 | 44,593 | 212.0 | 0.433 | 0.670 | 0.122 | 0.281 | 0.984 | 0.885 |  |
| archived-20261006-170257: db.jsonl | 4ba5b2c147 | 0.409 | 0.338 | 7,057 | 7,057 | 33,448 | 40,505 | 216.0 | 0.435 | 0.724 | 0.121 | 0.280 | 1.073 | 0.840 |  |
| archived-20261006-170257: db.jsonl | 0c5782b28a | 0.406 | 0.343 | 7,073 | 7,073 | 33,448 | 40,521 | 216.0 | 0.403 | 0.725 | 0.123 | 0.272 | 1.128 | 0.893 |  |
| archived-20261006-170257: db.jsonl | 31e4e22b2e | 0.389 | 0.343 | 7,085 | 7,085 | 33,448 | 40,533 | 216.0 | 0.415 | 0.632 | 0.116 | 0.261 | 1.127 | 0.982 |  |
| archived-20261006-170257: db.jsonl | a1578b537c | 0.392 | 0.334 | 7,120 | 7,120 | 37,544 | 44,664 | 216.0 | 0.382 | 0.798 | 0.111 | 0.241 | 1.133 | 0.957 |  |
| archived-20261006-170257: db.jsonl | e6a3c1fb8c | 0.393 | 0.318 | 7,130 | 7,130 | 37,544 | 44,674 | 212.0 | 0.378 | 0.821 | 0.112 | 0.244 | 1.104 | 0.898 |  |
| archived-20261006-170257: db.jsonl | ce3a84b4a0 | 0.320 | 0.307 | 7,217 | 7,217 | 33,448 | 40,665 | 216.0 | 0.430 | 0.803 | 0.123 | 0.258 | 0.310 | 0.613 |  |
| archived-20261006-170257: db.jsonl | 6583b9f742 | 0.318 | 0.277 | 7,218 | 7,218 | 37,544 | 44,762 | 216.0 | 0.447 | 0.782 | 0.125 | 0.265 | 0.280 | 0.649 |  |
| archived-20261006-170257: db.jsonl | 2b7e66e1f3 | 0.301 | 0.260 | 7,226 | 7,226 | 37,544 | 44,770 | 216.0 | 0.451 | 0.674 | 0.127 | 0.270 | 0.237 | 0.605 |  |
| archived-20261006-170257: db.jsonl | 38de166d54 | 0.300 | 0.267 | 7,234 | 7,234 | 37,544 | 44,778 | 216.0 | 0.451 | 0.659 | 0.127 | 0.270 | 0.239 | 0.611 |  |
| archived-20261006-170257: db.jsonl | 2b55d23a18 | 0.283 | 0.251 | 7,266 | 7,266 | 66,216 | 73,482 | 232.0 | 0.349 | 0.845 | 0.103 | 0.226 | 0.261 | 0.558 |  |
| archived-20261006-170257: db.jsonl | a36dc45e12 | 0.286 | 0.235 | 7,283 | 7,283 | 37,544 | 44,827 | 212.0 | 0.395 | 0.696 | 0.112 | 0.235 | 0.265 | 0.607 |  |
| archived-20261006-170257: db.jsonl | 5671742b27 | 0.306 | 0.234 | 7,690 | 7,690 | 37,544 | 45,234 | 212.0 | 0.384 | 0.887 | 0.113 | 0.232 | 0.302 | 0.611 |  |
| archived-20261006-175959: db.jsonl | 4996bc41b8 | 0.573 | 0.586 | 7,051 | 7,051 | 25,280 | 32,331 | 208.0 | 0.569 | 1.225 | 0.225 | 0.329 | 1.203 | 1.073 |  |
| archived-20261006-175959: db.jsonl | 844716c23e | 0.585 | 0.589 | 7,051 | 7,051 | 25,280 | 32,331 | 208.0 | 0.568 | 1.208 | 0.224 | 0.371 | 1.197 | 1.058 |  |
| archived-20261006-175959: db.jsonl | 776c86e476 | 0.578 | 0.574 | 7,059 | 7,059 | 25,280 | 32,339 | 208.0 | 0.562 | 1.133 | 0.228 | 0.371 | 1.199 | 1.045 |  |
| archived-20261006-175959: db.jsonl | 5c495fe0f3 | 0.569 | 0.568 | 7,090 | 7,090 | 25,280 | 32,370 | 212.0 | 0.553 | 1.156 | 0.223 | 0.361 | 1.154 | 1.014 |  |
| archived-20261006-175959: db.jsonl | f27cc3ce5a | 0.557 | 0.559 | 7,108 | 7,108 | 25,280 | 32,388 | 212.0 | 0.525 | 1.112 | 0.223 | 0.352 | 1.171 | 1.013 |  |
| archived-20261006-175959: db.jsonl | 51a8931db2 | 0.386 | 0.385 | 7,115 | 7,115 | 29,352 | 36,467 | 212.0 | 0.386 | 0.776 | 0.108 | 0.243 | 1.098 | 0.946 |  |
| archived-20261006-175959: db.jsonl | 4542a08fb0 | 0.463 | 0.466 | 7,194 | 7,194 | 25,280 | 32,474 | 212.0 | 0.585 | 1.091 | 0.232 | 0.375 | 0.382 | 0.729 | yes |
| archived-20261006-175959: db.jsonl | 8252421ca2 | 0.482 | 0.482 | 7,194 | 7,194 | 25,280 | 32,474 | 208.0 | 0.606 | 1.149 | 0.245 | 0.390 | 0.392 | 0.720 |  |
| archived-20261006-175959: db.jsonl | 8a6365a3ff | 0.407 | 0.406 | 7,217 | 7,217 | 29,376 | 36,593 | 212.0 | 0.531 | 1.102 | 0.148 | 0.296 | 0.433 | 0.751 |  |
| archived-20261006-175959: db.jsonl | 2789713e31 | 0.401 | 0.398 | 7,242 | 7,242 | 29,376 | 36,618 | 208.0 | 0.519 | 1.083 | 0.154 | 0.305 | 0.390 | 0.746 |  |
| archived-20261006-175959: db.jsonl | d26dfdeda4 | 0.466 | 0.461 | 7,250 | 7,250 | 25,280 | 32,530 | 208.0 | 0.575 | 1.145 | 0.230 | 0.364 | 0.397 | 0.740 |  |
| archived-20261006-175959: db.jsonl | dac6ff750a | 0.390 | 0.392 | 7,258 | 7,258 | 29,376 | 36,634 | 208.0 | 0.519 | 1.010 | 0.157 | 0.301 | 0.363 | 0.719 |  |
| archived-20261006-175959: db.jsonl | 2a2c2b4256 | 0.455 | 0.457 | 7,258 | 7,258 | 25,280 | 32,538 | 208.0 | 0.547 | 1.118 | 0.225 | 0.360 | 0.392 | 0.755 | yes |
| archived-20261006-175959: db.jsonl | e570f69332 | 0.438 | 0.434 | 7,274 | 7,274 | 25,280 | 32,554 | 216.0 | 0.514 | 1.122 | 0.220 | 0.322 | 0.397 | 0.729 |  |
| archived-20261006-175959: db.jsonl | f48c2a5150 | 0.379 | 0.377 | 7,276 | 7,276 | 29,376 | 36,652 | 212.0 | 0.406 | 0.942 | 0.204 | 0.302 | 0.330 | 0.673 |  |
| archived-20261006-175959: db.jsonl | a170190b5a | 0.391 | 0.386 | 7,298 | 7,298 | 29,376 | 36,674 | 208.0 | 0.515 | 1.164 | 0.147 | 0.284 | 0.367 | 0.729 |  |
| archived-20261006-175959: db.jsonl | 2117a45620 | 0.279 | 0.274 | 7,307 | 7,307 | 33,448 | 40,755 | 216.0 | 0.419 | 0.493 | 0.119 | 0.255 | 0.270 | 0.525 |  |
| archived-20261006-175959: db.jsonl | 4e3a904b8e | 0.252 | 0.255 | 7,323 | 7,323 | 62,128 | 69,451 | 232.0 | 0.367 | 0.592 | 0.105 | 0.232 | 0.193 | 0.538 |  |
| archived-20261006-175959: db.jsonl | 69842b04ad | 0.273 | 0.268 | 7,323 | 7,323 | 33,448 | 40,771 | 216.0 | 0.392 | 0.689 | 0.105 | 0.234 | 0.228 | 0.612 |  |
| archived-20261006-175959: db.jsonl | 609b436e3a | 0.447 | 0.450 | 7,329 | 7,329 | 25,280 | 32,609 | 212.0 | 0.562 | 1.062 | 0.221 | 0.363 | 0.374 | 0.708 |  |
| archived-20261006-175959: db.jsonl | 0f3d5dae58 | 0.361 | 0.352 | 7,331 | 7,331 | 29,376 | 36,707 | 216.0 | 0.457 | 0.945 | 0.132 | 0.262 | 0.406 | 0.731 |  |
| archived-20261006-175959: db.jsonl | bbab8560dd | 0.267 | 0.261 | 7,338 | 7,338 | 33,448 | 40,786 | 216.0 | 0.381 | 0.549 | 0.098 | 0.233 | 0.284 | 0.506 |  |
| archived-20261006-175959: db.jsonl | 1c4300cbbb | 0.281 | 0.285 | 7,338 | 7,338 | 33,448 | 40,786 | 216.0 | 0.412 | 0.666 | 0.103 | 0.236 | 0.263 | 0.623 |  |
| archived-20261006-175959: db.jsonl | c13c77dc7c | 0.288 | 0.286 | 7,339 | 7,339 | 33,472 | 40,811 | 208.0 | 0.392 | 0.648 | 0.111 | 0.240 | 0.291 | 0.640 |  |
| archived-20261006-175959: db.jsonl | b0a896c3c3 | 0.359 | 0.358 | 7,347 | 7,347 | 29,376 | 36,723 | 216.0 | 0.460 | 1.039 | 0.128 | 0.249 | 0.390 | 0.728 |  |
| archived-20261006-175959: db.jsonl | 416077aa2f | 0.281 | 0.272 | 7,349 | 7,349 | 33,448 | 40,797 | 212.0 | 0.381 | 0.744 | 0.112 | 0.238 | 0.233 | 0.593 |  |
| archived-20261006-175959: db.jsonl | 0cf9f1e76a | 0.269 | 0.265 | 7,365 | 7,365 | 62,128 | 69,493 | 232.0 | 0.400 | 0.725 | 0.107 | 0.239 | 0.191 | 0.545 |  |
| archived-20261006-175959: db.jsonl | 740331292d | 0.465 | 0.467 | 7,505 | 7,505 | 25,280 | 32,785 | 208.0 | 0.577 | 1.111 | 0.226 | 0.367 | 0.410 | 0.747 |  |
| archived-20261006-175959: db.jsonl | 03cf426d67 | 0.452 | 0.448 | 7,539 | 7,539 | 25,280 | 32,819 | 208.0 | 0.520 | 1.207 | 0.224 | 0.344 | 0.389 | 0.750 |  |
| archived-20261006-175959: db.jsonl | a03ef495f5 | 0.302 | 0.301 | 7,644 | 7,644 | 29,352 | 36,996 | 216.0 | 0.407 | 0.788 | 0.109 | 0.260 | 0.279 | 0.565 |  |
| archived-20261006-175959: db.jsonl | 63e3305540 | 0.449 | 0.438 | 7,664 | 7,664 | 25,280 | 32,944 | 212.0 | 0.534 | 1.201 | 0.218 | 0.339 | 0.387 | 0.732 |  |
| archived-20261006-175959: db.jsonl | 0039591d51 | 0.448 | 0.442 | 7,675 | 7,675 | 25,280 | 32,955 | 212.0 | 0.573 | 1.070 | 0.224 | 0.352 | 0.373 | 0.732 |  |
| archived-20261006-175959: db.jsonl | b46a9c7ad4 | 0.448 | 0.447 | 7,677 | 7,677 | 25,280 | 32,957 | 208.0 | 0.563 | 1.044 | 0.220 | 0.354 | 0.393 | 0.726 |  |
| archived-20261006-175959: db.jsonl | 301a268219 | 0.446 | 0.444 | 7,683 | 7,683 | 25,280 | 32,963 | 212.0 | 0.531 | 1.145 | 0.219 | 0.336 | 0.397 | 0.725 |  |
| archived-20261006-175959: db.jsonl | a808c92923 | 0.457 | 0.456 | 7,698 | 7,698 | 25,280 | 32,978 | 208.0 | 0.595 | 1.108 | 0.229 | 0.366 | 0.361 | 0.739 |  |
| archived-20261006-175959: db.jsonl | 7d7f1bf4fa | 0.292 | 0.291 | 7,707 | 7,707 | 29,352 | 37,059 | 212.0 | 0.393 | 0.784 | 0.108 | 0.235 | 0.272 | 0.604 |  |
| archived-20261006-175959: db.jsonl | 064ee4f23a | 0.266 | 0.263 | 7,718 | 7,718 | 33,448 | 41,166 | 212.0 | 0.411 | 0.561 | 0.107 | 0.239 | 0.227 | 0.606 |  |
| archived-20261006-175959: db.jsonl | ca2e692954 | 0.276 | 0.273 | 7,738 | 7,738 | 33,448 | 41,186 | 208.0 | 0.364 | 0.762 | 0.107 | 0.223 | 0.243 | 0.598 |  |
| archived-20261006-175959: db.jsonl | 7075e8f2b1 | 0.280 | 0.278 | 7,738 | 7,738 | 33,448 | 41,186 | 208.0 | 0.370 | 0.676 | 0.110 | 0.230 | 0.273 | 0.563 |  |
| archived-20261006-175959: db.jsonl | 9f9c8fdb94 | 0.309 | 0.310 | 7,744 | 7,744 | 33,448 | 41,192 | 208.0 | 0.432 | 0.786 | 0.105 | 0.250 | 0.313 | 0.639 |  |
| archived-20261006-175959: db.jsonl | ccc8da3b12 | 0.301 | 0.300 | 7,759 | 7,759 | 33,448 | 41,207 | 208.0 | 0.406 | 0.560 | 0.106 | 0.240 | 0.430 | 0.697 |  |
| archived-20261006-175959: db.jsonl | 2bdab2950f | 0.277 | 0.278 | 7,783 | 7,783 | 29,352 | 37,135 | 216.0 | 0.395 | 0.634 | 0.112 | 0.229 | 0.252 | 0.620 |  |
| archived-20261006-175959: db.jsonl | e076a00103 | 0.278 | 0.274 | 7,783 | 7,783 | 29,352 | 37,135 | 216.0 | 0.401 | 0.631 | 0.112 | 0.233 | 0.251 | 0.604 |  |
| archived-20261006-175959: db.jsonl | 7f07a469cb | 0.389 | 0.390 | 7,801 | 7,801 | 29,376 | 37,177 | 208.0 | 0.511 | 1.215 | 0.139 | 0.279 | 0.369 | 0.758 |  |
| archived-20261006-175959: db.jsonl | 4daab7895a | 0.428 | 0.425 | 7,806 | 7,806 | 25,280 | 33,086 | 212.0 | 0.521 | 1.079 | 0.216 | 0.326 | 0.365 | 0.710 | yes |
| archived-20261006-175959: db.jsonl | 7125b151e4 | 0.274 | 0.273 | 7,970 | 7,970 | 33,448 | 41,418 | 212.0 | 0.390 | 0.600 | 0.104 | 0.241 | 0.262 | 0.591 |  |
| archived-20261006-175959: db.jsonl | 60c95fbea3 | 0.244 | 0.239 | 8,332 | 8,332 | 66,216 | 74,548 | 232.0 | 0.379 | 0.428 | 0.105 | 0.232 | 0.219 | 0.547 |  |
| archived-20261006-175959: db.jsonl | 9517490eb3 | 0.257 | 0.258 | 8,350 | 8,350 | 33,448 | 41,798 | 212.0 | 0.383 | 0.601 | 0.109 | 0.231 | 0.194 | 0.615 | yes |
| archived-20261006-175959: db.jsonl | 0bab7fed3e | 0.256 | 0.252 | 8,357 | 8,357 | 33,448 | 41,805 | 212.0 | 0.384 | 0.613 | 0.107 | 0.232 | 0.187 | 0.586 | yes |
| archived-20261006-175959: db.jsonl | 436af85b80 | 0.249 | 0.249 | 8,401 | 8,401 | 33,448 | 41,849 | 216.0 | 0.387 | 0.513 | 0.109 | 0.233 | 0.190 | 0.493 | yes |
| archived-20261006-175959: db.jsonl | 44af4fb785 | 0.249 | 0.252 | 9,413 | 9,413 | 33,448 | 42,861 | 212.0 | 0.382 | 0.601 | 0.107 | 0.207 | 0.188 | 0.615 |  |
| archived-20261006-175959: db.jsonl | 98d7746633 | 0.281 | 0.282 | 9,598 | 9,598 | 29,352 | 38,950 | 216.0 | 0.383 | 0.637 | 0.109 | 0.231 | 0.286 | 0.679 |  |
| archived-20261006-175959: db.jsonl | 76ab789fed | 0.263 | 0.264 | 9,606 | 9,606 | 29,352 | 38,958 | 220.0 | 0.364 | 0.589 | 0.103 | 0.222 | 0.254 | 0.609 |  |
| archived-20261006-175959: db.jsonl | 35728dddcf | 1.085 | 1.080 | 25,144 | 25,144 | 25,280 | 50,424 | 204.0 | 1.212 | 0.942 | 1.129 | 1.169 | 0.997 | 1.057 |  |
| archived-20261006-175959: db.jsonl | eef03e6a19 | 1.089 | 1.087 | 25,144 | 25,144 | 25,256 | 50,400 | 204.0 | 1.216 | 0.910 | 1.135 | 1.160 | 1.050 | 1.043 |  |
| archived-20261006-175959: db.jsonl | 0350ea6ee2 | 1.179 | 1.182 | 25,144 | 25,144 | 21,184 | 46,328 | 204.0 | 1.317 | 1.011 | 1.245 | 1.270 | 1.082 | 1.126 |  |

The front of all runs together (speed, binary + image, peak memory), by binary + image: cc0b1e2aeb 0.238 at 42,512, 216.0 KB, 436af85b80 0.249 at 41,849, 216.0 KB, 0bab7fed3e 0.256 at 41,805, 212.0 KB, 9517490eb3 0.257 at 41,798, 212.0 KB, 1a90a3e004 0.261 at 37,064, 212.0 KB, c57aebeb3e 0.271 at 36,634, 212.0 KB, 74ea2d2e27 0.299 at 36,626, 212.0 KB, 9fac496194 0.348 at 36,467, 212.0 KB, 570f49c26e 0.353 at 36,454, 212.0 KB, 775d8dda6e 0.357 at 36,443, 212.0 KB, 4daab7895a 0.428 at 33,086, 212.0 KB, d05d104578 0.430 at 32,746, 212.0 KB, 8f0973fc8f 0.433 at 32,554, 212.0 KB, 2a2c2b4256 0.455 at 32,538, 208.0 KB, 4542a08fb0 0.463 at 32,474, 212.0 KB, 2f4c1d82ec 0.549 at 32,336, 208.0 KB, 263788ab64 0.558 at 32,312, 208.0 KB, f69da4fcc8 0.601 at 32,299, 212.0 KB

Memory within 8 KB counts as a tie (EVOLVE_MEM_TOL).
On the front by memory alone: 0 of 18

## The same session on two CPUs

Calibration on cpu 2: 1.009; on cpu 8: 0.996.

Speed on cpu 2 over speed on cpu 8, per design: median 1.003, 10-90% 0.988-1.026, extremes 0.970-1.064; rank agreement (Spearman) 1.00.

The front of all runs on cpu 2: cc0b1e2aeb 0.238 at 42,512, 436af85b80 0.249 at 41,849, 0bab7fed3e 0.256 at 41,805, 9517490eb3 0.257 at 41,798, 1a90a3e004 0.261 at 37,064, c57aebeb3e 0.271 at 36,634, 74ea2d2e27 0.299 at 36,626, 9fac496194 0.348 at 36,467, 570f49c26e 0.353 at 36,454, 775d8dda6e 0.357 at 36,443, 4daab7895a 0.428 at 33,086, d05d104578 0.430 at 32,746, 8f0973fc8f 0.433 at 32,554, 2a2c2b4256 0.455 at 32,538, 4542a08fb0 0.463 at 32,474, 2f4c1d82ec 0.549 at 32,336, 263788ab64 0.558 at 32,312, f69da4fcc8 0.601 at 32,299

The front of all runs on cpu 8: 60c95fbea3 0.238 at 74,548, cc0b1e2aeb 0.244 at 42,512, 064ee4f23a 0.250 at 41,166, 76ab789fed 0.257 at 38,958, 1a90a3e004 0.264 at 37,064, c57aebeb3e 0.265 at 36,634, 74ea2d2e27 0.295 at 36,626, 9fac496194 0.352 at 36,467, 570f49c26e 0.352 at 36,454, 775d8dda6e 0.359 at 36,443, 4daab7895a 0.428 at 33,086, ae5d7cdaae 0.432 at 32,597, 8f0973fc8f 0.437 at 32,554, 2a2c2b4256 0.448 at 32,538, 4542a08fb0 0.454 at 32,474, 2f4c1d82ec 0.546 at 32,336, 263788ab64 0.557 at 32,312, f69da4fcc8 0.599 at 32,299

On both fronts: 14 of 18 and 18.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| cc0b1e2aeb | 0.238 | 0.244 | 0.978 |
| 60c95fbea3 | 0.244 | 0.238 | 1.026 |
| 44af4fb785 | 0.249 | 0.252 | 0.986 |
| 3a96a12236 | 0.249 | 0.248 | 1.003 |
| 436af85b80 | 0.249 | 0.251 | 0.994 |
| 4e3a904b8e | 0.252 | 0.255 | 0.989 |
| d60e3aab99 | 0.253 | 0.247 | 1.026 |
| cbbc5291f8 | 0.254 | 0.255 | 0.999 |
| 0bab7fed3e | 0.256 | 0.252 | 1.016 |
| 9517490eb3 | 0.257 | 0.256 | 1.003 |
| 1a90a3e004 | 0.261 | 0.264 | 0.986 |
| 76ab789fed | 0.263 | 0.257 | 1.020 |
| 064ee4f23a | 0.266 | 0.250 | 1.064 |
| bbab8560dd | 0.267 | 0.260 | 1.029 |
| 0cf9f1e76a | 0.269 | 0.268 | 1.004 |
| 773f6d9daf | 0.269 | 0.269 | 0.998 |
| c57aebeb3e | 0.271 | 0.265 | 1.023 |
| 272854107e | 0.272 | 0.276 | 0.987 |
| 69842b04ad | 0.273 | 0.273 | 0.999 |
| 7125b151e4 | 0.274 | 0.275 | 0.994 |
| 7670d35541 | 0.274 | 0.272 | 1.006 |
| ca2e692954 | 0.276 | 0.277 | 0.996 |
| 8298ca5d59 | 0.276 | 0.274 | 1.008 |
| 2bdab2950f | 0.277 | 0.278 | 0.996 |
| e076a00103 | 0.278 | 0.273 | 1.018 |
| 2117a45620 | 0.279 | 0.281 | 0.992 |
| 7075e8f2b1 | 0.280 | 0.273 | 1.026 |
| 1c4300cbbb | 0.281 | 0.285 | 0.984 |
| 416077aa2f | 0.281 | 0.278 | 1.012 |
| 98d7746633 | 0.281 | 0.271 | 1.038 |
| d1b2f540a8 | 0.283 | 0.281 | 1.007 |
| 2b55d23a18 | 0.283 | 0.275 | 1.028 |
| 343d881df1 | 0.286 | 0.285 | 1.003 |
| a36dc45e12 | 0.286 | 0.285 | 1.004 |
| c13c77dc7c | 0.288 | 0.286 | 1.004 |
| 7d7f1bf4fa | 0.292 | 0.295 | 0.990 |
| 4446c9069e | 0.294 | 0.295 | 0.995 |
| 4bb0870716 | 0.297 | 0.301 | 0.987 |
| 74ea2d2e27 | 0.299 | 0.295 | 1.016 |
| 38de166d54 | 0.300 | 0.294 | 1.020 |
| 2b7e66e1f3 | 0.301 | 0.297 | 1.012 |
| ccc8da3b12 | 0.301 | 0.301 | 1.002 |
| a03ef495f5 | 0.302 | 0.301 | 1.004 |
| 19104ead72 | 0.303 | 0.312 | 0.970 |
| 5671742b27 | 0.306 | 0.305 | 1.006 |
| 9f9c8fdb94 | 0.309 | 0.312 | 0.988 |
| 6583b9f742 | 0.318 | 0.306 | 1.041 |
| ce3a84b4a0 | 0.320 | 0.321 | 0.999 |
| ce2e13ce87 | 0.332 | 0.332 | 0.999 |
| 2b5e92dd57 | 0.332 | 0.332 | 1.001 |
| 9fac496194 | 0.348 | 0.352 | 0.990 |
| 570f49c26e | 0.353 | 0.352 | 1.004 |
| 775d8dda6e | 0.357 | 0.359 | 0.993 |
| eb0033be3d | 0.358 | 0.356 | 1.005 |
| b0a896c3c3 | 0.359 | 0.343 | 1.046 |
| 0f3d5dae58 | 0.361 | 0.360 | 1.002 |
| bfa7370096 | 0.368 | 0.371 | 0.992 |
| 9f9bfa4f49 | 0.368 | 0.366 | 1.006 |
| f1c82fbd44 | 0.369 | 0.373 | 0.988 |
| f48c2a5150 | 0.379 | 0.382 | 0.993 |
| 323f2ccfb8 | 0.383 | 0.381 | 1.005 |
| 9c2db9aebe | 0.385 | 0.384 | 1.002 |
| 7c49a5ffca | 0.386 | 0.387 | 0.998 |
| 51a8931db2 | 0.386 | 0.386 | 1.000 |
| 7f07a469cb | 0.389 | 0.377 | 1.031 |
| 31e4e22b2e | 0.389 | 0.384 | 1.014 |
| dac6ff750a | 0.390 | 0.394 | 0.988 |
| a170190b5a | 0.391 | 0.390 | 1.003 |
| a1578b537c | 0.392 | 0.388 | 1.011 |
| e6a3c1fb8c | 0.393 | 0.388 | 1.013 |
| 3405116655 | 0.397 | 0.386 | 1.028 |
| 2789713e31 | 0.401 | 0.394 | 1.015 |
| df2ac6c7ab | 0.402 | 0.399 | 1.006 |
| 0c5782b28a | 0.406 | 0.413 | 0.982 |
| 8a6365a3ff | 0.407 | 0.410 | 0.991 |
| 4ba5b2c147 | 0.409 | 0.410 | 0.998 |
| a1ff4b8022 | 0.409 | 0.408 | 1.004 |
| 1d44bcb8a5 | 0.410 | 0.412 | 0.995 |
| 69270766bd | 0.412 | 0.407 | 1.012 |
| 0df4c46cec | 0.421 | 0.420 | 1.004 |
| 29b1a365dc | 0.427 | 0.416 | 1.026 |
| 4daab7895a | 0.428 | 0.428 | 1.001 |
| d05d104578 | 0.430 | 0.433 | 0.993 |
| 8f0973fc8f | 0.433 | 0.437 | 0.992 |
| ae5d7cdaae | 0.434 | 0.432 | 1.004 |
| e570f69332 | 0.438 | 0.439 | 0.999 |
| 870c24c9cf | 0.439 | 0.439 | 0.999 |
| eabd014b0c | 0.442 | 0.448 | 0.986 |
| 301a268219 | 0.446 | 0.445 | 1.003 |
| 609b436e3a | 0.447 | 0.444 | 1.009 |
| b46a9c7ad4 | 0.448 | 0.448 | 0.998 |
| 0039591d51 | 0.448 | 0.444 | 1.009 |
| 63e3305540 | 0.449 | 0.445 | 1.010 |
| 03cf426d67 | 0.452 | 0.453 | 0.998 |
| 2a2c2b4256 | 0.455 | 0.448 | 1.016 |
| a808c92923 | 0.457 | 0.447 | 1.023 |
| 635a47fd26 | 0.458 | 0.459 | 0.997 |
| 4542a08fb0 | 0.463 | 0.454 | 1.018 |
| 740331292d | 0.465 | 0.464 | 1.004 |
| b00da878bf | 0.465 | 0.460 | 1.012 |
| d26dfdeda4 | 0.466 | 0.472 | 0.986 |
| 58c0a33fbe | 0.470 | 0.464 | 1.013 |
| 8252421ca2 | 0.482 | 0.481 | 1.003 |
| 0826d64cd9 | 0.498 | 0.499 | 0.998 |
| 3d312e796e | 0.499 | 0.489 | 1.020 |
| 2f4c1d82ec | 0.549 | 0.546 | 1.006 |
| f27cc3ce5a | 0.557 | 0.556 | 1.002 |
| 263788ab64 | 0.558 | 0.557 | 1.002 |
| 5c495fe0f3 | 0.569 | 0.568 | 1.001 |
| 4996bc41b8 | 0.573 | 0.581 | 0.987 |
| 776c86e476 | 0.578 | 0.576 | 1.003 |
| 844716c23e | 0.585 | 0.577 | 1.014 |
| f69da4fcc8 | 0.601 | 0.599 | 1.003 |
| 35728dddcf | 1.085 | 1.082 | 1.003 |
| eef03e6a19 | 1.089 | 1.089 | 1.000 |
| 0350ea6ee2 | 1.179 | 1.183 | 0.997 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 18 - Iteration 79: seed 20 and the newest four - the stop

`seed 20 tag2 then experiment compare-fronts.py --rounds 10 --cpus 2,8`,
commit bdc17b1e: seeds 16-20, 128 designs. **Calibration 1.000.** The
CPUs: median 1.001, 10-90% 0.990-1.019, ranks 1.00. **The front of all
runs: 32, by memory alone 0** - 16 of seed 20, 11 of seed 19, 5 of seed
18. Seed 20 small (fastest none, smallest total 0.0%, memory none): the
second small run in a row - evolution stops (Iteration 79).

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 1.000** (kernel 1.005, fib 0.997, parse 1.002, corpus 1.003, loop 0.992, sieve 0.995).

| run | design | speed now | recorded | size now | recorded | binary | binary + image | memory KB | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | f932112676 | 0.608 | 0.612 | 7,019 | 7,019 | 25,280 | 32,299 | 216.0 | 0.574 | 1.140 | 0.237 | 0.405 | 1.318 | 1.096 |  |
| this clone: db.jsonl | 4add88f6fb | 0.558 | 0.558 | 7,032 | 7,032 | 25,280 | 32,312 | 208.0 | 0.510 | 1.207 | 0.210 | 0.333 | 1.253 | 1.064 |  |
| this clone: db.jsonl | 4e378cc12e | 0.553 | 0.550 | 7,056 | 7,056 | 25,280 | 32,336 | 208.0 | 0.515 | 1.105 | 0.212 | 0.334 | 1.286 | 1.068 |  |
| this clone: db.jsonl | 9133d8167a | 0.374 | 0.361 | 7,084 | 7,084 | 29,352 | 36,436 | 212.0 | 0.393 | 0.645 | 0.111 | 0.235 | 1.113 | 0.932 | yes |
| this clone: db.jsonl | 7887b32787 | 0.484 | 0.486 | 7,084 | 7,084 | 25,280 | 32,364 | 216.0 | 0.491 | 1.101 | 0.138 | 0.283 | 1.266 | 1.096 | yes |
| this clone: db.jsonl | 21e8b873fe | 0.361 | 0.346 | 7,089 | 7,089 | 29,352 | 36,441 | 216.0 | 0.353 | 0.663 | 0.107 | 0.239 | 1.024 | 0.841 | yes |
| this clone: db.jsonl | 75c9affa70 | 0.364 | 0.352 | 7,091 | 7,091 | 29,352 | 36,443 | 212.0 | 0.411 | 0.622 | 0.112 | 0.249 | 0.897 | 0.859 |  |
| this clone: db.jsonl | 83098a32c7 | 0.497 | 0.504 | 7,092 | 7,092 | 25,280 | 32,372 | 216.0 | 0.487 | 1.229 | 0.136 | 0.288 | 1.302 | 1.141 |  |
| this clone: db.jsonl | ea57db4076 | 0.362 | 0.356 | 7,102 | 7,102 | 29,352 | 36,454 | 212.0 | 0.390 | 0.608 | 0.102 | 0.242 | 1.058 | 0.896 |  |
| this clone: db.jsonl | d53d76f7db | 0.481 | 0.480 | 7,105 | 7,105 | 25,280 | 32,385 | 216.0 | 0.488 | 1.098 | 0.138 | 0.292 | 1.190 | 1.097 | yes |
| this clone: db.jsonl | 47da731a5c | 0.476 | 0.481 | 7,109 | 7,109 | 25,280 | 32,389 | 216.0 | 0.476 | 1.103 | 0.138 | 0.286 | 1.187 | 1.084 | yes |
| this clone: db.jsonl | f362a1bba0 | 0.486 | 0.492 | 7,110 | 7,110 | 25,280 | 32,390 | 216.0 | 0.487 | 1.130 | 0.135 | 0.285 | 1.288 | 1.082 |  |
| this clone: db.jsonl | 3e50dc7ea6 | 0.342 | 0.329 | 7,130 | 7,130 | 29,352 | 36,482 | 216.0 | 0.355 | 0.577 | 0.104 | 0.232 | 0.945 | 0.839 | yes |
| this clone: db.jsonl | 8581dba4f7 | 0.342 | 0.333 | 7,156 | 7,156 | 29,352 | 36,508 | 216.0 | 0.348 | 0.656 | 0.099 | 0.222 | 0.939 | 0.833 |  |
| this clone: db.jsonl | 735b92ad53 | 0.449 | 0.441 | 7,240 | 7,240 | 25,280 | 32,520 | 212.0 | 0.536 | 1.137 | 0.222 | 0.345 | 0.393 | 0.765 | yes |
| this clone: db.jsonl | a78522d7eb | 0.442 | 0.434 | 7,242 | 7,242 | 25,280 | 32,522 | 212.0 | 0.511 | 1.115 | 0.218 | 0.335 | 0.403 | 0.732 | yes |
| this clone: db.jsonl | 58159e130b | 0.305 | 0.299 | 7,250 | 7,250 | 29,352 | 36,602 | 216.0 | 0.418 | 0.673 | 0.120 | 0.268 | 0.289 | 0.587 | yes |
| this clone: db.jsonl | 7bdcdc8f27 | 0.440 | 0.447 | 7,250 | 7,250 | 25,280 | 32,530 | 212.0 | 0.543 | 1.037 | 0.228 | 0.353 | 0.364 | 0.725 | yes |
| this clone: db.jsonl | ed94bd7e99 | 0.406 | 0.402 | 7,266 | 7,266 | 25,280 | 32,546 | 216.0 | 0.516 | 1.188 | 0.144 | 0.285 | 0.440 | 0.765 | yes |
| this clone: db.jsonl | e5ddcbb6a5 | 0.298 | 0.267 | 7,274 | 7,274 | 29,352 | 36,626 | 212.0 | 0.405 | 0.491 | 0.175 | 0.286 | 0.238 | 0.570 | yes |
| this clone: db.jsonl | 7ab7315744 | 0.292 | 0.278 | 7,282 | 7,282 | 29,352 | 36,634 | 212.0 | 0.373 | 0.877 | 0.102 | 0.221 | 0.287 | 0.586 |  |
| this clone: db.jsonl | 06d1f9d029 | 0.269 | 0.262 | 7,346 | 7,346 | 29,352 | 36,698 | 216.0 | 0.365 | 0.634 | 0.111 | 0.221 | 0.247 | 0.579 | yes |
| this clone: db.jsonl | d35040fd68 | 0.403 | 0.400 | 7,348 | 7,348 | 25,280 | 32,628 | 216.0 | 0.516 | 1.166 | 0.138 | 0.284 | 0.452 | 0.784 | yes |
| this clone: db.jsonl | 8bbe1dad41 | 0.264 | 0.259 | 7,685 | 7,685 | 29,352 | 37,037 | 216.0 | 0.345 | 0.571 | 0.106 | 0.227 | 0.268 | 0.607 | yes |
| this clone: db.jsonl | 8637e4c37e | 0.267 | 0.268 | 7,685 | 7,685 | 29,376 | 37,061 | 216.0 | 0.353 | 0.556 | 0.108 | 0.235 | 0.270 | 0.568 |  |
| this clone: db.jsonl | 8162560177 | 0.393 | 0.384 | 7,686 | 7,686 | 25,280 | 32,966 | 216.0 | 0.480 | 1.113 | 0.138 | 0.273 | 0.464 | 0.725 | yes |
| this clone: db.jsonl | 7e91afe735 | 0.395 | 0.386 | 8,002 | 8,002 | 25,280 | 33,282 | 216.0 | 0.520 | 1.088 | 0.139 | 0.277 | 0.442 | 0.757 |  |
| archived-20261006-160616: db.jsonl | 0826d64cd9 | 0.501 | 0.415 | 7,009 | 7,009 | 33,448 | 40,457 | 216.0 | 0.527 | 0.761 | 0.196 | 0.365 | 1.104 | 0.916 |  |
| archived-20261006-160616: db.jsonl | 69270766bd | 0.409 | 0.366 | 7,049 | 7,049 | 33,448 | 40,497 | 216.0 | 0.427 | 0.761 | 0.120 | 0.272 | 1.085 | 0.929 |  |
| archived-20261006-160616: db.jsonl | df2ac6c7ab | 0.401 | 0.336 | 7,050 | 7,050 | 37,544 | 44,594 | 216.0 | 0.440 | 0.672 | 0.125 | 0.270 | 1.036 | 0.877 |  |
| archived-20261006-160616: db.jsonl | 323f2ccfb8 | 0.381 | 0.337 | 7,105 | 7,105 | 37,544 | 44,649 | 216.0 | 0.377 | 0.771 | 0.107 | 0.234 | 1.112 | 0.944 |  |
| archived-20261006-160616: db.jsonl | 7c49a5ffca | 0.387 | 0.333 | 7,123 | 7,123 | 37,544 | 44,667 | 212.0 | 0.386 | 0.813 | 0.110 | 0.239 | 1.053 | 0.908 |  |
| archived-20261006-160616: db.jsonl | 2b5e92dd57 | 0.334 | 0.336 | 7,186 | 7,186 | 62,120 | 69,306 | 232.0 | 0.497 | 0.655 | 0.193 | 0.331 | 0.200 | 0.580 |  |
| archived-20261006-160616: db.jsonl | bfa7370096 | 0.368 | 0.339 | 7,202 | 7,202 | 66,216 | 73,418 | 232.0 | 0.356 | 0.863 | 0.101 | 0.232 | 0.931 | 0.849 |  |
| archived-20261006-160616: db.jsonl | 19104ead72 | 0.305 | 0.301 | 7,225 | 7,225 | 66,216 | 73,441 | 232.0 | 0.415 | 0.855 | 0.116 | 0.274 | 0.233 | 0.592 |  |
| archived-20261006-160616: db.jsonl | 4bb0870716 | 0.287 | 0.256 | 7,226 | 7,226 | 37,544 | 44,770 | 216.0 | 0.453 | 0.675 | 0.125 | 0.268 | 0.192 | 0.600 |  |
| archived-20261006-160616: db.jsonl | 4446c9069e | 0.295 | 0.251 | 7,274 | 7,274 | 33,448 | 40,722 | 216.0 | 0.432 | 0.635 | 0.115 | 0.248 | 0.287 | 0.610 |  |
| archived-20261006-160616: db.jsonl | 343d881df1 | 0.286 | 0.237 | 7,708 | 7,708 | 37,544 | 45,252 | 212.0 | 0.398 | 0.675 | 0.110 | 0.234 | 0.275 | 0.616 |  |
| archived-20261006-170257: db.jsonl | 3d312e796e | 0.500 | 0.419 | 7,009 | 7,009 | 33,448 | 40,457 | 216.0 | 0.527 | 0.763 | 0.197 | 0.358 | 1.102 | 0.925 |  |
| archived-20261006-170257: db.jsonl | a1ff4b8022 | 0.405 | 0.388 | 7,043 | 7,043 | 33,448 | 40,491 | 216.0 | 0.431 | 0.698 | 0.125 | 0.269 | 1.078 | 0.894 |  |
| archived-20261006-170257: db.jsonl | 3405116655 | 0.394 | 0.353 | 7,049 | 7,049 | 37,544 | 44,593 | 212.0 | 0.426 | 0.673 | 0.121 | 0.274 | 0.993 | 0.865 |  |
| archived-20261006-170257: db.jsonl | 4ba5b2c147 | 0.407 | 0.338 | 7,057 | 7,057 | 33,448 | 40,505 | 216.0 | 0.433 | 0.720 | 0.122 | 0.270 | 1.092 | 0.892 |  |
| archived-20261006-170257: db.jsonl | 0c5782b28a | 0.411 | 0.343 | 7,073 | 7,073 | 33,448 | 40,521 | 216.0 | 0.430 | 0.725 | 0.123 | 0.272 | 1.124 | 0.868 |  |
| archived-20261006-170257: db.jsonl | 31e4e22b2e | 0.387 | 0.343 | 7,085 | 7,085 | 33,448 | 40,533 | 216.0 | 0.418 | 0.632 | 0.114 | 0.252 | 1.140 | 0.962 |  |
| archived-20261006-170257: db.jsonl | a1578b537c | 0.386 | 0.334 | 7,120 | 7,120 | 37,544 | 44,664 | 216.0 | 0.375 | 0.796 | 0.110 | 0.231 | 1.131 | 0.942 |  |
| archived-20261006-170257: db.jsonl | e6a3c1fb8c | 0.389 | 0.318 | 7,130 | 7,130 | 37,544 | 44,674 | 212.0 | 0.375 | 0.816 | 0.112 | 0.237 | 1.099 | 0.932 |  |
| archived-20261006-170257: db.jsonl | ce3a84b4a0 | 0.318 | 0.307 | 7,217 | 7,217 | 33,448 | 40,665 | 216.0 | 0.440 | 0.802 | 0.121 | 0.263 | 0.289 | 0.595 |  |
| archived-20261006-170257: db.jsonl | 6583b9f742 | 0.311 | 0.277 | 7,218 | 7,218 | 37,544 | 44,762 | 216.0 | 0.444 | 0.783 | 0.124 | 0.246 | 0.274 | 0.646 |  |
| archived-20261006-170257: db.jsonl | 2b7e66e1f3 | 0.289 | 0.260 | 7,226 | 7,226 | 37,544 | 44,770 | 216.0 | 0.447 | 0.676 | 0.124 | 0.228 | 0.234 | 0.605 |  |
| archived-20261006-170257: db.jsonl | 38de166d54 | 0.295 | 0.267 | 7,234 | 7,234 | 37,544 | 44,778 | 216.0 | 0.456 | 0.656 | 0.126 | 0.265 | 0.224 | 0.619 |  |
| archived-20261006-170257: db.jsonl | 2b55d23a18 | 0.283 | 0.251 | 7,266 | 7,266 | 66,216 | 73,482 | 232.0 | 0.355 | 0.838 | 0.103 | 0.227 | 0.262 | 0.563 |  |
| archived-20261006-170257: db.jsonl | a36dc45e12 | 0.284 | 0.235 | 7,283 | 7,283 | 37,544 | 44,827 | 212.0 | 0.391 | 0.698 | 0.113 | 0.237 | 0.254 | 0.627 |  |
| archived-20261006-170257: db.jsonl | 5671742b27 | 0.305 | 0.234 | 7,690 | 7,690 | 37,544 | 45,234 | 212.0 | 0.383 | 0.880 | 0.111 | 0.235 | 0.300 | 0.643 |  |
| archived-20261006-175959: db.jsonl | 4996bc41b8 | 0.581 | 0.586 | 7,051 | 7,051 | 25,280 | 32,331 | 208.0 | 0.560 | 1.216 | 0.224 | 0.365 | 1.193 | 1.075 |  |
| archived-20261006-175959: db.jsonl | 844716c23e | 0.585 | 0.589 | 7,051 | 7,051 | 25,280 | 32,331 | 208.0 | 0.574 | 1.209 | 0.224 | 0.364 | 1.212 | 1.061 |  |
| archived-20261006-175959: db.jsonl | 776c86e476 | 0.576 | 0.574 | 7,059 | 7,059 | 25,280 | 32,339 | 208.0 | 0.566 | 1.138 | 0.225 | 0.367 | 1.194 | 1.066 |  |
| archived-20261006-175959: db.jsonl | 5c495fe0f3 | 0.569 | 0.568 | 7,090 | 7,090 | 25,280 | 32,370 | 212.0 | 0.552 | 1.158 | 0.226 | 0.363 | 1.146 | 1.036 |  |
| archived-20261006-175959: db.jsonl | f27cc3ce5a | 0.557 | 0.559 | 7,108 | 7,108 | 25,280 | 32,388 | 212.0 | 0.534 | 1.114 | 0.223 | 0.345 | 1.173 | 1.032 |  |
| archived-20261006-175959: db.jsonl | 51a8931db2 | 0.390 | 0.385 | 7,115 | 7,115 | 29,352 | 36,467 | 212.0 | 0.382 | 0.789 | 0.112 | 0.238 | 1.120 | 0.939 |  |
| archived-20261006-175959: db.jsonl | 4542a08fb0 | 0.465 | 0.466 | 7,194 | 7,194 | 25,280 | 32,474 | 212.0 | 0.599 | 1.091 | 0.230 | 0.368 | 0.394 | 0.728 | yes |
| archived-20261006-175959: db.jsonl | 8252421ca2 | 0.481 | 0.482 | 7,194 | 7,194 | 25,280 | 32,474 | 208.0 | 0.605 | 1.140 | 0.235 | 0.400 | 0.395 | 0.736 |  |
| archived-20261006-175959: db.jsonl | 8a6365a3ff | 0.405 | 0.406 | 7,217 | 7,217 | 29,376 | 36,593 | 212.0 | 0.533 | 1.102 | 0.146 | 0.278 | 0.457 | 0.743 |  |
| archived-20261006-175959: db.jsonl | 2789713e31 | 0.391 | 0.398 | 7,242 | 7,242 | 29,376 | 36,618 | 208.0 | 0.503 | 1.093 | 0.151 | 0.296 | 0.373 | 0.751 |  |
| archived-20261006-175959: db.jsonl | d26dfdeda4 | 0.466 | 0.461 | 7,250 | 7,250 | 25,280 | 32,530 | 208.0 | 0.576 | 1.144 | 0.232 | 0.362 | 0.395 | 0.727 |  |
| archived-20261006-175959: db.jsonl | dac6ff750a | 0.391 | 0.392 | 7,258 | 7,258 | 29,376 | 36,634 | 208.0 | 0.521 | 1.006 | 0.155 | 0.300 | 0.376 | 0.718 |  |
| archived-20261006-175959: db.jsonl | 2a2c2b4256 | 0.452 | 0.457 | 7,258 | 7,258 | 25,280 | 32,538 | 208.0 | 0.573 | 1.118 | 0.224 | 0.355 | 0.372 | 0.735 |  |
| archived-20261006-175959: db.jsonl | e570f69332 | 0.441 | 0.434 | 7,274 | 7,274 | 25,280 | 32,554 | 216.0 | 0.515 | 1.125 | 0.222 | 0.329 | 0.394 | 0.725 |  |
| archived-20261006-175959: db.jsonl | f48c2a5150 | 0.378 | 0.377 | 7,276 | 7,276 | 29,376 | 36,652 | 212.0 | 0.398 | 0.945 | 0.203 | 0.298 | 0.338 | 0.667 |  |
| archived-20261006-175959: db.jsonl | a170190b5a | 0.398 | 0.386 | 7,298 | 7,298 | 29,376 | 36,674 | 208.0 | 0.527 | 1.168 | 0.149 | 0.284 | 0.386 | 0.728 |  |
| archived-20261006-175959: db.jsonl | 2117a45620 | 0.282 | 0.274 | 7,307 | 7,307 | 33,448 | 40,755 | 216.0 | 0.421 | 0.499 | 0.116 | 0.268 | 0.274 | 0.525 |  |
| archived-20261006-175959: db.jsonl | 4e3a904b8e | 0.254 | 0.255 | 7,323 | 7,323 | 62,128 | 69,451 | 232.0 | 0.371 | 0.594 | 0.105 | 0.240 | 0.191 | 0.531 |  |
| archived-20261006-175959: db.jsonl | 69842b04ad | 0.268 | 0.268 | 7,323 | 7,323 | 33,448 | 40,771 | 216.0 | 0.390 | 0.690 | 0.104 | 0.214 | 0.229 | 0.610 |  |
| archived-20261006-175959: db.jsonl | 609b436e3a | 0.445 | 0.450 | 7,329 | 7,329 | 25,280 | 32,609 | 212.0 | 0.565 | 1.059 | 0.220 | 0.362 | 0.368 | 0.711 |  |
| archived-20261006-175959: db.jsonl | 0f3d5dae58 | 0.357 | 0.352 | 7,331 | 7,331 | 29,376 | 36,707 | 216.0 | 0.465 | 0.947 | 0.131 | 0.252 | 0.402 | 0.731 |  |
| archived-20261006-175959: db.jsonl | bbab8560dd | 0.263 | 0.261 | 7,338 | 7,338 | 33,448 | 40,786 | 216.0 | 0.379 | 0.546 | 0.097 | 0.227 | 0.278 | 0.532 |  |
| archived-20261006-175959: db.jsonl | 1c4300cbbb | 0.281 | 0.285 | 7,338 | 7,338 | 33,448 | 40,786 | 216.0 | 0.406 | 0.668 | 0.100 | 0.236 | 0.271 | 0.600 |  |
| archived-20261006-175959: db.jsonl | c13c77dc7c | 0.286 | 0.286 | 7,339 | 7,339 | 33,472 | 40,811 | 208.0 | 0.386 | 0.659 | 0.110 | 0.234 | 0.291 | 0.629 |  |
| archived-20261006-175959: db.jsonl | b0a896c3c3 | 0.361 | 0.358 | 7,347 | 7,347 | 29,376 | 36,723 | 216.0 | 0.460 | 1.046 | 0.127 | 0.256 | 0.391 | 0.751 |  |
| archived-20261006-175959: db.jsonl | 416077aa2f | 0.284 | 0.272 | 7,349 | 7,349 | 33,448 | 40,797 | 212.0 | 0.379 | 0.748 | 0.111 | 0.242 | 0.240 | 0.590 |  |
| archived-20261006-175959: db.jsonl | 0cf9f1e76a | 0.265 | 0.265 | 7,365 | 7,365 | 62,128 | 69,493 | 232.0 | 0.404 | 0.717 | 0.107 | 0.228 | 0.184 | 0.578 |  |
| archived-20261006-175959: db.jsonl | 740331292d | 0.464 | 0.467 | 7,505 | 7,505 | 25,280 | 32,785 | 208.0 | 0.575 | 1.109 | 0.225 | 0.361 | 0.413 | 0.723 |  |
| archived-20261006-175959: db.jsonl | 03cf426d67 | 0.451 | 0.448 | 7,539 | 7,539 | 25,280 | 32,819 | 208.0 | 0.525 | 1.210 | 0.226 | 0.342 | 0.382 | 0.781 |  |
| archived-20261006-175959: db.jsonl | a03ef495f5 | 0.301 | 0.301 | 7,644 | 7,644 | 29,352 | 36,996 | 216.0 | 0.406 | 0.780 | 0.108 | 0.259 | 0.279 | 0.570 |  |
| archived-20261006-175959: db.jsonl | 63e3305540 | 0.449 | 0.438 | 7,664 | 7,664 | 25,280 | 32,944 | 212.0 | 0.532 | 1.191 | 0.219 | 0.340 | 0.388 | 0.722 |  |
| archived-20261006-175959: db.jsonl | 0039591d51 | 0.443 | 0.442 | 7,675 | 7,675 | 25,280 | 32,955 | 212.0 | 0.575 | 1.088 | 0.222 | 0.347 | 0.353 | 0.728 |  |
| archived-20261006-175959: db.jsonl | b46a9c7ad4 | 0.447 | 0.447 | 7,677 | 7,677 | 25,280 | 32,957 | 208.0 | 0.563 | 1.043 | 0.223 | 0.348 | 0.392 | 0.738 |  |
| archived-20261006-175959: db.jsonl | 301a268219 | 0.446 | 0.444 | 7,683 | 7,683 | 25,280 | 32,963 | 212.0 | 0.526 | 1.161 | 0.218 | 0.337 | 0.394 | 0.733 |  |
| archived-20261006-175959: db.jsonl | a808c92923 | 0.455 | 0.456 | 7,698 | 7,698 | 25,280 | 32,978 | 208.0 | 0.597 | 1.105 | 0.223 | 0.367 | 0.362 | 0.740 |  |
| archived-20261006-175959: db.jsonl | 7d7f1bf4fa | 0.292 | 0.291 | 7,707 | 7,707 | 29,352 | 37,059 | 212.0 | 0.392 | 0.781 | 0.110 | 0.231 | 0.272 | 0.608 |  |
| archived-20261006-175959: db.jsonl | 064ee4f23a | 0.266 | 0.263 | 7,718 | 7,718 | 33,448 | 41,166 | 212.0 | 0.401 | 0.559 | 0.110 | 0.242 | 0.224 | 0.604 |  |
| archived-20261006-175959: db.jsonl | 7075e8f2b1 | 0.272 | 0.278 | 7,738 | 7,738 | 33,448 | 41,186 | 208.0 | 0.364 | 0.680 | 0.110 | 0.222 | 0.249 | 0.579 |  |
| archived-20261006-175959: db.jsonl | ca2e692954 | 0.276 | 0.273 | 7,738 | 7,738 | 33,448 | 41,186 | 208.0 | 0.365 | 0.767 | 0.106 | 0.224 | 0.240 | 0.611 |  |
| archived-20261006-175959: db.jsonl | 9f9c8fdb94 | 0.309 | 0.310 | 7,744 | 7,744 | 33,448 | 41,192 | 208.0 | 0.429 | 0.785 | 0.109 | 0.244 | 0.315 | 0.628 |  |
| archived-20261006-175959: db.jsonl | ccc8da3b12 | 0.303 | 0.300 | 7,759 | 7,759 | 33,448 | 41,207 | 208.0 | 0.404 | 0.552 | 0.106 | 0.253 | 0.423 | 0.692 |  |
| archived-20261006-175959: db.jsonl | e076a00103 | 0.275 | 0.274 | 7,783 | 7,783 | 29,352 | 37,135 | 216.0 | 0.394 | 0.633 | 0.110 | 0.228 | 0.248 | 0.611 |  |
| archived-20261006-175959: db.jsonl | 2bdab2950f | 0.276 | 0.278 | 7,783 | 7,783 | 29,352 | 37,135 | 216.0 | 0.398 | 0.632 | 0.113 | 0.227 | 0.249 | 0.618 |  |
| archived-20261006-175959: db.jsonl | 7f07a469cb | 0.388 | 0.390 | 7,801 | 7,801 | 29,376 | 37,177 | 208.0 | 0.521 | 1.186 | 0.138 | 0.279 | 0.369 | 0.764 |  |
| archived-20261006-175959: db.jsonl | 4daab7895a | 0.427 | 0.425 | 7,806 | 7,806 | 25,280 | 33,086 | 212.0 | 0.519 | 1.082 | 0.215 | 0.325 | 0.361 | 0.723 |  |
| archived-20261006-175959: db.jsonl | 7125b151e4 | 0.272 | 0.273 | 7,970 | 7,970 | 33,448 | 41,418 | 212.0 | 0.385 | 0.605 | 0.102 | 0.239 | 0.262 | 0.589 |  |
| archived-20261006-175959: db.jsonl | 60c95fbea3 | 0.243 | 0.239 | 8,332 | 8,332 | 66,216 | 74,548 | 232.0 | 0.383 | 0.427 | 0.103 | 0.236 | 0.211 | 0.544 | yes |
| archived-20261006-175959: db.jsonl | 9517490eb3 | 0.258 | 0.258 | 8,350 | 8,350 | 33,448 | 41,798 | 212.0 | 0.385 | 0.600 | 0.108 | 0.239 | 0.194 | 0.602 | yes |
| archived-20261006-175959: db.jsonl | 0bab7fed3e | 0.252 | 0.252 | 8,357 | 8,357 | 33,448 | 41,805 | 212.0 | 0.382 | 0.598 | 0.106 | 0.227 | 0.184 | 0.612 | yes |
| archived-20261006-175959: db.jsonl | 436af85b80 | 0.247 | 0.249 | 8,401 | 8,401 | 33,448 | 41,849 | 216.0 | 0.386 | 0.511 | 0.108 | 0.246 | 0.175 | 0.486 | yes |
| archived-20261006-175959: db.jsonl | 44af4fb785 | 0.250 | 0.252 | 9,413 | 9,413 | 33,448 | 42,861 | 212.0 | 0.375 | 0.597 | 0.105 | 0.230 | 0.180 | 0.606 |  |
| archived-20261006-175959: db.jsonl | 98d7746633 | 0.282 | 0.282 | 9,598 | 9,598 | 29,352 | 38,950 | 216.0 | 0.386 | 0.647 | 0.108 | 0.230 | 0.287 | 0.660 |  |
| archived-20261006-175959: db.jsonl | 76ab789fed | 0.263 | 0.264 | 9,606 | 9,606 | 29,352 | 38,958 | 220.0 | 0.365 | 0.601 | 0.100 | 0.225 | 0.254 | 0.615 |  |
| archived-20261006-175959: db.jsonl | 35728dddcf | 1.077 | 1.080 | 25,144 | 25,144 | 25,280 | 50,424 | 204.0 | 1.205 | 0.968 | 1.114 | 1.128 | 0.989 | 1.076 |  |
| archived-20261006-175959: db.jsonl | eef03e6a19 | 1.088 | 1.087 | 25,144 | 25,144 | 25,256 | 50,400 | 204.0 | 1.213 | 0.908 | 1.139 | 1.160 | 1.048 | 1.048 |  |
| archived-20261006-175959: db.jsonl | 0350ea6ee2 | 1.186 | 1.182 | 25,144 | 25,144 | 21,184 | 46,328 | 204.0 | 1.338 | 1.009 | 1.255 | 1.278 | 1.085 | 1.144 |  |
| archived-20261006-185037: db.jsonl | f69da4fcc8 | 0.600 | 0.605 | 7,019 | 7,019 | 25,280 | 32,299 | 212.0 | 0.580 | 1.101 | 0.240 | 0.396 | 1.280 | 1.087 | yes |
| archived-20261006-185037: db.jsonl | 263788ab64 | 0.552 | 0.561 | 7,032 | 7,032 | 25,280 | 32,312 | 208.0 | 0.494 | 1.213 | 0.209 | 0.328 | 1.249 | 1.055 | yes |
| archived-20261006-185037: db.jsonl | 2f4c1d82ec | 0.548 | 0.541 | 7,056 | 7,056 | 25,280 | 32,336 | 208.0 | 0.503 | 1.100 | 0.210 | 0.340 | 1.256 | 1.051 | yes |
| archived-20261006-185037: db.jsonl | 775d8dda6e | 0.360 | 0.357 | 7,091 | 7,091 | 29,352 | 36,443 | 212.0 | 0.353 | 0.662 | 0.110 | 0.239 | 0.987 | 0.851 | yes |
| archived-20261006-185037: db.jsonl | 570f49c26e | 0.351 | 0.350 | 7,102 | 7,102 | 29,352 | 36,454 | 212.0 | 0.361 | 0.606 | 0.097 | 0.226 | 1.114 | 0.895 | yes |
| archived-20261006-185037: db.jsonl | 9fac496194 | 0.349 | 0.347 | 7,115 | 7,115 | 29,352 | 36,467 | 212.0 | 0.356 | 0.623 | 0.099 | 0.228 | 1.034 | 0.835 | yes |
| archived-20261006-185037: db.jsonl | b00da878bf | 0.463 | 0.469 | 7,210 | 7,210 | 25,280 | 32,490 | 216.0 | 0.566 | 1.109 | 0.231 | 0.372 | 0.394 | 0.715 | yes |
| archived-20261006-185037: db.jsonl | 635a47fd26 | 0.456 | 0.448 | 7,260 | 7,260 | 25,280 | 32,540 | 208.0 | 0.573 | 1.104 | 0.222 | 0.352 | 0.399 | 0.730 |  |
| archived-20261006-185037: db.jsonl | 74ea2d2e27 | 0.299 | 0.304 | 7,274 | 7,274 | 29,352 | 36,626 | 212.0 | 0.413 | 0.499 | 0.172 | 0.290 | 0.230 | 0.570 |  |
| archived-20261006-185037: db.jsonl | 8f0973fc8f | 0.435 | 0.438 | 7,274 | 7,274 | 25,280 | 32,554 | 212.0 | 0.514 | 1.100 | 0.217 | 0.327 | 0.390 | 0.690 |  |
| archived-20261006-185037: db.jsonl | c57aebeb3e | 0.275 | 0.277 | 7,282 | 7,282 | 29,352 | 36,634 | 212.0 | 0.363 | 0.604 | 0.106 | 0.233 | 0.289 | 0.579 | yes |
| archived-20261006-185037: db.jsonl | 272854107e | 0.274 | 0.275 | 7,290 | 7,290 | 29,352 | 36,642 | 212.0 | 0.370 | 0.668 | 0.104 | 0.224 | 0.269 | 0.608 | yes |
| archived-20261006-185037: db.jsonl | ae5d7cdaae | 0.434 | 0.434 | 7,317 | 7,317 | 25,280 | 32,597 | 212.0 | 0.528 | 1.141 | 0.214 | 0.323 | 0.369 | 0.725 |  |
| archived-20261006-185037: db.jsonl | d05d104578 | 0.431 | 0.436 | 7,466 | 7,466 | 25,280 | 32,746 | 212.0 | 0.488 | 1.097 | 0.219 | 0.320 | 0.397 | 0.701 |  |
| archived-20261006-185037: db.jsonl | 870c24c9cf | 0.438 | 0.440 | 7,632 | 7,632 | 25,280 | 32,912 | 212.0 | 0.509 | 1.130 | 0.215 | 0.323 | 0.405 | 0.715 |  |
| archived-20261006-185037: db.jsonl | 7670d35541 | 0.274 | 0.273 | 7,682 | 7,682 | 29,352 | 37,034 | 212.0 | 0.403 | 0.555 | 0.106 | 0.233 | 0.283 | 0.620 |  |
| archived-20261006-185037: db.jsonl | 1a90a3e004 | 0.260 | 0.257 | 7,712 | 7,712 | 29,352 | 37,064 | 212.0 | 0.357 | 0.610 | 0.104 | 0.220 | 0.237 | 0.514 | yes |
| archived-20261006-185037: db.jsonl | cc0b1e2aeb | 0.247 | 0.241 | 9,064 | 9,064 | 33,448 | 42,512 | 216.0 | 0.355 | 0.562 | 0.105 | 0.236 | 0.187 | 0.498 | yes |
| archived-20261006-185037: db.jsonl | d60e3aab99 | 0.251 | 0.253 | 9,064 | 9,064 | 37,544 | 46,608 | 216.0 | 0.355 | 0.606 | 0.104 | 0.228 | 0.197 | 0.514 |  |

The front of all runs together (speed, binary + image, peak memory), by binary + image: 60c95fbea3 0.243 at 74,548, 232.0 KB, cc0b1e2aeb 0.247 at 42,512, 216.0 KB, 436af85b80 0.247 at 41,849, 216.0 KB, 0bab7fed3e 0.252 at 41,805, 212.0 KB, 9517490eb3 0.258 at 41,798, 212.0 KB, 1a90a3e004 0.260 at 37,064, 212.0 KB, 8bbe1dad41 0.264 at 37,037, 216.0 KB, 06d1f9d029 0.269 at 36,698, 216.0 KB, 272854107e 0.274 at 36,642, 212.0 KB, c57aebeb3e 0.275 at 36,634, 212.0 KB, e5ddcbb6a5 0.298 at 36,626, 212.0 KB, 58159e130b 0.305 at 36,602, 216.0 KB, 3e50dc7ea6 0.342 at 36,482, 216.0 KB, 9fac496194 0.349 at 36,467, 212.0 KB, 570f49c26e 0.351 at 36,454, 212.0 KB, 775d8dda6e 0.360 at 36,443, 212.0 KB, 21e8b873fe 0.361 at 36,441, 216.0 KB, 9133d8167a 0.374 at 36,436, 212.0 KB, 8162560177 0.393 at 32,966, 216.0 KB, d35040fd68 0.403 at 32,628, 216.0 KB, ed94bd7e99 0.406 at 32,546, 216.0 KB, 7bdcdc8f27 0.440 at 32,530, 212.0 KB, a78522d7eb 0.442 at 32,522, 212.0 KB, 735b92ad53 0.449 at 32,520, 212.0 KB, b00da878bf 0.463 at 32,490, 216.0 KB, 4542a08fb0 0.465 at 32,474, 212.0 KB, 47da731a5c 0.476 at 32,389, 216.0 KB, d53d76f7db 0.481 at 32,385, 216.0 KB, 7887b32787 0.484 at 32,364, 216.0 KB, 2f4c1d82ec 0.548 at 32,336, 208.0 KB, 263788ab64 0.552 at 32,312, 208.0 KB, f69da4fcc8 0.600 at 32,299, 212.0 KB

Memory within 8 KB counts as a tie (EVOLVE_MEM_TOL).
On the front by memory alone: 0 of 32

## The same session on two CPUs

Calibration on cpu 2: 1.000; on cpu 8: 1.004.

Speed on cpu 2 over speed on cpu 8, per design: median 1.001, 10-90% 0.990-1.019, extremes 0.971-1.052; rank agreement (Spearman) 1.00.

The front of all runs on cpu 2: 60c95fbea3 0.243 at 74,548, cc0b1e2aeb 0.247 at 42,512, 436af85b80 0.247 at 41,849, 0bab7fed3e 0.252 at 41,805, 9517490eb3 0.258 at 41,798, 1a90a3e004 0.260 at 37,064, 8bbe1dad41 0.264 at 37,037, 06d1f9d029 0.269 at 36,698, 272854107e 0.274 at 36,642, c57aebeb3e 0.275 at 36,634, e5ddcbb6a5 0.298 at 36,626, 58159e130b 0.305 at 36,602, 3e50dc7ea6 0.342 at 36,482, 9fac496194 0.349 at 36,467, 570f49c26e 0.351 at 36,454, 775d8dda6e 0.360 at 36,443, 21e8b873fe 0.361 at 36,441, 9133d8167a 0.374 at 36,436, 8162560177 0.393 at 32,966, d35040fd68 0.403 at 32,628, ed94bd7e99 0.406 at 32,546, 7bdcdc8f27 0.440 at 32,530, a78522d7eb 0.442 at 32,522, 735b92ad53 0.449 at 32,520, b00da878bf 0.463 at 32,490, 4542a08fb0 0.465 at 32,474, 47da731a5c 0.476 at 32,389, d53d76f7db 0.481 at 32,385, 7887b32787 0.484 at 32,364, 2f4c1d82ec 0.548 at 32,336, 263788ab64 0.552 at 32,312, f69da4fcc8 0.600 at 32,299

The front of all runs on cpu 8: 60c95fbea3 0.232 at 74,548, d60e3aab99 0.244 at 46,608, cc0b1e2aeb 0.245 at 42,512, 436af85b80 0.250 at 41,849, 0bab7fed3e 0.252 at 41,805, 064ee4f23a 0.257 at 41,166, 8bbe1dad41 0.261 at 37,037, 06d1f9d029 0.268 at 36,698, c57aebeb3e 0.271 at 36,634, e5ddcbb6a5 0.298 at 36,626, 58159e130b 0.301 at 36,602, 3e50dc7ea6 0.342 at 36,482, 9fac496194 0.345 at 36,467, 570f49c26e 0.351 at 36,454, 775d8dda6e 0.359 at 36,443, 21e8b873fe 0.359 at 36,441, 9133d8167a 0.376 at 36,436, 8162560177 0.384 at 32,966, d35040fd68 0.400 at 32,628, ed94bd7e99 0.406 at 32,546, 7bdcdc8f27 0.431 at 32,530, a78522d7eb 0.441 at 32,522, 735b92ad53 0.451 at 32,520, 4542a08fb0 0.461 at 32,474, d53d76f7db 0.463 at 32,385, 7887b32787 0.489 at 32,364, 2f4c1d82ec 0.550 at 32,336, 4add88f6fb 0.557 at 32,312, f69da4fcc8 0.598 at 32,299

On both fronts: 26 of 32 and 29.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| 60c95fbea3 | 0.243 | 0.232 | 1.045 |
| cc0b1e2aeb | 0.247 | 0.245 | 1.008 |
| 436af85b80 | 0.247 | 0.250 | 0.988 |
| 44af4fb785 | 0.250 | 0.254 | 0.985 |
| d60e3aab99 | 0.251 | 0.244 | 1.029 |
| 0bab7fed3e | 0.252 | 0.252 | 0.998 |
| 4e3a904b8e | 0.254 | 0.254 | 1.002 |
| 9517490eb3 | 0.258 | 0.258 | 1.003 |
| 1a90a3e004 | 0.260 | 0.262 | 0.992 |
| 76ab789fed | 0.263 | 0.263 | 1.000 |
| bbab8560dd | 0.263 | 0.265 | 0.995 |
| 8bbe1dad41 | 0.264 | 0.261 | 1.010 |
| 0cf9f1e76a | 0.265 | 0.265 | 0.998 |
| 064ee4f23a | 0.266 | 0.257 | 1.034 |
| 8637e4c37e | 0.267 | 0.268 | 0.996 |
| 69842b04ad | 0.268 | 0.271 | 0.986 |
| 06d1f9d029 | 0.269 | 0.268 | 1.001 |
| 7125b151e4 | 0.272 | 0.263 | 1.033 |
| 7075e8f2b1 | 0.272 | 0.274 | 0.995 |
| 272854107e | 0.274 | 0.272 | 1.008 |
| 7670d35541 | 0.274 | 0.275 | 1.000 |
| e076a00103 | 0.275 | 0.277 | 0.990 |
| c57aebeb3e | 0.275 | 0.271 | 1.012 |
| ca2e692954 | 0.276 | 0.274 | 1.006 |
| 2bdab2950f | 0.276 | 0.278 | 0.992 |
| 1c4300cbbb | 0.281 | 0.284 | 0.990 |
| 98d7746633 | 0.282 | 0.279 | 1.009 |
| 2117a45620 | 0.282 | 0.277 | 1.019 |
| 2b55d23a18 | 0.283 | 0.281 | 1.007 |
| 416077aa2f | 0.284 | 0.282 | 1.006 |
| a36dc45e12 | 0.284 | 0.282 | 1.008 |
| 343d881df1 | 0.286 | 0.287 | 0.996 |
| c13c77dc7c | 0.286 | 0.289 | 0.990 |
| 4bb0870716 | 0.287 | 0.293 | 0.982 |
| 2b7e66e1f3 | 0.289 | 0.297 | 0.971 |
| 7d7f1bf4fa | 0.292 | 0.294 | 0.994 |
| 7ab7315744 | 0.292 | 0.295 | 0.991 |
| 38de166d54 | 0.295 | 0.298 | 0.990 |
| 4446c9069e | 0.295 | 0.286 | 1.031 |
| e5ddcbb6a5 | 0.298 | 0.298 | 1.001 |
| 74ea2d2e27 | 0.299 | 0.302 | 0.990 |
| a03ef495f5 | 0.301 | 0.297 | 1.012 |
| ccc8da3b12 | 0.303 | 0.300 | 1.008 |
| 58159e130b | 0.305 | 0.301 | 1.011 |
| 19104ead72 | 0.305 | 0.309 | 0.987 |
| 5671742b27 | 0.305 | 0.300 | 1.016 |
| 9f9c8fdb94 | 0.309 | 0.304 | 1.018 |
| 6583b9f742 | 0.311 | 0.310 | 1.003 |
| ce3a84b4a0 | 0.318 | 0.313 | 1.017 |
| 2b5e92dd57 | 0.334 | 0.333 | 1.004 |
| 3e50dc7ea6 | 0.342 | 0.342 | 1.000 |
| 8581dba4f7 | 0.342 | 0.345 | 0.991 |
| 9fac496194 | 0.349 | 0.345 | 1.011 |
| 570f49c26e | 0.351 | 0.351 | 1.000 |
| 0f3d5dae58 | 0.357 | 0.353 | 1.013 |
| 775d8dda6e | 0.360 | 0.359 | 1.002 |
| b0a896c3c3 | 0.361 | 0.362 | 0.997 |
| 21e8b873fe | 0.361 | 0.359 | 1.005 |
| ea57db4076 | 0.362 | 0.365 | 0.991 |
| 75c9affa70 | 0.364 | 0.364 | 1.001 |
| bfa7370096 | 0.368 | 0.350 | 1.052 |
| 9133d8167a | 0.374 | 0.376 | 0.994 |
| f48c2a5150 | 0.378 | 0.381 | 0.992 |
| 323f2ccfb8 | 0.381 | 0.375 | 1.017 |
| a1578b537c | 0.386 | 0.391 | 0.988 |
| 31e4e22b2e | 0.387 | 0.384 | 1.007 |
| 7c49a5ffca | 0.387 | 0.386 | 1.004 |
| 7f07a469cb | 0.388 | 0.389 | 0.996 |
| e6a3c1fb8c | 0.389 | 0.389 | 1.000 |
| 51a8931db2 | 0.390 | 0.384 | 1.014 |
| dac6ff750a | 0.391 | 0.392 | 0.998 |
| 2789713e31 | 0.391 | 0.396 | 0.988 |
| 8162560177 | 0.393 | 0.384 | 1.023 |
| 3405116655 | 0.394 | 0.395 | 0.997 |
| 7e91afe735 | 0.395 | 0.394 | 1.003 |
| a170190b5a | 0.398 | 0.390 | 1.020 |
| df2ac6c7ab | 0.401 | 0.394 | 1.017 |
| d35040fd68 | 0.403 | 0.400 | 1.009 |
| a1ff4b8022 | 0.405 | 0.408 | 0.994 |
| 8a6365a3ff | 0.405 | 0.406 | 0.997 |
| ed94bd7e99 | 0.406 | 0.406 | 1.002 |
| 4ba5b2c147 | 0.407 | 0.409 | 0.995 |
| 69270766bd | 0.409 | 0.410 | 0.998 |
| 0c5782b28a | 0.411 | 0.412 | 0.998 |
| 4daab7895a | 0.427 | 0.429 | 0.995 |
| d05d104578 | 0.431 | 0.431 | 1.000 |
| ae5d7cdaae | 0.434 | 0.432 | 1.004 |
| 8f0973fc8f | 0.435 | 0.429 | 1.013 |
| 870c24c9cf | 0.438 | 0.434 | 1.011 |
| 7bdcdc8f27 | 0.440 | 0.431 | 1.021 |
| e570f69332 | 0.441 | 0.435 | 1.014 |
| a78522d7eb | 0.442 | 0.441 | 1.000 |
| 0039591d51 | 0.443 | 0.447 | 0.991 |
| 609b436e3a | 0.445 | 0.446 | 0.999 |
| 301a268219 | 0.446 | 0.438 | 1.019 |
| b46a9c7ad4 | 0.447 | 0.448 | 0.998 |
| 63e3305540 | 0.449 | 0.445 | 1.010 |
| 735b92ad53 | 0.449 | 0.451 | 0.995 |
| 03cf426d67 | 0.451 | 0.452 | 0.998 |
| 2a2c2b4256 | 0.452 | 0.456 | 0.992 |
| a808c92923 | 0.455 | 0.458 | 0.995 |
| 635a47fd26 | 0.456 | 0.454 | 1.005 |
| b00da878bf | 0.463 | 0.466 | 0.993 |
| 740331292d | 0.464 | 0.454 | 1.020 |
| 4542a08fb0 | 0.465 | 0.461 | 1.009 |
| d26dfdeda4 | 0.466 | 0.458 | 1.016 |
| 47da731a5c | 0.476 | 0.477 | 0.998 |
| 8252421ca2 | 0.481 | 0.480 | 1.001 |
| d53d76f7db | 0.481 | 0.463 | 1.038 |
| 7887b32787 | 0.484 | 0.489 | 0.990 |
| f362a1bba0 | 0.486 | 0.469 | 1.037 |
| 83098a32c7 | 0.497 | 0.500 | 0.995 |
| 3d312e796e | 0.500 | 0.499 | 1.002 |
| 0826d64cd9 | 0.501 | 0.497 | 1.008 |
| 2f4c1d82ec | 0.548 | 0.550 | 0.996 |
| 263788ab64 | 0.552 | 0.557 | 0.992 |
| 4e378cc12e | 0.553 | 0.550 | 1.006 |
| f27cc3ce5a | 0.557 | 0.555 | 1.004 |
| 4add88f6fb | 0.558 | 0.557 | 1.002 |
| 5c495fe0f3 | 0.569 | 0.570 | 1.000 |
| 776c86e476 | 0.576 | 0.579 | 0.995 |
| 4996bc41b8 | 0.581 | 0.582 | 1.000 |
| 844716c23e | 0.585 | 0.585 | 1.001 |
| f69da4fcc8 | 0.600 | 0.598 | 1.002 |
| f932112676 | 0.608 | 0.607 | 1.001 |
| 35728dddcf | 1.077 | 1.081 | 0.997 |
| eef03e6a19 | 1.088 | 1.094 | 0.994 |
| 0350ea6ee2 | 1.186 | 1.187 | 0.999 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.

## Session 19 - Iteration 82: seed 21 (the JIT's first run) and the newest four

`seed 21 tag2 then experiment compare-fronts.py --rounds 10 --cpus 2,8`,
commit 32a746eb8: seeds 17-21. **Calibration 0.995.** The CPUs: median
1.006, 10-90% 0.987-1.022, ranks 1.00. **The front of all runs: 35, 1 by
memory alone; its four fastest carry the JIT** (6fd52398b1 0.204). Seed
21 not small: fastest +19.6%, smallest total +13.4%.

### The report

# Fronts measured again in one session

10 rounds, the median of them; every design paired with hand-made s6 on the same CPU (cpu 2, cpu 8); designs built with this commit.

**Calibration: hand-made s6 against itself 0.995** (kernel 1.004, fib 0.986, parse 0.994, corpus 0.993, loop 1.001, sieve 1.010).

| run | design | speed now | recorded | size now | recorded | binary | binary + image | memory KB | kernel | fib | parse | corpus | loop | sieve (held out) | on the front of all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| this clone: db.jsonl | 405b357aa4 | 0.602 | 0.597 | 7,011 | 7,011 | 25,280 | 32,291 | 212.0 | 0.573 | 1.206 | 0.228 | 0.389 | 1.297 | 1.157 | yes |
| this clone: db.jsonl | 7d6ad4a7c4 | 0.563 | 0.560 | 7,056 | 7,056 | 25,280 | 32,336 | 208.0 | 0.519 | 1.145 | 0.221 | 0.341 | 1.261 | 1.051 |  |
| this clone: db.jsonl | 914abba99c | 0.506 | 0.507 | 7,074 | 7,074 | 25,280 | 32,354 | 216.0 | 0.514 | 1.057 | 0.150 | 0.308 | 1.321 | 1.120 | yes |
| this clone: db.jsonl | 1ba7f7f337 | 0.361 | 0.349 | 7,090 | 7,090 | 29,352 | 36,442 | 212.0 | 0.388 | 0.610 | 0.109 | 0.238 | 0.996 | 0.894 |  |
| this clone: db.jsonl | 0c744b9d8a | 0.484 | 0.483 | 7,092 | 7,092 | 25,280 | 32,372 | 216.0 | 0.490 | 1.124 | 0.135 | 0.282 | 1.272 | 1.114 | yes |
| this clone: db.jsonl | c3cacf2f5f | 0.363 | 0.355 | 7,097 | 7,097 | 29,352 | 36,449 | 216.0 | 0.383 | 0.634 | 0.102 | 0.247 | 1.030 | 0.886 |  |
| this clone: db.jsonl | 8d9ba49cc5 | 0.349 | 0.331 | 7,100 | 7,100 | 29,352 | 36,452 | 212.0 | 0.371 | 0.578 | 0.111 | 0.239 | 0.906 | 0.900 | yes |
| this clone: db.jsonl | 482e8a7ed7 | 0.485 | 0.489 | 7,102 | 7,102 | 25,280 | 32,382 | 216.0 | 0.499 | 1.087 | 0.134 | 0.285 | 1.290 | 1.110 |  |
| this clone: db.jsonl | e1919aa461 | 0.487 | 0.490 | 7,115 | 7,115 | 25,280 | 32,395 | 216.0 | 0.489 | 1.149 | 0.134 | 0.285 | 1.276 | 1.137 |  |
| this clone: db.jsonl | 0644d0dd00 | 0.494 | 0.492 | 7,116 | 7,116 | 25,280 | 32,396 | 216.0 | 0.503 | 1.137 | 0.140 | 0.288 | 1.271 | 1.097 |  |
| this clone: db.jsonl | 51139692c8 | 0.369 | 0.365 | 7,129 | 7,129 | 29,352 | 36,481 | 216.0 | 0.378 | 0.613 | 0.108 | 0.243 | 1.111 | 0.954 |  |
| this clone: db.jsonl | f9683c9c5d | 0.344 | 0.337 | 7,130 | 7,130 | 29,352 | 36,482 | 216.0 | 0.347 | 0.588 | 0.101 | 0.227 | 1.027 | 0.838 |  |
| this clone: db.jsonl | b77ca6ac9d | 0.465 | 0.463 | 7,234 | 7,234 | 25,280 | 32,514 | 212.0 | 0.581 | 1.116 | 0.232 | 0.373 | 0.387 | 0.732 |  |
| this clone: db.jsonl | 2dbcfbd160 | 0.454 | 0.443 | 7,240 | 7,240 | 25,280 | 32,520 | 212.0 | 0.538 | 1.150 | 0.223 | 0.348 | 0.402 | 0.750 |  |
| this clone: db.jsonl | 7f2776ecd3 | 0.304 | 0.296 | 7,250 | 7,250 | 29,352 | 36,602 | 212.0 | 0.421 | 0.742 | 0.123 | 0.272 | 0.248 | 0.586 |  |
| this clone: db.jsonl | f38adae394 | 0.280 | 0.264 | 7,282 | 7,282 | 29,352 | 36,634 | 216.0 | 0.367 | 0.668 | 0.109 | 0.232 | 0.279 | 0.603 |  |
| this clone: db.jsonl | e4546dd17a | 1.069 | 1.066 | 7,286 | 7,286 | 21,184 | 28,470 | 216.0 | 1.287 | 1.002 | 0.875 | 1.103 | 1.120 | 1.132 | yes |
| this clone: db.jsonl | 02eb3a4510 | 0.396 | 0.384 | 7,314 | 7,314 | 25,280 | 32,594 | 216.0 | 0.487 | 1.165 | 0.139 | 0.282 | 0.439 | 0.733 | yes |
| this clone: db.jsonl | d96524713d | 0.392 | 0.380 | 7,686 | 7,686 | 25,280 | 32,966 | 216.0 | 0.487 | 1.102 | 0.136 | 0.278 | 0.459 | 0.741 | yes |
| this clone: db.jsonl | 69c8bd3461 | 0.378 | 0.370 | 7,695 | 7,695 | 25,280 | 32,975 | 216.0 | 0.483 | 1.080 | 0.135 | 0.272 | 0.402 | 0.741 | yes |
| this clone: db.jsonl | f0006562a1 | 0.240 | 0.230 | 7,704 | 7,704 | 29,448 | 37,152 | 220.0 | 0.533 | 0.190 | 0.147 | 0.302 | 0.178 | 0.777 | yes |
| this clone: db.jsonl | db03cd6821 | 0.239 | 0.236 | 7,712 | 7,712 | 29,448 | 37,160 | 220.0 | 0.512 | 0.194 | 0.144 | 0.304 | 0.179 | 0.767 | yes |
| this clone: db.jsonl | 2f752c5dba | 0.231 | 0.233 | 7,824 | 7,824 | 29,448 | 37,272 | 220.0 | 0.511 | 0.192 | 0.134 | 0.288 | 0.173 | 0.746 | yes |
| this clone: db.jsonl | fc82e55f22 | 0.236 | 0.238 | 7,888 | 7,888 | 29,448 | 37,336 | 220.0 | 0.514 | 0.193 | 0.146 | 0.291 | 0.173 | 0.755 |  |
| this clone: db.jsonl | 6fd52398b1 | 0.204 | 0.200 | 7,920 | 7,920 | 37,640 | 45,560 | 216.0 | 0.380 | 0.191 | 0.113 | 0.236 | 0.184 | 0.649 | yes |
| this clone: db.jsonl | b499c3cb39 | 0.233 | 0.232 | 8,136 | 8,136 | 29,448 | 37,584 | 208.0 | 0.505 | 0.192 | 0.140 | 0.286 | 0.176 | 0.731 | yes |
| this clone: db.jsonl | 3cec15fa82 | 0.234 | 0.230 | 8,160 | 8,160 | 29,448 | 37,608 | 208.0 | 0.495 | 0.194 | 0.137 | 0.286 | 0.185 | 0.754 |  |
| this clone: db.jsonl | 3d761d0518 | 1.086 | 1.080 | 8,342 | 8,342 | 21,184 | 29,526 | 216.0 | 1.282 | 1.015 | 0.867 | 1.105 | 1.211 | 1.148 |  |
| this clone: db.jsonl | 95e9361e80 | 0.219 | 0.222 | 8,648 | 8,648 | 29,448 | 38,096 | 212.0 | 0.491 | 0.151 | 0.137 | 0.297 | 0.169 | 0.685 | yes |
| this clone: db.jsonl | 363adb7a37 | 0.378 | 0.357 | 8,773 | 8,773 | 25,280 | 34,053 | 216.0 | 0.491 | 1.132 | 0.140 | 0.280 | 0.354 | 0.719 |  |
| archived-20261006-170257: db.jsonl | 3d312e796e | 0.501 | 0.419 | 7,009 | 7,009 | 33,448 | 40,457 | 216.0 | 0.528 | 0.768 | 0.198 | 0.357 | 1.106 | 0.917 |  |
| archived-20261006-170257: db.jsonl | a1ff4b8022 | 0.403 | 0.388 | 7,043 | 7,043 | 33,448 | 40,491 | 218.0 | 0.426 | 0.701 | 0.124 | 0.269 | 1.060 | 0.900 |  |
| archived-20261006-170257: db.jsonl | 3405116655 | 0.393 | 0.353 | 7,049 | 7,049 | 37,544 | 44,593 | 212.0 | 0.439 | 0.670 | 0.121 | 0.270 | 0.980 | 0.881 |  |
| archived-20261006-170257: db.jsonl | 4ba5b2c147 | 0.407 | 0.338 | 7,057 | 7,057 | 33,448 | 40,505 | 216.0 | 0.434 | 0.726 | 0.121 | 0.269 | 1.087 | 0.885 |  |
| archived-20261006-170257: db.jsonl | 0c5782b28a | 0.412 | 0.343 | 7,073 | 7,073 | 33,448 | 40,521 | 216.0 | 0.431 | 0.719 | 0.125 | 0.269 | 1.132 | 0.881 |  |
| archived-20261006-170257: db.jsonl | 31e4e22b2e | 0.385 | 0.343 | 7,085 | 7,085 | 33,448 | 40,533 | 216.0 | 0.410 | 0.634 | 0.113 | 0.251 | 1.148 | 0.977 |  |
| archived-20261006-170257: db.jsonl | 323f2ccfb8 | 0.383 | 0.337 | 7,105 | 7,105 | 37,544 | 44,649 | 216.0 | 0.378 | 0.763 | 0.109 | 0.235 | 1.117 | 0.943 |  |
| archived-20261006-170257: db.jsonl | a1578b537c | 0.395 | 0.334 | 7,120 | 7,120 | 37,544 | 44,664 | 216.0 | 0.382 | 0.796 | 0.113 | 0.244 | 1.151 | 0.949 |  |
| archived-20261006-170257: db.jsonl | e6a3c1fb8c | 0.390 | 0.318 | 7,130 | 7,130 | 37,544 | 44,674 | 212.0 | 0.378 | 0.829 | 0.109 | 0.233 | 1.124 | 0.921 |  |
| archived-20261006-170257: db.jsonl | ce3a84b4a0 | 0.323 | 0.307 | 7,217 | 7,217 | 33,448 | 40,665 | 216.0 | 0.433 | 0.811 | 0.122 | 0.269 | 0.306 | 0.590 |  |
| archived-20261006-170257: db.jsonl | 6583b9f742 | 0.321 | 0.277 | 7,218 | 7,218 | 37,544 | 44,762 | 216.0 | 0.447 | 0.780 | 0.124 | 0.276 | 0.284 | 0.641 |  |
| archived-20261006-170257: db.jsonl | 2b7e66e1f3 | 0.298 | 0.260 | 7,226 | 7,226 | 37,544 | 44,770 | 216.0 | 0.444 | 0.669 | 0.129 | 0.267 | 0.230 | 0.622 |  |
| archived-20261006-170257: db.jsonl | 38de166d54 | 0.295 | 0.267 | 7,234 | 7,234 | 37,544 | 44,778 | 216.0 | 0.450 | 0.659 | 0.126 | 0.258 | 0.233 | 0.607 |  |
| archived-20261006-170257: db.jsonl | 2b55d23a18 | 0.281 | 0.251 | 7,266 | 7,266 | 66,216 | 73,482 | 232.0 | 0.353 | 0.853 | 0.102 | 0.217 | 0.265 | 0.567 |  |
| archived-20261006-170257: db.jsonl | a36dc45e12 | 0.288 | 0.235 | 7,283 | 7,283 | 37,544 | 44,827 | 212.0 | 0.390 | 0.702 | 0.111 | 0.238 | 0.274 | 0.617 |  |
| archived-20261006-170257: db.jsonl | 5671742b27 | 0.305 | 0.234 | 7,690 | 7,690 | 37,544 | 45,234 | 212.0 | 0.388 | 0.877 | 0.112 | 0.230 | 0.300 | 0.642 |  |
| archived-20261006-175959: db.jsonl | 844716c23e | 0.584 | 0.589 | 7,051 | 7,051 | 25,280 | 32,331 | 208.0 | 0.568 | 1.216 | 0.226 | 0.364 | 1.197 | 1.068 |  |
| archived-20261006-175959: db.jsonl | 4996bc41b8 | 0.588 | 0.586 | 7,051 | 7,051 | 25,280 | 32,331 | 208.0 | 0.567 | 1.236 | 0.226 | 0.367 | 1.213 | 1.073 |  |
| archived-20261006-175959: db.jsonl | 776c86e476 | 0.577 | 0.574 | 7,059 | 7,059 | 25,280 | 32,339 | 208.0 | 0.556 | 1.131 | 0.229 | 0.371 | 1.195 | 1.038 |  |
| archived-20261006-175959: db.jsonl | 5c495fe0f3 | 0.567 | 0.568 | 7,090 | 7,090 | 25,280 | 32,370 | 212.0 | 0.549 | 1.157 | 0.227 | 0.358 | 1.135 | 1.027 |  |
| archived-20261006-175959: db.jsonl | f27cc3ce5a | 0.556 | 0.559 | 7,108 | 7,108 | 25,280 | 32,388 | 212.0 | 0.536 | 1.118 | 0.221 | 0.346 | 1.163 | 1.048 |  |
| archived-20261006-175959: db.jsonl | 51a8931db2 | 0.388 | 0.385 | 7,115 | 7,115 | 29,352 | 36,467 | 212.0 | 0.386 | 0.783 | 0.110 | 0.241 | 1.104 | 0.963 |  |
| archived-20261006-175959: db.jsonl | 4542a08fb0 | 0.458 | 0.466 | 7,194 | 7,194 | 25,280 | 32,474 | 212.0 | 0.588 | 1.099 | 0.228 | 0.371 | 0.369 | 0.725 | yes |
| archived-20261006-175959: db.jsonl | 8252421ca2 | 0.483 | 0.482 | 7,194 | 7,194 | 25,280 | 32,474 | 208.0 | 0.604 | 1.150 | 0.243 | 0.392 | 0.398 | 0.726 |  |
| archived-20261006-175959: db.jsonl | 8a6365a3ff | 0.407 | 0.406 | 7,217 | 7,217 | 29,376 | 36,593 | 212.0 | 0.526 | 1.117 | 0.143 | 0.289 | 0.460 | 0.750 |  |
| archived-20261006-175959: db.jsonl | 2789713e31 | 0.395 | 0.398 | 7,242 | 7,242 | 29,376 | 36,618 | 208.0 | 0.515 | 1.078 | 0.151 | 0.291 | 0.392 | 0.753 |  |
| archived-20261006-175959: db.jsonl | d26dfdeda4 | 0.463 | 0.461 | 7,250 | 7,250 | 25,280 | 32,530 | 208.0 | 0.575 | 1.147 | 0.231 | 0.358 | 0.390 | 0.756 |  |
| archived-20261006-175959: db.jsonl | dac6ff750a | 0.391 | 0.392 | 7,258 | 7,258 | 29,376 | 36,634 | 208.0 | 0.520 | 1.007 | 0.155 | 0.295 | 0.381 | 0.707 |  |
| archived-20261006-175959: db.jsonl | 2a2c2b4256 | 0.454 | 0.457 | 7,258 | 7,258 | 25,280 | 32,538 | 208.0 | 0.573 | 1.117 | 0.225 | 0.349 | 0.383 | 0.741 |  |
| archived-20261006-175959: db.jsonl | e570f69332 | 0.436 | 0.434 | 7,274 | 7,274 | 25,280 | 32,554 | 216.0 | 0.504 | 1.123 | 0.222 | 0.318 | 0.393 | 0.722 |  |
| archived-20261006-175959: db.jsonl | f48c2a5150 | 0.378 | 0.377 | 7,276 | 7,276 | 29,376 | 36,652 | 212.0 | 0.402 | 0.953 | 0.202 | 0.304 | 0.327 | 0.694 |  |
| archived-20261006-175959: db.jsonl | a170190b5a | 0.392 | 0.386 | 7,298 | 7,298 | 29,376 | 36,674 | 208.0 | 0.517 | 1.178 | 0.146 | 0.285 | 0.367 | 0.736 |  |
| archived-20261006-175959: db.jsonl | 2117a45620 | 0.278 | 0.274 | 7,307 | 7,307 | 33,448 | 40,755 | 216.0 | 0.419 | 0.498 | 0.116 | 0.256 | 0.270 | 0.520 |  |
| archived-20261006-175959: db.jsonl | 4e3a904b8e | 0.255 | 0.255 | 7,323 | 7,323 | 62,128 | 69,451 | 232.0 | 0.374 | 0.599 | 0.106 | 0.235 | 0.192 | 0.541 |  |
| archived-20261006-175959: db.jsonl | 69842b04ad | 0.273 | 0.268 | 7,323 | 7,323 | 33,448 | 40,771 | 216.0 | 0.391 | 0.696 | 0.106 | 0.229 | 0.229 | 0.605 |  |
| archived-20261006-175959: db.jsonl | 609b436e3a | 0.444 | 0.450 | 7,329 | 7,329 | 25,280 | 32,609 | 212.0 | 0.556 | 1.060 | 0.219 | 0.368 | 0.365 | 0.709 |  |
| archived-20261006-175959: db.jsonl | 0f3d5dae58 | 0.352 | 0.352 | 7,331 | 7,331 | 29,376 | 36,707 | 216.0 | 0.465 | 0.943 | 0.125 | 0.250 | 0.393 | 0.720 |  |
| archived-20261006-175959: db.jsonl | bbab8560dd | 0.265 | 0.261 | 7,338 | 7,338 | 33,448 | 40,786 | 216.0 | 0.382 | 0.554 | 0.098 | 0.226 | 0.279 | 0.533 |  |
| archived-20261006-175959: db.jsonl | 1c4300cbbb | 0.274 | 0.285 | 7,338 | 7,338 | 33,448 | 40,786 | 216.0 | 0.410 | 0.657 | 0.101 | 0.220 | 0.260 | 0.605 |  |
| archived-20261006-175959: db.jsonl | c13c77dc7c | 0.285 | 0.286 | 7,339 | 7,339 | 33,472 | 40,811 | 208.0 | 0.392 | 0.657 | 0.108 | 0.233 | 0.292 | 0.628 |  |
| archived-20261006-175959: db.jsonl | b0a896c3c3 | 0.359 | 0.358 | 7,347 | 7,347 | 29,376 | 36,723 | 216.0 | 0.445 | 1.045 | 0.133 | 0.253 | 0.381 | 0.739 |  |
| archived-20261006-175959: db.jsonl | 416077aa2f | 0.279 | 0.272 | 7,349 | 7,349 | 33,448 | 40,797 | 212.0 | 0.368 | 0.750 | 0.108 | 0.236 | 0.239 | 0.582 |  |
| archived-20261006-175959: db.jsonl | 0cf9f1e76a | 0.252 | 0.265 | 7,365 | 7,365 | 62,128 | 69,493 | 232.0 | 0.397 | 0.723 | 0.107 | 0.237 | 0.141 | 0.566 |  |
| archived-20261006-175959: db.jsonl | 740331292d | 0.466 | 0.467 | 7,505 | 7,505 | 25,280 | 32,785 | 208.0 | 0.583 | 1.091 | 0.227 | 0.366 | 0.415 | 0.745 |  |
| archived-20261006-175959: db.jsonl | 03cf426d67 | 0.453 | 0.448 | 7,539 | 7,539 | 25,280 | 32,819 | 208.0 | 0.526 | 1.212 | 0.222 | 0.345 | 0.392 | 0.753 |  |
| archived-20261006-175959: db.jsonl | a03ef495f5 | 0.302 | 0.301 | 7,644 | 7,644 | 29,352 | 36,996 | 216.0 | 0.408 | 0.796 | 0.109 | 0.252 | 0.279 | 0.568 |  |
| archived-20261006-175959: db.jsonl | 63e3305540 | 0.446 | 0.438 | 7,664 | 7,664 | 25,280 | 32,944 | 212.0 | 0.524 | 1.203 | 0.218 | 0.328 | 0.390 | 0.735 |  |
| archived-20261006-175959: db.jsonl | 0039591d51 | 0.446 | 0.442 | 7,675 | 7,675 | 25,280 | 32,955 | 212.0 | 0.568 | 1.064 | 0.225 | 0.350 | 0.371 | 0.725 |  |
| archived-20261006-175959: db.jsonl | b46a9c7ad4 | 0.445 | 0.447 | 7,677 | 7,677 | 25,280 | 32,957 | 208.0 | 0.575 | 1.036 | 0.219 | 0.347 | 0.388 | 0.716 |  |
| archived-20261006-175959: db.jsonl | 301a268219 | 0.444 | 0.444 | 7,683 | 7,683 | 25,280 | 32,963 | 212.0 | 0.530 | 1.142 | 0.216 | 0.340 | 0.389 | 0.730 |  |
| archived-20261006-175959: db.jsonl | a808c92923 | 0.457 | 0.456 | 7,698 | 7,698 | 25,280 | 32,978 | 208.0 | 0.594 | 1.099 | 0.228 | 0.368 | 0.363 | 0.752 |  |
| archived-20261006-175959: db.jsonl | 7d7f1bf4fa | 0.290 | 0.291 | 7,707 | 7,707 | 29,352 | 37,059 | 212.0 | 0.392 | 0.786 | 0.110 | 0.224 | 0.271 | 0.630 |  |
| archived-20261006-175959: db.jsonl | 064ee4f23a | 0.266 | 0.263 | 7,718 | 7,718 | 33,448 | 41,166 | 212.0 | 0.405 | 0.561 | 0.107 | 0.238 | 0.230 | 0.605 |  |
| archived-20261006-175959: db.jsonl | ca2e692954 | 0.274 | 0.273 | 7,738 | 7,738 | 33,448 | 41,186 | 208.0 | 0.366 | 0.765 | 0.106 | 0.218 | 0.238 | 0.599 |  |
| archived-20261006-175959: db.jsonl | 7075e8f2b1 | 0.278 | 0.278 | 7,738 | 7,738 | 33,448 | 41,186 | 208.0 | 0.374 | 0.675 | 0.109 | 0.230 | 0.263 | 0.561 |  |
| archived-20261006-175959: db.jsonl | 9f9c8fdb94 | 0.310 | 0.310 | 7,744 | 7,744 | 33,448 | 41,192 | 208.0 | 0.429 | 0.803 | 0.108 | 0.247 | 0.314 | 0.615 |  |
| archived-20261006-175959: db.jsonl | ccc8da3b12 | 0.306 | 0.300 | 7,759 | 7,759 | 33,448 | 41,207 | 208.0 | 0.400 | 0.554 | 0.109 | 0.255 | 0.435 | 0.687 |  |
| archived-20261006-175959: db.jsonl | 2bdab2950f | 0.276 | 0.278 | 7,783 | 7,783 | 29,352 | 37,135 | 216.0 | 0.398 | 0.638 | 0.110 | 0.229 | 0.251 | 0.611 |  |
| archived-20261006-175959: db.jsonl | e076a00103 | 0.280 | 0.274 | 7,783 | 7,783 | 29,352 | 37,135 | 216.0 | 0.401 | 0.645 | 0.115 | 0.233 | 0.248 | 0.620 |  |
| archived-20261006-175959: db.jsonl | 7f07a469cb | 0.389 | 0.390 | 7,801 | 7,801 | 29,376 | 37,177 | 208.0 | 0.512 | 1.194 | 0.139 | 0.286 | 0.366 | 0.760 |  |
| archived-20261006-175959: db.jsonl | 4daab7895a | 0.428 | 0.425 | 7,806 | 7,806 | 25,280 | 33,086 | 212.0 | 0.518 | 1.080 | 0.216 | 0.329 | 0.358 | 0.721 |  |
| archived-20261006-175959: db.jsonl | 7125b151e4 | 0.276 | 0.273 | 7,970 | 7,970 | 33,448 | 41,418 | 212.0 | 0.392 | 0.604 | 0.105 | 0.240 | 0.267 | 0.569 |  |
| archived-20261006-175959: db.jsonl | 60c95fbea3 | 0.244 | 0.239 | 8,332 | 8,332 | 66,216 | 74,548 | 232.0 | 0.380 | 0.434 | 0.103 | 0.236 | 0.216 | 0.550 |  |
| archived-20261006-175959: db.jsonl | 9517490eb3 | 0.255 | 0.258 | 8,350 | 8,350 | 33,448 | 41,798 | 212.0 | 0.381 | 0.598 | 0.107 | 0.229 | 0.190 | 0.604 |  |
| archived-20261006-175959: db.jsonl | 0bab7fed3e | 0.252 | 0.252 | 8,357 | 8,357 | 33,448 | 41,805 | 212.0 | 0.385 | 0.603 | 0.105 | 0.226 | 0.186 | 0.598 |  |
| archived-20261006-175959: db.jsonl | 436af85b80 | 0.250 | 0.249 | 8,401 | 8,401 | 33,448 | 41,849 | 216.0 | 0.385 | 0.512 | 0.109 | 0.244 | 0.185 | 0.503 |  |
| archived-20261006-175959: db.jsonl | 44af4fb785 | 0.252 | 0.252 | 9,413 | 9,413 | 33,448 | 42,861 | 212.0 | 0.381 | 0.598 | 0.105 | 0.232 | 0.182 | 0.612 |  |
| archived-20261006-175959: db.jsonl | 98d7746633 | 0.276 | 0.282 | 9,598 | 9,598 | 29,352 | 38,950 | 216.0 | 0.385 | 0.650 | 0.108 | 0.212 | 0.280 | 0.646 |  |
| archived-20261006-175959: db.jsonl | 76ab789fed | 0.267 | 0.264 | 9,606 | 9,606 | 29,352 | 38,958 | 220.0 | 0.359 | 0.602 | 0.104 | 0.230 | 0.266 | 0.608 |  |
| archived-20261006-175959: db.jsonl | 35728dddcf | 1.091 | 1.080 | 25,144 | 25,144 | 25,280 | 50,424 | 204.0 | 1.210 | 0.974 | 1.123 | 1.167 | 1.003 | 1.071 |  |
| archived-20261006-175959: db.jsonl | eef03e6a19 | 1.095 | 1.087 | 25,144 | 25,144 | 25,256 | 50,400 | 204.0 | 1.225 | 0.912 | 1.146 | 1.152 | 1.065 | 1.039 |  |
| archived-20261006-175959: db.jsonl | 0350ea6ee2 | 1.190 | 1.182 | 25,144 | 25,144 | 21,184 | 46,328 | 204.0 | 1.322 | 1.025 | 1.256 | 1.269 | 1.105 | 1.138 |  |
| archived-20261006-185037: db.jsonl | f69da4fcc8 | 0.604 | 0.605 | 7,019 | 7,019 | 25,280 | 32,299 | 212.0 | 0.580 | 1.109 | 0.238 | 0.397 | 1.325 | 1.069 |  |
| archived-20261006-185037: db.jsonl | 263788ab64 | 0.552 | 0.561 | 7,032 | 7,032 | 25,280 | 32,312 | 208.0 | 0.505 | 1.196 | 0.205 | 0.333 | 1.245 | 1.067 | yes |
| archived-20261006-185037: db.jsonl | 2f4c1d82ec | 0.551 | 0.541 | 7,056 | 7,056 | 25,280 | 32,336 | 208.0 | 0.506 | 1.107 | 0.213 | 0.338 | 1.255 | 1.073 | yes |
| archived-20261006-185037: db.jsonl | 775d8dda6e | 0.361 | 0.357 | 7,091 | 7,091 | 29,352 | 36,443 | 212.0 | 0.369 | 0.631 | 0.108 | 0.247 | 0.986 | 0.847 |  |
| archived-20261006-185037: db.jsonl | 570f49c26e | 0.348 | 0.350 | 7,102 | 7,102 | 29,352 | 36,454 | 212.0 | 0.357 | 0.613 | 0.099 | 0.212 | 1.110 | 0.863 | yes |
| archived-20261006-185037: db.jsonl | 9fac496194 | 0.351 | 0.347 | 7,115 | 7,115 | 29,352 | 36,467 | 212.0 | 0.365 | 0.617 | 0.099 | 0.230 | 1.042 | 0.842 |  |
| archived-20261006-185037: db.jsonl | b00da878bf | 0.464 | 0.469 | 7,210 | 7,210 | 25,280 | 32,490 | 216.0 | 0.558 | 1.106 | 0.235 | 0.385 | 0.385 | 0.715 |  |
| archived-20261006-185037: db.jsonl | 635a47fd26 | 0.457 | 0.448 | 7,260 | 7,260 | 25,280 | 32,540 | 208.0 | 0.574 | 1.089 | 0.220 | 0.366 | 0.394 | 0.735 |  |
| archived-20261006-185037: db.jsonl | 74ea2d2e27 | 0.300 | 0.304 | 7,274 | 7,274 | 29,352 | 36,626 | 212.0 | 0.408 | 0.503 | 0.171 | 0.296 | 0.233 | 0.579 | yes |
| archived-20261006-185037: db.jsonl | 8f0973fc8f | 0.438 | 0.438 | 7,274 | 7,274 | 25,280 | 32,554 | 212.0 | 0.521 | 1.100 | 0.216 | 0.332 | 0.392 | 0.700 |  |
| archived-20261006-185037: db.jsonl | c57aebeb3e | 0.275 | 0.277 | 7,282 | 7,282 | 29,352 | 36,634 | 212.0 | 0.360 | 0.607 | 0.107 | 0.232 | 0.292 | 0.581 | yes |
| archived-20261006-185037: db.jsonl | 272854107e | 0.274 | 0.275 | 7,290 | 7,290 | 29,352 | 36,642 | 212.0 | 0.365 | 0.700 | 0.105 | 0.205 | 0.281 | 0.598 | yes |
| archived-20261006-185037: db.jsonl | ae5d7cdaae | 0.429 | 0.434 | 7,317 | 7,317 | 25,280 | 32,597 | 212.0 | 0.514 | 1.124 | 0.208 | 0.327 | 0.368 | 0.733 |  |
| archived-20261006-185037: db.jsonl | d05d104578 | 0.431 | 0.436 | 7,466 | 7,466 | 25,280 | 32,746 | 212.0 | 0.488 | 1.093 | 0.213 | 0.326 | 0.401 | 0.698 |  |
| archived-20261006-185037: db.jsonl | 870c24c9cf | 0.436 | 0.440 | 7,632 | 7,632 | 25,280 | 32,912 | 212.0 | 0.512 | 1.121 | 0.214 | 0.317 | 0.406 | 0.726 |  |
| archived-20261006-185037: db.jsonl | 7670d35541 | 0.273 | 0.273 | 7,682 | 7,682 | 29,352 | 37,034 | 212.0 | 0.396 | 0.559 | 0.105 | 0.230 | 0.282 | 0.612 | yes |
| archived-20261006-185037: db.jsonl | 1a90a3e004 | 0.261 | 0.257 | 7,712 | 7,712 | 29,352 | 37,064 | 212.0 | 0.361 | 0.610 | 0.105 | 0.225 | 0.233 | 0.518 | yes |
| archived-20261006-185037: db.jsonl | cc0b1e2aeb | 0.245 | 0.241 | 9,064 | 9,064 | 33,448 | 42,512 | 216.0 | 0.361 | 0.555 | 0.104 | 0.222 | 0.189 | 0.496 |  |
| archived-20261006-185037: db.jsonl | d60e3aab99 | 0.252 | 0.253 | 9,064 | 9,064 | 37,544 | 46,608 | 216.0 | 0.350 | 0.603 | 0.103 | 0.234 | 0.200 | 0.501 |  |
| archived-20261006-203034: db.jsonl | f932112676 | 0.609 | 0.612 | 7,019 | 7,019 | 25,280 | 32,299 | 216.0 | 0.574 | 1.137 | 0.239 | 0.403 | 1.332 | 1.103 |  |
| archived-20261006-203034: db.jsonl | 4add88f6fb | 0.561 | 0.558 | 7,032 | 7,032 | 25,280 | 32,312 | 208.0 | 0.520 | 1.209 | 0.212 | 0.334 | 1.247 | 1.080 |  |
| archived-20261006-203034: db.jsonl | 4e378cc12e | 0.551 | 0.550 | 7,056 | 7,056 | 25,280 | 32,336 | 208.0 | 0.503 | 1.112 | 0.210 | 0.338 | 1.280 | 1.100 |  |
| archived-20261006-203034: db.jsonl | 9133d8167a | 0.379 | 0.361 | 7,084 | 7,084 | 29,352 | 36,436 | 212.0 | 0.402 | 0.646 | 0.110 | 0.243 | 1.123 | 0.900 |  |
| archived-20261006-203034: db.jsonl | 7887b32787 | 0.491 | 0.486 | 7,084 | 7,084 | 25,280 | 32,364 | 216.0 | 0.483 | 1.101 | 0.139 | 0.294 | 1.310 | 1.137 | yes |
| archived-20261006-203034: db.jsonl | 21e8b873fe | 0.356 | 0.346 | 7,089 | 7,089 | 29,352 | 36,441 | 216.0 | 0.356 | 0.658 | 0.103 | 0.234 | 1.019 | 0.851 | yes |
| archived-20261006-203034: db.jsonl | 75c9affa70 | 0.364 | 0.352 | 7,091 | 7,091 | 29,352 | 36,443 | 212.0 | 0.403 | 0.606 | 0.115 | 0.251 | 0.899 | 0.856 |  |
| archived-20261006-203034: db.jsonl | 83098a32c7 | 0.492 | 0.504 | 7,092 | 7,092 | 25,280 | 32,372 | 216.0 | 0.486 | 1.231 | 0.133 | 0.279 | 1.293 | 1.209 |  |
| archived-20261006-203034: db.jsonl | ea57db4076 | 0.364 | 0.356 | 7,102 | 7,102 | 29,352 | 36,454 | 212.0 | 0.386 | 0.613 | 0.100 | 0.243 | 1.104 | 0.904 |  |
| archived-20261006-203034: db.jsonl | d53d76f7db | 0.481 | 0.480 | 7,105 | 7,105 | 25,280 | 32,385 | 216.0 | 0.489 | 1.097 | 0.137 | 0.289 | 1.205 | 1.083 | yes |
| archived-20261006-203034: db.jsonl | 47da731a5c | 0.478 | 0.481 | 7,109 | 7,109 | 25,280 | 32,389 | 216.0 | 0.479 | 1.105 | 0.135 | 0.284 | 1.226 | 1.090 | yes |
| archived-20261006-203034: db.jsonl | f362a1bba0 | 0.491 | 0.492 | 7,110 | 7,110 | 25,280 | 32,390 | 216.0 | 0.485 | 1.127 | 0.141 | 0.288 | 1.281 | 1.105 |  |
| archived-20261006-203034: db.jsonl | 3e50dc7ea6 | 0.337 | 0.329 | 7,130 | 7,130 | 29,352 | 36,482 | 216.0 | 0.335 | 0.581 | 0.097 | 0.239 | 0.961 | 0.863 | yes |
| archived-20261006-203034: db.jsonl | 8581dba4f7 | 0.343 | 0.333 | 7,156 | 7,156 | 29,352 | 36,508 | 216.0 | 0.346 | 0.663 | 0.100 | 0.220 | 0.947 | 0.801 |  |
| archived-20261006-203034: db.jsonl | 735b92ad53 | 0.452 | 0.441 | 7,240 | 7,240 | 25,280 | 32,520 | 212.0 | 0.534 | 1.154 | 0.221 | 0.354 | 0.393 | 0.763 | yes |
| archived-20261006-203034: db.jsonl | a78522d7eb | 0.441 | 0.434 | 7,242 | 7,242 | 25,280 | 32,522 | 212.0 | 0.518 | 1.115 | 0.216 | 0.332 | 0.402 | 0.720 | yes |
| archived-20261006-203034: db.jsonl | 58159e130b | 0.302 | 0.299 | 7,250 | 7,250 | 29,352 | 36,602 | 216.0 | 0.420 | 0.683 | 0.118 | 0.264 | 0.283 | 0.580 | yes |
| archived-20261006-203034: db.jsonl | 7bdcdc8f27 | 0.437 | 0.447 | 7,250 | 7,250 | 25,280 | 32,530 | 212.0 | 0.545 | 1.038 | 0.225 | 0.345 | 0.362 | 0.723 | yes |
| archived-20261006-203034: db.jsonl | ed94bd7e99 | 0.406 | 0.402 | 7,266 | 7,266 | 25,280 | 32,546 | 216.0 | 0.514 | 1.207 | 0.144 | 0.284 | 0.434 | 0.769 | yes |
| archived-20261006-203034: db.jsonl | e5ddcbb6a5 | 0.303 | 0.267 | 7,274 | 7,274 | 29,352 | 36,626 | 212.0 | 0.407 | 0.503 | 0.170 | 0.289 | 0.256 | 0.571 |  |
| archived-20261006-203034: db.jsonl | 7ab7315744 | 0.293 | 0.278 | 7,282 | 7,282 | 29,352 | 36,634 | 212.0 | 0.375 | 0.884 | 0.104 | 0.220 | 0.288 | 0.591 |  |
| archived-20261006-203034: db.jsonl | 06d1f9d029 | 0.273 | 0.262 | 7,346 | 7,346 | 29,352 | 36,698 | 216.0 | 0.361 | 0.672 | 0.107 | 0.222 | 0.265 | 0.575 | yes |
| archived-20261006-203034: db.jsonl | d35040fd68 | 0.403 | 0.400 | 7,348 | 7,348 | 25,280 | 32,628 | 216.0 | 0.519 | 1.172 | 0.143 | 0.281 | 0.437 | 0.755 |  |
| archived-20261006-203034: db.jsonl | 8bbe1dad41 | 0.262 | 0.259 | 7,685 | 7,685 | 29,352 | 37,037 | 216.0 | 0.339 | 0.573 | 0.105 | 0.228 | 0.266 | 0.602 | yes |
| archived-20261006-203034: db.jsonl | 8637e4c37e | 0.265 | 0.268 | 7,685 | 7,685 | 29,376 | 37,061 | 216.0 | 0.348 | 0.558 | 0.110 | 0.230 | 0.263 | 0.565 |  |
| archived-20261006-203034: db.jsonl | 8162560177 | 0.395 | 0.384 | 7,686 | 7,686 | 25,280 | 32,966 | 216.0 | 0.491 | 1.111 | 0.137 | 0.279 | 0.462 | 0.738 |  |
| archived-20261006-203034: db.jsonl | 7e91afe735 | 0.401 | 0.386 | 8,002 | 8,002 | 25,280 | 33,282 | 216.0 | 0.526 | 1.091 | 0.141 | 0.291 | 0.439 | 0.754 |  |

The front of all runs together (speed, binary + image, peak memory), by binary + image: 6fd52398b1 0.204 at 45,560, 216.0 KB, 95e9361e80 0.219 at 38,096, 212.0 KB, b499c3cb39 0.233 at 37,584, 208.0 KB, 2f752c5dba 0.231 at 37,272, 220.0 KB, db03cd6821 0.239 at 37,160, 220.0 KB, f0006562a1 0.240 at 37,152, 220.0 KB, 1a90a3e004 0.261 at 37,064, 212.0 KB, 8bbe1dad41 0.262 at 37,037, 216.0 KB, 7670d35541 0.273 at 37,034, 212.0 KB, 06d1f9d029 0.273 at 36,698, 216.0 KB, 272854107e 0.274 at 36,642, 212.0 KB, c57aebeb3e 0.275 at 36,634, 212.0 KB, 74ea2d2e27 0.300 at 36,626, 212.0 KB, 58159e130b 0.302 at 36,602, 216.0 KB, 3e50dc7ea6 0.337 at 36,482, 216.0 KB, 570f49c26e 0.348 at 36,454, 212.0 KB, 8d9ba49cc5 0.349 at 36,452, 212.0 KB, 21e8b873fe 0.356 at 36,441, 216.0 KB, 69c8bd3461 0.378 at 32,975, 216.0 KB, d96524713d 0.392 at 32,966, 216.0 KB, 02eb3a4510 0.396 at 32,594, 216.0 KB, ed94bd7e99 0.406 at 32,546, 216.0 KB, 7bdcdc8f27 0.437 at 32,530, 212.0 KB, a78522d7eb 0.441 at 32,522, 212.0 KB, 735b92ad53 0.452 at 32,520, 212.0 KB, 4542a08fb0 0.458 at 32,474, 212.0 KB, 47da731a5c 0.478 at 32,389, 216.0 KB, d53d76f7db 0.481 at 32,385, 216.0 KB, 0c744b9d8a 0.484 at 32,372, 216.0 KB, 7887b32787 0.491 at 32,364, 216.0 KB, 914abba99c 0.506 at 32,354, 216.0 KB, 2f4c1d82ec 0.551 at 32,336, 208.0 KB, 263788ab64 0.552 at 32,312, 208.0 KB, 405b357aa4 0.602 at 32,291, 212.0 KB, e4546dd17a 1.069 at 28,470, 216.0 KB

Memory within 8 KB counts as a tie (EVOLVE_MEM_TOL).
On the front by memory alone: 1 of 35 - b499c3cb39 0.233 at 37,584, 208.0 KB

## The same session on two CPUs

Calibration on cpu 2: 0.995; on cpu 8: 0.990.

Speed on cpu 2 over speed on cpu 8, per design: median 1.006, 10-90% 0.987-1.022, extremes 0.946-1.061; rank agreement (Spearman) 1.00.

The front of all runs on cpu 2: 6fd52398b1 0.204 at 45,560, 95e9361e80 0.219 at 38,096, b499c3cb39 0.233 at 37,584, 2f752c5dba 0.231 at 37,272, db03cd6821 0.239 at 37,160, f0006562a1 0.240 at 37,152, 1a90a3e004 0.261 at 37,064, 8bbe1dad41 0.262 at 37,037, 7670d35541 0.273 at 37,034, 06d1f9d029 0.273 at 36,698, 272854107e 0.274 at 36,642, c57aebeb3e 0.275 at 36,634, 74ea2d2e27 0.300 at 36,626, 58159e130b 0.302 at 36,602, 3e50dc7ea6 0.337 at 36,482, 570f49c26e 0.348 at 36,454, 8d9ba49cc5 0.349 at 36,452, 21e8b873fe 0.356 at 36,441, 69c8bd3461 0.378 at 32,975, d96524713d 0.392 at 32,966, 02eb3a4510 0.396 at 32,594, ed94bd7e99 0.406 at 32,546, 7bdcdc8f27 0.437 at 32,530, a78522d7eb 0.441 at 32,522, 735b92ad53 0.452 at 32,520, 4542a08fb0 0.458 at 32,474, 47da731a5c 0.478 at 32,389, d53d76f7db 0.481 at 32,385, 0c744b9d8a 0.484 at 32,372, 7887b32787 0.491 at 32,364, 914abba99c 0.506 at 32,354, 2f4c1d82ec 0.551 at 32,336, 263788ab64 0.552 at 32,312, 405b357aa4 0.602 at 32,291, e4546dd17a 1.069 at 28,470

The front of all runs on cpu 8: 6fd52398b1 0.195 at 45,560, 95e9361e80 0.216 at 38,096, 3cec15fa82 0.231 at 37,608, b499c3cb39 0.233 at 37,584, 2f752c5dba 0.233 at 37,272, f0006562a1 0.236 at 37,152, 1a90a3e004 0.247 at 37,064, 8bbe1dad41 0.268 at 37,037, 272854107e 0.268 at 36,642, c57aebeb3e 0.274 at 36,634, 74ea2d2e27 0.284 at 36,626, 58159e130b 0.301 at 36,602, 3e50dc7ea6 0.341 at 36,482, 9fac496194 0.343 at 36,467, 8d9ba49cc5 0.345 at 36,452, 1ba7f7f337 0.353 at 36,442, 21e8b873fe 0.354 at 36,441, 363adb7a37 0.375 at 34,053, 69c8bd3461 0.378 at 32,975, 8162560177 0.390 at 32,966, 02eb3a4510 0.390 at 32,594, ed94bd7e99 0.409 at 32,546, 7bdcdc8f27 0.429 at 32,530, a78522d7eb 0.438 at 32,522, 735b92ad53 0.447 at 32,520, b77ca6ac9d 0.456 at 32,514, b00da878bf 0.457 at 32,490, 4542a08fb0 0.467 at 32,474, 47da731a5c 0.472 at 32,389, 482e8a7ed7 0.478 at 32,382, 0c744b9d8a 0.482 at 32,372, 7887b32787 0.490 at 32,364, 914abba99c 0.507 at 32,354, 2f4c1d82ec 0.541 at 32,336, 263788ab64 0.557 at 32,312, 405b357aa4 0.594 at 32,291, e4546dd17a 1.067 at 28,470

On both fronts: 29 of 35 and 37.

| design | speed cpu 2 | speed cpu 8 | ratio |
|---|---|---|---|
| 6fd52398b1 | 0.204 | 0.195 | 1.047 |
| 95e9361e80 | 0.219 | 0.216 | 1.014 |
| 2f752c5dba | 0.231 | 0.233 | 0.992 |
| b499c3cb39 | 0.233 | 0.233 | 0.999 |
| 3cec15fa82 | 0.234 | 0.231 | 1.012 |
| fc82e55f22 | 0.236 | 0.236 | 1.001 |
| db03cd6821 | 0.239 | 0.239 | 1.000 |
| f0006562a1 | 0.240 | 0.236 | 1.020 |
| 60c95fbea3 | 0.244 | 0.237 | 1.028 |
| cc0b1e2aeb | 0.245 | 0.235 | 1.039 |
| 436af85b80 | 0.250 | 0.248 | 1.007 |
| 44af4fb785 | 0.252 | 0.247 | 1.018 |
| d60e3aab99 | 0.252 | 0.247 | 1.021 |
| 0cf9f1e76a | 0.252 | 0.267 | 0.946 |
| 0bab7fed3e | 0.252 | 0.254 | 0.994 |
| 9517490eb3 | 0.255 | 0.257 | 0.989 |
| 4e3a904b8e | 0.255 | 0.251 | 1.014 |
| 1a90a3e004 | 0.261 | 0.247 | 1.058 |
| 8bbe1dad41 | 0.262 | 0.268 | 0.980 |
| 8637e4c37e | 0.265 | 0.268 | 0.989 |
| bbab8560dd | 0.265 | 0.257 | 1.030 |
| 064ee4f23a | 0.266 | 0.263 | 1.010 |
| 76ab789fed | 0.267 | 0.263 | 1.017 |
| 7670d35541 | 0.273 | 0.270 | 1.009 |
| 69842b04ad | 0.273 | 0.269 | 1.015 |
| 06d1f9d029 | 0.273 | 0.271 | 1.010 |
| ca2e692954 | 0.274 | 0.272 | 1.005 |
| 272854107e | 0.274 | 0.268 | 1.022 |
| 1c4300cbbb | 0.274 | 0.281 | 0.978 |
| c57aebeb3e | 0.275 | 0.274 | 1.004 |
| 98d7746633 | 0.276 | 0.280 | 0.986 |
| 7125b151e4 | 0.276 | 0.274 | 1.009 |
| 2bdab2950f | 0.276 | 0.280 | 0.986 |
| 7075e8f2b1 | 0.278 | 0.276 | 1.006 |
| 2117a45620 | 0.278 | 0.275 | 1.014 |
| 416077aa2f | 0.279 | 0.284 | 0.982 |
| e076a00103 | 0.280 | 0.281 | 0.995 |
| f38adae394 | 0.280 | 0.279 | 1.002 |
| 2b55d23a18 | 0.281 | 0.287 | 0.980 |
| c13c77dc7c | 0.285 | 0.283 | 1.008 |
| a36dc45e12 | 0.288 | 0.284 | 1.014 |
| 7d7f1bf4fa | 0.290 | 0.292 | 0.994 |
| 7ab7315744 | 0.293 | 0.292 | 1.005 |
| 38de166d54 | 0.295 | 0.299 | 0.987 |
| 2b7e66e1f3 | 0.298 | 0.299 | 0.998 |
| 74ea2d2e27 | 0.300 | 0.284 | 1.055 |
| a03ef495f5 | 0.302 | 0.297 | 1.014 |
| 58159e130b | 0.302 | 0.301 | 1.006 |
| e5ddcbb6a5 | 0.303 | 0.300 | 1.010 |
| 7f2776ecd3 | 0.304 | 0.308 | 0.986 |
| 5671742b27 | 0.305 | 0.301 | 1.012 |
| ccc8da3b12 | 0.306 | 0.303 | 1.010 |
| 9f9c8fdb94 | 0.310 | 0.307 | 1.009 |
| 6583b9f742 | 0.321 | 0.317 | 1.010 |
| ce3a84b4a0 | 0.323 | 0.320 | 1.009 |
| 3e50dc7ea6 | 0.337 | 0.341 | 0.989 |
| 8581dba4f7 | 0.343 | 0.344 | 0.997 |
| f9683c9c5d | 0.344 | 0.342 | 1.005 |
| 570f49c26e | 0.348 | 0.355 | 0.978 |
| 8d9ba49cc5 | 0.349 | 0.345 | 1.010 |
| 9fac496194 | 0.351 | 0.343 | 1.022 |
| 0f3d5dae58 | 0.352 | 0.357 | 0.986 |
| 21e8b873fe | 0.356 | 0.354 | 1.007 |
| b0a896c3c3 | 0.359 | 0.356 | 1.008 |
| 775d8dda6e | 0.361 | 0.354 | 1.019 |
| 1ba7f7f337 | 0.361 | 0.353 | 1.023 |
| c3cacf2f5f | 0.363 | 0.364 | 0.999 |
| 75c9affa70 | 0.364 | 0.362 | 1.004 |
| ea57db4076 | 0.364 | 0.364 | 0.998 |
| 51139692c8 | 0.369 | 0.366 | 1.007 |
| f48c2a5150 | 0.378 | 0.372 | 1.014 |
| 69c8bd3461 | 0.378 | 0.378 | 1.000 |
| 363adb7a37 | 0.378 | 0.375 | 1.009 |
| 9133d8167a | 0.379 | 0.382 | 0.990 |
| 323f2ccfb8 | 0.383 | 0.382 | 1.004 |
| 31e4e22b2e | 0.385 | 0.387 | 0.995 |
| 51a8931db2 | 0.388 | 0.366 | 1.061 |
| 7f07a469cb | 0.389 | 0.384 | 1.012 |
| e6a3c1fb8c | 0.390 | 0.389 | 1.001 |
| dac6ff750a | 0.391 | 0.391 | 1.001 |
| a170190b5a | 0.392 | 0.396 | 0.991 |
| d96524713d | 0.392 | 0.391 | 1.004 |
| 3405116655 | 0.393 | 0.398 | 0.987 |
| 2789713e31 | 0.395 | 0.386 | 1.023 |
| 8162560177 | 0.395 | 0.390 | 1.013 |
| a1578b537c | 0.395 | 0.385 | 1.026 |
| 02eb3a4510 | 0.396 | 0.390 | 1.016 |
| 7e91afe735 | 0.401 | 0.392 | 1.022 |
| a1ff4b8022 | 0.403 | 0.410 | 0.983 |
| d35040fd68 | 0.403 | 0.401 | 1.006 |
| ed94bd7e99 | 0.406 | 0.409 | 0.993 |
| 4ba5b2c147 | 0.407 | 0.398 | 1.022 |
| 8a6365a3ff | 0.407 | 0.405 | 1.006 |
| 0c5782b28a | 0.412 | 0.411 | 1.001 |
| 4daab7895a | 0.428 | 0.427 | 1.002 |
| ae5d7cdaae | 0.429 | 0.428 | 1.002 |
| d05d104578 | 0.431 | 0.432 | 0.997 |
| e570f69332 | 0.436 | 0.440 | 0.990 |
| 870c24c9cf | 0.436 | 0.435 | 1.004 |
| 7bdcdc8f27 | 0.437 | 0.429 | 1.019 |
| 8f0973fc8f | 0.438 | 0.435 | 1.008 |
| a78522d7eb | 0.441 | 0.438 | 1.007 |
| 301a268219 | 0.444 | 0.435 | 1.021 |
| 609b436e3a | 0.444 | 0.441 | 1.008 |
| b46a9c7ad4 | 0.445 | 0.443 | 1.005 |
| 63e3305540 | 0.446 | 0.445 | 1.002 |
| 0039591d51 | 0.446 | 0.426 | 1.047 |
| 735b92ad53 | 0.452 | 0.447 | 1.011 |
| 03cf426d67 | 0.453 | 0.445 | 1.019 |
| 2dbcfbd160 | 0.454 | 0.449 | 1.010 |
| 2a2c2b4256 | 0.454 | 0.457 | 0.994 |
| 635a47fd26 | 0.457 | 0.449 | 1.018 |
| a808c92923 | 0.457 | 0.453 | 1.008 |
| 4542a08fb0 | 0.458 | 0.467 | 0.980 |
| d26dfdeda4 | 0.463 | 0.466 | 0.993 |
| b00da878bf | 0.464 | 0.457 | 1.014 |
| b77ca6ac9d | 0.465 | 0.456 | 1.019 |
| 740331292d | 0.466 | 0.462 | 1.009 |
| 47da731a5c | 0.478 | 0.472 | 1.013 |
| d53d76f7db | 0.481 | 0.479 | 1.003 |
| 8252421ca2 | 0.483 | 0.478 | 1.012 |
| 0c744b9d8a | 0.484 | 0.482 | 1.004 |
| 482e8a7ed7 | 0.485 | 0.478 | 1.015 |
| e1919aa461 | 0.487 | 0.485 | 1.004 |
| f362a1bba0 | 0.491 | 0.482 | 1.018 |
| 7887b32787 | 0.491 | 0.490 | 1.001 |
| 83098a32c7 | 0.492 | 0.504 | 0.976 |
| 0644d0dd00 | 0.494 | 0.482 | 1.023 |
| 3d312e796e | 0.501 | 0.499 | 1.005 |
| 914abba99c | 0.506 | 0.507 | 0.997 |
| 2f4c1d82ec | 0.551 | 0.541 | 1.017 |
| 4e378cc12e | 0.551 | 0.544 | 1.012 |
| 263788ab64 | 0.552 | 0.557 | 0.992 |
| f27cc3ce5a | 0.556 | 0.557 | 0.998 |
| 4add88f6fb | 0.561 | 0.561 | 0.999 |
| 7d6ad4a7c4 | 0.563 | 0.561 | 1.003 |
| 5c495fe0f3 | 0.567 | 0.574 | 0.988 |
| 776c86e476 | 0.577 | 0.581 | 0.993 |
| 844716c23e | 0.584 | 0.583 | 1.001 |
| 4996bc41b8 | 0.588 | 0.583 | 1.009 |
| 405b357aa4 | 0.602 | 0.594 | 1.014 |
| f69da4fcc8 | 0.604 | 0.602 | 1.003 |
| f932112676 | 0.609 | 0.609 | 0.999 |
| e4546dd17a | 1.069 | 1.067 | 1.002 |
| 3d761d0518 | 1.086 | 1.083 | 1.003 |
| 35728dddcf | 1.091 | 1.089 | 1.002 |
| eef03e6a19 | 1.095 | 1.104 | 0.992 |
| 0350ea6ee2 | 1.190 | 1.194 | 0.997 |

sieve is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image's size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.
