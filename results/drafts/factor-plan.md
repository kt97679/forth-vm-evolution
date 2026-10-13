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
