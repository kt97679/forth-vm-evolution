# TRIZ applied to the search - the contradiction inventory and mechanism 9 priced (Iteration 706)

The owner (706): "use whatever is useful from TRIZ, proceed". TRIZ (Altshuller's ТРИЗ) proposes; measurement decides, as
always here - a candidate is priced first (bytes exact, dispatches by the profiler) and offered to evolution as a gene,
the owner choosing (HANDOFF-REFERENCE.md's standing decisions). Taken from TRIZ: the contradiction (technical: improving
one objective worsens another; physical: one element needs opposite properties), its elimination by **separation** (in
time, in space, on condition, between the whole and its parts, by moving to the supersystem or a subsystem), the ideal
final result (the function without the element), resources already present, trimming, S-curves. Not taken: the 39x39
matrix, the 76 standards, substance-field models and the effects database - tuned on physical patents, the matrix's
reliability itself questioned in the TRIZ literature; no published case of a software problem solved by them (Mann,
TRIZ Journal 2004).

**What TRIZ says about where we are**: an S-curve's plateau - the series' fastest 0.1245, 0.1218, 0.1216, 0.1199, 0.1190
over seeds 92-96 (4.4 %), nothing at either width after seed 96's generation 84 (results/stopping-series.md). The next
gain comes from a new principle - a mechanism, a gene - not from more generations; the search's own history agrees
(677: the reopening was new genes). Much of what moved the fronts already was a separation, unnamed: run-time compilation
(rtvar, rtconst, rtinline: in time), the lazy JIT and hot-word inlining (on condition), per-word encodings and near/far
calls (local quality, in space), self-hosting (trimming: the translator's job done by each design), consolidation
(trimming), deciding by dispatch counts (a resource already present). The register (GOALS.md) already holds TRIZ's
obvious others: the compressed image (separation by system level - rejected, 236: memory grows), headerless words
(trimming - deferred, 222-223), the echo instruction (260).

## The method - a contradiction inventory, when new genes are wanted

1. From a run's records: each technical contradiction on its front - a gene's pairs (lab/evolve/newgenes.py: the same
   expressed genome but for the gene) give "speed x for +y bytes"; a gap between two roles gives the rest.
2. Restated at one element: "E must be A (for objective 1) and not A (for objective 2)".
3. The separations, each: in time, in space, on condition, whole and parts, supersystem and subsystem - and the
   resources already there (the JIT's own memory, dead bytes, a structure that already holds the fact).
4. Each candidate checked against GOALS.md's register, then priced (lab/evolve/mech-census.py, mech-price.py; a prototype's
   bytes where the engine changes) - a row below.
5. The ones that pay: built as genes (the step-3 pattern of 687-695: the overlay, the engine, layout.py, the
   self-hosting compiler, the checks), the owner choosing which and when.

## The inventory - seed 96

| # | contradiction (from the records) | the element and its physical contradiction | separation | state |
|---|---|---|---|---|
| C1 | the run-time fusers: rtinline 0.939 of the speed for +672 B (441 pairs), rtconst 0.985 for +339, rtvar 0.980 for +505 (results/drafts/newgenes-seed96.txt) | the fuser must be in the image (the programs compile at run time) and must not (its bytes) | on condition - in use (rtinline's 3 instructions in 6 bytes; hotinl); by system level - the fuser in C | C: not pursued - the plan keeps run-time mechanisms in the overlays the translator and the self-hosting compiler share (search-reopen-plan-677.md, "What stays") |
| C2 | the JIT designs' size: the 5-byte header in every definition - 875 B of the five programs' code (175 definitions), 3,415 B of the held-out three's (683) | the header must be there (the first call translates; later calls find the native code) and must not (5 bytes a definition) | the field: on condition and in time (below); the trigger byte: none - it is the price of being lazy | **priced below - the one open candidate that pays past 1 %** |
| C3 | the 2@ of a tos=1 GCC design: one doubleword load (speed) and any address (Forth's unaligned `,`, the Hayes corpus) | the pair access must be joined and must not | local quality - byte-aligned access in 2@ and 2! alone | **built**: results/applied-after-seed96/arm2at-after-seed96.patch (results/drafts/arm2at-706.md) |
| C4 | the re-measures: accuracy (rounds) against throughput (designs) | a session must be long and short | in time - the screen, then the shortlist (in use: chains A and B, 705); on condition - more rounds only where a decision is close (deferred open item 7's screen) | in use; item 7 stays deferred |
| C5 | the 16-bit families: a short call and a far reach | - | in space, in use (near and far forms) | off the fronts already (seed 96: cpt16 and sod16 deaths only past their reach) |

## C2 - mechanism 9, the JIT header, priced

Today (forth/cv8t-jit.4; engine/vm-lab.c's L_x_jit): every colon word compiled at run time begins [JIT op][4 bytes] - the
op triggers translation at the first call; the field holds the body's length (top bit set) until then, the native code's
offset (or 0: bytecode, its callers re-pointed past the header - jit_repoint) after. jitimg=1 gives up to 18 kernel words
the same header (tools/layout.py's JITIMG_OUTER; 84 of seed 96's 504 front designs). Three jobs: the trigger, the
length, the offset. The trigger cannot go without a check on every call (the interpreter's hottest path) or a native
form at every call site (5 bytes a call): it stays. The field's two jobs can each go elsewhere:

- **The length**, found instead: `;8` compiles an end-EXIT (an EXIT of its own one-byte tag-2 code - EXIT's handler,
  a code the translator reads as the body's end) and the translator decodes up to it, as it decodes the body anyway.
- **The offset**, kept elsewhere - two ways:
  - **V1, a side table** (separation in space, a supersystem's resource - beside the JIT's code): keyed by the word's
    offset from cbase, open addressing, 1,024 slots. Its code: 95-152 bytes (a prototype, results/drafts/jit-header-table-706.c, `cc -OPT -fno-pie -c` its text; this
    iteration: clang -Os 95, -O2 118; GCC -Os 107, -O2 152), 8 KB of bss - up to two pages touched, so memory +0-8 KB;
    one probe at each entry from bytecode.
  - **V1', the dead body** (separation in time - the same bytes are bytecode before the first call and the offset after):
    native code runs the whole word, so a translated word's bytecode is not run again - but for the resume point of
    (ABORT") (jit.c, 488: the interpreter resumes at the call when the flag is true). Rewritten at translation: the
    trigger to a second code (native, the offset follows), the body's first 4 bytes to the offset. Not rewritten (left
    bytecode, its callers re-pointed as today): a body under 4 bytes, or a resume point inside its first 4. No table, no
    memory, the same one 4-byte read on entry as today.
- **V3, an index** (a smaller field): [JIT][2-byte slot] and the offsets in an array - 2 bytes a definition saved.

| variant | the five programs' code | the held-out three's | image | engine | memory | entry from bytecode |
|---|---:|---:|---:|---:|---:|---|
| today | 875 (175 x 5) | 3,415 | +5 a jitimg word | - | - | one 4-byte read |
| V1 side table | -700 | -2,732 | -4 a jitimg word (<= -72); `;8`'s length loop out (an estimate by its tokens: -40 to -55) | +95 to +152, the end-EXIT's decoding besides | +0 to +8 KB | one probe |
| V1' dead body | -700 (less the few short or resuming bodies) | -2,732 (the same) | as V1 | the second code's handler (most of it today's native branch moved) and the end-EXIT's decoding: not priced | 0 | one 4-byte read |
| V3 index | -350 | -1,366 | -2 a jitimg word | the array's code, about 30 | the array | one load more |

On the pool's JIT designs (results/followup-seed96-roles.md): the smallest, d8f72aa60f, 32,661 B - V1 or V1' about
-600 B net, -1.8 %; the fastest, 923951e8ab, 54,755 B - about -1.1 %. Both past the size's 1 % - the JIT end of the front
would move. At 4-byte cells the header and the field are the same 5 bytes: the same saving. Not priced, to measure when
built: the entries from bytecode (the profiler's count of L_x_jit; native-to-native calls do not pass it), and the
end-EXIT's decoding in the engine. **V1' is the TRIZ answer** (separation in time, no new resource); V1 the safe one.
Building either is a gene's work across forth/cv8t-jit.4, engine/vm-lab.c and jit.c, tools/layout.py (the jitimg
words' header), forth/cross-cv8.4 and cv8-self-jit.h (the self-built images write the header) and the JIT checks
(jit-diff, engines-check) - after the roles (it changes every JIT design's bytes and chain A measures them now), and
only if the owner wants the search reopened for it.
