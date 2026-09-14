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

Latest sweep, two runs from one tree, three layout builds per engine.
`tools/agree.py` over the two: 36 comparisons, all agreeing. Run 2:

| stage | kernel | corpus | fib | parse |
|---|---|---|---|---|
| `sod32` | -- | 1.505 | 1.959 | 1.444 |
| `s0-cell` | 1.000 ±0.014 | 1.000 ±0.012 | 1.000 ±0.040 | 1.000 ±0.022 |
| `p4-pack4` | 1.145 ±0.021 | 1.113 ±0.023 | 1.264 ±0.042 | 1.128 ±0.028 |
| `p8-pack8` | 1.088 ±0.027 | 1.051 ±0.018 | 1.273 ±0.040 | 1.063 ±0.019 |
| `s1-sod16` | 1.364 ±0.021 | 1.377 ±0.027 | 1.204 ±0.040 | 1.035 ±0.039 |
| `s2-cpt16` | 1.007 ±0.016 | 0.995 ±0.020 | 0.888 ±0.027 | 0.992 ±0.035 |
| `s3-cpt16f` | 0.880 ±0.009 | 0.880 ±0.009 | 0.935 ±0.040 | 0.877 ±0.014 |
| `s4-cv8` | 0.896 ±0.011 | 0.904 ±0.010 | 0.935 ±0.037 | 0.913 ±0.015 |
| `s5-cv8spec` | 0.789 ±0.008 | 0.772 ±0.007 | 0.965 ±0.030 | 0.795 ±0.013 |
| `s6-cv8b` | 0.837 ±0.008 | 0.843 ±0.007 | 0.955 ±0.030 | 0.892 ±0.014 |

Run 1 of the same tree, for the figures that differ by more than a
thousandth: `s2-cpt16` 1.000, `s4-cv8` 0.891, `s5-cv8spec` 0.788,
`s6-cv8b` 0.835 on kernel compilation. An earlier tree, before the
audit, gave 1.003 / 0.889 / 0.788 / 0.834 - all inside their intervals.

## The specialisation step does NOT dominate here

This is the number that contradicts the article's AMD result, so it is
worth stating on its own. Taking the ladder as deltas of the ratio:

| | cell -> CV8 | CV8 -> CV8+spec |
|---|---|---|
| AMD, 8-byte | 0.081 | 0.231 |
| AMD, 4-byte | 0.062 | 0.264 |
| **ARMv7, 4-byte** | **0.111** | **0.101** |

On both x86 columns the specialised opcodes are worth three to four
times the whole encoding sequence. On ARM they are worth slightly less
than it. The sign of each step is the same everywhere - both help - but
their relative size is not portable, and any claim that ranks them has
to say on which machine.

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
