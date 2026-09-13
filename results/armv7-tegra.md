# Results

Measured on:

```
date: 2026-09-13 05:25Z
uname: Linux 7.2.5-gentoo armv7l
cpu: ARMv7 Processor rev 3 (v7l), NVIDIA Tegra
cores: 4
cc: cc (Gentoo 16.2.0 p3) 16.2.0
```

A 32-bit host: the native build IS the 4-byte one, and an 8-byte column
does not exist on this machine.

Resolution floor from `tools/layout-noise.sh`: **1.3%** - the quietest
of the three machines measured.

## Speed, 32-bit cells, relative to the cell engine

Second run, with `fib` added. The kernel, corpus and parse columns
repeat the first run to within about 1%; the loop column does not
repeat itself at all - see `COMPARISON.md`.

| stage | kernel | corpus | loop | fib | parse |
|---|---|---|---|---|---|
| `sod32` | -- | 1.478 | 1.495 | 1.922 | 1.396 |
| `s0-cell` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `p4-pack4` | 1.128 | 1.095 | 0.991 | 1.290 | 1.094 |
| `p8-pack8` | 1.062 | 1.025 | 0.956 | 1.257 | 1.036 |
| `s1-sod16` | 1.371 | 1.405 | 1.576 | 1.186 | 0.994 |
| `s2-cpt16` | 0.992 | 0.979 | 0.948 | 0.947 | 0.957 |
| `s3-cpt16f` | 0.902 | 0.916 | 0.754 | 0.918 | 0.882 |
| `s4-cv8` | 0.890 | 0.904 | 1.069 | 0.932 | 0.886 |
| `s5-cv8spec` | 0.783 | 0.770 | 0.855 | 0.991 | 0.759 |

Absolute, for scale only - roughly 20x the x86 machines:

| stage | kernel ms | corpus ms | loop ms | fib ms | parse ms |
|---|---|---|---|---|---|
| `sod32` | -- | 400.37 | 244.71 | 984.17 | 1922.29 |
| `s0-cell` | 301.95 | 270.97 | 163.74 | 512.07 | 1376.66 |
| `p4-pack4` | 340.45 | 296.59 | 162.33 | 660.39 | 1505.52 |
| `p8-pack8` | 320.56 | 277.69 | 156.59 | 643.60 | 1426.71 |
| `s1-sod16` | 413.84 | 380.80 | 258.10 | 607.46 | 1368.25 |
| `s2-cpt16` | 299.47 | 265.41 | 155.28 | 485.04 | 1318.06 |
| `s3-cpt16f` | 272.38 | 248.29 | 123.54 | 470.18 | 1213.80 |
| `s4-cv8` | 268.79 | 245.03 | 175.08 | 477.49 | 1220.31 |
| `s5-cv8spec` | 236.45 | 208.64 | 139.94 | 507.23 | 1044.81 |

Image sizes are machine-independent and identical to every other run in
this directory - including across the architecture change, which is the
property SOD32's separated engine and image were designed to have.
