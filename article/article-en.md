# Making a Forth virtual machine smaller: four attempts, two of which failed

In 2004, out of curiosity rather than need, I forked L.C. Benschop's
SOD32 - the Stack Oriented Design, a 32-bit virtual machine with a Forth
on top - threw away its packed instruction format, and replaced it with
one relative offset per cell. I called the result RelF, for Relative Forth. The point was
speed: a cell you can jump through directly beats six 5-bit
subinstructions you have to unpack first. It was 32-bit only, it worked,
and it sat there. Whether it was actually faster than what it forked
from, I did not check at the time - a detail that comes back in section
8.

Recently I came back to it and built it for 64-bit. The deal changed:
the same Forth, the same words, in an image that had gone from 13,380
bytes to 24,320. One relative offset per cell means one *cell* per
operation, and the cell had just doubled.

What follows is what I tried, in the order I tried it, including the two
attempts that did not work and why.

Two words are load-bearing throughout. The **engine** is the C program
that fetches operations and runs them - a few thousand lines, compiled
once. The **image** is the compiled Forth system it runs: the dictionary,
every word body, the whole language. Only the image changes size between
the systems below; the engine changes only in how it decodes what it
reads. When I say "0.47x", I mean the image.

The **dispatch loop** is the part of the engine that reads the next
operation and jumps to the code for it. Every scheme here is a different
answer to "what does one operation look like in memory", and every one
is paid for in that loop.

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
and it cannot favour an encoding, because the image every system writes
is in the cell format regardless. It is also the correctness check - the
image produced must be byte-identical to the reference before any timing
is recorded, so a system that is fast because it is quietly wrong fails
the comparison that times it.

Ratios are against RelF, the cell engine, so smaller is better. They
carry one standard error, measured across several differently-laid-out
builds of each engine - see section 9, which is about measurement
and is the part I would keep if I had to cut the rest.

---

## 1. What 64-bit did

Here is what RelF's encoding actually looks like. This definition:

```forth
: COUNT   DUP 1 + SWAP C@ ;
```

compiles to seven consecutive cells, one per operation, holding these
values:

```
   25    9    1   93   29   41    5
  DUP  LIT   1    +   SWAP  C@  EXIT
```

A cell here holds one of two things. A **call** holds the distance from
itself to the word being called. A **primitive** holds a small number
saying which built-in operation it is. The low bit says which kind it
is, so `25` is a primitive: `1 + 6*4`, where 6 is the index of `DUP`.

Nothing in the image is an absolute address, which is why it can be
loaded anywhere. That was the point of the design.

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
already solved it by packing. So that is where I started.

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

| | predicted | 8-byte cells | 4-byte cells |
|---|---|---|---|
| PACK4, 4-bit opcodes | 2.05x | 1.13 | 1.14-1.18 |
| PACK8, 8-bit opcodes | 1.90x | 1.09 | 1.08-1.18 |

So the rejection was right and the reason was wrong by a factor of four.
The old benchmark's own header said why, in advance: its streams were
sized to run hot, so it measured decode cost with memory free, which it
called the pessimistic case. Pessimistic by four times, as it turned
out. The baseline it lost to was wrong too - token threading had been
recorded at 0.985, faster than cell dispatch, from a benchmark running a
32-megabyte stream against a 2-megabyte level-2 cache. It was measuring
memory traffic, not dispatch.

The other failure is the one worth reporting, and only building it
showed it. Counting on paper, PACK4 and PACK8 came out level, both at 0.76x - the
narrower field should pack twice as many operations per cell, which
ought to offset having fewer of them to choose from. Built, PACK4 folds
away *fewer* cells - 377 against 433 - and produces the **larger**
image, 21,296 bytes against 20,848.

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
paid for the joins as well and got 0.86x, while running 10-18% slower.
So packing was out.

## 3. Attempt two: a 16-bit token through a word table

If a cell is too wide, use a narrower unit. One 16-bit token per
operation: values below 256 are primitives, and 256+n means "the body of
the n'th word", looked up in a table of addresses the engine builds when
it loads the image. I called it SOD16, after the ancestor whose unit it
halves. This is textbook token threading, and a table is the obvious way
to turn a number into an address.

The image halved, 24,320 to 12,864 at 8-byte cells. And it was the
slowest system in the whole set:

    SOD16, kernel compile     1.37 (AMD)    1.36 (ARM)

Worse than the cell engine it was meant to improve on, on every machine
and every workload, by a wider margin than anything else I built.

It cost more than the table lookup, too, and the reason is a direction
problem. There are two tables, pointing opposite ways:

    the engine's      number -> address    built at load, in C memory
    the compiler's    address -> number    built by the image, on the heap

The engine's is the one that makes the encoding work: token 256+n, look
up entry n, jump there. But a *compiler* starts from the address of the
word being called and needs the number, which is the other direction -
and the engine's table is in memory Forth cannot see anyway. So the
image has to build and maintain a second, inverted copy of it, and
binary-search that on every call it compiles. The table is also sized at load and never grows, so a
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

## 4. Delete the table

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
because tokens below that are primitives. Compare that with the four
steps SOD16 needed.

    CPT16, kernel compile    1.024 ±0.021 (AMD)    1.007 ±0.016 (ARM)

Level with the cell engine, at half the image size. Not faster, and not
slower either: 1.024 against 1.000, with an error of 0.021.

What that measures is a sum, and it is worth being precise about which.
CPT16 removes two things at once - the table lookup in the dispatch
loop, and the compiler's search from address back to word number. The
37% between SOD16 and CPT16 is what those two cost together. Nothing
here separates them, and I have not tried to.

What the sum does show is that nothing here penalises the 16-bit unit
itself: SOD16's deficit disappears when the table machinery is replaced,
and the unit stays the same width throughout. The bookkeeping was the
expensive part, and it had looked like free indirection.

## 5. Attempt three: narrow the unit itself

Two lessons now point the same way. Packing fails because Forth code has
no long runs. Dispatcher logic fails because it costs what it costs. The
remaining lever is the size of the unit - not how many operations share
a cell, and not how cleverly the target is computed, but how many bytes
one operation takes.

So: a byte stream - CV8, one byte per unit. Values under 0x80 are
opcodes; 0x80 and above begin a call whose remaining bits are an
offset. No alignment, no tag bytes, no
runs required, nothing in the dispatch path but a compare and a shift.
Two bytes for a call to something nearby, three for one further away.
The general shape - a byte-coded stream with variable-length
instructions - is the one FCode and the Java virtual machine use, though
what their call instructions name is not what CV8's names.

    CV8, kernel compile    0.919 ±0.026 (AMD)    0.896 ±0.011 (ARM)
    CV8, image             11,416 bytes - 0.469x of cell threading

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

## 6. Then it compounds

Both of the tricks in that `COUNT` line are worth having on their own.

**Folding**: a primitive immediately followed by `EXIT` becomes a single
opcode, which removes one trip round the dispatch loop from the end of a
great many definitions.

**Specialisation**: give the common case its own opcode, the idea CPython
3.11 uses. Small integers get one each, so do the hottest kernel words,
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
the image. That is a trade, not an improvement, and the sequence is only
worth it because of the row underneath.

Because the specialisations are where the speed is. Measured as steps
along this sequence: everything from cell threading down to CV8 - two
failed attempts and three successful encodings - is worth 0.081 of the
ratio. Adding specialised opcodes is worth 0.231, about three times as
much.

That is a comparison of steps in one order, not a claim that
specialisation beats encoding in general. The opcodes were added last
and to a byte stream; several of them exist only because there is a
one-byte opcode space to put them in. What is fair to say is that the
encoding work was the smaller half of its own project, and that it took
five attempts to get to the point where the cheap win was available.

Measured by bytes saved in the image, small integers are worth 190, hot
words 194 and immediate operands 111.

## 7. The last place cell width was still being paid

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

`FINDINGS-CELL-WIDTH.md` accounts for every one of the 860 bytes still
separating the two widths: 408 in data fields, which are cells because a
`VARIABLE` holds a cell; 273 in seventeen inline operands that are still
cell-sized and in the padding they force on the bodies around them; 156
in a wordlist table; and 23 in the boot prologue and the links
themselves. Only the 273 is worth chasing.

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

The cause took an afternoon. SOD32's dictionary is 32 hashed chains,
selected on the first two characters of a name. RelF's was a single
chain walked from the top. I had dropped the hash while changing the
link fields from absolute to relative in 2004 and never went back to see
what it cost. It costs most on *numbers*, which are never found and so
pay a complete traversal before the interpreter gives up and converts
them - and about half the tokens in a program's text are numbers.

Restored, with SOD32's hash function unchanged:

    dictionary entries visited, same input     before  8,052,823
                                                after    288,037
                                                SOD32    397,720

Those are counts, not timings, so they are the same on every machine. In
time it was 3.7x on parsing at 4-byte cells and 4.4x at 8-byte. The
whole encoding sequence in this article is worth about 0.69. One
omission, restored, was worth more than all of it.

Hashing a dictionary is not an insight and SOD32 already did it, so the
fix is not the interesting part. Why nobody noticed is: every benchmark in this project compared the system against
itself - against the previous stage, against last week's build - never
against the thing it was forked from to beat. The fault went in in 2004
and sat there until this year, and the ancestor was in a tarball the
whole time.

It also means the eight encodings above were tuning a system that was
carrying a 4x handicap in its outer interpreter throughout. All the
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
measures the build, not the encoding.

Every conclusion above survived being measured twice on at least two
machines. Several earlier ones did not, and are not above.

## 10. Not measured

- Three machines is not a study. Two x86-64 and one ARMv7; nothing with
  a different memory order, and nothing without an operating system
  underneath.
- Nothing here measures pure execution reliably, since both
  microbenchmarks failed reproducibility.
- The locals and variable specialisations are inert in these images:
  `locals.4` is loaded only into the shell image, so the kernel that
  every benchmark runs has no locals to specialise.
- With token threading, `DOES>` is the only extension point - a new
  behaviour type cannot be added from Forth. That is the strongest
  architectural criticism this design has had and I have no answer.

## 11. What came out of it

Start and finish, same Forth, same 616 tests passing:

| | image | kernel compile | parsing |
|---|---|---|---|
| RelF, where this began | 24,320 bytes | 1.000 | 1.000 |
| CV8 + specialisation + byte headers | 7,609 bytes | 0.731 | 0.830 |

0.31x the image and 0.73 the time on the compiler's own largest job, at
the price of about 17% on text interpretation. At 4-byte cells, where
RelF started life, the same sequence gives 0.50x and 0.73.

Set against that: restoring one hash table that had been missing since
2004 was worth 3.7 to 4.4x on parsing by itself. Everything in the
sequence above is a fraction; that one omission was a multiple.

Seven things I would tell someone starting the same work.

**Packing needs runs, and this kernel has not got them.** The mean run
of consecutive packable primitives here is about 1.3, so a scheme that
pays a tag byte to amortise over a run never gets to amortise. I would
expect that of Forth code in general, because calls break runs and Forth
is mostly calls - but I have measured one kernel, not a language.

**A narrower unit beat a fuller cell, here.** Both failed attempts were
ways of fitting more into a cell; what worked was making the unit
smaller and giving up fixed width. Whether that holds for a language
with longer straight-line runs than Forth, I have not tested.

**A table costs more than its lookup.** The word-number table looked
like free indirection. Removing it and the bookkeeping it forced on the
compiler was worth 37% between them - and nothing in this experiment
separates the two, so I cannot tell you what the dispatch-loop half
alone was worth.

**Specialisation was worth about three times the encoding work.** As
steps along this sequence: 0.081 of the ratio for all the encoding
changes together, 0.231 for adding specialised opcodes. It was applied
last and to a byte stream, so it is not independent of what came before
- but it is the cheap step, and it arrived only after five attempts had
built somewhere to put it.

**Look outside the instruction stream.** Changing the dictionary header
took the image from 11,088 bytes to 7,609, and five rounds of encoding
work had never touched it. Before that change, three quarters of what
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
  specialising interpreter) for giving the common case its own opcode; Lua 5.4 for immediate operands; the Java virtual machine's `iload`, CPython
  `LOAD_FAST` and Smalltalk-80's bytecodes 16-31 for locals as opcodes;
  Titzer's in-place Wasm interpreter for interpreting the compact form
  rather than expanding it at load.
