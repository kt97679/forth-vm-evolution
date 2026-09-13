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

| stage | kernel | corpus | loop | parse |
|---|---|---|---|---|
| `sod32` | -- | 1.484 | 1.512 | 1.429 |
| `s0-cell` | 1.000 | 1.000 | 1.000 | 1.000 |
| `p4-pack4` | 1.122 | 1.100 | 0.974 | 1.110 |
| `p8-pack8` | 1.066 | 1.036 | 0.952 | 1.054 |
| `s1-sod16` | 1.380 | 1.381 | 1.551 | 1.023 |
| `s2-cpt16` | 0.997 | 0.985 | 0.845 | 0.970 |
| `s3-cpt16f` | 0.909 | 0.915 | 0.830 | 0.888 |
| `s4-cv8` | 0.899 | 0.902 | 0.884 | 0.896 |
| `s5-cv8spec` | 0.790 | 0.772 | 0.915 | 0.777 |

Absolute, for scale only - roughly 20x the x86 machines:

| stage | kernel ms | corpus ms | loop ms | parse ms |
|---|---|---|---|---|
| `sod32` | -- | 400.15 | 245.35 | 1955.33 |
| `s0-cell` | 301.64 | 269.59 | 162.31 | 1367.94 |
| `p4-pack4` | 338.55 | 296.42 | 158.13 | 1518.24 |
| `p8-pack8` | 321.63 | 279.23 | 154.45 | 1441.32 |
| `s1-sod16` | 416.19 | 372.33 | 251.77 | 1399.02 |
| `s2-cpt16` | 300.75 | 265.55 | 137.09 | 1327.20 |
| `s3-cpt16f` | 274.27 | 246.72 | 134.72 | 1214.22 |
| `s4-cv8` | 271.28 | 243.22 | 143.51 | 1225.32 |
| `s5-cv8spec` | 238.28 | 208.18 | 148.45 | 1062.66 |

Image sizes are machine-independent and identical to every other run in
this directory - including across the architecture change, which is the
property SOD32's separated engine and image were designed to have.
