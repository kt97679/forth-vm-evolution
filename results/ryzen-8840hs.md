# Ryzen 7 PRO 8840HS, 16 cores

Two full sweeps, five layout builds per engine, CPU time. `tools/agree.py`
over the two runs: **72 comparisons, every figure agrees within its
stated uncertainty**, widest spread 7.1% (fib/32-bit/p8-pack8).

```
uname: Linux 6.17.0-1030-oem x86_64
cpu:   AMD Ryzen 7 PRO 8840HS w/ Radeon 780M Graphics
cores: 16
cc:    cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
```

## Speed, 64-bit cells, ratio to the cell engine

| stage | kernel | corpus | fib | parse |
|---|---|---|---|---|
| `s0-cell` | 1.000 ±0.038 | 1.000 ±0.034 | 1.000 ±0.069 | 1.000 ±0.032 |
| `p4-pack4` | 1.115 ±0.032 | 1.126 ±0.030 | 1.393 ±0.073 | 1.130 ±0.028 |
| `p8-pack8` | 1.071 ±0.031 | 1.078 ±0.030 | 1.250 ±0.069 | 1.070 ±0.026 |
| `s1-sod16` | 1.351 ±0.039 | 1.437 ±0.036 | 1.180 ±0.065 | 1.020 ±0.025 |
| `s2-cpt16` | 1.010 ±0.036 | 1.019 ±0.034 | 0.984 ±0.058 | 1.027 ±0.031 |
| `s3-cpt16f` | 0.887 ±0.026 | 0.908 ±0.025 | 1.011 ±0.061 | 0.912 ±0.023 |
| `s4-cv8` | 0.893 ±0.026 | 0.923 ±0.024 | 1.088 ±0.060 | 0.934 ±0.023 |
| `s5-cv8spec` | 0.676 ±0.020 | 0.688 ±0.018 | 1.032 ±0.063 | 0.700 ±0.017 |
| `s6-cv8b` | 0.706 ±0.026 | 0.763 ±0.019 | 1.040 ±0.063 | 0.807 ±0.019 |

## Speed, 32-bit cells, ratio to the cell engine

| stage | kernel | corpus | fib | parse |
|---|---|---|---|---|
| `sod32` | -- | 1.393 | 1.574 | 1.336 |
| `s0-cell` | 1.000 ±0.014 | 1.000 ±0.021 | 1.000 ±0.059 | 1.000 ±0.014 |
| `p4-pack4` | 1.168 ±0.034 | 1.204 ±0.029 | 1.379 ±0.064 | 1.186 ±0.031 |
| `p8-pack8` | 1.177 ±0.021 | 1.189 ±0.026 | 1.276 ±0.061 | 1.185 ±0.025 |
| `s1-sod16` | 1.355 ±0.024 | 1.447 ±0.024 | 1.144 ±0.056 | 1.018 ±0.017 |
| `s2-cpt16` | 1.034 ±0.021 | 1.043 ±0.023 | 0.984 ±0.048 | 1.042 ±0.021 |
| `s3-cpt16f` | 0.917 ±0.012 | 0.943 ±0.016 | 1.025 ±0.051 | 0.929 ±0.011 |
| `s4-cv8` | 0.943 ±0.031 | 0.960 ±0.034 | 1.080 ±0.072 | 0.969 ±0.037 |
| `s5-cv8spec` | 0.675 ±0.008 | 0.708 ±0.013 | 1.005 ±0.056 | 0.711 ±0.008 |
| `s6-cv8b` | 0.729 ±0.008 | 0.794 ±0.014 | 0.998 ±0.044 | 0.826 ±0.009 |

Image sizes are machine-independent; see any other file here.

## What this run settles

**The byte-granular header buys size and costs time, and the cost is now
measurable rather than argued about.** `s6` against `s5`, differences
with their combined error:

    kernel compile, 8-byte    +0.030 +/- 0.033   not resolved
    kernel compile, 4-byte    +0.054 +/- 0.011   real
    corpus,         4-byte    +0.086 +/- 0.019   real
    parse,          4-byte    +0.115 +/- 0.012   real

The cost is largest on `parse` and smallest on kernel compilation, which
is the right shape: `parse` is almost nothing but dictionary search, and
searching is exactly what the byte-granular link made more expensive.
Against that, the image is 0.69x of `s5` at 8-byte cells.

**`fib` carries no information.** Five of its eight stages are
indistinguishable from the cell engine at two standard errors, and its
error bars are three to five times those of the other workloads. Now
that the uncertainty is reported rather than hidden, the benchmark says
plainly that it cannot resolve anything - which is what its 15-23%
run-to-run swing was already telling us.
