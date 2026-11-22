# Forth designs for relf - the new roles (draft, Iteration 721; final after chain D)

**Draft.** Written while chain D runs, so that chain D's processing only fills in what it decides - marked
**[chain D]** (decided at 725 - results/followup-roles-seed96-jitband.md: small-jit stays 15eda54ebd; the gate ships
fastest-x86-32, fastest-x86-64 and small-jit translator-built, named in designs/TRANSLATOR-BUILT; the Tegra's check to run
again - its first stopped on export-arm.py's own fault): small-jit (15eda54ebd, or a design of the JIT band that beats it by the rule), the self-hosting gate's
speed half (lab/evolve/selfhost-speed.py: a role whose self-built image is more than 2 % slower than its translator's ships
translator-built), the Tegra's check of the GCC designs (rage-designs.py), and the package's name and checksums. The final
document: results/handoff-relf-NNN.md, generated as 657's was (results/drafts/relf-handoff-657.py adapted to the new roles'
documents - the genes section from each design's expression).

## What changed since the 657 handoff

- **The measure** (676-686): the size is the engine, the image and the code the five selection programs lay (sim16, gc16,
  scan, evo, shellmix - relf's shellmix.fth the fifth, 686), at 8-byte cells - so designs/'s bytes are not comparable
  with 657's (which were the engine and the image only).
- **The search reopened** (677-704): seeds 92-96 with the run-time genes rtvar (a data word's @ and ! as one operation,
  relf's VAR@ and VAR!), rtconst (a constant compiled as its value - relf's rule), rtinline (a body of at most 3
  instructions in 6 bytes copied for its call - relf's inlining rule), DOES> @ in rtvar; the unaligned strings and VALUE
  without its kind cell taken for everyone (680-681). The series stopped at seed 96 by its rule.
- **The roles chosen again** (705-718): three chains on the laptop, dream and the Tegra - A a screen of 944, B a
  shortlist of 99, C the 66 it could not settle (results/followup-roles-seed96-roles.md, -b.md, -c.md); the ten by the
  rule - 1 % smaller, no machine class 2 % slower, memory within 8 KB; a speed role's challenger 2 % faster at 2 SE -
  results/new-roles-718.md, with every near design kept on record there. Seven of the ten changed.
- **The images are self-built** (666-718, relf's way): forth/cross-cv8.4, a CV8 cross compiler in Forth run by each
  design's own engine, writes the design's image from source - designs/forth/ (kernel.4, extend.4, cross-cv8.4 and the
  overlays its genes name) and designs/NAME/genes.4; `make selfhost` in a design rebuilds its image byte for byte. All
  ten ship self-built (722: the cross compiler does the fused =I?BRANCH and DUP?NBRANCH, so portable-fastest, d727605472,
  no longer ships the converter's images). The gate's speed half (chain D, 725): seven self-built; fastest-x86-32,
  fastest-x86-64 and small-jit translator-built - their self-built images 2.1-4.6 % slower at one width (median of 5
  alternations; designs/TRANSLATOR-BUILT gives each), the instructions the same (721): code placement. portable-fastest's
  timing is the next laptop run's.

## The designs

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

Speed: CPU time against the hand-made s6, lower faster; each class the geometric mean of its machines over a chain's
sessions (chain B's, or chain C's where B lacks a class - results/drafts/designs-table-718.py). \* the JIT designs on
ARMv7 without their JIT. - not measured on the Tegra. The same table: designs/README.md.

## For relf (RELF.md's adoption criteria) - what still holds from 657, and what is new

- **The JIT is x86 only**, as before; the six without it are relf's candidates as they stand.
- **New: the images are built relf's way** - by a cross compiler in Forth, from source, on the design's own engine - so
  what relf takes can now be the source as well as the mechanisms: designs/forth/ and a design's genes.4 rebuild its
  image (`make selfhost`); the genes as Forth (lab/evolve/export-genes.py) name each translator rewrite the design uses.
- **New: relf's own mechanisms measured in the lab** - rtvar, rtconst and rtinline (relf's VAR@/VAR!, constant rule and
  inlining rule, results/mech-prices-684.md, relf-reply-685.md): which of the ten carry them is in each record's genome;
  shellmix.fth (relf's) is in the size and the speed.
- **Without the C library and on ARMv7**, as before: `make libc`, `make arm` for the six without the JIT; the clang three
  (portable-fastest, portable-knee, smallest) cross-built, the lab's bytes, under qemu-arm; the GCC three (portable-arm,
  portable-small, least-memory) built on the Tegra by its own GCC **[chain D: rage-designs.py's PASS]**.
- **Not measured here**, as before: relf's shell workloads beyond shellmix, AArch64, RISC-V.

## The files and how to fetch them

- **designs/** in the repository (the bundle the owner hands over): each design's engine source, its Makefile, its images
  and their source; `make`, `make test`, `make selfhost`, `make 32`, `make libc`, `make arm` from the top.
- **The package** **[chain D: forth-vm-evolution-designs-iterNNN.tar.gz]** (lab/evolve/pack-designs.py, as 657's: per
  design ID/record.json and ID/cell8/, ID/cell4/ - engine, image.img, src/, build.txt, check.txt; SHA256SUMS), rebuilt
  byte for byte from the repository with results/relf-designs-NNN.md.
- **The build-out**: `sh results/drafts/roles-build-718.sh 1 . RECORDS NAMES`, the cross GCC's export-arm.py --gcc, then
  `... 2 . RECORDS NAMES` (the script's header) - a role changed later goes the same way, alone.
