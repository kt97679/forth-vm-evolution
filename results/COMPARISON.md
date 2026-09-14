# Two machines, measured the same way

Superseded everything written before the harnesses averaged over layout
builds. Those earlier files quoted single-build figures which repeat to
1% and can be wrong by 12%; they have been deleted rather than
annotated, because a wrong number with a caveat is still a wrong number
someone will quote.

    AMD Ryzen 7 PRO 8840HS, 16 cores   5 layout builds, 3 separate trees
    ARMv7 (Tegra), 4 cores, Gentoo     3 layout builds, 1 tree

Both swept twice. `tools/agree.py`: every figure on both machines agrees
with itself within its stated uncertainty.

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

## Method notes worth keeping

The per-build bias is larger than the run noise, and the BASELINE had
the widest spread of any stage at 12.6% - it divides every ratio here.

`s4-cv8` is consistently about three times more layout-sensitive than
its neighbours (SE 0.032 against 0.009-0.020) on every build and both
widths. It is the only stage compiled `VARCALL=0 VARSLOT=0`. Unexplained;
recorded because a per-stage error bar is itself a result.
