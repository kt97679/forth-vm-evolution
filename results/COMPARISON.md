# Three machines

The point of more than one machine is to find out which conclusions are
about the encodings and which are about the box. All three runs are post
I/O-buffering and share sources, images and corpus.

    A  Intel Xeon @ 2.10GHz, 1 vCPU, Firecracker VM     floor 3.1%
    B  AMD Ryzen 7 PRO 8840HS, 16 cores, bare metal     floor 4.3%
    C  ARMv7 (NVIDIA Tegra), 4 cores, Gentoo            floor 1.3%

C is roughly 20x slower than A and B in absolute terms and the quietest
of the three to measure on. It is also a different architecture, and the
images it runs are byte-for-byte the same files - which is the property
SOD32's separated engine and image were designed to have, tested here by
accident rather than on purpose.

## What reproduces on all three

**The ordering.** Kernel compile, corpus and parse rank the stages the
same way everywhere:

    s5-cv8spec < s4-cv8 < s3-cpt16f < s2-cpt16 < s0-cell < p8 < p4 < s1-sod16

**The magnitudes, at 4-byte cells, kernel compile:**

| stage | A | B | C |
|---|---|---|---|
| `p4-pack4` | 1.212 | 1.131 | 1.122 |
| `p8-pack8` | 1.186 | 1.103 | 1.066 |
| `s1-sod16` | 1.411 | 1.298 | 1.380 |
| `s2-cpt16` | 1.019 | 1.022 | 0.997 |
| `s3-cpt16f` | 0.923 | 0.918 | 0.909 |
| `s4-cv8` | 0.875 | 0.878 | 0.899 |
| `s5-cv8spec` | 0.593 | 0.738 | 0.790 |

Six of seven agree within about 0.1 across three machines and two
architectures. SOD16 is a real regression everywhere. Folding and CV8
are a real win everywhere.

**SOD32 is slower than the cell engine on all three**, by 1.3x to 1.7x,
on every workload it can run. Before the hashed word list was restored
it was 2x faster. That is the size of what one omission was costing.

## What varies, and what actually explains it

**The packed schemes depend on CELL WIDTH, not on the machine.** I had
this wrong: seeing the tagged-byte scheme cost 19% on A and nothing on B
at 8-byte cells, I put it down to B's larger caches. Machine C settles
it, because it has no 8-byte column and the numbers still line up by
width rather than by box:

| p8-pack8, kernel compile | 8-byte | 4-byte |
|---|---|---|
| A (Xeon VM) | 1.020 | 1.186 |
| B (Ryzen) | 0.939 | 1.103 |
| C (ARMv7) | -- | 1.066 |

The two 8-byte figures are better than all three 4-byte figures. The
reason is structural rather than architectural: a pack carries one
opcode per remaining byte of the cell, so it folds up to **seven**
operations on an 8-byte cell and only **three** on a 4-byte one. Wider
cells mean fewer packs for the same code, and the per-pack decode is
what the scheme pays for.

So the honest statement is that the tagged-byte scheme is close to free
where cells are wide and costs 7-19% where they are narrow - and CV8
beats it on both axes at both widths on every machine anyway.

**The loop benchmark does not reproduce and should carry no weight.**
It is the only column that disagrees between machines, and it disagrees
in different directions:

| stage | A, 32 | B, 32 | C, 32 |
|---|---|---|---|
| `p8-pack8` | 1.158 | 1.133 | **0.952** |
| `s2-cpt16` | 1.039 | 1.301 | **0.845** |
| `s3-cpt16f` | 0.958 | 1.198 | **0.830** |
| `s5-cv8spec` | 0.750 | 1.084 | 0.915 |

On C every stage but SOD16 beats the cell engine, including both packed
schemes; on B every stage loses to it; on A it is mixed. `loop.fth` is
the narrowest workload - counted loops over stack arithmetic, no
dictionary, no variables, no I/O - which makes it the most exposed to
register allocation and branch prediction, and evidently the least
portable thing measured here. Quote it as the outlier it is, or not at
all.

**CV8 with specialisations is worth most on the slowest machine's
opposite.** 0.593 on A, 0.738 on B, 0.790 on C. The spread is real and
unexplained; three machines is not enough to separate cache size from
issue width from compiler version.

## fib, and the one place the whole ladder loses

`fib.fth` was added late, because nothing else isolated the CALL - the
one operation every encoding here encodes differently. It says something
the other workloads cannot.

On call-dominated code at 4-byte cells, **every stage is slower than
plain cell threading**:

| stage | Ryzen, 8-byte | Ryzen, 4-byte | Xeon VM, 4-byte |
|---|---|---|---|
| `s0-cell` | 1.000 | 1.000 | 1.000 |
| `p4-pack4` | 1.423 | 1.740 | 1.653 |
| `p8-pack8` | 1.200 | 1.647 | 1.716 |
| `s2-cpt16` | 0.776 | 1.267 | 1.064 |
| `s4-cv8` | 0.886 | 1.185 | 1.005 |
| `s5-cv8spec` | 0.775 | 1.048 | 0.881 |

The best non-cell stage is 0.775 at 8-byte cells and 1.048 at 4-byte.
That is not noise, and it has a one-line explanation: a RelF call is a
single relative-offset cell, which is the cheapest call any of these
designs has. Nothing decodes, nothing is computed, the offset IS the
instruction. Every token encoding has to build the target address before
it can jump.

What the token encodings buy back is SIZE, and how much they buy depends
on the width of what they replace. A call costs 8 bytes under cell
threading on a 64-bit host and 2 under CV8 - a saving of 6. At 4-byte
cells the same call costs 4 and 2 - a saving of 2. So the density
argument is roughly three times stronger on a 64-bit host, and on
call-heavy code at 4-byte cells it is not strong enough to pay for the
decode at all.

This is the same axis the packed schemes sorted on, and it unifies them:
everything here is trading decode work for bytes, and the number of
bytes on offer scales with the cell.

The packed schemes fare worst of all on `fib`, which is also structural:
a pack ends at every call, so call-dense code gets almost no packing and
pays the decode anyway.

## A caution about the floor itself

`layout-noise.sh` does not give the same answer twice on the Ryzen:
0.6%, 4.3% and 5.8% across runs, against 3.1-3.4% on the Xeon VM and
1.3% on ARM. The fastest machine is the noisiest, which is what a
laptop with boost clocks and sixteen cores of scheduler should look
like. Take the worst floor seen on a machine, not the latest, and treat
anything under about 6% on the Ryzen as unresolved.

## For the article

State the ordering, which reproduces on three machines and two
architectures. State kernel-compile magnitudes, which agree within 0.1.
Explain the packed schemes by cell width, not by cache. Treat `loop.fth`
as a cautionary tale about narrow benchmarks rather than as evidence.

And note that three machines was enough to overturn an explanation that
two machines had seemed to support.
