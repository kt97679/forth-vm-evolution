# Making a Forth virtual machine smaller: six attempts, two of which failed

In 2004, out of curiosity rather than need, I forked L.C. Benschop's
SOD32 - the Stack Oriented Design, a 32-bit virtual machine with a Forth
on top - threw away its packed instruction format, and replaced it with
one relative offset per cell. I called the result RelF, for Relative Forth. The point was
speed: a cell you can jump through directly beats six 5-bit
subinstructions you have to unpack first. It was 32-bit only, and it sat there working. Whether it was actually faster than what it forked
from, I did not check at the time - a detail that comes back in section
8.

Recently I came back to it and built it for 64-bit. The deal changed:
the same Forth, the same words, in an image that had gone from 13,380
bytes to 24,320. One relative offset per cell means one *cell* per
operation, and the cell had just doubled.

What follows is what I tried, in the order I tried it, including the two
attempts that did not work and why.

Some vocabulary first. A **cell** is the machine word a Forth is built on -
four bytes on a 32-bit host, eight on a 64-bit one - and it is the unit
Forth uses for everything from stack items to dictionary pointers.
**Threading** is how a compiled Forth word records what it calls: a list
of references, walked by the engine, rather than machine code. The
schemes below differ only in what one of those references looks like.

The **engine** is the C program
that fetches operations and runs them - a few thousand lines, compiled
once. The **image** is the compiled Forth system it runs: the dictionary,
every word body, the whole language. Only the image changes size between
the systems below; the engine changes only in how it decodes what it
reads. When I say "0.47x", I mean the image.

The **dispatch loop** is the part of the engine that reads the next
operation and jumps to the code for it. Every scheme here is a different
answer to "what does one operation look like in memory", and every one
is paid for in that loop.

One more, needed late: Forth has an **inner** interpreter, the dispatch
loop that runs compiled words, and an **outer** interpreter, the part
that reads text, looks each word up in the dictionary and either runs or
compiles it. Everything in sections 2 to 7 is about the inner one.
Section 8 is about the outer one.

The systems have working names, used throughout:

| name | expansion | what it is |
|---|---|---|
| SOD32 | Stack Oriented Design, 32-bit | the ancestor: six 5-bit subinstructions packed per 32-bit cell |
| RelF | Relative Forth | one host cell per operation; a call holds the distance to its target, a primitive holds its opcode |
| PACK4, PACK8 | packed, 4- or 8-bit opcodes | RelF with several opcodes packed into a cell |
| SOD16 | the ancestor's name, unit halved | one 16-bit token per operation, calls looked up in a table |
| CPT16 | Compressed-Pointer Threading, 16-bit | the same, but the call target is computed rather than looked up |
| CV8 | (the 8 is the unit width in bits) | the same idea again, in a byte stream |

CV8 rather than "CPT8" because the step is not just a narrower unit.
CPT16 is fixed-width - every operation is one 16-bit token, primitive or
call. A byte cannot hold a call target, so CV8 gives that up: an opcode
is one byte, a call is two or three. It is the first scheme here where
operations are not all the same size.

Every system named here builds, boots, compiles its own encoding and
passes the same 616-case test corpus - the CORE word set of the ANS
Forth standard, 616 assertions about what each word must do. The tables
come out of the repository, not out of a model.

    tools/build-stages.sh      # every engine and image, both cell widths
    tools/run-tests.sh         # the corpus on all of them
    tools/collect-results.sh   # every table below

The headline benchmark is each system **cross-compiling the Forth
kernel**: reading the kernel's Forth source and writing out a fresh
image, which is the largest piece of real work any of them does. It
exercises the text interpreter, the compiler and the dictionary at once,
and it cannot favour an encoding by what it produces, because every
system writes the same cell-format image; the code doing the writing is
in the encoding under test. It doubles as the correctness check,
described in section 9.

Ratios are against RelF, the cell engine, so smaller is better. They
carry one standard error, measured across several differently-laid-out
builds of each engine. Section 9 says why that is done, and what it
costs to skip.

---

## 1. What 64-bit did

Here is what RelF's encoding actually looks like. This definition:

```forth
: COUNT   DUP 1 + SWAP C@ ;
```

compiles to seven consecutive cells - this is a 4-byte build - holding
these values:

```
   25    9    1   93   29   41    5
  DUP  LIT   1    +   SWAP  C@  EXIT
```

A cell here holds a **call** - the distance from itself to the word
being called - or a **primitive**, a small number saying which built-in
operation it is. Some operations are followed by an inline operand; the
`1` above is `LIT`'s.

The low bit distinguishes the two, and it is free because the primitive
index is scaled by the cell size before the bit is added. So `25` is
`1 + 6*4` with `DUP` at index 6, on a 4-byte build. On an 8-byte build
the same `DUP` cell reads 49.

Nothing in the image is an absolute address, so it can be loaded
anywhere - which was the point of the design.

Now count the bytes. Seven cells is 28 bytes on a 32-bit host and
**56 on a 64-bit one**, for a definition that has not changed. The
operation indices still fit in a byte; the cells holding them doubled.

That is cell threading's bargain and it is a fixed one: one host cell
per *operation*, whatever the host. Across the kernel it took the image
from 13,380 bytes to 24,320 for the same word set - the number from the
opening, and the reason for everything that follows.

The goal from here on is to stop paying twice for the same program
because the host got wider - and, since RelF existed to be fast, to do
it without giving the speed back.

The obvious first thought is that this is SOD32's problem, and SOD32
already solved it by packing.

## 2. Attempt one: pack several operations into a cell

SOD32's trick is that a cell holds six operations, not one. Nothing says
a RelF cell has to hold one either.

So: reserve the first byte of a cell as a tag marking it as packed, and
fill the rest with opcodes. Instead of the seven cells above, `COUNT`
would want something closer to

```
  [tag][DUP][LIT][ + ][SWAP][C@ ][EXIT]     one 8-byte cell
```

At 8-byte cells that is up to seven byte-sized opcodes in the space one
operation used to take (PACK8), or up to fourteen if an opcode is only
four bits (PACK4). A four-bit field reaches sixteen primitives, so PACK4
gets an alphabet of the sixteen most common; anything else stays a plain
cell.

I had costed both earlier in this work and rejected them, on a synthetic
benchmark that ran each dispatch loop over a stream of opcodes and
compared the time to cell threading. It said the packed schemes would
take 1.90 and 2.05 times as long - that is, 90% and 105% slower to run
the same program. On that basis I did not build them. This time I did.

Measured on real work - each system cross-compiling the Forth kernel -
across three machines, as a ratio of time to the cell engine:

Ranges in the 4-byte column are across the two machines that build it.

| | predicted | 8-byte cells | 4-byte cells |
|---|---|---|---|
| PACK4, 4-bit opcodes | 2.05x | 1.13 | 1.14-1.18 |
| PACK8, 8-bit opcodes | 1.90x | 1.09 | 1.08-1.18 |

So the rejection was right and the recorded reason for it was wrong by
between five and twelve times, depending which column you take: a
predicted penalty of 90-105%, against a measured 9-18%.
The old benchmark's own header said why, in advance: its streams were
sized to run hot, so it measured decode cost with memory free, which it
called the pessimistic case. Pessimistic by four times, as it turned
out. The baseline it lost to was wrong too - token threading had been
recorded at 0.985, faster than cell dispatch, from a benchmark running a
32-megabyte stream against a 2-megabyte level-2 cache. It was measuring
memory traffic.

The other failure is the one worth reporting, and only building it
showed it. Counting on paper, PACK4 and PACK8 came out level, both at 0.76x - the
narrower field should pack twice as many operations per cell, which
ought to offset having fewer of them to choose from. Built, PACK4 folds
away *fewer* cells - 377 against 433 - and produces the **larger**
image: 21,296 bytes against 20,848, at 8-byte cells.

The reason is the sixteen-opcode alphabet. A primitive outside it does
not merely fail to pack: it **ends the run it is sitting in**, and both
halves then need their own tag byte.

A run, here, is how many packable operations occur one after another
before something unpackable interrupts them - and it is what decides
whether the tag byte pays for itself. Measured on real kernel code, the
mean run is about 1.3. One tag byte to save one opcode is not a saving.

So packing needs long runs of packable operations, and this kernel has
not got them - it is mostly calls, and a call is never in the alphabet.
Whether that is true of Forth generally I cannot say from one codebase,
though the reason is not specific to this one: calls are what Forth is
made of.
Counting on paper priced the fields and got 0.76x. Built, the program
paid for the joins as well and got 0.86x, while running 10-18% slower,
which ended that line of attack.

## 3. Attempt two: a 16-bit token through a word table

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

It cost more than the table lookup, too, and the reason is a direction
problem. There are two tables, pointing opposite ways:

    the engine's      number -> address    built at load, in C memory
    the compiler's    address -> number    built by the image, on the heap

The engine's is the one that makes the encoding work: token 256+n, look
up entry n, jump there. That is enough to *run* a program. It is not
enough to *compile* one. A compiler that has just parsed a name has
found the word's address - that is what a dictionary search returns -
and now needs the number to emit, which is the opposite direction. The
engine's table cannot help even in principle: it is indexed by number,
and it lives in the engine's own memory, which the Forth program has no
way to read. So the image builds and maintains a second, inverted copy
of it, and binary-searches that on every call it compiles. The table is also sized at load and never grows, so a
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

## 4. Attempt three: delete the table

If the table is the problem, compute the address instead of looking it
up. Lay the words out so that a target is `base + (value << shift)`,
which is what HotSpot does for object references and why this one is
called CPT16 - compressed-pointer threading, 16-bit unit. No
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
bytes, identical to the byte, because the two encode the same operations
in the same width and differ only in what a call token means. Not faster, and not
slower either: 1.024 against 1.000, with an error of 0.021.

What that measures is a sum, and it is worth being precise about which.
CPT16 removes two things at once - the table lookup in the dispatch
loop, and the compiler's search from address back to word number. The
gap between SOD16 and CPT16 is 0.343 at 8-byte cells and 0.348 at
4-byte: about 34%, and that is what the two cost together.

What the sum does show is that a 16-bit unit is not itself a problem:
SOD16 and CPT16 use the same width, and one of them is level with the
cell engine. How that 34% divides between the dispatch-loop lookup and the
compiler's reverse map, I did not measure. The
bookkeeping had looked like free indirection; at least some of it was
not.

## 5. Attempt four: narrow the unit itself

Two lessons now point the same way. Packing fails because Forth code has
no long runs. Dispatcher logic fails because it costs what it costs. The
remaining lever is the size of the unit - not how many operations share
a cell, and not how cleverly the target is computed, but how many bytes
one operation takes.

So: a byte stream. One byte, one operation - if that operation is a
primitive. Values under 0x80 are the 128 primitives.

A call cannot fit in a byte, so it does not try. A byte of 0x80 or more
means "this is a call", and the next bit down says how long it is: one
more byte after it, giving a 14-bit offset, or two more, giving 22 bits.
Operations are no longer all the same size.

The offset is scaled, not absolute - it counts cells from the image
base, not bytes - so at this stage a call can still only name every
eighth address, and bodies are still padded to suit. Section 7 is about
removing that.

For the dispatch loop that is a compare and a shift, no tag byte, and no
dependence on runs of anything.
The general shape - a byte-coded stream with variable-length
instructions - is the one FCode and the Java virtual machine use. What
they name is different: an FCode token *is* a dictionary reference,
where a CV8 call carries an offset to a location.

    CV8, kernel compile    0.919 ±0.026 (AMD, 8-byte cells)
                           0.896 ±0.011 (ARM, 4-byte)
    CV8, image             11,416 bytes at 8-byte cells,
                           0.469x of cell threading

The first scheme in the sequence that beat the cell engine on both size
and speed at once. Here is the same definition in each encoding, dumped from the real
images at 4-byte cells by `tools/show-word.sh`:

```
: COUNT   DUP 1 + SWAP C@ ;

cell     25 9 1 93 29 41 5      7 cells x 4  = 28 bytes
token    6 2 1 23 7 10 1        7 tokens x 2 = 14 bytes
CV8      6 120 1 7 79                          5 bytes
```

`120` is an add-immediate opcode standing for "push 1, then add", and
`79` is a single opcode meaning "`C@`, then return".

## 6. Attempt five: give the common cases their own opcodes

Look again at the CV8 line of that dump: five bytes for six operations.
Two separate tricks are doing that, and each is worth having on its own.
This section is both of them, because they were built together.

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
CV8 is *slower* than folded CPT16, 0.919 against 0.897, on both machines.
Narrowing the unit to a byte does not come free - a call stops being one
fixed token and becomes two bytes to assemble. What it buys is 10% of
the image. It is a trade, and the sequence is only worth it because of the row
underneath.

Because on this machine the specialised opcodes are worth more than the
encodings that carried them. Taking the ladder as deltas of the ratio,
cell threading down to CV8 against CV8 down to CV8+specialisation:

| | cell -> CV8 | CV8 -> +spec |
|---|---|---|
| AMD, 8-byte | 0.081 | 0.231 |
| AMD, 4-byte | 0.062 | 0.264 |
| ARMv7, 4-byte | 0.111 | **0.101** |

Three to four times on x86. On the ARM board, slightly *less* than the
encoding work - and that is the machine section 9 says resolves best.
Both steps help everywhere; which of them is the bigger one is not
portable, and I would not have known that from one machine.

Those are sequential deltas along one path, not a ranking of techniques.
I never tried specialising CPT16, or adding opcodes before narrowing the
unit, so I have no measurement of what the same work would be worth in
another order. Several of these opcodes exist only because a byte stream
has a one-byte space to put them in. What the numbers
support is narrower and still worth knowing: on this path the last step
was the cheap one, and it took five attempts to build somewhere to put
it.

Measured by bytes each saves on its own, small integers are worth 190,
the hot kernel words 194 and immediate operands 111. Those do not add up
to the 328 bytes the image actually moved: they overlap, and one more
specialisation I left switched on - giving variables their own opcodes -
makes the image 18 bytes *larger* while doing nothing measurable for
speed.

## 7. Attempt six: the last place cell width was still being paid

At this point the token stream is the same size at both cell widths -
the same program either way. But the 64-bit image was still 2,980 bytes
larger than the 32-bit one. Measured, that was: 1,088 bytes of
dictionary link cells, 496 of padding to align names, 660 of padding to
align the end of each code body, and the rest data.

None of that is code. It is the dictionary *header*, which the whole
encoding exercise had never touched.

So the link became a distance rather than an address, 1 to 3 bytes, with
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

Only the 273 is worth chasing.

It is not free, either, and the cost lands where the design says it
should - on dictionary search, because a variable-length link is more
work to walk than a cell.

| workload | AMD | ARMv7 |
|---|---|---|
| kernel compile | +0.056 | +0.047 |
| corpus | +0.086 | +0.071 |
| parse | +0.119 | +0.099 |

Reproduced across three separate builds on the AMD machine and two on
the ARM board; the corpus figure repeats to a thousandth. It is a size
optimisation that costs time, on both architectures, and anyone adopting
it should know which of the two they are buying.

So the sequence ends on a trade rather than a win: 0.31x the image, 0.73
the time on kernel compilation, and a measurably slower dictionary.

## 8. The premise I never checked

One thing remained, and it is the part of this exercise I would most
like other people to avoid repeating.

RelF existed to be faster than SOD32 - that was the reason for the fork
- and at the end I ran the two side by side, which I had never done:
not in 2004, and not once in all the work above.

SOD32 was twice as fast as RelF on the test corpus and 2.9 times as fast
at interpreting text.

It was also *slower* than RelF on the one benchmark that is almost pure
inner interpreter - the counted loop - which is how I knew the problem
was not the VM. That detail matters for the premise, and not in my
favour: RelF was forked to make the inner interpreter faster, and the
benchmarks that could settle whether it did are the two this project
threw out for not reproducing. The 2004 claim is not vindicated here. It
is still unchecked.

The cause took an afternoon. SOD32's dictionary is 32 hashed chains,
selected on the first two characters of a name. RelF's was a single
chain walked from the top. I had dropped the hash while changing the
link fields from absolute to relative in 2004 and never went back to see
what it cost. It costs most on *numbers*, which are never found and so
pay a complete traversal before the interpreter gives up and converts
them - and in `parse.fth`, which is 4,000 lines of interpreted
arithmetic, about half the tokens are numbers. Ordinary source is less
extreme, but every number in it pays the same full traversal.

Restored, with SOD32's hash function unchanged:

    dictionary entries visited, same input     before  8,052,823
                                                after    288,037
                                                SOD32    397,720

Those are counts, so they are the same on every machine. In
time it was 3.7x on parsing at 4-byte cells and 4.4x at 8-byte. The
whole encoding sequence in this article is worth about 0.69. One
omission, restored, was worth more than all of it.

Hashing a dictionary is not an insight and SOD32 already did it, so the
fix is not the interesting part. Why nobody noticed is: every benchmark in this project compared the system against
itself - against the previous stage, against last week's build - never
against the thing it was forked from to beat. The fault went in in 2004
and sat there until this year, and the ancestor was in a tarball the
whole time.

It also means everything above was tuning a system that was
carrying a 4x handicap in its text interpreter throughout. All the
ratios in this article were measured after the fix.

If you have a project with a parent, go and run the parent.

## 9. How this was measured

Three machines: a single-core x86-64 virtual machine, a 16-core x86-64
laptop, and a 4-core ARMv7 board. Every stage cross-compiles the kernel and the output
image must be byte-identical to the reference *before* the timing is
recorded, so correctness and speed are the same run: a stage that is
fast because it is quietly wrong fails the comparison that times it.

Three things about how the numbers were taken.

**The variation is per-build, not per-run.** Repeated runs of the same
binaries agree to 1-2%. Rebuild the tree and a stage moves by five or
ten percent, because where the compiler places code is worth that much
and is fixed for a given binary. Taking the minimum over more
repetitions measures that bias more precisely rather than removing it.
So every engine is built five ways with flags that only move code, all
five are timed, and the figure is the mean with a standard error. The
widest spread of any stage was the *baseline* at 12.6% - the number that
divides every ratio in every table.

**The quiet machine measured better than the fast one.** The 16-core
laptop's resolution floor read 5.3% in one run and 13.1% in the next;
the ARM board, four slow cores with nothing else running, resolves to
about 1%.

**Two benchmarks had to be thrown away.** A counted-loop microbenchmark
swung 21% between runs of the same binary on the same machine; a
recursive Fibonacci swung 15-23%. Both are the short, narrow ones. Both
surviving workloads run a lot of varied code. A tight interpreter loop
over a handful of opcodes is dominated by indirect-branch prediction and
code placement, which is exactly what varies between builds - so it
the build is what it measures.

Every conclusion above survived being measured twice on at least two
machines. Several earlier ones did not, and are not above.

## 10. Not measured

- Three machines is not a study. Two x86-64 and one ARMv7; nothing with
  a different memory order, and nothing without an operating system
  underneath.
- Nothing here measures pure execution reliably, since both
  microbenchmarks failed reproducibility.
- The locals specialisation is inert in these images: `locals.4` is
  loaded only into the shell image, so the kernel that every benchmark
  runs has no locals to specialise. The variable specialisation is not
  inert but is not a gain either - it costs 18 bytes and no measurable
  time. Both were left switched on so the published figures match the
  build the repository produces.
(The one remaining limitation is large enough to have its own section,
below.)

## 11. What token threading takes away

In a cell-threaded Forth, the first field of a word points at the code
that runs it, so a program can invent a new *kind* of word - a new
behaviour, not just a new definition - by writing a new code field.
Several classic Forth techniques rest on that.

Under every token scheme here, a call names a word and nothing else.
`DOES>` remains, because it was given its own escape, but it is the only
extension point left: a new behaviour type cannot be added from Forth
any more, only from C. That is the strongest architectural criticism
this design has had, it is a direct consequence of the thing that made
the image small, and I do not have an answer to it.

## 12. What came out of it

Start and finish, same Forth, same 616 tests passing:

| | image | kernel compile | parsing |
|---|---|---|---|
| RelF, where this began | 24,320 bytes | 1.000 | 1.000 |
| CV8 + specialisation + byte headers | 7,609 bytes | 0.731 | 0.799 |

All three columns at 8-byte cells: 0.31x the image and 0.73 the time on
the compiler's own largest job, at the price of 20% on text
interpretation. At 4-byte cells, where RelF started life, the same
sequence gives 0.50x the image, 0.73 on kernel compilation and 0.83 on
parsing.

Set against that: restoring one hash table that had been missing since
2004 was worth 3.7 to 4.4x on parsing by itself. Everything in the
sequence above is a fraction; that one omission was a multiple.

That does not make the encoding work pointless. The two are
independent. The hash sits in the text
interpreter and has no effect on image size at all, so the whole size
result stands untouched by it; and every speed ratio in this article was
measured after the fix, on a system with the hash in place. What the
comparison does say is something about priorities: I spent months on the
part I found interesting and had never checked the part that was
already, demonstrably, three times worse.

Seven things I would tell someone starting the same work.

**Packing needs runs, and this kernel has not got them.** The mean run
of consecutive packable primitives here is about 1.3, so a scheme that
pays a tag byte to amortise over a run never gets to amortise. I would
expect that of Forth code in general, because calls break runs and Forth
is mostly calls - but I have measured one kernel, not a language.

**Fitting more into a cell failed twice; making the cell irrelevant
worked.** Both rejected attempts kept the cell and tried to use it
harder. What worked was dropping it as the unit of encoding altogether,
and accepting variable-length instructions to do it. That is one
kernel's answer, and it follows from this kernel's call density rather
than from anything about Forth as a language.

**A table costs more than its lookup.** The word-number table looked
like free indirection. Removing it and the bookkeeping it forced on the
compiler was worth 34% between them - and nothing in this experiment
separates the two, so I cannot tell you what the dispatch-loop half
alone was worth.

**Ask early whether the common cases could have their own opcodes.** On
x86 that step was worth three to four times the whole encoding sequence
that preceded it; on ARM it was worth slightly less than it. The size of
the win did not travel between machines, which is itself worth knowing
before planning around it.

**Look outside the instruction stream.** Changing the dictionary header
took the image from 11,088 bytes to 7,609, and none of the encoding
work had touched it. Before that change, three quarters of what
cell width still cost - links, name padding, body padding - was
dictionary structure rather than code. Afterwards the largest remaining
item is the parameter fields of data words, which are cells because they
have to be.

**Measure builds, not just runs.** Rebuilding the same source moves a
result by five or ten percent, because code placement is worth that and
is fixed for a given binary; repeating a run cannot see it. Build each
thing several ways and quote the spread. On this project the widest such
spread belonged to the *baseline*, which divides every ratio.

**Run the parent.** If your project was forked from something, measure
against that something, not only against your own last build. It is the
one check here that found a problem larger than everything the project
set out to do.

## References

- Brad Rodriguez, *Moving Forth*, part 1 -
  <https://www.bradrodriguez.com/papers/moving1.htm>
- R.G. Loeliger, *Threaded Interpretive Languages*, Byte Books, 1981
- L.C. Benschop, SOD32 - <https://github.com/lennart-benschop/sod32>,
  vendored here at a pinned revision, GPLv2
- ForthHub discussion #187, "An elevator description for Forth's
  threaded code models?", whose vocabulary this article uses -
  <https://github.com/ForthHub/discussion/discussions/187>
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
