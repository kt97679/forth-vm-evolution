# Branch misses by handler on the AMD Ryzen 7 PRO 8840HS (Iteration 301)

lab/evolve/missmap.py on the laptop (pack forth-vm-evolution-missmap-4282d4e17-fury-20261015-135020),
seed 51's front - the first run where it ran the unstripped engine (engine.full; its first try,
Iteration 297, ran the stripped one and attributed nothing). A sample every 500 user-space branch
misses; each sample's source line charged to the handler whose label comes last before it.

## What it says

- **(FIND) in C (L_x_find) is the largest single source on the interpreter's work**: 9-13% of the
  fast designs' misses on kernel and corpus - its walk along a thread's chain, comparing names, a
  loop whose length the data decides. The fast designs all chose 16 threads, the fewest the gene
  threads offers (Iteration 204: 16, 32, 64, 128 chains) - longer chains, less memory.
- **Calls and returns together, 15-25%** (L_t2call2, L_t2call4, L_exit): after a call or an EXIT
  the next operation depends on where the program is, and one shared indirect jump predicts it.
- **The JIT design: about 20% before any handler's label** - C before the handlers, its own
  runtime most likely; the design without the JIT has none there.
- Caveats: a few hundred samples a run; and where GCC merges handlers' final jumps into one, a
  dispatch's miss is charged to the handler holding the merged jump - s6's L_t2bad (a fault
  handler, 9-12% of its samples) is most likely that.

## The tables

# Branch misses by handler - lab/evolve/missmap.py

Sampled every 500 user-space branch misses (perf record), 1 run(s) a workload, by /usr/lib/linux-tools/6.8.0-147-generic/perf (perf version 6.8.12); a sample's source line charged to the handler whose label precedes it. Host: AMD Ryzen 7 PRO 8840HS w/ Radeon 780M Graphics.

## s6 on kernel - 105 samples

| handler | samples | share |
|---|---|---|
| L_t2bad | 13 | 12.4% |
| (before any handler) | 7 | 6.7% |
| L_0branch | 7 | 6.7% |
| L_drop | 6 | 5.7% |
| L_eq | 6 | 5.7% |
| L_dup | 5 | 4.8% |
| L_rot | 5 | 4.8% |
| L_over | 5 | 4.8% |
| L_noop | 4 | 3.8% |
| L_exit | 3 | 2.9% |

## s6 on corpus - 347 samples

| handler | samples | share |
|---|---|---|
| L_0branch | 41 | 11.8% |
| L_t2bad | 33 | 9.5% |
| L_dup | 19 | 5.5% |
| (before any handler) | 18 | 5.2% |
| L_lit8 | 17 | 4.9% |
| L_drop | 17 | 4.9% |
| L_eq | 14 | 4.0% |
| L_tor | 13 | 3.7% |
| L_dovar | 12 | 3.5% |
| L_noop | 11 | 3.2% |

## f7a7740238 on kernel - 183 samples

| handler | samples | share |
|---|---|---|
| (before any handler) | 36 | 19.7% |
| L_x_find | 20 | 10.9% |
| L_t2call4 | 15 | 8.2% |
| L_exit | 13 | 7.1% |
| L_t2call2 | 9 | 4.9% |
| L_vf | 8 | 4.4% |
| (no source line) | 6 | 3.3% |
| L_dup | 5 | 2.7% |
| L_tor | 5 | 2.7% |
| L_sub | 4 | 2.2% |

## f7a7740238 on corpus - 589 samples

| handler | samples | share |
|---|---|---|
| (before any handler) | 130 | 22.1% |
| L_x_find | 79 | 13.4% |
| L_t2call2 | 44 | 7.5% |
| L_exit | 36 | 6.1% |
| L_vf | 31 | 5.3% |
| L_t2call4 | 25 | 4.2% |
| L_x_qbr8 | 21 | 3.6% |
| L_lit8 | 19 | 3.2% |
| L_x_parse | 17 | 2.9% |
| L_dovar | 16 | 2.7% |

## a124348f83 on kernel - 390 samples

| handler | samples | share |
|---|---|---|
| L_t2call4 | 44 | 11.3% |
| L_t2call2 | 37 | 9.5% |
| L_x_find | 34 | 8.7% |
| L_exit | 28 | 7.2% |
| L_vf | 26 | 6.7% |
| L_dovar | 23 | 5.9% |
| L_lit8 | 15 | 3.8% |
| L_plus | 13 | 3.3% |
| L_cstore | 11 | 2.8% |
| L_x_parse | 9 | 2.3% |

## a124348f83 on corpus - 498 samples

| handler | samples | share |
|---|---|---|
| L_x_find | 66 | 13.3% |
| L_t2call2 | 47 | 9.4% |
| L_vf | 31 | 6.2% |
| L_exit | 30 | 6.0% |
| L_t2call4 | 23 | 4.6% |
| L_x_parse | 22 | 4.4% |
| L_lit8 | 18 | 3.6% |
| L_plus | 17 | 3.4% |
| (before any handler) | 16 | 3.2% |
| L_dup | 14 | 2.8% |

## 0285b1954f on kernel - 1610 samples

| handler | samples | share |
|---|---|---|
| L_t2call2 | 199 | 12.4% |
| L_t2call4 | 120 | 7.5% |
| L_dodoes | 120 | 7.5% |
| L_x_qbr8 | 85 | 5.3% |
| L_dovar | 81 | 5.0% |
| L_dup | 79 | 4.9% |
| L_eqix | 67 | 4.2% |
| L_rfetch | 65 | 4.0% |
| (before any handler) | 54 | 3.4% |
| L_lit8 | 49 | 3.0% |

## 0285b1954f on corpus - 4958 samples

| handler | samples | share |
|---|---|---|
| L_t2call2 | 599 | 12.1% |
| L_dodoes | 359 | 7.2% |
| L_t2call4 | 331 | 6.7% |
| L_x_qbr8 | 302 | 6.1% |
| L_dovar | 249 | 5.0% |
| L_dup | 246 | 5.0% |
| L_rfetch | 208 | 4.2% |
| L_eqix | 201 | 4.1% |
| (before any handler) | 179 | 3.6% |
| L_swap | 171 | 3.4% |

