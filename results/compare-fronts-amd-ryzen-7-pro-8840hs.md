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
