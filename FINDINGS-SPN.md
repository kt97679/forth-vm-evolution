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
