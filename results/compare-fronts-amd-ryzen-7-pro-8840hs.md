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
