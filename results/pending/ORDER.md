# The after-seed-41 batch: sixteen patches, in this order

Each was made on a fresh clone of master with all the ones before it applied,
and the sixteen together verified to apply in order on a fresh clone and to
reproduce the tested files (last: Iteration 192).

| # | patch | what |
|---|---|---|
| 1 | rtimm2-after-seed41.patch | rtimm=2: run-time immediates without pairs (175) |
| 2 | keepforms-after-seed41.patch | DUP+I, DUP<I: the keeping forms (176) |
| 3 | founder-after-seed41.patch | a founder with rtimm=2 and the forms (178; moved to the knee by 13) |
| 4 | regprice-names-after-seed41.patch | regprice.py names opcodes from CALLMAP (172) |
| 5 | opcall-band-after-seed41.patch | X;CALL in the base band only (180) - its containment removed by 15 |
| 6 | loopalign-after-seed41.patch | no loop NOOPs for non-JIT tag-2 (179) |
| 7 | coreext-w7-after-seed41.patch | SYNONYM, INCLUDE, REQUIRED, SAVE-INPUT, PARSE-NAME (181) |
| 8 | coreext-w8-after-seed41.patch | DEFER, S\", REPLACES, SUBSTITUTE, HOLDS (182) |
| 9 | dskew-after-seed41.patch | the data stack 2 KB lower; eff.get (183) |
| 10 | ansupper-sq-after-seed41.patch | S\" escaped quotes kept by ans-upper.py (183) |
| 11 | stacksep-after-seed41.patch | stacks apart, the 256 MB dictionary, ALLOT (184) |
| 12 | coreext-w9-after-seed41.patch | blocks, TRAVERSE-WORDLIST, name tokens (186) |
| 13 | weighing-after-seed41.patch | demote, don't delete: the attic, the knee kept, runs judged by five measures (189) |
| 14 | rtloop2-after-seed41.patch | headerless words in the converter; rtloop=2 (190) |
| 15 | opcall-fix-after-seed41.patch | opcall's cause fixed; every band open again (191) |
| 16 | coreext-w10-after-seed41.patch | RESTORE-INPUT across a file's lines; filetest whole (192) |

To apply, on a fresh clone of master:

    for f in rtimm2 keepforms founder regprice-names opcall-band loopalign coreext-w7 \
             coreext-w8 dskew ansupper-sq stacksep coreext-w9 weighing rtloop2 opcall-fix coreext-w10; do
        git apply results/pending/$f-after-seed41.patch || break
    done

Then, as for each batch: LAYOUTS=1 bash tools/build-stages.sh, bash tools/run-tests.sh
(bash, not sh), python3 lab/evolve/evolve.py --validate, the reseed's fixed point,
the front designs alive, and lab/evolve/ans-check.py on the front.
