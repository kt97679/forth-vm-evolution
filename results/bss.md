# Scratch buffers out of the image file: the gene `bss`

Iteration 44. An audit of a small image - seed 8's 85cac726b5 with
rtloopall, 8,234 bytes, from the converter's symbol map:

| part | bytes |
|---|---|
| the image header | 353 |
| headers of words - names, links, alignment | 2,686 (33%) |
| bodies | 5,195 |

and the largest "words" were buffers: INCLUDE-BUFFER 548, POCKET 285, TIB
284 - VARIABLEs with an ALLOT, whose contents nothing reads before it
writes them (ACCEPT fills TIB, PLACE fills POCKET, lines are read into
INCLUDE-BUFFER). NAMEBUF (63) too, but FIND reads it for every candidate
word, and as a call it would cost more than as a variable: it stays.
FORTH-WORDLIST (296) and CONTEXT (64) hold real data.

`--bss`: TIB, POCKET and INCLUDE-BUFFER become words that push START plus
an offset past the image's end (a LITOFF the converter patches once the
layout is known); their parameter fields move there - v8pfa and
remap_pfa_off send every reference after them - and DP starts past them.
The engine's memory there is a zeroed static array; nothing in the engine
changes.

## Checks

Without the gene: hand-made stages IDENTICAL, seven of seed 8's front
designs byte for byte, all 1,309 ids kept (bss is in LATE). With it, on
85cac726b5 and f41ab1810d: alive (the corpus, the kernel's rebuild - which
includes files, through INCLUDE-BUFFER), and S" interpreted and compiled,
DO LOOP and arithmetic at the prompt as before.

## Measured: image against image, one engine (development VM)

`lab/evolve/image-ab.py f41ab1810d 8a2189b3b6 85cac726b5 577c999e62 --db
<seed 8's> --set bss=1 --env SOD16_NO_BSS=1 --rounds 5`:

pinned to cpu 0 (it and its sibling 0% busy; BENCH_CPU=N to choose)
| design | size A | size B | B - A | dispatches B / A: kernel, fib, parse, corpus, loop, sieve | time B / A: kernel, fib, parse, corpus, loop, sieve | selection |
|---|---|---|---|---|---|---|
| f41ab1810d | 8034 | 6970 | -1064 | 1.000, 1.000, 1.000, 1.000, 1.045, 1.000 | 0.986, 1.031, 1.025, 1.021, 1.065, 0.975 | 1.025 |
| 8a2189b3b6 | 8171 | 7115 | -1056 | 1.000, 1.000, 1.000, 1.000, 1.099, 1.000 | 0.987, 0.982, 1.001, 0.969, 1.132, 0.969 | 1.012 |
| 85cac726b5 | 8614 | 7558 | -1056 | 1.000, 1.000, 1.000, 1.000, 1.000, 1.000 | 0.945, 0.944, 0.965, 1.103, 1.203, 0.861 | 1.027 |
| 577c999e62 | 9278 | 8214 | -1064 | 1.000, 1.000, 1.000, 1.000, 1.000, 1.000 | 0.983, 1.033, 0.992, 0.965, 1.023, 1.024 | 0.999 |

**1,056-1,064 bytes - 11-13% - and not a dispatch more** on kernel, fib,
parse, corpus and sieve. loop's +4.5% and +9.9% on the two designs without
rtloop is the alignment artefact (Iteration 13): DP starts elsewhere, so
the run-time compiler pads (LOOP) differently; with rtloop it is 1.000.
seed 8's smallest would be 6,970 bytes.

What the audit leaves: the names (a third of the image - but FIND needs
them), the image header's thread table (353 bytes), NAMEBUF.
