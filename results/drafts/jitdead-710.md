# The gene jitdead - mechanism 9's V1', built (Iteration 710)

The owner (708): the search reopens after the new roles, chainorder and mechanism 9's V1' built as genes first; (710)
"yes" to building them while chain A runs. This is V1' (results/drafts/triz-706.md: TRIZ's separation in time - the same
bytes bytecode before a word's first call, its native offset after). Chainorder was found mispriced first: below.

## What it does

Today every colon word compiled at run time on a JIT design begins [JIT][four bytes] (forth/cv8t-jit.4): the body's
length, top bit set, until the first call translates it (engine/jit.c), then the native offset, or 0. With jitdead:

- **The header is [JIT] alone** (forth/cv8t-jitd.4, a dump of its own, `-jitd`). The translator finds the end as the
  converter finds a body's - the first EXIT no branch reaches past (`;8` always ends a body so: an EXIT, or an operation
  with the EXIT folded in; a DOES> word's tail is decoded on past (;CODE), as before); an image word with the header
  (--jitimg) from the converter's ends table (jit_wends, Iteration 489), as DABS taught.
- **Translated, the trigger becomes JITN** - a code of its own, pinned (the tag's map, logical 0xFFFC; vm-lab.c's L_x_jit
  handles both) - and **the body's first four bytes the offset**: native code runs the whole word, so its bytecode is not
  run again. What native code does read there at run time is copied to the JIT's memory first (jit_keep): an inline
  string's bytes (S", .") and (ABORT")'s call and string, where the interpreter resumes on a true flag (Iteration 488).
- **Left bytecode - refused - the trigger becomes a NOOP** (code 0, pinned at 0 under the tag): its callers re-pointed
  past it as before, and to native code it is what a field of 0 was.
- **Bodies are padded to four bytes** with NOOPs after their EXIT (`;8`; the converter for the jitimg words), so every
  word has room for the offset; the translator checks the room (the body and the NOOPs after it) and leaves a word
  without it bytecode.
- While a word is translated it is in jit_busy at its depth (the field's 0 did that: a call to it from below is to a
  word not native meanwhile); a refusal for depth leaves its JIT code, to be translated again (490).
- The gene: `jitdead` 0/1, late, expressed with the JIT (jit_on), with or without jitx; -DJITDEAD=1, layout.py
  --jit-dead (the jitimg words' header, JITN's code in vm-jit-ops.h; INL-OPS's header length 1 for rtinline). Without
  jitx the end rule and a table of the jitimg words' ends alone come in (the whole table was 2,568 bytes there).
- Not yet: the self-hosting compiler (forth/cross-cv8.4) - `--jit-dead` is in export-genes.py's G-NOT-YET, so it refuses
  such a design. Before a jitdead design ships: its JIT-HEADER, as the code alone, the pad, the map's 65532, the ends
  table without the pad (as layout.py's). JIT_PRICE (jitstack.py's profiling build) refuses jitdead (#error).

## What it measured

Ten JIT designs of the screen's pool (results/followup-seed96-roles.md): the four smallest (GCC and clang, no jitx)
and six spread by speed (clang, jitx, five with jitexec). Each built with the gene off and on, on master with the
after-seed-96 batch (wends16 in it). Raw lines: results/drafts/jitdead-710.txt.

| design | engine | image | the five programs' code | total (8-byte cells) | | 4-byte |
|---|---:|---:|---:|---:|---:|---:|
| d8f72aa60f | +384 | -56 | -702 | 32,173 -> 31,799 | -1.2 % | -1.6 % |
| 6f46d6cf4f | +320 | -56 | -702 | 32,221 -> 31,783 | -1.4 % | -1.3 % |
| 1f7a2646cd | +432 | -24 | -701 | 32,044 -> 31,751 | -0.9 % | -1.8 % |
| d1db52a781 | +320 | -64 | -702 | 32,437 -> 31,991 | -1.4 % | -1.2 % |
| 923951e8ab | +464 | -80 | -731 | 52,723 -> 52,376 | -0.7 % | -1.3 % |
| c7688e0944 | +64 | -72 | -719 | 50,142 -> 49,415 | -1.4 % | -0.3 % |
| e14a018cb1 | +144 | -72 | -741 | 44,803 -> 44,134 | -1.5 % | -2.9 % |
| ebd3ad7619 | +96 | -64 | -703 | 49,871 -> 49,200 | -1.3 % | -1.1 % |
| 3bd45626a4 | -560 | -72 | -701 | 52,263 -> 50,930 | -2.6 % | -1.2 % |
| b90badf137 | -592 | -64 | -711 | 48,997 -> 47,630 | -2.8 % | -1.4 % |

The five programs' code -693 to -741 bytes on every one, as 706 priced (-700); the image -24 to -80 (the jitimg words'
four bytes each, less their pad). The engine moves -592 to +640: the translator's new paths are 200-400 bytes, and
clang's inlining moves with them (two of the large engines came out 560-590 bytes smaller). All 40 builds alive, fib and apps
as s6; fuzz-designs.py on the ten with the gene, 40 programs each at both widths: 800 runs, 0 differ.

**Instructions** (valgrind's callgrind; this VM reaches no PMU, so counts stand in for time - the laptop's readings are
the measure):

| design | kernel | fib | corpus | loop | bubble | ackermann | apps | sieve | parse |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| d8f72aa60f | -2.9 % | -0.0 % | -2.9 % | -0.0 % | -3.6 % | -1.5 % | -3.0 % | -5.1 % | -2.4 % |
| 923951e8ab | -0.1 % | -0.0 % | -0.7 % | -0.0 % | -0.0 % | +0.0 % | -0.4 % | +0.0 % | -0.7 % |
| e14a018cb1 | -0.4 % | +0.0 % | -1.0 % | +0.0 % | -0.0 % | +0.0 % | -1.6 % | +0.0 % | -1.5 % |
| 3bd45626a4 | -4.3 % | -0.0 % | -5.9 % | -0.0 % | -0.1 % | -0.0 % | -2.0 % | -0.0 % | -5.8 % |

None more on any workload. One op loses its one-byte code to JITN (CHAR+ on 923951e8ab, the lowest-ranked).

**Two wrong turns on the way**, found by the counts: the first build sent a NOOP word to native callers as a word
without the header (jit_kslot) - EXECUTE then paid jit_ksig's decode at every call of a refused word, shellmix +11 %;
and its room check took the decoded end for the room, so every short word (`: X FOO ;`, three bytes and its pad) stayed
bytecode - gc16 +129 %. Both fixed above; the table is the build that has neither.

## Found on the way: wends16 (into the after-seed-96 batch)

The JIT's image-word ends table (jit_wends) was in a design without jitx - and in every jitx engine it is 2,568 bytes
of 5-6 KB of rodata, two 4-byte numbers a row where every number is under 64 KB. Two bytes each: -1,096 to -1,176
bytes on the six jitx engines at both widths, the four without it unchanged; the self-hosting compiler writes its
table the same way and selfhost-check.sh takes either (small-jit PASS at both widths). results/applied-after-seed96/ORDER.md.

## Chainorder - mispriced at 707

707 priced the image's names in their chains by use at zero bytes. Every design on the front (944 of 944) has byte
headers, whose links are unsigned backward distances (vm-lab.c's PREVNFA, cv8b.4's NEXT-NFA8): a chain by use needs
75-85 forward links an image, so signed links, one bit less reach - +19 to +73 bytes of links on six designs (a
scratch pricing, the engine's sign handling besides), and the engine's walk, the Forth walkers, HEADER's link sizes and
the self-hosting compiler's one-pass headers (forward links reserved, fixed up at the end) all change. The owner told
(710); next: a converter-and-engine prototype, instructions counted on parse and the corpus, before the full build.
