# The outer interpreter, and a regression RelF inherited by omission

## The symptom

SOD32 is faster than every system in this repository on any workload
that interprets text, by roughly 2x on the shared CORE corpus and 2.9x
on `bench/parse.fth`. It is SLOWER than all of them on `bench/loop.fth`,
which is almost pure inner interpreter. So the VM is not the reason, and
the encoding work is not implicated either way.

## The measurement

Counting executed VM operations on `bench/parse.fth` - 4000 lines of
interpreted arithmetic - with a counter added to each engine's dispatch:

    SOD32      44,539,357
    RelF      266,555,732      6.0x

RelF does six times the work for the same result. Since its dispatch is
the faster of the two, the whole gap and more is in what it executes.

Profiling the calls says where. Of 72 distinct call targets, the three
hottest are `DOVAR`, `-` and `NAMEBUF`, and `NAMEBUF` alone is entered
8.1 million times for 28,000 words of input - about 290 times per word
parsed. `NAMEBUF` is referenced once per iteration of the outer loop of
`SEARCH-WORDLIST`. So 290 is the average number of dictionary entries
examined per lookup.

## The cause

`tools/find-depth.sh` measures it directly and symmetrically: one
counter in the outer loop of each system's own `SEARCH-WORDLIST`, each
system rebuilt with its own cross-compiler, the same workload.

    system     entries visited
    sod32              397,720
    relf             8,052,823      20.2x

SOD32's `FORTH-WORDLIST` is an array of 33 cells: a thread count and 32
chain heads. `SEARCH-WORDLIST` hashes the first two characters of the
name and walks only the matching thread.

    NAMEBUF COUNT 2 PICK @ HASH 1+ CELLS SWAP + @   \ get the right thread

RelF's `FORTH-WORDLIST` is one cell, described in `kernel.4` as "a
pointer to the last definition in the Forth word list", and
`SEARCH-WORDLIST` walks it from the top:

    @ DUP IF

The hash was dropped when RelF was derived from SOD32. Nothing replaced
it. Every lookup is a linear scan of the whole wordlist, twice, because
the default search order holds `FORTH-WORDLIST` in two slots.

It is worst for numbers, and a program's text is full of them: a number
is never found, so it costs a complete traversal before the system gives
up and converts it. Half the tokens in `parse.fth` are numbers.

## What it is worth

At roughly 27 VM operations per entry examined, the 8.05M entries
account for about 217M of RelF's 266M operations - 81% of everything the
benchmark executes. SOD32's 398K entries account for about 6M of its
44.5M, or 13%.

A hashed wordlist would not make RelF faster than SOD32, and it is not
supposed to: the rest of the system would still be doing what it does.
It would move the two within a modest factor of each other instead of
six, and it would remove the single largest cost in the system.

## Why this has not been fixed here yet

The single chain is load-bearing in one place. SOD16 names a call by
WORD NUMBER, and both the engine's loader and `tools/layout.py` derive
those numbers by walking the dictionary chain from newest to oldest -
"walk the chain to the end, then assign numbers coming back, so entry N
is the Nth word ever defined". With 32 threads there is no single chain
to walk and no such ordering, so the numbering would need a separate
definition order to follow.

That is a real constraint and it is worth stating plainly rather than
presenting the hash as free. It is also only a constraint for SOD16:
CPT16, CV8 and the packed schemes name a call by ADDRESS and do not care
how the dictionary is threaded.

## The general point

Two hundred iterations of this project went into the inner interpreter,
and the measured result of all of it is between 0.72x and 0.81x. A
regression introduced at the very first step, by leaving something out
rather than by changing anything, was worth 6x on the same workload and
was never looked for, because every benchmark the project used compared
the system against ITSELF.

---

# The fix, and what it was worth

The hashed word list is now in `kernel.4`, threaded by `cross.4`, with
`extend.4`'s `WORDLIST` building the same shape and `COLD` relocating
each thread head. 32 threads, SOD32's hash function unchanged.

Dictionary entries visited on `bench/parse.fth`, by `tools/find-depth.sh`:

    before       8,052,823
    after           288,037      28x fewer
    sod32           397,720

RelF now examines fewer entries than SOD32 does, because its dictionary
is smaller at the same thread count.

Wall clock, minimum of interleaved repetitions in a single run, so the
before and after figures are comparable to each other and to SOD32:

    bench/parse.fth        4-byte    8-byte
      before                611 ms    786 ms
      after                 165 ms    179 ms
      sod32                 225 ms       -

    ANS CORE corpus        4-byte    8-byte
      before                 93 ms    100 ms
      after                  41 ms     43 ms
      sod32                  50 ms       -

3.7x on parsing at 4-byte cells, 4.4x at 8-byte. The system that was
2.7x slower than its ancestor on interpreted text is now slightly faster
than it, and the same change is worth 2.3x on the CORE corpus.

For scale: the entire encoding ladder, from cell threading to CV8 with
every specialisation, is worth between 0.72x and 0.81x on the same
workloads. One omission, restored, is worth more than all of it.

## What is not done

The change is complete and tested for the stages whose images are CELL
images - `s0-cell`, `p4-pack4`, `p8-pack8` - which pass the full corpus
at both widths and cross-compile the kernel byte-identically.

The TRANSLATED stages - SOD16 through CV8 - do not yet build.
`tools/layout.py` rebuilds the dictionary's link fields when it moves
every word to its new address, and it still writes ONE chain in dump
order. It needs to write 32, and to relocate the thread heads held in
`FORTH-WORDLIST`'s data body, which it currently copies verbatim
because it has no way to know those cells are addresses.

That is mechanical but it is not small, and it is the honest state of
the branch: the finding is confirmed and measured, the fix is real, and
half the ladder is waiting on the translator.
