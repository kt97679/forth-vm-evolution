# Which numbers survive being measured twice

Two full sweeps on each of two machines, plus the floors the harness
measures per workload. This is the table that decides what the article
may claim.

## Run-to-run swing, same machine, same binaries

Largest change in any stage's ratio between two consecutive sweeps:

| workload | Ryzen 8840HS | ARMv7 Tegra |
|---|---|---|
| `kernel` | 8.1% | **2.0%** |
| `parse` | 7.0% | **1.6%** |
| `corpus` | 12.9% | 3.7% |
| `fib` | 23.1% | 15.1% |

## Measured floor, same runs

`layout-noise.sh`, five semantically identical builds, per workload:

| workload | Ryzen run 1 | Ryzen run 2 | ARM run 1 | ARM run 2 |
|---|---|---|---|---|
| `kernel` | 5.3% | 13.1% | 1.4% | 1.1% |
| `corpus` | 7.8% | 6.3% | 1.0% | 1.3% |
| `parse` | 7.4% | 7.7% | 1.6% | 1.4% |
| `fib` | 22.9% | 16.8% | 14.0% | 6.0% |

## What this says

**The laptop is not a measuring instrument.** Sixteen cores, boost
clocks and a desktop session give a kernel-compile floor that is 5.3%
one minute and 13.1% the next. Nothing under about 13% measured there
means anything, which removes most of the interesting distinctions. The
ARM board - four slow cores, no desktop, nothing else running - resolves
to about 1%.

That is worth saying plainly because the instinct is the opposite: the
fast machine feels like the serious one. For this kind of work the quiet
machine is the serious one, and the fastest hardware available was the
worst tool in the set.

**`fib` is not usable.** It swings 15-23% between consecutive runs on
both machines and its floor is 6-23%. It measures something real - the
call - but it cannot measure it reliably, and no conclusion should rest
on it. It joins `loop`.

Both unreliable workloads are the two SHORT, NARROW ones. Both reliable
workloads are the two that run a large amount of varied code. That is
the pattern, and it is not a coincidence: a tight interpreter loop over
a handful of opcodes is dominated by indirect-branch prediction and code
placement, which is exactly what varies between builds and between runs.

**`kernel` and `parse` are load-bearing.** On the ARM board they repeat
to 2.0% and 1.6% against floors of about 1.4%, which is as good as this
setup gets. `corpus` is usable there too at 3.7%.

## The rule the article follows

Quote ARM numbers for magnitudes. Quote all three machines for the
ordering, which reproduces everywhere. Use `kernel` and `parse` as the
evidence, `corpus` as support, and present `fib` and `loop` as the
finding that microbenchmarks of threaded interpreters do not reproduce -
which is a result about measurement, not about encodings.
