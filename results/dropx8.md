# The compiler's X8 copies, dropped: the gene `dropx8`

*Since Iteration 39 part of the gene `lean` (results/lean.md), which also
leaves out the dump tool and dead shadowed words.*

Iteration 38. Every CV8 image carries the compiler that writes CV8 at run
time (forth/cv8.4, cv8b.4, and with run-time fusion cv8-fuse.4). They are
written as `X8` words - IF8, ;8, COMPILE,8 - because redefining `;` in the
cell system would break the cell compiler mid-build; the converter gives
each X the body of its X8 (tools/layout.py, phase 3). The X8 words stayed,
"harmlessly", its comment said. Not for size: **25-27 copies, 751-1,080
bytes, 7.7-8.1% of seed 6's front designs**, priced with SYMMAP and
CALLMAP before anything was built.

Only two were reached at all: CREATE8 and NAME>8, called from copied
bodies (VARIABLE, carrying VARIABLE8's, calls CREATE8) - and (POSTPONE)
operands may point at any of them. `--drop-x8`: every call to a swapped
X8 goes to its X - the same code - a (POSTPONE) operand of one resolves to
its X, and the X8 words leave `order`, so the hash threads, links and
offsets are laid out without them.

## Checks

- The designs without the gene: hand-made stages IDENTICAL; seed 6's
  422d6bcbca and cd943ed219 at their recorded sizes; all 1,309 of seed 6's
  ids unchanged (dropx8 is in LATE).
- With it: both alive (the corpus and the kernel's rebuild); IF ELSE THEN,
  BEGIN UNTIL, DO LOOP, VARIABLE, CONSTANT and CREATE DOES> compiled at
  run time, all giving the recorded designs' answers.

## Measured: image against image, one engine (development VM)

`lab/evolve/image-ab.py <seed 6's front, all ten> --set dropx8=1 --env
SOD16_NO_DROPX8=1 --rounds 5`:

pinned to cpu 0 (it and its sibling 0% busy; BENCH_CPU=N to choose)
| design | size A | size B | B - A | dispatches B / A: kernel, fib, parse, corpus, loop | time B / A: kernel, fib, parse, corpus, loop | selection |
|---|---|---|---|---|---|---|
| 422d6bcbca | 9327 | 8558 | -769 | 0.996, 1.000, 0.976, 0.986, 1.041 | 0.918, 1.013, 0.971, 1.004, 0.934 | 0.976 |
| 6495dcb5dd | 9343 | 8574 | -769 | 0.996, 1.000, 0.975, 0.985, 1.041 | 1.011, 1.013, 0.983, 0.816, 1.030 | 0.952 |
| c40ba92d5b | 9511 | 8719 | -792 | 0.996, 1.000, 0.972, 0.985, 1.000 | 0.940, 0.964, 0.948, 1.047, 1.016 | 0.974 |
| c61857fc89 | 10034 | 9074 | -960 | 0.991, 1.000, 0.965, 0.982, 1.000 | 0.960, 1.105, 0.839, 0.742, 1.165 | 0.901 |
| b06a4cf784 | 10246 | 9206 | -1040 | 0.991, 1.000, 0.964, 0.982, 1.000 | 1.002, 1.000, 0.944, 0.981, 1.004 | 0.981 |
| af5e8dc29f | 10254 | 9214 | -1040 | 0.991, 1.000, 0.964, 0.982, 1.000 | 0.987, 1.010, 0.948, 1.016, 0.999 | 0.990 |
| a74b828e9b | 13073 | 12289 | -784 | 0.998, 1.000, 0.983, 0.992, 1.000 | 1.005, 1.044, 0.964, 1.033, 1.010 | 1.011 |
| dc02ceae31 | 13161 | 12377 | -784 | 0.998, 1.000, 0.984, 0.992, 1.000 | 0.931, 0.941, 0.965, 0.929, 0.991 | 0.941 |
| 15dde12f04 | 13345 | 12513 | -832 | 0.998, 1.000, 0.984, 0.992, 1.000 | 1.040, 0.995, 0.976, 0.996, 0.974 | 1.002 |
| cd943ed219 | 14081 | 12961 | -1120 | 0.992, 1.000, 0.976, 0.990, 1.000 | 1.005, 1.040, 1.015, 0.990, 1.009 | 1.012 |

**6-10% smaller, 769-1,120 bytes, and no slower**: the dictionary threads
are shorter, so kernel, parse and corpus run 0.2-3.6% fewer dispatches;
fib does not move. loop's +4.1% on the two smallest is the alignment
artefact Iteration 13 found - the image size mod 8 sets the NOOPs the
run-time compiler pads before (LOOP) - and loop is held out. Free, so
evolution should take it everywhere: a gene only so the recorded designs
keep building as recorded. seed 6's smallest would be 8,558 bytes.
