# The Forth sources: where the dispatches go, and the gene `kfast`

Iteration 49 - the owner's item: look through the Forth sources for
simplifications and optimisations. First where the time goes: every
dispatch attributed to the word it ran in (the profiler's counts per
address, the converter's symbol map; a word's own body - what it calls is
counted to the callee), on seed 10's 96f2d8bfd7 (0.486 at 7,236 bytes):

| workload | the largest |
|---|---|
| kernel | FILL 27.5%, code compiled at run time 14.1%, CMOVE 6.9%, REFILL 6.7%, SEARCH-WORDLIST 6.1%, NEXT-NFA8 5.2%, SCAN 5.0% |
| parse | FILL 25.4%, NEXT-NFA8 19.2%, SEARCH-WORDLIST 14.4%, CMOVE 4.8%, PARSE 4.0%, FIND 3.8% |
| corpus | FILL 26.9%, NEXT-NFA8 11.2%, SEARCH-WORDLIST 10.5%, CMOVE 6.9%, SCAN 5.2% |
| fib, loop | code compiled at run time 98-100% |
| sieve (held out) | code compiled at run time 82%, FILL 15% (its own flags) |

**A quarter of three selected workloads was FILL** - and nearly all of it
one call: NAME>BUF zero-fills all 32 bytes of NAMEBUF before every
dictionary lookup (`NAMEBUF 32 0 FILL`), a byte at a time, about 12
dispatches a byte. The padding serves the cell kernel's SEARCH-WORDLIST,
which compares names a cell at a time; the byte-header system's
SEARCH-WORDLIST8 (cv8b.4) compares the count and that many bytes, and
nothing else there reads NAMEBUF.

**`forth/cv8b-kfast.4`**, the gene `kfast` (LATE; byte-header designs):
`NAME>BUF8` = `32 MIN NAMEBUF PLACE` - an X8, so the kernel's NAME>BUF
gets the body and every caller with it.

## Measured (counted on profiling engines - the same on every machine)

| design | kernel | fib | parse | corpus | loop | sieve | size |
|---|---|---|---|---|---|---|---|
| 295a6acd98 | 0.749 | 1.000 | 0.722 | 0.713 | 0.999 | 0.998 | 6,977 -> 6,977 |
| 96f2d8bfd7 | 0.762 | 1.000 | 0.740 | 0.725 | 0.995 | 0.997 | 7,236 -> 7,228 |

**24-29% fewer dispatches on kernel, parse and corpus**, nothing slower,
no bytes more; alive. Recorded designs untouched (kfast is in LATE: every
id kept, sizes as recorded). 14 of seed 10's 15 front designs and 82% of
its living designs have byte headers.

## Iteration 50: FILL and CMOVE as opcodes

The kernel's byte loops - 12-14 dispatches a byte - as format-10 opcodes
(OPS10_POOL; engine handlers under X_FILL / X_CMOVE, a byte at a time,
ascending, so CMOVE's overlap behaves as the loop's; the converter
replaces a call only after reading the word's body as exactly the
definition the opcode does - `_expect`, written from SOD16_SHOW). And
with the opcode, the colon word's own body becomes the opcode and EXIT:
code compiled at run time still calls FILL - the sieve's - and now gets a
call and two dispatches. Only these two, which never read their caller's
return address; no recorded design has them, so none changes.

96f2d8bfd7 with kfast, then with FILL and CMOVE added (two pairs lose
their slots for them), dispatches counted:

| | kernel | fib | parse | corpus | loop | sieve | size |
|---|---|---|---|---|---|---|---|
| the opcodes / kfast alone | 0.865 | 1.000 | 0.944 | 0.917 | 0.998 | 0.848 | 7,228 -> 7,196 |

alive; the sieve still counts 1899. With kfast: kernel about 0.65 of what
it was, parse 0.69, corpus 0.66 - and the held-out sieve 0.85.

## Iteration 51: the thread walk as an opcode

After the fill and the byte loops, the dictionary search was what was
left: on the same design, NEXT-NFA8, SEARCH-WORDLIST8's loop, NAME=?, FIND
and HASH were about 63% of parse, half of corpus, 30% of kernel - the walk
along one thread, ~20 dispatches a candidate word. kfast's overlay now
factors it out of SEARCH-WORDLIST8 unchanged - `THREAD-FIND ( nfa namebuf
--- nfa' | 0 )` - and THREAD-FIND is a format-10 opcode (OPS10_POOL; the
handler does the count, the bytes, and NEXT-NFA8's three link forms; the
converter checks the body; dormant in a design without kfast - only kfast
has the word). kfast had not been in any run, so its overlay could change.

96f2d8bfd7 with kfast, FILL and CMOVE, then THREAD-FIND added:

| | kernel | fib | parse | corpus | loop | sieve | size |
|---|---|---|---|---|---|---|---|
| THREAD-FIND / without | 0.799 | 1.000 | 0.489 | 0.631 | 0.997 | 0.997 | 7,212 -> 7,212 |

alive in all four engine forms (cached top with multi-state, multi-state,
tail calls, no cached top). **From the design as recorded to here, by
counted dispatches: kernel about 0.53, parse 0.34, corpus 0.42, fib and
loop 1.00, sieve 0.85 - the selected workloads' geometric mean about
0.60.** Time falls less than dispatches - one opcode does a whole walk -
which is what the next run measures.

## Seed 11 (Iteration 52): timed, and the gene `tfind`

On the laptop the batch made the fastest design yet, 0.413 at 8,030 bytes,
9-30% faster than anything earlier at every size - with kfast and CMOVE
only: THREAD-FIND sat in a pool of thirty names and met kfast once in
1,425 designs. `tfind` (LATE, with kfast): THREAD-FIND first among the
format-10 names, sure of a slot. results/evolve-amd-ryzen-7-pro-8840hs-seed11.md.

## Seed 12 (Iteration 53): THREAD-FIND taken up

With tfind, THREAD-FIND was expressed on 11 of the 12 designs on the front
of all runs (8 by tfind, 3 by the pool, from ancestors that had it), first
in generation 7, 37% of the living at the end. The fastest yet, 0.326 at
9,014 bytes; parse at 0.21-0.28 of hand-made s6's time, where seed 11's
front was at 0.40-0.58.

## Iteration 54: the input side - the gene `kinput`

Attributed again on seed 12's fastest (dcbaf0e29f, 0.326): the dictionary
no longer leads; REFILL, SCAN, PARSE, SKIP and WORD were 27-36% of kernel,
parse and corpus, and FILL still 7.5% of kernel - called by code the
workload compiles; in the pool since Iteration 50, never taken up (1% of
seed 11's living). REFILL's share is mostly its tab loop, ten dispatches
a character of every line read.

**`kinput`** (LATE, with kfast): `forth/cv8b-kinput.4` - TABS>BL, the tab
loop factored out unchanged, and REFILL8, the kernel's REFILL calling it -
and SCAN, SKIP, TABS>BL and FILL first among the format-10 names, after
THREAD-FIND: one switch, as tfind. Their handlers go a character at a
time as the loops do, comparing the character as a cell as = and - do;
their colon bodies become the opcode too (calls from run-time code);
their expected bodies from SOD16_SHOW.

| design | kernel | fib | parse | corpus | loop | sieve | size |
|---|---|---|---|---|---|---|---|
| dcbaf0e29f | 0.720 | 1.000 | 0.838 | 0.787 | 0.996 | 0.838 | 9,014 -> 8,974 |
| 35135bde2f | 0.725 | 1.000 | 0.842 | 0.793 | 0.996 | 0.847 | 7,105 -> 7,074 |

alive in all four engine forms; the selected workloads' geometric mean
about 0.86 of the dispatches.

## Iteration 55: kinput completed

Attributed again with kinput on dcbaf0e29f: what was left was spread -
FIND, SEARCH-WORDLIST, HASH and PLACE 22-35% of kernel, parse and corpus;
PARSE's own stack work 9-14%; ?STACK's check after every word, with
DEPTH and the (ABORT") it calls each time to skip its message, 8-10% of
parse and corpus. kinput's overlay had been in no run, so it grew:
`(PARSE) ( addr u c --- a1 len adv )` - PARSE's skip, scan and how far
>IN moves - with PARSE8, the kernel's PARSE around it; ?STACK8 - the same
test as one unsigned compare (DEPTH's logical shift makes an underflow
huge), (ABORT") called only on an error. kinput puts (PARSE), HASH and
PLACE first with the other four; HASH's handler is the kernel's hash
exactly (cross.4's THASH must agree with it).

| design, against it as recorded | kernel | fib | parse | corpus | loop | sieve | size |
|---|---|---|---|---|---|---|---|
| dcbaf0e29f | 0.620 | 0.999 | 0.645 | 0.614 | 0.995 | 0.837 | 9,014 -> 8,951 |
| 35135bde2f | 0.631 | 1.000 | 0.662 | 0.630 | 0.995 | 0.846 | 7,105 -> 7,042 |

alive in all four engine forms; **the selected workloads' geometric mean
about 0.75 of the dispatches**; recorded designs and ids untouched.

## Seed 13 (Iteration 56): kinput taken up

kinput on all 10 designs on the front of all runs, first in generation 1,
66% of the living at the end (kfast 78%, tfind 69%). The fastest yet,
0.284 at 7,799 bytes - 3.5x hand-made s6 - parse at 0.15-0.18 of s6's
time, corpus 0.28-0.33, kernel 0.36-0.43.

## Open

- **Cell headers**: the kernel's SEARCH-WORDLIST compares cell by cell
  "until different" past the name, so its NAMEBUF must be zero past the
  name; a version zeroing only the name's cells hung the converted image
  at its first lookup, and the plain cell system's test harness could
  not compile S" inside a definition - undiagnosed; not built.
- SCAN, PARSE, REFILL: 4-7% each of kernel and corpus.

The converter translates only what the kernel itself uses: an overlay
word with `?DO` was refused ("UNTRANSLATED code bodies"), as cv8b.4's
own comment warns. BEGIN WHILE REPEAT, DO LOOP are safe.
