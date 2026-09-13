# AMD Ryzen 7 PRO 8840HS, 16 cores

```
uname: Linux 6.17.0-1030-oem x86_64
cpu:   AMD Ryzen 7 PRO 8840HS w/ Radeon 780M Graphics
cores: 16
cc:    cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
```

Five layout builds per engine, CPU time, two sweeps per build, and the
whole thing done from a clean tree three separate times. `tools/agree.py`
across the two sweeps of the last build: **72 comparisons, every figure
inside its stated uncertainty**, widest spread 9.3% (fib/32/s4-cv8).

## Speed, 8-byte cells, ratio to the cell engine

| stage | kernel | corpus | fib | parse |
|---|---|---|---|---|
| `s0-cell` | 1.000 ±0.037 | 1.000 ±0.030 | 1.000 ±0.023 | 1.000 ±0.030 |
| `p4-pack4` | 1.130 ±0.031 | 1.144 ±0.025 | 1.386 ±0.045 | 1.132 ±0.028 |
| `p8-pack8` | 1.090 ±0.030 | 1.086 ±0.025 | 1.259 ±0.056 | 1.070 ±0.027 |
| `s1-sod16` | 1.378 ±0.040 | 1.457 ±0.034 | 1.195 ±0.045 | 1.023 ±0.024 |
| `s2-cpt16` | 1.035 ±0.033 | 1.032 ±0.033 | 1.022 ±0.037 | 1.034 ±0.032 |
| `s3-cpt16f` | 0.897 ±0.027 | 0.913 ±0.025 | 1.011 ±0.024 | 0.908 ±0.025 |
| `s4-cv8` | 0.919 ±0.026 | 0.933 ±0.021 | 1.045 ±0.058 | 0.943 ±0.023 |
| `s5-cv8spec` | 0.688 ±0.019 | 0.705 ±0.017 | 1.073 ±0.028 | 0.698 ±0.015 |
| `s6-cv8b` | 0.731 ±0.020 | 0.771 ±0.017 | 0.985 ±0.068 | 0.799 ±0.018 |

## Speed, 4-byte cells, ratio to the cell engine

| stage | kernel | corpus | fib | parse |
|---|---|---|---|---|
| `sod32` | -- | 1.395 | 1.623 | 1.326 |
| `s0-cell` | 1.000 ±0.017 | 1.000 ±0.010 | 1.000 ±0.038 | 1.000 ±0.013 |
| `p4-pack4` | 1.183 ±0.031 | 1.202 ±0.023 | 1.386 ±0.055 | 1.193 ±0.025 |
| `p8-pack8` | 1.175 ±0.027 | 1.175 ±0.028 | 1.251 ±0.069 | 1.177 ±0.031 |
| `s1-sod16` | 1.372 ±0.023 | 1.439 ±0.019 | 1.161 ±0.045 | 1.024 ±0.015 |
| `s2-cpt16` | 1.024 ±0.021 | 1.032 ±0.021 | 1.006 ±0.028 | 1.047 ±0.021 |
| `s3-cpt16f` | 0.919 ±0.018 | 0.936 ±0.015 | 1.060 ±0.040 | 0.929 ±0.014 |
| `s4-cv8` | 0.938 ±0.032 | 0.973 ±0.031 | 1.131 ±0.056 | 0.965 ±0.030 |
| `s5-cv8spec` | 0.674 ±0.012 | 0.707 ±0.007 | 0.966 ±0.061 | 0.711 ±0.008 |
| `s6-cv8b` | 0.730 ±0.009 | 0.792 ±0.008 | 1.042 ±0.037 | 0.830 ±0.009 |

## The measurement finally survives a rebuild

This is the test the old method failed. Three separate builds of the
same source, each with its own set of layout variants, each swept twice.
Twelve figures compared across all three:

| workload | stage | three builds | spread |
|---|---|---|---|
| kernel 8-byte | `s5` | 0.676 0.683 0.688 | 1.8% |
| kernel 8-byte | `s6` | 0.706 0.727 0.731 | 3.5% |
| kernel 4-byte | `s5` | 0.675 0.690 0.674 | 2.4% |
| kernel 4-byte | `s6` | 0.729 0.749 0.730 | 2.7% |
| parse 4-byte | `s5` | 0.711 0.718 0.711 | 1.0% |
| parse 4-byte | `s6` | 0.826 0.838 0.830 | 1.5% |

All twelve agree inside their error bars. Under the single-build method a
rebuild moved a stage by five or ten percent with nothing to warn you.

## What the byte-granular header costs

`s6` minus `s5`, measured three times from scratch:

    kernel, 8-byte    +0.030 +0.044 +0.043    mean +0.039
    kernel, 4-byte    +0.054 +0.059 +0.056    mean +0.056
    corpus, 4-byte    +0.086 +0.086 +0.085    mean +0.086
    parse,  4-byte    +0.115 +0.120 +0.119    mean +0.118

The corpus figure reproduces to a thousandth across three independent
builds. The cost is smallest on kernel compilation and largest on
parsing, which is the shape the design predicts: `parse.fth` is almost
nothing but dictionary search, and the variable-length link is what made
searching dearer. Against it, the image is 0.69x of `s5` at 8-byte cells
and 0.31x of cell threading.

## One stage is three times more layout-sensitive than its neighbours

Standard errors at 4-byte cells on kernel compilation:

    s1 0.024   s2 0.020   s3 0.015   s4 0.032   s5 0.010   s6 0.009

`s4-cv8` is consistently the widest, across every build and both widths,
and on `fib` at 4-byte cells one build put it at ±0.138. It is the only
stage compiled with `VARCALL=0 VARSLOT=0` - fixed-width call and slot
fields - so its dispatch loop has a different shape from every
neighbour's, and that shape is evidently more sensitive to where the
compiler puts it. Not chased further; recorded because an error bar that
varies by stage is itself a result, and it is invisible without building
each stage more than once.
