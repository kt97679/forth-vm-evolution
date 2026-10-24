/*
 *  sod16.c - RelF's engine with SOD16 code: one 16-bit token per
 *  operation instead of one host cell.
 *
 *  DERIVED FROM relf.c, DELIBERATELY BY MINIMAL EDIT. The point of this
 *  file is how little of it differs. 64 of the 68 primitives are
 *  byte-for-byte identical to relf.c's, because a primitive's body does
 *  not depend on how code is represented - only on the stacks and
 *  memory, which are unchanged. Just four touch `ip`: exit, lit,
 *  branch, ?branch. Plus NEXT() and the boot sequence.
 *
 *  That is the argument for SOD16 as a change to this project rather
 *  than a rewrite of it, and it should stay true: if this file starts
 *  diverging from relf.c anywhere except the marked places, something
 *  has gone wrong.
 *
 *  WHAT CHANGED
 *
 *    NEXT()     reads a 16-bit token. t < 256 is a primitive index;
 *               t >= 256 is word number t-256, and the target comes
 *               from wordtab[] - one load, no base add, no shift.
 *    L_lit      operand is a 16-bit token, not a cell.
 *    L_branch   offset is in TOKEN units, signed 16-bit. Measured on
 *               the real image, zero branches need more than that.
 *    L_0branch  same.
 *    L_exit     unchanged - the return stack holds ip values either way.
 *
 *  WHAT IS NOT DONE YET
 *
 *    Loading. A token image's bodies are a different size from a cell
 *    image's, so every address in the dictionary moves: link fields,
 *    HERE, and anything a VARIABLE holds that points into the image.
 *    It BOOTS (Iteration 179). Both cell widths run every word that
 *    was compiled into the image: arithmetic, strings, HEX/DECIMAL,
 *    tick, and the whole pre-compiled shell.
 *
 *    It CANNOT COMPILE. `,` and `COMPILE,` write CELLS, so a new
 *    definition lays down cell-threaded code that this engine then
 *    reads as tokens. `: SQ DUP * ;` segfaults. Making the compiler
 *    emit tokens is the next piece, and it is the same work as
 *    GOALS.md's phase 3.
 */
/*
 *  RelF - Relative Forth
 *  Based on SOD32 by L.C. Benschop
 *  Copyright 2001 - 2005, Kirill Timofeev, kt97679@gmail.com
 *  The program is released under the GNU General Public License version 2.
 *  There is NO WARRANTY.
 *
 *  Phase 5 engine (see GOALS.md): portable across every architecture the
 *  build's libc supports. Cell width is chosen at compile time to match
 *  the host's own pointer width (4 bytes on 32-bit hosts, 8 on 64-bit
 *  ones) - see GOALS.md, "load-bearing facts", for why cell width and
 *  host pointer width must match in this design. Images are native host
 *  endianness (little-endian only - see GOALS.md non-goals), not a
 *  portable on-disk format; a magic header records both cell width and
 *  a fixed tag, so a mismatched image fails cleanly instead of silently
 *  misbehaving. Dispatch is computed-goto threaded code (GCC/Clang
 *  "labels as values"), not a function-pointer table - see PROGRESS.md
 *  for why. kernel.img itself must be built for the same cell width as
 *  this binary (see README.md) - a 32-bit build needs its own image,
 *  cross-compiled with TARGET-CELL-BYTES set to 4 (see cross.4).
 */

#ifndef SYSC
#define SYSC 1      /* the single-SYSCALL model, every engine (Iteration 147) */
#endif
#if SYSC
#include <errno.h>      /* SYSCALL's -errno (Iteration 141) */
#if defined(__i386__) || defined(__arm__)
#include <sys/mman.h>   /* Iteration 325: mmap through the C library */
#endif
#endif
#if SYSC && (defined(__i386__) || defined(__arm__))
/* The image's numbers are x86-64 Linux's; i386's (and, Iteration 325, 32-bit ARM's) for the calls the shell's
   overlay makes (forth/shell-sysc.4; Iteration 141). Any other: ENOSYS. */
static long sysc_i386(long n)
{
    switch (n) {
    case 39: return 20;   case 57: return 2;    case 33: return 63;   case 80: return 12;
#if defined(__arm__)
    case 231: return 248;                       /* exit_group: ARM's is not i386's */
#else
    case 231: return 252;
#endif
    case 79: return 183;  case 61: return 114;  case 22: return 42;
    case 97: return 191;  case 160: return 75;  case 59: return 11;
    /* Iteration 325: the file overlays' (forth/file-sysc*.4) - read, write, open, close,
       lseek, munmap, ioctl, mremap, exit, unlink; mmap goes through the C library (mmap2) */
    case 0: return 3;     case 1: return 4;     case 2: return 5;     case 3: return 6;
    case 8: return 19;    case 11: return 91;   case 16: return 54;   case 25: return 163;
    case 60: return 1;    case 87: return 10;   default: return -1;
    }
}
#endif
#include <unistd.h>
#include <sys/mman.h>
#ifndef MAP_32BIT
#define MAP_32BIT 0      /* Iteration 329: x86's alone - on a 32-bit ARM host every address is below 4 GB anyway */
#endif
#include <pwd.h>
#include <sys/resource.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint16_t UNS16;   /* SOD16: a code token */

extern char **environ;

/* Process argv, exposed to Forth via SYS-ARGC/SYS-ARG below - argv[0]
 * and argv[1] (the program name and kernel-image path) are not part
 * of this; SYS-ARG(0) is argv[2], the first argument after the image
 * path, matching a shell's own convention of not exposing its own
 * name via the primitives that expose *its* arguments. */
static int g_argc;
static char **g_argv;

#define FOLDBASE 128
#ifndef ESCAPE
/*  ESCAPE: the 32 OS/libc primitives move behind ESC + a selector,
 *  which renumbers the primitive band. Both the engine and the
 *  translator (--escape) must agree, so this is off until the fault in
 *  BUF-ALLOC is found.  */
#define ESCAPE 0
#endif
#ifndef DISPATCH256
/*  DISPATCH256: no opcode-vs-call test at all. The table gets 256
 *  entries, every one with the top bit set pointing at do_call, so
 *  NEXT is load / increment / indirect jump. Suggested in review:
 *  the CPU should not have to learn whether this is a one- or
 *  two-byte instruction before it can jump. Costs 1 KB more table.  */
#define DISPATCH256 0
#endif
#ifndef VARSLOT
/*  VARSLOT: slot operands (VAR@/VAR!, the locals opcodes) are variable
 *  too. 0xxxxxxx + 1 byte is a 15-bit payload; 1xxxxxx + 2 bytes is
 *  23-bit. Without this a slot is a fixed 16 bits, so variables had to
 *  live in the first 512 KB (64-bit) / 256 KB (32-bit) while VARCALL
 *  let code span 32 MB - an asymmetry that fails silently.  */
#define VARSLOT 1
#endif
#ifndef DOESFAR
/*  DOESFAR: CREATE reserves THREE bytes after the DOVAR opcode and
 *  DOES> writes the three-byte far call, so the parameter field is at
 *  align(body+4). Needed when the call scale is 0, where the two-byte
 *  near form reaches only 16 KB and the cross-compiler's dictionary is
 *  far larger. Without it CREATE reserves two and the field is at
 *  align(body+3), which is what every other CV8 stage uses.  */
#define DOESFAR 0
#endif
#ifndef HOTCALLS
/*  HOTCALLS (Iteration 14): one-byte calls. The far-call prefixes
 *  0xE0-0xFF become calls to up to 32 of the image's own words, whose
 *  image offsets the image's header carries (F_HOTCALLS), chosen per
 *  design by the converter from its own call sites (--hotcalls N). The
 *  far form keeps 0xC0-0xDF: 21 bits, 2 MB at scale 0. Priced at
 *  Iteration 13: 1-3% of the image, no dispatch removed.  */
#define HOTCALLS 0
#endif
#ifndef TAG2
/*  TAG2 (Iteration 65, FORMAT-TAG2.md): the two-bit tag, relf's planned
 *  format, decided with the owner. A byte's top two bits: 00 an opcode -
 *  64 of them, one the escape to 256 more - and 01, 10, 11 a call of 2,
 *  3, 4 bytes with a 14-, 22-, 30-bit byte offset from the image base: a
 *  1 GB code space. Which operation each code is, the design's profile
 *  decides (the converter writes vm-tag2-one.h and vm-tag2-esc.h). The
 *  dictionary's byte-header links take the same tag, read backwards.  */
#define TAG2 0
#endif
#if TAG2 && (HOTCALLS || SCALE != 0 || ENC != 3)
#error "TAG2: no one-byte hot calls, byte offsets (SCALE 0), CV8 only"
#endif
#if TAG2 && defined(MEMSIZE) && MEMSIZE > (1 << 30)
#error "TAG2: a call reaches 1 GB from the image base - MEMSIZE at most that"
#endif
#if TAG2
/*  A byte-header link, read backwards from the name: the byte before it
 *  carries the tag - 00 one byte (6 bits; 0 ends the thread), 01 two (14
 *  bits), 10 three (22), 11 four (30) - the bytes below it high to low.  */
#define PREVNFA(a) ({ UNS64 a__ = (a); UNS8 t__ = BYTE(a__ - 1); UNS64 d__;                  \
    switch (t__ >> 6) {                                                                   \
    case 0: d__ = t__; break;                                                             \
    case 1: d__ = ((UNS64)(t__ & 63) << 8) | BYTE(a__ - 2); break;                        \
    case 2: d__ = ((UNS64)(t__ & 63) << 16) | ((UNS64)BYTE(a__ - 2) << 8) | BYTE(a__ - 3); break; \
    default: d__ = ((UNS64)(t__ & 63) << 24) | ((UNS64)BYTE(a__ - 2) << 16)                \
                   | ((UNS64)BYTE(a__ - 3) << 8) | BYTE(a__ - 4); }                        \
    d__ ? a__ - d__ : 0; })
#else
/*  A byte-header link in CV8 (cv8b.4's NEXT-NFA8): its last byte, the one
 *  before the name - below 0x80 seven bits (0 ends the thread), below 0xC0
 *  fourteen, else twenty-two.  */
#define PREVNFA(a) ({ UNS64 a__ = (a); UNS8 t__ = BYTE(a__ - 1);                               \
    t__ < 128 ? (t__ ? a__ - t__ : 0)                                                     \
    : t__ < 192 ? a__ - (((UNS64)(t__ & 63) << 8) | BYTE(a__ - 2))                        \
    : t__ < 224 ? a__ - (((UNS64)(t__ & 31) << 16) | ((UNS64)BYTE(a__ - 2) << 8) | BYTE(a__ - 3)) \
    : a__ - (((UNS64)(t__ & 31) << 24) | ((UNS64)BYTE(a__ - 2) << 16)                     \
             | ((UNS64)BYTE(a__ - 3) << 8) | BYTE(a__ - 4)); })   /* 416: a fourth form, 29 bits */
#endif
#ifndef VARCALL
/*  VARCALL: the call form is variable too. 10xxxxxx takes one more byte
 *  (14-bit payload), 11xxxxxx takes two (22-bit). Costs one extra test
 *  on the call path; buys a far call without spending an opcode.
 *  VARCALL=0 is the fixed 15-bit form.  */
#define VARCALL 1
#endif
#ifndef SIGNTEST
/*  Measured in guest instructions (tools/lab/xarch, qemu): -3.6% on
 *  AArch64, -4.2% on RISC-V 64, +/-0.3% on x86, but +3.0% on ARMv7.  */
#if defined(__arm__) && !defined(__aarch64__)
#define SIGNTEST 0
#else
#define SIGNTEST 1
#endif
#endif
#ifndef SPEC
#define SPEC 0     /* 1: CV8 specialised opcodes 0x60-0x77 (CV8.md 10) */
#endif
#ifndef VMPUSH
#define VMPUSH PUSH
#endif
#define UNS8 unsigned char /* byte access; width-independent */

#if UINTPTR_MAX == 0xFFFFFFFFFFFFFFFFULL
typedef uint64_t UNS64; /* the VM's cell type - 8 bytes on this host */
typedef int64_t  INT64;
#define CELL_BYTES 8
#define CELL_SHIFT 3     /* log2(CELL_BYTES): primitive dispatch stride */
#elif UINTPTR_MAX == 0xFFFFFFFFUL
typedef uint32_t UNS64; /* the VM's cell type - 4 bytes on this host */
typedef int32_t  INT64;
#define CELL_BYTES 4
#define CELL_SHIFT 2
#else
#error "relf: unsupported pointer size (only 32-bit and 64-bit hosts are supported)"
#endif

/*  How much memory the VM gets: dictionary at the bottom, return and
 *  data stacks at the top (see rp/dsp below). Raised from 256K to 1M
 *  in Iteration 40, after a prebuilt shell image measured 253,256
 *  bytes - i.e. kernel.img plus locals.4 plus shell.4 had come within
 *  a few KB of the old ceiling, with the stacks living in what was
 *  left. Overflowing it does not fail cleanly: the symptom is
 *  corrupted compilation reported as "Undefined word" against an
 *  empty name, nowhere near the actual cause. 1M is still small
 *  enough to be unremarkable and leaves real headroom for shell.4 to
 *  keep growing.  */
/*  The whole VM: image, all dictionary growth, and the two stacks. This
 *  is the FIRST ceiling a growing system meets - far below the call
 *  reach - and it is a plain parameter: every reference in an image is
 *  relative, so raising it breaks nothing. Overridable at build time,
 *  and at run time with RELF_MEMSIZE (in MB).  */
#ifndef MEMSIZE
#define MEMSIZE (16 * 1024 * 1024)
#endif
/*  Room reserved for the return stack. Raised from 2048 in Iteration
 *  90: 2048 bytes is 256 cells, and each level of shell function
 *  recursion nests roughly a dozen Forth calls, so the return stack
 *  overflowed - segfaulting - at around fifteen levels, before
 *  shell.4's own MAX-POS-PARAM-DEPTH guard of 32 could report
 *  "recursion too deep". A limit that pre-empts a higher-level one
 *  turns a diagnosable error into a crash.  */
/*  SOD16: code is 16-bit tokens, and the word table is DERIVED - it is
 *  rebuilt at load by walking the dictionary link chain, holds absolute
 *  addresses because it is rebuilt after relocation, and is never
 *  saved. Nothing about it goes in the image.  */
#define TOK(a)   (*(UNS16 *)(uintptr_t)(a))
/*  CV8 operands are unaligned little-endian. Composed from bytes, not
 *  memcpy'd: GCC merges this into one ldrh/movzwl on x86, ARMv7 and
 *  AArch64, while on RISC-V the memcpy form compiled to byte loads, a
 *  stack round trip and a stack-protector check on every operand.  */
static inline UNS64 LD16(UNS64 a) {
    const UNS8 *p = (const UNS8 *)(uintptr_t)a;
    return (UNS64)p[0] | (UNS64)p[1] << 8;
}
#if ENC == 3
#define OPND16(a) LD16(a)
#else
#define OPND16(a) TOK(a)
#endif
static inline UNS64 LD32(UNS64 a) {
    const UNS8 *p = (const UNS8 *)(uintptr_t)a;
    return (UNS64)p[0] | (UNS64)p[1] << 8 | (UNS64)p[2] << 16 | (UNS64)p[3] << 24;
}
#define MAXWORDS 65280
static UNS64 *wordtab;          /* absolute body addresses, malloc'd */
/* n_words: superseded by nwords, set by load_image */

#define RSTACK_BYTES 65536
/*  Room the data stack is allowed to occupy before it is declared
 *  overflowed. Nothing enforced this until Iteration 151: dsp simply
 *  descended out of its own region, through free space, and into the
 *  dictionary, silently rewriting compiled words from the top down
 *  until it eventually walked off the bottom of mem[] and took a
 *  SIGSEGV. The corruption came first and the crash came much later,
 *  which is why the symptom recorded above - "Undefined word" against
 *  an empty name - points nowhere near the cause.
 *
 *  256KB is 32768 cells at 8-byte width. The floor it puts under the
 *  data stack sits at MEMSIZE-RSTACK_BYTES-DSTACK_BYTES = 720,896
 *  bytes from base, and the largest image this project builds (the
 *  x86-64 prebuilt shell) ends at 206,024 - so the check fires with
 *  half a megabyte still between the stack and the dictionary, i.e.
 *  strictly BEFORE any corruption rather than after it. This reserves
 *  nothing and moves nothing: dsp and rp start exactly where they
 *  always did, so S0/R0 and every saved image are unaffected.  */
#define DSTACK_BYTES 262144
#ifndef STACKSEP
#if ENC == 3          /* the cv8 family only: sod16's and cpt16's compact encodings keep the stacks in reach (they crashed apart) */
#define STACKSEP 1   /* Iteration 184 (the owner): the stacks in a chunk of their own; the dictionary in
                        a reservation of MEMMAX, committed as touched, that never moves - so it can grow
                        past MEMSIZE (addresses are absolute everywhere: a moved block would break them) */
#else
#define STACKSEP 0
#endif
#endif
#ifndef MEMMAX
#define MEMMAX (256u << 20)   /* within the jail's 1 GB of address space, and tag 2's 1 GB call reach */
#endif
#ifndef DSKEW
#define DSKEW 0   /* Iteration 183: bytes the data stack starts lower - its top cells' page offsets apart from the return stack's (4K aliasing) */
#endif

/*
 *  Macroses for memory access. Plain native access, both cell- and
 *  byte-granularity: no byte-order opinion of its own (see GOALS.md,
 *  phase 5). Correctness of any Forth-level code that compares whole
 *  cells of byte data (e.g. SEARCH-WORDLIST's name-comparison trick)
 *  doesn't depend on which convention this is, only that reads and
 *  writes agree with each other - which they trivially do here, since
 *  there's only one access path.
 */

#define CELL(reg) (*(UNS64*)(reg))
#define BYTE(reg) (*(UNS8*)(reg))
#if BFIND
/*  Iteration 316, the gene bfind: THREAD-FIND's and (FIND)'s walk with fewer branches to
 *  mispredict ((FIND) was 9-13% of the interpreter-heavy runs' mispredictions,
 *  results/missmap-amd-ryzen-7-pro-8840hs.md). A candidate's count byte and first seven
 *  characters are one masked 64-bit compare - almost always unequal, so predicted - and the
 *  rest of a longer name is compared only on a match; a link is read without a branch on its
 *  form: the four bytes ending at its tag as one word, shifted by its length. The same walk
 *  as PREVNFA's and the loops' below: the same word found, or none. Iteration 399: the
 *  signature and its mask are 64 bits at either width - UNS64 is the cell, 4 bytes at 4-byte
 *  cells, where they held the count and three characters: a name of 4 to 7 matched the newest
 *  of its length and first three (seed 59: 34 of its front died on the corpus at 32 bits).  */
static inline uint64_t bf_ld64(UNS64 a) { uint64_t x; memcpy(&x, (const void *)(uintptr_t)a, 8); return x; }
static inline uint32_t bf_ld32(UNS64 a) { uint32_t x; memcpy(&x, (const void *)(uintptr_t)a, 4); return x; }
#if TAG2
static inline UNS64 bf_prev(UNS64 a) {          /* tag t: t+1 bytes, the top one's 6 bits */
    uint32_t w = bf_ld32(a - 4); UNS64 d = (UNS64)((w & 0x3FFFFFFFu) >> (8 * (3 - (w >> 30))));
    return d ? a - d : 0;
}
#else
static inline UNS64 bf_prev(UNS64 a) {          /* below 0x80 one byte, 7 bits; below 0xC0 two, 14; below 0xE0 three, 21; else four, 29 (416) */
    static const uint32_t bf_mask[5] = { 0, 0x7F, 0x3FFF, 0x1FFFFF, 0x1FFFFFFF };
    uint32_t w = bf_ld32(a - 4); unsigned t = w >> 24, l = 1 + (t >= 128) + (t >= 192) + (t >= 224);
    UNS64 d = (UNS64)(w >> (8 * (4 - l))) & bf_mask[l];
    return (d || l > 1) ? a - d : 0;
}
#endif
static inline UNS64 bf_walk(UNS64 a, UNS64 nb) {    /* THREAD-FIND: the nfa whose name is nb's, or 0 */
    unsigned m = BYTE(nb), c = m < 7 ? m : 7, k;
    uint64_t M, sig;
    if (m > 31) return 0;                           /* a count has five bits: never equal there either */
    M = 0x1Fu | ((c ? ((1ULL << (8 * c)) - 1) : 0) << 8);
    sig = bf_ld64(nb) & M;
    while (a) {
        if ((bf_ld64(a) & M) == sig) {
            for (k = 7; k < m && BYTE(a + 1 + k) == BYTE(nb + 1 + k); k++) ;
            if (k >= m) return a;
        }
        a = bf_prev(a);
    }
    return 0;
}
#endif
/*  Iteration 402: a name's walk down one thread - bf_walk's in a bfind design, else the plain one - as one
 *  macro, taken by THREAD-FIND and (FIND) here and by tools/gen-tos.py's TOS bodies of them: those, written
 *  before the gene, had the plain walk, and bfind was inert in every TOS design (Iteration 399).  */
#if BFIND
#define NAME_WALK(a_, nb_) ((a_) = bf_walk((a_), (nb_)))
#else
#define NAME_WALK(a_, nb_) do { UNS8 wn_ = BYTE(nb_); while (a_) { if ((BYTE(a_) & 31) == wn_) { UNS64 wk_ = 0; \
    while (wk_ < wn_ && BYTE((a_) + 1 + wk_) == BYTE((nb_) + 1 + wk_)) wk_++; if (wk_ == wn_) break; } (a_) = PREVNFA(a_); } } while (0)
#endif
#if X_JIT
/*  Iteration 218: JIT_PRICE - a profiling build in which the JIT translates
 *  as it would but native code never runs: every operation of every word it
 *  translated is dispatched as bytecode, so the profiler counts it, and the
 *  translator's dump lists the operations (lab/evolve/jitstack.py). A
 *  translated word keeps its header, so the translations that follow see what
 *  they would have seen. Never in a design's engine.  */
#ifndef JIT_PRICE
#define JIT_PRICE 0
#endif
#if JIT_PRICE
#define JIT_NATIVE(f) 0                 /* translated, run as bytecode */
#define JIT_REPOINT(f) ((f) < 2)        /* a translated word keeps its header */
#else
#define JIT_NATIVE(f) ((f) > 1)
#define JIT_REPOINT(f) 1
#endif
/*  Iteration 239, the gene jitos: the translator compiled for size. It runs
 *  once per word translated, not per instruction - jit_body alone is 3.5 KB
 *  at -O2; -Os takes 400-800 bytes off a JIT engine (results/price-stencils-
 *  bloom.md). The stencils it copies are compiled apart (spn-stencils.c),
 *  untouched; translation speed is the trade evolution weighs.  */
#if JITOS
#pragma GCC push_options
#pragma GCC optimize ("Os")
#endif
#include "jit.c"        /* JIT.md (Iteration 80): SPN's stencils, read, copied and patched */
#if JITOS
#pragma GCC pop_options
#endif
#endif

/*
 *  Macroses for stack access
 */

#define RS       CELL(rp)                    /* top of return stack     */
#define DS0      CELL(dsp)                   /* top of data stack       */
#define DS1      CELL(dsp + CELL_BYTES)      /* 2nd element on d.stack  */
#define DS2      CELL(dsp + 2 * CELL_BYTES)  /* 3d element on d.stack   */
#define DS3      CELL(dsp + 3 * CELL_BYTES)  /* 4th element on d.stack  */
/*  Both stacks grow DOWN, and both are checked on every push. A push
 *  is the only way either of them can grow, so this is the complete
 *  set of sites - there is no cheaper subset that still catches
 *  runaway recursion and runaway loops both. Measured on fib.4, which
 *  is call- and push-dense by construction: see PROGRESS.md's
 *  Iteration 151 entry for the numbers.  */
#if GUARD
#define PUSH(x)  do { dsp -= CELL_BYTES; DS0 = x; } while (0)
#else
#define PUSH(x)  do { dsp -= CELL_BYTES;                              \
                      if (dsp < dsp_limit) stack_fault(0);            \
                      DS0 = x; } while (0)  /* pushes x to data stack  */
#endif
#if GUARD
#define RPUSH(x) do { rp -= CELL_BYTES; RS = x; } while (0)
#else
#define RPUSH(x) do { rp -= CELL_BYTES;                               \
                      if (rp < rp_limit) stack_fault(1);              \
                      RS = x; } while (0)   /* pushes x to return stack*/
#endif

/*
 *  VM memory. +(CELL_BYTES-1) is necessary to be able to allocate
 *  MEMSIZE bytes from a CELL_BYTES-aligned address in order to have
 *  native word access.
 */

#ifndef GUARD
/*  GUARD: catch stack overflow with an unreadable page below each
 *  stack instead of a compare on every push. The checks cost 5-6% of
 *  run time (measured); a guard page costs nothing in the loop and is
 *  exact rather than probabilistic. Needs an MMU, so a target without
 *  one (MSP430) builds with GUARD=0 and keeps the checks.  */
#define GUARD 0   /* 1: guard pages. See PROGRESS.md 206 - one
                    * tests/diff case (tilde) regresses, not yet diagnosed. */
#endif
#if STACKSEP
#include <sys/mman.h>
#if GUARD
#include <signal.h>
#endif
#define PAGE 4096
static UNS8 stackmem[RSTACK_BYTES + DSTACK_BYTES] __attribute__((aligned(PAGE)));   /* the stacks' own chunk */
static UNS8 *mem;                                                  /* the dictionary: mmap'd at load */
#define STK_END ((UNS64)(uintptr_t)stackmem + RSTACK_BYTES + DSTACK_BYTES)
#else
#if GUARD
#include <sys/mman.h>
#include <signal.h>
#define PAGE 4096
static UNS8 mem[MEMSIZE + CELL_BYTES - 1] __attribute__((aligned(PAGE)));
#else
static UNS8 mem[MEMSIZE + CELL_BYTES - 1];
#endif
#define STK_END ((UNS64)(uintptr_t)base + MEMSIZE)
#endif

/*
 *  1st CELL_BYTES-aligned address in mem array. Base address of the
 *  system.
 */

static UNS8 *base;

/* VM registers and related variables */

#if REG
static UNS64  g_ip, g_rp, g_dsp;
#define VMREGS UNS64 ip = g_ip, rp = g_rp, dsp = g_dsp, t; const UNS64 dsp_limit = g_dsp_limit, rp_limit = g_rp_limit;
#if defined(REGPIN) && REGPIN && defined(__x86_64__)
/*  Iteration 197, the gene regpin (Gforth's build tuning: explicit register
 *  allocation, results/forth-implementations-survey.md): the VM registers
 *  pinned to callee-saved machine registers, in one of three assignments -
 *  they live across every call and system call the engine makes. GCC keeps a
 *  local register variable in its register where it can; whether that helps
 *  the 10 KB dispatch function is the laptop's measurement. 0: GCC chooses.  */
#undef VMREGS
#if REGPIN == 1
#define VMREGS register UNS64 ip asm("rbx") = g_ip; register UNS64 rp asm("r12") = g_rp; \
               register UNS64 dsp asm("r13") = g_dsp; UNS64 t; const UNS64 dsp_limit = g_dsp_limit, rp_limit = g_rp_limit;
#define TOSREG "r14"
#elif REGPIN == 2
#define VMREGS register UNS64 ip asm("r12") = g_ip; register UNS64 rp asm("r13") = g_rp; \
               register UNS64 dsp asm("r14") = g_dsp; UNS64 t; const UNS64 dsp_limit = g_dsp_limit, rp_limit = g_rp_limit;
#define TOSREG "r15"
#else
#define VMREGS register UNS64 ip asm("r15") = g_ip; register UNS64 rp asm("r14") = g_rp; \
               register UNS64 dsp asm("rbx") = g_dsp; UNS64 t; const UNS64 dsp_limit = g_dsp_limit, rp_limit = g_rp_limit;
#define TOSREG "r12"
#endif
#endif
#else
static UNS64 ip, rp, dsp, t;
#define g_ip ip
#define g_rp rp
#define g_dsp dsp
#define g_dsp_limit dsp_limit
#define g_rp_limit rp_limit
#define VMREGS
#endif

/*  Floors for the two stacks, both set once in main() and never
 *  changed. Kept as plain variables rather than recomputed from base
 *  at each check so the hot path compares against something already
 *  in a register.  */
#if REG
static UNS64 g_dsp_limit, g_rp_limit;
#else
static UNS64 dsp_limit, rp_limit;
#endif

/*
 *  8-byte magic every image starts with: "RELF" + cell width + 3
 *  reserved bytes. Always 8 bytes on disk regardless of the engine's
 *  own cell width - it's a fixed file-format constant, not a cell.
 *  Plain byte comparison - see cross.4's SAVE-IMAGE for why this needs
 *  no endianness handling of its own.
 */

#if ENC == 1
static const UNS8 IMAGE_MAGIC[8] = { 'S', 'O', 'D', '1', CELL_BYTES, 0, 0, 0 };
#elif ENC == 3
/*  Header bytes 0-7. Byte 6 is a FORMAT VERSION and byte 7 a FEATURE
 *  BITMAP, so an engine can tell what an image needs instead of the
 *  widths being implied by the magic string. Widening a field in future
 *  sets a bit here rather than breaking the format.  */
/*  CV8: Compressed-pointer, Variable-length, 8-bit units. The compressed
 *  pointer is CPT16's - a call target is base + (v << SCALE) - the unit
 *  narrows from 16 bits to 8, and the middle term is the difference that
 *  matters: unlike CPT16, an operation is not one fixed-width token. An
 *  opcode is one byte, a call two or three.  */
#define CV8_VERSION 1
#define F_VARCALL 0x01   /* calls are 2 or 3 bytes                      */
#define F_VARSLOT 0x02   /* slot operands are 2 or 3 bytes              */
#define F_SPEC    0x04   /* specialised opcodes present (locals header) */
#define F_LIT64   0x08   /* LIT64 may appear                            */
#define F_HOTCALLS 0x20  /* one-byte calls: 0xE0-0xFF through a table   */
#define F_TAG2    0x40   /* the two-bit tag (FORMAT-TAG2.md)             */
#define F_BYTEHDR 0x10   /* dictionary headers are byte-granular: a 1-3
                            byte link with its tag last, unpadded names.
                            The engine never reads a link in this
                            encoding, so it accepts this unconditionally;
                            the flag exists so an ENC=1 build, which does
                            walk links, can refuse. */
static const UNS8 IMAGE_MAGIC[8] = { 'C', 'V', '8', '0' + SCALE, CELL_BYTES,
    SPEC ? 'L' : 0, CV8_VERSION,
    (VARCALL ? F_VARCALL : 0) | (VARSLOT ? F_VARSLOT : 0)
        | (SPEC ? F_SPEC : 0) | F_LIT64 | F_BYTEHDR | (HOTCALLS ? F_HOTCALLS : 0)
        | (TAG2 ? F_TAG2 : 0) };
#else
static const UNS8 IMAGE_MAGIC[8] = { 'C', 'P', 'T', '0' + SCALE, CELL_BYTES, 0, 0, 0 };
#endif

/*
 *  write() wrapper: don't care about partial writes here, only used for
 *  short fixed error/usage messages before exit.
 */

static void write_str(int fd, const char *s);
static void stack_fault(int which) __attribute__((noreturn, cold));

/* Read/write the full requested amount, looping over short reads/writes.
 * Returns bytes transferred, or a negative value on a real error. */
static long full_read(int fd, void *buf, long count) {
    long total = 0, n;
    UNS8 *p = (UNS8*)buf;
    while (total < count) {
        n = read(fd, p + total, count - total);
        if (n == 0) break;   /* EOF, not an error */
        if (n < 0) return n; /* real error */
        total += n;
    }
    return total;
}

static long full_write(int fd, const void *buf, long count) {
    long total = 0, n;
    const UNS8 *p = (const UNS8*)buf;
    while (total < count) {
        n = write(fd, p + total, count - total);
        if (n < 0) return n;
        if (n == 0) return -1; /* no progress, avoid spinning forever */
        total += n;
    }
    return total;
}

static void write_str(int fd, const char *s) {
    (void)full_write(fd, s, (long)strlen(s));
}

/*
 *  Report an exhausted stack and stop. There is deliberately no
 *  attempt to recover into the Forth interpreter: by the time either
 *  pointer is out of bounds the system has usually been running away
 *  for a while, and ABORTing back into QUIT would need a working data
 *  stack to do it with. Diagnosing the condition is the whole point -
 *  what this replaces is silent dictionary corruption followed much
 *  later by a bare "Segmentation fault", which named neither the
 *  stack involved nor the fact that a stack was involved at all.
 *
 *  Status 70 (EX_SOFTWARE) rather than 1, so a test harness can tell
 *  an engine fault from a Forth-level ABORT.
 */
#if GUARD
/*  One unreadable page below each stack. The data stack's guard sits
 *  below its floor; the return stack's sits between the two stacks, so
 *  a return-stack overflow traps instead of quietly eating the data
 *  stack. Both are inside mem, so nothing else has to move.  */
static UNS64 g_dguard, g_rguard, g_ctop;
static char g_altstack[16384];   /* the handler's own stack: a C-stack overflow leaves none */
static void t_flush(void);
/*  Iteration 119 (the ANS tests found it, results/forth-collection.md): which
 *  stack, which way - a stack meets its guard at the page's near edge. The
 *  data stack UNDERFLOWS into the bottom of the return stack's guard (it
 *  starts right below it), the return stack overflows into its top; the data
 *  stack overflows into the top of its own guard, the dictionary grows into
 *  its bottom. Called "return stack overflow" before, for a data stack
 *  underflow. And the output written so far is flushed first - it was lost -
 *  and the status is 70, an engine fault, as stack_fault's.  */
static void guard_trap(int sig, siginfo_t *si, void *uc) {
    UNS64 a = (UNS64)(uintptr_t)si->si_addr;
    const char *m = "relf: segmentation fault (not a stack guard)\n";
    (void)sig; (void)uc;
    if (a >= g_rguard && a < g_rguard + PAGE)
        m = a < g_rguard + PAGE / 2 ? "relf: data stack underflow\n" : "relf: return stack overflow\n";
    else if (a >= g_dguard && a < g_dguard + PAGE)
        m = a >= g_dguard + PAGE / 2 ? "relf: data stack overflow\n" : "relf: dictionary full\n";
    else if (a < g_ctop && a > g_ctop - (64u << 20))   /* below main's frame: the C stack -  */
        m = "relf: native (C) stack overflow\n";        /* the JIT's native words call on it */
    t_flush();
    write_str(2, m);
    _exit(70);
}
/*  The regions, top down:
 *      [rfloor, MEMSIZE)        return stack
 *      [rfloor - PAGE, rfloor)  GUARD - return stack overflow
 *      [dfloor, rfloor - PAGE)  data stack
 *      [dfloor - PAGE, dfloor)  GUARD - data stack overflow (and the
 *                               dictionary growing up into the stacks)
 *  The two guard pages come out of the data stack, so the stacks stay
 *  where they were and only the usable data depth shrinks by 8 KB. */
static void install_guards(UNS8 *b) {
    UNS64 dfloor = STK_END - RSTACK_BYTES - DSTACK_BYTES;   /* the stacks' top: their own chunk with STACKSEP */
    UNS64 rfloor = STK_END - RSTACK_BYTES;
    (void)b;
    struct sigaction sa;
    stack_t ss;
    ss.ss_sp = g_altstack; ss.ss_size = sizeof g_altstack; ss.ss_flags = 0;
    sigaltstack(&ss, (stack_t *)0);
    g_ctop = (UNS64)(uintptr_t)&ss;
    mprotect((void *)(uintptr_t)(rfloor - PAGE), PAGE, PROT_NONE);
    mprotect((void *)(uintptr_t)dfloor, PAGE, PROT_NONE);
    g_dguard = dfloor; g_rguard = rfloor - PAGE;
    sa.sa_sigaction = guard_trap;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_SIGINFO | SA_ONSTACK;
    sigaction(SIGSEGV, &sa, (struct sigaction *)0);
    sigaction(SIGBUS, &sa, (struct sigaction *)0);
}
#endif

#if !GUARD
/*  Iteration 252: a fault handler in every engine, not only the guard gene's.
 *  A runaway pointer (0 @) killed 114 of seed 46's 127 front designs with a
 *  bare SIGSEGV, and those whose output waited in a buffer for a pipe or a
 *  file lost it. This one flushes it (t_flush: the engine's buffer and, at
 *  fsys 4-5, the Forth side's), reports, and exits 70 as guard_trap does; the
 *  guard gene adds the guard pages, the handler's own stack, and the messages
 *  that say which stack.  */
static void t_flush(void);
static void fault_trap(int sig) {
    (void)sig;
    t_flush();
    write_str(2, "relf: segmentation fault\n");
    exit(70);
}
#if RTLIB
/*  Without the C library (engine/rt-linux-*.c): the runtime's rt_fault fills the
 *  kernel's struct itself - sigaction's general conversion cost ~300 bytes.  */
void rt_fault(void (*h)(int));
#define install_fault_trap() rt_fault(fault_trap)
#else
#include <signal.h>
static void install_fault_trap(void) {
    struct sigaction sa;
    sa.sa_handler = fault_trap;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGSEGV, &sa, (struct sigaction *)0);
    sigaction(SIGBUS, &sa, (struct sigaction *)0);
}
#endif
#endif

/*  Iteration 257: the engine's opens, through rt_open where the runtime is
 *  linked - three arguments, no va_list: the C library's variadic open made
 *  the runtime's set up a register save area (open was 95 bytes).  */
#if RTLIB
int rt_open(const char *p, int flags, int mode);
#define OPEN3(p, f, m) rt_open((p), (f), (m))
#else
#define OPEN3(p, f, m) open((p), (f), (m))
#endif

static void stack_fault(int which) {
    write_str(2, which ? "relf: return stack overflow\n"
                       : "relf: data stack overflow\n");
    exit(70);
}

/*
 *  Multiply two cell-width unsigned numbers *a and *b.
 *  High half of the double-width result in *a, low half in *b.
 *  Divide a double-width unsigned number (high half *b, low half *c) by
 *  a cell-width unsigned number in *a. Quotient in *b, remainder in *c.
 *
 *  On a 64-bit host this needs a genuine 128-bit intermediate (the
 *  GCC/Clang __int128 extension); on a 32-bit host a plain "unsigned
 *  long long" (guaranteed >=64 bits by the C standard) is already wide
 *  enough for a 64-bit intermediate, no extension needed.
 */

#if CELL_BYTES == 8
static void umul(UNS64 *a, UNS64 *b) {
    unsigned __int128 p = (unsigned __int128)(*a) * (unsigned __int128)(*b);
    *a = (UNS64)(p >> 64);
    *b = (UNS64)p;
}
#if defined(__x86_64__)
/*  Iteration 102 (an engine trim): the CPU's 128/64 divide, not libgcc's
 *  __udivmodti4 (430 bytes in every engine). The C below truncates a
 *  quotient that does not fit 64 bits, where divq would fault: so the high
 *  half is reduced modulo the divisor first - the low 64 bits of the
 *  quotient and the remainder are the same. A zero divisor faults, as the
 *  library's division did.  */
static void udiv(UNS64 *a, UNS64 *b, UNS64 *c) {
    UNS64 d = *a, hi = *b, lo = *c, q, r;
    if (d && hi >= d) hi %= d;
    __asm__("divq %4" : "=a"(q), "=d"(r) : "a"(lo), "d"(hi), "rm"(d));
    *b = q; *c = r;
}
#else
static void udiv(UNS64 *a, UNS64 *b, UNS64 *c) {
    unsigned __int128 dividend =
        ((unsigned __int128)(*b) << 64) | (unsigned __int128)(*c);
    UNS64 divisor = *a;
    *b = (UNS64)(dividend / divisor);
    *c = (UNS64)(dividend % divisor);
}
#endif
#else
static void umul(UNS64 *a, UNS64 *b) {
    unsigned long long p = (unsigned long long)(*a) * (unsigned long long)(*b);
    *a = (UNS64)(p >> 32);
    *b = (UNS64)p;
}
static void udiv(UNS64 *a, UNS64 *b, UNS64 *c) {
    unsigned long long dividend =
        ((unsigned long long)(*b) << 32) | (unsigned long long)(*c);
    UNS64 divisor = *a;
    *b = (UNS64)(dividend / divisor);
    *c = (UNS64)(dividend % divisor);
}
#endif

/*
 *  virtual machine I/O primitives' shared state
 */

static const int open_flags[10] = {
    O_WRONLY | O_CREAT | O_TRUNC,  /* w  */
    O_WRONLY | O_CREAT | O_TRUNC,  /* wb : same, no text/binary distinction */
    O_RDONLY,                      /* r  */
    O_RDONLY,                      /* rb */
    O_RDWR,                        /* r+ */
    O_RDWR,                        /* r+b */
    O_WRONLY | O_CREAT | O_APPEND, /* a  - added for shell.4's ">>" (see
                                       PROGRESS.md, Iteration 7): none of
                                       the original six modes create a
                                       missing file *without* truncating
                                       it, which append redirection needs */
    O_WRONLY | O_CREAT | O_APPEND, /* ab : same */
    O_RDWR | O_CREAT | O_TRUNC,    /* w+ : CREATE-FILE with R/W - created to read and write (Iteration 168) */
    O_RDWR | O_CREAT | O_TRUNC     /* w+b: same */
};

/*
 *  This function reads binary forth image from file into memory.
 */

#define MAX_THREADS 4096
#define MAX_TAILS 16
static UNS64 nwords;
static UNS64 loc_hdr[5];   /* SPEC: lsp, lstk, lmax, lsave, lrestore (offsets) */
#if ENC == 3
static UNS64 throw_off;    /* Iteration 229: THROW's body (offset), from the header - 0: none */
/*  Iteration 229: a zero divisor is -10 THROW (Forth 2012's "division by
 *  zero"), not the CPU's fault: -10 where the divisor was, then a call to
 *  THROW, as LSAVE's fallback calls a Forth word. Its dispatch is a macro of
 *  its own, so a superinstruction that copies UM/MOD's body (gen-super.py)
 *  does not run its second operation after it, and the cached-top engine
 *  refills its top first (gen-tos.py redefines DIV0_DISPATCH as FILLNEXT).
 *  Macros, so UM/MOD stays one line for the generators that read handlers.  */
#ifndef DIV0_DISPATCH
#define DIV0_DISPATCH() NEXT()
#endif
#define DIV0() do { DS0 = (UNS64)-10; RPUSH(ip); ip = cbase + throw_off; TRACE_CALL(); DIV0_DISPATCH(); } while (0)
#define DIV0_CHECK() do { if (!DS0 && throw_off) DIV0(); } while (0)
#else
#define DIV0_CHECK() do { } while (0)
#endif
#if ENC == 3 && HOTCALLS
static UNS64 hot_tab[32];  /* one-byte calls: image offsets, from the header */
#endif

static void load_image(const char *name) {
    int fd;
    long len;
    UNS8 magic[8];
    UNS64 head_nfa, ntails, nfa, link, nthreads;
    /*  Iteration 228: static, not on the C stack - 32 KB there, and the
        compiler's stack-clash protection (Ubuntu's default) probed every page
        of it at each start: 8 pages of every run's memory, for the 16 to 128
        heads an image has. In BSS only the pages written count.  */
    static UNS64 heads[MAX_THREADS];
    UNS64 tail_w[MAX_TAILS], tail_o[MAX_TAILS];
    long i, n;

    fd = OPEN3(name, O_RDONLY, 0);
    if (fd < 0) {
        write_str(2, "Cannot open image file.\n");
        exit(2);
    }
    /* Iteration 257: the magic's first four bytes as one 32-bit compare and the
     * fifth alone - memcmp, its only caller here, was 42 bytes of every engine */
    if (full_read(fd, magic, 8) != 8
        || ((uint32_t)magic[0] | (uint32_t)magic[1] << 8 | (uint32_t)magic[2] << 16 | (uint32_t)magic[3] << 24)
           != ((uint32_t)IMAGE_MAGIC[0] | (uint32_t)IMAGE_MAGIC[1] << 8 | (uint32_t)IMAGE_MAGIC[2] << 16 | (uint32_t)IMAGE_MAGIC[3] << 24)
        || magic[4] != IMAGE_MAGIC[4]) {
        write_str(2, "not a RelF image, or built for a different encoding "
                     "or cell width.\n");
        exit(2);
    }
    /*  Bytes 6-7 are a format version and a FEATURE BITMAP. The engine
     *  runs any image whose required features it implements, so adding
     *  a feature later does not invalidate older images, and an older
     *  engine refuses a newer image cleanly instead of misreading it. */
    if (magic[6] > IMAGE_MAGIC[6]) {
        write_str(2, "image is a newer CV8 format version than this engine\n");
        exit(2);
    }
    if (magic[7] & ~IMAGE_MAGIC[7]) {
        write_str(2, "image needs CV8 features this engine was not built "
                     "with (varcall/varslot/spec/lit64)\n");
        exit(2);
    }
    /*
     *  Header, after the magic: the newest word's NFA as an offset, the
     *  number of DOES> tail entries, then that many (word number, byte
     *  offset) pairs.
     *
     *  The word table is DERIVED, not saved - it holds absolute
     *  addresses and would not survive relocation. It is rebuilt here by
     *  walking the link chain, which is the same walk FIND does. The
     *  tail entries exist because a DOES>-created word's body begins
     *  with a call to a MID-WORD address, and a call token can only name
     *  a word start; there are exactly two such addresses in the image,
     *  so the header describes how to finish deriving the table rather
     *  than carrying the table itself.
     */
    /*  The word list is HASHED, so there is no single chain to walk and
     *  the header carries every thread head: a count, then that many
     *  START-relative offsets. Only SOD16 uses them - it is the one
     *  encoding that names a call by word NUMBER - but the header has
     *  one shape for every encoding.  */
    if (full_read(fd, (UNS8*)&nthreads, CELL_BYTES) != CELL_BYTES) {
        write_str(2, "Truncated image header.\n");
        exit(2);
    }
    if (nthreads < 1 || nthreads > MAX_THREADS) {
        write_str(2, "Image declares an impossible thread count.\n");
        exit(2);
    }
    for (i = 0; i < nthreads; i++)
        if (full_read(fd, (UNS8*)&heads[i], CELL_BYTES) != CELL_BYTES) {
            write_str(2, "Truncated image header.\n");
            exit(2);
        }
    head_nfa = heads[0];
    if (full_read(fd, (UNS8*)&ntails, CELL_BYTES) != CELL_BYTES) {
        write_str(2, "Truncated image header.\n");
        exit(2);
    }
    if (ntails > MAX_TAILS) {
        write_str(2, "Image declares too many DOES> tails.\n");
        exit(2);
    }
#if SPEC
    /* locals opcodes: save-stack variable, buffer, limit, fallback words */
    for (i = 0; i < ntails; i++) {
        UNS64 w_, o_;
        if (full_read(fd, (UNS8*)&w_, CELL_BYTES) != CELL_BYTES ||
            full_read(fd, (UNS8*)&o_, CELL_BYTES) != CELL_BYTES) exit(2);
        tail_w[i] = w_; tail_o[i] = o_;
    }
    /*  The locals header is present only if the image was built from a
     *  dictionary that had locals.4 loaded; a bare kernel has none. */
    if (full_read(fd, (UNS8*)loc_hdr, 5 * CELL_BYTES) != 5 * CELL_BYTES)
        loc_hdr[0] = loc_hdr[1] = 0;
    if (0)
#endif
    for (i = 0; i < ntails; i++) {
        if (full_read(fd, (UNS8*)&tail_w[i], CELL_BYTES) != CELL_BYTES ||
            full_read(fd, (UNS8*)&tail_o[i], CELL_BYTES) != CELL_BYTES) {
            write_str(2, "Truncated image header.\n");
            exit(2);
        }
    }
#if ENC == 3
    /*  Iteration 229: THROW's body, written by the converter and by
     *  SAVE-SYSTEM after the locals block - UM/MOD throws -10 there.  */
    if (full_read(fd, (UNS8*)&throw_off, CELL_BYTES) != CELL_BYTES) {
        write_str(2, "Truncated image header.\n");
        exit(2);
    }
#endif

#if ENC == 3 && HOTCALLS
    /*  Last in the header: a count byte, then that many 2-byte offsets.  */
    if (magic[7] & F_HOTCALLS) {
        UNS8 k_, b_[2];
        if (full_read(fd, &k_, 1) != 1 || k_ > 32) {
            write_str(2, "Truncated image header.\n");
            exit(2);
        }
        for (i = 0; i < k_; i++) {
            if (full_read(fd, b_, 2) != 2) {
                write_str(2, "Truncated image header.\n");
                exit(2);
            }
            hot_tab[i] = b_[0] | (UNS64)b_[1] << 8;
        }
    }
#endif
#if STACKSEP
    mem = (UNS8 *)mmap(NULL, MEMMAX, PROT_READ | PROT_WRITE,
                       MAP_PRIVATE | MAP_ANONYMOUS | MAP_NORESERVE | (CELL_BYTES == 4 ? MAP_32BIT : 0), -1, 0);
    if (mem == (UNS8 *)MAP_FAILED) { write_str(2, "no room for the dictionary\n"); _exit(1); }
#endif
    base = (UNS8*)(((UNS64)(uintptr_t)mem + CELL_BYTES - 1)
                    & ~(UNS64)(CELL_BYTES - 1));
    len = full_read(fd, base, MEMSIZE);
    close(fd);
    if (len < 0) {
        write_str(2, "Error reading image file.\n");
        exit(2);
    }

#if ENC != 1
    /*  Only SOD16 names a call by word number, so only SOD16 needs the
     *  table, and only SOD16 walks the link chain to build it. The
     *  others compute a call target from the address and never read a
     *  link - which is what lets the byte-header CV8 layout change the
     *  link's encoding without the engine knowing.  */
    (void)link; (void)nfa; (void)n;
    return;
#else
    if (magic[7] & 0x10) {
        write_str(2, "Byte-granular headers are not supported by this encoding.\n");
        exit(2);
    }
    /*  Collect every word from every thread, then sort by address.
     *
     *  A word NUMBER is its position in definition order, and the
     *  dictionary only ever grows upwards, so definition order IS
     *  ascending body address. That used to fall out of walking the one
     *  chain backwards; with a hashed word list it has to be recovered
     *  by sorting, and the sort is the definition both the loader and
     *  tools/layout.py now agree on.  */
    {
        UNS64 cap = 4096, i2, j2;
        UNS64 *nfas = malloc(cap * sizeof *nfas);
        if (!nfas) { write_str(2, "Out of memory building the word table.\n"); exit(2); }
        n = 0;
        for (i2 = 0; i2 < nthreads; i2++) {
            if (!heads[i2]) continue;
            nfa = (UNS64)(uintptr_t)base + heads[i2];
            for (;;) {
                if (n == cap) {
                    cap *= 2;
                    nfas = realloc(nfas, cap * sizeof *nfas);
                    if (!nfas) { write_str(2, "Out of memory building the word table.\n"); exit(2); }
                }
                nfas[n++] = nfa;
                link = CELL(nfa - CELL_BYTES);
                if (link == 0) break;
                nfa = (nfa - CELL_BYTES) + link;
            }
        }
        /*  Insertion sort, ascending. It runs once at load over a few
         *  hundred entries.  */
        for (i2 = 1; i2 < n; i2++) {
            UNS64 k = nfas[i2];
            for (j2 = i2; j2 > 0 && nfas[j2 - 1] > k; j2--) nfas[j2] = nfas[j2 - 1];
            nfas[j2] = k;
        }
        nwords = n;
        wordtab = malloc((n + ntails) * sizeof *wordtab);
        if (!wordtab) { write_str(2, "Out of memory building the word table.\n"); exit(2); }
        for (i2 = 0; i2 < n; i2++) {
            UNS64 nlen = (*(UNS8*)(uintptr_t)nfas[i2]) & 31;
            wordtab[i2] = nfas[i2] + ((nlen + 1 + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1));
#if SKIPPAD
            while (TOK(wordtab[i2]) == 0) wordtab[i2] += 2;
#endif
        }
        free(nfas);
        for (i = 0; i < ntails; i++) {
            if (tail_w[i] >= (UNS64)n) {
                write_str(2, "DOES> tail names a word outside the chain.\n");
                exit(2);
            }
            wordtab[n + i] = wordtab[tail_w[i]] + tail_o[i];
        }
        return;
    }
#endif
    nwords = n;
    wordtab = malloc((n + ntails) * sizeof *wordtab);
    if (!wordtab) {
        write_str(2, "Out of memory building the word table.\n");
        exit(2);
    }
    nfa = (UNS64)(uintptr_t)base + head_nfa;
    for (i = 0; i < n; i++) {
        UNS64 nlen = (*(UNS8*)(uintptr_t)nfa) & 31;
        wordtab[n - 1 - i] =
            nfa + ((nlen + 1 + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1));
#if SKIPPAD
        /* skip leading NOOP padding: calls land on the first real token */
        while (TOK(wordtab[n - 1 - i]) == 0) wordtab[n - 1 - i] += 2;
#endif
        link = CELL(nfa - CELL_BYTES);
        if (link == 0) break;
        nfa = (nfa - CELL_BYTES) + link;
    }
    for (i = 0; i < ntails; i++) {
        if (tail_w[i] >= (UNS64)n) {
            write_str(2, "DOES> tail names a word outside the chain.\n");
            exit(2);
        }
        wordtab[n + i] = wordtab[tail_w[i]] + tail_o[i];
    }
}

/*
 *  Virtual machine itself: computed-goto threaded dispatch. Each
 *  primitive is a labeled block ending in NEXT; primitive tokens are
 *  (index * CELL_BYTES) + 1, matching cross.4's PRIMITIVE numbering
 *  (stride == sizeof(void*) on this host, since dispatch-table entries
 *  are pointer-sized - which is exactly CELL_BYTES on every host this
 *  targets).
 */

#if PROFILE
#include <stdio.h>
#define PROFDUMP do { dump_prof(); TR_DUMP(); } while (0)
/*  Per address over the whole memory: they were masked to 1 MB, and code
    past it - the far tests, the far benchmark - was counted elsewhere
    (Iteration 162). Untouched pages cost nothing.  */
#define PROFOFF(a) ((unsigned)(((a) - (UNS64)(uintptr_t)base) % MEMSIZE))
static unsigned long long prof[258], pair[258][258], callc[65536], ipc[MEMSIZE], rcnt[MEMSIZE];
static unsigned long long trip[258][258][258];   /* an opcode and the two before it: the hybrid's price (Iteration 173) */
static unsigned rtgt[MEMSIZE];
#if PROFILE >= 2
/*  The tracer (Iteration 162, the owner): every call pushes a frame on a
    shadow stack - target, return address, and rp just after the push. A
    frame whose rp the live rp has passed has returned - an EXIT, a fold's
    return, R> DROP, RP! - so returns need no hook, and >R or loop data on
    the return stack cannot confuse the path. The first time an instruction
    runs: a record of its offset, the call path, the top three data-stack
    cells, and the input line being interpreted (SRC, #SRC, >IN, their
    offsets in VMTRACE_PROBES). Each frame counts the dispatches it runs
    itself; when it returns they go to its call path - folded stacks at the
    end. Output: VMTRACE. tools/vmtrace.py reads it with the converter's map. */
#ifndef TR_TOP3
#define TR_TOP3 DS0, DS1, DS2      /* gen-tos.py: the top in its register */
#endif
#define TR_MAX 4096
#define TR_PATHS (1 << 16)
#define TR_DEPTH 24
static UNS64 tr_rp[TR_MAX]; static unsigned tr_tgt[TR_MAX], tr_ret[TR_MAX];
static unsigned long long tr_self[TR_MAX], tr_hash[TR_MAX], tr_top; static int tr_n, tr_lost;
static UNS8 tr_seen[MEMSIZE / 8];
static FILE *tr_f; static long tr_probe[3] = { -1, -1, -1 };
static struct { unsigned long long h, n; int d; unsigned t[TR_DEPTH]; } tr_path[TR_PATHS];
static unsigned tr_off(UNS64 a) { return (unsigned)(a - (UNS64)(uintptr_t)base); }
static void tr_open(void) {
    if (tr_f) return;
    const char *f = getenv("VMTRACE"); tr_f = fopen(f ? f : "/dev/null", "w"); if (!tr_f) tr_f = fopen("/dev/null", "w");
    const char *p = getenv("VMTRACE_PROBES"); if (p) sscanf(p, "%ld,%ld,%ld", &tr_probe[0], &tr_probe[1], &tr_probe[2]);
}
static void tr_close_frame(void) {
    int i = tr_n - 1; unsigned long long h = tr_hash[i]; unsigned k = (unsigned)(h % TR_PATHS);
    for (int j = 0; j < TR_PATHS; j++, k = (k + 1) % TR_PATHS) {
        if (tr_path[k].h == 0) {
            int d = tr_n < TR_DEPTH ? tr_n : TR_DEPTH; tr_path[k].h = h; tr_path[k].d = d;
            for (int m = 0; m < d; m++) tr_path[k].t[m] = tr_tgt[tr_n - d + m];
        }
        if (tr_path[k].h == h) { tr_path[k].n += tr_self[i]; break; }
    }
    tr_n--;
}
static void tr_call(UNS64 ip_, UNS64 ret, UNS64 rp_) {
    tr_open();
    if (tr_n >= TR_MAX) { tr_lost++; return; }
    tr_rp[tr_n] = rp_; tr_tgt[tr_n] = tr_off(ip_); tr_ret[tr_n] = tr_off(ret); tr_self[tr_n] = 0;
    tr_hash[tr_n] = (((tr_n ? tr_hash[tr_n - 1] : 0x9E3779B97F4A7C15ull) ^ tr_tgt[tr_n]) * 0x100000001B3ull) | 1;
    tr_n++;
}
static void tr_first(unsigned o, UNS64 d0, UNS64 d1, UNS64 d2) {
    tr_open();
    int s_ = tr_n > TR_DEPTH ? tr_n - TR_DEPTH : 0;
    fprintf(tr_f, "F %u d=%d p=", o, tr_n);
    for (int i = s_; i < tr_n; i++) fprintf(tr_f, "%s%u/%u", i > s_ ? "," : "", tr_tgt[i], tr_ret[i]);
    fprintf(tr_f, " s=%lld,%lld,%lld", (long long)d0, (long long)d1, (long long)d2);
    if (tr_probe[0] >= 0) {
        UNS64 src = CELL(base + tr_probe[0]), n = CELL(base + tr_probe[1]), in = CELL(base + tr_probe[2]);
        fprintf(tr_f, " in=%llu l=", (unsigned long long)in);
        if (src >= (UNS64)(uintptr_t)base && src < (UNS64)(uintptr_t)base + MEMSIZE && n <= 4096)
            for (UNS64 i = 0; i < n && i < 160; i++) { int c = ((const UNS8 *)(uintptr_t)src)[i]; fputc(c >= 32 && c < 127 ? c : '.', tr_f); }
    }
    fputc('\n', tr_f);
}
static void tr_dump(void) {
    tr_open(); while (tr_n) tr_close_frame();
    for (int k = 0; k < TR_PATHS; k++) if (tr_path[k].n) {
        fprintf(tr_f, "P %llu", tr_path[k].n);
        for (int m = 0; m < tr_path[k].d; m++) fprintf(tr_f, "%s%u", m ? ";" : " ", tr_path[k].t[m]);
        fputc('\n', tr_f);
    }
    fprintf(tr_f, "T top=%llu lost=%d\n", tr_top, tr_lost); fclose(tr_f); tr_f = 0;
}
#define TRACE_STEP(a) do { while (tr_n && rp > tr_rp[tr_n - 1]) tr_close_frame(); \
    if (tr_n) tr_self[tr_n - 1]++; else tr_top++; \
    UNS64 o_ = (UNS64)(a) - (UNS64)(uintptr_t)base; \
    if (o_ < MEMSIZE && !(tr_seen[o_ >> 3] & (1u << (o_ & 7)))) { \
        tr_seen[o_ >> 3] |= (UNS8)(1u << (o_ & 7)); tr_first((unsigned)o_, TR_TOP3); } } while (0)
#define TRACE_CALL() tr_call(ip, RS, rp)
#define TR_DUMP() tr_dump()
#else
#define TRACE_STEP(a)
#define TRACE_CALL()
#define TR_DUMP()
#endif
static const char *prof_names[258];
static void dump_prof(void) {
    const char *f = getenv("VMPROF"); if (!f) return;
    int fd = open(f, O_WRONLY|O_CREAT|O_APPEND, 0644); char b[128];
    for (int i = 0; i < 258; i++) for (int j = 0; j < 258; j++) if (pair[i][j]) {
        int n = snprintf(b, sizeof b, "%d %d %llu\n", i, j, pair[i][j]); write(fd, b, n); }
    for (int i = 0; i < 258; i++) for (int j = 0; j < 258; j++) for (int k = 0; k < 258; k++) if (trip[i][j][k]) {
        int n = snprintf(b, sizeof b, "T %d %d %d %llu\n", i, j, k, trip[i][j][k]); write(fd, b, n); }
    for (int i = 0; i < MEMSIZE; i++) if (ipc[i]) {   /* per-address: patterns.py */
        int n = snprintf(b, sizeof b, "I %d %llu\n", i, ipc[i]); write(fd, b, n); }
    for (int i = 0; i < 65536; i++) if (callc[i]) {
        int n = snprintf(b, sizeof b, "C %d %llu\n", i, callc[i]); write(fd, b, n); }
    /* Iteration 88: every call under the tag by its return address - the
       target, the count, the byte after the call and the callee's first
       eight, read now, at the end: lab/evolve/callsites.py (calls compiled
       at run time included, which no census of the image sees) */
    for (int i = 0; i < MEMSIZE; i++) if (rcnt[i]) {
        const UNS8 *x_ = base + i, *y_ = base + rtgt[i];
        int n = snprintf(b, sizeof b, "R %d %u %llu %d %d %d %d %d %d %d %d %d\n", i, rtgt[i], rcnt[i], x_[0],
                         y_[0], y_[1], y_[2], y_[3], y_[4], y_[5], y_[6], y_[7]); write(fd, b, n); }
#if X_JIT
    jit_dump(fd);                                  /* Iteration 90: what the JIT left bytecode, and why */
#endif
    close(fd);
}
static int prev_op = 257, prev_op2 = 257;
#define PROFC(t) (callc[t]++)
#define PROFIP(a) do { ipc[PROFOFF(a)]++; TRACE_STEP(a); } while (0)
#define PROF(k) do { pair[prev_op][k]++; trip[prev_op2][prev_op][k]++; prev_op2 = prev_op; prev_op = (k); } while (0)
#define PROFRET(r, t) do { unsigned o_ = PROFOFF(r); \
                           rcnt[o_]++; rtgt[o_] = (unsigned)(t); } while (0)
#else
#define PROFRET(r, t)
#define PROF(k)
#define PROFC(t)
#define PROFIP(a)
#define PROFDUMP
#define TRACE_CALL()
#endif

/*
 *  Buffered terminal I/O.
 *
 *  KEY and EMIT used to do one read(2) or write(2) PER CHARACTER. On a
 *  host where a syscall is cheap that is merely wasteful; on real
 *  hardware with the usual mitigations it dominates every workload that
 *  touches text. Running the 616-case CORE corpus made 26,950 one-byte
 *  reads of stdin and 5,373 one-byte writes: 32,357 syscalls against
 *  SOD32's 59 for the identical input, because SOD32 reads in blocks.
 *
 *  That is not a small constant. Measured on two machines, the same
 *  build was 5x slower on the faster CPU, purely because its syscalls
 *  cost more - and the constant is identical for every stage, so it also
 *  compressed every ratio in the comparison towards 1.0 and hid the
 *  differences the benchmarks exist to show.
 *
 *  Ordering is the thing to get right. Output is flushed before any
 *  read of stdin, so a prompt appears before the input it asks for;
 *  before any other write to fd 1, so interleaving is preserved; and
 *  before exit, fork and exec, so nothing is lost or duplicated into a
 *  child.
 */
#define TIOBUF 4096
static int  t_seek0 = -1;          /* can descriptor 0 seek? -1: not asked yet (Iteration 104) */
static UNS8 t_obuf[TIOBUF];
static int  t_olen = 0;


/*
 *  Buffered READ-LINE for FILES, the same problem as KEY and EMIT and a
 *  larger one. Cross-compiling the kernel reads extend.4, cross.4 and
 *  kernel.4 - about 62 KB of source - and READ-LINE was doing
 *  read(fd, &c, 1) for every byte of it: 67,316 syscalls for one build.
 *
 *  The OS file offset has to stay honest, because REPOSITION-FILE,
 *  FILE-POSITION and READ-FILE all depend on it and none of them know
 *  about this buffer. So any of those drops the buffer first, seeking
 *  back over whatever was read ahead and not yet consumed.
 */
/*  These MUST NOT be inlined into virtual_machine(). They are cold I/O
 *  paths with loops and static state; inlined, they wreck register
 *  allocation across the whole dispatch function and the VM registers
 *  stop living in registers. Measured: the specialised CV8 engine went
 *  from 9.5 ms to 17.6 ms on a workload that reads no files at all,
 *  same image, same input - an 85% loss from adding a function nothing
 *  in that run ever called. Iteration 189a found the same class of
 *  problem from the other direction, when the VM registers were
 *  file-scope statics.  */
#define NOINLINE_IO __attribute__((noinline))
#ifndef FBUFN
#define FBUFN  8
#endif
#ifndef FBUFSZ
#define FBUFSZ 4096
#endif
/*  Iteration 225: the slots' state together, their buffers apart. With each
    buffer inside its slot, t_fslot's scan of the fd fields touched one page a
    slot - 8 pages (32 KB) at 4 KB buffers, the first time any file was read -
    and the fbuf gene bought that back with smaller buffers and more read(2).
    Apart, the scan touches the state's one page; a buffer is touched when its
    slot reads.  */
static UNS8 t_fbb[FBUFN][FBUFSZ];
static struct fbuf { int fd, len, pos, raw; UNS8 *b; } t_fb[FBUFN];

NOINLINE_IO static struct fbuf *t_fslot(int fd) {
    int i, free_ = -1;
    for (i = 0; i < FBUFN; i++) {
        if (t_fb[i].fd == fd) return &t_fb[i];
        if (t_fb[i].fd == 0 && free_ < 0) free_ = i;   /* 0 marks unused */
    }
    if (free_ < 0) return 0;                           /* fall back to raw */
    t_fb[free_].fd = fd; t_fb[free_].len = t_fb[free_].pos = 0; t_fb[free_].b = t_fbb[free_];
    /* Iteration 104 (relf's READ-LINE): a descriptor that cannot seek - a
       pipe, a FIFO, a terminal - is read a byte at a time: a byte read
       ahead could not be given back, and the other end is shared with
       whatever reads next. Asked once, when the descriptor gets its slot. */
    t_fb[free_].raw = lseek(fd, 0, SEEK_CUR) < 0;
    return &t_fb[free_];
}

NOINLINE_IO static void t_fdrop(int fd) {
    int i;
    for (i = 0; i < FBUFN; i++) if (t_fb[i].fd == fd) {
        int un = t_fb[i].len - t_fb[i].pos;
        if (un > 0) lseek(fd, -(off_t)un, SEEK_CUR);
        t_fb[i].fd = 0; t_fb[i].len = t_fb[i].pos = 0;
    }
}

/*  Next byte of fd: >=0 a character, -1 end of file, -2 error.  */
NOINLINE_IO static int t_fgetc(int fd) {
    struct fbuf *f = t_fslot(fd);
    long n;
    if (!f || f->raw) { UNS8 c; n = read(fd, &c, 1);
              return n == 1 ? (int)c : (n == 0 ? -1 : -2); }
    if (f->pos >= f->len) {
        n = read(fd, f->b, FBUFSZ);
        if (n < 0) return -2;
        if (n == 0) return -1;
        f->len = (int)n; f->pos = 0;
    }
    return f->b[f->pos++];
}

#if FSYS >= 4
/*  Iteration 207, fsys 4: the Forth output buffer (forth/file-sysc4.4) - its
 *  [address, fill], registered by SYSCALL -5 - is flushed wherever t_obuf
 *  is: before every system call, before a read blocks, at every exit, the
 *  faults' included. The flush points are the native engine's, unchanged.  */
static UNS64 *g_fbuf;
#endif
NOINLINE_IO static void t_flush(void) {
    if (t_olen) { full_write(1, t_obuf, (size_t)t_olen); t_olen = 0; }
#if FSYS >= 4
    if (g_fbuf && g_fbuf[1]) { full_write(1, (const void *)(uintptr_t)g_fbuf[0], (size_t)g_fbuf[1]); g_fbuf[1] = 0; }
#endif
}

/*  WRITE and READ - primitives 30 and 31, where EMIT and KEY were; the
 *  kernel builds EMIT, KEY and TYPE on them in Forth. The same buffers as
 *  before: WRITE adds to t_obuf, flushed when full and wherever it was
 *  flushed before. Out of line, like every I/O path here.
 *
 *  Input has no buffer (Iteration 104, the owner - relf's KEY and
 *  READ-LINE, forth/kernel.4 there): descriptor 0 is inherited, shared
 *  with every child, and a byte read ahead is a byte taken from whatever
 *  runs next - with 4096 bytes held here, `read x; cat` lost the pipe to
 *  the engine. READ still hands over at most a line: from a descriptor 0
 *  that can seek, a block and a seek back to just after the line; from
 *  anything else, a byte per read(2), up to the first character ACCEPT
 *  treats specially - LF, CR, backspace, DEL - or the count asked for.  */
/*  Iteration 231: output to a terminal is not held (the owner's rule,
 *  Gforth's: Iteration 202) - descriptor 1 asked once, at the first WRITE,
 *  as fsys 4's FS-OINIT asks in Forth; a terminal gets each WRITE at once.  */
static int t_otty = -1;
NOINLINE_IO static void t_write(const UNS8 *p, UNS64 n) {
    while (n) {
        UNS64 k;
        if (t_olen == TIOBUF) t_flush();
        k = (UNS64)(TIOBUF - t_olen);
        if (k > n) k = n;
        memcpy(t_obuf + t_olen, p, (size_t)k);
        t_olen += (int)k; p += k; n -= k;
    }
    if (t_otty < 0) t_otty = isatty(1) == 1;
    if (t_otty) t_flush();
}

NOINLINE_IO static int t_getc(void) {     /* READ-LINE on descriptor 0: a byte per read(2) */
    UNS8 c;
    t_flush();                         /* prompt before blocking */
    return read(0, &c, 1) == 1 ? (int)c : -1;
}
#define T_EDIT(c) ((c) == 10 || (c) == 13 || (c) == 8 || (c) == 127)
NOINLINE_IO static UNS64 t_read(UNS8 *p, UNS64 n) {
    UNS64 k = 0;
    long got;
    if (n == 0) return 0;
    t_flush();                         /* prompt before blocking */
    if (t_seek0 < 0) t_seek0 = lseek(0, 0, SEEK_CUR) >= 0;
    if (t_seek0) {                     /* a block, and what follows the line given back */
        got = read(0, p, (size_t)n);
        if (got <= 0) return 0;        /* end of input */
        while (k < (UNS64)got && !T_EDIT(p[k])) k++;
        if (k < (UNS64)got) { k++; if (k < (UNS64)got) lseek(0, (off_t)k - (off_t)got, SEEK_CUR); }
        return k;
    }
    while (k < n && read(0, p + k, 1) == 1) {  /* a byte at a time: nothing read ahead */
        UNS8 c_ = p[k++];                      /* not T_EDIT(p[k++]): a macro reads its argument four times */
        if (T_EDIT(c_)) break;
    }
    return k;
}

#if X_NUMBERQ
/*  Iteration 295, the gene knumber: NUMBER? - cv8b-knumber.4's (NUMBER?), step for
    step: a 'c' literal; DPL -1; a sign before or after the prefixes $ # %, each
    tested in turn as the Forth tests them; (>NUMBER)'s loop in that base, uppercase
    digits only; a point sets DPL to the digits after it; 0 0 0 on failure. */
static UNS64 numberq(UNS64 a, UNS64 base, UNS64 dpl, UNS64 *lo, UNS64 *hi) {
    INT64 n = BYTE(a); UNS64 s = a + 1, b = base, lo_ = 0, hi_ = 0; int neg;
    if (n == 3 && BYTE(s) == 39 && BYTE(s + 2) == 39) { CELL(dpl) = (UNS64)-1; *lo = BYTE(s + 1); *hi = 0; return (UNS64)-1; }
    CELL(dpl) = (UNS64)-1;
    neg = BYTE(s) == 45; if (neg) { n--; s++; }
    if (BYTE(s) == 36) { b = 16; n--; s++; }
    if (BYTE(s) == 35) { b = 10; n--; s++; }
    if (BYTE(s) == 37) { b = 2; n--; s++; }
    if (!neg && BYTE(s) == 45) { neg = 1; n--; s++; }
    if (n <= 0) { *lo = *hi = 0; return 0; }
    for (;;) {
        while (n) {
            INT64 d_ = (INT64)BYTE(s) - 48; UNS64 ph_, pl_;
            if (d_ < 0 || (d_ > 9 && d_ < 17)) break;
            if (d_ > 9) d_ -= 7;
            if (!(d_ < (INT64)b)) break;
            ph_ = lo_; pl_ = b; umul(&ph_, &pl_); hi_ = ph_ + hi_ * b; lo_ = pl_ + (UNS64)d_; if (lo_ < pl_) hi_++;
            s++; n--;
        }
        if (n) { if (BYTE(s) == 46) { n--; CELL(dpl) = (UNS64)n; s++; } else { *lo = *hi = 0; return 0; } }
        if (!n) break;
    }
    if (neg) { hi_ = ~hi_ + (lo_ == 0); lo_ = -lo_; }
    *lo = lo_; *hi = hi_; return (UNS64)-1;
}
#endif
#if JITRE || JITEXEC
/*  Iteration 346, the gene jitre: native code calling bytecode, as SPN's spn_interp - the stack back
 *  into memory (the top where dsp points: a nested virtual_machine fills its TOS from there), the
 *  sentinel pushed as a return address, the interpreter run from the body; its EXIT lands on the
 *  sentinel, L_x_jit "calls" the trampoline, and jit_leave longjmps here with the stack.  */
static void virtual_machine(void);
/* the compiler's own setjmp, not the C library's: an engine links no libc - its frame keeps every
   callee-saved register, which the longjmp out of the nested interpreter gives back */
static void **jit_jb;
static cell *jit_lsp; static cell jit_ltos;
static spn_st jit_leave(cell *sp, cell tos) { jit_lsp = sp; jit_ltos = tos; __builtin_longjmp(jit_jb, 1); }
static spn_st jit_interp(cell *sp, cell tos, cell body) {
    void *jb[5]; void **prev = jit_jb;
#if JITMUL
    void **prevtb = jit_tb;             /* 476: a throw's return point is the outer jit_call's again after */
#endif
    g_dsp = (UNS64)(uintptr_t)sp - CELL_BYTES; CELL(g_dsp) = (UNS64)tos;
    g_rp = (UNS64)jit_rp - CELL_BYTES; CELL(g_rp) = (UNS64)(uintptr_t)jit_sentinel;
    g_ip = (UNS64)body;
    jit_jb = jb;
    if (!__builtin_setjmp(jb)) virtual_machine();
    jit_jb = prev;
#if JITMUL
    jit_tb = prevtb;
#endif
    return SPN_ST(jit_lsp, jit_ltos);
}
#endif
static void virtual_machine(void) {
    VMREGS
#if ENC == 1
#define CALLTARGET(t) (wtab[(t) - 256])
    const UNS64 *const wtab = wordtab;
#elif ENC == 3
    /* CV8: byte stream. b < 0x80 is an opcode; otherwise b and the next
     * byte are a 15-bit scaled offset from the image base. */
    const UNS64 cbase = (UNS64)(uintptr_t)base;
#else
    /* CPT16: compressed-pointer threading. A call token is a scaled
     * offset from the image base: target = base + (t - 256) << SCALE.
     * No table, so no second dependent load. */
#define CALLTARGET(t) (cbase + ((t) << SCALE))
    const UNS64 cbase = (UNS64)(uintptr_t)base - (256u << SCALE);
#endif
#if SYSC
#if !defined(__x86_64__) && !defined(__i386__) && !defined(__arm__)
#error "the gene sysc: the image's system-call numbers are x86-64 Linux's (i386's and 32-bit ARM's mapped)"
#endif
#define SYSF DSP(L_syscall)
#define SYSX(l) DSP(L_nosys)
#else
#define SYSF DSP(L_fork)
#define SYSX(l) DSP(l)
#endif
/*  Iteration 202, the gene fsys: six file words and RESIZE in Forth over
 *  SYSCALL (forth/file-sysc.4, loaded last in the design's dump) - their
 *  handlers out of the engine, as SYSX's for the shell's words. ALLOCATE and
 *  FREE stay: SAVE-SYSTEM was compiled against them.  */
/*  Iteration 237: the dispatch table in the file as OFFSETS from L_noop, not
 *  addresses - 4 bytes an entry, not 8: about 500 bytes off every CV8 engine
 *  file. At the first entry the addresses are made once, into a copy in BSS
 *  that everything reads as it read the table before (cv8_tab, esc_tab, the
 *  tag's t2tab, the dispatch itself), so no dispatch pays for it. A signed 32-bit offset sets no limit an engine can
 *  reach (16 bits would save 256 more, and cap the interpreter at 32 KB:
 *  not taken - the owner: no limits a developer could hit). Off with
 *  -DDISPOFF=0, and where ENC is not 3; gen-tail.py turns it off (its tables
 *  hold functions). SYSF/SYSX and FSX are table entries, so DSP() too.  */
#ifndef DISPOFF
#define DISPOFF (ENC == 3)
#endif
#if DISPOFF
#define DSP(l) (&&l - &&L_noop)
#define DPTR(o) ((const void *)((const char *)&&L_noop + (o)))
#else
#define DSP(l) &&l
#define DPTR(p) (p)
#endif
#if FSYS
#define FSX(l) DSP(L_nosys)
#else
#define FSX(l) DSP(l)
#endif
/*  Iteration 205, fsys 2 - the single-SYSCALL family: OPEN-FILE, CLOSE-FILE,
 *  WRITE-FILE, ALLOCATE and FREE too (forth/file-sysc2.4); the kernel's uses
 *  of them rebound to the Forth words by the converter (--rebind).  */
#if FSYS >= 2
#define FSX2(l) DSP(L_nosys)
#else
#define FSX2(l) DSP(l)
#endif
/*  Iteration 206, fsys 3: WRITE, READ, READ-LINE and BYE too (forth/file-
 *  sysc3.4: unbuffered, no read-ahead from what cannot seek) - the engine's
 *  I/O is then SYSCALL alone.  */
#if FSYS >= 3
#define FSX3(l) DSP(L_nosys)
#else
#define FSX3(l) DSP(l)
#endif
#if DISPOFF
    static const int dispatch_o[] = {
#else
    static const void *const dispatch[] = {
#endif
        DSP(L_noop), DSP(L_exit), DSP(L_lit), DSP(L_branch), DSP(L_0branch), DSP(L_drop),
        DSP(L_dup), DSP(L_swap), DSP(L_rot), DSP(L_over), DSP(L_cfetch), DSP(L_fetch),
        DSP(L_cstore), DSP(L_store), DSP(L_and), DSP(L_or), DSP(L_xor), DSP(L_fromr),
        DSP(L_tor), DSP(L_rfetch), DSP(L_eq), DSP(L_ugt), DSP(L_gt), DSP(L_plus),
        DSP(L_negate), DSP(L_lshift), DSP(L_rshift), DSP(L_ummult), DSP(L_umdiv),
        DSP(L_dplus), FSX3(L_write), FSX3(L_read), FSX3(L_bye), DSP(L_spfetch), DSP(L_spstore),
        DSP(L_rpfetch), DSP(L_rpstore), FSX2(L_openfile), FSX2(L_closefile),
        FSX3(L_readline), FSX(L_writeline), FSX(L_readfile), FSX2(L_writefile),
        SYSX(L_system), FSX(L_reposfile), FSX(L_filepos), FSX(L_delfile), FSX(L_filesize),
        SYSF, SYSX(L_execve), SYSX(L_waitpid), SYSX(L_pipe), SYSX(L_dup2),
        SYSX(L_getenv), SYSX(L_setenv), SYSX(L_sysexit), SYSX(L_chdir), SYSX(L_getcwd),
        SYSX(L_sysargc), SYSX(L_sysarg), SYSX(L_getpid), SYSX(L_unsetenv),
        FSX2(L_allocate), FSX2(L_free), FSX(L_resize), SYSX(L_getpwhome),
        SYSX(L_getfsize), SYSX(L_setfsize),
        /*  LIT32 is not one of kernel.4's primitives. It is appended
         *  past the real ones so the table has no hole - `dispatch[255]`
         *  would have read past the end.  */
        DSP(L_lit32), DSP(L_dovar), DSP(L_dodoes),
#if ENC != 3
        /*  LIT64 at 71, the first index past DODOES. Folded opcodes
         *  start at FOLDBASE (128) and calls at 256, so 71..127 is
         *  free space in both 16-bit encodings.  */
        [71] = DSP(L_lit64t),
#endif
#if ENC == 1
        [72] = DSP(L_farcall), [73] = DSP(L_dodoesf),
#endif
#if ENC == 3
        DSP(L_lit8), DSP(L_lit8x),
        [0x7C] = DSP(L_lit64), [0x7D] = DSP(L_esc),
#endif
#if ENC == 3 && SPEC
        [0x60] = DSP(L_lit0), DSP(L_lit1), DSP(L_litm1), DSP(L_vf), DSP(L_vs),
        DSP(L_lsave), DSP(L_lrest), DSP(L_lstore), DSP(L_lzero),
        DSP(L_zeq), DSP(L_sub), DSP(L_ne), DSP(L_zlt), DSP(L_sgt), DSP(L_2dup), DSP(L_2drop),
        DSP(L_charp), DSP(L_onep), DSP(L_cellp), DSP(L_cells), DSP(L_onem), DSP(L_invert),
        DSP(L_count), DSP(L_aligned), DSP(L_addi), DSP(L_addix), DSP(L_eqi), DSP(L_eqix),
#endif
#if FOLD
#include "vm-fold-table.h"
#endif
#if SUPER   /* superinstructions: a pair of primitives per opcode (tools/gen-super.py) */
#include "vm-super-table.h"
#endif
#if OPS10   /* colon words as opcodes, at this design's slots (lab/evolve) */
#include "vm-ops10-table.h"
#endif
    };
#if DISPOFF
    static const void *dispatch[sizeof dispatch_o / sizeof dispatch_o[0]];
    if (!dispatch[0]) { int d_; for (d_ = 0; d_ < (int)(sizeof dispatch_o / sizeof dispatch_o[0]); d_++) dispatch[d_] = DPTR(dispatch_o[d_]); }
#endif
#if ENC == 3 && ESCAPE
    /*  CV8 renumbers the primitive band: the 36 non-escaped primitives
     *  keep kernel.4's order compacted into 0..35, and the 32 escaped
     *  ones are reached as ESC + index. dispatch[] is in kernel.4
     *  order, so both tables are derived from it here rather than
     *  written out twice.  */
#if ESCAPE == 2
    /*  The second level (Iteration 11): also the nine rarest of the rest -
     *  UM* UM/MOD D+ WRITE READ SP@ SP! RP@ RP! - which are the tail of
     *  the compacted band (27..35), so no opcode before them moves and the
     *  compiler's opcode constants (EXIT-OP .. 0BRANCH-OP) still hold. In
     *  kernel.4 order the escaped are then 27..67, contiguous: 41 of them,
     *  and 27..67 free - nine slots more.  */
#define ESC_N 41
    static const UNS8 esc_k[ESC_N] = { 27,28,29,30,31,32,33,34,35,36,
        37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,
        52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67 };
#else
#define ESC_N 32
    static const UNS8 esc_k[ESC_N] = { 32,
        37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,
        52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67 };
#endif
    const void *cv8_tab[128], *esc_tab[ESC_N];
    { int i_, n_ = (int)(sizeof dispatch / sizeof dispatch[0]);
      for (i_ = 0; i_ < 128; i_++) cv8_tab[i_] = (i_ < n_) ? dispatch[i_] : &&L_noop;
#if ESCAPE == 2
      for (i_ = 0; i_ < 27; i_++)  cv8_tab[i_] = dispatch[i_];
      for (i_ = 27; i_ < 68; i_++) cv8_tab[i_] = &&L_noop;          /* freed */
#else
      for (i_ = 0; i_ < 32; i_++)  cv8_tab[i_] = dispatch[i_];
      for (i_ = 32; i_ < 36; i_++) cv8_tab[i_] = dispatch[i_ + 1];  /* SP@..RP! */
      for (i_ = 36; i_ < 68; i_++) cv8_tab[i_] = &&L_noop;          /* freed */
#endif
#if SUPER   /* what this design put in the freed band (lab/evolve): */
#include "vm-super-esc.h"
#endif
#if OPS10   /* assigned here, as dispatch[36..67] still holds the escaped primitives */
#include "vm-ops10-esc.h"
#endif
      for (i_ = 0; i_ < ESC_N; i_++)  esc_tab[i_] = dispatch[esc_k[i_]]; }
#define dispatch cv8_tab
#endif
#if ENC == 3 && HOTCALLS          /* a one-byte call's entry; without, the same code as ever */
#define HCALL(i) (((i) & 0xE0) == 0xE0 ? &&L_hcall : &&do_call)
#else
#define HCALL(i) &&do_call
#endif
#if ENC == 3 && TAG2
    /*  The two-bit tag: 0x00-0x3F through this design's 64 one-byte codes,
     *  0x40-0xFF straight to the call handler of their width - no test. A
     *  code names a logical operation (vm-tag2-*.h, the converter's): below
     *  128 the table above, 128 + k the k-th escaped primitive, T2_ESC the
     *  escape, T2_NONE nothing - a fault, not a no-op.  */
#define T2_ESC  0xFFFE
#define T2_NONE 0xFFFF
/*  Iteration 95, the gene t2wide: no 3-byte call - 10xxxxxx are 64 more
 *  one-byte codes (0x80-0xBF), the calls 01 (2 bytes, 16 KB) and 11 (4
 *  bytes, 1 GB). The map's second half are those codes. */
#if T2WIDE
#define T2_ONES 128
#define T2_IS_OP(t) (((t) & 0x40) == 0)
#else
#define T2_ONES 64
#define T2_IS_OP(t) ((t) < 64)
#endif
#if X_JIT     /* the lazy JIT's opcode (JIT.md): a code, no slot in the table */
#define T2_JIT  0xFFFD
#define T2JIT(x) (x) == T2_JIT ? &&L_x_jit :
#else
#define T2JIT(x)
#endif
#if OPCALL  /* Iteration 121: the op;CALL opcodes - codes of their own under the tag
             * (logical 0xFE00 + k), no slot in the 128-entry table, as T2_JIT */
#define T2_OC0 0xFE00
    static const void *const oc_tab[] = {
#include "vm-opcall-table.h"
    };
#define T2OC(x) ((x) >= T2_OC0 && (x) - T2_OC0 < (int)(sizeof oc_tab / sizeof oc_tab[0])) ? oc_tab[(x) - T2_OC0] :
#else
#define T2OC(x)
#endif
#if ESCAPE
#define T2OP(x) (T2JIT(x) T2OC(x) (x) == T2_ESC ? &&L_t2esc : (x) == T2_NONE ? &&L_t2bad \
                 : (x) < 128 ? dispatch[(x)] : (x) - 128 < ESC_N ? esc_tab[(x) - 128] : &&L_t2bad)
#else
#define T2OP(x) (T2JIT(x) T2OC(x) (x) == T2_ESC ? &&L_t2esc : (x) >= n_ ? &&L_t2bad : dispatch[(x)])
#endif
    static const void *t2tab[256], *t2esc[256];
    if (!t2tab[0]) {
        static const UNS16 one_[T2_ONES] = {
#include "vm-tag2-one.h"
        };
        static const UNS16 esc_[256] = {
#include "vm-tag2-esc.h"
        };
        int i_, n_ = (int)(sizeof dispatch / sizeof dispatch[0]);
        (void)n_;
        for (i_ = 0; i_ < 256; i_++) {
#if T2WIDE
            t2tab[i_] = i_ < 64 ? T2OP(one_[i_]) : i_ < 128 ? &&L_t2call2
                      : i_ < 192 ? T2OP(one_[i_ - 64]) : &&L_t2call4;
#else
            t2tab[i_] = i_ < 64 ? T2OP(one_[i_]) : i_ < 128 ? &&L_t2call2
                      : i_ < 192 ? &&L_t2call3 : &&L_t2call4;
#endif
            t2esc[i_] = T2OP(esc_[i_]);
        }
    }
#endif
#if ENC == 3 && SHAREDCALL && DISPATCH256
    /*  Same handlers, but indexed by the whole byte: 0x80-0xFF all land
     *  on do_call, so no test is needed to tell an opcode from a call. */
    /*  Static, and filled once: s8 re-enters this function every time
     *  native code runs a word it could not translate, and a local table
     *  refilled on every entry made s8 two to four times slower. */
    static const void *dtab256[256];
    if (!dtab256[0]) {
        int i_, n_ = (int)(sizeof dispatch / sizeof dispatch[0]);
        for (i_ = 0; i_ < 256; i_++)
            dtab256[i_] = (i_ < n_ && i_ < 128) ? dispatch[i_] : HCALL(i_);
    }
#endif

#if ENC == 3 && TAG2
/*  One byte, one indirect jump: a call's three widths are three entries
 *  of the table, so no opcode-or-call test either.  */
#define NEXT() do { \
        PROFIP(ip); t = BYTE(ip); ip += 1; if (T2_IS_OP(t)) PROF(t); goto *t2tab[t]; \
    } while (0)
#elif ENC == 3 && SHAREDCALL
/*  Every handler keeps its own opcode dispatch (what the branch predictor
 *  needs), but the call path - decode, RPUSH, limit check - exists once.
 *  GCC otherwise replicates ~50 bytes of it into all ~120 handlers.  */
#if DISPATCH256
#define NEXT() do { \
        PROFIP(ip); t = BYTE(ip); ip += 1; PROF(t); goto *dtab256[t]; \
    } while (0)
#elif SIGNTEST
/*  Load the byte sign-extended: an opcode is then just t >= 0, one
 *  branch-on-sign (bgez / tbz / js) with no constant and no compare.
 *  RISC-V otherwise rematerialises 127 for bltu on every dispatch.  */
#define NEXT() do { \
        PROFIP(ip); t = (UNS64)(INT64)(int8_t)BYTE(ip); \
        if ((INT64)t >= 0) { ip += 1; PROF(t); goto *dispatch[t]; } \
        goto do_call; \
    } while (0)
#else
#define NEXT() do { \
        PROFIP(ip); t = BYTE(ip); \
        if (t < 0x80) { ip += 1; PROF(t); goto *dispatch[t]; } \
        goto do_call; \
    } while (0)
#endif
#elif ENC == 3
#define NEXT() do { \
        PROFIP(ip); t = BYTE(ip); \
        if (t < 0x80) { ip += 1; PROF(t); goto *dispatch[t]; } \
        t = ((t & 0x7F) << 8) | BYTE(ip + 1); ip += 2; \
        PROF(256); RPUSH(ip); ip = cbase + (t << SCALE); TRACE_CALL(); \
        goto next; \
    } while (0)
#else
#define NEXT() do { \
        t = TOK(ip); ip += 2; \
        if (t < 256) { PROF(t); goto *dispatch[t]; } \
        PROF(256); PROFC(t); RPUSH(ip); ip = CALLTARGET(t); TRACE_CALL(); \
        goto next; \
    } while (0)
#endif

next:
    NEXT();
#if ENC == 3 && TAG2
    /*  t holds the first byte (NEXT), ip is past it.  */
L_t2call2: t = ((t & 0x3F) << 8) | BYTE(ip); ip += 1; goto t2call;
#if !T2WIDE
L_t2call3: t = ((t & 0x3F) << 16) | ((UNS64)BYTE(ip) << 8) | BYTE(ip + 1); ip += 2; goto t2call;
#endif
L_t2call4: t = ((t & 0x3F) << 24) | ((UNS64)BYTE(ip) << 16) | ((UNS64)BYTE(ip + 1) << 8)
               | BYTE(ip + 2); ip += 3;
t2call:    PROF(256); PROFRET(ip, t); RPUSH(ip); ip = cbase + t; TRACE_CALL(); NEXT();
L_t2esc:   t = BYTE(ip); ip += 1; goto *t2esc[t];
L_t2bad:   write_str(2, "relf: no operation has this code\n"); exit(70);
#endif
#if ENC == 3 && SHAREDCALL
do_call:
#if DISPATCH256
    /*  ip is already past the first byte here.  */
    if (t & 0x40) { t = ((t & 0x3F) << 16) | ((UNS64)BYTE(ip) << 8) | BYTE(ip + 1);
                    ip += 2; }
    else          { t = ((t & 0x3F) << 8) | BYTE(ip); ip += 1; }
#elif VARCALL
#if HOTCALLS
    if ((t & 0xE0) == 0xE0) { ip += 1; goto L_hcall; }   /* the low byte, as SIGNTEST sign-extends */
#endif
    if (t & 0x40) {                       /* 11xxxxxx: 22-bit target */
        t = ((t & 0x3F) << 16) | ((UNS64)BYTE(ip + 1) << 8) | BYTE(ip + 2);
        ip += 3;
    } else {                              /* 10xxxxxx: 14-bit target */
        t = ((t & 0x3F) << 8) | BYTE(ip + 1);
        ip += 2;
    }
#else
    t = ((t & 0x7F) << 8) | BYTE(ip + 1); ip += 2;
#endif
    PROF(256); RPUSH(ip); ip = cbase + (t << SCALE); TRACE_CALL();
    NEXT();
#endif
#if ENC == 3 && HOTCALLS
#if !(SHAREDCALL && VARCALL)
#error "HOTCALLS needs the shared, variable-length call path"
#endif
L_hcall:   /* one-byte call: t holds the byte (0xE0-0xFF), ip is past it */
    PROF(256); RPUSH(ip); ip = cbase + hot_tab[t & 0x1F]; TRACE_CALL(); NEXT();
#endif

L_noop:    /* noop    */ NEXT();
L_exit:    /* exit    */ ip = RS; rp += CELL_BYTES; NEXT();
L_lit:     /* lit     */ PUSH(OPND16(ip)); ip += 2; NEXT();
#if ENC == 3
L_lit8:    /* lit8    */ PUSH(BYTE(ip)); ip += 1; NEXT();
L_lit8x:   /* lit8;exit */ PUSH(BYTE(ip)); ip = RS; rp += CELL_BYTES; NEXT();
L_lit32:   /* lit32   */ { UNS64 v = LD32(ip);
                           if (v & 0x80000000u) v |= ~(UNS64)0xFFFFFFFFu;
                           PUSH(v); ip += 4; } NEXT();
#else
L_lit32:   /* lit32   */ { UNS64 v = (UNS64)TOK(ip) | ((UNS64)TOK(ip + 2) << 16);
                           if (v & 0x80000000u) v |= ~(UNS64)0xFFFFFFFFu;
                           PUSH(v); ip += 4; } NEXT();
/*  A literal too wide for LIT32's sign-extended 32 bits, as CELL_BYTES/2
 *  tokens, little end first. The 16-bit encodings did not have this: the
 *  translator masked every literal to 32 bits and a wider one was
 *  silently truncated. Nothing noticed, because no image in these
 *  encodings had ever COMPILED a literal - they were all translated from
 *  a cell image whose own constants happened to fit. The first thing to
 *  find it was the CORE suite's MAX-INT on a 64-bit cell.  */
L_lit64t:  /* lit64   */ { UNS64 v = 0; int k_;
                           for (k_ = 0; k_ < CELL_BYTES / 2; k_++)
                               v |= (UNS64)TOK(ip + 2 * k_) << (16 * k_);
                           PUSH(v); ip += CELL_BYTES; } NEXT();
#endif
#if ENC == 1
/*  FARCALL: [72][low 16][high 16] - a call to an absolute byte offset
 *  from the image base, bypassing the word table entirely.
 *
 *  SOD16 needs this to compile anything. Its table is derived at load
 *  by walking the dictionary chain, sized to exactly the words that
 *  were in the image, and malloc'd once; a word defined afterwards has
 *  no entry and therefore no number that a call token could name. The
 *  table is the whole point of the encoding and it is also the reason
 *  the encoding cannot host its own compiler without an escape.
 *
 *  CPT16, one step later, needs nothing of the kind: it computes the
 *  target from the address. That contrast is the argument for deleting
 *  the table, and this opcode is what makes it measurable rather than
 *  hypothetical.  */
L_farcall: { UNS64 off = (UNS64)TOK(ip) | ((UNS64)TOK(ip + 2) << 16);
             RPUSH(ip + 4); ip = (UNS64)(uintptr_t)base + off; }
           goto next;
/*  DODOES with an address instead of a word number, for a DOES> word
 *  created after load. Body is [DODOESF][offset/2][pad][PFA].
 *
 *  The operand is ONE token, not two, and that is forced by the layout
 *  rather than chosen: CREATE reserves exactly one cell before the
 *  parameter field, so on a 4-byte cell there are four bytes to
 *  overwrite and a 32-bit offset does not fit. Bodies are 2-byte
 *  aligned, so halving the offset costs nothing and reaches 128 KB.
 *  Past that the compiler refuses rather than truncating.  */
L_dodoesf: { UNS64 off = (UNS64)TOK(ip) << 1;
             RPUSH((ip + 2 + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1));
             ip = (UNS64)(uintptr_t)base + off; }
           goto next;
#endif
#if ENC == 3 && SPEC
/*  Specialised opcodes, each borrowed from another VM (CV8.md 10).
 *  The slot/variable operand is a 16-bit little-endian value v; the
 *  address is base + (v << SCALE), the same compressed pointer calls use. */
#if VARSLOT
#define SLOT() (t = BYTE(ip), \
        (t & 0x80) ? (t = ((t & 0x7F) << 16) | ((UNS64)BYTE(ip + 1) << 8) \
                         | BYTE(ip + 2), ip += 3, cbase + (t << SCALE)) \
                   : (t = (t << 8) | BYTE(ip + 1), ip += 2, cbase + (t << SCALE)))
#else
#define SLOT() (t = LD16(ip), ip += 2, cbase + (t << SCALE))
#endif
L_lit0:   VMPUSH(0); NEXT();                          /* JVM iconst_0  */
L_lit1:   VMPUSH(1); NEXT();
L_litm1:  VMPUSH(~(UNS64)0); NEXT();
L_vf:     { UNS64 a = SLOT(); VMPUSH(CELL(a)); } NEXT();   /* getstatic */
L_vs:     { UNS64 a = SLOT(); CELL(a) = DS0; dsp += CELL_BYTES; } NEXT();
/*  Locals are shallow-bound VARIABLEs (locals.4). These do LSAVE,
 *  LRESTORE, L! and LZERO in one dispatch, on the SAME Forth-visible save
 *  stack (LSAVE-SP, LSAVE-STACK), and fall back to the Forth word itself
 *  - pushing the START offset exactly as `LIT off` did - whenever the
 *  Forth version would take its ABORT" path. Specialise, and deoptimise
 *  to the general code on the rare case: CPython 3.11's pattern.  */
L_lsave: { UNS64 a = SLOT(), lsp = cbase + loc_hdr[0];
    UNS64 sp = CELL(lsp), stk = CELL(cbase + loc_hdr[1]);
    if ((INT64)sp >= (INT64)loc_hdr[2] || (INT64)sp < 0 || !stk) {
        VMPUSH(a - cbase); RPUSH(ip); ip = cbase + loc_hdr[3]; TRACE_CALL(); NEXT(); }
    CELL(stk + sp * CELL_BYTES) = CELL(a); CELL(lsp) = sp + 1; } NEXT();
L_lrest: { UNS64 a = SLOT(), lsp = cbase + loc_hdr[0];
    UNS64 sp = CELL(lsp), stk = CELL(cbase + loc_hdr[1]);
    if ((INT64)sp <= 0 || !stk) {
        VMPUSH(a - cbase); RPUSH(ip); ip = cbase + loc_hdr[4]; TRACE_CALL(); NEXT(); }
    CELL(lsp) = --sp; CELL(a) = CELL(stk + sp * CELL_BYTES); } NEXT();
L_lstore: { UNS64 a = SLOT(); CELL(a) = DS0; dsp += CELL_BYTES; } NEXT();
L_lzero:  { UNS64 a = SLOT(); CELL(a) = 0; } NEXT();
/*  The kernel's hottest tiny colon words, as opcodes (Gforth-style
 *  primitive selection). The translator substitutes one only where the
 *  compiled body is exactly the definition implemented here.  */
L_zeq:    DS0 = -(UNS64)(DS0 == 0); NEXT();                     /* 0=  */
L_sub:    DS1 -= DS0; dsp += CELL_BYTES; NEXT();                /* -   */
L_ne:     DS1 = -(UNS64)(DS1 != DS0); dsp += CELL_BYTES; NEXT(); /* <> */
L_zlt:    DS0 = -(UNS64)((INT64)DS0 < 0); NEXT();               /* 0<  */
L_sgt:    DS1 = -(UNS64)((INT64)DS0 < (INT64)DS1); dsp += CELL_BYTES; NEXT();
L_2dup:   { UNS64 a_ = DS1, b_ = DS0; PUSH(a_); PUSH(b_); } NEXT();
L_2drop:  dsp += 2 * CELL_BYTES; NEXT();
L_charp:  DS0 += 1; NEXT();                                     /* CHAR+ */
L_onep:   DS0 += 1; NEXT();                                     /* 1+  */
L_cellp:  DS0 += CELL_BYTES; NEXT();                            /* CELL+ */
L_cells:  DS0 <<= CELL_SHIFT; NEXT();
L_onem:   DS0 -= 1; NEXT();                                     /* 1-  */
L_invert: DS0 = ~DS0; NEXT();
L_count:  { UNS64 a_ = DS0; DS0 = a_ + 1; PUSH(BYTE(a_)); } NEXT();
L_aligned: DS0 = (DS0 + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1); NEXT();
/*  Lua 5.4's OP_ADDI / OP_EQI: a signed 8-bit immediate. Lua added
 *  immediate forms for every operator and kept only these.  */
L_addi:   DS0 += (UNS64)(INT64)(int8_t)BYTE(ip); ip += 1; NEXT();
L_addix:  DS0 += (UNS64)(INT64)(int8_t)BYTE(ip); ip = RS; rp += CELL_BYTES; NEXT();
L_eqi:    DS0 = -(UNS64)(DS0 == (UNS64)(INT64)(int8_t)BYTE(ip)); ip += 1; NEXT();
L_eqix:   DS0 = -(UNS64)(DS0 == (UNS64)(INT64)(int8_t)BYTE(ip)); ip = RS; rp += CELL_BYTES; NEXT();
#endif
#if ENC == 3 && OPS10
/*  relf's format-10 opcodes: kernel colon words given opcodes from the
 *  free slots, per design (tools/sod16.py X_OPS10, lab/evolve), each only
 *  where its compiled body is exactly the definition here. As opcodes the
 *  return-stack words have no return address of their own on top: I is
 *  the top cell, J two below it.  */
L_x_plusstore: { UNS64 a_ = DS0; CELL(a_) += DS1; dsp += 2 * CELL_BYTES; } NEXT(); /* +!      */
/* ?DUP: the value first - one PUSH lowers dsp before it evaluates x,
   so PUSH(DS0) would copy the new, empty slot onto itself.  */
L_x_qdup:      if (DS0) { UNS64 v_ = DS0; PUSH(v_); } NEXT();                    /* ?DUP    */
L_x_2fetch:    { UNS64 a_ = DS0; DS0 = CELL(a_ + CELL_BYTES); PUSH(CELL(a_)); } NEXT();   /* 2@ (Iteration 290) */
L_x_2store:    { UNS64 a_ = DS0; CELL(a_) = DS1; CELL(a_ + CELL_BYTES) = DS2; dsp += 3 * CELL_BYTES; } NEXT(); /* 2! */
L_x_gt:        { INT64 b_ = (INT64)DS0, a_ = (INT64)DS1; dsp += CELL_BYTES; DS0 = -(UNS64)(a_ > b_); } NEXT();   /* > (Iteration 299) */
L_x_zeq:       DS0 = -(UNS64)(DS0 == 0); NEXT();                                  /* 0= */
L_x_execute:   { UNS64 x_ = DS0; dsp += CELL_BYTES; RPUSH(ip); ip = x_; TRACE_CALL(); } NEXT();    /* EXECUTE */
L_x_i:         PUSH(RS); NEXT();                                                    /* I       */
L_x_j:         PUSH(CELL(rp + 2 * CELL_BYTES)); NEXT();                             /* J       */
L_x_unloop:    rp += 2 * CELL_BYTES; NEXT();                                        /* UNLOOP  */
#if X_IPLUS
L_x_iplus:     DS0 += RS; NEXT();                     /* I + (Iteration 60: run-time code's I+)  */
#endif
L_x_do:        { RPUSH(DS1); RPUSH(DS0); dsp += 2 * CELL_BYTES; } NEXT();            /* (DO)    */
/*  The loop words with an operand: where the colon word jumps to its
 *  return address plus the operand cell, these take the branch offset
 *  after the opcode, as ?BRANCH does; where it skips the cell, they skip
 *  the two bytes. (+LOOP) leaves as the kernel's does: when index - limit
 *  changes sign AND the step points at the limit - the sign alone also
 *  flips where index - limit wraps (Iteration 125, RelF's rule).  */
/*  Short branches: a one-byte offset, from the operand, where it fits -
 *  the converter decides branch by branch (tools/sod16.py, shorten).  */
L_x_br8:   ip += (int8_t)BYTE(ip); NEXT();                                         /* BRANCH8  */
L_x_qbr8:  if (DS0) ip += 1; else ip += (int8_t)BYTE(ip);                          /* ?BRANCH8 */
           dsp += CELL_BYTES; NEXT();
/*  0= ?BRANCH as one branch that jumps when the top is NOT zero: about 4%
 *  of the dispatches on kernel, parse and corpus (lab/evolve/price.py,
 *  Iteration 8). The converter fuses them where nothing jumps between
 *  (tools/sod16.py, testbranch); offsets as ?BRANCH's, from the operand.  */
L_x_nqbr:  if (DS0) ip += (int16_t)LD16(ip); else ip += 2;                     /* 0= ?BRANCH  */
           dsp += CELL_BYTES; NEXT();
L_x_nqbr8: if (DS0) ip += (int8_t)BYTE(ip); else ip += 1;                      /* 0= ?BRANCH8 */
           dsp += CELL_BYTES; NEXT();
/*  < ?BRANCH: falls through when a < b, jumps otherwise - fib's test, 9% of
 *  its dispatches; in code compiled at run time, fused by the compiler
 *  overlay (forth/cv8-fuse.4, ?BRANCH,) from SUPER-TABLE (Iteration 9).  */
L_x_ltbr:  { INT64 a_ = (INT64)DS1, b_ = (INT64)DS0; dsp += 2 * CELL_BYTES;    /* < ?BRANCH  */
             if (a_ < b_) ip += 2; else ip += (int16_t)LD16(ip); } NEXT();
L_x_ltbr8: { INT64 a_ = (INT64)DS1, b_ = (INT64)DS0; dsp += 2 * CELL_BYTES;    /* < ?BRANCH8 */
             if (a_ < b_) ip += 1; else ip += (int8_t)BYTE(ip); } NEXT();
/*  = ?BRANCH and U< ?BRANCH: as < ?BRANCH (Iteration 9) - about 1-2% of
 *  the dispatches each on kernel, parse and corpus (lab/evolve/price.py).  */
L_x_eqbr:   { UNS64 a_ = DS1, b_ = DS0; dsp += 2 * CELL_BYTES;    /* = ?BRANCH */
             if (a_ == b_) ip += 2; else ip += (int16_t)LD16(ip); } NEXT();
L_x_eqbr8:  { UNS64 a_ = DS1, b_ = DS0; dsp += 2 * CELL_BYTES;    /* = ?BRANCH8 */
             if (a_ == b_) ip += 1; else ip += (int8_t)BYTE(ip); } NEXT();
L_x_ultbr:  { UNS64 a_ = DS1, b_ = DS0; dsp += 2 * CELL_BYTES;    /* U< ?BRANCH */
             if (a_ < b_) ip += 2; else ip += (int16_t)LD16(ip); } NEXT();
L_x_ultbr8: { UNS64 a_ = DS1, b_ = DS0; dsp += 2 * CELL_BYTES;    /* U< ?BRANCH8 */
             if (a_ < b_) ip += 1; else ip += (int8_t)BYTE(ip); } NEXT();
/*  Iteration 12: the rest of the tests before a branch - "-" and <> (one
 *  pair: both fall through when a != b), >, 0<, and = with an immediate
 *  (EQI then ?BRANCH: the immediate byte, then the offset). Each pair is
 *  compiled only in a design that has it (-DX_NEBR ..., from lab/evolve),
 *  so no other engine changes - unused code moves GCC's layout too.  */
#if X_NEBR
L_x_nebr:   { UNS64 a_ = DS1, b_ = DS0; dsp += 2 * CELL_BYTES;      /* <> ?BRANCH, - ?BRANCH */
              if (a_ != b_) ip += 2; else ip += (int16_t)LD16(ip); } NEXT();
L_x_nebr8:  { UNS64 a_ = DS1, b_ = DS0; dsp += 2 * CELL_BYTES;
              if (a_ != b_) ip += 1; else ip += (int8_t)BYTE(ip); } NEXT();
#endif
#if X_SGTBR
L_x_sgtbr:  { INT64 a_ = (INT64)DS1, b_ = (INT64)DS0; dsp += 2 * CELL_BYTES;  /* > ?BRANCH */
              if (a_ > b_) ip += 2; else ip += (int16_t)LD16(ip); } NEXT();
L_x_sgtbr8: { INT64 a_ = (INT64)DS1, b_ = (INT64)DS0; dsp += 2 * CELL_BYTES;
              if (a_ > b_) ip += 1; else ip += (int8_t)BYTE(ip); } NEXT();
#endif
#if X_ZLTBR
L_x_zltbr:  if ((INT64)DS0 < 0) ip += 2; else ip += (int16_t)LD16(ip);     /* 0< ?BRANCH */
            dsp += CELL_BYTES; NEXT();
L_x_zltbr8: if ((INT64)DS0 < 0) ip += 1; else ip += (int8_t)BYTE(ip);
            dsp += CELL_BYTES; NEXT();
#endif
#if X_EQIBR
L_x_eqibr:  { UNS64 v_ = DS0, i_ = (UNS64)(INT64)(int8_t)BYTE(ip); dsp += CELL_BYTES; ip += 1;   /* n = ?BRANCH */
              if (v_ == i_) ip += 2; else ip += (int16_t)LD16(ip); } NEXT();
L_x_eqibr8: { UNS64 v_ = DS0, i_ = (UNS64)(INT64)(int8_t)BYTE(ip); dsp += CELL_BYTES; ip += 1;
              if (v_ == i_) ip += 1; else ip += (int8_t)BYTE(ip); } NEXT();
#endif
/*  Iteration 33: DUP ?BRANCH and OVER ?BRANCH - the test KEEPS its value:
 *  5.8-6.2% and 0.5-0.8% of the front designs' image dispatches
 *  (lab/evolve/regprice.py), which the pairs could not fuse - ?BRANCH
 *  carries an operand. Nothing popped; compiled only where a design has
 *  them, as Iteration 12's.  */
#if X_DUPBR
L_x_dupbr:   if (DS0) ip += 2; else ip += (int16_t)LD16(ip); NEXT();        /* DUP ?BRANCH   */
L_x_dupbr8:  if (DS0) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();         /* DUP ?BRANCH8  */
#endif
#if X_OVERBR
L_x_overbr:  if (DS1) ip += 2; else ip += (int16_t)LD16(ip); NEXT();        /* OVER ?BRANCH  */
L_x_overbr8: if (DS1) ip += 1; else ip += (int8_t)BYTE(ip); NEXT();         /* OVER ?BRANCH8 */
#endif
/*  Iteration 34: DUP 0= ?BRANCH kept - jumps when the top is NOT zero, and
 *  keeps it (3.4-4.3%) - and SWAP n + : ( a b -- b a+n ), ADDI's immediate
 *  (3.7-5.0%; lab/evolve/regprice.py).  */
#if X_DUPNBR
L_x_dupnbr:  if (DS0) ip += (int16_t)LD16(ip); else ip += 2; NEXT();        /* DUP 0= ?BRANCH  */
L_x_dupnbr8: if (DS0) ip += (int8_t)BYTE(ip); else ip += 1; NEXT();         /* DUP 0= ?BRANCH8 */
#endif
#if X_SWAPADDI
L_x_swapaddi: t = DS1; DS1 = DS0; DS0 = t + (UNS64)(INT64)(int8_t)BYTE(ip); ip += 1; NEXT();   /* SWAP n + */
#endif
/*  Iteration 176, the hybrid's keeping forms: an operation on the top with an
 *  immediate, the top kept - DUP n + and DUP n < (fib's DUP -1 + and DUP 2 <),
 *  one dispatch for three. results/price-hybrid.md.  */
#if X_DUPADDI
L_x_dupaddi: PUSH(DS1 + (UNS64)(INT64)(int8_t)BYTE(ip)); ip += 1; NEXT();                 /* DUP n + */
#endif
#if X_DUPLTI
L_x_duplti: PUSH(-(UNS64)((INT64)DS1 < (INT64)(int8_t)BYTE(ip))); ip += 1; NEXT();         /* DUP n < */
#endif
/*  Iteration 50: FILL and CMOVE, the kernel's byte loops (12-14 dispatches a
 *  byte in Forth; CMOVE 5-7% of kernel, parse and corpus), as opcodes - a
 *  byte at a time, ascending, as the loops: CMOVE's overlap behaves the same.  */
#if X_FILL
L_x_fill:  { UNS64 c_ = DS0, u_ = DS1, a_ = DS2; dsp += 3 * CELL_BYTES;             /* FILL  */
             while (u_) { BYTE(a_) = (UNS8)c_; a_++; u_--; } } NEXT();
#endif
#if X_CMOVE
L_x_cmove: { UNS64 u_ = DS0, d_ = DS1, s_ = DS2; dsp += 3 * CELL_BYTES;             /* CMOVE */
             while (u_) { BYTE(d_) = BYTE(s_); s_++; d_++; u_--; } } NEXT();
#endif
/*  Iteration 51: THREAD-FIND ( nfa namebuf --- nfa' | 0 ) - the byte-header
 *  dictionary's walk along one thread (forth/cv8b-kfast.4): count, then the
 *  bytes (NAME=?), then the link back - NEXT-NFA8's three forms. ~20
 *  dispatches a candidate word in Forth; 37-63% of kernel, parse, corpus.  */
#if X_THREADFIND
L_x_threadfind: { UNS64 nb_ = DS0, a_ = DS1; dsp += CELL_BYTES;
             NAME_WALK(a_, nb_);                    /* Iteration 316: bfind; 402: either walk, one macro */
             DS0 = a_; } NEXT();
#endif
/*  Iteration 54: the input side - SCAN and SKIP ( c-addr u c --- c-addr' u' ),
 *  the kernel's character loops, and TABS>BL ( c-addr u --- ), REFILL's tab
 *  loop (forth/cv8b-kinput.4): a character at a time, as the loops; the
 *  character compared as a cell, as = and - compare it.  */
#if X_SCAN
L_x_scan:  { UNS64 c_ = DS0, u_ = DS1, a_ = DS2; dsp += CELL_BYTES;
             if (c_ == 32) while (u_ && BYTE(a_) > 32) { a_++; u_--; }   /* a space: any control character too (Iteration 145) */
             else while (u_ && (UNS64)BYTE(a_) != c_) { a_++; u_--; }
             DS1 = a_; DS0 = u_; } NEXT();
#endif
#if X_SKIP
L_x_skip:  { UNS64 c_ = DS0, u_ = DS1, a_ = DS2; dsp += CELL_BYTES;
             if (c_ == 32) while (u_ && BYTE(a_) <= 32) { a_++; u_--; }  /* a space: any control character too (Iteration 145) */
             else while (u_ && (UNS64)BYTE(a_) == c_) { a_++; u_--; }
             DS1 = a_; DS0 = u_; } NEXT();
#endif
/*  (PARSE) ( addr u c --- a1 len adv ): SKIP then SCAN, the string between and
 *  how far >IN moves (kinput's PARSE8). HASH ( c-addr u #threads --- n ): the
 *  kernel's, exactly - cross.4's THASH must agree. PLACE ( addr len c-addr --- ). */
#if X_PARSE
L_x_parse: { UNS64 c_ = DS0, u_ = DS1, a_ = DS2, p_ = a_, s_;
             if (c_ == 32) {                       /* a space: any control character too (Iteration 145) */
                 while (u_ && BYTE(p_) <= 32) { p_++; u_--; } s_ = p_;
                 while (u_ && BYTE(p_) > 32) { p_++; u_--; }
             } else {
                 while (u_ && (UNS64)BYTE(p_) == c_) { p_++; u_--; } s_ = p_;
                 while (u_ && (UNS64)BYTE(p_) != c_) { p_++; u_--; }
             }
             DS2 = s_; DS1 = p_ - s_; DS0 = (p_ - a_) + (u_ ? 1 : 0); } NEXT();
#endif
#if X_HASH
L_x_hash:  { UNS64 t_ = DS0, u_ = DS1, a_ = DS2, h_; dsp += 2 * CELL_BYTES;
             h_ = (UNS64)BYTE(a_) << 1; if ((INT64)u_ > 1) h_ ^= (UNS64)BYTE(a_ + 1) << 2;
             DS0 = (h_ ^ u_) & (t_ - 1); } NEXT();
#endif
/*  Iteration 57: (FIND) ( c-addr nb ctx n --- c-addr 0 | xt 1 | xt -1 ) -
 *  the kernel's FIND with kfast's SEARCH-WORDLIST8 (forth/cv8b-klookup.4):
 *  the last wordlist not searched twice; from the top of the search order,
 *  the name to NAMEBUF (32 MIN, PLACE), HASH, the thread's head, THREAD-FIND's
 *  walk, NAME>8 and the immediate bit.  */
#if X_FIND
L_x_find: { UNS64 n_ = DS0, ctx_ = DS1, nb_ = DS2, c_ = CELL(dsp + 3 * CELL_BYTES), x_ = c_, r_ = 0;
            if ((INT64)n_ > 1 && CELL(ctx_ + (n_ - 1) * CELL_BYTES) == CELL(ctx_ + (n_ - 2) * CELL_BYTES)) n_--; while (n_) { UNS64 w_, u_, k_, h_, a_; n_--; w_ = CELL(ctx_ + n_ * CELL_BYTES); u_ = BYTE(c_); if ((INT64)u_ > 32) u_ = 32; BYTE(nb_) = (UNS8)u_; for (k_ = 0; k_ < u_; k_++) BYTE(nb_ + 1 + k_) = BYTE(c_ + 1 + k_); h_ = (UNS64)BYTE(nb_ + 1) << 1; if ((INT64)u_ > 1) h_ ^= (UNS64)BYTE(nb_ + 2) << 2; h_ = (h_ ^ u_) & (CELL(w_) - 1); a_ = CELL(w_ + (h_ + 1) * CELL_BYTES); NAME_WALK(a_, nb_); if (a_) { x_ = a_ + 1 + (BYTE(a_) & 31); r_ = (BYTE(a_) & 64) ? 1 : (UNS64)-1; break; } }   /* Iteration 316: bfind; 402: either walk, NAME_WALK */
            dsp += 2 * CELL_BYTES; DS1 = x_; DS0 = r_; } NEXT();
#endif
/*  (>NUMBER) ( ud c-addr u base --- ud2 c-addr2 u2 ) - the kernel's >NUMBER
 *  with BASE @ given (klookup's >NUMBER8): DIGIT?'s test exactly - '0'-'9',
 *  nothing between '9' and 'A', then A on, below base (signed) - and ud*base
 *  + digit as the kernel does it: UM* of the low cell, * of the high, D+.  */
#if X_TONUMBER
L_x_tonumber: { UNS64 b_ = DS0, u_ = DS1, a_ = DS2, hi_ = CELL(dsp + 3 * CELL_BYTES), lo_ = CELL(dsp + 4 * CELL_BYTES);
            while (u_) { INT64 d_ = (INT64)BYTE(a_) - 48; UNS64 ph_, pl_; if (d_ < 0 || (d_ > 9 && d_ < 17)) break; if (d_ > 9) d_ -= 7; if (!(d_ < (INT64)b_)) break; ph_ = lo_; pl_ = b_; umul(&ph_, &pl_); hi_ = ph_ + hi_ * b_; lo_ = pl_ + (UNS64)d_; if (lo_ < pl_) hi_++; a_++; u_--; }
            dsp += CELL_BYTES; DS0 = u_; DS1 = a_; DS2 = hi_; CELL(dsp + 3 * CELL_BYTES) = lo_; } NEXT();
#endif
#if X_NUMBERQ
L_x_numberq: { UNS64 p_ = DS0, b_ = DS1, a_ = DS2, lo_, hi_, f_ = numberq(a_, b_, p_, &lo_, &hi_); DS2 = lo_; DS1 = hi_; DS0 = f_; } NEXT();   /* (NUMBER?) */
#endif
#if X_PLACE
L_x_place: { UNS64 d_ = DS0, n_ = DS1, s_ = DS2; dsp += 3 * CELL_BYTES;
             BYTE(d_) = (UNS8)n_; d_++; while (n_) { BYTE(d_) = BYTE(s_); d_++; s_++; n_--; } } NEXT();
#endif
L_x_qdo:   { UNS64 n2_ = DS0, n1_ = DS1; dsp += 2 * CELL_BYTES;                  /* (?DO)   */
             if (n1_ != n2_) { RPUSH(n1_); RPUSH(n2_); ip += 2; } else ip += (int16_t)LD16(ip); } NEXT();
L_x_leave: rp += 2 * CELL_BYTES; ip += (int16_t)LD16(ip); NEXT();                        /* (LEAVE) */
L_x_loop:  { UNS64 i_ = RS + 1;                                                  /* (LOOP)  */
             if (i_ == CELL(rp + CELL_BYTES)) { rp += 2 * CELL_BYTES; ip += 2; }
             else { CELL(rp) = i_; ip += (int16_t)LD16(ip); } } NEXT();
L_x_ploop: { UNS64 n_ = DS0, i_ = RS, l_ = CELL(rp + CELL_BYTES), j_ = i_ + n_;  /* (+LOOP) */
             dsp += CELL_BYTES;
             if ((INT64)(((i_ - l_) ^ (j_ - l_)) & ((i_ - l_) ^ n_)) < 0) { rp += 2 * CELL_BYTES; ip += 2; }
             else { CELL(rp) = j_; ip += (int16_t)LD16(ip); } } NEXT();
#endif
#if ENC == 3
L_lit64:   /* lit64: a full cell, little-endian. CELL_BYTES bytes.      */
    { UNS64 v = 0; int i_;
      for (i_ = CELL_BYTES - 1; i_ >= 0; i_--) v = (v << 8) | BYTE(ip + i_);
      PUSH(v); ip += CELL_BYTES; } NEXT();
L_esc:     /*  The escaped band: one more byte selects an OS/libc
            *  primitive. Half the primitive band was these, for 3.2% of
            *  static sites and 0.006% of dispatches; behind an escape
            *  they cost a byte each and free 32 opcodes.  */
#if ESCAPE
    t = BYTE(ip); ip += 1; PROF(t); goto *esc_tab[t];
#else
    write_str(2, "CV8: image uses the escaped band, engine built without it\n");
    exit(2);
#endif
#endif
#if X_JIT
/*  JIT.md (Iteration 80): a colon word compiled at run time begins [JIT]
 *  [four bytes] - its length, top bit set, until its first call; then
 *  the native code's offset (engine/jit.c), or 0: it stays bytecode.
 *  Native code runs the whole word, EXIT included; this then returns as
 *  EXIT does. The return stack crosses in jit_rp, for loops and >R.
 *  Here among the ordinary handlers: gen-tos.py must wrap it in SPILL
 *  and FILL - after the tag's call handlers it is left bare (Iteration 81). */
L_x_jit:   { uint32_t f_ = jit_ld32(ip);
             jit_cbase = cbase;
             if (f_ & 0x80000000u) f_ = jit_word(ip - 1, 0);
             if (JIT_NATIVE(f_)) {
                 spn_st r_;
                 jit_rp = (ucell)rp;
                 /* the stack in memory here (gen-tos.py spills around a handler it
                    has no rule for): dsp at the top; native code wants sp at the
                    second, the top apart - SPN's convention */
#if JITMUL
                 if (jit_call(f_, (cell *)(uintptr_t)(dsp + CELL_BYTES), (cell)DS0, &r_)) {   /* 475: a zero divisor in native code */
                     rp = (UNS64)jit_rp; dsp = (UNS64)(uintptr_t)jit_tsp - CELL_BYTES;
                     DS0 = (UNS64)-10; RPUSH(ip); ip = cbase + throw_off; NEXT();            /* as L_umdiv's DIV0 */
                 }
#else
                 r_ = ((spn_st (SPN_CC *)(cell *, cell))(void *)(jit_mem + f_))((cell *)(uintptr_t)(dsp + CELL_BYTES), (cell)DS0);
#endif
                 rp = (UNS64)jit_rp; dsp = (UNS64)(uintptr_t)SPN_SP(r_) - CELL_BYTES; DS0 = (UNS64)SPN_TOS(r_);
                 ip = RS; rp += CELL_BYTES;
             } else { if (JIT_REPOINT(f_)) jit_repoint(ip - 1, RS); ip += 4; } } NEXT();   /* bytecode: its caller skips the header next time */
#endif
L_dovar:   /* DOVAR as a primitive: [DOVAR][pad][PFA] -> push PFA, return */
#if ENC == 3
    /*  The PFA is align(body+3), not align(body+1), so that it is the
     *  SAME address DODOES computes after overwriting the front of the
     *  body with a 2-byte call. With bodies always cell-aligned the two
     *  agreed by accident; the byte-header layout leaves bodies wherever
     *  the name ends, and a DOES> word created at run time then found
     *  its parameter field one cell away from where CREATE had put it.
     *  cv8.4's CREATE8 reserves the two bytes.  */
#if TAG2
    /*  Tag 2: CREATE reserves the longest call, 4 bytes (FORMAT-TAG2.md).  */
    PUSH((ip + 4 + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1));
#else
    PUSH((ip + (DOESFAR ? 3 : 2) + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1));
#endif
#else
    PUSH((ip + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1));
#endif
    ip = RS; rp += CELL_BYTES; NEXT();
L_dodoes:  /* [DODOES][tail][pad][PFA] -> the tail's R> finds the PFA */
#if ENC == 3 && TAG2
    /*  Tag 2: always the 4-byte call, 11 + 30 bits, in the 4 bytes CREATE
     *  reserved - the parameter field where DOVAR puts it.  */
    t = ((UNS64)(BYTE(ip) & 0x3F) << 24) | ((UNS64)BYTE(ip + 1) << 16) | ((UNS64)BYTE(ip + 2) << 8) | BYTE(ip + 3);
    RPUSH((ip + 4 + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1));
    ip = cbase + t; NEXT();
#elif ENC == 3
#if VARCALL
    if (BYTE(ip) & 0x40) {
        t = ((BYTE(ip) & 0x3F) << 16) | ((UNS64)BYTE(ip + 1) << 8) | BYTE(ip + 2);
#if DOESFAR
        t <<= (CELL_BYTES == 8 ? 3 : 2) - SCALE;  /* Iteration 416: a far DOES> call counts cells - its tail is aligned */
#endif
        RPUSH((ip + 3 + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1));
    } else {
        t = ((BYTE(ip) & 0x3F) << 8) | BYTE(ip + 1);
        RPUSH((ip + 2 + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1));
    }
#else
    t = ((BYTE(ip) & 0x7F) << 8) | BYTE(ip + 1);
    RPUSH((ip + 2 + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1));
#endif
    ip = cbase + (t << SCALE); NEXT();
#else
    t = TOK(ip);
    RPUSH((ip + 2 + CELL_BYTES - 1) & ~(UNS64)(CELL_BYTES - 1));
    ip = CALLTARGET(t); NEXT();
#endif
#if ENC == 3
L_branch:  /* branch  */ ip += (int16_t)LD16(ip); NEXT();
#else
L_branch:  /* branch  */ ip += 2 * (int16_t)TOK(ip); NEXT();
#endif
L_0branch: /* 0branch */
#if ENC == 3
    if (DS0) ip += 2; else ip += (int16_t)LD16(ip);
#else
    if (DS0) ip += 2; else ip += 2 * (int16_t)TOK(ip);
#endif
    dsp += CELL_BYTES;
    NEXT();
L_drop:    /* drop    */ dsp += CELL_BYTES; NEXT();
L_dup:     /* dup     */ PUSH(DS1); NEXT();
L_swap:    /* swap    */ t = DS0; DS0 = DS1; DS1 = t; NEXT();
L_rot:     /* rot     */ t = DS2; DS2 = DS1; DS1 = DS0; DS0 = t; NEXT();
L_over:    /* over    */ PUSH(DS2); NEXT();
L_cfetch:  /* C@      */ DS0 = BYTE(DS0); NEXT();
L_fetch:   /* @       */ DS0 = CELL(DS0); NEXT();
L_cstore:  /* c!      */ BYTE(DS0) = (UNS8)DS1; dsp += 2 * CELL_BYTES; NEXT();
L_store:   /* !       */ CELL(DS0) = DS1; dsp += 2 * CELL_BYTES; NEXT();
L_and:     /* and     */ DS1 &= DS0; dsp += CELL_BYTES; NEXT();
L_or:      /* or      */ DS1 |= DS0; dsp += CELL_BYTES; NEXT();
L_xor:     /* xor     */ DS1 ^= DS0; dsp += CELL_BYTES; NEXT();
L_fromr:   /* r>      */ PUSH(RS); rp += CELL_BYTES; NEXT();
L_tor:     /* >r      */ RPUSH(DS0); dsp += CELL_BYTES; NEXT();
L_rfetch:  /* r@      */ PUSH(RS); NEXT();
L_eq:      /* =       */ DS1 = - (UNS64)(DS0 == DS1); dsp += CELL_BYTES; NEXT();
L_ugt:     /* u<      */ DS1 = - (UNS64)(DS1 < DS0); dsp += CELL_BYTES; NEXT();
L_gt:      /* <       */
    DS1 = - (UNS64)((INT64)DS1 < (INT64)DS0);
    dsp += CELL_BYTES;
    NEXT();
L_plus:    /* +       */ DS1 += DS0; dsp += CELL_BYTES; NEXT();
L_negate:  /* negate  */ DS0 = - DS0; NEXT();
L_lshift:  /* lshift  */ DS1 <<= DS0; dsp += CELL_BYTES; NEXT();
L_rshift:  /* rshift  */ DS1 >>= DS0; dsp += CELL_BYTES; NEXT();
L_ummult:  /* um*     */ umul(&DS0, &DS1); NEXT();
L_umdiv:   /* um/mod  */ DIV0_CHECK(); udiv(&DS0, &DS1, &DS2); dsp += CELL_BYTES; NEXT();
L_dplus:   /* d+      */
    DS3 += DS1; DS2 += DS0; DS2 += (DS3 < DS1);
    dsp += 2 * CELL_BYTES;
    NEXT();

L_write: { /* write   c-addr u --- : u bytes to the terminal (t_write) */
    t_write((const UNS8 *)(uintptr_t)DS1, (UNS64)DS0);
    dsp += 2 * CELL_BYTES;
    NEXT();
}
L_read: { /* read    c-addr u --- u2 : what input there is, 0 at its end (t_read) */
    UNS64 n_ = t_read((UNS8 *)(uintptr_t)DS1, (UNS64)DS0);
    DS1 = n_;
    dsp += CELL_BYTES;
    NEXT();
}
L_bye:     /* bye     */ t_flush(); PROFDUMP; exit(0);
L_spfetch: /* sp@     */ PUSH(dsp + CELL_BYTES); NEXT();
L_spstore: /* sp!     */ dsp = DS0; NEXT();
L_rpfetch: /* rp@     */ PUSH(rp); NEXT();
L_rpstore: /* rp!     */ rp = DS0; dsp += CELL_BYTES; NEXT();

L_openfile: { /* c-addr u fam --- fid ior */
    int fd;
    t = BYTE(DS2 + DS1);
    BYTE(DS2 + DS1) = 0;
    fd = OPEN3((char *)(uintptr_t)DS2, open_flags[DS0], 0644);
    BYTE(DS2 + DS1) = t;
    DS2 = (UNS64)fd;
    DS1 = (fd >= 0) ? 0 : 200;
    dsp += CELL_BYTES;
    NEXT();
}
L_closefile: {/* fid --- ior */
    t_fdrop((int)DS0);

    DS0 = (UNS64)close((int)DS0);
    NEXT();
    }
L_readline: { /* c-addr u1 fid --- u2 flag ior */
    int fd = (int)DS0;
    UNS64 addr = DS2, max = DS1, count = 0;
    long n, err = 0, got_any = 0;
    UNS8 c;

    if (max == 0) got_any = 1;   /* zero characters: not end of file (Iteration 125, as RelF) */
    while (count < max) {
        int ch = (fd == 0) ? t_getc() : t_fgetc(fd);
        n = (ch == -2) ? -1 : (ch < 0 ? 0 : 1);
        c = (UNS8)ch;
        if (n < 0) { err = 1; break; }
        if (n == 0) break;      /* EOF */
        got_any = 1;
        if (c == '\n') break;   /* line terminator, not stored */
        BYTE(addr + count) = c;
        count++;
    }
    /* Tolerate CRLF files: a trailing \r right before the \n we just
     * stopped at is a line terminator too, not payload. */
    if (count > 0 && BYTE(addr + count - 1) == '\r') count--;
    DS2 = count;
    DS1 = got_any ? (UNS64)-1 : 0;
    DS0 = err ? (UNS64)-200 : 0;
    NEXT();
}
L_writeline: { /* c-addr u fid --- ior */
    t_flush();
    t_fdrop((int)DS0);          /* Iteration 225: what READ-LINE read ahead given back first, as WRITE-FILE does -
                                   else a line written after a line read lands past the read-ahead */
    int fd = (int)DS0;
    UNS64 addr = DS2, len = DS1;
    long n;

    n = full_write(fd, (void*)(uintptr_t)addr, len);
    if (n == (long)len) {
        n = full_write(fd, "\n", 1);
        DS2 = (n == 1) ? 0 : (UNS64)-200;
    } else {
        DS2 = (UNS64)-200;
    }
    dsp += 2 * CELL_BYTES;
    NEXT();
}
L_readfile: { /* c-addr u1 fid --- u2 ior */
    t_fdrop((int)DS0);
    int fd = (int)DS0;
    UNS64 addr = DS2, maxlen = DS1;
    long n;

    n = full_read(fd, (void*)(uintptr_t)addr, maxlen);
    if (n < 0) {
        DS2 = 0;
        DS1 = (UNS64)-200;
    } else {
        DS2 = (UNS64)n;
        DS1 = 0;
    }
    dsp += CELL_BYTES;
    NEXT();
}
L_writefile: { /* c-addr u fid --- ior */
    t_fdrop((int)DS0);
    t_flush();
    int fd = (int)DS0;
    UNS64 addr = DS2, len = DS1;
    long n;

    n = full_write(fd, (void*)(uintptr_t)addr, len);
    DS2 = (n == (long)len) ? 0 : (UNS64)-200;
    dsp += 2 * CELL_BYTES;
    NEXT();
}
#if !SYSC
L_system: { t_flush(); /* c-addr u --- ior */
    UNS64 addr = DS1, len = DS0;
    UNS8 saved;
    pid_t pid;
    long ior;
    int status = 0;
    char *argv[4];

    saved = BYTE(addr + len);
    BYTE(addr + len) = 0;
    argv[0] = "/bin/sh";
    argv[1] = "-c";
    argv[2] = (char*)(uintptr_t)addr;
    argv[3] = 0;
    pid = fork();
    if (pid == 0) {
        execve("/bin/sh", argv, environ);
        _exit(127);
    }
    if (pid > 0) {
        waitpid(pid, &status, 0);
        ior = (status >> 8) & 0xff;
    } else {
        ior = 200;
    }
    BYTE(addr + len) = saved;
    DS1 = (UNS64)ior;
    dsp += CELL_BYTES;
    NEXT();
}
#endif /* !SYSC */
L_reposfile: {/* ud fid --- ior */
    /*  ANS: ( ud fileid -- ior ) - the offset a double, low cell under the
     *  high one; the ior 0 or 200. It took one cell and returned the new
     *  position as its ior, so any position but 0 read as a failure
     *  (Iteration 125; RelF's cv8.c has the double). */
    t_fdrop((int)DS0);
    {   unsigned long long off_ = (CELL_BYTES == 8) ? (unsigned long long)DS2
            : ((unsigned long long)DS2 | ((unsigned long long)DS1 << 32));
        long r_ = lseek((int)DS0, (long)off_, SEEK_SET);
        dsp += 2 * CELL_BYTES;
        DS0 = (r_ < 0) ? 200 : 0;
    }
    NEXT();
    }
L_filepos: {/* fid --- ud ior */
    /*  ANS: ( fileid -- ud ior ) - a double, low cell under the high one.
     *  It returned one cell until the Forth 2012 file tests said so;
     *  nothing in Forth calls it (Iteration 125; RelF: the same fault and
     *  fix). */
    t_fdrop((int)DS0);
    {   long p_ = lseek((int)DS0, 0, SEEK_CUR);
        unsigned long long q_ = (unsigned long long)p_;
        dsp -= 2 * CELL_BYTES;
        if (p_ < 0) { DS2 = 0; DS1 = 0; DS0 = 200; }
        else { DS2 = (UNS64)q_; DS1 = (UNS64)(CELL_BYTES == 8 ? 0ULL : (q_ >> 32)); DS0 = 0; }
    }
    NEXT();
    }
L_delfile: { /* c-addr u --- ior */
    t = BYTE(DS1 + DS0);
    BYTE(DS1 + DS0) = 0;
    {   /* the byte back first, then the result (Iteration 124: storing the
           result first restored the byte at result + u - a segfault, always) */
        int r_ = unlink((char*)(uintptr_t)DS1);
        BYTE(DS1 + DS0) = t;
        DS1 = (UNS64)r_;
    }
    dsp += CELL_BYTES;
    NEXT();
}
L_filesize: { /* fid --- ud ior */
    /*  ANS: ( fileid -- ud ior ), a double - see L_filepos; the ior 200
     *  where the size cannot be had, not always 0 (Iteration 125). */
    t_fdrop((int)DS0);
    int fd = (int)DS0;
    long cur = lseek(fd, 0, SEEK_CUR), size = -1;
    if (cur >= 0) { size = lseek(fd, 0, SEEK_END); lseek(fd, cur, SEEK_SET); }
    {   unsigned long long q_ = (unsigned long long)size;
        dsp -= 2 * CELL_BYTES;
        if (size < 0) { DS2 = 0; DS1 = 0; DS0 = 200; }
        else { DS2 = (UNS64)q_; DS1 = (UNS64)(CELL_BYTES == 8 ? 0ULL : (q_ >> 32)); DS0 = 0; }
    }
    NEXT();
}
/*
 *  Process-control primitives (shell support). Callers are responsible
 *  for NUL-terminating any string these pass to libc (matching the
 *  existing OPEN-FILE/DELETE-FILE/SYSTEM convention above - none of
 *  these do their own save/restore-a-byte trick, since the strings
 *  they're given - paths, argv entries, env names/values - are usually
 *  already being built fresh in a scratch buffer, not sliced out of
 *  live source text the way OPEN-FILE's c-addr/u pair typically is).
 */
#if SYSC
/* The gene sysc (Iteration 133): one system call in FORK's place, the shell's
 * process and environment words written in Forth on it (forth/shell-sysc.4);
 * the other seventeen of them gone. ( block num --- r ): the six arguments in
 * the block, r the kernel's result - on failure -errno (Iteration 141: the
 * shell can tell EINTR from ENOENT; the runtime's syscall gives -1 and errno);
 * num -1, -2, -3: argc, argv, the initial environment - what no call returns. */
L_syscall: {
    long num = (long)(INT64)DS0, r;
    const UNS64 *a = (const UNS64 *)(uintptr_t)DS1;
    t_flush();
#if FSYS
    /*  -4 (Iteration 202): fid a[0]'s read-ahead dropped, as the native READ-FILE
     *  and the positioning words did first - file-sysc.4's need it: READ-LINE,
     *  native, reads ahead.  */
    if (num == -4) { t_fdrop((int)a[0]); r = 0; } else
#endif
#if FSYS >= 4
    if (num == -5) { g_fbuf = (UNS64 *)(uintptr_t)a[0]; r = 0; } else   /* the Forth output buffer registered */
    if (num == -6) r = 0; else                                          /* a flush: done on entry, above */
#endif
    if (num < 0) r = num == -1 ? (long)g_argc : num == -2 ? (long)(uintptr_t)g_argv : num == -3 ? (long)(uintptr_t)environ : -1;
    else {
        if (num == 60 || num == 231) { PROFDUMP; }
#if defined(__i386__) || defined(__arm__)
        if (num == 9) {                                        /* Iteration 325: mmap, as mmap2 under the C library */
            void *m_ = mmap((void *)(uintptr_t)a[0], (size_t)a[1], (int)a[2], (int)a[3], (int)a[4], (off_t)a[5]);
            r = m_ == MAP_FAILED ? -1 : (long)(uintptr_t)m_;   /* Iteration 400: no local label - gen-tail.py took */
        } else if ((num = sysc_i386(num)) < 0) r = -38;        /* sysc_done for a handler. ENOSYS */
        else
#endif
        r = syscall(num, (long)a[0], (long)a[1], (long)a[2], (long)a[3], (long)a[4], (long)a[5]);
        if (r == -1) r = -(long)errno;
    }
    DS1 = (UNS64)(INT64)r;
    dsp += CELL_BYTES;
    NEXT();
}
L_nosys:   /* a primitive the gene sysc removed: the shell's are Forth now */
    t_flush(); _exit(70);
#endif
#if !SYSC
L_fork: /* --- pid */
     t_flush();PUSH((UNS64)(INT64)fork());
    NEXT();
#endif /* !SYSC */
#if !SYSC
L_execve: { t_flush(); /* argv-addr path-addr --- ior */
    char *path = (char*)(uintptr_t)DS0;
    char **argv = (char**)(uintptr_t)DS1;
    execve(path, argv, environ);
    /* only reached if execve itself failed */
    DS1 = (UNS64)200;
    dsp += CELL_BYTES;
    NEXT();
}
#endif /* !SYSC */
#if !SYSC
L_waitpid: { /* pid --- status ior */
    int status = 0;
    pid_t r = waitpid((pid_t)(INT64)DS0, &status, 0);
    if (r < 0) {
        DS0 = (UNS64)(INT64)-1;
        PUSH(200);
    } else {
        DS0 = (UNS64)(INT64)status;
        PUSH(0);
    }
    NEXT();
}
#endif /* !SYSC */
#if !SYSC
L_pipe: { /* --- fd-read fd-write ior */
    int fds[2];
    if (pipe(fds) < 0) {
        PUSH(0); PUSH(0); PUSH(200);
    } else {
        PUSH((UNS64)fds[0]); PUSH((UNS64)fds[1]); PUSH(0);
    }
    NEXT();
}
#endif /* !SYSC */
#if !SYSC
L_dup2: /* oldfd newfd --- ior */
    DS1 = (UNS64)((dup2((int)DS1, (int)DS0) < 0) ? 200 : 0);
    dsp += CELL_BYTES;
    NEXT();
#endif /* !SYSC */
#if !SYSC
L_getenv: { /* c-addr --- addr */
    char *v = getenv((char*)(uintptr_t)DS0);
    DS0 = (UNS64)(uintptr_t)v;
    NEXT();
}
#endif /* !SYSC */
#if !SYSC
L_setenv: /* value-addr name-addr --- ior */
    DS1 = (UNS64)((setenv((char*)(uintptr_t)DS0, (char*)(uintptr_t)DS1, 1) < 0) ? 200 : 0);
    dsp += CELL_BYTES;
    NEXT();
#endif /* !SYSC */
#if !SYSC
L_sysexit: /* n --- */
     t_flush();PROFDUMP; _exit((int)DS0);
#endif /* !SYSC */
#if !SYSC
L_chdir: /* c-addr --- ior */
    DS0 = (UNS64)((chdir((char*)(uintptr_t)DS0) < 0) ? 200 : 0);
    NEXT();
#endif /* !SYSC */
#if !SYSC
L_getcwd: { /* addr max-len --- len ior */
    char *r = getcwd((char*)(uintptr_t)DS1, (size_t)DS0);
    if (r == 0) {
        DS1 = 0;
        DS0 = 200;
    } else {
        DS1 = (UNS64)strlen(r);
        DS0 = 0;
    }
    NEXT();
}
#endif /* !SYSC */
#if !SYSC
L_sysargc: /* --- n */
    PUSH((UNS64)(g_argc > 2 ? g_argc - 2 : 0));
    NEXT();
#endif /* !SYSC */
#if !SYSC
L_sysarg: { /* n --- c-addr */
    long n = (long)(INT64)DS0;
    if (n < 0 || n + 2 >= g_argc) {
        DS0 = 0;
    } else {
        DS0 = (UNS64)(uintptr_t)g_argv[n + 2];
    }
    NEXT();
}
#endif /* !SYSC */
#if !SYSC
L_getpwhome: { /* c-addr --- addr | 0 */
    /* A named user's home directory, via NSS rather than by reading
     * /etc/passwd. That file is one NSS source among several: on a
     * host using LDAP, SSSD, NIS or systemd-homed a real user may not
     * appear in it at all, and "~alice" would quietly stay literal.
     * getpwnam(3) returns whatever the system is actually configured
     * to use. The returned string is in getpwnam's own static
     * storage, valid until the next call - the caller copies it
     * immediately. */
    struct passwd *pw = getpwnam((const char *)(uintptr_t)DS0);
    DS0 = pw ? (UNS64)(uintptr_t)pw->pw_dir : 0;
    NEXT();
}
#endif /* !SYSC */
#if !SYSC
L_getfsize: { /* --- n */
    /* RLIMIT_FSIZE's soft limit in POSIX's 512-byte blocks, or -1 for
     * unlimited. Blocks rather than bytes deliberately: POSIX specifies
     * ulimit in 512-byte units (which is where bash differs, reporting
     * 1024), and a byte count of a large limit does not fit a 4-byte
     * cell on a 32-bit build. File size is the only resource POSIX's
     * own ulimit covers, so this pair is narrow on purpose - see
     * GOALS.md goal 3. */
    struct rlimit rl;
    if (getrlimit(RLIMIT_FSIZE, &rl) < 0 || rl.rlim_cur == RLIM_INFINITY) {
        PUSH((UNS64)(INT64)-1);
    } else {
        PUSH((UNS64)(rl.rlim_cur / 512));
    }
    NEXT();
}
#endif /* !SYSC */
#if !SYSC
L_setfsize: { /* n --- ior */
    struct rlimit rl;
    INT64 n = (INT64)DS0;
    if (getrlimit(RLIMIT_FSIZE, &rl) < 0) {
        DS0 = (UNS64)202;
    } else {
        /* POSIX: with neither -H nor -S, ulimit sets the soft *and*
         * hard limit. Setting only rlim_cur left the hard limit
         * untouched, which /proc/self/limits reports in a second
         * column - caught by mrsh's ulimit.sh, whose last assertion
         * greps that line. */
        rl.rlim_cur = (n < 0) ? RLIM_INFINITY : (rlim_t)n * 512;
        rl.rlim_max = rl.rlim_cur;
        DS0 = (UNS64)((setrlimit(RLIMIT_FSIZE, &rl) < 0) ? 202 : 0);
    }
    NEXT();
}
#endif /* !SYSC */
#if !SYSC
L_getpid: /* --- pid */
    PUSH((UNS64)(INT64)getpid());
    NEXT();
#endif /* !SYSC */
#if !SYSC
L_unsetenv: /* c-addr --- ior */
    DS0 = (UNS64)((unsetenv((char*)(uintptr_t)DS0) < 0) ? 200 : 0);
    NEXT();

/*
 *  ALLOCATE / FREE / RESIZE - the standard Forth-2012 memory-allocation
 *  wordset, backed by libc. This is memory OUTSIDE the image: it lives
 *  in the C heap, not in the VM's own mem[] region, so it does not
 *  consume dictionary space and is not written out by save-system.4's
 *  SAVE-SYSTEM.
 *
 *  The addresses handed back are absolute and process-local. They are
 *  therefore NOT valid across a save/reload, which is why buffer
 *  pointers are reset before an image is written - see pool.4.
 */
#endif /* !SYSC */
L_allocate: /* u --- a-addr ior */
{
    void *p = malloc((size_t)DS0);
    DS0 = (UNS64)(uintptr_t)p;
    PUSH((UNS64)(p == NULL ? 201 : 0));
    NEXT();
}
L_free: /* a-addr --- ior */
    free((void*)(uintptr_t)DS0);
    DS0 = 0;
    NEXT();
L_resize: /* a-addr u --- a-addr' ior */
{
    void *p = realloc((void*)(uintptr_t)DS1, (size_t)DS0);
    if (p == NULL) {
        /*  Forth-2012: on failure a-addr is unchanged and still valid,
         *  so the caller can carry on with the original block.  */
        DS0 = 202;
    } else {
        DS1 = (UNS64)(uintptr_t)p;
        DS0 = 0;
    }
    NEXT();
}
#if FOLD
#define EXITNEXT() do { ip = RS; rp += CELL_BYTES; NEXT(); } while (0)
#include "vm-fold-bodies.h"
#endif
#if SUPER
#include "vm-super-bodies.h"
#endif
#if OPCALL
/*  Iteration 121, the gene opcall: an operation and the call after it in one
 *  opcode (Koopman's op+CALL, results/docs-reuse.md). The operation's body,
 *  then straight into the call's code for its width - its first byte read,
 *  a compare, a direct jump - where NEXT would have gone through the table.
 *  Not counted as a dispatch by the profiler: it is not one.  */
#if T2WIDE
#define CALLNEXT() do { t = BYTE(ip); ip += 1; if (t >= 0xC0) goto L_t2call4; goto L_t2call2; } while (0)
#else
#define CALLNEXT() do { t = BYTE(ip); ip += 1; if (t >= 0xC0) goto L_t2call4; \
                        if (t >= 0x80) goto L_t2call3; goto L_t2call2; } while (0)
#endif
#include "vm-opcall-bodies.h"
#endif

}

/*
 *  Program entry point.
 */

int main(int argc, char **argv) {
#if defined(__i386__) || defined(__arm__)
    /*  Iteration 326: on a 32-bit host, the memory the image maps (ALLOCATE's mmap, RESIZE's
     *  mremap) below 2 GB: past it, a 4-byte cell holding the address is negative, and the file
     *  overlays test a system call's result with 0< (forth/file-sysc.4) - a good allocation read
     *  as a failure. Linux's legacy layout (setarch -L) maps bottom-up from 1 GB: set it and run
     *  again, once - an exec, not a new process. If the exec fails (qemu-arm without binfmt,
     *  whose guest maps low anyway), on as we are. A 64-bit engine is what it was.  */
    {   /* raw calls - 136 personality, 11 execve, the same on i386 and 32-bit ARM - as the
           C-library-less runtimes have neither wrapper; 0x0200000 is ADDR_COMPAT_LAYOUT */
        long p_ = syscall(136, 0xffffffffUL);
        if (p_ >= 0 && !(p_ & 0x0200000L) && syscall(136, (unsigned long)p_ | 0x0200000UL) >= 0)
            syscall(11, "/proc/self/exe", argv, environ);
    }
#endif
    if (argc < 2) {
        write_str(2, "Usage: relf <filename>\n");
        return 1;
    }
    g_argc = argc;
    g_argv = argv;
    load_image(argv[1]);
    g_ip = (UNS64)(uintptr_t)base;
    g_rp = STK_END;
#if GUARD
    install_guards(base);
    /*  Below the return stack's guard page, not below the return stack.
     *  TWO cells of slack, not one: with TOS caching dsp sits one cell
     *  ABOVE the logical top, so with one cell the empty stack would
     *  put dsp exactly on the guard and any NOS read would trap. */
    g_dsp = STK_END - RSTACK_BYTES - PAGE - 2 * CELL_BYTES
            - 64 * CELL_BYTES - DSKEW;   /* Iteration 119: slack for a shallow underflow -
                                    ?STACK reports it after the word, as without
                                    the guard ("Stack error DROP"); only a
                                    runaway one reaches the guard page */
#else
    install_fault_trap();
    g_dsp = STK_END - RSTACK_BYTES - CELL_BYTES - DSKEW;
#endif
    g_rp_limit  = STK_END - RSTACK_BYTES;
    g_dsp_limit = STK_END - RSTACK_BYTES - DSTACK_BYTES
#if GUARD
                  + PAGE
#endif
                  ;
    CELL(g_dsp) = g_ip;
    virtual_machine();
    return 0; /* unreachable: virtual_machine() only leaves via BYE/EOF */
}
