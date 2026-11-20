# The sweep, by symbol size (Iteration 709)

The owner asked whether TRIZ and the other methods can find better designs (708), then said "proceed" to the answer: a
systematic sweep with the evaluator in the loop (results/drafts/ideation-707.md, row 1 - FunSearch's loop, by hand).
The engine's largest pieces were read by size (nm -S, the smallest design's engine.full), a change was proposed against
each, and each was built and measured exactly. Taken: two patches, both in the after-seed-96 batch (results/pending),
which apply on top of 707's four. Measured by results/drafts/rtsc-707.py (the same check: each design's bytes,
evolve.alive, fib and apps against s6), master with the batch as the base and the patched tree after; the raw lines,
the ARM check's and the kernel words' table in results/drafts/sweep-709.txt.

## Taken

**sysstubs** (engine/rt-linux-x86_64.c) - dietlibc's "unified syscall": the 19 wrappers whose C arguments are the
kernel's own registers (rdi, rsi, rdx; the fourth moved rcx to r10) are 4-5 byte assembler stubs that put the number
in rax and jump to one shared tail (syscall; -errno to -1 and errno); rt_syscall6 (707) shuffles its arguments into
the same tail. Each stub has its own section, so --gc-sections keeps only those called. Kept in C: isatty, waitpid,
getcwd, abort, the variadic open and syscall, exit.

| sample (8-byte cells, x86-64) | designs | bytes |
|---|---|---|
| the 8 smallest + 12 spread by speed (clang 19, GCC 1) | 20 | clang -176 to -400; the smallest 4,768 to 4,576 |
| GCC only, spread over size | 14 | v1 of the patch: -1,856 to +192 (below) |

Clang's engines only, by `#if defined(__clang__)`. GCC's designs on the front are LTO builds (99 of 103; 4 of 944
without), and GCC's LTO inlined the C wrappers into their callers: an inline `syscall` clobbers rcx and r11, a call
every caller-saved register. With the stubs (v1) its small engines shrank (-32 to -128) but its large -O2 ones grew:
94a4605110 +192 (nm: rt_main +64, t_write +161, sigaction +50, virtual_machine +64; 258 bytes of code more in all), 89da7aaa44
+128, bd8a9677de +64, b4c80cafb1 +64; and 1875a6900d -1,856, an inlining decision in virtual_machine moved - the kind
of change to a fast design that wants a speed reading. So GCC keeps the C wrappers: its preprocessed runtime is
byte-identical to master's (`gcc -E -P`, compared), and so is the i386 runtime's (rt-linux-i386.c includes the file's
portable part only, RT_PORTABLE_ONLY) - every GCC engine and every 4-byte engine unchanged by construction; the 14 GCC
designs and b4c80cafb1 measured +0 with v2. All 34 alive, fib and apps identical.

**imagemsg** (engine/vm-lab.c) - every refusal of an image's contents is one message from one function,
`not a RelF image (N)`, N a check digit: 1 the magic (another encoding or cell width), 2 a newer CV8 format, 3 CV8
features the engine was built without, 4 the header truncated, 5 an impossible thread count, 6 too many DOES> tails,
7 the escaped band without the engine's, 8 byte-granular headers and 9 a DOES> tail outside the chain (SOD16 only).
The seven messages a CV8 engine carried were 374 bytes (with their NULs) of the smallest engine's 1,072 bytes of
rodata; each of the seven call sites of "Truncated image header." set up write_str and exit. Kept: "Cannot open image
file.", "Error reading image file.", the memory messages, the usage line, the stack and fault messages. The message
starts "not a RelF image" because relf's crash fuzzer (vendor/relf/tree/tools/crashfuzz.py) matches that phrase;
nothing else in the tree reads these texts (grep, designs/ and results/ aside - designs/ are frozen copies).

| sample | designs | bytes |
|---|---|---|
| 8-byte cells, the 20 above | 20 | -226 to -400; the smallest 4,576 to 4,230 (-346) |
| 8-byte cells, GCC | 14 | -226 to -458 |
| 4-byte cells (i386), the 20 above | 20 | -234 to -336; the smallest 5,524 to 5,190 |

All 54 alive, fib and apps identical. The digits checked by hand on the smallest design's i386 engine: a file of text
gave (1), the first 8 and 12 bytes of its image (4), the version byte raised (2), a feature bit set (3), a missing file
"Cannot open image file.", each exit 2; the image itself ran. One trap on the way: `cold` on bad_image made GCC move
L_esc's call (in virtual_machine) to .text.unlikely, out of reach of the dispatch table's label differences - the
build failed ("can't resolve .text.unlikely - .L135"); without `cold` it builds (noreturn, noinline).

Together, on the smallest design: its engine 4,768 to 4,230 bytes (-538), its total 22,409 to 21,679 with 707's rtsc
(-3.3 %); chain B measures these engines, chain A (running) master's.

ARMv7: imagemsg changes the ARM engines too (sysstubs is x86-64's runtime) - checked by tools/arm-cross-check.py
(clang, cross-built, qemu-arm) on 10 of the ARM list spread by speed; the result is in ORDER.md's paragraph.

## Measured, not taken

- **The stubs for GCC** - above: its LTO inlines the wrappers; a call costs it more than the bytes the stubs save.
- **The kernel's largest words** (the smallest design's image, 9,059 bytes, at 8-byte cells; each word's xt by `'`
  in one session, its bytes to the next word found - the next header included, and a word whose name was not found
  counted in the one before): NUMBER? 259, HEADER 154, THROW 152, READ 147, READ-FILE 143, STRING, 143, LOOP, 129,
  INTERPRET 118, DOES> 109, CALL, 104 (READ-LINE's 1,242 and RESIZE's 273 run on into the boot's allocations and
  unnamed words). The largest read at source: NUMBER?'s three prefix tests (`OVER C@ 36 = IF 16 BASE ! -1 + SWAP 1 +
  SWAP THEN`, about 17 bytes each) as one range test and a three-byte table - about 18 bytes; the seven `-1 + SWAP 1 +
  SWAP` as a word - about 4. Not taken: tens of bytes each against the engine's hundreds, every change goes through the
  kernel's seeds and the self-hosting gate, and 707's superoptimizer found at most 11 bytes in the kernel's sequences
  (results/drafts/superopt-707.txt).
- **The profiler's top dispatches** (for speed) - not reached this iteration: the next sweep's, on the shortlist's
  fastest designs, after chain A.
