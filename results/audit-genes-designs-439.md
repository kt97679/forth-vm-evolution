# Are good genes or promising designs being rejected? A deep audit (Iteration 439)

The owner: a deep audit to ensure we are not rejecting good genes and promising designs, and of any genes not used
yet. Sources: seed 62's database (38,210 CV8 designs, every one the run made), seeds 58-62's fronts, the current master
(the after-seed-62 batch applied). The per-gene table: results/drafts/audit-genes-439.out.

## 1. Where the pipeline turns designs away

| where | what it turns away (seed 62) | verdict |
|---|---|---|
| Survival (NSGA ranking, crowding) | designs off the front each generation | guarded: the attic keeps 128 demoted designs carrying gene values the population lost, a tenth of parents drawn from it; each family's best and the 8 best by Q always survive |
| The surrogate screen | 7,547 children never measured (20%) | **works, at a small cost**: of 880 screened children measured anyway, 1 reached the final front against 5.3 expected at the base rate (0.60%) - so about 9 front-quality designs a run go unmeasured (1 in 880 of 7,547), for a fifth of the run's measuring saved. Keep; an option below |
| The reach limit | 219 refused, not run | gone with the freeze (varcall and doesfar always on, patch 10); rule 4 checks it |
| 32-bit failures (both widths selected) | 1,966 - every tail design, and bfind without tos | **fixed and verified**: on today's master a design of each failing kind - tail with GCC, tail with clang, tail with preserve_none - builds and lives at 32 bits; tail and tailpn get their first fair run in seed 63 |
| The freeze (patch 10) | values off the frozen ones | checked at 431 and 433: 13 front designs over seeds 56-62 broke it, every one smaller and alive with the frozen value |
| The rules (results/seed63-rules.md) | genes proposed out | guarded: three runs of votes, keep votes blocking, a dependence test, reversible (431-432) |
| The tag-2 requirement | plain-CV8 designs (seeds 59-62) | gone in seed 63 |
| Selection on the laptop alone | designs best across the machine classes | a known blind spot: bf439eb307, rejected by seed 60's selection, the best on all three machines in seed 61's chain - the head to head in seed 63's chain measures it |

## 2. The genes - which are not used, and why

| gene | seed 62: set / expressed | fronts 58-62 | why |
|---|---|---|---|
| jithelp, jitre, jitret | 0 / 0 | - | new (the batch); seed 63 is their first run - no founders carry them, mutation must find them (some 3 draws a generation each) |
| **rtloopall** | 5,819 / **92** | 55, 65, 28, 42, **1%** | **blocked by its prerequisite**: all eight loop words in the format-10 list. Of the 5,819 genomes that set it, 4,159 lacked some - J in 4,044, UNLOOP in 3,380, (LEAVE) in 3,250 - and 1,465 had rtloop off. Words that buy little alone: a stepping stone, reached by chance - on 42% of seed 61's front, 1% of seed 62's |
| **rtiplus** | 10,485 / **1** | 23, 5, 1, 5, 0% | needs rtloopall: blocked behind it. Patch 11 made it fire on the tag, but only where rtloopall is - rule 7's prediction (I+ on 10% of seed 63's front) rides on rtloopall's chance |
| tail, tailpn | 2,925 / 2,138; 10,991 / 1,046 | 0% | every one died at 32 bits - fixed (above) |
| hotcalls | 4,991 / 0 | 16, 0, 0, 0, 0% | none under the tag by design; back in the free seed 63 |
| sharedcall | 35,190 / 79 | 0% | unexpressed under the tag (its own call path); 0% on seed 58's free front too - the votes will decide |
| alignhot, jitos, knumber, regpin, jitimg, jitvar, rtimm | 4,755-12,084 set, 788-4,189 expressed | 0-12% | rare but used - each in a fastest tenth in some run, or blocked only by its own prerequisites (the JIT, clang) |
| msc, scale; bss, thinhdr, lean, bytehdr, doesfar, varcall | - | 0% / 96-100% | frozen (patch 10) |

**The one real rejection found: rtloopall, and rtiplus behind it.** Not by a rule or a gate - by a prerequisite the
search can only meet by chance: eight list entries at once, three of them (J, UNLOOP, (LEAVE)) worth little alone.
When a lineage meets it the gene spreads (28-65% of seeds 58-61's fronts); when none does, it is gone (seed 62: 1%).
That is between-run luck of exactly the kind the replicates measured at the fast end.

## 3. Mechanisms that are not genes yet (lab/evolve/GENES.md, "Not yet")

| mechanism | state |
|---|---|
| Translation to direct threading at load | never built nor priced - the one untried idea left |
| Dynamic superinstructions (SPN's phase 3) | SPN's genes, phase 3 |
| A register machine | parked (418-424): its gains mostly reachable through existing genes; two of them made cheaper (the after-seed-63 batch) |
| Indirect threading | priced out (Iteration 29) |
| relf's format 10 | the words, loop words, short branches and escape - in relf's genome |

## 4. Recommendations - each the owner's call

1. **A repair for rtloopall** (a patch after seed 63): when a mutation turns rtloopall on, the missing loop words go to
   the front of the format-10 list, so they get their slots. The search still weighs it - the words take slots from
   others, which can cost (Iteration 420: kernel and corpus 6-9% for one slot) - but it no longer depends on eight
   draws coinciding. rtiplus follows it.
2. **Direct threading at load, priced** - the one mechanism never measured; a pricing like 418's, kept apart.
3. **The screen, an option**: measure screened children anyway when their predicted speed falls in the fast tenth -
   the few front-quality designs it costs a run are likeliest there. Small; only if seed 63's audit line shows more
   than one reaching the front.
4. **Nothing for the new JIT genes now**: mutation reaches them in a few generations; founders (as Iteration 155 gave
   the JIT's earlier genes) only if seed 63's front shows them absent for want of a start.
