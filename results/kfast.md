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

## Open

- **Cell headers**: the kernel's SEARCH-WORDLIST compares cell by cell
  "until different" past the name, so its NAMEBUF must be zero past the
  name; a version zeroing only the name's cells hung the converted image
  at its first lookup, and the plain cell system's test harness could
  not compile S" inside a definition - undiagnosed; not built.
- **The thread walk** - NEXT-NFA8 and SEARCH-WORDLIST8's loop, a third of
  parse - as one opcode.
- SCAN, PARSE, REFILL: 4-7% each of kernel and corpus.

The converter translates only what the kernel itself uses: an overlay
word with `?DO` was refused ("UNTRANSLATED code bodies"), as cv8b.4's
own comment warns. BEGIN WHILE REPEAT, DO LOOP are safe.
