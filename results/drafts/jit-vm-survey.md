# JITs and VM speed elsewhere - what to borrow (Iteration 217)

The owner (2026-10-12, seed 44 running): look at JIT implementations on
GitHub and for other ways to make virtual machines faster; borrow ideas.
This is a survey, not a decision: every item below names how it would be
priced first (prompts/10) and what it would cost against the aim (GOALS.md:
the smallest mechanism that pays, behind a gene, measured).

## What this project has already, so nothing here re-proposes it

Threading forms, the CV8/tag-2 byte code, superinstructions from each
design's own profile, folds and specialisations, format-10 words, a cached
top of stack (`tos`) and multi-state caching (`msc`, which bought less on
Zen 4), tail-call dispatch (`tail`, measured no in Iteration 89), pinned VM
registers (`regpin`), compiler-flag genes (`nocrossjump` among them), hot
call sites inlined in the image (`hotinl`), and a lazy copy-and-patch JIT
for words compiled at run time (JIT.md: SPN's C stencils, the stack as
`(sp, tos)` across stencils, all or nothing per word; `jitx`, `jitloop`,
`jitinl`). Priced and waiting: a register machine (results/price-register-
machine.md: 38-50% of the front's dispatches are moves or lone literals;
stage 1 19-24%), native code calling byte code (GENES.md candidate 5: 10%
of the kernel workload's dispatches, 80% of the sieve's), the interpreter's
handlers as the JIT's stencils (candidate 11), instruction replication
(open item 7). Rejected: GOALS.md's register.

## What was found

**RPyForth (Izawa and Hakamada, arXiv 2609.23759, September 2026;
github.com/3tty0n/rpyforth).** A Forth interpreter in RPython, so PyPy's
meta-tracing JIT compiles it. The data stack is split into a fixed window
of named locations - two scalar fields and eight frame slots - over one
shared spill array for everything deeper, with no stack-effect analysis and
no private call frames. The finding that matters here: with layout and call
policy fixed, letting the compiler name the window's cells (instead of only
caching them) gave 1.44-1.45x on 18 Shootout kernels and about 1.60x on six
Appbench applications; the window's shape and whether calls normalise it
moved results per program but not on the whole. As a system it beat
gforth-fast and SwiftForth on both suites and VFX Forth on the kernels
(1.90-2.36x), but lost to VFX on the applications (0.68-0.76x) - the deeper
stacks and far more frequent calls. Its front end also splices colon
bodies of up to 32 instructions and turns final calls into jumps.
*Lesson: the stack cells must be values the code generator can name, across
a whole region of code; that is where the time goes once dispatch is gone.*

**CPython's copy-and-patch JIT (python/cpython; issues 135379, 115802,
139038).** The 3.15 JIT added top-of-stack caching the copy-and-patch way:
several stencils per operation, one for each number of stack values held in
registers on entry and exit (`LOAD_FAST_0_1`, `BINARY_OP_ADD_INT_2_1`...),
the translator choosing the variant that matches the state - Ertl's 1995
stack caching, with no dispatch tables because nothing is dispatched. Its
first numbers were small on average (+0.5% on pyperformance, Python's
operations being heavy) but +16% on the numeric nbody. They also split
stencils into hot and cold parts, and tail-call between stencils with
`preserve_none` (more argument registers, none callee-saved) so more values
can stay in registers. *Lesson: the cached-top state machine is cheap in a
JIT - the cost of `msc` in the interpreter (a dispatch table per state) does
not exist there - and Forth's operations are far lighter than Python's, so
the share of stack traffic is larger.*

**Copy-and-patch itself (Xu and Kjolstad, OOPSLA 2021, arXiv 2011.13127).**
The stencil library holds many variants per operation - by operand type and
by where values live - and passes values from stencil to stencil in
registers ("pass-through" parameters: a stencil hands on registers it does
not use untouched). Their WebAssembly compiler: 1,666 stencils, 35 KB;
code 39-63% faster than V8 Liftoff's, compiled 4.9-6.5x faster.
*Lesson: the register state lives in the choice of variant; a small set of
states covers most code.*

**Single-pass compilers with an abstract stack (V8 Liftoff, Wizard's SPC,
SpiderMonkey's baseline; Titzer, "Whose baseline compiler is it anyway?",
CGO 2024, arXiv 2305.13241).** One pass over stack byte code, keeping a
virtual stack whose entries are a register, a constant or a memory slot:
a constant pushed costs no code until something uses it (Liftoff records
small constants and emits nothing), stack shuffles are bookkeeping, and the
state is made canonical only at control-flow joins and calls. Comparing six
such compilers: letting one register hold several slots, and tracking
constants, both measurably improve the code; constant and branch folding
added little. *Lesson: the same as above, with constants as a state too.*

**Deegen and LuaJIT Remake (Xu and Kjolstad, OOPSLA 2026, arXiv 2411.11469;
github.com/luajit-remake/luajit-remake).** One semantic description of each
byte code, in C++, generates both the interpreter and a copy-and-patch
baseline JIT, with hot/cold splitting, inline caches and tier-up (OSR
entry). The interpreter beat LuaJIT's hand-written one by 31% on 44
benchmarks; the baseline JIT is 33% behind LuaJIT's optimizing JIT on
average and ahead on 13. *Lesson: candidate 11 (the handlers as the
stencils) is how the state of the art avoids two copies of every
operation; hot/cold splitting keeps copied code small.*

**Ertl and Paysan, "The Performance Effects of Virtual-Machine Instruction
Pointer Updates" (ECOOP 2024, doi 10.4230/LIPIcs.ECOOP.2024.14).** On recent
out-of-order cores the chain of VM instruction-pointer updates can become
the critical path when VM instructions are light and programs loop-bound;
combining the updates, shortening their latency, and loading loop-back
targets without the IP gave speedups above 2x on some Gforth benchmarks on
the newest cores, 1.1-1.3x on many. *Lesson: on Zen 4 a dependence chain,
not dispatch, can be what limits a tight loop - in the interpreter here
`ip` and `sp` both form one.*

**Branch prediction (Rohou, Swamy and Seznec 2015, "Don't trust folklore";
Ertl's measurements, comp.compilers 2022-10-056).** With TAGE/ITTAGE-class
predictors a plain switch interpreter mispredicts little on small loops;
Ertl's Haswell numbers on Gforth's larger applications still showed 1.08-
1.37x from a dispatch at the end of every handler, 1.06-1.81x and up to
8.8x fewer mispredictions from replication, and 1.18-1.96x from dynamic
superinstructions. *Lesson: replication's prize depends on the program's
size and the predictor - measure the mispredictions before building it.*

**Tail-calling interpreters (CPython 3.14; Nelson Elhage's analysis,
blog.nelhage.com/post/cpython-tail-call).** First reported at 10-15%, the
gain shrank to 1-5% once an LLVM 19 regression was found that had slowed
the computed-goto baseline by ~10% by merging its dispatch jumps. WasmKit
(PR 145) and Wasm3 chose tail-called handlers because a single big
interpreter function spills `sp` and `pc` under register pressure.
*Lesson: little left for `tail` here; but a compiler change can silently
cost ~10% by merging dispatch jumps - `nocrossjump` exists for gcc's
version of that.*

**Register-machine interpreters (wasmi 0.32's switch from stack to register
byte code; Wasm3's "M3" design, VM registers as the handler functions'
arguments; Gregg et al. 2005: 35% fewer VM instructions executed for 45%
more byte-code loads).** The interpreter-side form of the register machine.
Here it would enlarge every image; the JIT form below gets the same
operations out of hot code without a second byte code.

**Native Forth compilers.** Mecrisp-Stellaris's RA kernel (ARM Cortex-M;
mecrisp-stellaris-folkdoc.sourceforge.io) tracks the top five stack
elements in registers, folds constants - words carry an "n-foldable" flag,
run at compile time when their n inputs are literals - inlines, and turns
final calls into jumps; where the stack depth is unknown it shifts the
register assignment by one. VFX Forth keeps stack items in registers across
a region; SwiftForth is subroutine threaded with inlining and peephole
rules (both commercial). On GitHub for reading: mecrisp-stellaris mirrors,
zeptoforth, feline (x86-64 native), Factor (its optimizing compiler checks
stack effects by abstract interpretation and builds SSA from the stack
code), ncw/ccforth (Forth compiled through C, with peephole patterns).

## What to borrow, in order

1. **Stack state in the JIT's translator - stencil variants by cached
   cells, and constants.** Today every stencil enters and leaves with
   `(sp, tos)`, so DUP, SWAP, OVER, DROP, a literal - 38-50% of the front's
   dispatches - each still emit code and touch memory in native code. The
   translator would track, through each word's straight-line code, how
   many of the top cells are in registers (0-2, or 0-3) and which are known
   constants; a shuffle becomes a change of state (no code, or one move), a
   literal a constant until an operation takes it as an immediate (ADDI and
   the fused tests exist already), and every stencil comes in the variants
   of its input and output states. At branch targets, loop heads and calls
   the state is made canonical (one cell, as now) by small spill and fill
   stencils - RPyForth found call-entry policies a wash, so the simplest
   one. Fits the aim: no image bytes, the JIT gene only; engine bytes grow
   with the variants (CPython's lesson: few states). **Price first**:
   `stackops.py`'s count restricted to the words the JIT translates
   (callsites.py names them), simulating a two- and a three-register cache
   with constants over each word's operations, weighted by the per-address
   counts of a run with the JIT off - the share of operations that would
   emit nothing, and the spills and fills added at joins. Then one
   prototype on fib and loop to turn that count into time (prompts/10:
   convert the proxy once). Budget against JIT.md's: engine +15 KB at most.
2. **Native code calling byte code (candidate 5)** - already priced (10%
   of the kernel workload, 80% of the sieve). Item 1 makes each native
   region worth more, so the two compound; build after 1 is priced.
3. **The handlers as the stencils (candidate 11)**, Deegen's way - one
   C description per operation for both tiers; with item 1 the variants
   multiply, so one source matters more. Price: the engine bytes the
   duplicated stencils cost on the front's JIT designs today.
4. **Hot/cold splitting of stencils** - error and rare paths out of the
   copied bytes. Price: the bytes of cold paths in the stencils the
   translator copies (tools/jit-check.sh prints each stencil's shape).
5. **The loop's back edge and the IP chain** (Ertl and Paysan) - on the
   laptop, `perf stat` IPC and branch misses for loop and fib on the
   interpreter path (no JIT) of the front's fastest design; if the loop
   runs near one VM instruction a cycle, the IP/`sp` chain is the limit,
   and loading `(LOOP)`'s target without `ip` is the cheap test.
6. **Replication (open item 7)** - only if 5 shows mispredictions that
   matter: `perf stat -e branch-misses` per thousand VM instructions on
   the corpus and the kernel workload. Ertl's gains came on large
   applications; ours are small.
7. **Compile-time folding of literal inputs** (Mecrisp's n-foldable) - in
   the run-time compiler, `3 CELLS` and the like computed once. Price: the
   dispatched pairs LIT + foldable word whose other input is a literal too,
   from the profiler's pair counts. Probably small; item 1 does it in
   native code for free.

Not borrowed: meta-tracing (RPython's toolchain is the whole VM), tracing
JITs in general (a trace recorder and guards are far more mechanism than
this project's aim allows), a register byte code for the interpreter
(every image larger - item 1 instead), `preserve_none` (clang only; `tail`
already measured).

## Sources

- Y. Izawa, K. Hakamada, RPyForth: Exposing a Call-Shared Data Stack to a
  Meta-Tracing JIT Compiler, 2026 - https://arxiv.org/abs/2609.23759
- CPython JIT: top-of-stack caching https://github.com/python/cpython/issues/135379 ;
  code quality https://github.com/python/cpython/issues/115802 ;
  plans for 3.15/3.16 https://github.com/python/cpython/issues/139038 ;
  K. Jin's plan https://fidget-spinner.github.io/posts/faster-jit-plan.html
- H. Xu, F. Kjolstad, Copy-and-Patch Compilation, OOPSLA 2021 - https://arxiv.org/abs/2011.13127
- H. Xu, F. Kjolstad, Deegen, OOPSLA 2026 - https://arxiv.org/abs/2411.11469 ;
  https://github.com/luajit-remake/luajit-remake
- B. Titzer, Whose baseline compiler is it anyway?, CGO 2024 - https://arxiv.org/abs/2305.13241 ;
  V8 Liftoff - https://v8.dev/blog/liftoff
- M. A. Ertl, B. Paysan, The Performance Effects of Virtual-Machine
  Instruction Pointer Updates, ECOOP 2024 - https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2024.14
- M. A. Ertl on replication and dispatch, Haswell - https://compilers.iecc.com/comparch/article/22-10-056
- N. Elhage, Performance of the Python 3.14 tail-call interpreter - https://blog.nelhage.com/post/cpython-tail-call/
- wasmi 0.32 register byte code - https://github.com/wasmi-labs/wasmi ;
  Wasm3 - https://github.com/wasm3/wasm3 ; WasmKit PR 145 - https://github.com/swiftwasm/WasmKit/pull/145
- D. Gregg et al., The case for virtual register machines, SCP 2005
- Mecrisp-Stellaris RA kernel and folding - https://mecrisp-stellaris-folkdoc.sourceforge.io/ra-kernel.html ,
  https://mecrisp-stellaris-folkdoc.sourceforge.io/folding.html
