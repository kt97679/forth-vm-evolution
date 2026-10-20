# Seed 63's decisions - the rules, written before its results (Iterations 430-432)

The owner: write down seed 63's decision rules before seeing its results, so that its processing applies agreed rules;
then (431) check that none would lose potentially good designs - and if none would, use them. One would have, as first
written: the rule for taking a gene out. It is revised below, with the evidence; the rest were checked and stand.
**Adopted at Iteration 431 (the owner).** Then (432, the owner) no rule takes a gene out: the rules vote, and only
several votes and no keep vote make a gene a candidate - "The gene votes" below, in place of 431's gene rule.
Where a rule's outcome is a change, it is proposed to the owner, not made.

Seed 63 is the after-seed-62 batch's first run (its 13 patches), free of the tag-2 requirement, 11 hours with a
comparison against seeds 59-62 at both widths (HANDOFF.md, item 0).

## The rules

| # | what | measured by | rule | then |
|---|---|---|---|---|
| 1 | The verdict | compare-fronts (both widths, both CPUs) | the routine's 5% bar | as always |
| 2 | jithelp, jitre (patches 2-3), jitret (patch 8) | the gene votes below | kept unless the votes make it a candidate | a candidate: the dependence test, then proposed to the owner - reversibly |
| 3 | The fast gate (patch 1) | review-checks.py curse: the fastest tenth's re-measured / in-run, median | 0.98 to 1.05: it works | 1.05-1.066: partly; above 1.066 (seeds 58, 60, 61: 1.112, 1.066, 1.095): its threshold revisited; under 0.98: too harsh - in-run speeds now pessimistic, good designs undercounted - revisited |
| 4 | The freeze (patch 10) | seed-facts.py; the front's expressed genomes | no design refused at the reach limit; every front design holds bytehdr, doesfar, thinhdr, varcall, bss and lean on, msc and scale 0 | any exception: a fault in patch 10, fixed before seed 64 |
| 5 | 32-bit correctness (patches 4-6, 9) | review-checks.py fail32 | no failure of a known cause | a known cause: a regression, fixed before seed 64; "not a known cause": investigated |
| 6 | The small end | the front's smallest | at most 14,535 bytes: seed 58's 14,146 within 2%, and patch 12's 104 bytes | above: the frozen genes' bytes at the small end examined first |
| 7 | I+ on the two-bit tag (patch 11) | the share of the front with rtiplus | above 10% (Iteration 412's prediction; seeds 53-60: 4%) | below: noted - the search's choice, no fault |
| 8 | The tail engines (HANDOFF item 4b) | the gene votes below - seeds 63-65 its first fair runs, the 32-bit fixes (patches 5, 6, 9) applied | kept unless the votes make it a candidate | a candidate: as 2 (gen-tail.py and build_tail removed last) |
| 9 | The rtimm=2 / rtfuse overlap (item 4b, Iteration 423) | the front's designs with rtimm=2, rtfuse off and built pairs or fused tests | none: proposed - rtfuse governs (rtimm=2 passes --rtfuse only with rtfuse on) | some: no change |
| 10 | Programs past 4 MB (patch 12) | the corpus and the tests | pass | a failure: fixed before seed 64 |

**The gene votes** (rules 2 and 8; every gene not frozen - the owner, Iteration 432). No rule takes a gene out; each
run votes, and votes for keeping weigh more than votes for removal - keeping a useless gene costs code, removing a
useful one loses designs.

1. **Removal votes - weak, four a run.** On under 10% of the front; on no design of its fastest tenth; of its smallest
   tenth; of its best-Q tenth (speed x binary + image x memory). Written to results/gene-votes.md at each processing
   (`review-checks.py votes ... --ledger results/gene-votes.md --append`), from seed 63 on; the last three runs count.
2. **Keep votes - strong, any one blocks.** In any of those tenths in any of the last three runs; a dependence test
   showing loss; the owner's word.
3. **A candidate:** three runs in the window, no keep vote, at least 11 of the 12 removal votes - never in a fastest,
   smallest or best-Q tenth, and under 10% of the front in at least two of the three runs.
4. **Then the dependence test, for candidates only:** every front design carrying it rebuilt with it off - a loss of 2%
   on any selection workload or 1% in bytes is a keep vote (deterministic where the gene acts on dispatches - the
   profiler; jithelp and jitre by jitleft.py's interpreted share; jitret by timing, six rounds a design).
5. **Then proposed to the owner, reversibly:** frozen off for one run with the code kept; the code removed only if that
   run's comparison shows no loss (verdict small or better). It stays in git's history either way.
6. **Votes the other way:** a frozen gene can be voted back - the small end above rule 6's bound after a freeze, or a
   knockout showing a front design losing 2% or 1% by the frozen value, is a vote to unfreeze, put to the owner.

A dry run over seeds 59-61 (tag-2 runs, older code - not in the ledger): candidates after the three - skippad, scale,
fold, sharedcall, tail, msc, hotcalls, tailpn, alignhot (12 of 12 each; scale and msc are frozen at 0 by patch 10
already); jitimg, jitvar, jitos and opcall not - each was in a fastest tenth in one of them, which the one-run rule of
430 would have missed.

Not a seed 63 rule: the best design across the machine classes is read at seed 62's processing (review-checks.py
generic over its chain's remote checks: three candidates asked for by id - results/candidates-generic.md); the generic
design is chosen when the owner asks for one (GOALS.md).

## Checked against losing good designs (Iteration 431)

**The gene rule, as first written, would have** (430; replaced by the gene votes at 432). It judged one run: "used" meant on 10% of the front or on one design
of its fastest tenth. A run's gene shares swing too much for that. Seeds 58-61's fronts (share / designs of the fastest
tenth):

| gene | seed 58 | seed 59 | seed 60 | seed 61 |
|---|---|---|---|---|
| jitimg | 5% / 5 | 4% / 1 | 9% / 5 | 4% / **0** |
| jitvar | 5% / 1 | 4% / **0** | 12% / 8 | 6% / **0** |
| jitos | **0%** | 3% / 5 | **0%** | **0%** |
| rtimm | 6% / **0** | 6% / 3 | 11% / 2 | 6% / **0** |
| opcall | 5% / 1 | 4% / **0** | 2% / **0** | 30% / 9 |

The one-run rule would have marked jitimg out after seed 61, jitvar after seeds 59 and 61, jitos after 58, 60 and 61,
rtimm after 58 and 61, opcall after 59 and 60 - each of them among the fastest designs in another run; and seeds 60 and
61 are replicates of one setup (jitvar 12% and 6%, opcall 2% and 30%). rtimm, in no fastest or smallest tenth in two
of the four, cuts fib's dispatches 13.6% where it is on (Iteration 420) - only a dependence test sees that. Hence three
runs, the smallest tenth beside the fastest, the dependence test, and reversibility.

**The freeze loses nothing worth keeping.** Of seeds 56-61's 1,050 front designs, four carried a value the freeze now
forbids, none in a smallest tenth. Rebuilt with the frozen value, all four live and are smaller: seed 57's 24d1ad82d8
with bss -1,040 bytes, seed 60's 4ac602c8bd and 129e7a9271 with lean -2,370 and -2,322, seed 61's 81a79ed494 with thinhdr
-120. The largest effect on speed, 4ac602c8bd with lean, by its dispatches: kernel +1.25%, corpus -0.31%, the other four
unchanged - for 9.5% fewer bytes.

**The rest change no design**: the verdict, the fast gate (now also checked for being too harsh), 32-bit correctness, the
small end, I+ and programs past 4 MB only measure or report. The rtimm/rtfuse proposal removes no behaviour: with
rtfuse on, rtimm=2 does exactly what it does now with pairs - one mutation further, nothing lost - and it is proposed
only if no front design relies on the overlap.
