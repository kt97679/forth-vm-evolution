# Two machines, measured the same way

Superseded everything written before the harnesses averaged over layout
builds. Those earlier files quoted single-build figures which repeat to
1% and can be wrong by 12%; they have been deleted rather than
annotated, because a wrong number with a caveat is still a wrong number
someone will quote.

    AMD Ryzen 7 PRO 8840HS, 16 cores   5 layout builds, 3 separate trees
    ARMv7 (Tegra), 4 cores, Gentoo     3 layout builds, 1 tree

Both swept twice. `tools/agree.py`: every figure on both machines agrees
with itself within its stated uncertainty. The CV8-against-SPN section
is the Ryzen alone: SPN runs on x86-64 only.

## Ratios to the cell engine, 4-byte cells

| stage | AMD kernel | ARM kernel | AMD parse | ARM parse |
|---|---|---|---|---|
| `p4-pack4` | 1.183 | 1.145 | 1.193 | 1.114 |
| `p8-pack8` | 1.175 | 1.081 | 1.177 | 1.053 |
| `s1-sod16` | 1.372 | 1.364 | 1.024 | 1.035 |
| `s2-cpt16` | 1.024 | 1.003 | 1.047 | 0.983 |
| `s3-cpt16f` | 0.919 | 0.870 | 0.929 | 0.870 |
| `s4-cv8` | 0.938 | 0.889 | 0.965 | 0.901 |
| `s5-cv8spec` | 0.674 | 0.788 | 0.711 | 0.784 |
| `s6-cv8b` | 0.730 | 0.834 | 0.830 | 0.885 |

Typical errors: ±0.01 to ±0.03 on both machines, so a difference under
about 0.05 between the two columns is not a difference.

## What reproduces on both

**The ordering.** Identical on kernel compilation, corpus and parse.

**SOD16 is a real regression**, 1.36-1.37 on both, the worst stage
anywhere. The word table costs more than it saves.

**CPT16 is indistinguishable from the cell engine**: 1.024 ±0.021 and
1.003 ±0.017. Removing the word table and the compiler bookkeeping that
went with it closes the whole of SOD16's deficit; nothing here separates
the two contributions.

**The packed schemes cost 5-20%** and never win, on either machine.

## What differs, and by how much

**The ladder is worth less on ARM.** `s5` is 0.674 on the Ryzen and
0.788 on the Tegra - 33% against 21%. Consistent across every ARM
measurement in this project.

**The byte-granular header costs slightly less on ARM**, 82-85% of the
AMD cost on every workload. The direction a smaller cache predicts, but
a sixth of the cost rather than all of it. It stays a size optimisation
that costs time, on both architectures.

## `fib` and `loop` are not evidence

`loop.fth` is out of the default sweep: 17.5% resolution floor, 21%
swing between runs of the same binary on the same board.

`fib.fth` is still measured and should not be quoted. Its error bars are
±0.023 to ±0.138 on the Ryzen and ±0.004 to ±0.026 on the Tegra - an
apparent precision differing thirtyfold between machines. On the Ryzen
five of its eight stages are indistinguishable from the cell engine.

Both are the short, narrow workloads. Both reliable ones run a lot of
varied code. That is the pattern, and it is the article's one result
about measurement rather than about encodings.

## CV8 against SPN - the Ryzen only

SPN runs on x86-64 only, so this is one machine: the Ryzen, in CPU
cycles (`tools/bench-laptop.sh` at 60b5f39; the files are
`amd-ryzen-7-pro-8840hs-x86_64-*.md` here). s8 is CV8 plus a
translator: the same byte code, about 235 words turned into native code
and about 100 refused and left interpreted.

**Once running** - net of start-up, 8-byte cells, ratio to the cell
engine, mean of two sweeps:

| stage | kernel | corpus | fib | parse |
|---|---|---|---|---|
| `s4-cv8` | 0.903 | 0.929 | 1.095 | 0.933 |
| `s5-cv8spec` | 0.677 | 0.698 | 1.026 | 0.700 |
| `s6-cv8b` | 0.722 | 0.776 | 1.036 | 0.814 |
| `s7-spn` | 0.311 | 0.302 | 0.110 | 0.314 |
| `s8-spncv8` | 0.292 | 0.322 | 0.111 | 0.314 |
| `s8-lazy` | 0.312 | 0.351 | 0.124 | 0.304 |

Errors about ±0.02 for the interpreters (±0.04 on fib) and ±0.008 for
SPN (±0.004 on fib). s8-spncv8 is 2.4-2.6x faster than `s6-cv8b`, the
CV8 it is built on, on the three workloads that are evidence, and
2.2-2.3x faster than `s5-cv8spec`, the fastest CV8. On fib the gap is
ninefold - wide enough to survive the error bars that make fib's
interpreter figures unquotable above.

**End to end** - CPU time, ms, start-up included:

| stage | start-up | kernel | fib | corpus | parse |
|---|---|---|---|---|---|
| `s5-cv8spec` | 0.55 | 10.51 | 34.92 | 8.40 | 40.39 |
| `s6-cv8b` | 0.55 | 11.15 | 33.29 | 9.38 | 46.80 |
| `s8-lazy` | 1.51 | 6.21 | 5.63 | 5.57 | 19.00 |
| `s8-spncv8` | 1.76 | 6.20 | 5.34 | 5.50 | 19.93 |
| `s8-full` | 6.48 | 11.06 | 10.24 | 10.16 | 24.66 |
| `s7-spn` | 1.93 | 6.64 | 5.53 | 5.41 | 19.96 |

SPN starts 1-1.2 ms later and repays it once a program would run about
2 ms under CV8; a shorter script finishes sooner on CV8. `s8-full`
translates the whole dictionary at every start, and wins only on long
runs.

**Why it is faster** - end to end, instructions and instructions per
cycle:

| workload | `s6-cv8b` | per cycle | `s8-spncv8` | per cycle |
|---|---|---|---|---|
| kernel | 114.2 M | 2.31 | 66.8 M | 2.61 |
| fib | 378.2 M | 2.44 | 76.9 M | 3.41 |
| corpus | 93.5 M | 2.26 | 60.9 M | 2.68 |
| parse | 507.2 M | 2.36 | 247.8 M | 2.78 |

35-80% fewer instructions - no fetch, decode and dispatch per
operation - and 13-40% more per cycle, most likely from losing the
dispatch jumps (mispredictions not measured). The CV8 interpreters run
2.3-2.4 instructions per cycle against the cell engine's 2.6-2.8: the
compact byte code costs cycles to decode.

**What SPN costs:**

| | `s6-cv8b` | `s8-lazy` | `s8-spncv8` | `s8-full` |
|---|---|---|---|---|
| image, bytes | 9,881 | 32,220 | 36,897 | 23,652 |
| start-up, ms | 0.55 | 1.51 | 1.76 | 6.48 |
| native code at start | - | 66 KB | 105 KB | 105 KB |
| private memory, corpus | 148 KB | 336 KB | 332 KB | 352 KB |

Private memory is resident memory less the shared libraries. The engine
is 28.3 KB of machine code against 19.7 KB; SPN adds 1,171 lines of
Forth (translator, recorder, saver) and 199 of C (stencils, markers).
`s7-spn` reached the same speed with a 103,441-byte image.

**What CV8 keeps:** every platform a C compiler reaches - it is the only
one of the two measured on the Tegra - both cell widths, no executable
memory, and images that are plain data, independent of the engine
build and byte-reproducible. SPN images are tied to their engine build
and are not yet reproducible: pointer variables are saved with
addresses that change every run.

## Method notes worth keeping

The per-build bias is larger than the run noise, and the BASELINE had
the widest spread of any stage at 12.6% - it divides every ratio here.

`s4-cv8` is consistently about three times more layout-sensitive than
its neighbours (SE 0.032 against 0.009-0.020) on every build and both
widths. It is the only stage compiled `VARCALL=0 VARSLOT=0`. Unexplained;
recorded because a per-stage error bar is itself a result.
