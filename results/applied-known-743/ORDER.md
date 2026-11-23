# s1-sod16's ARM reach as known (Iteration 743) - applied at 743

Found at 742 (results/drafts/thumb-742.txt): the hand-made stage s1-sod16, built for ARM by GCC (tools/arm-cross-check.py
--gcc), gives "sod16: DOES> tail beyond 128 KB" on apps, where its x86 4-byte build passes - on master, with step 2 and
without engine/data-layout.ld alike, in A32 and in Thumb-2. A reach limit of the 16-bit stage, like s2-cpt16's on apps;
no design is affected. The owner (742): open questions decided as is most reasonable - so it is listed in
arm-cross-check.py's KNOWN (reported apart, as s2-cpt16), and a check of the Tegra (tools/rage-check.sh) does not fail on
it. Check, then apply, from the repository's top:

    env RECORD=1 sh tools/batch-check.sh
    git apply results/applied-known-743/arm-known-sod16-743.patch

batch-check (743, on Iteration 742 with this batch committed - 1 patch): PASS - run-tests PASS (the generators: 118 paths), validate 7 of 7
IDENTICAL, the jail PASS.

