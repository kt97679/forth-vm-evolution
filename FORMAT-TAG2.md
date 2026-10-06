# FORMAT-TAG2.md - the two-bit tag: 64 opcodes and a 1 GB code space

The byte format evolved designs move to, decided with the owner on
2026-10-06 (Iteration 64). It is relf's planned next format, taken here
first: relf's `docs/GOALS.md` item 2 ("a two-bit selector") and
`docs/OPTIMIZATIONS.md` Z5, declined in relf "for now" by its decision A15
("use the smaller opcode set, but don't implement the 1 GB call range
yet"), priced by relf's Iteration 501 at 0-0.7% on real workloads - "a
format decision, not a performance one" (relf `docs/CV8.md` 13).

## Why

The CV8 every design here uses so far is relf's older one: 128 one-byte
opcodes, calls of two bytes (14 bits, 16 KB) and three (22 bits, 4 MB),
the target a byte offset from the image base. Evolved designs add 32
one-byte "hot" calls in the top of the call space, which leaves the far
call 21 bits: **2 MB**, with 16 MB of engine memory above it, and nothing
in the run-time compiler's `CALL,` to stop a call to a word past 2 MB
being encoded as a hot call to some other word. The owner: limiting the
code space to 2 MB "can hit us badly in the future"; be consistent with
relf - 64 opcodes, more through escapes - and able to address 1 GB, in
whatever format keeps images small.

## The decisions

1. **The byte format** - the top two bits of the first byte:

   | first byte | meaning | bytes | reach |
   |---|---|---|---|
   | `00xxxxxx` | opcode: 64 one-byte codes | 1 (+ operands) | - |
   | `01xxxxxx` | call, 6 + 8 = 14-bit offset | 2 | 16 KB |
   | `10xxxxxx` | call, 6 + 16 = 22-bit offset | 3 | 4 MB |
   | `11xxxxxx` | call, 6 + 24 = 30-bit offset | 4 | **1 GB** |

   A call's offset is the target's distance in bytes from the image base,
   not from the call site (relf's idea: no pointer in an image). Both
   compilers pick the shortest form that reaches, as they pick a literal's.
2. **64 one-byte opcodes**, one of them `ESC` plus a selector byte: 256
   more, two bytes each, a second dispatch. (relf A15.)
3. **One-byte codes by measured rank.** The converter ranks every
   operation a design has - primitives, specialisations, pairs, format-10
   words, folds - by the design's own dispatch profile, exact counts, so
   the numbering and the image are reproducible; the hottest get the
   one-byte codes, the rest are escaped (relf Iteration 501's method).
   Evolution chooses which operations exist; their codes follow from the
   profile. This retires the "put X first" genes (tfind, kinput's and
   klookup's lists, rtiplus's and swapi's slots) - they stay for the
   designs recorded with them.
4. **No hot calls** - the format has no call prefix to spare, and relf has
   none.
5. **Variable length everywhere; a full cell only where nothing smaller
   holds the value.**
   - calls: 2, 3 or 4 bytes, by distance;
   - dictionary links: 1-4 bytes, read backwards from the name, with the
     same two-bit tag as calls (the one-byte link holds 6 bits, not 7);
   - branches: relative, within one word, at most 16 bits (+-32 KB -
     "enough for a relative jump in reasonable code"). Backward branches
     8 or 16 bits by distance, in both compilers. Forward branches: the
     run-time compiler, compiling in one pass, does not know the distance
     when it compiles IF, so always 16 bits; the image converter sees the
     whole definition and uses 8 bits where they reach;
   - `CREATE` reserves room for a later `DOES>` call whose target it
     cannot know: the longest call, 4 bytes;
   - literals: 1, 2, 4 bytes, or a full cell, by value (as now);
   - every other operand with a reach (variable slots, tables the
     converter fills) audited and widened the same way.
6. **Engine memory** stays a parameter (16 MB by default, `RELF_MEMSIZE`
   at run time); the format no longer caps it below 1 GB.
7. **The old CV8 stays buildable**: every recorded design rebuilds as
   recorded; the hand-made stages, and s6 as the measure of speed, do not
   change. New runs evolve only the new format, carrying the current
   front's genomes into it; the old front is the baseline the new one is
   compared against - the owner accepts changed designs if they buy the
   code space and keep images small.
8. **Not ported**: the native-code SPN stages read the old format and
   are not used by evolved designs.
9. **Proof**: the life test and the differential tests in all four engine
   forms; a test that compiles words past 4 MB and calls them - the
   30-bit form exercised, links across it - at both cell widths.

## The plan

- **T1 engine** (`TAG2`) - **done, Iteration 65**, base and cached-top
  engines; the multi-state generator (gen-msc.py) finds the dispatch fill
  by pattern and copies the call path per state, so it needs its own port
  (**T1b**) - **done, Iteration 70**, with gen-tail.py's port: all four
  engine forms read the tag.
  Dispatch by tag - 0x00-0x3F through a 64-entry
  table, 0x40-0xFF to the call path, three widths; `ESC` through a
  256-entry table; both tables from a header the converter writes for
  the design (every handler already exists - the ranking only orders
  them); the link decoding shared by the handlers that walk the
  dictionary (THREAD-FIND, (FIND)).
- **T2 converter** (`--tag2`) - **core done, Iteration 66**: ranking (a
  reference profile's weight, then static use; the reference file still
  to make), the map headers, opcodes, calls, links, DOES> bodies; a
  tag-2 design boots and interprets. Left for T3: the run-time compiler's
  tables in tag-2 codes. The ranking from the design's profile; the
  map header; opcodes in one or two bytes; calls of 2-4; links of 1-4;
  branches as above; `DOES>` with a 4-byte reservation; the run-time
  compiler's tables with this design's codes.
- **T3 the run-time compiler** - **done, Iteration 67**: forth/cv8t.4,
  cv8bt.4, cv8t-fuse.4, cv8t-fuse-imm.4; the converter rewrites the opcode
  constants and the tables; a tag-2 design passes the life test (8,314
  bytes against 7,799 in the old format, static ranking). The plan was
  `forth/tag2/` - cv8.4 and cv8b.4 and every
  overlay that assumes the old numbering - with `OP,` escaping what has
  no one-byte code, `CALL,` in three widths, branches and links as above.
  The old files are frozen by the designs recorded with them.
- **T4 evolver** - **done, Iteration 71**: the gene `tag2` (converter
  before engine), `t2hot` (the ranking's threshold), `--require tag2`
  and next-run.sh's `seed N tag2`; carried designs re-encoded as the
  run's own. (The analysis tools still name opcodes the old way.) The
  plan: the gene `tag2`; profile, rank, then build; new runs
  with `tag2` required; hot calls off under it; the profiler and the
  analysis tools reading calls as 0x40-0xFF.
- **T5 proof** - **done, Iterations 67-70, but 32-bit cells**: alive in
  all four engine forms, the differential tests identical, calls and
  links past 4 MB right; the price +5.4-5.8% size and +2-3% dispatches
  on the front (Iteration 69). Left: 32-bit cells (the converter refuses
  them under the tag: a DOES> body's 4-byte call does not fit a 4-byte
  first cell) - before the Tegra. The plan: decision 9 and the price,
  counted on the VM: size and
  dispatches of the current front re-encoded, design by design.
- **T6 laptop runs**: seeds with `tag2` required, carrying the front.
  Seed 16 (Iteration 72): the old front moved ~370 bytes right at about
  its speed - the price, confirmed; the old format keeps the front of all
  runs until the tag-2 runs win it back.
