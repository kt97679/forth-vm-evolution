# The after-seed-43 batch - the order to apply it in

Against master after Iteration 210 (the after-seed-42 batch applied). Seed 43
runs WITHOUT these (it started on Iteration 210's commit).

| # | patch | what |
|---|---|---|
| 1 | rebind-after-seed43.patch | --rebind takes the NEWEST redefinition (the dump lists words newest first): fsys 4's buffered WRITE bound at last; INCLUDED uses fsys 3's forgetting OPEN-FILE and CLOSE-FILE (211) |
| 2 | fsys5-after-seed43.patch | fsys 5: READ-LINE reading ahead where a file can seek, given back before every other use; outbuf-check.py with level 5 (211) |
| 3 | guard-after-seed43.patch | the dump guard: setup stops when a library does not load whole - load errors, names missing, definitions short by count (212) |

No engine or kernel change: no reseed; the stages rebuild only for the new
forth/file-sysc5.4 (the evolver's freshness check asks for it).

```
for f in rebind fsys5 guard; do git apply results/pending/$f-after-seed43.patch; done
LAYOUTS=1 bash tools/build-stages.sh && bash tools/run-tests.sh && python3 lab/evolve/evolve.py --validate
```

**Seed 43 and fsys 4.** Seed 43 runs with patch 1's fault: its fsys 4 is fsys
3 with dead bytes (the buffered WRITE never bound), so it will look strictly
worse than 3 - its count on seed 43's front says nothing about buffering. Its
fsys 3 and 4 designs work; INCLUDED's descriptors are regular files, which the
unforgotten seek cache describes rightly.
