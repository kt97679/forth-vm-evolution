# The owner's Forth collection, kept (Iteration 213)

From forth.tgz (uploaded 2026-10-10; 138 MB, 3,106 files; cataloged item by
item in results/forth-collection-catalog.md). Kept here so the archive need
not be uploaded again: what the project uses or plans to, within the licence
policy (results/forth-collection-catalog.md) - code only from public-domain or
permissive sources and the owner's own work; GPL sources ideas only.

| here | from forth.tgz | licence | why |
|---|---|---|---|
| relf_dev/relf01, relf-0.2, relf-0.3 | relf_dev/ | the owner's | the 2009 JIT base: t1.asm copy-and-patch per opcode (the stencil idea), RelF's VM |
| relf_dev/bench | relf_dev/bench | - | the benchmarks bench/ was taken from |
| RelF/ | RelF/ | the owner's | RelF 0.1-0.3, stat/ (word and opcode-pair statistics, Perl), todo, vmll.4 and vmhl.4 (the VM in Forth) |
| small/kernel/ | small/kernel/ | the owner's | which words SOD32's kernel uses (process.sh, kernel-words, words-defined-in-kernel.4, cross-kernel-words) - the SOD32 package beside it is GPL, not kept |
| SnailForth/ | SnailForth/ | the owner's port of SOD32's engine (GPL v2 by descent) | SnailForth.asm and .lst (2013), its C, Makefile, test programs - SOD32's own files not kept |
| itsy/ | itsy/ | Itsy Forth (John Metcalf) and the owner's Linux port | a minimal native Forth; a subroutine-threaded variant (stc/) |
| eforth/ | eforth/ | eForth 1.0 (Ting, Muench), freely distributed | the 31-primitive core - a floor for moving primitives to Forth |
| ioccc/ | ioccc/ | IOCCC buzzard.2 | FIRST and THIRD: a Forth grown from a dozen primitives |
| bench/ | bench/ | various | Benchmark.html, bench.zip - more execution-heavy workloads |
| PFTHPC19.ZIP | the same | pForth v19, public domain | ANS-like Forth in C - code usable |
| ficl202.zip | the same | FICL 2.02, freeware | code usable |
| 3ins4th.zip, 3ins4th.htm | the same | Frank Sergeant | the 3-instruction target: fetch, store, call |
| cmforth.zip | the same | Chuck Moore, cmFORTH | minimalism; a compiler for a stack CPU |
| beetle.zip | the same | Reuben Thomas - licence to check | a portable Forth VM in C |
| forth_3.zip | the same | strongForth - licence to check | static stack-effect typing |
| colorforth-chars.md | colorforth/www.colorforth.com/chars.html | facts, noted | colorForth's packed-name encoding, for the packed-names gene |

Not kept, and where to find them if needed: colorForth (33 MB, mostly
binaries and images - colorforth.com; the encoding is in colorforth-chars.md);
SOD32 (GPL - the origin, ideas only; L.C. Benschop's site); gforth 0.6.2 (GPL -
vmgen's superinstruction lists; gnu.org); SP-Forth 4 (GPL - macroopt.f, its
peephole optimizer; spf.sourceforge.net); bigFORTH, ciforth (GPL); the doc/
books - Koopman's Stack Computers (free online, Koopman's CMU pages) and
Rodriguez's Moving Forth (bradrodriguez.com); DOS and Windows binaries;
duplicates. The catalog and results/forth-sources.md, results/docs-reuse.md
hold what each was read for.
