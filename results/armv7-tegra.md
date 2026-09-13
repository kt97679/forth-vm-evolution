# ARMv7 (NVIDIA Tegra), 4 cores, Gentoo

```
uname: Linux 7.2.5-gentoo armv7l
cpu:   ARMv7 Processor rev 3 (v7l)
cores: 4
cc:    cc (Gentoo 16.2.0 p3) 16.2.0
```

A 32-bit host: the native build IS the 4-byte one, so there is no 8-byte
column. Three layout builds per engine, CPU time, two sweeps.
`tools/agree.py`: 36 comparisons, all agreeing at 95% for three
variants, widest spread 4.0%.

## Speed, 4-byte cells, ratio to the cell engine

| stage | kernel | corpus | fib | parse |
|---|---|---|---|---|
| `sod32` | -- | 1.571 | 1.978 | 1.436 |
| `s0-cell` | 1.000 ±0.016 | 1.000 ±0.012 | 1.000 ±0.004 | 1.000 ±0.019 |
| `p4-pack4` | 1.145 ±0.022 | 1.110 ±0.023 | 1.301 ±0.023 | 1.114 ±0.029 |
| `p8-pack8` | 1.081 ±0.024 | 1.049 ±0.021 | 1.261 ±0.012 | 1.053 ±0.019 |
| `s1-sod16` | 1.364 ±0.024 | 1.383 ±0.032 | 1.225 ±0.011 | 1.035 ±0.037 |
| `s2-cpt16` | 1.003 ±0.017 | 0.995 ±0.021 | 0.939 ±0.022 | 0.983 ±0.026 |
| `s3-cpt16f` | 0.870 ±0.012 | 0.880 ±0.009 | 0.884 ±0.019 | 0.870 ±0.012 |
| `s4-cv8` | 0.889 ±0.012 | 0.905 ±0.010 | 0.956 ±0.007 | 0.901 ±0.014 |
| `s5-cv8spec` | 0.788 ±0.009 | 0.772 ±0.007 | 1.021 ±0.026 | 0.784 ±0.014 |
| `s6-cv8b` | 0.834 ±0.009 | 0.843 ±0.007 | 0.956 ±0.007 | 0.885 ±0.014 |

Absolute, roughly 20x the x86 machines:

| stage | kernel ms | corpus ms | fib ms | parse ms |
|---|---|---|---|---|
| `sod32` | -- | 410.24 | 971.56 | 1954.77 |
| `s0-cell` | 293.13 | 261.18 | 491.31 | 1361.64 |
| `s3-cpt16f` | 255.15 | 229.87 | 434.41 | 1185.14 |
| `s5-cv8spec` | 230.95 | 201.66 | 501.80 | 1067.82 |
| `s6-cv8b` | 244.54 | 220.21 | 469.77 | 1204.51 |

## What it says

**The byte-granular header costs less here, but not much less.** `s6`
minus `s5` at 4-byte cells, against the same difference on the Ryzen:

| workload | AMD | ARMv7 | |
|---|---|---|---|
| kernel | +0.056 | +0.046 | 82% of the AMD cost |
| corpus | +0.085 | +0.071 | 84% |
| parse | +0.119 | +0.101 | 85% |

The direction is what a smaller cache predicts - a 0.69x image should
pay for more of its own search cost where memory is dearer - but the
effect is about a sixth of the cost, not all of it. The byte-granular
header remains a size optimisation that costs time, on both
architectures, and parsing remains where it costs most.

**The whole ladder is worth less on ARM.** `s5` against the cell engine
is 0.674 on the Ryzen and 0.788 here: 33% against 21%. That has held
across every ARM measurement in this project.

**`fib` behaves differently here, and that is itself a warning.** Its
error bars on this machine are ±0.004 to ±0.026, tighter than any other
workload, where on the Ryzen the same benchmark gives ±0.023 to ±0.138.
A benchmark whose apparent precision swings by a factor of thirty
between machines is not measuring the thing it claims to.

## A note on LAYOUTS=3

Three variants give a standard error with two degrees of freedom, which
is a poor estimate - and `agree.py` originally reported a disagreement
here (`s1-sod16` on fib) that turned out to be nothing but the 2-sigma
rule being 2.2x too tight at that sample size. The tool now uses
Student's t for the number of variants actually built. Five variants
are worth the extra minutes where the machine can spare them.
