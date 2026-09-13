# The stage ladder

Every stage in this table is a *working system*: an engine binary plus an
image that boots, runs the shell, and (where marked) compiles new Forth
definitions. Nothing here is modelled or estimated.

The article's claim is that each row is reachable from the row above it
by one identifiable change, and that the cost of each change can be
measured in two dimensions at once: image bytes, and time to recompile
the kernel.

| id | name | one-line change from the previous row | emits its own encoding |
|----|------|----------------------------------------|------------|
| `s0-cell` | RelF, cell threading | baseline: one host cell per operation | yes |
| `p4-pack4` | tagged nibble | pack 4-bit opcodes into a cell behind a tag byte; rejected by a 2024 design note, built here | no |
| `p8-pack8` | tagged byte | the same with byte opcodes | no |
| `s1-sod16` | SOD16 | one 16-bit token per operation; `>=256` indexes a word table built at load | yes |
| `s2-cpt16` | CPT16 | delete the table: a call target is `base + (v << S)` | yes |
| `s3-cpt16f` | CPT16 + folding | fold `prim;EXIT` into single opcodes; inline data prims | yes |
| `s4-cv8` | CV8 | narrow the unit from 16 bits to one byte; calls become 2-3 bytes | yes |
| `s5-cv8spec` | CV8 + specialisations | tiny kernel words, small integers and immediate operands as opcodes (see the note below on locals and variables) | yes |
| `s6-cv8b` | CV8 + byte headers | dictionary link becomes a 1-3 byte backward-tagged distance; names and code bodies stop being padded; call scale drops to 0 | yes |

## Self-hosting

EVERY stage cross-compiles the kernel and produces an image byte-identical
to the reference - that is the gate `bench/kernel-compile.sh` applies
before it times anything, and all nine pass it at both cell widths.

The last column above is a narrower question: does the image's own
compiler EMIT that stage's encoding? For `s1` through `s6` it does, via
the overlays in `forth/` - `sod16.4`, `cpt16.4`, `cv8.4`, `cv8b.4`.

`p4-pack4` and `p8-pack8` are the exception. They rewrite a finished cell
image in place, so the compiler they carry is the cell compiler and the
code it compiles at run time is unpacked. They self-host in the sense
that matters for the benchmark - same input, same output image - but a
word defined after boot is not packed.

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

## What the specialisations actually contribute

`--spec` takes five names and only three of them do anything to the
images this project measures. Measured on the 8-byte kernel, bytes saved
by each in isolation:

    tiny   194     small  190     imm    111
    loc      0     var    -18

`loc` is inert because `locals.4` is loaded only into the SHELL image,
not into the kernel that every benchmark here runs - so there are no
locals to specialise. The engine's locals opcodes are real and tested
(`tests/core/locals.fth`, run by `tools/run-tests.sh`), but they do not
appear in the measured images.

`var` makes the image slightly LARGER. It may still be worth its place
on time rather than size, but measured here the difference between
`loc,var,tiny,small,imm` and `tiny,small,imm` was 8 bytes and 0.8% on
kernel compilation - the latter well inside the noise. Treat "locals and
variables as opcodes" as a description of what the ENGINE supports, not
of where the measured gain comes from.

The build keeps all five (`SPECS` in `tools/build-stages.sh`) so that
the published figures are not invalidated; the note is here so nobody
reads the gain as coming from parts that contributed none of it.
