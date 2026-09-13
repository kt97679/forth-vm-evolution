# forth-vm-evolution

Working code for an article about how a Forth virtual machine changed
shape over a sequence of encodings, from L.C. Benschop's SOD32 to a
byte-coded VM under a third its size, and what each change cost or
saved.

Every row of the ladder in `stages/STAGES.md` is a system that builds,
boots, compiles its own encoding, and passes the same 616-case ANS CORE
corpus. Nothing in the measured tables is modelled.

## Build and test

    tools/build-stages.sh      # every engine and image, both cell widths
    tools/run-tests.sh         # the shared ANS CORE corpus on every stage

That is enough to check that the systems work. To MEASURE them, build
several layouts first - see below.

## Measure

    LAYOUTS=5 tools/build-stages.sh    # five builds of each engine
    tools/collect-results.sh sweep 2   # measure twice, save, compare

`sweep N` runs everything N times, saves each under a name taken from
this machine's CPU, and finishes by checking whether the runs agree
within their own error bars (`tools/agree.py`).

`LAYOUTS` is not optional if you intend to quote a number. The variation
here is dominated by per-BUILD bias, not run-to-run noise: repeated runs
of the same binaries agree to 1-2%, but a rebuild moves a stage by five
or ten, and the cell-engine baseline - which divides every ratio - had
the widest spread of all at 12.6%. Building each engine several ways and
averaging is what turns that hidden constant into a measured interval.
`bench/README.md` has the detail. On a slow board `LAYOUTS=3` is a fine
trade; `LAYOUTS=1` gives no error bar at all and the tools say so.

Timing uses CPU time where `tools/cputime.c` builds, wall clock
otherwise. Each report says which, and prints both spreads.

## The stages

`s0-cell` through `s6-cv8b`, plus the two schemes an earlier design note
rejected and this project built anyway (`p4-pack4`, `p8-pack8`), plus
vendored SOD32 for comparison. `stages/STAGES.md` describes each.

The last of them, `s6-cv8b`, makes the dictionary header byte-granular -
a 1-3 byte link with its tag read backward - which takes the 8-byte
image from 11,088 bytes to 7,609, or 0.31x of cell threading.
`FINDINGS-CELL-WIDTH.md` accounts for every byte of what is left.

## Layout

    vendor/sod32/   upstream SOD32, unmodified (GPLv2, see its LICENSE)
    engine/         the C engines: relf.c, pack4/pack8, vm-lab.c
    forth/          the Forth sources: kernel, cross-compiler, overlays
    tools/          build, test and measurement scripts
    bench/          the workloads and the shared measurement library
    tests/corpus/   the shared test corpus every stage must pass
    stages/         what the stages are and how they differ
    results/        measurements, one file per machine
    article/        the write-up

## Method

Rules, each learned the hard way:

1. A benchmark or a test that cannot fail is worse than none. Every
   stage runs a negative control - the corpus plus one deliberately
   wrong case - and is reported BROKEN if it does not notice. Three
   separate harnesses here once reported success while measuring
   nothing.
2. A number is quoted only from a build that is in this repository and
   reproduces. Where an old figure could not be reproduced, the article
   says so rather than repeating it.
3. Correctness and speed are measured by the SAME run. Every stage
   cross-compiles the kernel and the image must be byte-identical to the
   reference before the timing is recorded, so a stage that is fast
   because it is quietly wrong fails the comparison that times it.
4. One run is not evidence. Every conclusion in the article survived
   being measured twice on at least two machines; several did not
   survive, and are reported as things that did not reproduce.
