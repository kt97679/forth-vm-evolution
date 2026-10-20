# Seed 63's decisions - the rules, written before its results (Iteration 430)

The owner: write down seed 63's decision rules before seeing its results, so that its processing applies agreed rules
rather than ones made up after the fact. Seed 63 is the after-seed-62 batch's first run (its 13 patches), free of the
tag-2 requirement, 11 hours with a comparison against seeds 59-62 at both widths (HANDOFF.md, item 0). Each rule
names what is measured, by which tool, the threshold, and what follows. Where a rule's outcome is a change, it is
proposed to the owner, not made. "Used" below means: expressed on at least 10% of seed 63's front, or on at least one
design of its fastest tenth at 64 bits (the fast end is where a speed gene earns its bytes).

| # | what | measured by | rule | then |
|---|---|---|---|---|
| 1 | The verdict | compare-fronts (both widths, both CPUs) | the routine's 5% bar | as always |
| 2 | jithelp, jitre (patches 2-3) | seed-facts.py: each gene's share of the front; the fastest tenth's genomes | used: kept | not used: proposed out - frozen off, the code removed later (Iteration 397's prediction: under 10%) |
| 3 | jitret (patch 8) | the same | used: kept | not used: proposed out, as 2 |
| 4 | The fast gate (patch 1) | review-checks.py curse: the fastest tenth's re-measured / in-run, median | at most 1.05: it works | 1.05-1.066: partly; above 1.066 (seeds 58, 60, 61: 1.112, 1.066, 1.095): its threshold revisited |
| 5 | The freeze (patch 10) | seed-facts.py; the front's expressed genomes | no design refused at the reach limit; every front design holds bytehdr, doesfar, thinhdr, varcall, bss and lean on, msc and scale 0 | any exception: a fault in patch 10, fixed before seed 64 |
| 6 | 32-bit correctness (patches 4-6, 9) | review-checks.py fail32 | no failure of a known cause | a known cause: a regression, fixed before seed 64; "not a known cause": investigated |
| 7 | The small end | the front's smallest | at most 14,535 bytes: seed 58's 14,146 within 2%, and patch 12's 104 bytes | above: the frozen genes' bytes at the small end examined first |
| 8 | I+ on the two-bit tag (patch 11) | the share of the front with rtiplus | above 10% (Iteration 412's prediction; seeds 53-60: 4%) | below: noted - the search's choice, no fault |
| 9 | The tail engines (HANDOFF item 4b) | the share of the front with tail; the fastest tenth | used: kept | not used: proposed out - frozen off, gen-tail.py and build_tail removed later; the 32-bit fixes (patches 5, 6, 9) gave it its chance |
| 10 | The rtimm=2 / rtfuse overlap (item 4b, Iteration 423) | the front's designs with rtimm=2, rtfuse off and built pairs or fused tests | none: proposed - rtfuse governs (rtimm=2 passes --rtfuse only with rtfuse on), no front design changed | some: their run-time fusion knocked out and measured; the owner decides |
| 11 | Programs past 4 MB (patch 12) | the corpus and the tests | pass | a failure: fixed before seed 64 |

Not a seed 63 rule: the best design across the machine classes is read at seed 62's processing (review-checks.py
generic over its chain's remote checks: three candidates asked for by id - results/candidates-generic.md); the generic
design is chosen when the owner asks for one (GOALS.md).
