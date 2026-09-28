# Making a Forth virtual machine smaller: seven attempts, three of which failed

I have always liked L.C. Benschop's SOD32 - the Stack Oriented Design, a
32-bit virtual machine with a Forth on top - for how lean, minimal and
simple it is. But its performance is fairly low, and in 2004 I started
wondering whether that could be improved. That is how RelF, for Relative
Forth, came about: I threw away SOD32's packed instruction format and
replaced it with one relative offset per cell. (A cell is the machine
word a Forth is built on: four bytes on a 32-bit host, eight on a 64-bit
one.) The speed-up turned out to be fairly modest, and for a long time I
lost interest in the project.

Recently I came back to it and built it for 64 bits. The same Forth, the
same words, in an image that had gone from 13,380 bytes to 24,320 - one
relative offset per cell means one *cell* per operation, and the cell
had just doubled. I wanted those bytes back, so I started trying other
ways of encoding the system. Below they are, in the order I tried them.

Everything here regenerates from the repository - ten systems, SOD32
and nine descendants, all passing the same 616-case ANS CORE corpus, and every table below
produced by the scripts named at the end.

```
: COUNT   DUP 1 + SWAP C@ ;        4-byte cells, from the real images

cell     25  0  0  0 |  9  0  0  0 |  1  0  0  0 | 93  0  0  0 | ...
         '--- DUP ---'  '--- LIT ---'  '---- 1 ----'  '---- + ----'
         7 cells x 4 bytes ....................................  28 bytes

token     6  0 |  2  0 |  1  0 | 23  0 |  7  0 | 10  0 |  1  0
          DUP     LIT      1       +      SWAP     C@     EXIT
         7 tokens x 2 bytes ...................................  14 bytes

CV8       6 | 120   1 |  7 | 79
          DUP    +1     SWAP  C@;EXIT ...........................  5 bytes

drawn to scale, one # per byte:

cell     ############################
token    ##############
CV8      #####
```

Some vocabulary. A **cell** is the machine word a Forth is built on -
four bytes on a 32-bit host, eight on a 64-bit one. **Threading** is how
a compiled word records what it calls: a list of references, walked at
run time, rather than machine code. The schemes below differ only in
what one of those references looks like.

Two more that the tables depend on. The **engine** is the C program that
fetches operations and runs them, a few thousand lines, compiled once.
The **image** is the compiled Forth system it runs: the dictionary,
every word body, the whole language. Only the image changes size between
the systems below. When I say "0.47x", I mean the image.

The systems have working names, used throughout:

| name | expansion | what it is |
|---|---|---|
| SOD32 | Stack Oriented Design, 32-bit | the ancestor: six 5-bit subinstructions packed per 32-bit cell |
| RelF | Relative Forth | direct threading with relative addresses: one host cell per operation, a call holding the distance to its target and a primitive its opcode |
| SOD16 | the ancestor's name, unit halved | one 16-bit token per operation, calls looked up in a table |
| CPT16 | Compressed-Pointer Threading, 16-bit | the same, but the call target is computed rather than looked up |
| CV8 | Compressed-pointer, Variable-length, 8-bit units | the same idea again, in a byte stream |

Every system here builds, boots, and passes the same 616-case test
corpus - the CORE word set of the ANS Forth standard. Ratios are against
RelF, so smaller is better, and each carries one standard error. Section
9 describes how they were taken and why it matters more than it sounds.

    tools/build-stages.sh      # every engine and image, both cell widths
    tools/run-tests.sh         # the corpus on all of them
    tools/collect-results.sh   # every table below

---

## 1. What 64-bit did

Take the top row of the figure above. `COUNT` compiles to seven
consecutive cells, one per operation, holding the values
`25 9 1 93 29 41 5`.

A cell here holds a **call** - the distance from itself to the word
being called - or a **primitive**, a small number saying which built-in
operation it is. Some operations are followed by an inline operand; the
`1` above is `LIT`'s.

The low bit distinguishes the two, and it is free: scaling the primitive
index by the cell size - 4 or 8, both powers of two - leaves the bottom
bits empty, so one is available to mark with. So `25` is
`1 + 6*4` with `DUP` at index 6, on a 4-byte build. On an 8-byte build
the same `DUP` cell reads 49.

Nothing in the image is an absolute address, so it can be loaded
anywhere - which was the point of the design.

Now count the bytes. Seven cells is 28 bytes on a 32-bit host and
**56 on a 64-bit one**, for a definition that has not changed. The
operation indices still fit in a byte; the cells holding them doubled.

That is RelF's bargain, and it is a fixed one: one host cell
per *operation*, whatever the host. Across the kernel it took the image
from 13,380 bytes to 24,320 for the same word set - the number from the
opening, and the reason for everything that follows.

The goal from here on is to stop paying twice for the same program
because the host got wider - and, since RelF existed to be fast, to do
it without giving the speed back.

The first thing that comes to mind is packing - which is exactly how
SOD32 saves its space.

## 2. Attempt one: pack operations into a cell, four bits each

One term before the attempts start. The **dispatch loop** is the part of
the engine that reads the next operation and jumps to the code for it.
Every scheme here is a different answer to "what does one operation look
like in memory", and every one of them is paid for in that loop.

SOD32 fits six operations into one cell. Nothing says a RelF cell has to
hold only one, so the first thing I tried was a packed format that would
work well at both cell widths: four-bit opcodes, which I will call
**PACK4**. A packed cell starts with a tag byte - a value the low-bit
test above can never produce, so packed and ordinary cells live side by
side in one image - and the rest of the cell holds opcodes:

```
  [tag][DUP][LIT][ + ][SWAP][C@ ][EXIT]     one packed cell
```

Four bits per opcode gives six of them in a 4-byte cell and fourteen in
an 8-byte one, which is why the format is worth having on both widths.
The price is the alphabet: four bits name only sixteen primitives, so
PACK4 packs the sixteen most common and leaves everything else as a
plain cell.

Measured on each system cross-compiling the Forth kernel:

    PACK4 image           21,296 bytes at 8-byte cells, 0.876x
    PACK4 kernel compile  1.13 at 8-byte cells, 1.14-1.18 at 4-byte

An eighth smaller and 13-18% slower. Not good, and the alphabet is why -
specifically, what it does to *runs*. A run is how many packable
operations come one after another before something unpackable interrupts
them, and it decides whether the tag byte pays for itself, since every
uninterrupted run needs one. A primitive outside the sixteen does not
just fail to pack: it **ends the run it is sitting in**, and both halves
then need a tag of their own.

## 3. Attempt two: pack operations into a cell, a byte each

So the next attempt widened the opcode to a byte - **PACK8**. Two
hundred and fifty-six values cover every primitive, so nothing falls
outside the alphabet any more. The price is fewer operations per cell:
seven in an 8-byte cell, but only three in a 4-byte one.

    PACK8 image           20,848 bytes at 8-byte cells, 0.857x
    PACK8 kernel compile  1.09 at 8-byte cells, 1.08-1.18 at 4-byte

Smaller than PACK4 despite the wider field - it folds away 433 cells
where PACK4 managed 377 - and slightly less slow. Still slower than the
plain cell engine, though, and still only an eighth smaller.

The reason is the same one a level down. Even with every primitive in
the alphabet, the runs are short: measured on real kernel code, the mean
run of consecutive packable operations is about 1.3. One tag byte to save
one opcode is not a saving. This kernel is mostly calls, and a call is
never packable. Whether that holds for Forth in general I cannot say from
one codebase, though the reason is not particular to it - calls are what
Forth is made of.

That was the end of packing.

## 4. Attempt three: a 16-bit token through a word table

If a cell is too wide, use a narrower unit. One 16-bit token per
operation: values below 256 are primitives, and 256+n means "the body of
the n'th word", looked up in a table of addresses the engine builds when
it loads the image. I called it SOD16, after the ancestor whose unit it halves.

This is the standard arrangement usually called token threading: the
reference in a compiled word is not an address but a number, and
something at run time turns the number into an address. A table is the
obvious something.

The image halved, 24,320 to 12,864 at 8-byte cells. And on the workload
this article measures things by, it was the worst system in the set:

    SOD16, kernel compile     1.378 (AMD, 8-byte)   1.364 (ARM, 4-byte)

Not uniformly worst, and the exception is interesting. On `parse.fth` -
4,000 lines of arithmetic typed at the interpreter - SOD16 runs at 1.023
where the packed schemes run at 1.07 and 1.13. That workload spends its
time inside kernel words that were already translated, where SOD16's
half-sized image starts paying for itself in cache. The table hurts when
you are *compiling*, which is when new calls have to be resolved; it
costs much less when you are only running what is already there.

On kernel compilation, though, it is 37% behind the cell engine it was
meant to improve on, and no other stage is close.

It cost more than the table lookup, too. The engine's table is enough to
*run* a program and not enough to *compile* one, and that asymmetry is
the whole of the problem.

```
        the engine's table                 the compiler's table
        number  ->  address                address  ->  number
   built at load, in C memory        built by the image, on the heap
   enough to RUN a program           needed to COMPILE one
                    \                        /
                     '--- opposite ways ----'

```

Running needs the first: token 256+n, look up entry n, jump there.
Compiling needs the second, because a dictionary search hands the
compiler an *address* and the instruction it must emit holds a *number*.
The engine's table cannot serve: it is indexed the wrong way round, and
it lives in the engine's own memory, which a Forth program has no way to
read. So the image builds and maintains an inverted copy of it, and
binary-searches that on every call it compiles. The table is also sized at load and never grows, so a
word defined afterwards has no number at all. That needed an escape
opcode carrying a full address.

It needed a second one for `DOES>`. `DOES>` is how Forth defines a word
that makes other words - the code after `DOES>` becomes the behaviour of
everything the defining word creates. So the address that has to be
jumped to sits in the *middle* of a definition, and a scheme whose only
name for anything is "word number n" cannot say that.

Concretely, compiling one call in SOD16 means: take the target address;
walk the image's own copy of the word list to find which word begins
there; binary-search a sorted array to turn that into a number; and if
the word was defined after load, give up and emit the escape form
instead. Compare that with CPT16's version in the next section, which is
one line of Forth.

## 5. Attempt four: delete the table

If the table is the problem, compute the address instead of looking it
up. Lay the words out so that a target is `base + (value << shift)`,
the same base-plus-scaled-index idea HotSpot uses for object references,
and the reason this one is called CPT16 - compressed-pointer threading, 16-bit unit. No
word-address table, so no second dependent load on the way to a call,
and the compiler's job becomes one line:

```forth
: CALL, ( a-addr --- )
  START @ - CPT-SHIFT RSHIFT 256 + OP, ;
```

Subtract the image base from the target, shift it down, and add 256
because tokens below that are primitives. No search and no second table.

    CPT16, kernel compile    1.035 ±0.033 (AMD, 8-byte cells)
                             1.024 ±0.021 (AMD, 4-byte)
                             1.007 ±0.016 (ARM, 4-byte)

Level with the cell engine, at the same image size as SOD16 - 12,864
bytes, identical to the byte. The kernel triggers neither of SOD16's
escapes: every call in it is to a word that existed at load time, and
the one `DOES>` is handled by its own opcode in both schemes. So the two
images encode the same operations in the same width and differ only in
what a call token means. Not faster, and not
slower either: 1.024 against 1.000, with an error of 0.021.

What that measures is a sum, and it is worth being precise about which.
CPT16 removes two things at once - the table lookup in the dispatch
loop, and the compiler's search from address back to word number. The
gap between SOD16 and CPT16 is 0.343 at 8-byte cells and 0.348 at
4-byte: about 34%. That is the measured cost of SOD16's table-based design on
kernel compilation, not the cost of a lookup.

What the sum does show is that a 16-bit unit is not itself a problem:
SOD16 and CPT16 use the same width, and one of them is level with the
cell engine. How that 34% divides between the dispatch-loop lookup and the
compiler's reverse map, I did not measure. The
bookkeeping had looked like free indirection; at least some of it was
not.

## 6. Attempt five: narrow the unit itself

Two lessons now point the same way. Packing failed because this kernel has no long runs. The word table
failed because the bookkeeping it forced on the compiler was expensive
and the lookup was not free either. The
remaining lever is the size of the unit - not how many operations share
a cell, and not how cleverly the target is computed, but how many bytes
one operation takes.

So: a byte stream. The name says why it is not simply "CPT8":
compressed-pointer, **variable-length**, 8-bit units. The compressed
pointer is inherited from CPT16 and the unit narrows from 16 bits to 8,
but the middle word is the real change. CPT16 is fixed-width - every
operation is one token, primitive or call. A byte cannot hold a call
target, so CV8 gives up fixed width, and is the first scheme here whose
operations are not all the same size.

One byte, one operation - if that operation is a primitive. Values under 0x80 are the 128 primitives.

A call cannot fit in a byte, so it does not try. A byte of 0x80 or more
means "this is a call", and the next bit down says how long it is: one
more byte after it, giving a 14-bit offset, or two more, giving 22 bits.
Operations are no longer all the same size.

One thing has not moved, and it matters later: the instructions are
byte-sized now, but their targets are still on the old cell grid. The
offset a call carries is scaled - it counts cells from the image base,
not bytes - so a call can still only name every eighth address, and
bodies are still padded so that they land on one. Section 8 is about
removing that.

For the dispatch loop that is a compare and a shift, no tag byte, and no
dependence on runs of anything.

The budget matters, and it ends up tight. Of the 128 values below 0x80:
68 are the kernel's primitives, five more are literal and data-word
forms, 23 are the folded pairs of section 7, and 24 are its specialised
opcodes. The highest value used is 119, leaving eight spare. That is
close enough that adding another family of specialisations would mean
choosing what to drop.
The general shape - a byte-coded stream with variable-length
instructions - is the one FCode and the Java virtual machine use. What
they name is different: an FCode token *is* a dictionary reference,
where a CV8 call carries an offset to a location.

    CV8, kernel compile    0.919 ±0.026 (AMD, 8-byte cells)
                           0.896 ±0.011 (ARM, 4-byte)
    CV8, image             11,416 bytes at 8-byte cells,
                           0.469x of cell threading

Faster and smaller than the cell engine. The figure at the top of this article is now readable
in full: `COUNT` as 28 bytes of cells, 14 of tokens and 5 of CV8, all
three dumped from the real images by `tools/show-word.sh`. In the CV8
row, `120` is an add-immediate opcode standing for "push 1, then add",
and `79` is a single opcode meaning "`C@`, then return" - the two tricks
section 7 is about.

## 7. Attempt six: give the common cases their own opcodes

Five bytes for six operations, in that CV8 line, is two separate tricks
working at once. Folding actually came earlier - I added it to CPT16,
which is the "CPT16 + folding" row in the table below - but both are
easiest to see in the CV8 line, so they are described together here.

**Folding**: a primitive immediately followed by `EXIT` becomes a single
opcode, which removes one trip round the dispatch loop from the end of a
great many definitions.

**Specialisation**: give the common case its own opcode. This is the old
bytecode trick - Smalltalk-80 spends bytecodes 16 to 31 on "push
temporary variable n", Lua carries small operands inside the
instruction - rather than CPython 3.11's adaptive specialisation, which
rewrites opcodes at run time from observed types. Everything here is
decided at compile time. Small integers get one each, so do the hottest kernel words,
and so does an operand small enough to travel inside the instruction
rather than after it - `1 +` becoming a single add-immediate.

| stage | kernel compile (AMD, 8-byte) | image | vs cell |
|---|---|---|---|
| cell | 1.000 ±0.037 | 24,320 | 1.000 |
| CPT16 | 1.035 ±0.033 | 12,864 | 0.529 |
| CPT16 + folding | 0.897 ±0.027 | 12,696 | 0.522 |
| CV8 | 0.919 ±0.026 | 11,416 | 0.469 |
| CV8 + specialisation | 0.688 ±0.019 | 11,088 | 0.456 |

One row in that table goes the wrong way and should not be glossed over:
CV8 is *slower* than folded CPT16, 0.919 against 0.897. That gap is
smaller than either figure's error bar, so on its own it would be
nothing - but it has the same sign in every column measured, +0.022 at
8-byte cells on AMD, +0.019 at 4-byte, +0.016 on ARM. Three independent
measurements agreeing in direction is worth more than one of them
agreeing with itself.
Narrowing the unit to a byte does not come free - a call stops being one
fixed token and becomes two bytes to assemble. What it buys is 10% of
the image. It is a trade, and the sequence is only worth it because of the row
underneath.

The specialised opcodes are the larger step on x86, and by a lot. Take
the ladder in two halves - cell threading down to CV8, then CV8 down to
CV8 with the opcodes - and subtract:

| | cell -> CV8 | CV8 -> +spec |
|---|---|---|
| AMD, 8-byte | 0.081 | 0.231 |
| AMD, 4-byte | 0.062 | 0.264 |
| ARMv7, 4-byte | 0.104 | 0.107 |

Three to four times on x86. On ARM the two come out the same size to within their error bars, which
are ±0.011 and ±0.008 on the stages involved, so there they are
indistinguishable rather than ranked. Both steps help on both
machines; how much bigger one is than the other does not travel, and I
would not have known that from a single machine.

Those are sequential deltas along one path, not a ranking of techniques.
I never tried specialising CPT16, or adding opcodes before narrowing the
unit, so I have no measurement of what the same work would be worth in
another order. Several of these opcodes exist only because a byte stream
has a one-byte space to put them in. What the numbers
support is narrower and still worth knowing: on this path the last step
was the cheap one, and it took five attempts to build somewhere to put
it.

Not all five of them earn their place; section 10 has the accounting.

## 8. Attempt seven: the last place cell width was still being paid

At this point the token stream is the same size at both cell widths -
the same program either way. But the 64-bit image was still 2,980 bytes
larger than the 32-bit one. Measured, that was: 1,088 bytes of
dictionary link cells, 496 of padding to align names, 660 of padding to
align the end of each code body, and the rest data.

None of that is code. It is the dictionary *header*, which the whole
encoding exercise had never touched.

So the link became a distance, 1 to 3 bytes, with
its tag byte last so that it decodes read backwards from the name the
same way a call decodes read forwards. Names stopped being padded, code
bodies stopped being padded, and calls became able to name any byte
rather than only every eighth one.

    image, 8-byte cells    11,088 -> 7,609     0.456x -> 0.313x
    image, 4-byte cells     8,108 -> 6,749     0.606x -> 0.504x

The largest single size result in the sequence, and it came from the
part of the system that is not the instruction encoding at all.

The 860 bytes still separating the two widths break down as:

    408   data fields - cells, because a VARIABLE holds a cell
    273   seventeen inline operands still cell-sized, plus the
          padding they force on the bodies around them
    156   a wordlist table
     23   the boot prologue and the links themselves

Only the 273 is worth chasing - and it is worth saying what those
seventeen operands are, because it is the one thing that makes them
interesting. They are control flow and its relatives: five `(DO)`/`(LOOP)`
offsets and twelve execution tokens from `[']` and `POSTPONE`. Branches
themselves are fine - a conditional branch in CPT16 or CV8 carries a
signed 16-bit offset counted from the operand, which no definition in
this kernel comes close to exhausting. It is the loop and token operands
that were left cell-sized, because the loop runtime reads its own with a
single aligned fetch and making it byte-granular would put decode work
in the inner loop of every `DO`.

It is not free, either, and the cost lands where the design says it
should - on dictionary search, because a variable-length link is more
work to walk than a cell.

All at 4-byte cells, where both machines build:

| workload | AMD | ARMv7 |
|---|---|---|
| kernel compile | +0.056 | +0.046 |
| corpus | +0.086 | +0.085 |
| parse | +0.119 | +0.101 |

At 8-byte cells on the AMD machine the kernel-compile cost is +0.039.

Reproduced across three separate builds on the AMD machine and two on
the ARM board; the corpus figure repeats to a thousandth. It is a size
optimisation that costs time, on both architectures, and anyone adopting
it should know which of the two they are buying.

So the sequence ends on a trade rather than a win: 0.31x the image, 0.73
the time on kernel compilation, and a measurably slower dictionary.

## 9. How this was measured

Everything was built and tested on three machines - a single-core
x86-64 virtual machine, a 16-core x86-64 laptop and a 4-core ARMv7
board - but only two of them are quoted here. The VM is the container
this work was done in; it is too noisy to resolve anything and its
figures are not in `results/`. Every number in this article comes from
the laptop or the board.

The headline benchmark is each system **cross-compiling the Forth
kernel**: reading the kernel's Forth source and writing out a fresh
image, the largest piece of real work any of them does. It exercises the
text interpreter, the compiler and the dictionary at once, and it cannot
favour an encoding by what it produces, because every system writes the
same cell-format image - what differs is the code doing the writing.

It doubles as the correctness check. The image produced must be
byte-identical to the reference before any timing is recorded, so
correctness and speed come out of the same run and a system that is fast
because it is quietly wrong fails the comparison that times it.

PACK4 and PACK8 are the exception here: they are produced by rewriting
a finished cell image, so they run packed code but compile new
definitions as plain cells. Every other system compiles in its own
encoding.

Three things about how the numbers were taken.

**The variation is per-build.** Repeated runs of the same
binaries agree to 1-2%. Rebuild the tree and a stage moves by five or
ten percent, because where the compiler places code is worth that much
and is fixed for a given binary. Taking the minimum over more
repetitions measures that bias more precisely rather than removing it.
So every engine is built several ways - five on the laptop, three on
the slower board - with flags that only move code; all are timed, and
the figure is the mean with a standard error.

**The quiet machine measured better than the fast one.** On the 16-core
laptop, the spread between identical builds of one engine read 5.3% in
one run and 13.1% in the next;
the ARM board, four slow cores with nothing else running, resolves to
about 1%.

**Two benchmarks had to be thrown away.** A counted-loop microbenchmark
swung 21% between runs of the same binary on the same machine; a
recursive Fibonacci swung 15-23%. Both are the short, narrow ones. Both
surviving workloads run a lot of varied code. A tight interpreter loop
over a handful of opcodes is dominated by indirect-branch prediction and
code placement, which is exactly what varies between builds - so it
the build is what it measures.

Every conclusion above survived being measured twice on both
machines.

## 10. Not measured

- Two machines is not a study. One x86-64 laptop and one ARMv7 board;
  nothing with a different memory order, and nothing without an
  operating system underneath.
- Nothing here measures pure execution reliably, since both
  microbenchmarks failed reproducibility.
- Not all five specialisations earn their place. Measured by what each
  saves on its own: small integers 190 bytes, hot kernel words 194,
  immediate operands 111. Those overlap, so they do not sum to the 328
  the image actually moved. The other two are worse than that. Locals
  are inert - `locals.4` is loaded only into the shell image, so the
  kernel every benchmark runs has none to specialise - and the variable
  specialisation makes the image 18 bytes *larger* for no measurable
  time. Both were left switched on so the published figures match what
  the repository builds.
### What token threading takes away

The last limitation is the largest, and it is a direct consequence of
the thing that made the image small.

In a cell-threaded Forth, the first field of a word points at the code
that runs it, so a program can invent a new *kind* of word - a new
behaviour, not just a new definition - by writing a new code field.
Several classic Forth techniques rest on that.

In SOD16 and CPT16 a call names a word, and in CV8 it names an address
that some word begins at. Neither can name a behaviour. `DOES>` survives
only because it was given an opcode of its own, and it is the only
extension point left: a new behaviour type cannot be added from Forth
any more, only from C. That is the strongest architectural criticism
this design has had, it is a direct consequence of the thing that made
the image small, and I do not have an answer to it.

## 11. What came out of it

```
Forth image, 8-byte cells                              bytes  vs cell

cell (RelF)           ##############################  24,320  1.000
PACK4                 ##########################      21,296  0.876
PACK8                 ##########################      20,848  0.857
SOD16                 ################                12,864  0.529
CPT16                 ################                12,864  0.529
CPT16 + folding       ################                12,696  0.522
CV8                   ##############                  11,416  0.469
CV8 + spec            ##############                  11,088  0.456
CV8 + byte headers    #########                        7,609  0.313

The last row is the dictionary header, not the instruction encoding.
```

Start and finish, same Forth, same 616 tests passing:

| | image | kernel compile | parsing |
|---|---|---|---|
| RelF, where this began | 24,320 bytes | 1.000 | 1.000 |
| CV8 + specialisation + byte headers | 7,609 bytes | 0.731 | 0.799 |

One property survived the whole sequence untouched: every image here is
still position-independent. CPT16 and CV8 both compute call targets from
the image base, so an image still loads at any address, which was the
reason RelF existed in the first place.

All three columns at 8-byte cells: 0.31x the image and 0.73 the time on
the compiler's own largest job, at the price of 20% on text
interpretation. At 4-byte cells, where RelF started life, the same
sequence gives 0.50x the image, 0.73 on kernel compilation and 0.83 on
parsing.

Six things I would tell someone starting the same work.

**A tag-based packing scheme needs long runs of packable operations, and
this kernel has not got them.** The mean run here is about 1.3, so the
tag byte never gets to amortise. I would expect that of Forth generally,
since calls break runs and Forth is mostly calls, but one kernel is not
a language.

**Using the cell harder failed; dropping it as the unit of encoding
worked.** The price was variable-length instructions, which is a real
cost in decoder complexity and was worth paying here.

**A table imposes costs outside the dispatch loop.** Removing the
word-number table and the bookkeeping it forced on the compiler was
worth 34% between them. Which of the two mattered more, I did not
measure.

**Ask early whether the common cases could have their own opcodes.** On
the path measured here, adding them improved kernel compilation three to
four times as much as the cell-to-CV8 transition before it on x86, and
about equally on ARM. I never tried them in any other order, so this
compares two steps in one sequence.

**Look outside the instruction stream.** The dictionary header, which
none of the encoding work had touched, was the largest single size
result in the sequence.

**If code placement affects your benchmark, account for build-to-build
variation.** Here a rebuild moved a result five or ten percent and
repeating a run could not see it.

## What still bothers me

Two things, in case somebody reading this knows better.

**The 34%.** CPT16 removes the word-number table and the compiler's
reverse map at the same time, so I know what the pair cost and not what
either cost alone. I could not think of a way to separate them without
building a third system that keeps the table and drops the reverse map,
which is a system nobody would want.

**The 273 bytes.** Seventeen operands in the kernel are still cell-sized
- five loop offsets and twelve execution tokens - and they force the
bodies around them to stay aligned. Making them byte-granular is
straightforward except for `(LOOP)`, which reads its operand with a
single aligned fetch in the inner loop of every `DO`. A 16-bit unaligned
fetch primitive would fix it. I have not built it, and I am not certain
it is worth the opcode.

The repository is at REPO_URL, everything in it builds with two
commands, and I would rather be corrected in the comments than be wrong
quietly.

## References

- Brad Rodriguez, [*Moving Forth*, part 1](https://www.bradrodriguez.com/papers/moving1.htm)
- R.G. Loeliger, *Threaded Interpretive Languages*, Byte Books, 1981
- L.C. Benschop, [SOD32](https://github.com/lennart-benschop/sod32),
  vendored here at a pinned revision, GPLv2
- ForthHub discussion #187, ["An elevator description for Forth's threaded code models?"](https://github.com/ForthHub/discussion/discussions/187), whose vocabulary this article uses
- IEEE 1275-1994, the Open Firmware standard, whose FCode is a byte-coded
  Forth: one-byte codes `0x10`-`0xFE`, escape band
  `0x01`-`0x0F` for two-byte codes. CV8 took the idea of a byte stream
  with an escape, not the layout - it splits on the top bit and has a
  single escape opcode, and FCode has no call band because an FCode
  token *is* a dictionary reference.
- Named in the source where borrowed: HotSpot's compressed object
  pointers for `base + (v << shift)`; CPython 3.11 (PEP 659, the
  specialising interpreter), which is adaptive where this project's
  specialisation is static; Lua 5.4 for immediate operands; the Java
  virtual machine's `iload`, CPython `LOAD_FAST` and Smalltalk-80's
  bytecodes 16-31 for locals as opcodes;
  Titzer's in-place Wasm interpreter for interpreting the compact form
  rather than expanding it at load.
