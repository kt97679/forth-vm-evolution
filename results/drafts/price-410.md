# Two levers for the interpreted designs, priced on seed 60's front (Iteration 410, HANDOFF item 4e)

**Handler replication for calls and returns** (Ertl and Gregg: copies of EXIT and the call handlers, each copy its own
indirect jump, so each sees fewer targets). Its bound, from the laptop's counters (results/counters-amd-ryzen-7-pro-
8840hs.md, Iteration 285) and the misprediction map (results/missmap-amd-ryzen-7-pro-8840hs.md, Iteration 301): on the
compute workloads - fib, loop, bubble, ackermann - every interpreted design mispredicts at most 0.54 branches a thousand
instructions, dispatch already predicted; on kernel and corpus the misses cost 6.8-23.6% of the fast designs' cycles
(12-18 cycles a miss), and calls and returns are 15-25% of them. If replication removed every call and return miss:
kernel 1.5-5.9% faster, corpus 1.0-3.4%, the rest nothing - the six workloads' geometric mean 0.4-1.6%, a bound no
replication reaches on a predictor that already follows history. And it removes no dispatch, where the front end waits
on the taken indirect jump itself (Iteration 301: the remedy is fewer of them). **Not built.**

**The register machine, re-priced** - the share of dispatches that only move a value or push a lone literal, what a
register machine could remove at most (lab/evolve/stackops.py, its profile parse fixed for the profiler's later lines),
for seed 60's three fastest interpreted designs (4ac602c8bd, 129e7a9271, f36c7b4bd1):

| workload | the bound | the largest movers |
|---|---|---|
| kernel | 11-13% | ROT 6%, DROP 4% |
| fib | 7-14% | DROP 7% |
| corpus | 12-15% | DROP 5%, ROT 4% |
| loop | 20% | R> 20% |
| bubble | 39% | R> 26%, DROP 13% |
| ackermann | 0.1% | - |
| sieve (held out) | 21-22% | ROT 7%, DROP 5% |
| parse (held out) | 9-13% | DROP 4%, ROT 3% |

Seed 5's front gave 38-50% (Iteration 29): folds, specialisations, the cached top and the format-10 words have taken most
of it. The first stage as planned (lab/evolve/regprice.py: register forms within a block, the stack synchronised at
calls, returns and branches) saves 3.8-4.8% of kernel's image-code dispatches, 6.5-7.4% of corpus's, 7-8% of parse's -
and only the image's code: fib, loop and bubble run code compiled at run time (0-1% of their dispatches in the image),
where the compiler would have to emit the register forms too. **The lead it leaves**: R> in the run-time-compiled loops
of loop and bubble (20-26% of their dispatches) and DROP, ROT - a run-time fusion's target (the rt* genes' family),
cheaper than a register machine; to be priced next.

## Corrected (Iteration 411): the register machine's table, and its lead

**The table above is wrong**: stackops.py named each opcode by the old one-byte layout, and seed 60's designs - escape 2,
the two-bit tag - number theirs otherwise. The converter's own map (CALLMAP) for 4ac602c8bd: the opcode stackops called
R> is I, its < is DUP, its NEGATE SWAP, its LSHIFT XOR, its DROP LIT8 (results/drafts/opnames-411.py). stackops.py now
names an opcode by the converter's map first. Again, the same three designs:

| workload | the bound | the largest movers |
|---|---|---|
| kernel | 20-22% | ROT 6%, DUP 3%, >R 3%, SWAP 2% |
| fib | 7-14% | literals 7% |
| corpus | 24% | SWAP 4%, ROT 4%, DUP 3%, I 3% |
| loop | 40% | DUP 20%, I 20% |
| bubble | 46% | I 26%, literals 14%, SWAP 6% |
| ackermann | 19% | DUP 10%, SWAP 10% |
| sieve (held out) | 28% | ROT 7%, DUP 7%, I 4% |
| parse (held out) | 23% | SWAP 5%, >R 3-5%, ROT 3% |

So the prize is larger than the first table said, and **there is no R> lead: it is I**, the loop index - 20% of loop's
dispatches and 26% of bubble's. Its fusion exists: the gene rtiplus (Iteration 60) compiles I + as I+ at run time - and
on 4ac602c8bd it does nothing. With rtiplus on, I+ gets its opcode slot and the overlay its kernel variant
(k64-bt-...-loopall-iplus), yet the loop's dispatches stay 20,032,046 against 20,031,683, I still 4,000,038 of them
(results/drafts/rtiplus-count-411.py): on the two-bit tag the fusion never fires - an expressed gene with no effect,
as bfind was on the cached top. (A timing of the two here, results/drafts/rtiplus-time-411.py, said -5.5% on the
geometric mean - with -19% on ackermann, where nothing differs: this VM's noise and layout, not the gene; a dispatch
count is the measure to trust here.) **The lead now**: make I+ fire on the two-bit tag - cv8-fuse-iplus.4 was written
for cv8-fuse.4, and a tag-2 kernel loads cv8t-fuse.4 - or, failing that, rtiplus needing a design off the tag.
