# The after-seed-83 batch - to apply first at seed 83's processing (Iteration 570)

process-run.sh checks and applies it.

    git apply results/pending/armrt-after-seed83.patch
    git apply results/pending/prebuiltarm-after-seed83.patch

**armrt-after-seed83.patch** (engine/rt-linux-armv7.c, engine/rt-linux-x86_64.c, lab/evolve/evolve.py, tools/arm-cross-check.py) - TODO: what it does, why, how it was tested.

**prebuiltarm-after-seed83.patch** (lab/evolve/README.md, lab/evolve/REMOTES, lab/evolve/remote-checks.sh, lab/evolve/xcheck.py) - TODO: what it does, why, how it was tested.
