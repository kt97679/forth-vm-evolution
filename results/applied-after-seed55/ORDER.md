# The after-seed-55 batch - applied (Iteration 335)

| # | patch | what it does |
|---|---|---|
| 1 | tegra-engines-after-seed55.patch | The Tegra's build-stages.sh (seed 55's check: "engine/pack4.c:540: #error the gene sysc ... x86-64 Linux's (i386's mapped)"): the 32-bit work (Iterations 324-331) ported vm-lab.c and relf.c, the engines the evolver builds; four hand-made engines build-stages.sh also compiles kept the x86-only system-call guard. pack4.c, pack8.c, spn.c, spn-cv8.c get the same: SYSC's guard and table admitting 32-bit ARM (exit_group 248 there), the file overlays' calls mapped, mmap through the library, and the legacy layout at start. All under i386/ARM conditions - no 64-bit engine changes. |

    git apply results/applied-after-seed55/tegra-engines-after-seed55.patch

Tested on master at Iteration 334: each of the four compiled for 32-bit ARM by
arm-linux-gnueabihf-gcc with build-stages.sh's flags (-I build; spn-cv8 -DSCALE) - all clean, where
pack4.c stopped the Tegra; build-stages.sh's 16 64-bit binaries hashed before and after - all
identical; run-tests PASS; validate 7 of 7 IDENTICAL. Not testable here: build-stages.sh run whole
on ARM - the Tegra's next check is that; qemu-arm has no binfmt here to run it under.

**Applied on master at Iteration 335**: build-stages; run-tests PASS, 63 engine paths; validate 7 of
7 IDENTICAL; the gate 248 of 248 alive (seed 55's front 168, the joint front 133, 53 in both).

