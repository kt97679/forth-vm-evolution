# The applications' code in the size score - step 0 measured and checked (Iteration 678)

Step 0 of results/drafts/search-reopen-plan-677.md: evolve.py's size objective now counts the code the selection's
four applications lay. `rec['total'] = bin + size + app`; `rec['app']` the sum, `rec['appby']` per program [sim16,
gc16, scan, evo]; at 4-byte cells `app32` / `appby32`, tracked, not scored. Each program by two deterministic loads
after the gate (no timing): HERE's advance over its load, less what its own ALLOT , and C, lay - genapps.py's count,
now one definition in lab/evolve/appsize.py that both tools use (genapps.py's driver text unchanged, mode by mode).
Sixteen short loads a design, both widths. A program that gives no reading kills the design ("died: application size").
A database without `app` is refused a resume (it ranks on the old size); --report and --carry still read it, by its own.

## The check - lab/evolve/appsize-check.py: PASS

| part | what | result |
|---|---|---|
| 1 | the same binaries, genapps.py --sizes against evolve.py's app_size(): s6 and the ten designs of designs/ | 11 of 11 equal per program at 8-byte cells, 11 of 11 at 4 |
| 2 | the translator's images (evolve.build() from each record's genome), against 674's table | 10 of 10 equal per program at both widths |
| 3 | planted in sim16: `: PLANTED-677 DUP + ;` / `CREATE PLANTED-677B 100 ALLOT` | 1,737 -> 1,754 (the others unmoved) / 1,760 (the header only, not the 100) |
| 4 | a database of the old size resumed | refused |

The check made to fail: evolve.py's app_size() planted not subtracting the data - parts 1 and 3 failed, FAIL; restored,
PASS. run-tests runs `--quick` (1 on s6 at 8-byte cells, and 3; under a second).

## The four's code now (bytes, sim16 + gc16 + scan + evo)

| system | 8-byte cells, the search's image | 4-byte | designs/ (self-built, 676) 8 / 4 |
|---|---:|---:|---:|
| s6 | 7,572 | 6,808 | the same |
| portable-small | 6,948 | 6,416 | the same |
| portable-arm | 6,972 | 6,444 | the same |
| portable-knee | 6,988 | 6,464 | the same |
| portable-fastest | 7,020 | 6,480 | 7,012 / 6,476 |
| least-memory | 7,052 | 6,500 | the same |
| smallest | 7,524 | 6,764 | the same |
| small-jit | 7,860 | 7,380 | the same |
| fastest-x86-32 | 8,352 | 7,828 | the same |
| best-all-round | 8,336 | 7,808 | the same |
| fastest-x86-64 | 8,368 | 7,852 | 8,352 / 7,844 |

Two self-built images lay a little less application code than the translator's (8-16 bytes at 8-byte cells): the
records measure the translator's, which builds the search's images (the plan, "What stays").

The cross-run tools (Iteration 679): appsize.one_size() - compare-fronts refuses databases of both sizes, final-pick
candidates of both, stopping.py judges a run only against a series of its own size and marks its ledger line `"app":
true`; the first run of the new measure opens a series (process-records.sh's NEXT_METHOD). hv-bounds.json's box
(total 12,000-64,000) holds the new totals (about 21-51 KB), so it stands. appsize-check.py part 5: 5 of 5; made to
fail with the guard off (2 of 5 wrong). The full check:
`python3 lab/evolve/appsize-check.py` (about a minute and a half; build/appsize-check.json).
