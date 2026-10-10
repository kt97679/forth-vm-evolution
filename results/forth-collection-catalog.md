# The owner's Forth collection, item by item (Iteration 119)

forth.tgz: 138 MB unpacked, 3,106 files. Every top-level item, what it is, its
licence where it matters, and how useful it is for THIS project:

- ★★★ use now - code or tests that can be used, or directly on the plan
- ★★ study - ideas or references for genes, the JIT, the instruction set
- ★ background - history, context, little direct use
- – no use here - binaries, unrelated applications, duplicates

Code can be taken only from public-domain or permissive sources and from the
owner's own work; from GPL ones (SOD32, gforth, bigFORTH, SP-Forth, ciforth,
C4th) ideas only.

## The twelve worth most

1. **anstests0.3.zip** ★★★ - the ANS test suite, now tests/ans and the
   held-out check (lab/evolve/ans-check.py); it found the stack-guard fault.
2. **relf_dev/relf-0.3** ★★★ - the owner's 2009 JIT base (below): the
   template-copy idea the project's JIT uses today.
3. **RelF/** ★★★ - RelF's history: the origin, opcode-chain statistics, the
   todo with primitive-set decisions, the VM in Forth.
4. **doc/Koopman** ★★★ - Stack Computers: instruction sets for stack
   machines, the reference for "an instruction set evolution builds".
5. **doc/Rodriguez (Moving Forth)** ★★★ - threading techniques measured, and
   CamelForth's source.
6. **PFTHPC19.ZIP** ★★★ - pForth (Phil Burk), PUBLIC DOMAIN: an ANS-like
   Forth in C, usable code and its tests.
7. **ficl202.zip** ★★★ - FICL 2.02 (John Sadler), freeware "use it in any
   way": a C Forth built for embedding.
8. **eforth/** ★★ - eForth's 31 primitives (only UM+ for arithmetic): a floor
   for the primitive-set search.
9. **ioccc/** ★★ - FIRST and THIRD: a Forth grown from about a dozen
   primitives in under 800 bytes of C - the smallest floor.
10. **forth_3.zip** ★★ - strongForth: a STATICALLY TYPED Forth; stack-effect
    checking could guard genetic improvement's edits.
11. **relf_dev/gforth-0.6.2** ★★ (GPL) - vmgen, its superinstruction lists
    (super2.i) and peephole rules (peeprules.vmg).
12. **spf4/** ★★ (GPL) - SP-Forth 4: macroopt.f, a peephole optimizer for
    native code, and spf_inline.f, an inliner - ideas for the JIT.

## The owner's own work

| item | what it is | use |
|---|---|---|
| RelF/ | RelF 0.1-0.3 releases; stat/ (word and opcode-pair statistics, Perl tools); todo (CP866: = as a primitive - done; - and DOVAR as primitives; D+ in Forth, with its definition); vmll.4 and vmhl.4 - the VM written in Forth for SP-Forth (low- and high-level); com/ - a DOS .COM build in assembler; eforth/eforth.prims - eForth's primitive list; bench/ - ackermann, bubble, sieve, fib; ASM/ and EXT/ - SP-Forth's assembler and CASE; Relf.f, test.4, words.txt, sockets.txt; SPF3.EXE (binary) | ★★★ history, statistics, the primitive-set ideas |
| relf_dev/ | the development tree. relf01, relf-0.2, relf-0.3 (2009): **the JIT base** - t1.asm copies precompiled x86 snippets per opcode into a buffer and runs it (copy-and-patch, the stencil idea), t3.asm copies a code block and calls it, relf2.c pre-decodes threaded code into a table of handler pointers (codedata, codeindx, vmupdatecode, vmdonext), relf1.c a call encoding and tracing (log is a trace); vm.asm and vm_tos.asm - NASM VMs, the second with a cached top of stack; relfgcc.c - computed goto. Also sod32/ (SOD32, GPL v2), spf/ (SP-Forth 3 for Linux, GPL), gforth-0.6.2/ (full source, GPL), bench/, and tarballs of the same | ★★★ the JIT base and the engines' history |
| small/ | the SOD32 package (GPL v2) and the owner's analysis of which words the kernel uses (kernel/process.sh, kernel-words, words-defined-in-kernel.4, cross-kernel-words) | ★★ the kernel's word usage |
| SnailForth/ | SOD32's engine (GPL v2) and the owner's 2013 assembly port (SnailForth.asm, .lst), with test programs (exit-42.4, terminal.4) | ★★ |
| itsy/ | Itsy Forth (John Metcalf's tiny DOS Forth), the owner's Linux port (itsy-linux.asm, 2013) and a subroutine-threaded variant (stc/) | ★★ a minimal native Forth |
| src/ | the owner's programs: crc.4, LZSS (lzss.fo, lzss.doc), BASIC.4TH (a BASIC interpreter in Forth), bot1-9, bota, botb (bots), dreams.4, dynmem_4th.txt (dynamic memory), XanHash.seq, SYSTEM.F32 | ★ candidate workloads (BASIC, LZSS, CRC: real programs) |
| bench.txt | RelF's benchmark results across FreeBSD versions | ★ |
| sod/ | SOD32 by L.C. Benschop, two versions, and ENGINE.SOD (sod32ll.4, sod32hl.4 - SOD32's simulator in Forth); GPL v2 | ★★ the origin (ideas only) |

## Tests and benchmarks

| item | what it is | use |
|---|---|---|
| anstests0.3.zip | ANS test suite 0.3 (Gerry Jackson 2006-07, around John Hayes's core.fr); freely distributable with the notice | ★★★ added: tests/ans |
| bench/ | Benchmark.html and bench.zip - a collection of Forth benchmarks | ★★ execution-heavy workloads |
| RelF/bench, relf_dev/bench | ackermann (deep recursion), bubble (memory, loops), sieve, fib | ★★ execution-heavy workloads |

## Minimal and historic Forths - floors for the instruction-set search

| item | what it is | use |
|---|---|---|
| eforth/, eforth.zip | eForth 1.0 (C.H. Ting, Bill Muench, 1990): EFORTH.SRC/ASM, glossary, 86eForth | ★★ the 31-primitive core |
| eforth.tar.bz2 | lx-eforth: eForth for Linux (hp, 2001) | ★ |
| e4a.src.tar.bz2 | eForth for Linux/i586 (Andy Valencia's port) | ★ |
| ioccc/, ioccc.rar | buzzard.2 (IOCCC): FIRST and THIRD, with the design notes; the same twice | ★★ |
| 3ins4th.htm, 3ins4th.zip | Frank Sergeant's 3-instruction Forth for the 68HC11: the target needs only fetch, store and call; the host does the rest | ★★ the smallest target |
| cmforth.zip | Chuck Moore's cmFORTH (FORTHkit 1986) for the Novix NC4000 | ★★ minimalism, a compiler for a stack CPU |
| colorforth/, color.zip | colorForth: Moore's site (32 MB), its assembler sources and blocks, a Windows port | ★ |
| ok101.zip | OK for P21Forth (MuP21) | ★ |
| nforth.tgz | a tiny Forth in six files | ★ |
| Open Source - 8086 Forth 83 2.1.0 | F83 (Laxen and Perry), public domain, metacompiled | ★★ a classic, well-commented kernel |
| Haydon - MVP Forth 1.0305.02 | MVP-FORTH (1982), fig-derived | ★ |
| fig86g2d148.zip, ci86g3d275.zip, wna4d0d6.zip | Albert van der Horst's fig86 and ciforth, one source generated by m4 for many targets; GPL | ★★ ideas: one source, many builds |

## Virtual machines and portable C Forths

| item | what it is | use |
|---|---|---|
| PFTHPC19.ZIP | pForth v19, public domain, ANS-like, in C | ★★★ code usable |
| ficl202.zip | FICL 2.02, freeware | ★★★ code usable |
| beetle.zip | Beetle (Reuben Thomas): a portable Forth virtual machine in C (release 2); licence to check | ★★ VM design |
| FVM0217.RAR | FVM: a tiny Forth VM (C++) with a target compiler in Forth (tc.4th) and Python tools | ★★ |
| forth.rar | a Forth in C, one file per word set (core, double, except, file, block) | ★★ |
| c-forth.zip | C-FORTH: a portable figFORTH in C | ★ |
| cforth.zip | "Portable Forth in C" | ★ |
| c4th100.zip | C4th 1.00, GPL | ★ |
| 6th.zip, SIXTH.LZH | Sixth (I.M. Wilson): a Forth-like in C; the same twice | ★ |
| bashforth.txt | a Forth written in bash | ★ |
| java/ | Forths in Java: jeForth, WebForth, FIJI and more | ★ |
| mfdoswin.zip | a Forth with a C kernel, .mf sources and a kernel image | ★ |
| nfsdk-0.0.2a.tar.gz | NF SDK: a Forth VM (nfvm.exe) and compiler (nfc.exe), binaries and kernel sources | ★ |

## Optimizing and native-code Forths - ideas for the JIT

| item | what it is | use |
|---|---|---|
| spf4/ | SP-Forth 4 source (GPL): macroopt.f (peephole optimizer), spf_inline.f (inliner), compiler/ | ★★ |
| relf_dev/spf | SP-Forth 3 for Linux, source (GPL) | ★★ |
| relf_dev/gforth-0.6.2 | gforth 0.6.2 (GPL): vmgen, super2.i, peeprules.vmg, engine/ | ★★ |
| bigforth/ | bigFORTH and the MINOS GUI (Bernd Paysan, GPL): native code | ★ |
| isforth-1.14b.tar.tar | IsForth (Mark Manning): Linux x86 assembler Forth | ★ |
| F386.rar | a bootable 386 Forth with Python tools | ★ |
| F386V10.ZIP | MB&WW Forth for MSDOS | ★ |

## Typed, object-oriented and structured extensions

| item | what it is | use |
|---|---|---|
| forth_3.zip | strongForth 0.03 (Stephan Becher): statically typed | ★★ stack-effect checking |
| objects.zip | Anton Ertl's structures and objects packages | ★ |
| CLASS10.ZIP, OOPS.RAR, POLYOBJ.RAR, UR-OBJS1.RAR | object systems for Forth | – |
| day.zip | an OOP engine for SP-Forth 3.70 | – |

## Systems, applications and examples

| item | what it is | use |
|---|---|---|
| ALEFTH.RAR | a Forth system written in Forth, on blocks (COMPILER, CONTROL, BOOT ...) | ★ |
| aforth.zip | a Forth written in Forth, with its RCS history | ★ |
| angel.tgz | "angel": a small Forth in assembler and C | ★ |
| Forthish.zip | 4THICE, rev .23 | ★ |
| Forth.Compiler.1.0.zip | BBL Forth: reference and blocks | ★ |
| myforth.zip | a small Forth package | ★ |
| maf1v02.zip, paf0v04.zip | Chris Jakeman, 1996: F-PC sources (.seq) | ★ |
| ffpdp.zip | a PDP-11 Forth environment and a terminal emulator | ★ |
| fprimer.zip | a Forth primer with F-PC 3.56 and eForth86 | ★ |
| Zimmer - Forth 8.11 | Tom Zimmer's F-PC sources (.seq) and help | ★ |
| FDDBootOS3.rar, fddbootos3.imz | a Forth OS booting from a floppy (Mihail Maksimov) | ★ |
| forthimage.img.gz | a disk image | – |
| forth.cx.tgz | the forth.cx website: articles | ★ |
| PMForth/, PMforth12.zip, Pmfv1.rar | PMForth for DOS | – |
| larionov.zip | Golden Porcupine Forth (1991) | – |
| BetaForth.rar | a DOS Forth: binaries and screens | – |
| pf.zip | the STEALTH group's Forth (assembler) | – |
| aclock.zip, units.zip | SP-Forth examples | – |
| FOODFTH.RAR | French example programs | – |
| frts.zip | FRTScript, a scripting system | – |
| forth_1.zip | a Flash-Forth primer | – |
| aztec.zip | Aztec Forth, binary | – |
| t32distr.rar | T32 Forth for DOS/Windows: binaries and help | – |
| kfwin10.zip | KForth, binary | – |
| LinuxSPF_6_win32.rar | SP-Forth test files and a binary | – |
| 6.08.00.exe, spf4-014.exe, spf4-19-setup.exe, spf4/jpf375c.exe | installers | – |
| 4T.HA, FORTH.HA | HA archives - no extractor available here | ? |
| dssp/ | DSSP (Moscow State University's Dialogue System for Structured Programming, heir of the Setun's software): website mirror, sources, papers | ★ another stack language's design |

## Documentation (doc/, 52 MB)

| item | what it is | use |
|---|---|---|
| Koopman/ | Stack Computers: the new wave (English and Russian) | ★★★ |
| Rodriguez/Moving Forth | threading compared; CamelForth Z80 source (camel80*.txt) | ★★★ |
| Optimal Code Generation For Stack Machines.pdf | stack scheduling | ★★ the JIT, register caching |
| Threading in forth.txt | threading techniques | ★★ |
| Knaggs/ | P.J. Knaggs's thesis: practical and theoretical aspects of Forth development - stack-effect algebra | ★★ |
| ANSI/, ANSI X3.215-1993 draft, the .chm | the ANS standard (English, Russian) | ★★ |
| Baranov/, Язык Форт и его реализации | Baranov's "Forth and its implementations" | ★★ implementation techniques |
| Brodie/ | Starting Forth, Thinking Forth (English, Russian) | ★ |
| Burk/ | pForth reference, tutorial, FAQ | ★ |
| Pelc/, Bezemer, Noble/, Charlton/, Technoforth/ | books and tutorials | ★ |
| Semenov/, Tarasov/, Kelly/, Ponyatov/, Gritsenko/, Gassanenko/, Cherezov/ | Russian books and papers (Gassanenko: backtracking in Forth; Cherezov: ideas) | ★ |
| forthwrite/ | the FIG UK magazine, issues 105-127 | ★ |
| FORTH.4ME, 102-Forth-Paper.pdf, 225-Forth-Slides.pdf | papers and slides | ★ |
