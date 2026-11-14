# Self-hosting the ten designs - the plan (Iteration 666)

**The owner's decision (666)**: every one of the ten designs (designs/, results/handoff-relf-657.md) self-hosting,
relf's way - a CV8 cross compiler written in Forth, run by the design itself, compiling the kernel and its compiler
straight into the design's CV8 image. relf made the same move in its Iteration 243: its cross.4 had emitted cells, and
every CV8 image was translated from the cell image by this lab's tools/layout.py after running it on relf.c; emitting
CV8 in cross.4 retired both (vendor/relf/tree/forth/cross.4, its header). New images, so every figure is measured
again; all ten designs, both cell widths. Chosen over an exact port of the translator, which would have kept today's
images byte for byte (the owner, 666).

## Today

How a winner's image is made (tools/build-stages.sh, lab/evolve/evolve.py's build()): RelF's cell engine
(engine/relf.c) boots the cell kernel (forth/kernel-seed.img - cross.4's own output, a fixed point), loads the
design's overlays, and prints an addressed dictionary dump (tools/dict-dump-addr.4); then tools/layout.py translates
the dump into CV8 with about twenty-five options. The winners use 782 of layout.py's 1,060 statements and 712 of the
939 in sod16.py's library part, which layout.py loads (traced at 666 on all twenty of their translator calls).

The run-time compiler: forth/cv8.4, cv8b.4 and the fusion overlays define `X8` words (`;8`, `IF8`, `COMPILE,8` -
26 names); the cell image keeps its own compiler, and the translator's --cv8-compiler puts each `X8` body in `X`, so
the CV8 image's compiler emits CV8. Load-time code in the overlays builds tables from the kernel's opcodes
(`' + >OP C,` in cv8.4's FOLD-OPS) and sets variables (cv8b.4's CV8-SHIFT-V).

What each winner already does on its own (665): it runs forth/cross.4 and writes the cell kernel byte for byte
equal to the seed - 10 of 10 at both widths.

Each design's overlays (the dump's name) and its translator-only options, besides the ones every design has (v8,
bytehdr, dataprims, fold and its set, cv8-compiler, set-compiler-vars, long branches):

| design | overlays | options |
|---|---|---|
| `fastest-x86-64` | bt-kfast-kinput-klookup-knumber-fuse-loopall-iplus-jit-fsys2 | escape, spec, ops10-file, rtfuse, tag2, tag2-rank, tag2-hot, tag2-wide, hot-inline, op-bodies, bss, thin-header, drop-x8, drop-dumptool, jit, jitx, jitloop, jitinl, jitmul, jitexec, jitimg, jitvar, rebind, headerless, threads |
| `fastest-x86-32` | bt-kfast-kinput-klookup-knumber-loopall-jit-fsys2 | escape, escape2, spec, no-varslot, supers-file, ops10-file, tag2, tag2-rank, tag2-hot, tag2-wide, hot-inline, op-bodies, bss, thin-header, drop-x8, drop-dumptool, op-inline, jit, jitx, jitloop, jitinl, jitmul, jitexec, jitimg, rebind, headerless, threads |
| `best-all-round` | bt-kfast-kinput-klookup-knumber-loopall-jit-fsys2 | escape, spec, supers-file, ops10-file, tag2, tag2-rank, tag2-hot, tag2-wide, hot-inline, op-bodies, bss, thin-header, drop-x8, drop-dumptool, op-inline, jit, jitx, jitloop, jitinl, jitmul, jitexec, rebind, headerless |
| `small-jit` | bt-kfast-kinput-klookup-loopall-jit-fsys2 | spec, no-varslot, ops10-file, tag2, tag2-rank, tag2-hot, hot-inline, op-bodies, bss, thin-header, drop-x8, drop-dumptool, op-inline, jit, jitx, jitloop, jitinl, jitmul, jitimg, rebind, headerless |
| `portable-fastest` | b-kfast-kinput-klookup-knumber-fuse-imm-loopall-iplus-fsys2 | escape, spec, supers-file, ops10-file, rtfuse, op-bodies, bss, thin-header, drop-x8, drop-dumptool, op-inline, rebind, headerless, threads |
| `portable-arm` | b-kfast-kinput-klookup-fuse-imm-loopall-iplus-fsys2 | escape, spec, no-varslot, supers-file, ops10-file, rtfuse, op-bodies, bss, thin-header, drop-x8, drop-dumptool, op-inline, rebind, headerless |
| `portable-knee` | b-kfast-kinput-klookup-fuse-imm-loopall-iplus-fsys2 | escape, spec, no-varslot, supers-file, ops10-file, rtfuse, op-bodies, bss, thin-header, drop-x8, drop-dumptool, op-inline, rebind, headerless |
| `portable-small` | b-kfast-kinput-klookup-fuse-loopall-iplus-fsys2 | no-varslot, supers-file, ops10-file, rtfuse, op-bodies, bss, thin-header, drop-x8, drop-dumptool, op-inline, rebind, headerless, threads |
| `least-memory` | b-kfast-kinput-klookup-fuse-loopall-iplus-fsys3 | ops10-file, rtfuse, hotcalls, op-bodies, bss, thin-header, drop-x8, drop-dumptool, rebind, headerless |
| `smallest` | b-kfast-fsys3 | supers-file, ops10-file, hotcalls, op-bodies, bss, thin-header, drop-x8, drop-dumptool, op-inline, rebind, headerless, threads |

## The target

For each design and each width: the design's engine running its own image, given `S" selfhost.4" INCLUDED`, writes
an image byte for byte equal to the one it runs - the fixed point - from source alone: forth/kernel.4 (unchanged: the
cell stages and the kernel workload keep it), the CV8 compiler's sources, the design's genes in a Forth file of its
own (designs/NAME/genes.4), and its engine's opcode map. That image passes the evolver's gate - the corpus (661
cases), the kernel workload, the far tests - and is the one designs/ ships. The engines stay as shipped
(designs/NAME/src): the cross compiler targets each engine's map, read from the tables the translator wrote there.

## The pieces

1. **forth/cross-cv8.4** - the CV8 cross compiler: cross.4's vocabularies, target space, definitions, forward
   references, defining and compiling words, with part 4 emitting CV8 - calls, literals, branches, DOES>, byte
   headers. relf's cross.4 is the template.
2. **The swap at compile time** - the target's `X` compiled as `X8`'s definition for the 26 names; the overlays'
   other words compiled after the kernel; their load-time tables and settings given cross-compile-time twins.
3. **The genes**, in the cross compiler's code generator and layout:
   - encoding: the fold set, specialisation (loc, var, tiny, small, imm), fused pairs, format-10 operations, escape
     bands, op-bodies, op-inline, hotcalls;
   - layout: byte and thin headers, headerless words and rebinding, dictionary threads, bss, drop-x8,
     drop-dumptool, long branches;
   - kernel variants: kfast, kinput, klookup, knumber; the file words (fsys2, fsys3); the run-time fusion
     overlays (fuse, fuse-imm, loopall, iplus);
   - the JIT designs: the tag-2 encoding and its ranking, hot-site inlining (lab/evolve/hotsites-v1.json), the
     image's JIT candidates and variables.

## The order - each phase leaves a working state

1. **s6-cv8b**, the ladder's last stage, no genes: the format, the swap, the bootstrap. The translator-built s6
   image runs cross-cv8.4 and writes image A; A, booted, writes B; A = B; A passes the gate.
2. **The six portable designs**: smallest, least-memory, portable-small, portable-knee, portable-arm,
   portable-fastest - each self-hosting when its genes are in.
3. **The four JIT designs**.
4. **4-byte cells** for all ten - cross-cv8.4 retargeted as cross.4 is (one width line).
5. **Shipping**: designs/ holds the self-built images; `make selfhost` in a design's directory checks the fixed
   point; tools/run-tests.sh runs it for all ten. The evolver keeps layout.py: its records describe the search as it
   was measured.
6. **Measured again**: sizes here; speed on the laptop, the i7 and the Tegra as the final check was run; the roles
   re-derived (one could change hands - the owner's call); designs/README.md, the relf handoff and the article's
   tables and text redone, with the self-hosting the article now lacks.

## The checks

- The fixed point for every design and width, from a fresh clone.
- The gate on every new image: corpus, kernel workload, far.
- A check that can fail (prompts/15): a planted change in the cross compiler or a genes file changes the image, and
  the fixed-point check says so.

## Risks

- **Speed and size move.** Some translator passes work on the whole image after the fact (hotcalls, op-bodies,
  hot-site inlining by a profile, the tag-2 ranking); a compiler meets the code once, in source order. Where the
  cross compiler's version differs from the translator's, the difference is measured and said.
- **Effort.** Several sessions. The phases are ordered so that each one ends in a working, checked state.

## Phase 1 notes - what the s6 engine and the cell cross compiler expect (666)

- **The file** (engine/vm-lab.c, load_image): an 8-byte magic - "RELF", an encoding and width byte, a format version,
  a feature bitmap (varcall, varslot, spec, lit64) the engine must implement - then the thread count and the thread
  heads (START-relative), the DOES> tail entries (a count, then word number and byte offset pairs), then the image:
  a prologue (two call tokens, filler, three cells) and the words, each a byte-granular link, a flags-and-length byte,
  the name, padding as body_needs_align() asks, and the body (tools/layout.py's emit()).
- **The engine never reads a dictionary link** (tools/build-stages.sh, s6): headers are the image code's own business -
  cv8b.4's HEADER8, NEXT-NFA8 and SEARCH-WORDLIST8 write and read them.
- **The opcodes** (forth/cv8.4): primitives in kernel.4's PRIMITIVE order; EXIT 1, LIT16 2, BRANCH 3, 0BRANCH 4,
  LIT32 68, DOVAR 69, DODOES 70, LIT8 71, LIT64 124; the fold band from 73 (23 operations); a call 0x80-0xBF in two
  bytes (14 bits) or 0xC0-0xFF in three (22), a byte offset from the image base at s6's SCALE 0. s6's kernel code also
  carries the five specialisations (tools/build-stages.sh: --spec loc,var,tiny,small,imm), which its run-time compiler
  does not emit.
- **The cell cross compiler** (forth/cross.4): CROSS-COMPILE searches TARGET then TRANSIENT; a target word, executed,
  compiles a call; a number is a literal when compiling and stays on the host stack otherwise. kernel.4 has no
  top-level code that runs in the target; the overlays have some - cv8.4's FOLD-OPS table (`' + >OP C,`), cv8b.4's
  settings (`0 CV8-SHIFT-V !`) - which the CV8 cross compiler gives twins at cross-compile time, as relf's kernel.4
  and cross.4 are written.

## Phase 1 progress (667)

forth/cross-cv8.4 - forth/cross.4's parts 1-2 (vocabularies, target space), then CV8: byte headers as cv8b.4's HEADER8,
calls in two or three bytes at scale 0, literals in cv8.4's narrowest forms, branches with 16-bit offsets from the
operand, a definition's last primitive folded into its EXIT (FOLDMAP from the fold set's names), data words
[DOVAR][3][aligned field]. What it took that the plan did not say:
- **The swap at compile time**: kernel.4's own definition of each of the 27 names is a BRANCH to its X8 - resolved at the
  end, its body skipped (SKIP-DEF) - a branch and not a call, because (;CODE) takes its caller's return address. A name
  kernel.4 does not define (AGAIN) keeps only its X8, as in the translator's s6.
- **The overlays' load-time code**: every target word has a shadow whose action outside a definition is the host word
  I-name if there is one (I-! stores into the image, I-' is T', I->OP reads a primitive's opcode, I-CREATE makes a data
  word), else a data word's address or a constant's value; anything else stops the build by name.
- **What the translator wrote that the kernel needs**: DICT-MAX, 256 MB (tools/layout.py's CVARS, Iteration 184) -
  without it an ALLOT past the dictionary crashed instead of being refused; the gate's full.fth found it.
- **The file**: the magic CV80, cell width, 'L', version 1, features 31 (engine/vm-lab.c's IMAGE_MAGIC); 32 thread heads;
  no DOES> tails; the five-cell locals block, zero; THROW's body; the image. The prologue: calls to COLD and WARM (3
  bytes each, forward), three cells of -1 at 16-39, the first word at 40.
- **Forward calls** are three bytes, chained through themselves; once the word exists a call is made at once.

The image: 9,792 bytes against the translator's 9,265 - no specialisation yet, the X8 headers kept, 3-byte calls before a
runtime word is defined. tools/selfhost-check.sh: the fixed point and the evolver's gate, with a planted-fault self-test.

## Phase 1 done (668)

s6's specialisations in the cross compiler's code generator, as patterns completed while compiling (tools/sod16.py's
specialise() and fold_exit(), engine/vm-lab.c's opcodes 0x60-0x7B): small (0, 1, -1 one byte), imm (LIT n + and
LIT n =, n in -128..127, to ADDI and EQI), var (a data word's call then @ or ! to VF or VS and a slot operand), tiny
(calls to fifteen words to their opcodes), and the folds - a fold-set primitive, ADDI, EQI or a literal below 64 KB
with the EXIT after it, at ; and at an EXIT inside a definition. A pattern is fused only where nothing branches into
it: a resolved branch and BEGIN end it. The X8 words whose X branches to them are made without headers (the
translator's --drop-x8); AGAIN8 keeps its name. loc is for locals, which s6's kernel has none of.

The image: 9,077 bytes, 188 fewer than the translator's 9,265; A = B; the gate passed. Best of five on this VM, the
translator's s6 against the self-built: fib 36 and 36 ms, loop 15 and 15, bubble 8 and 8, ackermann 6 and 6 - code
these workloads compile at run time, through the same run-time compiler; the kernel's own code is measured at phase 6.


## Phase 2 progress (669) - smallest self-hosting

**The genes.** lab/evolve/export-genes.py runs evolve.py's own build() for a design with every command recorded and
writes what the evolver handed the translator - tools/layout.py's options and the overlays of the dump it read - as
Forth words: designs/NAME/genes.4 (and stages/s6-genes.4 for s6). G-OVERLAYS, G-FOLDS, G-SPEC, G-SUPERS, G-OPS10,
G-HOTCALLS, G-OP-BODIES, G-OP-INLINE, G-BSS, G-THIN-HEADER, G-THREADS, G-REBIND, G-HEADERLESS, the engine's flags
(G-ENGINE-SPEC, G-FEATURES, G-MAGIC5) from its Makefile. Options not handled yet are written as comments ("\ not yet:
--escape", --rtfuse, ...); the four JIT designs' dumps are tag 2 and are skipped (phase 3). export-designs.py remakes
each designs/NAME/ from nothing and would take genes.4 with it: rerun export-genes.py after it (phase 5 joins them).

**forth/cross-cv8.4, genes-driven.** Run as `S" extend.4" INCLUDED S" genes.4" INCLUDED S" cross-cv8.4" INCLUDED`.
A definition is a list of operations until its ; and then the design's rewrites run over it in the translator's
order (tools/sod16.py's read_ops: specialise, the format-10 calls as opcodes, fold, pairs, test-branches, short
branches); dead operations are squeezed out after each rewrite, as the translator's lists have none (without that,
`1+` stayed ADDI 1 EXIT); short branches by relaxation (laid out, misfits long, again). Besides s6's: the design's
fold set (FOLD-BASE + place, and cv8.4's FOLD-OPS rewritten to it), pairs (resolved as their words appear),
format-10 operations (a kernel word's calls become its opcode, before a tiny word's, as opcode_L reads them),
fused test-branches and BRANCH8/?BRANCH8; --op-bodies ([op][EXIT]) and --op-inline (made at (PRIMITIVES-END) in
kernel.4's order, the kernel's own definition skipped - the words defined once, by a pre-scan of the sources);
--bss (TIB, POCKET, INCLUDE-BUFFER words pushing START + an offset past the image, the ALLOT after each counted
there); --threads (FORTH-WORDLIST allots the design's heads); --thin-header; --rebind (the kernel's primitives of
those names: their uses calls to the newest definition, resolved at the end); --headerless. The swap set is now
read from the overlays (every `: X8`); a call to an X8 goes to X, the latest code of the name, except from a later
X8 of its own name, which defers to the one before (drop-x8's rule). A definition no longer finds itself until its
; - file-sysc3.4's OPEN-FILE calls the one before it; inside a target definition every target word compiles,
immediate or not (cross.4's rule: kernel.4's `[']` calls LITERAL, its `;` calls `[`).

**Three passes** in one run, the state reset between them, a word known from pass to pass by its ordinal: pass 1
finds the dead words - defined again under their name, never called, POSTPONEd or taken by `'` (the translator's
dead shadowed words) - and whether the image ends below 16 KB (then a call laid down before its target exists is two
bytes, not three); pass 2 leaves the dead words out and counts the call sites; pass 3 gives the most-called targets
one-byte calls (--hotcalls: three free sites at least, ranked by free sites, all sites, then definition order) and is
the image. Passes 2 and 3 check that they found what the pass before found.

**smallest**: 8,739 bytes, 232 fewer than the translator's 8,971 - 17 dead words out (the translator's 16, the 17th
the first SEARCH-WORDLIST8, which drop-x8 took there), 32 one-byte calls; the same 300 named words. A = B on its own
engine (designs/smallest/forth, FSYS=3: the image's own file words read the sources and write the image); the gate
passed; `sh tools/selfhost-check.sh --self-test smallest`: the planted fault caught. Best of five on this VM,
translator's against self-built: fib 58 and 57 ms, loop 21 and 20, bubble 8 and 8, ackermann 3 and 4, parse 124 and
119, sieve 17 and 17. **s6** with stages/s6-genes.4: 9,069 bytes (8 fewer than phase 1's: the two-byte pending
calls), A = B, the gate passed.

**Next in phase 2**, each needing more of the translator: least-memory (format-10 loop words as branch kinds -
(DO) (LOOP) (+LOOP) (?DO) (LEAVE) I J, I+, --rtfuse's tables: FOLD-TABLE, SUPER-TABLE, IMM-OPS, LOOPTAB), then
portable-small (DUP+I, DUP<I, OVER?BRANCH, U<?BRANCH), portable-knee and portable-arm (SWAP+I, --escape), and
portable-fastest (=?BRANCH8, <>?BRANCH, DUP?BRANCH, (NUMBER?)).

## Phase 2 done (670) - the six portable designs self-hosting

What the other five needed, each a rule of the translator done while compiling:

- **The genes as short lines**: REFILL reads 256 characters a line, least-memory's format-10 list is 265. A list is now
  `G-LIST: NAME` and its text a line at a time (`S" ..." G+`); the check copies all of forth/*.4. A genes file names
  what the compiler has no rule for in G-NOT-YET (--escape2, --tag2, --hot-inline, --jit, --opcall-file,
  --guard-abort, =I?BRANCH, DUP?NBRANCH), and the compiler refuses it.
- **Format-10 words defined in an overlay** - (FIND) and (>NUMBER) in cv8b-klookup.4, THREAD-FIND in cv8b-kfast.4,
  (PARSE) in cv8b-kinput.4, (NUMBER?) in cv8b-knumber.4: each format-10 word has one definition, wherever it is, and
  its calls are its opcode (a second definition is refused); op-bodies and op-inline take them too. (DO) and the loop
  words as format-10 operations: a FORWARD that has an opcode compiles it; (LOOP) and its cell a branch with (LOOP)'s
  opcode (ops10_rewrite's LOOPKIND).
- **The run-time fuser's tables** (--rtfuse), as layout.py writes them: cv8-fuse.4's FOLD-TABLE (always) and
  SUPER-TABLE (I + as I+ first, the fused tests the compiler can make, the pairs), cv8-fuse-imm.4's IMM-OPS,
  cv8-fuse-loopall.4's LOOPTAB (the eight loop opcodes, I's offset, J's and UNLOOP's distances). cv8-fuse.4's
  FOLD-DEFAULTS runs at load time: a host action copies FOLD-OPS in the image. Checked against the translator's
  least-memory: the same table bytes (LOOPTAB's I offset aside - the layout differs; J and UNLOOP at the same
  distances).
- **keepbranch**: SWAP or DUP before an ADDI as SWAP+I and DUP+I, DUP n < as DUP<I.
- **--escape** (knee, arm, fastest): the rarely used primitives (tools/sod16.py's ESC_PRIMS_ALL, exported as
  G-ESC-PRIMS) are ESC (0x7D) and a selector in kernel.4's order, the others' opcodes closing up; an escaped primitive
  never folds. **--no-varslot**: slot operands two bytes, low first.
- **An overlay's IMMEDIATE word** met in one of its definitions is refused unless TRANSIENT has a twin: the overlays
  are written for a running Forth, where it would run. kernel.4 keeps cross.4's rule (every target word compiles).

| design | the translator's image | self-built | dead words out | one-byte calls |
|---|---|---|---|---|
| smallest | 8,971 | 8,739 | 17 | 32 |
| least-memory | 9,638 | 9,422 | 28 | 32 |
| portable-small | 9,183 | 8,975 | 24 | - |
| portable-knee | 9,049 | 8,841 | 26 | - |
| portable-arm | 9,202 | 8,970 | 26 | - |
| portable-fastest | 9,706 | 9,554 | 26 | - |
| s6 (the ladder) | 9,265 | 9,069 | - | - |

Bytes of the image file, header included, 8-byte cells. Each: A = B on the design's own engine and the evolver's gate
passed (`sh tools/selfhost-check.sh NAME`; --self-test on smallest and least-memory: the planted fault caught). Best
of five on this VM, translator's image against self-built, ms - least-memory fib 41/42, parse 47/45; portable-small
32/32, 25/25; portable-knee 27/26, 21/20; portable-arm 25/25, 22/22; portable-fastest 24/22, 21/19; loop, bubble,
ackermann and sieve within a millisecond (build/selfhost/speed.sh; the laptop, the i7 and the Tegra at phase 6).

**Next**: phase 3, the four JIT designs (tag 2's ranked codes, hot-inline, the JIT's options, --escape2,
--no-varslot) - the largest step; or phase 4 first for the six (4-byte cells: TARGET-CELL-BYTES, the designs'
forth32 and image32.img), the smaller one.

## Phase 4 done (671) - the six at 4-byte cells too

**The width is a gene**: G-CELL (8 or 4) sets the cross compiler's TARGET-CELL-BYTES. lab/evolve/export-genes.py
writes designs/NAME/genes32.4 from the 4-byte build (evolve.py's build() at_width(WIDTH4), as export-designs.py makes
image32.img; the same options and tables as the 8-byte build, the k32 dump). A literal is the target's value
whichever host compiles it (T-NORM: on a wider host, the low bytes sign-extended, as @-T reads a cell).
`sh tools/selfhost-check.sh [--self-test] --32 NAME` runs the design's forth32 on image32.img with genes32.4; the
gate is eval32's, against the evolver's 4-byte references (setup_widths, at_width(WIDTH4)); and the design's 64-bit
build must make the same 32-bit image - it does, for all six: the host's width does not reach the image.

**No more branches to the X8s.** At 4-byte cells the translator's images have less padding (its data words' bodies
are aligned before DOVAR, four bytes at 8-byte cells), and four of the six came out 16-68 bytes larger: the cost was
the swap's 3-byte branches (27 of them in least-memory). Now kernel.4's X waits - no header and no code, its calls
chained like a FORWARD's and its POSTPONEd cells chained through themselves (only (;CODE), in DOES> and DOES>8) - and
at the last X8 of its name (the pre-scan counts them) X's header is laid down, the X8's code is X's, and what waited
on X is made. X's header sits a little later in the dictionary than kernel.4's place for it; X is defined once.
A `'` or `[']` of a word still waiting is refused (the sources have none).

| design | translator, 8-byte | self-built | translator, 4-byte | self-built |
|---|---|---|---|---|
| smallest | 8,971 | 8,675 | 8,167 | 8,087 |
| least-memory | 9,638 | 9,358 | 8,782 | 8,746 |
| portable-small | 9,183 | 8,887 | 8,451 | 8,375 |
| portable-knee | 9,049 | 8,753 | 8,177 | 8,125 |
| portable-arm | 9,202 | 8,898 | 8,350 | 8,286 |
| portable-fastest | 9,706 | 9,482 | 8,474 | 8,458 |
| s6 (the ladder) | 9,265 | 8,983 | - | - |

Bytes of the image file. Each: A = B on the design's own engine (forth, forth32), the gate passed; at 4-byte cells
the 64-bit build makes the same image.
Speed at 4-byte cells on this VM (forth32, translator's image against self-built, best of five): within noise - the
four widest gaps, timed again best of fifteen with the images alternating, were smallest loop 24/23 ms, least-memory
fib 46/42, portable-fastest fib 24/25, portable-knee parse 624/578. --self-test --32 portable-fastest: the planted
fault caught.

**Next**: phase 3, the four JIT designs (tag 2's ranked codes, hot-inline, the JIT's options, --escape2); then phase 5
(designs/ ships the self-built images, `make selfhost`, run-tests runs the checks) and phase 6 (re-measured).
