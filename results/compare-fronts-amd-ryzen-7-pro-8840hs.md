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
