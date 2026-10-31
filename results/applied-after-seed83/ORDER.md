# The after-seed-83 batch - to apply first at seed 83's processing (Iteration 570)

process-run.sh checks and applies it.

    git apply results/applied-after-seed83/armrt-after-seed83.patch
    git apply results/applied-after-seed83/prebuiltarm-after-seed83.patch
    git apply results/applied-after-seed83/ragecheck-after-seed83.patch

batch-check (571, on 67231cc - 3 patches): PASS - run-tests PASS (the generators: 107 paths), validate 7 of 7 IDENTICAL,
the jail PASS.

**armrt-after-seed83.patch** (engine/rt-linux-armv7.c, engine/rt-linux-x86_64.c, lab/evolve/evolve.py, tools/arm-cross-
check.py) - Iteration 570, the owner's open item 1: clang for the Tegra. engine/rt-linux-armv7.c is rt-linux-i386.c's
twin for 32-bit ARM: system calls by svc #0 (i386's numbers but exit_group, 248), the signals' restorer, _start, byte-
loop memcpy/memmove/memset (rt-linux-x86_64.c's x86 string instructions now behind RT_OWN_MEM; its portable rest
included). evolve.py: rt() links it on an ARM host (rage's GCC builds, s6 among them) and under EVOLVE_TARGET=armv7
(arm_cross(): a clang cv8 design cross-built here by clang --target=arm-linux-gnueabihf -march=armv7-a with lld; _build
refuses every other design in that mode). Tested: nothing changes on x86 - master's and the batch's engines and images
byte-identical, s6 and 13 of seed 82's front (JIT and not, GCC and clang) at 8- and 4-byte cells
(results/drafts/x86-identity-570.py); tools/arm-cross-check.py --n 40 - 40 of seed 82's 193 clang no-JIT designs, spread
by speed, all alive under qemu-arm (corpus, kernel, far, full) and identical to x86-32 on fib and apps, the ARM engines
6,444-16,064 bytes (static glibc: 347,688). The Tegra's side simulated with Ubuntu's arm-linux-gnueabihf-gcc 13 (it
removes gcc-multilib: swapped in, then setup-sandbox.sh restored it), --gcc: s6 and the front's 3 GCC designs alive and
identical; s0-cell and s1-sod16 alive, s0's apps output the same as at x86-32; s2-cpt16 alive, out of reach on apps at
both widths' builds (scale 1) and faulting after it at a layout-dependent point (the fault trap's exit 70 at both);
s3-s5 not converted at 4-byte cells at either - the converter, not the runtime.

**prebuiltarm-after-seed83.patch** (lab/evolve/README.md, lab/evolve/REMOTES, lab/evolve/remote-checks.sh,
lab/evolve/xcheck.py) - Iteration 570: rage's check as REMOTES' prebuiltarm, was native. xcheck.py --sample --arm (with
--cell 4 --bundle) takes clang's designs, no JIT: each alive as 32-bit x86 as before and, a cv8 clang one, cross-built
for ARMv7 too - taken only if that builds; the bundle holds those ARM engines alone. On the host a bundle without s6 is
partial: s6 and every design not in it built there by its GCC (its expression compared, as native's), the rest measured
as shipped, marked prebuilt; the report says how many were built where. Dream's bundles always hold s6: unchanged. Seed
82's front: 196 designs eligible for rage, 3 before (193 clang, 3 GCC). Tested end to end
(results/drafts/prebuiltarm-e2e-570.sh: remote-checks.sh probe, start, gather with ssh and scp stand-ins, this x86 VM as
the host): 12 sampled (no db.jsonl, so none rejected), 10 cross-built into a 74 KB bundle, 2 GCC; s6 and the 2 built and
measured on the host, the 10 shipped (not runnable on x86 - as expected); the report's "Built where" line. The laptop
needs `sudo apt-get install lld libc6-dev-armhf-cross libgcc-13-dev-armhf-cross` - none conflicts with gcc-multilib
(whose Conflicts name only the gcc-N-<arch> cross compilers); qemu-user only for tools/arm-cross-check.py.

**ragecheck-after-seed83.patch** (tools/arm-cross-check.py, tools/rage-check.sh) - Iteration 571 (the owner): the
Tegra's engines checked on the Tegra itself before its check of the confirmation front - what qemu cannot say: rage's
GCC 16 with engine/rt-linux-armv7.c, and the engine's start on a 32-bit host (the legacy-layout re-exec, which fails and
is skipped under qemu). From the laptop, after seed 83's processing and before seed 84: `sh tools/rage-check.sh` - HEAD
bundled, copied to rage.lan:fve-ragecheck/, cloned, the stages built there, then arm-cross-check.py on the newest
results file, natively: the hand-made stages and the front's GCC designs built by rage's cc as its check builds them,
each alive and giving fib and apps as the stage s6 with the C library does; exit 0 and the clone removed on a pass, kept
with check.log on a failure. arm-cross-check.py: a native mode on an ARM host, and the stage s6 (build/s6-cv8b-32) its
reference in every mode - no x86 run before needed; the known cases (s2-cpt16 out of reach on apps, s3-s5 not converted
at 4-byte cells) listed apart. Tested: the reference the same as 570's (3 designs IDENTICAL under qemu-arm); rage-
check.sh end to end with ssh and scp stand-ins (results/drafts/rage-check-e2e-571.sh) - PASS, the clone removed; a
failing check (no design) - exit 1, the clone and its log kept. Not timed on rage.