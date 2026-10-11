# Other Forths: ideas to borrow (Iteration 196)

The owner: search GitHub for other Forth implementations and borrow ideas. Each
read for one question - what does it do that our genes do not? Checked against
our engine and converter (engine/vm-lab.c, tools/sod16.py, tools/layout.py).

## Already ours, in some form

Superinstructions (pairs, folds) and opcodes for words (ops10, opbody); TOS in a
register (tos); tail calls (tail); X;CALL (opcall); inlining at hot sites
(hotinl); copy-and-patch JIT stencils (jit, jitx, jitloop, jitinl); headers
thinned (thinhdr, bytehdr, headerless words); literals and calls sized by value
(LIT8/16/32, 2- and 4-byte calls); GCC's interpreter-hostile optimisations off
(nogcse, nocrossjump, noreorder) and alignment (alignfn); literal-into-operation
at run time (rtimm). Retro's Nga (four opcodes packed per cell, literal values
after the bundle) and zForth (variable-length cells, 30-50% smaller dictionary)
are what our byte codes and sized operands already do.

## New genes, ranked by value over cost

1. **Pinned VM registers** - Gforth's build tuning: the interpreter's
   instruction pointer, stack pointers and top of stack in chosen machine
   registers (GCC explicit register variables), the best assignment kept. Ours
   pins none (no register asm in vm-lab.c) and leaves a 10.7 KB interpreter
   function to GCC's allocator. A gene: regpin 0..3 - none, and three
   assignments over rbx, r12-r15. Cost: small (a few #if lines); the laptop's
   GCC decides.
2. **Primitives demoted to Forth** - sectorforth: eight primitives, five
   variables and two I/O words; branching, compiling and the return stack in
   Forth (milliForth: 336 bytes). At our small end the engine is ~60% of the
   size, and in a tag-2 JIT design the interpreter function alone is 10,658 of
   the stripped binary's 21,104 bytes. A gene: a set of rarely executed
   primitives built as colon definitions in the image instead of handlers in
   the engine (no gene moves this way today: kfast, kinput, klookup and opbody
   all move work into native code). Each needs a reference Forth definition;
   the gate proves them. Cost: medium; the largest size lever left.
3. **Packed names** - colorForth: characters in three classes of 4, 5 and 7
   bits, a name packed into 28 bits of a cell, lookup a cell compare. Headers
   smaller, and FIND - hot in corpus, parse and kernel - a word compare instead
   of a string compare. WORDS, NAME>STRING and the rest decode. The owner's
   "packed names later" (Iteration 103). Cost: medium-large.
4. **Folding at run time** - Mecrisp: any word replaced by simpler code when
   its inputs are constants, inlining first so folding crosses words. Ours
   folds a literal into the next operation (rtimm); next: two literals and a
   pure operation to one literal (10 CELLS, BL 1+, 2 4 +), a literal and a
   comparison to an immediate test. Cost: small, on rtimm's machinery.
5. **Single-use words inlined in the image** - Mecrisp-Across: automatic
   inlining of definitions used once, with dead code removed. The converter
   knows every call site; an internal word called once (the --headerless kind)
   inlined and its body dropped saves a call, an EXIT and a header. Cost:
   medium; only words nothing finds by name.
6. **The superinstruction choice** - Gforth: --ss-greedy against optimal
   selection, cost by code size, loads/stores or dispatches. Ours is greedy,
   left to right (tools/sod16.py: a pair fused wherever it starts); where pairs
   overlap and one is escaped, choosing by bytes saves. A gene: greedy or
   shortest-path, by bytes or by dispatches. Cost: small-medium; gain modest.
7. **Stack caching for the hottest only** - Gforth's peeprules give the
   multi-state (two-register) versions to the primitives that run most (;s,
   lit, call, @, ?branch, ...). The cheap form of "two stack registers"
   (results/gp-deep-dive.md): the top-N handlers in a TOS+NOS variant. And in
   the JIT, Mecrisp's RA kernel keeps the top five stack items in registers.
   Cost: large.
8. **Tail-call threading** - Tails (a Forth core with musttail, after Wasm3's
   interpreter), CPython 3.14, PHP's TAILCALL VM (Clang 19+ as fast as GCC's
   computed goto): each handler a function, the compiler allocating per
   handler. Needs musttail and preserve_none - Clang 19+ (GCC has musttail
   only). Cost: large; first: which compilers the laptop has.

## Not borrowed

Instruction bundles (Nga) - byte codes already one byte an op; the JIT through
libfirm or LLVM - a dependency heavier than the engine; WAForth's per-word Wasm
modules - another target.

## References

- sectorforth - github.com/cesarblum/sectorforth; milliForth - github.com/fuzzballcat/milliForth
- RETRO / Nga - forthworks.com/retro (Handbook; image/retro.muri)
- zForth - github.com/zevv/zForth
- Gforth engine options - complang.tuwien.ac.at/forth/gforth/Docs-html/Invoking-Gforth.html; peeprules.vmg - github.com/earl/gforth-mirror; Ertl, A Look at Gforth Performance, EuroForth 2009
- Mecrisp, Mecrisp-Stellaris RA kernel, Mecrisp-Across - mecrisp.sourceforge.net; mecrisp-stellaris-folkdoc.sourceforge.io
- Lars Brinkhoff's inlining, folding, register-allocating compiler - github.com/larsbrinkhoff/forth-compiler
- Tails - github.com/snej/tails; Wasm3's interpreter design - github.com/wasm3/wasm3/blob/main/docs/Interpreter.md
- CPython's tail-calling interpreter - github.com/python/cpython/issues/128563; PHP's TAILCALL VM
- colorForth's packed names - the colorForth mailing list (strangegizmo.com/forth/colorforth)
