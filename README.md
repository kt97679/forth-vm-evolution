# forth-vm-evolution

Working code for an article about how a Forth virtual machine changed
shape over a sequence of encodings, from L.C. Benschop"s SOD32 to a
byte-coded VM roughly half its size, and what each change cost or saved.

Every row of the ladder in `stages/STAGES.md` is a system that builds,
boots, and is tested. Nothing in the measured tables is modelled.

## Build and test

    tools/build-stages.sh      # ~40s: every engine and image, both widths
    tools/run-tests.sh         # the shared ANS CORE corpus on every stage

## Layout

    vendor/sod32/   upstream SOD32, unmodified (GPLv2, see its LICENSE)
    engine/         the C engines: relf.c, and vm-lab.c for the ladder
    forth/          the Forth sources: kernel, cross-compiler, overlays
    tools/          build, test and measurement scripts
    tests/corpus/   the shared test corpus every stage must pass
    stages/         what the stages are and how they differ
    article/        the write-up

## Method

Two rules, both learned the hard way in the parent project:

1. A benchmark or a test that cannot fail is worse than none. Every
   stage runs a negative control - the corpus plus one deliberately
   wrong case - and is reported BROKEN if it does not notice.
2. A number is quoted only from a build that is in this repository and
   reproduces. Where an old figure could not be reproduced, the article
   says so rather than repeating it.
