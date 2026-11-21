# The winning designs - build one with `make`

Ten Forth systems found by this project's genetic algorithm, each the best at something - none is best at
everything (article/article-en-draft.md, section 15). Every one is a complete Forth: an engine in C and an image, the
compiled Forth system it runs (the dictionary, every word, the language), shipped here as SOD32 shipped its own.
Every engine is compiled from source.

## Quick start

    make                       # from the repository's top: all ten (x86-64 Linux)
    make test                  # each one runs a definition: : SQ DUP * ; 7 SQ .
    designs/portable-knee/forth designs/portable-knee/image.img

Then type Forth - names in upper case, `BYE` to leave:

    : SQ DUP * ;  7 SQ .       \ 49

One design: `make portable-knee`, or `make` in its directory. A file: `./forth image.img < program.fth`.

## Which to use

Speed is CPU time against the hand-made s6 the search started from, so lower is faster - 0.161 is 6.2 times s6's
speed; each class the geometric mean of its machines (x86-64: an AMD Ryzen 7 PRO 8840HS and an Intel i7-6700; x86-32:
the same at 4-byte cells; ARMv7: an NVIDIA Tegra), every session pooled - the portable designs re-measured side by
side in the new roles' chains (Iterations 713-716: results/followup-roles-seed96-roles.md, -b.md, -c.md; the ten
chosen at 718, results/new-roles-718.md), each figure from chain B's sessions or, where chain B lacks a class, chain C's
(results/drafts/designs-table-718.py). Bytes: engine, image and the five selection programs' code at 8-byte cells (the
search's size since Iteration 686), the engine as measured (`make tight`). Memory: peak resident.

| `make` target | design | what it wins | x86-64 | x86-32 | ARMv7 | bytes | memory | JIT |
|---|---|---|---|---|---|---|---|---|
| `fastest-x86-64` | 9b15ba26f7 | fastest on x86-64 | 0.161 | 0.186 | - | 53,503 | 292 KB | yes |
| `fastest-x86-32` | 11f956db93 | fastest on x86-32 | 0.175 | 0.180 | - | 49,925 | 264 KB | yes |
| `best-all-round` | df097ba2e2 | best mean of x86-64, x86-32 and ARMv7 | 0.162 | 0.187 | 0.432* | 54,695 | 288 KB | yes |
| `small-jit` | 15eda54ebd | smallest of the JIT designs | 0.219 | 0.234 | - | 36,344 | 208 KB | yes |
| `portable-fastest` | d727605472 | fastest without the JIT, by the mean | 0.318 | 0.317 | 0.324 | 35,539 | 148 KB | no |
| `portable-arm` | a8d35bdccc | fastest on ARMv7 | 0.339 | 0.431 | 0.302 | 45,274 | 140 KB | no |
| `portable-knee` | 48a012411a | fast without the JIT; small | 0.385 | 0.373 | 0.408 | 26,957 | 144 KB | no |
| `portable-small` | ae99617f06 | small, fast on ARMv7 | 0.451 | 0.443 | 0.324 | 26,261 | 124 KB | no |
| `least-memory` | fb0d57c8a2 | least memory | 0.849 | 0.880 | 0.477 | 25,569 | 112 KB | no |
| `smallest` | 219878ec89 | smallest | 1.483 | 1.285 | 1.234 | 21,673 | 116 KB | no |

\* on ARMv7 without its JIT: the JIT generates x86 code, so the JIT designs are for x86 only. - : not measured on the Tegra.

## Builds

- `make` (in a design's directory) - `forth`, the build the project measured: 8-byte cells, x86-64 Linux, without the
  C library (its own small runtime, `src/rt-linux-x86_64.c`), static. Needs gcc or clang - each design names its own
  compiler in its Makefile (`make CC=gcc` works with either; another compiler gives other bytes, the same Forth).
- `make forth-arm` - 4-byte cells for 32-bit ARM Linux (ARMv7, hard float), without the C library (its own runtime,
  `srcarm/rt-linux-armv7.c`), static - the build the lab measured on the Tegra (`./forth-arm image32.img`). A clang design
  cross-builds from any host with clang and lld; a GCC design builds on the ARM host with its own GCC
  (`make forth-arm CCARM=arm-linux-gnueabihf-gcc` to cross-build; the Tegra measured GCC 16). The six designs without
  the JIT; `make arm` from the top builds them all.
- `make forth-libc` - the same design with the C library, for any other host with a C compiler (other Unixes). The six
  designs without the JIT; `make libc` from the top builds them all.
- `make forth32` - 4-byte cells (`./forth32 image32.img`); needs 32-bit support (gcc-multilib); `make 32` from the top.
- `make tight` - the file exactly as measured: the same loaded bytes, without section headers or symbols (python3).
- `make selfhost` (`make selfhost32`) - the image rebuilt from its source by its own engine: `image.img` runs the CV8
  cross compiler (`forth/cross-cv8.4`) on the kernel and overlays in `forth/` with the design's genes (`genes.4`,
  `genes32.4`), and the image it writes must be `image.img` byte for byte (`selfhost.sh`); `make selfhost` from the
  top checks all ten at both widths - all but those `TRANSLATOR-BUILT` names, if any.

Warnings about an optimize attribute and an RWX segment are expected. Each engine here is byte for byte the one the
project measured once tightened, checked when these directories were generated - but for the four JIT designs' layout
lines (`src/vm-jit-ops.h`'s `JIT_NWENDS`, `jit_wends`, `JIT_W_`), which describe the self-built image they ship.

## Where they come from

Generated by `lab/evolve/export-designs.py` from the relf handoff's ten (results/relf-designs-636.md; Iteration 611 - fastest-x86-32, small-jit and portable-arm made again at 628,
portable-small at 631, portable-knee at 636): each
design built by the project's own build, the compiler asked for the files it really reads, those copied into `src/`
(and `src32/`), the compile command written into the Makefile. Regenerate after a change to the project:

    python3 lab/evolve/export-designs.py designs results/relf-designs-636.md NAME=ID,...

in a built and validated tree (README.md, "Build and test"). `record.json` in each directory is the design's genome
and the project's record of it.

The images are self-built (Iteration 675; results/drafts/selfhost-plan-666.md): the project's converter
(`tools/layout.py`) made the first image of each design, that image cross-compiled its successor from source, and
the successor rebuilt itself byte for byte - 16-304 bytes smaller than the converter's; the converter's are the
ones the search measured. `tools/selfhost-ship.sh designs` makes them, after `export-designs.py` and
`lab/evolve/export-arm.py`.
A design the cross compiler cannot yet build keeps the converter's images, and `TRANSLATOR-BUILT` here names it
with the reason (`make selfhost` and the tests skip it); with no such design there is no such file.
