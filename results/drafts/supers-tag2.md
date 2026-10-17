# The supers gene in tag-2 designs: a misnamed pool, and no slots (Iteration 367)

**The finding.** design_pairs (lab/evolve/evolve.py) profiles a design and gives the supers gene its
pool - the hottest primitive pairs a mutation may fuse. It names each profiled code as a plain CV8
opcode. A tag-2 design profiles its own one-byte codes (the engine: `if (T2_IS_OP(t)) PROF(t)`), which
the converter assigns through a per-design table (vm-tag2-one.h; t2hot orders it hot first). Seed 56's
fastest (a0a0277bf2): its table is the identity for the first 5 codes of 128 only. So every tag-2
design's pool has been its codes misread - since tag2 (Iteration 66), the lineage of every front since:

| the pool the search saw | share | what it really was |
|---|---|---|
| OR DROP | 5.12 % | DUP, then a specialisation (op 71) |
| DUP + | 5.11 % | a specialisation (op 68), then + |
| AND + | 3.80 % | op 90, then + |
| OR AND | 3.80 % | DUP, then op 90 |

and wide codes 128-191 (t2wide) were dropped outright (`a < 128`).

**What it cost.** Little speed, by accident: the slots superinstructions take (super_slots: 126-127, the
fold band past the folds, the specialisation band when spec is off) are first taken by format-10
words (ops10) - the fastest design lists 17 pairs and has 16 slots, all its 16 ops10 words'. Across the
fronts: seed 55, 168 designs listing 2,940 pairs, 4 building any (71 built); seed 56, 187 designs,
3,234 listed, 6 building any (94) - and those built misread pairs: NEGATE NEGATE, DROP UM*, C@ OR,
XOR C!, RSHIFT @ - engine bytes for nothing, against the small end's size.

**What is really there** (a0a0277bf2 over kernel, fib, parse and corpus, 105,295,516 dispatches; the
fusable pairs - primitives among the first 33, no control flow - named through its table): + XOR
3.80 %, then SWAP OVER and OVER ! 0.25 % each, the rest below 0.1 %. Its other fusions (folds,
specialisations, format-10 words) have taken the rest.

**The fix** (results/applied-after-seed57/tag2-pairs-after-seed57.patch): codes named through the table, wide codes
kept. Tested: the fixed pool of a0a0277bf2 is the hand count's; the same genome without the tag - named
right all along - gives the same ten pairs. **Decided (Iteration 368; the owner left it to the lab): no new mechanism - GOALS.md's rule.** A
slot allocation by value would profile every design in evaluation and tie the genome to its profile:
complexity, for one pair at 3.8 % of dispatches. The search can already make the trade: a pair listed
first lies dormant, free to drift, until a mutation drops a format-10 word - which then weighs the
word against the pair in one step. With the fix, the pool is right. **After seed 58, measured**: if
no front design builds a real pair, or a knockout shows superinstructions buy nothing, the supers
gene comes out of tag-2 designs - a mechanism that buys nothing comes out (rtlit, Iteration 59).
