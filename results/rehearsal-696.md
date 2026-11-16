# Step 4's rehearsal of the three genes together - rtvar (with DOES> @), rtconst, rtinline (Iteration 696)

A scratch clone at 695 (HANDOFF-REFERENCE.md's lesson, 405). results/drafts/search-reopen-plan-677.md step 4; 693 had
rehearsed rtvar and rtconst alone.

## The front, the genes off against on (evolve.evaluate at 3 rounds, two widths; two interleaved pairs each)

| role | genes it can express | speed (64) | speed (32) | the apps' code | image | total |
|---|---|---|---|---|---|---|
| least-memory | rtconst, rtinline | 0.939 | 0.950 | 8,429 -> 8,663 | 9,566 -> 10,398 | 26,187 -> 27,253 |
| portable-small | rtconst, rtinline | 1.013 | 0.993 | 8,320 -> 8,515 | 9,135 -> 9,991 | 26,871 -> 27,922 |
| portable-knee | rtconst, rtinline | 0.969 | 0.928 | 8,365 -> 8,504 | 8,953 -> 9,721 | 28,030 -> 28,937 |
| portable-arm | rtconst, rtinline | 0.967 | 0.980 | 8,340 -> 8,471 | 9,098 -> 9,882 | 30,758 -> 31,673 |
| portable-fastest | all three | 0.964 | 0.983 | 8,392 -> 8,561 | 9,642 -> 11,074 | 34,570 -> 36,171 |
| fastest-x86-64 | all three | 1.014 | 1.031 | 9,988 -> 9,985 | 9,734 -> 11,230 | 49,022 -> 50,627 |

Every evaluation status ok; smallest, best-all-round, small-jit and fastest-x86-32 express none (no run-time fusers).
The short run (--pop 8 --gens 2, seed 695): 33 records, 29 alive, the deaths 693's (two retired genes, the founders
s2-cpt16 and s1-sod16); none of the live ones expressed a new gene, as 693 found (mutation reaches them ~1 % of the time).

## Where the score moves - each workload, the genes on over off (medians of three evaluations)

| role | kernel | fib | corpus | loop | bubble | ackermann | apps | speed |
|---|---|---|---|---|---|---|---|---|
| fastest-x86-64 | 1.038 | 1.016 | **1.218** | 0.935 | 0.889 | 0.913 | 0.986 | 0.993 |
| portable-small | 1.024 | 1.003 | **1.109** | 0.981 | 0.878 | 0.899 | 0.965 | 0.976 |
| portable-knee | 1.046 | 0.992 | **1.150** | 0.997 | 0.864 | 0.921 | 1.025 | 0.998 |

The programs gain (bubble, ackermann about 0.9); the corpus, which compiles source, pays: the compile layer's cost
relf warned of. Each gene alone on the knee's corpus (medians of 7): rtconst 1.018, **rtinline 1.125**, rtvar 1.055 -
but varslot alone, which rtvar needs and the knee lacks, 1.016 of it.

## rtinline's scan made cheaper (in this iteration)

INL-UNFOLD searched the up-to-26 fold pairs for every instruction scanned, on every call compiled. A bitmap of the
folded codes (INL-OPS [64-95], 32 bytes) leaves the search to them: rtinline's corpus cost 1.125 -> 1.065-1.083 (two
measures). What is left (SOD16_NO_INLINE=1 writes the table empty, to measure): an empty table 1.024-1.059 of the
corpus, the copying 1.5-2.5 % more. A second bitmap, of the codes a body can begin with, to pass over calls to anything
else at once, bought nothing measurable (1.080 and 1.066 with it) - the scan's cost is in words that begin with a
copied operation - and was taken out. rtinline-check.py PASS on portable-knee and fastest-x86-64 after it.

## What it means for the run

The genes pay on run-time code - the programs alone 5-15 % (rtinline), shellmix 0.61-0.78 (DOES> @) - and the score's
fib, loop, bubble, ackermann; they cost the corpus 6-20 %, the kernel workload a few %, and 0.8-1.6 KB of image. The
score nets 0.94-1.01: the search will weigh them, and may well take them only toward the fast end. Decided by the run.
