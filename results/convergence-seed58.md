# Is the search stuck in a local minimum? What is tested, what is not, and seed 58's run seen from inside (Iteration 392)

The owner's concern (Iteration 373, asked again at 392): the search may settle in a local minimum and miss better
designs because it cannot get out. A local minimum can come from five places; each is a different test.

1. **A constraint fencing off a region** - tested by seed 58, and real: without the tag-2 requirement the search
   found plain-CV8 designs 10.5% smaller and 21.5% faster at 32 bits than any carried run.
2. **The carry anchoring the search** - seed 60 tests it (noevolved: no design from an earlier run's record).
3. **Every run starting from the same human designs** - fresh or carried, all start from the hand-made stages and
   founders built from them, and could land in one basin. Seed 60 cannot rule this out; fromzero could, but in
   miniature it starts too far down (results/review-methodology-386.md, section 1). Seeds 58, 59 and 60 start
   three ways (evolved founders, free; evolved founders, tag-2; none, tag-2): ending in one structure and quality
   would say one basin is reached from different starts.
4. **The search collapsing inside a run** - measured here, below, on seed 58: **no**.
5. **The gene set's edge** - no run can find a mechanism no gene offers. This is the largest local minimum of a
   designed search space, and no search setting leaves it: new mechanisms do (HANDOFF item 4, fewer dispatches).

## Seed 58 from inside (`lab/evolve/review-checks.py progress`)

Diversity is the mean share of built genes (express()) in which two designs of a generation differ. **It does
not collapse - it holds and rises**: 0.47-0.56 over all designs, within the tag-2 family 0.35-0.47 (rising
to the end), within the plain family 0.46-0.53; the two encodings stay side by side to the last generation.
**And the run was still gaining when it stopped**: the smallest binary + image - exact, no noise - improved in
21 generations, the last at generation 130 of 133 (40 bytes in the last third); the 32-bit best to generation
120; the speed's large steps early (generations 5 and 15: 22.9%, 3.6%), then gains of under 2% each to
generation 100. Diminishing returns, not a stall: the population was exploring, not stuck - though from inside
a run no measure can say whether a better region lies beyond what it can reach.

**Proposed** (the owner's): after seed 60, this check and gene-usage.py on seeds 58, 59 and 60 - three starts, one
end or several; replicates if the hours allow, two shorter runs from the noevolved start with different seeds,
to measure how far endpoints spread; escape mechanisms (immigrants, islands, restarts) only if those show runs
stuck - seed 58 gives no sign, and each is complexity; and new mechanisms, the only way past the space's edge.

---

| generation | alive | best speed so far | smallest so far | best 32-bit so far | diversity: all / tag-2 family / plain family | encodings alive (enc/tag2: designs) |
|---|---|---|---|---|---|---|
| 0 | 139 | 0.1744 | 18,986 | 0.4610 | 0.587 / 0.631 / 0.583 | cv8/0: 60, cpt16/0: 38, sod16/0: 22, cell/0: 16 |
| 10 | 203 | 0.1356 | 14,933 | 0.3624 | 0.488 / 0.386 / 0.531 | cv8/1: 140, cv8/0: 62, cpt16/0: 1 |
| 20 | 169 | 0.1304 | 14,563 | 0.3461 | 0.501 / 0.352 / 0.530 | cv8/1: 104, cv8/0: 65 |
| 30 | 198 | 0.1286 | 14,563 | 0.3461 | 0.470 / 0.394 / 0.502 | cv8/1: 122, cv8/0: 76 |
| 40 | 177 | 0.1258 | 14,368 | 0.3303 | 0.503 / 0.375 / 0.527 | cv8/0: 88, cv8/1: 87, cpt16/0: 2 |
| 50 | 202 | 0.1234 | 14,272 | 0.3137 | 0.529 / 0.408 / 0.498 | cv8/1: 101, cv8/0: 101 |
| 60 | 202 | 0.1234 | 14,210 | 0.3027 | 0.526 / 0.394 / 0.506 | cv8/0: 108, cv8/1: 94 |
| 70 | 179 | 0.1234 | 14,202 | 0.3027 | 0.523 / 0.389 / 0.491 | cv8/0: 97, cv8/1: 82 |
| 80 | 194 | 0.1220 | 14,202 | 0.2937 | 0.546 / 0.421 / 0.501 | cv8/0: 109, cv8/1: 85 |
| 90 | 176 | 0.1220 | 14,186 | 0.2915 | 0.549 / 0.427 / 0.518 | cv8/0: 94, cv8/1: 81, sod16/0: 1 |
| 100 | 200 | 0.1179 | 14,170 | 0.2915 | 0.550 / 0.425 / 0.498 | cv8/0: 119, cv8/1: 81 |
| 110 | 170 | 0.1179 | 14,170 | 0.2915 | 0.553 / 0.427 / 0.460 | cv8/0: 106, cv8/1: 64 |
| 120 | 188 | 0.1179 | 14,170 | 0.2843 | 0.550 / 0.440 / 0.500 | cv8/0: 96, cv8/1: 92 |
| 130 | 155 | 0.1179 | 14,146 | 0.2843 | 0.542 / 0.452 / 0.465 | cv8/0: 104, cv8/1: 51 |
| 133 | 166 | 0.1179 | 14,146 | 0.2843 | 0.564 / 0.473 / 0.497 | cv8/0: 106, cv8/1: 60 |

the smallest binary + image (exact) gained in 21 generations; the last at generation 130 of 133; in the last third 2 gains, 40 bytes in all
the best speed gained 2% or more in 2 generations; the last at generation 15 (5: 22.9%, 15: 3.6%)
