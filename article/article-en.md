# Nine Forth virtual machines, and the bug that beat all of them

*Everything here builds and regenerates from the repository with two
commands. Nothing is quoted from memory.*

L.C. Benschop's SOD32 is a 32-bit stack machine with a Forth on top,
published in the 1990s and still building today. Twenty years ago I took
it apart, replaced its packed instruction format with one relative
offset per cell, and called the result RelF. Recently I went back to my
own system and spent some months making the image smaller and the
interpreter faster: eight encodings, each one a working Forth that
compiles itself.

The encodings were worth about 22%.

Then I ran the ancestor side by side with the descendant for the first
time, and found that I had dropped a hash table out of the dictionary in
2004 and never noticed. Putting it back was worth 4x.

This is a report on both halves, and on the three separate occasions
when a measurement I trusted turned out to be measuring something else.

    tools/build-stages.sh      # nine systems, both cell widths
    tools/run-tests.sh         # the same 616-case corpus on all of them
    tools/collect-results.sh   # regenerate every table below

---

## 1. Names, against the real taxonomy

The best short treatment of threaded code models I know is a 2024
ForthHub thread, "An elevator description for Forth's threaded code
models?" (<https://github.com/ForthHub/discussion/discussions/187>).
Mitch Bradley, who wrote Open Firmware, ruv, Anthony Howe and others try
there to explain the family in the space of a lift ride. I will use
their vocabulary rather than invent my own. Bradley's summary:

> Threaded code is a compact binary representation of a computer program
> as a list of pointers. In direct threaded code, the pointers point
> directly to machine code. In indirect threaded code, they point to
> object structures, the first field of which is a pointer to machine
> code.

and, from the same thread, the variant this article lives in:

> There is also a "token threaded" variant where the pointers are not
> full addresses, but instead some extra-compact representation like
> indices into an array, or variable-length identifiers.

That sentence describes most of what follows. The systems have local
names because they were built one after another and needed telling
apart; here is what each one actually is.

| name here | in standard terms |
|---|---|
| SOD32 | six 5-bit subinstructions packed per 32-bit cell, plus a return flag |
| cell | one host cell per operation, and the cell IS a relative offset |
| PACK4 | tagged nibble: a tag byte then 4-bit opcodes, 16-opcode alphabet |
| PACK8 | tagged byte: a tag byte then 8-bit opcodes |
| SOD16 | token threading, word numbers through a table built at load |
| CPT16 | token threading, table deleted; target = base + (v << S) |
| CV8 | the same, narrowed to a byte stream - byte-coded |
| +spec | CV8 plus specialised opcodes for locals, variables, hot words |

One property is shared by all nine and is SOD32's: the engine and the
image are separate artefacts, and the image is machine independent while
the engine is not. The other is RelF's and is *not* true of SOD32 - in
RelF every reference inside an image is relative, so an image loads
anywhere, where SOD32 uses absolute addresses inside its own simulated
memory.

That first property got tested by accident. The images the ARM board
runs are byte-for-byte the same files the x86 machines run.

---

## 2. Nine systems, and what "built" means

All nine boot, run a Forth interpreter, compile new definitions at run
time, and pass the same 616-case ANS CORE corpus at both cell widths.
Eight of them cross-compile the kernel and produce an image
byte-identical to the reference.

That makes the correctness check and the benchmark the same run. A stage
that is fast because it is quietly wrong fails the comparison that times
it.

Getting SOD32 to read the same corpus took three fixes to the file and
none to SOD32: CRLF line endings, some CP1251 comments, and comments
that opened on one line and closed on another. Only the last matters.
ANSI `(` skips to the next `)` *in the current parse area*; RelF extends
that across lines and SOD32 does not. A shared corpus must not depend on
one system's extension.

### What self-hosting costs, per encoding

A translated image runs what was compiled into it and compiles nothing
new. To make each stage compile *its own* encoding I wrote an emitter
overlay in Forth for each - a file replacing `;`, `IF`, `LITERAL`,
`CREATE`, `DOES>` and the rest with versions that lay down that
encoding. The overlays measure how complicated each design really is,
and they are not close.

**CPT16's `CALL,` is one line:**

    : CALL, ( a-addr --- )
      START @ - CPT-SHIFT RSHIFT 256 + OP, ;

Subtract the base, shift, add the opcode band. That is the whole call
mechanism.

**SOD16's is a page.** A SOD16 call names a *word number*; the compiler
has an address. The engine's table runs number-to-address and lives in
the engine's `malloc`ed memory, unreachable from Forth, so the image
builds its own sorted copy on the heap and binary-searches it on every
call it compiles.

And the table is sized at load and never grows, so a word defined
afterwards has no number at all. That needed a new opcode - a far call
naming an address directly - plus a second for `DOES>`, whose runtime
pushes a mid-word address no word number can name.

Deleting the table is usually argued for on dispatch cost, one fewer
dependent load. This is the argument that convinced me, and it is
invisible until the system has to compile for itself.

### Literals and control flow, since somebody will ask

ruv's reply to Bradley in that thread was "what about literals and
control-flow? ... The devil is in the details". He is right:

- **Literals.** CV8 picks the narrowest of five forms: single-byte
  opcodes for 0, 1 and -1, then 8-, 16-, 32-bit and full-cell. The
  16-bit encodings have a 16-bit `LIT`, a 32-bit form, and - added
  during this work - a 64-bit one. That gap is one of the bugs below.
- **Branches.** A signed 16-bit offset from the operand itself, in
  tokens for SOD16 and CPT16, in bytes for CV8. No branch in a real
  image needs more than 16 bits, checked rather than assumed.
- **`DO ... LOOP`.** `(LOOP)` reads an inline *cell* operand holding a
  byte offset, the one place CV8 keeps cell granularity, so the compiler
  pads with NOOPs to keep it aligned. The pad executes, once per loop.
- **`DOES>`.** A created word's body is `[DOVAR][pad][PFA]`, and `DOES>`
  overwrites the front with a call to the tail. There is exactly one
  cell of room. That is why SOD16's far `DOES>` form uses a halved
  16-bit offset: on a 4-byte build, 32 bits does not fit.

---

## 3. How this is measured, before any table

Three machines: a single-vCPU x86-64 VM, a 16-core x86-64 laptop, and a
4-core ARMv7 board. Every timing is the minimum of interleaved
repetitions, net of process startup, and every harness checks
correctness before it measures anything.

**The resolution floor belongs to the WORKLOAD, not the machine.**
`tools/layout-noise.sh` builds one engine five times, varying only flags
that move code without changing what it computes, checks all five still
produce a byte-identical kernel, and times them. On the ARM board:
kernel compile 1.1%, corpus 1.3%, parse 1.4%, `fib` 6.0%. On the laptop
the same measurement reads 5.3% in one run and 13.1% in the next.

**The fastest machine is the worst instrument.** Two consecutive sweeps,
largest change in any stage's ratio:

| workload | laptop | ARM board |
|---|---|---|
| kernel | 8.1% | **2.0%** |
| parse | 7.0% | **1.6%** |
| corpus | 12.9% | 3.7% |
| `fib` | 23.1% | 15.1% |

Sixteen cores, boost clocks and a desktop session leave the laptop
unable to resolve anything under about 13%. Four slow cores with nothing
else running resolve to about 1%. Intuition says the opposite and
intuition is wrong.

**Two workloads had to be discarded.** `loop.fth`, nested counted loops
over stack arithmetic, swings 21% between runs of the same binary on the
same board. `fib.fth`, naive recursive Fibonacci, added late because
nothing else isolated the *call*, swings 15-23%. Both are the short
narrow ones; both surviving workloads run a lot of varied code. A tight
interpreter loop over a handful of opcodes is dominated by
indirect-branch prediction and code placement, which is exactly what
moves between builds and between runs.

So magnitudes come from the ARM board, on kernel compilation and
parsing. Ordering is quoted only where all three machines agree.

---

## 4. Results

### Size, which is machine-independent

The unit is the Forth image: the smallest image that boots into the
interpreter and can rebuild the system, following SOD32's own Makefile
where `forth.img` is the finished artefact.

| stage | 8-byte cells | 4-byte cells |
|---|---|---|
| SOD32 | -- | 13,292 |
| cell | 24,320 | 13,380 |
| PACK4 | 21,296 | 11,900 |
| PACK8 | 20,848 | 11,844 |
| SOD16 | 12,864 | 10,000 |
| CPT16 | 12,864 | 10,000 |
| CPT16+fold | 12,696 | 9,772 |
| CV8 | 11,416 | 8,456 |
| CV8+spec | 11,088 | 8,108 |

The 8-byte column is where token encodings earn their keep: a cell
scheme costs twice as much on a 64-bit host, a token stream costs the
same on both. 0.46x against 0.61x.

The packed figures are arithmetic rather than files - those schemes
rewrite the image in place and leave the cells they skip where they
were. Since packing is cell-granular and every reference is relative,
compacting removes exactly (cells folded) x (cell size) bytes and can
change nothing else.

### Speed, ARM board, 4-byte cells, against the cell engine

Floors: kernel 1.1%, parse 1.4%. A second sweep agreed within 2.0%.

| stage | kernel compile | parse |
|---|---|---|
| SOD32 | -- | 1.397 |
| cell | 1.000 | 1.000 |
| PACK4 | 1.130 | 1.106 |
| PACK8 | 1.066 | 1.045 |
| SOD16 | 1.400 | 1.017 |
| CPT16 | 0.997 | 0.964 |
| CPT16+fold | 0.913 | 0.885 |
| CV8 | 0.890 | 0.890 |
| CV8+spec | **0.782** | **0.765** |

The ordering is identical on all three machines. The whole ladder is
worth about 22% at 4-byte cells, and rather more at 8-byte, where the
laptop puts CV8+spec at 0.636-0.670 on kernel compilation.

Three things are worth pulling out.

**SOD16 is a real regression** - 1.40 on kernel compilation, the worst
stage anywhere, on every machine. The word table costs more than it
saves, and it also costs the compiler a binary search and two escape
opcodes.

**CPT16 is indistinguishable from the cell engine** at 0.997 against a
1.1% floor. Deleting the table recovers everything SOD16 lost and
nothing more. The encoding wins come afterwards, from folding
`prim;EXIT` and from the specialisations.

**The specialisations are most of the total.** CV8 alone is 0.890;
adding locals, variables, tiny kernel words and small integers as
opcodes takes it to 0.782. That is a larger step than every encoding
change put together.

---

## 5. Four times the work was wrong

This is the part I would keep if I had to cut the rest.

### 5.1 Two designs rejected on a benchmark four times too harsh

Before SOD16 I considered packing several opcodes into a cell in the
SOD32 manner but with different field widths: a tagged nibble scheme
(4-bit opcodes, sixteen of them) and a tagged byte scheme. Both were
sized on a census, both were timed in a synthetic dispatch loop, both
were rejected on the timing - 1.65x and 1.60x on x86-64, 2.05x and 1.90x
on i386 - and neither was ever built.

Built, on kernel compilation:

| | predicted | 8-byte cells | 4-byte cells |
|---|---|---|---|
| tagged nibble | 2.05x | 0.993-1.128 | 1.111-1.212 |
| tagged byte | 1.90x | 0.980-1.034 | 1.044-1.186 |

At 8-byte cells they are indistinguishable from the cell engine. At
4-byte they cost 5-20%. Not 90-105%.

The benchmark's own header says why, in advance:

> This benchmark's streams are sized to run hot, so it isolates decode
> cost and deliberately ignores the advantage density would bring. Read
> it as "what does unpacking cost when memory is free", i.e. the
> pessimistic case for the packed schemes.

It was the pessimistic case by a factor nobody estimated. The baseline
it lost to was also wrong: token threading had been recorded at 0.985 -
faster than cell dispatch - from a benchmark running a 32 MB stream
against a 2 MB L2. It was measuring memory traffic.

The rejection still stands, because CV8 beats both packed schemes on
both axes at both widths on every machine. The reason recorded for it
does not.

And there is a result only building could produce. The census had nibble
and byte level on size, both at 0.76x. Built, the nibble scheme folds
away *fewer* cells - 377 against 433 - and ends up the larger image. A
four-bit opcode reaches only sixteen primitives, and a primitive outside
that alphabet does not merely fail to pack: it *ends the run it sits
in*. The mean run of packable primitives is about 1.3. Breaking runs
costs more than the narrow field saves.

A size model prices the fields. The program pays for the joins.

### 5.2 A 4x regression I introduced in 2004

Before the fix below, SOD32 beat every system here on any workload that
interprets text: 2x on the corpus, 2.9x on parsing. On a pure-execution
loop it was slower than almost all of them. So the difference was not
the VM.

Counting executed VM operations on the same 4000 lines of input: SOD32
44,539,357, RelF 266,555,732. Six times the work for the same result,
with the faster dispatch of the two.

Profiling the calls: of 72 distinct call targets the three hottest are
`DOVAR`, `-` and `NAMEBUF`, and `NAMEBUF` is entered 8.1 million times
for 28,000 words of input. `NAMEBUF` is touched once per iteration of
`SEARCH-WORDLIST`'s outer loop. That is 290 dictionary entries examined
per lookup.

SOD32's `FORTH-WORDLIST` is an array of 33 cells - a thread count and 32
chain heads - and its `SEARCH-WORDLIST` hashes the first two characters
of the name to pick a thread:

    NAMEBUF COUNT 2 PICK @ HASH 1+ CELLS SWAP + @   \ get the right thread

RelF's `FORTH-WORDLIST` is one cell, described in my own source as "a
pointer to the last definition in the Forth word list", and the search
walks it from the top. I dropped the hash when I derived RelF from
SOD32 and put nothing in its place. I do not remember deciding to; I
think I simplified the structure while changing the link fields from
absolute to relative, and never went back to see what it cost.

It costs most on *numbers*, which are never found and so pay a complete
traversal before the system gives up and converts them. Half the tokens
in a program's text are numbers.

Restored, with SOD32's hash function unchanged:

    dictionary entries visited     before  8,052,823
                                    after    288,037
                                    sod32    397,720

That is a count, not a timing, so it is the same on every machine. In
time it was 3.7x on parsing at 4-byte cells and 4.4x at 8-byte. The
system that was 2.7x slower than its ancestor at interpreting text is
now faster than it.

For scale: the entire encoding ladder is worth 0.78. One omission,
restored, was worth more than all of it. It survived twenty years and
two hundred iterations of optimisation work, because every benchmark I
ever ran compared the system against *itself* - against last week's
build, never against the thing it came from. The ancestor was in a
tarball the whole time, and running the two side by side was an
afternoon's work I did not do until this year.

### 5.3 One syscall per character

`KEY` was `read(0, &c, 1)` and `EMIT` was `write(1, &c, 1)`. `READ-LINE`
on a file was `read(fd, &c, 1)`. One corpus run made 32,357 syscalls
against SOD32's 59; one kernel cross-compile made 67,316.

It never showed on my own machine, which is a Firecracker VM where
syscalls are unusually cheap. It showed the moment the same build ran on
a faster laptop and came out five times slower on every workload that
touches text while the pure-execution loop was unchanged.

Buffered: 49 and 66. Kernel compilation halved, and - the part that
matters - the ratios decompressed. The constant was identical for every
stage, so it had been dragging every comparison towards 1.0 and hiding
the differences the benchmarks exist to show.

Then adding the buffer cost the specialised CV8 engine 85% on a workload
that reads no files at all: 9.5 to 17.6 ms, same image, same input. GCC
had inlined the cold I/O helpers into the dispatch function and register
allocation collapsed. `__attribute__((noinline))` put it back. A
function nothing in that run ever called was enough, purely by being
inlinable.

### 5.4 Tests and benchmarks that could not fail

Three of them, all mine.

A harness that reported "0 failures" because the engine had segfaulted
on line 9 - `$?` after a pipeline is `tr`'s status, not the engine's.

A `layout-noise` run that reported a tidy 1.9% spread over five builds
that had each executed for two milliseconds and done nothing: the
engines died on startup, which left the output file untouched, which
made it byte-identical to the reference, which passed the correctness
gate.

And the best one. After the hashed word list went in, the system passed
all 616 CORE cases and then could not cross-compile itself. `WORDLIST`
still made a one-cell word list, so the cross compiler's vocabularies
were one cell each and `SEARCH-WORDLIST` read a chain head as a thread
count. A test suite that exercises the language thoroughly and never
creates a vocabulary.

Every stage now runs a negative control: the corpus plus one
deliberately wrong case, and a stage that does not notice is reported
BROKEN rather than ok.

The ratio is worth stating plainly. Across this whole exercise, almost
every defect found was in the measuring apparatus rather than in the
nine Forth systems. The systems passed 616 cases on every machine they
were built on. What kept breaking was the scaffolding that measured
them.

---

## 6. What is not measured

- **Three machines is not a study.** Two x86-64 and one ARMv7. No
  RISC-V, no big-endian anything, no bare metal without an OS. Two
  machines were enough to overturn one claim; the third overturned my
  explanation of it.
- **Two microbenchmarks were discarded**, so nothing here measures pure
  execution reliably. `loop` and `fib` are in the repository as the
  worked example of microbenchmarks that do not reproduce.
- **Relocation and portability**, two of the axes Bradley's fuller
  answer in that thread lists, are untested. RelF's relative addressing
  has something to say about both and I have not measured what it costs.
- **The thread count is 32 because SOD32's is 32.** For a dictionary of
  a few hundred words that is inheritance, not a choice.
- **ITC extensibility.** With token threading a new behaviour type
  cannot be added from Forth; `DOES>` is the only extension point. That
  is the strongest architectural criticism this design has had and I do
  not have an answer to it.

## 7. References

- Brad Rodriguez, *Moving Forth*, part 1 -
  <https://www.bradrodriguez.com/papers/moving1.htm>
- R.G. Loeliger, *Threaded Interpretive Languages*, Byte Books, 1981
- L.C. Benschop, SOD32 - <https://github.com/lennart-benschop/sod32>,
  vendored here at a pinned revision, GPLv2
- ForthHub discussion #187, "An elevator description for Forth's
  threaded code models?"
- IEEE Standard 1275-1994, *Standard for Boot Firmware*, which defines
  FCode. The accessible description of the encoding is Oracle's *Writing
  FCode 3.x Programs* -
  <https://docs.oracle.com/cd/E19957-01/802-3239-10/fcprog.html> - and
  there is a working tokenizer and detokenizer in
  <https://github.com/openbios/fcode-utils>.
- Borrowed, and named in the source where borrowed: JVM and FCode for
  byte-granular tokens; HotSpot compressed oops for
  `base + (v << shift)`; JVM `iload`, CPython `LOAD_FAST` and
  Smalltalk-80's bytecodes 16-31 for locals as opcodes; CPython 3.11 /
  PEP 659 for specialise-the-common-case; Lua 5.4 for small immediate
  operands; Titzer's in-place Wasm interpreter for interpreting the
  compact form rather than expanding it at load.

### What CV8 took from FCode, and what it did not

The project's notes credited FCode for "byte tokens with an escape for
two-byte codes" and admitted the ranges were remembered rather than
checked. Checked, they are these. One-byte FCode numbers run `0x10` to
`0xFE`. A byte in `0x01`-`0x0F` is an escape: it and the byte after it
form a two-byte FCode number, yielding 15 x 256 further codes. `0x00`
and `0xFF` both mean end of program.

CV8's layout is not that. CV8 splits on the top bit - `0x00`-`0x7F` is
an opcode, `0x80`-`0xFF` begins a call whose remaining bits are part of
a scaled offset - and its escape is a single reserved opcode rather than
a band of fifteen. FCode has no call band, because an FCode token *is* a
dictionary reference.

So the debt is narrower than "we used FCode's encoding". What was taken
is the demonstration that a byte-granular token stream with an escape
hatch works as a compact, position-independent representation for a
Forth. IEEE 1275 is where that was shown at scale, long before this
project.
