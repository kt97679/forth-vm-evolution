# The gene factor - repeated code moved into headerless shared bodies (plan, Iteration 264)

## Why

Iteration 263's price: on the smallest design's image, runs of whole
instructions that recur byte for byte - no branch, branch target, EXIT, fused
EXIT or return-stack word inside, within a word - factored greedily into
bodies the converter makes and never names: **154 bytes with 2-byte calls (40
bodies), 359 with 1-byte calls** where slots allow. The echo instruction would
save 283-427 before its handler and needs end-of-fragment detection in the
interpreter; this needs no engine change. Iteration 254's 12 bytes charged each
body a header it does not need. The cost: a call and a return wherever a body
is used - so hot code is left alone.

## Where it goes

- **tools/layout.py**, after the loop at line ~280 that fills `kind, info, tok`
  for every word (each word keyed by its start in the dump, `w['s']`; `tok[s]`
  the CV8/tag-2 token list `to_tokens` produced through sod16.py's rewrites -
  shorten, keepbranch, specialise, fuse_pairs, fold_exit ...), and before
  placement (`new_body_bytes` sizes bodies from `len(tok[s])`).
- **The pass:** (1) cut every code word's tokens into safe runs - split at
  branch tokens and at their targets (sod16.branch_targets), at EXIT and fused
  EXITs, return-stack operations, and any token with an OPD, XT, STR or ALN
  operand (they align or relocate); (2) greedy: the run with the largest net
  saving, k uses x (len - call) - (len + 1), recomputed after each choice, as
  /tmp/factor.py did - kept in results/drafts/ when built; (3) each choice a new
  word: a synthetic key past the dump's end (the maps are keyed by old
  addresses), `kind` 'code', `tok` = the run + EXIT, its name `(F<n>)` for
  CALLMAP and the tools, and **in HL** - Iteration 190's headerless set: code,
  no link, no name, on no thread; (4) every use replaced by a call token to the
  key; (5) the new words appended to `order` at the end, so they sit after
  (PRIMITIVES-END) - PRIMITIVE? (Iteration 242) must never take one for a
  primitive.
- **Left out:** words the run-time compiler reads or patches (T2_CONSTS,
  G['HOT_PATCHED'], opbody's [opcode EXIT] bodies, the X8 bodies swapped in,
  PRIMITIVE stubs, the dump tool's words) and **hot words**: the reference
  profile the tag's ranking uses (t2hot) names them - a word in its top share
  keeps its code.
- **The gene:** `factor` (0/1) in LATE and EXPRESSED['cv8'] for the tag; the
  converter's `--factor`; a 1-byte call when the body earns a hot slot
  (hotcalls), else 2.

## Checks before it is a patch

engines-check with factor on (and with tail, msc, the JIT); names-check (the
CALLMAP names); run-tests; the gate; ans-check on the small end; dispatch
counts on the corpus and kernel (each factored use adds a call and a return -
on cold code it should not show); the image bytes against Iteration 263's
price.

## Built (Iterations 267-268): after-seed-47 patch 6

Where the build parted from this plan, and why:

- **A use is the call and a GAP**, an operation of the run's remaining cells and
  no bytes (sod16 op_cells, op_bytes). Branch, loop-operand, xt and DOES>-entry
  offsets are old cell offsets and the locals literals are found by adjacency;
  one call in place of a run would have shifted every offset after it.
- **No 1-byte calls**: the tag has none (FORMAT-TAG2.md, decision 4), so every use
  is 2 bytes and 263's 154, not 359, was the price to meet.
- **Hot words by levels, not one threshold.** The first build (cold words only,
  below 0.01%) saved 16 image bytes; lifting one exclusion at a time showed the
  hot-word filter was the gap and the safety rules cost 3 bytes. Counted on
  3456ac1e5e: below 0.1% -41 bytes for +0.007% dispatches, below 1% -95 for
  +0.17%, every word -127 for +1.98% - a trade-off, so the gene's levels.
- **The swapped compiler bodies take part**: a GAP keeps the old cell offsets
  their xts resolve from.
- **Placed after the tag's ranking**, before the token fill: the ranking counts
  the uses as they were before factoring - reproducible, near enough.
- The converter's own estimate runs ahead of the image (31 against 16, 147
  against 127): not explained yet; image bytes are what is measured.
