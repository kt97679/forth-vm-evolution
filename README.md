# forth-vm-evolution

Working code for an article about how a Forth virtual machine changed
shape over a sequence of encodings, from L.C. Benschop's SOD32 to a
byte-coded VM under a third its size, and what each change cost or
saved.

Every row of the ladder in `stages/STAGES.md` is a system that builds,
boots, compiles its own encoding, and passes the same 616-case ANS CORE
corpus. Nothing in the measured tables is modelled.

## Build and test

    tools/build-stages.sh      # every engine and image, both cell widths,
                               # and the SPN stages on an x86-64 host
    tools/run-tests.sh         # the shared ANS CORE corpus on every stage

That is enough to check that the systems work. To MEASURE them, build
several layouts first - see below.

## Measure

    tools/bench-laptop.sh              # everything below, then packed to send

or step by step:

    LAYOUTS=5 tools/build-stages.sh    # five builds of each engine
    tools/collect-results.sh sweep 2   # measure twice, save, compare
    tools/spn-bench.py build results/spn-HOST.md   # SPN: start-up, end to
                                       # end, memory - not in the sweep

On x86-64 Linux, `ENGINE_RT=nolibc` in front of `tools/build-stages.sh` (or
`tools/bench-laptop.sh`) builds the 64-bit engines without the C library:
a sixth of the start-up and a thirteenth of the resident memory for CV8.
`FINDINGS-FOOTPRINT.md` has the measurements and the one thing given up.

`tools/bench-laptop.sh` stops at the first failure - nothing is measured
unless every test passes - warns about what makes a laptop noisy
(governor, battery, load), and packs the results and logs into one
archive under `build/bench-laptop/`. `QUICK=1` runs the whole pipeline
in a few minutes, without error bars, as a check before the real run.

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
vendored SOD32 for comparison. `stages/STAGES.md` describes each. And
`relf` as it is today (`vendor/relf`): the system this ladder led to, with
its own CV8 and its own kernel, built and measured beside the stages as a
reference - it is where the shell and CV8 as a product now live.

The last of them, `s6-cv8b`, makes the dictionary header byte-granular -
a 1-3 byte link with its tag read backward - which takes the 8-byte
image from 11,088 bytes to 7,609, or 0.31x of cell threading.
`FINDINGS-CELL-WIDTH.md` accounts for every byte of what is left.

## Native code: SPN

On top of the encodings, two stages add a native-code layer, SPN
(Stencil-Patched Native): at start-up every word that can be proved
safe becomes x86-64 code, made by copying machine-code stencils out of
the engine and patching their holes; everything else stays interpreted.
`s8-spncv8` does it over `s6-cv8b`'s CV8 image and is the current one;
`s7-spn` does it over the cell image and is frozen. In one build on the
development VM, s8 runs the four workloads at 0.21-0.37x of the cell
system end to end, start-up included, from a 36 KB image - s7 needs
103 KB for roughly the same speed; s8-lazy, translating most words the
first time they run, needs 32 KB and starts fastest. `stages/STAGES.md` lists them;
`FINDINGS-SPN.md` has the design, the measurements and what they do and
do not show. x86-64 only.

## Layout

    vendor/sod32/   upstream SOD32, unmodified (GPLv2, see its LICENSE)
    vendor/relf/    relf's engine and kernel images at the commit in
                    UPSTREAM (GPLv2 only, see LICENCE.md); tools/update-relf.sh
    engine/         the C engines: relf.c, pack4/pack8, vm-lab.c; for SPN,
                    spn.c and spn-cv8.c, the stencils in spn-stencils.c
    forth/          the Forth sources: kernel, cross-compiler, overlays
    tools/          build, test and measurement scripts
    bench/          the workloads and the shared measurement library
    tests/corpus/   the shared test corpus every stage must pass,
                    normalised from the RelF tree by tools/make-corpus.py
                    (CRLF, CP1251, and multi-line `(` comments - only the
                    last has semantic weight, and that header explains why)
    stages/         what the stages are and how they differ
    results/        measurements, one file per machine
    lab/            experiments: dispatch/ (dispatch techniques side by
                    side), evolve/ (evolutionary search; RUNNING.md)
    article/        the write-up: article-en.md for ForthHub,
                    article-ru.md for Habr
    prompts/        reusable prompts for this kind of work, from relf
                    (INDEX.md; the commit in UPSTREAM)
    GOALS.md        where things stand, what is next, what was rejected
    PROGRESS.md     the log, one entry per session

## Working on this project

    Prompt library: prompts/INDEX.md
    Read INDEX.md at the start of the session and follow its dispatch rules.

None is skipped: this is a measurement project with a write-up, worked on
across sessions and handed between machines. Scopes worth stating:
`02-escape-recall` covers the gene pool (`lab/evolve/GENES.md`) and any
"which design is best" question; `03-audit-tooling` every figure, since
all of them come from this repository's own tools; `14`, `04` and `05`
the article. Before trying an approach, search `GOALS.md` and
`PROGRESS.md` for it. A handoff is an `Iteration N:` commit, then
`tools/make-bundle.sh DIR`, which names the bundle by `GOALS.md`'s
convention and checks that it clones.

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
