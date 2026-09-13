# Two machines

The whole point of a second machine is to find out which conclusions are
about the encodings and which are about the box. Both runs are post
I/O-buffering and use the same sources, images and corpus.

    A  Intel Xeon @ 2.10GHz, 1 vCPU, Firecracker VM   floor 3.4%
    B  AMD Ryzen 7 PRO 8840HS, 16 cores, bare metal   floor 4.3%

## What reproduces

**The ordering, on three workloads out of four.** Kernel compile, corpus
and parse rank the eight stages identically on both machines:

    s5-cv8spec < s4-cv8 < s3-cpt16f < s2-cpt16 < s0-cell < p8 < p4 < s1-sod16

**The magnitudes, mostly.** Kernel compile at 4-byte cells:

| stage | A | B |
|---|---|---|
| `p4-pack4` | 1.212 | 1.131 |
| `p8-pack8` | 1.186 | 1.103 |
| `s1-sod16` | 1.411 | 1.298 |
| `s2-cpt16` | 1.019 | 1.022 |
| `s3-cpt16f` | 0.923 | 0.918 |
| `s4-cv8` | 0.875 | 0.878 |
| `s5-cv8spec` | 0.593 | 0.738 |

Five of seven agree to within the noise floor. SOD16 is a real
regression on both. CV8 and folding are a real win on both.

**That SOD16 is the worst stage, and that its parse column is the
exception.** Both machines put SOD16 last everywhere except parsing,
where it comes level with the cell engine (0.99 / 1.02). The far-call
escape explains it: `parse.fth` runs inside translated kernel code,
where SOD16's table calls survive.

## What does not reproduce, and matters

**The packed schemes are machine-dependent, and that reverses a
conclusion.** At 8-byte cells on machine B:

| stage | kernel | corpus | loop | parse |
|---|---|---|---|---|
| `p8-pack8` | 0.939 | 0.990 | 0.993 | 0.971 |

The tagged-byte scheme costs **nothing** there - if anything it is
slightly ahead - while on machine A it cost 15-25%. It is also 0.857x
the size. So "packing buys density and costs speed" is true on a
cache-poor VM and false on a laptop with a real cache hierarchy.

This is precisely the effect `pack-bench.c` excluded by design in 2024:
its streams were sized to stay hot, so density earned no credit, and its
header called that the pessimistic case. It was pessimistic on machine
A. On machine B it was wrong about the sign.

CV8 still dominates both packed schemes on both axes on both machines -
0.813 against 0.939 on speed, 0.47x against 0.86x on size - so the
decision survives. The *reason* does not.

**Machine B's 4-byte loop column disagrees with everything else.** Every
stage comes out slower than the cell engine there, including the ones
that are faster at 8-byte cells on the same machine and faster at 4-byte
cells on machine A:

| stage | B, loop 64 | B, loop 32 | A, loop 32 |
|---|---|---|---|
| `s2-cpt16` | 0.983 | 1.301 | 1.039 |
| `s3-cpt16f` | 0.908 | 1.198 | 0.958 |
| `s4-cv8` | 1.038 | 1.178 | 0.907 |
| `s5-cv8spec` | 0.783 | 1.084 | 0.750 |

`loop.fth` is the narrowest workload - counted loops over stack
arithmetic, no dictionary, no variables, no I/O - so it is the one most
exposed to register allocation, and i386 has eight registers to x86-64's
sixteen. A plausible story is that the token engines' decode state
spills on the 32-bit build of machine B's compiler and not on machine
A's, but the two machines run the *same compiler version*, so that story
is incomplete. Unexplained.

**CV8 with specialisations is worth more on A than on B** - 0.593
against 0.738 on kernel compile. Consistent with a denser image helping
more when caches are smaller, but two machines cannot separate that from
anything else.

## What this means for the article

Quote the ordering, which reproduces. Quote the spread across machines
for anything whose magnitude matters. Do not quote a single machine's
number for the packed schemes at all - their cost is the thing that
moved most, and it moved enough to change the conclusion's basis.

And say plainly that two machines is not a study. It was enough to
overturn one claim; a third would probably overturn another.
