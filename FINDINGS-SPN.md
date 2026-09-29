# SPN: Stencil-Patched Native - proof of concept

The question: can a Forth keep compact code and a minimal VM and still
run within about 2x of C? The research answer was that no interpreter
does - the fastest known ones sit near 10x of native - but that
copy-and-patch baseline compilation reaches roughly that range for
WebAssembly. This is a working test of the idea on this system.

## Design

A STENCIL is one Forth operation written as an ordinary C function in
`engine/spn-stencils.c`. They are compiled into the engine by the same C
compiler that builds it, and never called. Forth reads their machine
code out of the running engine, copies it into executable memory back
to back, and patches the holes.

The data stack travels as the function arguments `(sp, tos)`, so under
the calling convention the top of stack stays in a register from one
stencil to the next. No register allocator exists anywhere.

Holes are found exactly, not guessed. A stencil marks one by referring
to a marker function (`engine/spn-markers.c`, kept in a separate file so
the compiler cannot see - and optimise around - their bodies), and Forth
recognises a hole as a 32-bit relative field that points precisely at
that marker's address. Literals are 8- or 4-byte immediates found by
value. A stencil without the expected shape is simply not used.

**External tooling: none beyond the C compiler already needed.** No
object-file parsing, no clang, no separate build step.

What is in C (`engine/spn.c`): the cell engine unchanged, plus three
primitives numbered past the kernel's 68 - the stencil table,
executable memory, and a call into native code. The kernel and its seed
are untouched; the ordinary cell image runs on this engine as-is, and
Forth reaches the new primitives by compiling their raw tokens.

What is in Forth (`forth/spn.4`, about 250 lines): reading and
verifying the stencils, copying and patching them, and the translator
itself - including two small peephole rules, `LIT n +` to one add and
`DUP n < IF` to one compare-and-branch.

## Results

x86-64, the development VM, best of 7-9 interleaved runs, startup and
translation subtracted.

    10 x fib(30)                      ms    vs C -O2    vs same-algorithm C
    cell interpreter, same engine   342.0    23.9x        8.1x
    SPN native                       57.8     4.0x        1.37x
    C -O0                            65.3     4.6x        1.55x
    C -O2, plain recursion           42.2     3.0x        1.00x
    C -O2, as GCC compiles it        14.3     1.0x        0.34x

    SUMTO, 50 million iterations      ms    vs C -O2
    cell interpreter, same engine   784.5    49.8x
    SPN native                       82.6     5.2x
    C -O0                           124.1     7.9x
    C -O2                            15.8     1.0x

Both are correct against the interpreter, and a native call leaves the
rest of the data stack intact.

## Reading them honestly

**Against C doing the same work, fib is already inside 2x: 1.37x.** The
4.0x against GCC's fib is real, but it is not code quality: at -O2 GCC
inlines the recursion into itself and turns calls into loops, with a
184-byte frame. No baseline compiler does that, and the Forth performs
all 2.7 million calls. `bench/spn/fib.c` built with
`-fno-inline -fno-optimize-sibling-calls` is the same algorithm.

**The loop is 5.2x, and the cause is visible.** C keeps both loop
variables in registers: two adds and a branch, about one cycle per
iteration. SPN caches only the top of stack, so SWAP and OVER go through
memory and the loop-carried value makes a store-then-load round trip
every iteration - 1.65 ns against 0.32.

In both, SPN beats C -O0, as the copy-and-patch literature predicts.

## The next step

Stack caching with more than one register, as states the translator
tracks: top-of-stack only, top two, and so on, with a stencil variant
per state and spills only where a branch or call needs a canonical
state. That is Ertl's static stack caching, and within this design it
is exactly "register allocation as table lookup". SUMTO's loop never
holds more than three items, so with three cached registers it would
run entirely in registers. That is the change most likely to take the
loop from 5x toward 2x.

After that: calls. Each native call currently pays the C ABI - stack
alignment and moving the returned pair back into the argument
registers - about eight instructions where C pays about three.

## As a whole system: s7-spn

The proof of concept translated two benchmarks by hand. s7-spn is a
complete Forth: the kernel image plus the translator (forth/spn-full.4),
saved with SPN-BOOT as its boot word. Every start translates the
dictionary, then falls through to the ordinary interpreter; new
definitions are translated as their ; completes.

**It passes the same 616-case ANS CORE corpus as the other ten systems**,
through the same harness, with the deliberately wrong control case
detected. In the kernel-compile benchmark it reproduces the reference
image byte for byte, or it would have been excluded from timing.

Mixed mode: a translated word's body becomes [SPN-ENTER][native
address], so interpreted callers run native code transparently. Native
code reaches an untranslated word through a re-entry helper that runs
the interpreter until a sentinel return address hands control back.
Both share one return stack. A word is validated completely - calls,
branches, return-stack depth - before anything is emitted, and left
untouched if any check fails.

At boot: 167 words native, 43 refused, the rest inlined as data.
The 43 are mostly words that read their CALLER'S return address - DOVAR,
the loop runtimes - which by design stay interpreted, and words
containing DO loops. SPN-WHY reports the reason for any word.

### Results

One layout build per stage on the development VM, best of 5 rounds.
Indicative: the project has measured 5-10% per-build bias.

    net of start-up (as the harness reports)
                     cell   CV8+spec  CV8+hdr   SPN
    kernel compile  1.000    0.535     0.577    0.308
    fib             1.000    0.829     0.776    0.164
    corpus          1.000    0.511     0.588    0.400
    parse           1.000    0.482     0.576    0.373

**The harness subtracts each binary's start-up, and SPN's start-up is
translating the whole dictionary**: 4.9 ms of CPU against 0.84 for the
other stages. Included, the answer changes for short workloads:

    end to end, start-up included
                     cell   CV8+spec    SPN
    kernel compile  1.000    0.556     0.568
    fib             1.000    0.833     0.293
    corpus          1.000    0.540     0.726
    parse           1.000    0.488     0.439

SPN wins clearly on anything that runs long enough to repay 4 ms; ties
on the 10 ms kernel compile; loses on the 14 ms corpus.

### What moved it

Start-up was 17.3 ms at first. Most of it was the byte-at-a-time FILL
again - clearing 8 KB of tables per word when a word uses a few dozen
cells. Clearing only what the last word dirtied took it to 4.1 ms.

Kernel compile went from 0.523 to 0.308 once the outer interpreter
itself - INTERPRET and REFILL - became native. They had been refused
for calling (ABORT"), which finds its message through its return
address; (S"), (.") and (ABORT") are now compiled natively, their
strings being constants by translation time.

### Bugs found on the way

In SPN: a primitive's own entry [prim][EXIT] was inlined as the bare
primitive, which is wrong for EXECUTE (>R ;) - the EXIT is the jump.
Latent until INTERPRET, which calls EXECUTE, became translatable.
Patching CELL+ while using CELL+ to do the patching. A data-word test
that scanned a variable's body as code and walked into its data.

In the kernel, and on the published branch too: every image written by
SAVE-SYSTEM crashed on boot, because the hashed word list's 32 thread
heads were saved as absolute addresses; and ?DO and LEAVE compiled
absolute leave addresses, the one exception to RelF's relative
branches. Both fixed, with tests that fail on the old code.

### After native loops, native PICK, and translating the translator first

    net of start-up                          end to end
                     cell  CV8+spec   SPN     cell  CV8+spec   SPN
    kernel compile  1.000   0.519   0.300    1.000   0.537   0.489
    fib             1.000   0.826   0.158    1.000   0.830   0.254
    corpus          1.000   0.503   0.386    1.000   0.528   0.626
    parse           1.000   0.475   0.360    1.000   0.480   0.409

193 words native, 32 refused. Start-up 4.4 ms against 0.84. End to end
SPN now wins kernel compile as well as fib and parse; it still loses the
14 ms corpus, by less than before (0.626 against 0.726).

How start-up was reduced, each step measured by counting interpreted
cells at boot - deterministic, unlike timing on this machine:

    first version                              17.3 ms
    stop clearing tables no word used           4.1 ms
    (more words translatable: loops, strings)   5.7 ms
    tables zeroed by cells, not bytes           5.0 ms
    translator translated first, depth first    4.4 ms   2.61M -> 1.46M cells

One ordering was measured WORSE and reverted: seeding the walk with
VALIDATE first left CMOVE interpreted while VALIDATE's subtree was
emitted, byte by byte (1.81M cells). The seeds are now the words every
translation needs, in the order it needs them: CMOVE, EMIT-ST,
VALIDATE, TRANSLATE-ALL.

What remains interpreted is mostly that seeding phase: the first few
dozen words are translated by a translator that is not yet native, and
the tree walk validates each twice. Stencil reading is 12%.

### Recipes: translation decided when the image is built

Everything the translator decides depends only on the dictionary -
which words translate, which stencil each cell becomes, what each hole
is filled with. So the build now runs the boot translation once with a
recorder attached, writes those decisions into the image as a compact
RECIPE per word, and undoes every patch, so the saved dictionary is
exactly as it was. Boot reads the stencils from the running engine as
before - their bytes and hole offsets belong to the machine and are
never stored - and replays the recipes. A signature of every stencil's
hole kinds guards the replay: on an engine whose stencils differ, boot
falls back to full translation.

tools/mk-spn-image.sh builds both variants from the same source:
s7-spn with recipes, s7-full without. Checked, not assumed: they make
the same 208 words native and emit byte-identical native code, 70,279
bytes, and both pass all 616 cases.

    image                       bytes     start-up (CPU, best of 45)
    s7-full, no recipes        88,880        4.87 ms
    s7-spn, recipes            99,169        2.44 ms
    CV8+spec, for reference    13,488        0.70 ms

**Cost: 10,289 bytes, all of it recipe data** - the image difference is
exactly the recipe length, since the recorder and replayer are in both.
That is 12% of the SPN image, and 15% of the native code it describes.
**Gain: start-up halved**, 4.87 ms to 2.44.

End to end, start-up included (net figures identical for both):

                     cell  CV8+spec  SPN full  SPN recipes
    kernel compile  1.000   0.518     0.510     0.397
    fib             1.000   0.799     0.262     0.207
    corpus          1.000   0.515     0.651     0.506
    parse           1.000   0.499     0.425     0.394

With recipes SPN wins kernel compile, fib and parse end to end, and the
corpus - which it lost clearly before - is now level: 0.506 against
0.515 is under 2%, inside this project's measured per-build noise.

Three things found on the way, each measured before fixing:

- The first recipe replay was barely faster (3.8 ms), because 1.6M
  cells still ran interpreted. The replayer's own words were recorded
  last. The cause was a 64-cell limit in the return-address scan: any
  longer word counted as unsafe to call, and REPLAY-WORD is longer, so
  the boot-time tree walk failed at its root. Raised to MAX-CELLS.
  Interpreted cells in replay: 1.62M -> 0.72M.
- A flags byte per op said which fields follow; the stencil's hole
  kinds already say that, and the signature guarantees they match.
  Dropping it: 14,799 -> 10,289 bytes.
- What remains of the 2.44 ms is mostly reading the stencils (27% of
  the interpreted work), which must happen before anything can be
  emitted, and the first few words replayed before the replayer is
  itself native.

### Next

The next real step for start-up is a design change rather than a tune:
validation depends only on the dictionary, so its results could be
computed when the image is built and saved in it, leaving boot only the
emission. That trades image size for start-up, and is worth deciding
deliberately.

Start-up is now the limit on short workloads. Translating on first
call rather than all at boot would pay only for words actually used.
And native DO loops would take most of the remaining 43 refusals.

## Memory, against CV8

All 8-byte cells, measured on this branch (terminal buffer at 256, so
every image is 176 bytes larger than the article's figures).

    engine code (text)            CV8 engine 19,664    SPN engine 14,707
    image on disk                 CV8+hdr    9,873     cell       24,496
    translator in the dictionary     -                 35,200

    one word, header and body     cell   CV8+spec  CV8+hdr   native
    FIB                            200      49        39       138
    SUMTO                          160      44        29       163

**The SPN engine is smaller than the CV8 one** - the plain cell engine
plus about 2 KB of stencils, against CV8's variable-length decoder,
folding and specialised opcodes. The complexity moved into Forth.

**The image is 2.5x larger only because this PoC translates from the
cell format.** Nothing in the design requires that; translating from
CV8 would keep the 9.9 KB image.

**Native code is the real cost: 3.5 to 5.6 times the CV8 form of the
same word.** And the PoC keeps the source form too, so a translated
word costs both.

**The translator is 35 KB, but 24.8 KB of that is two tables sized far
beyond need** - 16 KB of source map and 8 KB of branch fix-ups, where
FIB needs about twenty entries of each. The translator's own code is
about 10 KB in cell form; in CV8 form that would be roughly 3 KB, an
estimate from the usual cell-to-CV8 ratio rather than a measurement.
*Measured since, on s8 below: 12.6 KB with its saver. The estimate
ignored the headers - a CV8 translator of about 200 definitions carries
their names - and the CV8 translator is a bigger program, since it must
decode CV8 and bound every decode.*

Peak resident memory is useless for this comparison here: a C program
that does nothing measures 11,260 KB in this sandbox, and every Forth
configuration lands within 200 KB of that. The differences that matter
are tens of kilobytes and have to be counted inside Forth.

So SPN done properly would cost, over CV8: a few KB of translator, a
KB or two of tables, and native code only for the words actually
translated - which argues for translating hot words on demand rather
than everything.

## Limits of this version

- x86-64 only. 32-bit ARM needs `-mslow-flash-data` so constants are
  built with movw/movt instead of literal pools, and a different hole
  rule in the ARCH section of spn.4. Not yet tried on the Tegra.
- Translates only words made of the implemented primitives and calls
  to themselves. Calls to other words, inlining, and falling back to
  the interpreter mid-word are not done.
- The two peephole rules do not check that nothing branches into the
  middle of the sequence they fuse; correct for these benchmarks, not
  in general.
- No data-stack bounds checks in native code.
- Two benchmarks, one machine.

## On a CV8 image: s8-spncv8

The step "Memory, against CV8" argued for: translate from CV8, so the
image stays compact and only native code is expanded. Built in stages,
each committed; `tools/mk-spn-cv8-image.sh` makes two variants, as for
s7 - s8-spncv8 with recipes and s8-full without.

**Engine.** `engine/spn-cv8.c` is the CV8 engine plus SPN, put through
`gen-tos.py` and compiled exactly as s6 is. Its top-of-stack register
convention is SPN's native one, so entering native code converts
nothing. CV8 leaves only two opcodes free - 126 and 127, which indexed
past the end of the dispatch table until now - so 126 is SPN-ENTER and
127 a service opcode with a selector byte. A translated word's entry
becomes three bytes: SPN-ENTER and the native code's offset in 16-byte
units.

**Translator.** `forth/spn-cv8.4` decodes CV8 itself, with operand
sizes taken from the engine's handlers; the decoder was checked on the
whole dictionary before anything relied on it. Words shorter than a
patch cannot be patched, so short straight-line callees - constants
among them - are copied into native callers instead. Every decode is
held inside the word's own body. Working tables are allocated at boot,
not kept in the image.

### Results

One build per stage, x86-64, CPU time.

    image (bytes)   s6-cv8b 9,881   s8-full 22,514   s8-spncv8 35,369
                    s0-cell 24,560  s7-full 88,880   s7-spn    99,169
    start-up        s6-cv8b 0.72    s8-full 7.80     s8-spncv8 2.44 ms
                    s0-cell 0.73    s7-full 4.98     s7-spn    2.53 ms

End to end - nothing subtracted, minimum of 15 rounds interleaved across
all seven systems, ratio to s0-cell:

    workload  s5-cv8spec s6-cv8b s7-spn s7-full s8-spncv8 s8-full
    kernel    0.531      0.588   0.416  0.527   0.373     0.625
    fib       0.824      0.781   0.214  0.268   0.210     0.357
    corpus    0.514      0.595   0.511  0.654   0.446     0.765
    parse     0.490      0.590   0.404  0.436   0.311     0.380

**With recipes, s8 is the fastest system on all four workloads, start-up
included, from an image 2.8 times smaller than s7-spn's** (fib is a tie
with s7-spn). Without recipes it translates everything at every boot,
7 ms, and loses the short workloads to plain CV8. Recipes cost 12.9 KB
here - a third of the image, against a tenth of s7's - and replay makes
the same 226 words native that full translation does.

**Why end to end, and not the harness's net-of-start-up tables.**
`bench/lib.sh` subtracts the *mean* of five start-up runs from the
*minimum* of the workload runs; the minimum run also had a lucky
start-up, so the subtraction over-corrects, the more so the longer and
noisier the start-up - favouring exactly the systems that translate at
boot. It showed as s8-full beating s8-spncv8 by 20-26% net on corpus
and parse, with the same native code on the same engine. Taking the
minimum of both instead, the two variants agree within 2%.

### What makes it faster than s7

Same measurement, ms:

                     s7-spn   s8-spncv8   s8 without inlining
    kernel           9.06     8.18        9.62
    fib              9.54     9.40       10.78
    corpus           8.75     7.71        8.29
    parse           33.11    25.37       25.76

Inlining short words accounts for kernel compile and fib - without it
s8 falls behind s7 on both - and about half of corpus. It does not
account for parse. Part of that is the engine words run on when they
stay interpreted: FIND is refused by both translators, and a failed
FIND costs 389 ns on s7 and 332 ns on s8 (815 and 1,639 fully
interpreted on CV8 and on cells) - roughly a third of s8's lead on
parse at its token count. The rest is not attributed.

### Memory

    native code at boot     s8 91,770 bytes, 226 words   s7 70,279, 208
    translator and saver    12,633 bytes in CV8 form

About 20% more native code per word than s7: inlining copies callee
code into callers, and every word starts on a 16-byte boundary.

### Bugs found on the way

- **Opcode band.** SPN first went into opcodes 36-67, described in the
  source as freed. The remapping that freed them is off in the real
  build, so opcode 36 was RP!. Computed from the compiled table instead.
- **Entry after padding.** CV8 pads some bodies with leading NOOPs and
  compiled calls enter at the first real operation - HEADER's xt is
  4135, `:` calls 4136. Patching at the xt put SPN-ENTER's address
  bytes where every call landed; EXECUTE enters at the xt, which is why
  direct tests passed.
- **A signed index.** PM@ compared signed, and a literal's value
  reached it as a primitive number: -2147483647 read gigabytes off the
  table.
- **Clobbered decoder state.** Classifying a callee decodes it,
  overwriting the caller's decoded operation.
- **A word patched while patching itself** - OP-ENTER, the CELL+ bug of
  s7 in a new form.
- **The intermittent crash** was deterministic: LIT's entry
  `[LIT][EXIT]` decoded with LIT's two operand bytes ran into BRANCH's
  header, validated, and the patch overwrote BRANCH's link. Every boot
  did it; a crash needed a failed FIND to walk that thread off the
  image into unmapped memory - about one run in five. Found with a
  fault report now built into the engine: native offset, code bytes,
  registers, both return stacks.

### Limits and loose ends

- x86-64 only, and one build per stage: indicative, not a layout study.
- `forth/cv8-save.4` cannot save today's CV8 systems: it writes the
  header layout from before the word list was hashed again, and its
  scrub needs the shell. Nothing tests CV8 saving. s8 has its own saver.
- s8-full's start-up rose from 7.04 to 7.80 ms when the translator
  gained the recipe machinery - more words to translate at boot.

