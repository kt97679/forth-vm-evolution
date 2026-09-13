# The stage ladder

Every stage in this table is a *working system*: an engine binary plus an
image that boots, runs the shell, and (where marked) compiles new Forth
definitions. Nothing here is modelled or estimated.

The article's claim is that each row is reachable from the row above it
by one identifiable change, and that the cost of each change can be
measured in two dimensions at once: image bytes, and time to recompile
the kernel.

| id | name | one-line change from the previous row | self-hosts |
|----|------|----------------------------------------|------------|
| `s0-cell` | RelF, cell threading | baseline: one host cell per operation | yes |
| `s1-sod16` | SOD16 | one 16-bit token per operation; `>=256` indexes a word table built at load | not yet |
| `s2-cpt16` | CPT16 | delete the table: a call target is `base + (v << S)` | not yet |
| `s3-cpt16f` | CPT16 + folding | fold `prim;EXIT` into single opcodes; inline data prims | not yet |
| `s4-cv8` | CV8 | narrow the unit from 16 bits to one byte; calls become 2-3 bytes | not yet |
| `s5-cv8spec` | CV8 + specialisations | locals, variables, tiny kernel words and small ints as opcodes | yes |

## Self-hosting

A stage self-hosts when the image's own compiler emits that stage's
encoding. Only `s0-cell` (the compiler that was always there) and
`s5-cv8spec` (via `forth/cv8.4`) do so today. The intermediate images are
*translated* from the cell image by `tools/layout.py`, which means they
run every word that was compiled into them but cannot compile a new one.

This matters because it decides which benchmarks a stage can take part
in. See `bench/README.md`.

## Cell widths

Every stage is built at both 8-byte and 4-byte cells from the same Forth
source. The 4-byte column is not decoration: it is where the density
argument is weakest, because a cell is already only 4 bytes there, and
the article should say so.

## The stage that was never supposed to exist

`p8-pack8` is not a step on the road to CV8. It is a design that was
proposed, costed, and rejected in Iteration 157 without ever being
built - `ENCODING-COMPARISON.md` calls it "tagged byte (8-bit x3/x7)" -
and it is here because the rejection rested on a synthetic benchmark
whose author flagged it as the pessimistic case.

A cell is a call, a plain primitive, or a PACK: a tag byte plus one
opcode byte per remaining byte of the cell. The plain cell form survives
underneath, which is what lets this stage self-host with no compiler
overlay at all - the existing compiler already emits valid, if unpacked,
PACK8.

`tools/pack8.py` rewrites runs of primitives in place and steps `ip`
over the cells they occupied, so the image keeps every address it had
and needs no relocation pass. The density is therefore reported as an
exact count of cells folded away rather than as a smaller file. See the
tool's header for why that is the right trade for this question.
