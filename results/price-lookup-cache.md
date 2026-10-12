# A name-lookup cache, priced (Iteration 221)

The handoff's open item 5 (results/loop-audit.md, "What would cut the lookup
loop", 2): a cache from name to word beside the threads gene, cleared exactly
on every definition and order change. Priced offline with
results/drafts/lookup-cache-model.py, as loop-audit-chains.py priced the
chains: the workload's own token stream (comments and strings skipped; a
number looked up first, as INTERPRET does; `'` and POSTPONE looking up their
name; the dictionary growing as it defines, every pass of the long workload
defining again), the kernel's hash of the length and two characters, FORTH
searched once (the audit), the design's image names by the converter's
symbol map. Cost: dictionary entries visited per lookup. Seed 43's smallest
design, add5ec8937 (313 names):

| workload | lookups | chains | entries a lookup now | of them for names not found | with a cache of 16 / 64 / 256 entries | lookups it serves |
|---|---|---|---|---|---|---|
| corpus | 33,150 | 16 | 23.5 | 57% | 18.3 / 16.5 / 15.4 | 46% / 56% / 63% |
| corpus | 33,150 | 32 | 12.2 | 53% | 9.3 / 8.4 / 7.8 | 46% / 56% / 63% |
| corpus | 33,150 | 64 | 6.1 | 41% | 4.3 / 3.9 / 3.6 | 46% / 56% / 63% |
| parse | 96,009 | 16 | 22.7 | 49% | 11.8 (any size) | 50% |
| parse | 96,009 | 32 | 12.4 | 46% | 6.3 | 50% |
| parse | 96,009 | 64 | 5.8 | 39% | 2.8 | 50% |

**Not built.** At the 16 chains most of seed 43's front chose (121 of 165), a
16-entry cache cuts the walk 22% on the corpus and 48% on parse; doubling the
chains instead halves it on both, and 64 chains cut it by three quarters -
for 128-384 bytes of heads, which evolution already declined at the small end
(the bytes won). A cache costs its code in the image and its invalidation in
every header-making word, for less per byte. Half of the walk is names not
found - numbers and names being defined, 57% of the corpus's visits and 49%
of parse's at 16 chains - which no cache of found names can serve: a filter
per chain (a bitmask of what its names could be, set as headers are made)
would reject most of them without a walk. Not priced in bytes; it would meet
the same verdict as the chains unless much cheaper. Recorded in GOALS.md's
register.
