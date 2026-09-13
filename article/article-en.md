# Nine Forth virtual machines, measured against each other

*Working draft. Numbers regenerate from the repository with two
commands; nothing below is quoted from memory.*

L.C. Benschop's SOD32 is a 32-bit stack machine with a Forth on top,
published in the 1990s and still building today. Twenty years ago Kirill
Timofeev took it apart, replaced its packed instruction format with
one relative offset per cell, and called the result RelF. I have spent
some months taking RelF apart in turn, trying to make its image smaller
and its interpreter faster, and this is a report on what the encodings
were actually worth.

The short version is that the encoding work was worth about 20%, that
two designs the project rejected without building were rejected for a
reason that turned out to be wrong by a factor of four, and that the
largest single number in the whole exercise came from a hash table
somebody forgot to copy across in 2004.

Everything here builds:

    tools/build-stages.sh      # nine systems, both cell widths
    tools/run-tests.sh         # the same 616-case corpus on all of them
    tools/collect-results.sh   # regenerate every table below

---

## 1. Names, and how they map onto the real taxonomy

Discussion #187 on this forum is the best short treatment of threaded
code models I know of, and I am going to lean on its vocabulary rather
than invent my own. Mitch Bradley's summary there:

> Threaded code is a compact binary representation of a computer program
> as a list of pointers. In direct threaded code, the pointers point
> directly to machine code. In indirect threaded code, they point to
> object structures, the first field of which is a pointer to machine
> code.

and, in the same thread, the variant this article lives in:

> There is also a "token threaded" variant where the pointers are not
> full addresses, but instead some extra-compact representation like
> indices into an array, or variable-length identifiers.

That sentence describes most of what follows. Everything below is token
threading of one shape or another, and the article is about which shape.

The systems have local names, because they were built one after another
and needed distinguishing. Here is what each one actually is:

| name here | what it is in standard terms |
|---|---|
| SOD32 | six 5-bit subinstructions packed per 32-bit cell, plus a return flag |
| cell | one host cell per operation, the cell IS a relative offset - closest to direct threading with relocatable pointers |
| PACK4 | tagged nibble: a tag byte then 4-bit opcodes, 16-opcode alphabet |
| PACK8 | tagged byte: a tag byte then 8-bit opcodes |
| SOD16 | token threading with a word-number table built at load |
| CPT16 | token threading with the table deleted; target = base + (v << S) |
| CV8 | the same, narrowed to a byte stream - byte-coded |
| +spec | CV8 plus specialised opcodes for locals, variables and hot words |

Two properties are constant across all of them and are RelF's, not mine.
Every reference in an image is *relative*, so an image is position
independent and loads anywhere. And the engine and the image are
separate artefacts, which is SOD32's idea - the image is machine
independent, the engine is not.

---

## 2. The chain, and what "built" means

Nine systems. All nine boot, run a Forth interpreter, compile new
definitions at run time, and pass the same test corpus at both 4-byte
and 8-byte cells. Eight of them cross-compile the kernel and produce an
image byte-identical to the reference.

That last property is doing more work than it looks. It means the
correctness check and the benchmark are the same run: a stage that is
fast because it is quietly wrong fails the comparison that times it.

The corpus is the Hayes ANS CORE suite, 616 cases, identical source text
for every system including SOD32. Getting SOD32 to read it needed three
fixes to the file and none to SOD32: CRLF line endings, some CP1251
comments, and - the only one with any weight - comments that opened on
one line and closed on another. ANSI `(` skips to the next `)` *in the
current parse area*. RelF extends that across lines; SOD32 does not. A
corpus shared between two systems must not depend on an extension of
one of them.

### What self-hosting costs, per encoding

This is the part that generalises, and it is the part a size model
cannot see.

A translated image can run everything compiled into it and compile
nothing new. Making each stage compile *its own* encoding meant writing
an emitter overlay in Forth for each - a file that replaces `;`, `IF`,
`LITERAL`, `CREATE`, `DOES>` and the rest with versions that lay down
that encoding. The overlays are the honest measure of how complicated
each design is, and they differ enormously.

**CPT16's `CALL,` is one line:**

    : CALL, ( a-addr --- )
      START @ - CPT-SHIFT RSHIFT 256 + OP, ;

Subtract the base, shift, add the opcode band. That is the entire call
mechanism.

**SOD16's is a page**, because a SOD16 call names a *word number*, and
the compiler has an address. The engine's table is number-to-address and
lives in the engine's `malloc`ed memory, unreachable from Forth. So the
image rebuilds its own sorted copy on the heap and binary searches it on
every call it compiles. Worse: the table is sized at load and never
grows, so a word defined afterwards has no number at all. That needed a
new opcode - a far call naming an address directly - and a second one
for `DOES>`, whose runtime pushes a mid-word address that no word number
can name.

Deleting the table is usually argued for on dispatch cost: one fewer
dependent load. The argument that actually convinced me is this one, and
it only becomes visible when the system has to compile for itself.

### Literals and control flow, since somebody will ask

ruv's response to Bradley's summary in #187 was "what about literals and
control-flow? ... The devil is in the details", and he is right, so:

- **Literals.** CV8 picks the narrowest of five forms: three
  single-byte opcodes for 0, 1 and -1, then 8-bit, 16-bit, 32-bit and
  full-cell forms. The 16-bit encodings have `LIT` with a 16-bit
  operand, a 32-bit form, and - added during this work - a 64-bit form.
  More on why below; it is one of the bugs.
- **Branches.** A signed 16-bit offset, measured from the operand
  itself, counted in tokens for SOD16/CPT16 and in bytes for CV8. Zero
  branches in a real image need more than 16 bits, which was checked
  rather than assumed.
- **`DO ... LOOP`.** `(LOOP)` reads an inline *cell* operand holding a
  byte offset. That is the one place CV8 keeps cell granularity, and the
  compiler pads with NOOPs before the call so the operand lands aligned.
  The pad executes, once per loop.
- **`DOES>`.** A created word's body is `[DOVAR][pad][PFA]`, and
  `DOES>` overwrites the front of it with a call to the tail. There is
  exactly one cell of room, which is why SOD16's far `DOES>` form takes
  a halved 16-bit offset rather than a 32-bit one: on a 4-byte build,
  32 bits does not fit.

---

## 3. Results

One machine, a single-vCPU x86-64 VM. Ratios travel; the milliseconds do
not. Minimum of interleaved repetitions, net of process startup.

### How small a difference is real

Before any table: build the *same* engine five times, varying only flags
that move code and change nothing about what it computes, check all five
still produce a byte-identical kernel, and time them on the same
workload. The spread is **5.3%**.

That is the resolution of everything below. A difference smaller than it
is not a result. It is why I report CPT16 and the cell engine as
indistinguishable rather than ranking them.

The harness needed its own medicine. At six repetitions it reported 5.3%
and then 11.2% on consecutive runs and disagreed about which build was
fastest - it was measuring the machine. Forty repetitions settles it,
and *which* build wins still moves, so the figure is a band and not a
ranking of compiler flags.

### Size

The unit is the Forth image: the smallest image that boots into the
interpreter and can rebuild the system. That follows SOD32's own
Makefile, where `forth.img` is the finished artefact. Run-only images
carry an identical word set at every stage, so a difference between two
rows is the encoding and nothing else.

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

Two remarks. The packed figures are arithmetic rather than files: those
schemes rewrite the image in place and leave the cells they skip where
they were, and since packing is cell-granular and every reference is
relative, compacting removes exactly (cells folded) x (cell size) bytes
and can change nothing else. And the 8-byte column is where the
token encodings earn their keep - a cell scheme costs twice as much on a
64-bit host, a token stream costs the same on both.

### Speed, 4-byte cells, against the cell engine

| stage | kernel compile | CORE corpus | loop | parse |
|---|---|---|---|---|
| SOD32 | -- | 1.162 | 1.625 | 1.315 |
| cell | 1.000 | 1.000 | 1.000 | 1.000 |
| PACK4 | 1.158 | 1.159 | 1.175 | 1.242 |
| PACK8 | 1.120 | 1.123 | 1.238 | 1.255 |
| SOD16 | 1.241 | 1.326 | 1.658 | 1.115 |
| CPT16 | 1.036 | 1.020 | 1.106 | 1.112 |
| CPT16+fold | 0.983 | 0.927 | 0.946 | 1.011 |
| CV8 | 0.962 | 0.931 | 1.032 | 0.993 |
| CV8+spec | 0.751 | 0.722 | 0.864 | 0.684 |

Four workloads: cross-compiling the kernel (self-hosting work, and the
one with the byte-identical check), the CORE corpus, a nested counted
loop that is almost pure inner interpreter, and 4000 lines of
interpreted arithmetic that is almost pure outer interpreter.

Seven of the eight rows agree to within 0.18 across all four workloads.
Where two of those seven swap places between columns - CV8 against
CPT16+fold, PACK4 against PACK8 - the gap between them is inside the
5.3% floor, so they were never orderable in the first place. The
conclusion does not depend on which benchmark you pick.

**SOD16 is the exception and the reason is the escape hatch.** Its
spread is 0.543 - worst of everything on the loop, and on parsing it
overtakes both packed schemes and comes within noise of CPT16. It is the only stage whose runtime-compiled code
differs systematically from its translated code: every call to a word
defined after load costs three tokens instead of one. `loop.fth` is
almost entirely runtime-compiled definitions calling each other.
`parse.fth` runs inside the translated kernel, where the table calls
survive and SOD16's denser image starts paying for itself in cache.

A cost the image does not pay. Whatever it compiles later pays it.

---

## 4. Three times the work was wrong

This is the part I would keep if I had to cut the rest.

### 4.1 Two designs rejected on a measurement four times too harsh

Before SOD16 the project considered packing several opcodes into a cell,
in the SOD32 manner but with different field widths: a tagged nibble
scheme (4-bit opcodes, 16 of them) and a tagged byte scheme (8-bit
opcodes). Both were sized on a census, both were timed in a synthetic
dispatch loop, and both were rejected on the timing: 1.65x and 1.60x on
x86-64, 2.05x and 1.90x on i386. Neither was ever built.

I built them. Measured in a real engine, at 4-byte cells:

| | predicted | measured, kernel compile |
|---|---|---|
| tagged nibble | 2.05x | 1.158x |
| tagged byte | 1.90x | 1.120x |

The rejection was right - CV8 beats both on size and speed at once - but
the number it rested on was wrong by about four times. The benchmark's
own header says why, and says it in advance:

> This benchmark's streams are sized to run hot, so it isolates decode
> cost and deliberately ignores the advantage density would bring. Read
> it as "what does unpacking cost when memory is free", i.e. the
> pessimistic case for the packed schemes.

It was the pessimistic case by a factor nobody estimated. And the
baseline it lost to was itself wrong: token threading was recorded at
0.985 - faster than cell dispatch - from a benchmark running a 32 MB
stream against a 2 MB L2. It was measuring memory traffic. The real
figure is about 6%.

There is a second result that only building could produce. The census
had nibble and byte level on size, both at 0.76x. Built, the nibble
scheme folds away *fewer* cells - 377 against 433 - and ends up the
larger image. A four-bit opcode reaches only sixteen primitives, and a
primitive outside that alphabet does not merely fail to pack: it *ends
the run it sits in*. The mean run of packable primitives is about 1.3.
Breaking runs costs more than the narrow field saves.

A size model prices the fields. The program pays for the joins.

### 4.2 A 4x regression, inherited by omission

Before the fix described in this section, SOD32 was faster than every
system in this repository on any workload that interprets text - 2x on
the corpus, 2.9x on parsing - while being *slower* than almost all of
them on the loop benchmark. So it was not the VM.

Counting executed VM operations on the same 4000 lines: SOD32
44,539,357, RelF 266,555,732. Six times the work for the same result,
with the faster dispatch of the two.

Profiling the calls: of 72 distinct call targets, the three hottest are
`DOVAR`, `-`, and `NAMEBUF`, and `NAMEBUF` is entered 8.1 million times
for 28,000 words of input. `NAMEBUF` is touched once per iteration of
`SEARCH-WORDLIST`'s outer loop. That is 290 dictionary entries examined
per lookup.

SOD32's `FORTH-WORDLIST` is an array of 33 cells - a thread count and 32
chain heads - and its `SEARCH-WORDLIST` hashes the first two characters
of the name to pick a thread:

    NAMEBUF COUNT 2 PICK @ HASH 1+ CELLS SWAP + @   \ get the right thread

RelF's `FORTH-WORDLIST` is one cell, described in its own source as "a
pointer to the last definition in the Forth word list", and the search
walks it from the top. The hash was dropped when RelF was derived from
SOD32. Nothing replaced it. Every lookup is a linear scan of the whole
dictionary - twice, because the default search order holds the wordlist
in two slots - and it is worst for *numbers*, which are never found and
so cost a complete traversal before the system gives up and converts
them. Half the tokens in a program's text are numbers.

Restoring it, with SOD32's hash function unchanged:

    dictionary entries visited     before  8,052,823
                                    after    288,037
                                    sod32    397,720

    parse.fth, 4-byte cells        before      611 ms
                                    after      165 ms
                                    sod32      225 ms

3.7x on parsing at 4-byte cells, 4.4x at 8-byte, 2.3x on the corpus. The
system that was 2.7x slower than its ancestor at interpreting text is
now slightly faster than it.

For scale: the entire encoding ladder is worth 0.75x. One omission,
restored, was worth more than all of it - and it went unnoticed for two
hundred iterations, because every benchmark the project used compared
the system against *itself*.

All the numbers in section 3 are from after this fix. Anything measured
before it is not comparable and is not reproduced.

### 4.3 A test suite that could not fail

For several iterations the only suites being run were shell tests, which
never compile anything, so they passed long before the Forth compiler
was correct. I repeated the same class of mistake twice in one afternoon
while building the new harness: a run that reported "0 failures" because
the engine had segfaulted on line 9 (`$?` after a pipeline is `tr`'s
status, not the engine's), and a pattern that matched the *tester's own
definition* of `ERROR` when an engine echoes its input, inventing two
failures on SOD32.

Every stage now also runs a negative control - the corpus plus one
deliberately wrong case - and is reported BROKEN rather than ok if it
does not notice.

The best instance of this was later. After the hashed wordlist went in,
the system passed all 616 CORE cases and then could not cross-compile
itself: `WORDLIST` still made a one-cell word list, so the cross
compiler's vocabularies were one cell each and `SEARCH-WORDLIST` read a
chain head as a thread count. A suite that exercises the language
thoroughly and never creates a vocabulary.

---

## 5. What is not measured

- **One machine.** A single-vCPU x86-64 VM. No ARM, no RISC-V, no bare
  metal, no cache-hierarchy variation. Density arguments are exactly the
  ones most sensitive to that, and the packed schemes were originally
  rejected by a benchmark that held memory free.
- **Relocation and portability**, two of the axes Bradley's fuller
  answer in #187 lists. RelF's relative addressing has something to say
  about both - the same image runs at any load address, and the same
  image file runs on any host agreeing on cell width and endianness -
  but I have not measured what that costs.
- **The thread count** is 32 because SOD32's is 32. For a dictionary of
  a few hundred words that is a guess, not a choice.
- **ITC extensibility.** With token threading a new behaviour type
  cannot be added from Forth; `DOES>` is the only extension point. That
  is the strongest architectural criticism this design has had and I do
  not have an answer to it.

## 6. References

- Brad Rodriguez, *Moving Forth*, part 1 -
  <https://www.bradrodriguez.com/papers/moving1.htm>
- R.G. Loeliger, *Threaded Interpretive Languages*, Byte Books, 1981
- L.C. Benschop, SOD32 - <https://github.com/lennart-benschop/sod32>,
  vendored here at a pinned revision, GPLv2
- ForthHub discussion #187, "An elevator description for Forth's
  threaded code models?"
- Borrowed, and named in the source where borrowed: JVM and Open
  Firmware FCode for byte-granular tokens; HotSpot compressed oops for
  `base + (v << shift)`; JVM `iload`, CPython `LOAD_FAST` and
  Smalltalk-80's bytecodes 16-31 for locals as opcodes; CPython 3.11 /
  PEP 659 for specialise-the-common-case; Lua 5.4 for small immediate
  operands; Titzer's in-place Wasm interpreter for interpreting the
  compact form rather than expanding it at load.

*The FCode attribution needs checking against IEEE 1275 before this is
published: the general shape - byte tokens with an escape for two-byte
codes - is remembered, the exact ranges are not.*
