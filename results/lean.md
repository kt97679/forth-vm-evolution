# Build artifacts left out of the image: the gene `lean`

Iteration 39 - Iteration 38's `dropx8`, renamed (no recorded design used
it yet) and extended. An image is made by dumping the dictionary the
build loaded; three kinds of words came along that the running system
never uses:

- **the compiler's X8 copies** (Iteration 38): each X carries its X8's
  body, and the X8 words stayed - calls and (POSTPONE)s to them now go to
  X; `--drop-x8`;
- **the dump tool**: tools/dict-dump-addr.4 is loaded last, to write this
  very dump - NFA BP BE NFATAB #NFA TA CELLB INIT-NFATAB COLLECT SWAPC
  SORTNFA DUMP, 490-688 bytes of seed 6's front; `--drop-dumptool`, from
  the last NFA on, only if every word there is the tool's and nothing
  refers to one;
- **dead shadowed words**: defined again under the same name, so no
  longer reachable by name, and called or (POSTPONE)d by nothing - cv8.4's
  FOLD-OP under cv8-fuse.4's; the same option.

Words the system runs by name - `;`, LOOP, DOES>, EVALUATE - are never
called from code either, and stay: "never called" is not "unused".

## Checks

Without the gene: the hand-made stages IDENTICAL, seed 6's designs at
their recorded sizes, all 1,309 ids unchanged (lean is in LATE). With it,
on 422d6bcbca and cd943ed219: alive (the corpus, the kernel's rebuild),
and IF ELSE THEN, BEGIN UNTIL, DO LOOP, VARIABLE, CONSTANT and CREATE
DOES> compiled at run time give the recorded designs' answers.

## Measured: image against image, one engine (development VM)

`lab/evolve/image-ab.py <seed 6's front, all ten> --set lean=1 --env
SOD16_NO_LEAN=1 --rounds 5`:

pinned to cpu 0 (it and its sibling 0% busy; BENCH_CPU=N to choose)
| design | size A | size B | B - A | dispatches B / A: kernel, fib, parse, corpus, loop | time B / A: kernel, fib, parse, corpus, loop | selection |
|---|---|---|---|---|---|---|
| 422d6bcbca | 9327 | 8060 | -1267 | 0.994, 1.000, 0.966, 0.979, 1.124 | 0.989, 1.001, 0.858, 1.035, 1.082 | 0.968 |
| 6495dcb5dd | 9343 | 8076 | -1267 | 0.994, 1.000, 0.964, 0.978, 1.124 | 1.000, 0.997, 0.921, 1.052, 1.104 | 0.992 |
| c40ba92d5b | 9511 | 8164 | -1347 | 0.994, 1.000, 0.962, 0.978, 1.124 | 0.950, 0.994, 0.935, 1.004, 1.084 | 0.970 |
| c61857fc89 | 10034 | 8516 | -1518 | 0.989, 1.000, 0.948, 0.975, 1.284 | 1.043, 1.006, 0.871, 0.925, 1.236 | 0.959 |
| b06a4cf784 | 10246 | 8618 | -1628 | 0.989, 1.000, 0.947, 0.975, 0.841 | 0.988, 0.989, 0.941, 0.988, 0.875 | 0.976 |
| af5e8dc29f | 10254 | 8626 | -1628 | 0.989, 1.000, 0.947, 0.975, 0.841 | 0.998, 1.129, 0.994, 0.971, 0.840 | 1.021 |
| a74b828e9b | 13073 | 11673 | -1400 | 0.997, 1.000, 0.975, 0.987, 1.000 | 1.134, 0.909, 0.832, 1.006, 1.002 | 0.964 |
| dc02ceae31 | 13161 | 11721 | -1440 | 0.997, 1.000, 0.975, 0.988, 1.000 | 0.993, 1.003, 1.106, 0.915, 1.079 | 1.002 |
| 15dde12f04 | 13345 | 11801 | -1544 | 0.997, 1.000, 0.976, 0.988, 1.000 | 1.015, 0.992, 0.979, 0.878, 1.074 | 0.964 |
| cd943ed219 | 14081 | 12185 | -1896 | 0.991, 1.000, 0.963, 0.985, 1.000 | 1.014, 0.983, 0.983, 1.076, 0.990 | 1.013 |

**12-16% smaller - 1,267-1,896 bytes - and no slower**: kernel, parse and
corpus 1-5% fewer dispatches (shorter dictionary threads), fib unchanged.
loop swings both ways (0.84-1.28 in dispatches): the image size mod 8 sets
the NOOPs the run-time compiler pads before (LOOP) - executed on every
pass (Iteration 13's artefact; loop is held out).

**And rtimm gets cheaper**: its overlay's X8 copies go too. c61857fc89:
rtimm +408 bytes, with lean +278; cd943ed219: +472, with lean +336.
